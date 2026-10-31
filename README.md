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
- `exercise/` — separate learning and experimentation files, including super-resolution evaluation
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

## Learning examples

### Stage 2 — OpenCV

- `test/Stage 2/color.py` prints image dimensions and a BGR pixel. It also compares interpolation methods, which are covered in Stage 3.

### Stage 3 — Image Processing

- `test/Stage 3/limitation.py` shrinks an image, enlarges it again, and compares the result with the original.

### Stage 5 — Deep Learning

- `test/Stage 5/cnn.py` demonstrates a small neural network's forward pass, backpropagation, and one parameter update. Despite its filename, this example does not implement a CNN.

### Stage 6 — PyTorch

- `tensor.py` and `tensor2.py` introduce tensors and normalization.
- `device.py` selects CPU or CUDA.
- `dataset.py` defines a tiny image dataset and shows batches.
- `linear_model.py` demonstrates a `Linear` layer with known weights.
- `train_classifier.py` trains a small classifier and saves its weights.
- `save_load_model.py` loads those weights.
- `training_validation_loss.py` compares loss on separate toy training and validation examples.
- Run `train_classifier.py` before `save_load_model.py`. The four-image dataset is only for learning the mechanics, not for meaningful model evaluation.

### Stage 7 — Super-Resolution

- `test/Stage 7/low_reso.py` creates low-resolution copies from the high-resolution dataset by resizing each image to half its width and height.
- `test/Stage 7/espcn.py` defines and trains an ESPCN model for 2× upscaling. It uses paired low- and high-resolution images, reserves `Alexei_Leonov.jpg` for a held-out inference example, and saves the model weights and output image beside the learning script and in `test/SR_results/`, respectively.
- `test/Stage 7/model_comparison.py` demonstrates the tensor shape flow of SRCNN-style and ESPCN-style upscaling on a small example. It compares their stages and shapes, not their image quality or runtime.

### Stage 9 — Real-ESRGAN

- Explored Real-ESRGAN as a generative super-resolution approach.
- Installed and configured Real-ESRGAN in a separate Python environment.
- Ran inference using the pretrained `RealESRGAN_x2plus` model.
- Evaluated its ability to generate visually convincing image details.

### Stage 10 — Super-Resolution Evaluation

Compared three image upscaling approaches using the same low-resolution input image and original high-resolution reference:

1. **Bicubic interpolation** — traditional image interpolation using OpenCV.
2. **ESPCN** — a deep learning-based super-resolution model.
3. **Real-ESRGAN** — a generative super-resolution model.

The evaluation workflow is located in `exercise/Stage 10/`.

#### Evaluation metrics

- **PSNR (Peak Signal-to-Noise Ratio):** Measures pixel-level similarity between the generated output and reference image. Higher values indicate greater numerical similarity.
- **SSIM (Structural Similarity Index):** Measures structural similarity between the generated output and reference image. Higher values indicate greater similarity.
- **Runtime:** Measures the processing time required by each method. Lower values indicate faster processing.

#### Experimental results

The following results were obtained using `Alexei_Leonov.jpg`, with all outputs standardized to 3844 × 3075 pixels.

| Method | PSNR (dB) | SSIM | Runtime (seconds) |
|---|---:|---:|---:|
| Bicubic | 33.9431 | 0.8926 | 0.0116 |
| ESPCN | 15.5001 | 0.5581 | 0.7384 |
| Real-ESRGAN | 31.2559 | 0.8255 | 79.8095 |

#### Evaluation workflow

- `quality_evaluator.py` coordinates the evaluation of all three methods.
- `realesrgan_test.py` runs Real-ESRGAN using its separate Python environment.
- `test_result.py` saves the evaluation results into an SQLite database.
- `evaluation.db` stores the method names, image paths, PSNR, SSIM, runtime, image dimensions, and timestamps.
- Standardized output images are saved in `exercise/SR_results/standardized/`.

Run the evaluation from the repository root using the main project environment:

```powershell
python "exercise/Stage 10/quality_evaluator.py"
```

Real-ESRGAN runs on the CPU in the current setup and takes significantly longer than the other methods. Keep the device adequately ventilated during evaluation.

#### Observations and limitations

- **Bicubic:** Fastest method and achieved the highest PSNR and SSIM in this experiment. However, interpolation cannot reconstruct genuinely missing image details.
- **ESPCN:** Requires more processing time than Bicubic. Its relatively low evaluation scores may be related to the limited training dataset and model training process.
- **Real-ESRGAN:** Produced visually detailed results and achieved higher PSNR and SSIM than ESPCN. However, it required significantly more processing time. Its generative approach may introduce plausible details that do not accurately represent the original image.

PSNR and SSIM do not fully represent perceived image quality. Furthermore, this experiment uses only one reference image, so the results should not be treated as universal rankings of the three approaches.

## Current development status

The current learning focus is Stage 10: Super-Resolution Evaluation.

The super-resolution models and Real-ESRGAN inference workflow are experimental learning components. They are not integrated into the desktop application.

No AI model is currently integrated into or bundled with the application. Model and dataset licensing will be documented if they are added to the project.