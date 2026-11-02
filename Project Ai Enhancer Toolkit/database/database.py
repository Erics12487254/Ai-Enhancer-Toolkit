
import sqlite3
from contextlib import contextmanager
from pathlib import Path


class ImageDatabase:
    """Manage database operations for the image gallery."""

    def __init__(self, database_path=None):
        self.database_path = (
            Path(database_path)
            if database_path is not None
            else Path(__file__).resolve().parent / "gallery.db"
        )

    @contextmanager
    def get_connection(self):
        """Create a database connection and manage its transaction."""

        connection = sqlite3.connect(
            self.database_path,
            timeout=10
        )

        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 10000")

        try:
            yield connection
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def initialize_database(self):
        """Create the database table and apply necessary migrations."""

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.get_connection() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    output_name TEXT NOT NULL,
                    output_path TEXT NOT NULL UNIQUE,
                    staging_path TEXT,
                    operation TEXT NOT NULL,
                    model TEXT,
                    width INTEGER NOT NULL,
                    height INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (
                        strftime('%Y-%m-%dT%H:%M:%f', 'now', 'localtime')
                    ),
                    settings TEXT,
                    status TEXT NOT NULL DEFAULT 'pending'
                        CHECK (
                            status IN ('pending', 'ready', 'deleting')
                        )
                )
            """)

            # Check whether an older database needs the staging_path column.
            columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(images)"
                )
            }

            if "staging_path" not in columns:
                connection.execute("""
                    ALTER TABLE images
                    ADD COLUMN staging_path TEXT
                """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_images_status_created
                ON images(status, created_at)
            """)

    def add_image(
        self,
        output_name,
        output_path,
        operation,
        width,
        height,
        staging_path=None,
        model=None,
        settings=None
    ):
        """Register a processed image and return its database ID."""

        with self.get_connection() as connection:

            cursor = connection.execute("""
                INSERT INTO images (
                    output_name,
                    output_path,
                    staging_path,
                    operation,
                    model,
                    width,
                    height,
                    settings
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                output_name,
                str(output_path),
                str(staging_path) if staging_path else None,
                operation,
                model,
                width,
                height,
                settings
            ))

            return cursor.lastrowid

    def update_image_status(self, image_id, status):
        """Update an image's storage status."""

        if status not in ("pending", "ready", "deleting"):
            raise ValueError("Invalid image status.")

        with self.get_connection() as connection:

            if status == "ready":
                cursor = connection.execute("""
                    UPDATE images
                    SET status = ?, staging_path = NULL
                    WHERE id = ?
                """, (status, image_id))

            else:
                cursor = connection.execute("""
                    UPDATE images
                    SET status = ?
                    WHERE id = ?
                """, (status, image_id))

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Image record {image_id} was not found."
                )

    def get_images(self):
        """Return all ready images, newest first."""

        with self.get_connection() as connection:

            cursor = connection.execute("""
                SELECT
                    id,
                    output_name,
                    output_path,
                    operation,
                    width,
                    height,
                    created_at,
                    settings
                FROM images
                WHERE status = 'ready'
                ORDER BY created_at DESC, id DESC
            """)

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

    def get_image(self, image_id):
        """Retrieve one image record by its ID."""

        with self.get_connection() as connection:

            cursor = connection.execute("""
                SELECT *
                FROM images
                WHERE id = ?
            """, (image_id,))

            row = cursor.fetchone()

            return dict(row) if row else None

    def get_pending_images(self):
        """Retrieve images waiting for their staged files to be published."""

        with self.get_connection() as connection:

            cursor = connection.execute("""
                SELECT id, output_path, staging_path
                FROM images
                WHERE status = 'pending'
            """)

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

    def mark_expired_images(self):
        """Mark ready images older than 30 days for deletion."""

        with self.get_connection() as connection:

            connection.execute("""
                UPDATE images
                SET status = 'deleting'
                WHERE status = 'ready'
                  AND julianday(created_at) <=
                      julianday('now', 'localtime', '-30 days')
            """)

            cursor = connection.execute("""
                SELECT id, output_path
                FROM images
                WHERE status = 'deleting'
            """)

            return [
                (row["id"], row["output_path"])
                for row in cursor.fetchall()
            ]

    def delete_image_record(self, image_id):
        """Delete an image's database record."""

        with self.get_connection() as connection:

            cursor = connection.execute("""
                DELETE FROM images
                WHERE id = ?
            """, (image_id,))

            if cursor.rowcount == 0:
                raise ValueError(
                    f"Image record {image_id} was not found."
                )

    def synchronize_images(self):
        """
        Remove records for missing permanent image files.

        Pending records are excluded because recovery handles them.
        """

        with self.get_connection() as connection:

            cursor = connection.execute("""
                SELECT id, output_path
                FROM images
                WHERE status IN ('ready', 'deleting')
            """)

            records = cursor.fetchall()

            for record in records:

                if not Path(record["output_path"]).is_file():
                    connection.execute("""
                        DELETE FROM images
                        WHERE id = ?
                    """, (record["id"],))
