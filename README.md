# AI Enhancer Toolkit

A Python image-processing application with a drag-and-drop desktop interface and a persistent image gallery. AI enhancement is planned for a future version.

## Features

- Resize, crop, blur, and sharpen images.
- Drag and drop an image, choose an operation, and process it through the desktop interface.
- Validate image files and display processing errors.
- Store processed images in a persistent gallery.
- Keep image metadata in an SQLite database.
- Download or delete images from the gallery.
- Automatically remove gallery images after 30 days.
- Recover interrupted image-saving operations.

The **Enhance** option is listed in the interface but is not implemented yet.

## Requirements

- Python 3.10 or newer.
- Packages listed in `requirements.txt`.
- Pytest is required only for running automated tests.

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/Erics12487254/Ai-Enhancer-Toolkit.git
cd Ai-Enhancer-Toolkit
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you may need to adjust the execution policy for your current user.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Running the Application

From the repository root, run:

```powershell
python "Project Ai Enhancer Toolkit/gui.py"
```

### Using the Application

1. Open the application.
2. Drag and drop an image into the input area.
3. Choose an available processing operation.
4. Select **Process image**.
5. The processed image is saved in the application's `saved_images/` directory and appears in the gallery.
6. Use the gallery's **Download** option to copy an image to a chosen destination.
7. Use **Delete** to remove an image from the gallery.

Gallery images and their metadata persist after the application is closed.

Images are automatically removed after 30 days, based on their processing timestamp. The application also performs maintenance to recover interrupted saves and synchronize missing image files.

## Running Automated Tests

The automated tests are located inside `Project Ai Enhancer Toolkit/tests/`.

Install pytest in the active virtual environment:

```powershell
python -m pip install pytest
```

From the repository root, enter the application directory:

```powershell
cd "Project Ai Enhancer Toolkit"
```

Run the storage and gallery tests:

```powershell
python -m pytest tests/test_storage.py -v
```

## Project Structure

- `Project Ai Enhancer Toolkit/` — application and image-processing modules.
  - `database/` — SQLite database and database operations.
  - `saved_images/` — persistent storage for processed images.
  - `.staging_images/` — temporary staging area used during image saving.
  - `tests/` — automated tests for application functionality.
- `resource/` — sample project resources.
- `test/` — local learning examples arranged by roadmap stage; this folder is currently excluded by `.gitignore`.
- `exercise/` — separate learning and experimentation files, including super-resolution evaluation.
- `ROADMAP.md` — learning checklist.
- `PROGRESS.md` — session progress and next learning plan.
- `WORKFLOW.md` — application flow and module responsibilities.

## Learning Examples

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

#### Evaluation Metrics

- **PSNR (Peak Signal-to-Noise Ratio):** Measures pixel-level similarity between the generated output and reference image. Higher values indicate greater numerical similarity.
- **SSIM (Structural Similarity Index):** Measures structural similarity between the generated output and reference image. Higher values indicate greater similarity.
- **Runtime:** Measures the processing time required by each method. Lower values indicate faster processing.

#### Experimental Results

The following results were obtained using `Alexei_Leonov.jpg`, with all outputs standardized to 3844 × 3075 pixels.

| Method | PSNR (dB) | SSIM | Runtime (seconds) |
|---|---:|---:|---:|
| Bicubic | 33.9431 | 0.8926 | 0.0116 |
| ESPCN | 15.5001 | 0.5581 | 0.7384 |
| Real-ESRGAN | 31.2559 | 0.8255 | 79.8095 |

#### Evaluation Workflow

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

#### Observations and Limitations

- **Bicubic:** Fastest method and achieved the highest PSNR and SSIM in this experiment. However, interpolation cannot reconstruct genuinely missing image details.
- **ESPCN:** Requires more processing time than Bicubic. Its relatively low evaluation scores may be related to the limited training dataset and model training process.
- **Real-ESRGAN:** Produced visually detailed results and achieved higher PSNR and SSIM than ESPCN. However, it required significantly more processing time. Its generative approach may introduce plausible details that do not accurately represent the original image.

PSNR and SSIM do not fully represent perceived image quality. Furthermore, this experiment uses only one reference image, so the results should not be treated as universal rankings of the three approaches.

## Current Development Status

The current development focus is **Stage 11 — Final Application**.

### Recent Progress

- Implemented persistent image storage using a dedicated `saved_images/` directory.
- Added SQLite-backed gallery metadata storage.
- Implemented a staging and publishing workflow to reduce the risk of incomplete image saves.
- Added recovery for interrupted image-saving operations.
- Implemented gallery image downloading and deletion.
- Added automatic expiration and cleanup of images after 30 days.
- Added synchronization between stored image files and database records.
- Added seven automated storage and gallery tests. All seven passed.
- Manually verified image persistence after restarting the application, downloading images, and deleting gallery images.

The super-resolution models and Real-ESRGAN inference workflow remain experimental learning components. They are not integrated into the desktop application.

No AI model is currently integrated into or bundled with the application. Model and dataset licensing will be documented if they are added to the project.