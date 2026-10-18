# Project Progress Log

## Progress Template

# YYYY-MM-DD

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | [Main task completed during the session.] | Done |
| 2 | [Second task completed during the session.] | Done |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | [Additional experiment, practice, or discovery.] | Done |

If no extra work was done, write `None`.

### Plan for the next session

- [Next stage, topic, or project task.]

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | [First learning objective.] | [ ] |
| 2 | [Second learning objective.] | [ ] |
| 3 | [Third learning objective.] | [ ] |

### Status definitions

- `[ ]` = Not completed
- `[x]` = Completed
- `In Progress` = Started but unfinished
- `Done` = Task finished
- `Deferred` = Postponed for future development
- `None` = No extra work was done

### Progress logging rules

1. Before updating today's work, review the previous date's `Tomorrow's learning checklist`.
2. Carry unfinished learning tasks forward unless there is a clear reason to defer them.
3. Mark a learning task as completed only when I can explain the concept independently and demonstrate it with an example or in the project.
4. Record actual accomplishments, not planned accomplishments, under `What we did`.
5. Keep deferred features separate from completed tasks.

---

# 2026-10-15

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

### Extra

None.

### Plan for the next session

- Run the full GUI resize-and-save flow after the latest success-message change.
- Continue the GUI workflow.
- Decide how to handle the unfinished Enhance option and fixed output location.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Run the GUI resize-and-save flow after the success-message change. | [ ] |
| 2 | Continue understanding the GUI-to-backend workflow. | [ ] |
| 3 | Decide how to handle the unfinished Enhance option and fixed output location. | [ ] |

---

# 2026-10-16

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

### Extra

None.

### Plan for the next session

- Display an image and understand the difference between BGR and RGB.
- Compare OpenCV's nearest, linear, cubic, and Lanczos interpolation methods.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Display an image and explain the difference between OpenCV's BGR channel order and RGB. | [x] |
| 2 | Compare nearest, linear, cubic, and Lanczos interpolation methods. | [x] |

---

# 2026-10-17

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
| 4 | Deferred brightness, contrast, and color adjustments to future development. | Deferred |

### Plan for the next session

- Begin Stage 4 — Machine Learning Fundamentals.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Understand features, labels, datasets, and predictions using an image example. | [ ] |
| 2 | Understand training, validation, and test sets using the same example. | [ ] |
| 3 | Learn loss functions and optimization at a high level using a simple prediction example. | [ ] |

---

# 2026-10-18

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Discussed features, labels, datasets, and predictions using cat, dog, and wolf examples. | Done |
| 2 | Explained training, validation, and test sets, including why the test set is held back for final evaluation. | Done |
| 3 | Worked through loss and optimization using cat/dog prediction probabilities. | Done |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Discussed overfitting, generalization, data variety, data quality, and preprocessing with image examples. | Done |
| 2 | Ran a small supervised cat/dog classifier demonstration using synthetic features, learned class centroids, and separate training, validation, and test examples. | Done |
| 3 | Compared predictions with known labels and calculated 0–1 error rates for the tiny validation and test splits. | Done |

### Plan for the next session

- Begin Stage 5 — Deep Learning.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Understand tensors and layers. | [ ] |
| 2 | Understand weights, biases, and activations. | [ ] |
| 3 | Understand a forward pass conceptually. | [ ] |
