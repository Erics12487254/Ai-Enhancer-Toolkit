
import base64
import sqlite3
import tkinter as tk
from pathlib import Path

import cv2

from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

from main import (
    OPERATIONS,
    process_image,
    validate_input,
    initialize_app,
    run_maintenance,
    get_gallery_images,
    download_image,
    delete_image
)


class ToolkitGUI:

    def __init__(self, root):
        self.root = root
        self.image_path = None

        self.operation = tk.StringVar(
            master=self.root,
            value="Choose an operation"
        )

        # Keep references to thumbnail images.
        self.thumbnail_images = []

        self._configure_window()
        self._build_interface()
        self.refresh_gallery()

        # Run maintenance every hour while the GUI is open.
        self.root.after(
            60 * 60 * 1000,
            self.run_periodic_maintenance
        )

    def _configure_window(self):
        """Configure the main application window."""

        self.root.title("AI Enhancer Toolkit")
        self.root.geometry("1050x800")
        self.root.minsize(800, 600)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _build_interface(self):
        """Build the image input area and gallery."""

        # ---------------- IMAGE INPUT ----------------

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.drop_area = tk.Label(
            self.main_frame,
            text="Drag an image here!",
            relief="ridge",
            width=40,
            height=8,
            wraplength=350
        )

        self.drop_area.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind(
            "<<Drop>>",
            self.on_drop
        )

        # ---------------- OPERATION CONTROLS ----------------

        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.operation_menu = tk.OptionMenu(
            self.control_frame,
            self.operation,
            *OPERATIONS.keys()
        )

        self.operation_menu.pack(pady=10)

        self.process_button = tk.Button(
            self.control_frame,
            text="Process image",
            command=self.process_selected_image
        )

        self.process_button.pack(pady=10)

        # ---------------- GALLERY ----------------

        self.gallery_frame = tk.LabelFrame(
            self.root,
            text="Processed Images",
            padx=10,
            pady=10
        )

        self.gallery_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.gallery_frame.grid_rowconfigure(0, weight=1)
        self.gallery_frame.grid_columnconfigure(0, weight=1)

        self.gallery_canvas = tk.Canvas(
            self.gallery_frame,
            highlightthickness=0
        )

        self.gallery_scrollbar = tk.Scrollbar(
            self.gallery_frame,
            orient="vertical",
            command=self.gallery_canvas.yview
        )

        self.gallery_canvas.configure(
            yscrollcommand=self.gallery_scrollbar.set
        )

        self.gallery_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.gallery_canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.gallery_inner = tk.Frame(
            self.gallery_canvas
        )

        self.gallery_window = self.gallery_canvas.create_window(
            (0, 0),
            window=self.gallery_inner,
            anchor="nw"
        )

        self.gallery_inner.bind(
            "<Configure>",
            self._update_scroll_region
        )

        self.gallery_canvas.bind(
            "<Configure>",
            self._resize_gallery_inner
        )

    def _update_scroll_region(self, event=None):
        """Update the scrollable gallery area."""

        self.gallery_canvas.configure(
            scrollregion=self.gallery_canvas.bbox("all")
        )

    def _resize_gallery_inner(self, event):
        """Make the gallery content fit the canvas width."""

        self.gallery_canvas.itemconfigure(
            self.gallery_window,
            width=event.width
        )

    # ---------------- IMAGE INPUT ----------------

    def on_drop(self, event):
        """Receive an image dropped into the application."""

        paths = self.root.tk.splitlist(event.data)

        if paths:
            self._select_image(paths[0])

    def _select_image(self, path):
        """Validate the selected image."""

        try:
            self.image_path = validate_input(path)

        except (ValueError, OSError) as error:
            self.image_path = None

            self.drop_area.config(
                text=f"Invalid image:\n{error}"
            )

            return

        self.drop_area.config(
            text=f"Selected image:\n{self.image_path}"
        )

    # ---------------- IMAGE PROCESSING ----------------

    def process_selected_image(self):
        """Process and save the selected image."""

        if self.image_path is None:
            self.drop_area.config(
                text="Please select an image first."
            )
            return

        try:
            output_path = process_image(
                self.image_path,
                self.operation.get()
            )

        except (
            ValueError,
            OSError,
            RuntimeError,
            sqlite3.Error,
            cv2.error
        ) as error:

            self.drop_area.config(
                text=f"Could not process image:\n{error}"
            )

            return

        self.drop_area.config(
            text=f"Image saved successfully!\n{output_path}"
        )

        # Display the newly processed image.
        self.refresh_gallery()

    # ---------------- GALLERY ----------------

    def refresh_gallery(self):
        """Retrieve database records and rebuild the gallery."""

        for widget in self.gallery_inner.winfo_children():
            widget.destroy()

        self.thumbnail_images.clear()

        try:
            images = get_gallery_images()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Gallery error",
                str(error)
            )
            return

        if not images:
            tk.Label(
                self.gallery_inner,
                text="No processed images yet."
            ).grid(
                row=0,
                column=0,
                padx=10,
                pady=20
            )

            return

        # Display three image cards per row.
        for index, record in enumerate(images):

            row = index // 3
            column = index % 3

            self._create_image_card(
                record,
                row,
                column
            )

    def _create_image_card(self, record, row, column):
        """Create one gallery card with its own actions."""

        card = tk.LabelFrame(
            self.gallery_inner,
            text=record["output_name"],
            padx=8,
            pady=8
        )

        card.grid(
            row=row,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        image_path = record["output_path"]

        # Load and create a thumbnail.
        image = cv2.imread(image_path)

        if image is not None:

            thumbnail = cv2.resize(
                image,
                (140, 100),
                interpolation=cv2.INTER_AREA
            )

            success, encoded_image = cv2.imencode(
                ".png",
                thumbnail
            )

            if success:

                image_data = base64.b64encode(
                    encoded_image.tobytes()
                ).decode("ascii")

                photo = tk.PhotoImage(
                    data=image_data
                )

                self.thumbnail_images.append(photo)

                tk.Label(
                    card,
                    image=photo
                ).pack(pady=5)

        else:

            tk.Label(
                card,
                text="Preview unavailable"
            ).pack(pady=5)

        # Display processing information.
        details = (
            f"Operation: {record['operation']}\n"
            f"Resolution: {record['width']} x {record['height']}\n"
            f"Created: {record['created_at']}"
        )

        tk.Label(
            card,
            text=details,
            justify="left",
            wraplength=200
        ).pack(pady=5)

        # Individual download button.
        tk.Button(
            card,
            text="Download",
            command=lambda item=record: self.download_selected_image(item)
        ).pack(fill="x", pady=2)

        # Individual delete button.
        tk.Button(
            card,
            text="Delete",
            command=lambda item=record: self.delete_selected_image(item)
        ).pack(fill="x", pady=2)

    # ---------------- DOWNLOAD ----------------

    def download_selected_image(self, record):
        """Let the user choose where to download an image."""

        destination = filedialog.asksaveasfilename(
            title="Download processed image",
            initialfile=record["output_name"],
            defaultextension=".jpg",
            filetypes=[
                ("JPEG images", "*.jpg"),
                ("PNG images", "*.png"),
                ("All files", "*.*")
            ]
        )

        if not destination:
            return

        try:
            download_image(
                record["id"],
                destination
            )

        except (ValueError, OSError, sqlite3.Error) as error:

            messagebox.showerror(
                "Download failed",
                str(error)
            )

            return

        messagebox.showinfo(
            "Download complete",
            f"Image downloaded to:\n{destination}"
        )

    # ---------------- DELETE ----------------

    def delete_selected_image(self, record):
        """Delete the selected image and its database record."""

        confirmed = messagebox.askyesno(
            "Delete image",
            f"Are you sure you want to delete {record['output_name']}?"
        )

        if not confirmed:
            return

        try:
            delete_image(record["id"])

        except (ValueError, OSError, sqlite3.Error) as error:

            messagebox.showerror(
                "Deletion failed",
                str(error)
            )

            return

        self.refresh_gallery()

    # ---------------- PERIODIC MAINTENANCE ----------------

    def run_periodic_maintenance(self):
        """Perform storage maintenance while the GUI is running."""

        try:
            run_maintenance()
            self.refresh_gallery()

        except (OSError, sqlite3.Error) as error:
            print(f"Periodic maintenance failed: {error}")

        finally:
            # Schedule another check in one hour.
            self.root.after(
                60 * 60 * 1000,
                self.run_periodic_maintenance
            )


# ---------------- APPLICATION ENTRY POINT ----------------

if __name__ == "__main__":

    root = TkinterDnD.Tk()

    try:
        # Initialize storage before building the gallery.
        initialize_app()

    except (OSError, sqlite3.Error) as error:

        messagebox.showerror(
            "Application startup failed",
            str(error),
            parent=root
        )

        root.destroy()
        raise SystemExit(1)

    app = ToolkitGUI(root)

    root.mainloop()
