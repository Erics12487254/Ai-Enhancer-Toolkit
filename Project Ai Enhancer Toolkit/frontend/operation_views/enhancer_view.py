
import tkinter as tk

from frontend.components.widgets import create_button


def create_enhancer_view(parent, on_apply, state="preparing"):
    """Create the image enhancement interface."""

    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="Enhance your image with Real-ESRGAN (2×)",
        font=("Arial", 12),
    ).pack(pady=(20, 10))

    # Display the interface according to the current enhancement stage.
    if state == "preparing":
        tk.Label(
            frame,
            text="Preparing enhancement engine... Please wait.",
        ).pack(pady=20)

    elif state == "ready":
        tk.Label(
            frame,
            text="Enhancement engine is ready.",
        ).pack(pady=10)

        def apply_enhancement():
            on_apply({})

        create_button(
            frame,
            "Apply Enhancement",
            apply_enhancement,
        ).pack(pady=20)

    elif state == "enhancing":
        tk.Label(
            frame,
            text="Enhancing image... Please wait.",
        ).pack(pady=20)

    return frame
