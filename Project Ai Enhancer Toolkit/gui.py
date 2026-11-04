import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD

from main import OPERATIONS, create_application


class ToolkitGUI:
    """Frontend for the AI Enhancer Toolkit."""

    def __init__(self, root):
        self.root = root
        self.root.title("AI Enhancer Toolkit")
        self.root.geometry("1000x750")
        self.root.minsize(750, 550)

        self.application = create_application()
        self.image_path = None
        self.thumbnail_images = []

        self.operation = tk.StringVar(value=next(iter(OPERATIONS)))

        self._build_interface()
        self.refresh_gallery()

    def _build_interface(self):
        """Create the application interface."""

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame,
            text="AI Enhancer Toolkit",
            font=("Arial", 22, "bold"),
        ).pack(pady=(0, 20))

        self.drop_area = tk.Label(
            main_frame,
            text="Drag and drop an image here\nor click to browse",
            relief="groove",
            borderwidth=2,
            height=5,
            font=("Arial", 12),
        )
        self.drop_area.pack(fill="x", pady=10)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)
        self.drop_area.bind(
            "<Button-1>",
            lambda event: self._browse_image(),
        )

        self.status_label = tk.Label(
            main_frame,
            text="No image selected.",
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=5)

        operation_frame = tk.Frame(main_frame)
        operation_frame.pack(fill="x", pady=10)

        tk.Label(operation_frame, text="Operation:").pack(
            side="left",
            padx=(0, 10),
        )

        tk.OptionMenu(
            operation_frame,
            self.operation,
            *OPERATIONS.keys(),
        ).pack(side="left")

        self.process_button = tk.Button(
            operation_frame,
            text="Process Image",
            command=self.process_selected_image,
        )
        self.process_button.pack(side="left", padx=15)

        tk.Label(
            main_frame,
            text="Saved Images",
            font=("Arial", 16, "bold"),
        ).pack(anchor="w", pady=(20, 10))

        self.gallery_canvas = tk.Canvas(
            main_frame,
            highlightthickness=0,
        )

        scrollbar = tk.Scrollbar(
            main_frame,
            orient="vertical",
            command=self.gallery_canvas.yview,
        )

        self.gallery_frame = tk.Frame(self.gallery_canvas)
        self.gallery_frame.bind(
            "<Configure>",
            lambda event: self.gallery_canvas.configure(
                scrollregion=self.gallery_canvas.bbox("all")
            ),
        )

        self.gallery_canvas.create_window(
            (0, 0),
            window=self.gallery_frame,
            anchor="nw",
        )
        self.gallery_canvas.configure(yscrollcommand=scrollbar.set)

        self.gallery_canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )
        scrollbar.pack(side="right", fill="y")

    def _browse_image(self):
        """Ask the user to select an image."""

        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("All files", "*.*"),
            ],
        )

        if path:
            self._select_image(path)

    def on_drop(self, event):
        """Handle an image dropped into the application."""

        paths = self.root.tk.splitlist(event.data)

        if paths:
            self._select_image(paths[0])

    def _select_image(self, path):
        """Validate and retain the selected image path."""

        try:
            self.application.validate_input(path)
        except (ValueError, OSError, RuntimeError) as error:
            self.image_path = None
            self.status_label.config(text=f"Invalid image: {error}")
            return

        self.image_path = path
        self.status_label.config(text=f"Selected: {path}")

    def process_selected_image(self):
        """Send the processing request to the application."""

        if not self.image_path:
            messagebox.showwarning(
                "No image selected",
                "Please select an image first.",
            )
            return

        try:
            output_path = self.application.process_image(
                self.image_path,
                self.operation.get(),
            )
        except (ValueError, OSError, RuntimeError) as error:
            self.status_label.config(text=f"Processing failed: {error}")
            messagebox.showerror("Processing failed", str(error))
            return

        self.status_label.config(text=f"Successfully saved: {output_path}")
        self.refresh_gallery()
        messagebox.showinfo(
            "Success",
            "Image processed and saved successfully.",
        )

    def refresh_gallery(self):
        """Display gallery records returned by the application."""

        for widget in self.gallery_frame.winfo_children():
            widget.destroy()

        self.thumbnail_images.clear()

        try:
            images = self.application.get_gallery_images()
        except (ValueError, OSError, RuntimeError) as error:
            self.status_label.config(text=f"Could not load gallery: {error}")
            return

        if not images:
            tk.Label(
                self.gallery_frame,
                text="No processed images yet.",
            ).grid(row=0, column=0, padx=10, pady=20)
            return

        for index, record in enumerate(images):
            self._create_image_card(
                record,
                index // 3,
                index % 3,
            )

    def _create_image_card(self, record, row, column):
        """Display one gallery record."""

        card = tk.Frame(
            self.gallery_frame,
            relief="groove",
            borderwidth=1,
            padx=10,
            pady=10,
        )
        card.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="n",
        )

        thumbnail_data = record.get("thumbnail_data")

        if thumbnail_data:
            photo = tk.PhotoImage(data=thumbnail_data)
            self.thumbnail_images.append(photo)
            tk.Label(card, image=photo).pack(pady=5)
        else:
            tk.Label(card, text="Preview unavailable").pack(pady=5)

        tk.Label(
            card,
            text=record["filename"],
            wraplength=160,
        ).pack(pady=5)

        width = record.get("width")
        height = record.get("height")
        resolution = (
            f"{width} × {height}"
            if width and height
            else "Unavailable"
        )

        tk.Label(card, text=f"Resolution: {resolution}").pack()

        created_at = datetime.fromtimestamp(
            record["created_at"]
        ).strftime("%Y-%m-%d %H:%M")

        tk.Label(card, text=f"Date: {created_at}").pack(pady=5)

        button_frame = tk.Frame(card)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Download",
            command=lambda item=record: self._download_image(item),
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="Delete",
            command=lambda item=record: self._delete_image(item),
        ).pack(side="left", padx=3)

    def _download_image(self, record):
        """Ask where to copy the selected gallery image."""

        destination = filedialog.asksaveasfilename(
            title="Download image",
            initialfile=record["filename"],
            defaultextension=".jpg",
            filetypes=[
                ("JPEG image", "*.jpg *.jpeg"),
                ("PNG image", "*.png"),
                ("All files", "*.*"),
            ],
        )

        if not destination:
            return

        try:
            self.application.download_image(
                record["path"],
                destination,
            )
        except (ValueError, OSError, RuntimeError) as error:
            messagebox.showerror("Download failed", str(error))
            return

        messagebox.showinfo(
            "Download complete",
            "Image downloaded successfully.",
        )

    def _delete_image(self, record):
        """Ask for confirmation, then delete the selected gallery image."""

        confirmed = messagebox.askyesno(
            "Delete image",
            f'Delete "{record["filename"]}"?',
        )

        if not confirmed:
            return

        try:
            self.application.delete_image(record["path"])
        except (ValueError, OSError, RuntimeError) as error:
            messagebox.showerror("Delete failed", str(error))
            return

        self.refresh_gallery()
        self.status_label.config(text=f'Deleted: {record["filename"]}')


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    ToolkitGUI(root)
    root.mainloop()