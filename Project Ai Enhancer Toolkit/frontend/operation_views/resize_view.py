
import tkinter as tk

from frontend.components.widgets import create_button


DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600


def create_resize_view(parent, on_apply):
    """Create the resize operation interface."""

    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="Width (px)",
    ).pack(pady=(15, 5))

    width_entry = tk.Entry(frame)
    width_entry.insert(0, str(DEFAULT_WIDTH))
    width_entry.pack()

    tk.Label(
        frame,
        text="Height (px)",
    ).pack(pady=(15, 5))

    height_entry = tk.Entry(frame)
    height_entry.insert(0, str(DEFAULT_HEIGHT))
    height_entry.pack()

    def apply_resize():
        settings = {
            "width": width_entry.get(),
            "height": height_entry.get(),
        }

        on_apply(settings)

    create_button(
        frame,
        "Apply Resize",
        apply_resize,
    ).pack(pady=20)

    return frame
