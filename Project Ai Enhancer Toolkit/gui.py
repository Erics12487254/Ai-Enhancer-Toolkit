import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

from main import OPERATIONS, create_application

from frontend.components.widgets import (
    create_button,
    create_scrollable_frame,
    create_gallery_card,
)

from frontend.operation_views.resize_view import create_resize_view


OPERATION_VIEWS = {
    "Resize the image": create_resize_view,
}


class ToolkitGUI:
    """Frontend orchestrator for the AI Enhancer Toolkit."""

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
        """Create the four main GUI sections."""

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame,
            text="AI Enhancer Toolkit",
            font=("Arial", 22, "bold"),
        ).pack(pady=(0, 15))

        self._build_image_input(main_frame)
        self._build_operation_selector(main_frame)
        self._build_operation_workspace(main_frame)
        self._build_gallery(main_frame)

    def _build_image_input(self, parent):
        """Section 1: Image input."""

        frame = tk.LabelFrame(
            parent,
            text="1. Image Input",
            padx=10,
            pady=10,
        )
        frame.pack(fill="x", pady=5)

        self.drop_area = tk.Label(
            frame,
            text="Drag and drop an image here or click to browse",
            relief="groove",
            borderwidth=2,
            height=3,
            font=("Arial", 11),
        )
        self.drop_area.pack(fill="x")

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)
        self.drop_area.bind(
            "<Button-1>",
            lambda event: self._browse_image(),
        )

        self.status_label = tk.Label(
            frame,
            text="No image selected.",
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=(5, 0))

    def _build_operation_selector(self, parent):
        """Section 2: Operation selector."""

        frame = tk.LabelFrame(
            parent,
            text="2. Select Operation",
            padx=10,
            pady=10,
        )
        frame.pack(fill="x", pady=5)

        self.operation_buttons = {}

        for operation in OPERATIONS:
            button = create_button(
                frame,
                operation,
                lambda selected=operation: self.select_operation(selected),
            )
            button.pack(side="left", padx=5)

            self.operation_buttons[operation] = button

    def _build_operation_workspace(self, parent):
        """Section 3: Dynamic operation workspace."""

        self.workspace = tk.LabelFrame(
            parent,
            text="3. Operation Workspace",
            padx=10,
            pady=10,
        )
        self.workspace.pack(fill="both", expand=True, pady=5)

        self.workspace_content = tk.Frame(self.workspace)
        self.workspace_content.pack(fill="both", expand=True)

        self.select_operation(self.operation.get())

    def select_operation(self, operation):
        """Display the selected operation interface."""

        self.operation.set(operation)

        for widget in self.workspace_content.winfo_children():
            widget.destroy()

        for name, button in self.operation_buttons.items():
            button.config(
                relief="sunken" if name == operation else "raised"
            )

        view_function = OPERATION_VIEWS.get(operation)

        if view_function:
            view_function(
                self.workspace_content,
                self._apply_operation,
            )

    def _apply_operation(self, settings):
        """Send operation requests to the application."""

        if not self.image_path:
            messagebox.showwarning(
                "No Image",
                "Please select an image first.",
            )
            return

        try:
            self.application.process_image(
                self.image_path,
                self.operation.get(),
                settings={
                    key: int(value)
                    for key, value in settings.items()
                },
            )

        except (ValueError, OSError, RuntimeError) as error:
            messagebox.showerror(
                "Operation failed",
                str(error),
            )
            return

        self.refresh_gallery()
        self.status_label.config(text="Operation completed successfully.")

        messagebox.showinfo(
            "Success",
            "Image processed successfully.",
        )

    def _build_gallery(self, parent):
        """Section 4: Saved image gallery."""

        frame = tk.LabelFrame(
            parent,
            text="4. Saved Gallery",
            padx=10,
            pady=10,
        )
        frame.pack(fill="both", expand=True, pady=5)

        self.gallery_frame = create_scrollable_frame(frame)

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
            create_gallery_card(
                self.gallery_frame,
                record,
                index // 3,
                index % 3,
                self.thumbnail_images,
                self._download_image,
                self._delete_image,
            )

    def _download_image(self, record):
        """Download a gallery image."""

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
        """Delete a gallery image after confirmation."""

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
