# Application Workflow

This document describes the intended user flow and the responsibilities of each module. It serves as a learning guide while the GUI and image-processing workflow are developed.

The application must separate its core logic from the user interface so that another frontend can be introduced in the future without rewriting the image-processing workflow.

## Intended User Flow

1. **Drop an Image.** The user drags an image from File Explorer into the GUI's drop area.
2. **Validate the Image.** `gui.py` sends the dropped file path to `main.py`. `main.py` checks whether OpenCV can decode it. If validation fails, the GUI displays the returned error, and the invalid file is not retained as the selected input.
3. **Choose an Operation.** The user selects an available operation, such as resize or enhance, through the GUI.
4. **Process the Image.** When the user presses Process, `gui.py` sends the selected path and operation to `main.py`. `main.py` checks the request, loads the image, selects the processing function, and coordinates the workflow.
5. **Save the Result.** `main.py` passes the processed image to `save.py`. `save.py` reports a write failure and returns the output path when saving succeeds. The original image must not be overwritten by default.
6. **Display the Outcome.** The GUI displays the processing status, output location, or an appropriate error message returned through `main.py`.

## Module Responsibilities

- **`gui.py` — Presentation Layer**
  - Displays the interface, including the image drop area, operation choices, progress indicators, and result messages.
  - Collects user input and sends user actions to `main.py`.
  - Displays validation results, processing status, and errors returned by `main.py`.
  - Contains no application-level validation, image-processing logic, or file-saving logic; it asks `main.py` to validate and process.
  - Must remain replaceable by another frontend without requiring changes to the core application logic.

- **`main.py` — Application Logic and Coordination**
  - Acts as the central coordinator for the application workflow.
  - Contains the required application-level validations, functions, and methods.
  - Validates the selected image and operation requests, and handles a missing image selection.
  - Determines which processing operation to execute based on the user's request.
  - Coordinates image processing and saving by calling the appropriate modules.
  - Handles results and errors returned by other modules and returns the saved output path or raises a clear error for the frontend to display.
  - Must not depend on a specific GUI framework or contain presentation logic.
  - Keeps the workflow organized by delegating specialized tasks to their respective modules instead of implementing everything in one file.

- **`resize.py` — Image Resizing**
  - Contains the functions and logic required to resize an image.
  - Receives a decoded image from `main.py` and returns the resized image.
  - Does not load files or depend on the GUI.
  - Does not depend on the GUI.

- **`enhance.py` — Image Enhancement**
  - Contains the image-enhancement logic when implemented.
  - Receives the required inputs from `main.py`.
  - Returns the processed image or reports a processing failure.
  - Does not depend on the GUI.

- **`save.py` — Output Saving**
  - Contains the logic for writing processed images to the configured or selected output location.
  - Reports whether saving succeeded or failed.
  - Avoids overwriting the original image by default.
  - Does not depend on the GUI.

## Architecture Rules

1. **Separate presentation from application logic.** The GUI handles display and user interaction; `main.py` handles application logic and workflow coordination.
2. **Keep `main.py` as the coordinator.** It owns the overall workflow but delegates specialized processing and saving tasks to their respective modules.
3. **Keep the frontend replaceable.** The core application must work independently of a specific GUI framework.
4. **Use a clear communication boundary.** The GUI communicates with the application through `main.py` rather than importing processing or saving modules directly.
5. **Keep processing modules independent of the frontend.** Modules such as `resize.py`, `enhance.py`, and `save.py` must not require a GUI to function.
6. **Give each module a clear responsibility.** Avoid duplicating logic or placing unrelated responsibilities in the same module.
7. **Handle errors explicitly.** Failed validation, processing, or saving must produce a clear result that the frontend can display.
8. **Protect the original input.** Processed output must not overwrite the source image by default.
9. **Keep modules testable.** Application logic and processing functions should be testable without launching the GUI wherever practical.

## Current Implementation

Update this section as the implementation evolves.

- **`gui.py`:** Has a drag-and-drop target and operation menu. It sends dropped paths to `main.py` for validation and sends the selected path and operation to `main.py` for processing and saving. It displays errors and the returned output path.
- **`main.py`:** Provides UI-independent `validate_input()` and `process_image()` functions. It loads the selected image, routes it to the requested operation, and coordinates saving without terminal prompts or Tkinter.
- **`loader.py`:** Uses `cv2.imread()` and raises a clear error when OpenCV cannot decode the image.
- **`resize.py`:** Receives an already loaded image and returns its resized version; it does not load files or depend on the GUI.
- **`enhance.py`:** Not implemented yet.
- **`save.py`:** Saves to `saved_image.jpg` in the current working directory by default, returns the saved path, and raises an error when OpenCV reports a failed write. If the default output path matches the source path, it uses `saved_image_processed.jpg` to protect the original.

Update these notes as behaviors change. Do not mark a workflow step complete merely because its code has been written. Mark it complete only after it works as intended and you can explain how the relevant modules participate.

## Learning Requirements

- Explain the purpose of each new function, method, validation, and module before or while introducing it.
- Prefer guiding the user through the implementation instead of writing the entire solution on their behalf.
- Explain why a particular approach is suitable and discuss reasonable alternatives when relevant.
- Verify that the user understands the changes made during each daily task.
- Keep implementation consistent with `ROADMAP.md` and follow its checklist from top to bottom.
