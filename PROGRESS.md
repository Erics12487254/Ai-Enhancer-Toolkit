# Project Progress Log

## 2026-10-15

### What we did

- Reviewed the image input flow across `gui.py`, `main.py`, and `loader.py`.
- Confirmed that the GUI receives a dropped file path temporarily and passes it to `validate_input()` in `main.py`.
- Confirmed that `load_image()` uses `cv2.imread()` and raises a `ValueError` when OpenCV cannot load the file.
- Confirmed that the GUI displays an error for an invalid drop and keeps the valid dropped path for later processing.
- Updated the Stage 2 checklist in `ROADMAP.md` for successful-load checking and handling invalid or unsupported image files.
- Ran `gui.py` and confirmed that the GUI window appears.
- Confirmed drag-and-drop image selection and the operation dropdown work.
- Marked “Build a simple GUI to select an input image” complete in `ROADMAP.md`.
- Adjusted `user_option()` in `main.py` so it can route either a terminal choice or the GUI's operation choice.
- Changed `main()` to receive the image path and operation, then reuse the existing processing and saving functions.
- Connected the GUI's Process button to `main.py` and moved the saved-image confirmation into the GUI.

### Plan for tomorrow

- Run the full GUI resize-and-save flow after the latest success-message change.
- Continue the GUI workflow, then decide how to handle the unfinished Enhance option and fixed output location.

## 2026-10-16

### What we did

- Reviewed `WORKFLOW.md` against the current GUI and backend design.
- Removed the terminal menu from `main.py` and made it provide UI-independent validation and processing functions.
- Connected `gui.py` to `main.py` for image validation, processing, and saving; the GUI displays errors and the returned output path.
- Changed processing functions to receive an already loaded image, leaving image loading and operation routing to `main.py`.
- Updated `save.py` to return the output path, report failed writes, and protect the source image if it matches the default output path.
- Updated `WORKFLOW.md` to describe the implemented responsibilities and current behavior.
- Left roadmap checkboxes unchanged because the new workflow still needs to be demonstrated in the GUI before marking an item complete.

### Plan for next work session

- Keep tomorrow's session light and focus on understanding the code that is already in the project.

### Tomorrow's learning checklist

- [ ] Explain what `validate_input()` checks and why `gui.py` calls it when an image is dropped.
- [ ] Trace how `process_image()` loads the image, chooses an operation, and sends the result to `save.py`.
- [ ] Explain what `gui.py` displays when the workflow succeeds or raises an error.
- [ ] Run the GUI flow and confirm the behavior together before changing any more code or checking off a roadmap item.

