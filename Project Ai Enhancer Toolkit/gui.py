# GUI workflow: receive an image, validate it through main.py, and let the user choose an operation.
import tkinter as tk

from tkinterdnd2 import DND_FILES, TkinterDnD

from main import process_image, validate_input


class ToolkitGUI:
    def __init__(self, root):
        self.root = root
        self.image_path = None
        self.operation = tk.StringVar(
            master=self.root,
            value="Choose an operation"
        )  # Stores the selected operation.

        self._configure_window()
        self._build_interface()

    def _configure_window(self):
        # Set the window title, starting size, minimum size, and resize behavior.
        self.root.title("Toolkit GUI")
        self.root.geometry("800x600")
        self.root.minsize(400, 500)
        self.root.resizable(True, True)

    def _build_interface(self):
        # Create the frame and input controls for the image workflow.
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.drop_area = tk.Label(
            self.main_frame,
            text="Drag an image here!",
            relief="ridge",
            width=40,
            height=8
        )
        self.drop_area.grid(row=0, column=0, padx=10, pady=10)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

        self.operation_menu = tk.OptionMenu(
            self.main_frame,
            self.operation,
            "Resize the image",
            "Enhance the image",
            "Crop the image",
            "Blur the image",
            "Sharpen the image"
        )
        self.operation_menu.grid(row=1, column=0, padx=10, pady=10)

        self.process_button = tk.Button(
            self.main_frame,
            text="Process image",
            command=self.process_selected_image
        )
        self.process_button.grid(row=2, column=0, padx=10, pady=10)

    # Handle a dropped file and ask main.py to validate it.
    def on_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        if paths:
            self._select_image(paths[0])

    # Keep a valid selection, or show the validation error from main.py.
    def _select_image(self, path):
        try:
            self.image_path = validate_input(path)
        except ValueError as error:
            self.image_path = None
            self.drop_area.config(text=f"Invalid image:\n{error}")
            return

        self.drop_area.config(text=f"Selected image:\n{self.image_path}")

    # Workflow: send the selected image and operation to main.py for processing and saving.
    def process_selected_image(self):
        try:
            output_path = process_image(self.image_path, self.operation.get())
        except (ValueError, OSError) as error:
            self.drop_area.config(text=f"Could not process image:\n{error}")
            return

        self.drop_area.config(text=f"Image saved successfully!\nSaved to: {output_path}")


# Start the GUI only when gui.py is launched directly.
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ToolkitGUI(root)
    root.mainloop()
