# Application Workflow

This document describes the current application architecture and the responsibilities of its modules. The intended boundary is that the GUI handles presentation, `main.py` coordinates requests, and backend modules perform specialized work without depending on the GUI.

## Architecture Goal

- `gui.py` is the frontend. It gathers user input and displays information returned by the application.
- `main.py` is the application orchestrator and the interface through which the frontend requests backend work.
- Backend modules handle image loading, processing, previews, gallery listing, and file storage.
- Backend modules do not import `gui.py` or depend on Tkinter.

## Current User Workflow

1. The user chooses an image by browsing or dragging it into the GUI.
2. The GUI calls `Application.validate_input()` through the application instance created by `create_application()` in `main.py`.
3. The user selects an operation. The current GUI does not expose operation-specific settings.
4. The GUI calls `Application.process_image()` with the image path and operation name.
5. `main.py` validates the operation, loads the image through `loader.py`, and calls the matching processing function.
6. The result is passed to `save.py`, which writes it into `saved_images/` as JPEG by default.
7. `main.py` returns the output path, and the GUI displays a success or error message.
8. The GUI requests gallery records from `main.py` and displays the returned records and thumbnail data.
9. Download and delete actions are sent through `main.py` and delegated to `save.py`.

The current GUI runs processing synchronously. Long processing operations can temporarily block interaction with the window.

## Module Responsibilities

### `gui.py` — Frontend

- Displays the interface and collects user choices.
- Calls the application instance exposed by `main.py`.
- Displays status messages, gallery records, and thumbnail data returned by the backend.
- Creates Tkinter widgets, including `PhotoImage` instances, to display backend-provided thumbnail data.
- Does not load images with OpenCV or call processing, gallery, or storage modules directly.
- Owns presentation actions such as file dialogs and confirmation dialogs.

### `main.py` — Application Orchestrator

- Defines the `Application` service and `create_application()` factory.
- Validates image paths and operation names.
- Coordinates image loading, processing, gallery retrieval, preview preparation, and storage.
- Passes operation-specific settings to processing functions when provided.
- Passes output format separately to the storage module.
- Returns paths, gallery records, and errors to the frontend.
- Does not import Tkinter or contain GUI presentation logic.
- Receives the storage dependency when the application is created; it does not create a module-level default application.

### `loader.py` — Image Loading

- Loads an image path into an OpenCV image array.
- Raises a clear error if the image cannot be decoded.
- Does not process, save, copy, delete, or display images.
- Does not depend on the GUI.

### Processing Modules

`resize.py`, `crop.py`, `blur.py`, `sharpen.py`, and `enhance.py`:

- Receive decoded image data and, where supported, operation-specific settings.
- Return processed image data.
- Do not load or save files.
- Do not depend on the GUI or gallery storage.

### `gallery.py` — Gallery Listing

- Finds supported image files in the gallery directory.
- Returns file paths, names, and modification timestamps for display.
- Does not save, copy, or delete files.
- Does not create GUI widgets.

### `preview.py` — Thumbnail Preparation

- Loads a stored image through `loader.py` for preview preparation.
- Scales it to fit the configured thumbnail dimensions.
- Encodes it as PNG data that the frontend can display.
- Returns thumbnail data and image dimensions, or empty preview fields if loading or encoding fails.
- Does not create Tkinter widgets or depend on the GUI.

### `save.py` — File Storage

- Saves processed images in a supported format.
- Copies stored images to user-selected destinations.
- Deletes images from the managed storage directory.
- Does not list gallery contents or prepare previews.
- Does not depend on the GUI.

### `tests/` — Automated Checks

- Tests backend behavior without starting the GUI where practical.
- Storage tests cover saving, listing through `gallery.py`, copying, deleting, and unsupported formats.
- Processing tests cover image-operation behavior and invalid inputs.

## Request and Data Boundaries

The GUI sends simple values to the application, such as:

- Input image path
- Operation name
- Operation-specific settings (supported by the backend, though not currently exposed in the GUI)
- Output format (supported by the backend; the current GUI uses JPEG by default)

Processing functions receive decoded image arrays and only settings relevant to that operation. The backend returns simple values such as output paths, gallery records, thumbnail data, and clear errors. Tkinter widgets and GUI framework objects do not cross into the backend.

## Error Handling

- `loader.py` reports image loading failures.
- Processing modules report invalid operation inputs.
- `save.py` reports file operation failures.
- `main.py` coordinates backend calls and returns useful errors to the frontend.
- `gui.py` displays those errors to the user.

## Current Implementation Notes

- The GUI supports image selection, operation selection, processing, gallery previews, downloading, and deleting.
- The GUI does not currently provide controls for resize dimensions, crop coordinates, or output format.
- Processing is synchronous, so long operations can make the window unresponsive until they finish.
- Processed images are saved as JPEG by default. PNG transparency is not retained because `loader.py` loads images in OpenCV color mode.
- Real-ESRGAN is configured for CPU inference and depends on its model weights being available under `models/`.
- Gallery metadata is derived from files and modification timestamps; there is no SQLite gallery database.

Update these notes when implementation behavior changes. A planned workflow step should not be described as complete until the behavior exists and has been confirmed.

## Learning Approach

For each architecture change:

1. Trace one concrete request from the GUI through `main.py` to the backend module and back.
2. Identify each function's inputs, behavior, return value, and possible errors.
3. Keep each module focused on its responsibility.
4. Update this document to match implemented behavior.
