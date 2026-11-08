import tkinter as tk
from datetime import datetime
from tkinterdnd2 import DND_FILES


def create_image_input(parent, on_browse, on_drop):
    """Create a drag-and-drop image input area."""

    drop_area = tk.Label(
        parent,
        text="Drag and drop an image here\nor click to browse",
        relief="groove",
        borderwidth=2,
        height=5,
        font=("Arial", 12),
    )
    drop_area.pack(fill="x", pady=10)

    drop_area.drop_target_register(DND_FILES)
    drop_area.dnd_bind("<<Drop>>", on_drop)
    drop_area.bind("<Button-1>", lambda event: on_browse())

    return drop_area


def create_button(parent, text, command, **kwargs):
    """Create a reusable button."""

    button = tk.Button(
        parent,
        text=text,
        command=command,
        **kwargs,
    )
    return button



def create_scrollable_frame(parent):
    """Create a scrollable frame with mouse wheel support."""

    canvas = tk.Canvas(parent, highlightthickness=0)

    scrollbar = tk.Scrollbar(
        parent,
        orient="vertical",
        command=canvas.yview,
    )

    content_frame = tk.Frame(canvas)

    content_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        ),
    )

    canvas.create_window(
        (0, 0),
        window=content_frame,
        anchor="nw",
    )

    canvas.configure(yscrollcommand=scrollbar.set)

    def on_mousewheel(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units",
        )

    def bind_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def unbind_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", bind_mousewheel)
    canvas.bind("<Leave>", unbind_mousewheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return content_frame


def create_gallery_card(
    parent,
    record,
    row,
    column,
    thumbnail_images,
    on_download,
    on_delete,
):
    """Create one gallery image card."""

    card = tk.Frame(
        parent,
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
        thumbnail_images.append(photo)

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

    tk.Label(
        card,
        text=f"Resolution: {resolution}",
    ).pack()

    created_at = datetime.fromtimestamp(
        record["created_at"]
    ).strftime("%Y-%m-%d %H:%M")

    tk.Label(
        card,
        text=f"Date: {created_at}",
    ).pack(pady=5)

    button_frame = tk.Frame(card)
    button_frame.pack(pady=5)

    create_button(
        button_frame,
        "Download",
        lambda: on_download(record),
    ).pack(side="left", padx=3)

    create_button(
        button_frame,
        "Delete",
        lambda: on_delete(record),
    ).pack(side="left", padx=3)