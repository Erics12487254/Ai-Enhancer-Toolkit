# AI Enhancer Toolkit

A Python image-processing app with a drag-and-drop desktop interface. AI enhancement is planned for a future version.

## Features

- Resize, crop, blur, and sharpen images
- Drag and drop an image, choose an operation, and save the result as `saved_image.jpg`
- Validate image files and show processing errors in the interface

The **Enhance** option is listed in the interface but is not implemented yet.

## Requirements

- Python 3.10 or newer
- Packages listed in `requirements.txt`
- Pytest is needed only to run the automated tests: `python -m pip install pytest`

## Setup

From the project folder, create a virtual environment and install the dependencies:

```text
python -m venv .venv
python -m pip install -r requirements.txt
```

## Run

```text
python "Project Ai Enhancer Toolkit/gui.py"
```

Drag an image into the window, choose an operation, then select **Process image**. The result is saved in the current working directory. If the default output path would overwrite the input, the app uses `saved_image_processed.jpg` instead.

## Project files

- `Project Ai Enhancer Toolkit/` — application and image-processing modules
- `tests/` — automated pytest tests for application functions
- `resource/` — sample project resources
- `test/` — local learning examples arranged by roadmap stage; this folder is currently excluded by `.gitignore`
- `ROADMAP.md` — learning checklist
- `PROGRESS.md` — session progress and next learning plan
- `WORKFLOW.md` — application flow and module responsibilities

## Run tests

Install pytest in the active environment:

```text
python -m pip install pytest
```

From the repository root, run:

```text
python -m pytest tests/test_crop.py
```

## Learning examples

- **Stage 2 — OpenCV:** `test/Stage 2/color.py` prints image dimensions and a BGR pixel. It also compares interpolation methods, which are covered in Stage 3.
- **Stage 3 — Image Processing:** `test/Stage 3/limitation.py` shrinks an image, enlarges it again, and compares the result with the original.
- **Stage 5 — Deep Learning:** `test/Stage 5/cnn.py` demonstrates a small neural network's forward pass, backpropagation, and one parameter update. Despite its filename, this example does not implement a CNN.
- **Stage 6 — PyTorch:** `tensor.py` and `tensor2.py` introduce tensors and normalization; `device.py` selects CPU or CUDA; `dataset.py` defines a tiny image dataset and shows batches; `linear_model.py` demonstrates a `Linear` layer with known weights; `train_classifier.py` trains a small classifier and saves its weights; `save_load_model.py` loads those weights; `training_validation_loss.py` compares loss on separate toy training and validation examples. Run `train_classifier.py` before `save_load_model.py`. The four-image dataset is only for learning the mechanics, not for meaningful model evaluation.

The current learning focus is Stage 9: Generative AI Enhancement. The remaining Stage 7 super-resolution objectives are postponed for now.

### Stage 7 — Super-Resolution

- `test/Stage 7/low_reso.py` creates low-resolution copies from the high-resolution dataset by resizing each image to half its width and height.
- `test/Stage 7/espcn.py` defines and trains a grayscale ESPCN model for 2× upscaling. It uses paired low- and high-resolution images, reserves `Alexei_Leonov.jpg` for a held-out inference example, and saves the model weights and output image beside the learning script and in `test/SR_results/`, respectively.
- `test/Stage 7/model_comparison.py` demonstrates the tensor shape flow of SRCNN-style and ESPCN-style upscaling on a small example. It compares their stages and shapes, not their image quality or runtime.

No AI model is currently bundled or used. Model and dataset licensing will be documented if they are added.
