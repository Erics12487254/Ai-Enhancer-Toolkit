# Project Progress Log

## Progress Template

# YYYY-MM-DD

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | [Main task completed during the session.] | [x] |
| 2 | [Second task completed during the session.] | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | [Additional experiment, practice, or discovery.] | [x] |

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
- `Postpone` = Postponed for future development
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
| 1 | Reviewed the image input flow across `gui.py`, `main.py`, and `loader.py`. | [x] |
| 2 | Confirmed that the GUI temporarily receives a dropped file path and passes it to `validate_input()` in `main.py`. | [x] |
| 3 | Confirmed that `load_image()` uses `cv2.imread()` and raises a `ValueError` when OpenCV cannot load the file. | [x] |
| 4 | Confirmed that the GUI displays an error for an invalid drop and keeps a valid dropped path for later processing. | [x] |
| 5 | Updated the Stage 2 checklist in `ROADMAP.md` for successful-load checking and invalid or unsupported image files. | [x] |
| 6 | Ran `gui.py` and confirmed that the GUI window appears. | [x] |
| 7 | Confirmed drag-and-drop image selection and the operation dropdown work. | [x] |
| 8 | Marked “Build a simple GUI to select an input image” complete in `ROADMAP.md`. | [x] |
| 9 | Adjusted `user_option()` in `main.py` to route either a terminal choice or the GUI's operation choice. | [x] |
| 10 | Changed `main()` to receive the image path and operation, then reuse existing processing and saving functions. | [x] |
| 11 | Connected the GUI's Process button to `main.py` and moved the saved-image confirmation into the GUI. | [x] |

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
| 1 | Reviewed `WORKFLOW.md` against the current GUI and backend design. | [x] |
| 2 | Removed the terminal menu from `main.py` and made it provide UI-independent validation and processing functions. | [x] |
| 3 | Connected `gui.py` to `main.py` for image validation, processing, and saving; the GUI displays errors and the returned output path. | [x] |
| 4 | Changed processing functions to receive an already loaded image, leaving image loading and operation routing to `main.py`. | [x] |
| 5 | Updated `save.py` to return the output path, report failed writes, and protect the source image if it matches the default output path. | [x] |
| 6 | Updated `WORKFLOW.md` to describe the implemented responsibilities and current behavior. | [x] |
| 7 | Ran the GUI resize-and-save workflow and confirmed the processed image was saved. | [x] |
| 8 | Explained what `validate_input()` checks and why `gui.py` calls it when an image is dropped. | [x] |
| 9 | Traced how `process_image()` selects an operation, loads and processes the image, and sends the result to `save.py`. | [x] |
| 10 | Explained what `gui.py` displays when the workflow succeeds or raises an error. | [x] |
| 11 | Ran the GUI flow and confirmed the behavior before changing code or checking off another roadmap item. | [x] |

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
| 1 | Displayed an image and reviewed OpenCV's BGR channel order, image shape, and pixel values. | [x] |
| 2 | Compared nearest, linear, cubic, and Lanczos interpolation methods. | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Compared an original image with one downscaled and enlarged again; observed the limits of traditional upscaling. | [x] |
| 2 | Added the crop operation to the GUI workflow and confirmed the saved crop shape was 400 × 400 × 3. | [x] |
| 3 | Applied Gaussian blur and sharpening filters; reviewed the sharpening kernel and confirmed the output dimensions and pixel values changed. | [x] |
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
| 1 | Discussed features, labels, datasets, and predictions using cat, dog, and wolf examples. | [x] |
| 2 | Explained training, validation, and test sets, including why the test set is held back for final evaluation. | [x] |
| 3 | Worked through loss and optimization using cat/dog prediction probabilities. | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Discussed overfitting, generalization, data variety, data quality, and preprocessing with image examples. | [x] |
| 2 | Ran a small supervised cat/dog classifier demonstration using synthetic features, learned class centroids, and separate training, validation, and test examples. | [x] |
| 3 | Compared predictions with known labels and calculated 0–1 error rates for the tiny validation and test splits. | [x] |

### Plan for the next session

- Begin Stage 5 — Deep Learning.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Understand tensors and layers. | [x] |
| 2 | Understand weights, biases, and activations. | [x] |
| 3 | Understand a forward pass conceptually. | [x] |

---

# 2026-10-20

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Learned how tensors and layers represent and process image data. | [x] |
| 2 | Understood how weights, biases, and activation functions affect layer calculations. | [x] |
| 3 | Traced a forward pass from input values through layers to an output. | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Learned how backpropagation uses prediction error to update weights and biases. | [x] |
| 2 | Learned how epochs, batches, and learning rate shape the training process. | [x] |
| 3 | Learned how CNN filters produce feature maps and how layers can combine image features. | [x] |
| 4 | Ran a small neural-network example in the project virtual environment; one training update reduced the loss from 0.2113 to 0.1460. | [x] |

### Plan for the next session

- Begin Stage 6 — PyTorch.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Create and manipulate PyTorch tensors. | [x] |
| 2 | Understand CPU vs. GPU device selection. | [x] |
| 3 | Build a `Dataset` and `DataLoader`. | [x] |

---

# 2026-10-21

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Learned how tensor normalization changes pixel values without changing tensor shape. | [x] |
| 2 | Learned how PyTorch selects a CPU or CUDA device and how `.to(device)` moves a tensor while preserving its values and shape. | [x] |
| 3 | Learned how a `Dataset` pairs each image with its label and how a `DataLoader` groups those pairs into batches. | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Organized the learning scripts under `test/` by roadmap stage. | [x] |
| 2 | Documented the stage-based learning examples in `README.md`. | [x] |

### Plan for the next session

- Define a simple model with `torch.nn` and trace how it turns an input tensor into an output.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Define a model with `torch.nn`. | [x] |
| 2 | Understand the steps in a basic PyTorch training loop. | [x] |
| 3 | Calculate loss and update model parameters. | [x] |

---

# 2026-10-23

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Define a model with `torch.nn`. | [x] |
| 2 | Write a training loop. | [x] |
| 3 | Calculate loss and update model parameters. | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Save and load model weights. | [x] |
| 2 | Track training and validation loss. | [x] |

### Plan for the next session

- Research beginner-friendly super-resolution models, then choose a realistic dataset and check its usage licence.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Research beginner-friendly super-resolution models such as SRCNN or ESPCN. | [x] |
| 2 | Choose a realistic super-resolution dataset and check its usage licence. | [x] |

# 2026-10-24

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Researched beginner-friendly super-resolution models, including SRCNN and ESPCN. | [x] |
| 2 | Selected five Wikimedia Commons images and reviewed their usage licence information. | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Created low-resolution copies for five high-resolution images and paired them with their originals. | [x] |

### Plan for the next session

- Understand the baseline model before continuing with training.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Trace one low-resolution tensor through the baseline model and explain the shape changes at each stage. | [x] |

---

# 2026-10-25

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Traced a grayscale low-resolution tensor through ESPCN, including convolution channel changes, preserved spatial dimensions, and PixelShuffle's 2× output shape. | [x] |
| 2 | Explained why PixelShuffle needs four channels for grayscale 2× upscaling and generalized the channel count to upscale factor squared. | [x] |

### Extra

None.

### Plan for the next session

- Postpone the four remaining Stage 7 objectives and finish the stage. Begin Stage 8.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Review what has become difficult to maintain | [x] |
| 2 | Separate image I/O, processing, model inference, and UI responsibilities | [x] |
| 3 | Define clear class and method responsibilities | [x] |

# 2026-10-26

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Review what has become difficult to maintain | [x] |
| 2 | Separate image I/O, processing, model inference, and UI responsibilities | [x] |
| 3 | Define clear class and method responsibilities | [x] |

### Extra

None.

### Plan for the next session

- Continue stage 8.

### Tomorrow's learning checklist

# 2026-10-27

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Review what has become difficult to maintain | [x] |
| 2 | Separate image I/O, processing, model inference, and UI responsibilities | [x] |
| 3 | Define clear class and method responsibilities | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Reviewed inheritance and composition; concluded the current image-operation functions do not need an additional class hierarchy. | [x] |
| 2 | Added input-type and minimum-dimension validation to `crop_image()` with clear errors. | [x] |
| 3 | Added pytest unit tests for the crop result, undersized images, and non-NumPy input; confirmed the tests pass with `python -m pytest tests/test_crop.py`. | [x] |
| 4 | Refactored the GUI operation menu to use the keys from `main.py`'s `OPERATIONS` mapping instead of repeating the labels. | [x] |

### Plan for the next session

- Begin Stage 9 — Generative AI Enhancement.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Learn the difference between restoration, super-resolution, and generative enhancement. | [ ] |

---

# 2026-10-29

### What we did

| # | Task | Status |
|---:|---|---|
| 1 | Learned the difference between restoration, super-resolution, and generative enhancement, including that models estimate details that are missing from a low-resolution image. | [x] |
| 2 | Explored Real-ESRGAN as a pretrained image-restoration approach for the project’s wallpaper use case. | [x] |
| 3 | Reviewed the model’s licence, hardware, and dependencies: the repository code uses BSD-3-Clause, separate pretrained-weight terms were not clear in the repository, the laptop has Intel Arc 140T graphics, and the portable NCNN Vulkan build avoids adding BasicSR to the project environment. | [x] |

### Extra

| # | Task | Status |
|---:|---|---|
| 1 | Ran Real-ESRGAN inference on sample images and compared its output with the super-resolution baseline. | [x] |
| 2 | Reviewed artifacts: the very blurry portrait became uncanny, while the clearer anime image retained coherent linework. | [x] |
| 3 | Concluded that enhancement works better when the source has enough detail; very small or blurry images leave the model to guess. | [x] |
| 4 | Observed that 4× upscaling produced a 10,200 × 5,624 image of about 51 MB and increased fan noise during processing. | [x] |

### Plan for the next session

- Begin Stage 10 — Evaluation.
- Learn PSNR and SSIM, then evaluate outputs against suitable reference images.

### Tomorrow's learning checklist

| # | Learning task | Status |
|---:|---|---|
| 1 | Understand PSNR and what it measures. | [ ] |
| 2 | Understand SSIM and what it measures. | [ ] |
| 3 | Evaluate outputs against suitable reference images. | [ ] |
