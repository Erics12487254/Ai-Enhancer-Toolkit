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
- `resource/` — sample project resources
- `test/` — local learning examples arranged by roadmap stage; this folder is currently excluded by `.gitignore`
- `ROADMAP.md` — learning checklist
- `PROGRESS.md` — session progress and next learning plan
- `WORKFLOW.md` — application flow and module responsibilities

## Learning examples

- **Stage 2 — OpenCV:** `test/Stage 2/color.py` prints image dimensions and a BGR pixel. It also compares interpolation methods, which are covered in Stage 3.
- **Stage 3 — Image Processing:** `test/Stage 3/limitation.py` shrinks an image, enlarges it again, and compares the result with the original.
- **Stage 5 — Deep Learning:** `test/Stage 5/cnn.py` demonstrates a small neural network's forward pass, backpropagation, and one parameter update. Despite its filename, this example does not implement a CNN.
- **Stage 6 — PyTorch:** `tensor.py` and `tensor2.py` introduce tensors and normalization; `device.py` selects CPU or CUDA; `dataset.py` defines a tiny image dataset and shows batches; `linear_model.py` demonstrates a `Linear` layer with known weights; `train_classifier.py` trains a small classifier and saves its weights; `save_load_model.py` loads those weights; `training_validation_loss.py` compares loss on separate toy training and validation examples. Run `train_classifier.py` before `save_load_model.py`. The four-image dataset is only for learning the mechanics, not for meaningful model evaluation.

The current learning focus is Stage 7: understanding and building a beginner-friendly super-resolution baseline. Training and evaluation will follow once the baseline is understood.

No AI model is currently bundled or used. Model and dataset licensing will be documented if they are added.
