# AI Image Enhancer — Project Roadmap Checklist

> Use this checklist to track progress. Check an item only when you can explain it and demonstrate it in your project.
>
> **Estimated total:** about 33–55 weeks, depending on pace and how much time you can study each week. Stages may overlap.

## Progress tracker
 
- [x] **Stage 1 — Python + OOP** *(2–4 weeks)*
  - [x] Review Python fundamentals used in the project
  - [x] Understand classes, objects, attributes, methods, and `self`
  - [x] Understand `__init__`, properties, and `__str__`
  - [x] Understand method arguments, return values, and how callers use them
  - [x] Practice composition vs. inheritance
  - [x] Split the project into clear modules/files
  - [x] Import and use classes across files
  - [x] Handle common errors with exceptions
  - [x] Write basic tests for important methods

- [x] **Stage 2 — OpenCV** *(2–3 weeks)*
  - [x] Load an image with `cv2.imread()`
  - [x] Check whether an image loaded successfully
  - [x] Understand image shape: height, width, and channels
  - [x] Display images and understand BGR vs. RGB
  - [x] Save images with `cv2.imwrite()`
  - [x] Handle invalid paths and unsupported files
  - [x] Build a simple load → process → save workflow

- [x] **Stage 3 — Image Processing** *(3–5 weeks)*
  - [x] Resize images to custom dimensions
  - [x] Compare interpolation methods (nearest, linear, cubic, Lanczos)
  - [x] Preserve aspect ratio when resizing
  - [x] Crop an image using array slicing
  - [x] Apply blur and sharpening filters
  - [x] Understand the limits of traditional upscaling
  - [x] Compare original and processed outputs

- [x] **Stage 4 — Machine Learning Fundamentals** *(3–5 weeks)*
  - [x] Understand features, labels, datasets, and predictions
  - [x] Understand training, validation, and test sets
  - [x] Learn loss functions and optimization at a high level
  - [x] Understand overfitting and generalization
  - [x] Learn why data quality and preprocessing matter
  - [x] Complete a small beginner ML exercise

- [x] **Stage 5 — Deep Learning** *(4–6 weeks)*
  - [x] Understand tensors and layers
  - [x] Understand weights, biases, and activations
  - [x] Understand forward pass and backpropagation conceptually
  - [x] Understand epochs, batches, and learning rate
  - [x] Learn the basics of convolutional neural networks (CNNs)
  - [x] Understand how a CNN can learn image features
  - [x] Run a small neural-network example

- [x] **Stage 6 — PyTorch** *(2–4 weeks)*
  - [x] Create and manipulate tensors
  - [x] Understand CPU vs. GPU device selection
  - [x] Build a `Dataset` and `DataLoader`
  - [x] Define a model with `torch.nn`
  - [x] Write a training loop
  - [x] Calculate loss and update model parameters
  - [x] Save and load model weights
  - [x] Track training and validation loss

- [ ] **Stage 7 — Super-Resolution** *(4–7 weeks)*
  - [x] Research beginner-friendly super-resolution models (e.g. SRCNN or ESPCN)
  - [x] Choose a realistic dataset and check its usage licence
  - [x] Prepare low-resolution inputs and high-resolution targets
  - [x] Build or adapt a baseline model
  - [postpone] Train a small model or run a pretrained model as a baseline
  - [postpone] Test on images not used during training
  - [postpone] Compare the model against traditional interpolation
  - [postpone] Record limitations, artifacts, and failure cases

- [x] **Stage 8 — Advanced OOP / Refactoring** *(2–3 weeks)*
  - [x] Review what has become difficult to maintain
  - [x] Separate image I/O, processing, model inference, and UI responsibilities
  - [x] Define clear class and method responsibilities
  - [x] Avoid unnecessary inheritance and overly complicated abstractions
  - [x] Add input validation and useful error messages
  - [x] Add or improve unit tests
  - [x] Refactor without changing expected behavior

- [x] **Stage 9 — Generative AI Enhancement** *(3–6 weeks)*
  - [x] Learn the difference between restoration, super-resolution, and generative enhancement
  - [x] Explore a suitable pretrained generative/image-restoration approach
  - [x] Check model licence, hardware requirements, and dependencies
  - [x] Run inference on sample images
  - [x] Compare outputs with the super-resolution baseline
  - [x] Check for invented details, distorted faces, or other artifacts
  - [x] Document when the generative approach is and is not appropriate

- [x] **Stage 10 — Evaluation** *(2–3 weeks)*
  - [x] Understand PSNR and what it measures
  - [x] Understand SSIM and what it measures
  - [x] Evaluate outputs against suitable reference images
  - [x] Compare traditional interpolation, the SR model, and the generative approach
  - [x] Keep test images and settings consistent
  - [x] Create a results table with metrics and runtime
  - [x] Include side-by-side visual comparisons
  - [x] Explain metric limitations and observed failure cases

- [ ] **Stage 11 — Final Application** *(2–4 weeks)*
  - [x] Build a simple GUI to select an input image
  - [ ] Let the user choose an enhancement method and settings
  - [ ] Let the user choose where to save the output
  - [x] Show useful progress, success, and error messages
  - [ ] Keep the interface responsive during processing where practical
  - [ ] Organize the project files and dependencies
  - [ ] Add installation and usage instructions to `README.md`
  - [ ] Include example images and evaluation results
  - [ ] Add tests for key functionality
  - [ ] Check licences and acknowledge external models/datasets
  - [ ] Remove temporary files, debug output, and unused code
  - [ ] Push the finished project to GitHub

## Final portfolio checklist

- [ ] A new user can install and run the project using the README
- [ ] The app handles missing, invalid, or unsupported image files gracefully
- [ ] Results can be reproduced using documented settings
- [ ] Traditional and AI-based methods are compared fairly
- [ ] Evaluation includes both metrics and visual examples
- [ ] Known limitations are explained honestly
- [ ] Git history shows meaningful development
- [ ] Screenshots or a short demo are included in the repository

# Future development
- [ ] Continue developing gui or replace with another front end. 
- [ ] Update crop.py into realistic version.
- [ ] Update resize.py into realistic version.
- [ ] Update filter.py into system deciding a suitable one on it's own.
- [ ] Update sharpen.py into realistic version.
- [ ] Experiment with brightness, contrast, and color adjustments


