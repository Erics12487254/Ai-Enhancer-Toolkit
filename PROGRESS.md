# Project Progress Log

## 2026-10-15

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Reviewed the image input flow across `gui.py`, `main.py`, and `loader.py`. | Done |
| 2 | Confirmed that the GUI temporarily receives a dropped file path and passes it to `validate_input()` in `main.py`. | Done |
| 3 | Confirmed that `load_image()` uses `cv2.imread()` and raises a `ValueError` when OpenCV cannot load the file. | Done |
| 4 | Confirmed that the GUI displays an error for an invalid drop and keeps a valid dropped path for later processing. | Done |
| 5 | Updated the Stage 2 checklist in `ROADMAP.md` for successful-load checking and invalid or unsupported image files. | Done |
| 6 | Ran `gui.py` and confirmed that the GUI window appears. | Done |
| 7 | Confirmed drag-and-drop image selection and the operation dropdown work. | Done |
| 8 | Marked “Build a simple GUI to select an input image” complete in `ROADMAP.md`. | Done |
| 9 | Adjusted `user_option()` in `main.py` to route either a terminal choice or the GUI's operation choice. | Done |
| 10 | Changed `main()` to receive the image path and operation, then reuse existing processing and saving functions. | Done |
| 11 | Connected the GUI's Process button to `main.py` and moved the saved-image confirmation into the GUI. | Done |

### Plan for the next session

- Run the full GUI resize-and-save flow after the latest success-message change.
- Continue the GUI workflow.
- Decide how to handle the unfinished Enhance option and fixed output location.

---

## 2026-10-16

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Reviewed `WORKFLOW.md` against the current GUI and backend design. | Done |
| 2 | Removed the terminal menu from `main.py` and made it provide UI-independent validation and processing functions. | Done |
| 3 | Connected `gui.py` to `main.py` for image validation, processing, and saving; the GUI displays errors and the returned output path. | Done |
| 4 | Changed processing functions to receive an already loaded image, leaving image loading and operation routing to `main.py`. | Done |
| 5 | Updated `save.py` to return the output path, report failed writes, and protect the source image if it matches the default output path. | Done |
| 6 | Updated `WORKFLOW.md` to describe the implemented responsibilities and current behavior. | Done |
| 7 | Ran the GUI resize-and-save workflow and confirmed the processed image was saved. | Done |
| 8 | Explained what `validate_input()` checks and why `gui.py` calls it when an image is dropped. | Done |
| 9 | Traced how `process_image()` selects an operation, loads and processes the image, and sends the result to `save.py`. | Done |
| 10 | Explained what `gui.py` displays when the workflow succeeds or raises an error. | Done |
| 11 | Ran the GUI flow and confirmed the behavior before changing code or checking off another roadmap item. | Done |

### Plan for the next session

First display an image and understand the difference between BGR and RGB. Then compare OpenCV's nearest, linear, cubic, and Lanczos interpolation methods.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Display an image and explain the difference between OpenCV's BGR channel order and RGB. | [x] |
| 2 | Compare nearest, linear, cubic, and Lanczos interpolation methods. | [x] |

---

## 2026-10-17

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Displayed an image and reviewed OpenCV's BGR channel order, image shape, and pixel values. | Done |
| 2 | Compared nearest, linear, cubic, and Lanczos interpolation methods. | Done |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Compared an original image with one downscaled and enlarged again; observed the limits of traditional upscaling. | Done |
| 2 | Added the crop operation to the GUI workflow and confirmed the saved crop shape was 400 × 400 × 3. | Done |
| 3 | Applied Gaussian blur and sharpening filters; reviewed the sharpening kernel and confirmed the output dimensions and pixel values changed. | Done |
| 4 | Deferred brightness, contrast, and color adjustments to Future development. | Deferred |

### Plan for the next session

- Begin Stage 4 — Machine Learning Fundamentals.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Understand features, labels, datasets, and predictions using an image example. | [ ] |
| 2 | Understand training, validation, and test sets using the same example. | [ ] |
| 3 | Learn loss functions and optimization at a high level using a simple prediction example. | [ ] |

