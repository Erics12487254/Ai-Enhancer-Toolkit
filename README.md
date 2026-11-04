# AI Enhancer Toolkit

A Python image-processing application with a drag-and-drop desktop interface and a persistent image gallery. The desktop app supports resize, crop, blur, sharpen, and Real-ESRGAN enhancement.

Real-ESRGAN runs on the CPU in the current setup and may take considerably longer than the traditional image-processing operations. The supplied model weights are expected at `Project Ai Enhancer Toolkit/models/RealESRGAN_x2plus.pth`.

## Features

- Select an image by dragging it into the app or browsing for it.
- Resize, crop, blur, sharpen, or enhance an image.
- Validate selected images and display processing errors.
- Save results in `Project Ai Enhancer Toolkit/saved_images/`.
- Browse, download, and delete saved images.
- Keep saved images after closing and reopening the application.

The GUI currently uses the backend defaults for resize and crop. It does not yet provide controls for operation settings or output format. Processed results are saved as JPEG by default.

## Requirements

- Python 3.10 or newer
- Tkinter support in the Python installation
- Packages listed in `requirements.txt`
- Real-ESRGAN model weights at the path listed above to use enhancement

## Installation

From the repository root, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the Application

From the repository root:

```powershell
python "Project Ai Enhancer Toolkit/gui.py"
```

1. Drop an image into the input area or click it to browse.
2. Choose an operation.
3. Select **Process Image**.
4. Find the result in the gallery.
5. Use **Download** to copy a gallery image elsewhere, or **Delete** to remove it.

The current interface runs processing synchronously. Long operations, especially Real-ESRGAN enhancement, may temporarily make the window unresponsive.

## Run the Tests

Install pytest if it is not already available:

```powershell
python -m pip install pytest
```

Run the tests from the application directory:

```powershell
cd "Project Ai Enhancer Toolkit"
python -m pytest tests/ -v
```

## Project Structure

```text
Ai Enhancer Toolkit/
├── Project Ai Enhancer Toolkit/
│   ├── blur.py
│   ├── brightness.py
│   ├── color.py
│   ├── config.py
│   ├── contrast.py
│   ├── crop.py
│   ├── enhance.py
│   ├── gallery.py
│   ├── gui.py
│   ├── loader.py
│   ├── main.py
│   ├── preview.py
│   ├── resize.py
│   ├── save.py
│   ├── scaler.py
│   ├── sharpen.py
│   ├── models/
│   ├── saved_images/
│   └── tests/
├── exercise/
├── resource/
├── AI_ASSISTANCE_RULES.md
├── PROGRESS.md
├── README.md
├── ROADMAP.md
├── WORKFLOW.md
└── requirements.txt
```

### Application Modules

- `gui.py` — collects user input and displays results and gallery previews.
- `main.py` — validates requests and orchestrates backend work.
- `loader.py` — loads images into OpenCV arrays.
- `resize.py`, `crop.py`, `blur.py`, `sharpen.py`, and `enhance.py` — implement processing operations.
- `gallery.py` — finds saved images and returns gallery records.
- `preview.py` — prepares thumbnail data and image dimensions for the frontend.
- `save.py` — saves, copies, and deletes image files.
- `tests/` — automated tests for image operations and storage behavior.

## Learning and Evaluation Work

The repository also contains learning examples and experiments for machine learning, PyTorch, super-resolution, and image-quality evaluation. These experiments are separate from the desktop workflow unless explicitly integrated above.

The Stage 10 evaluation uses a single reference image. Its PSNR and SSIM values are useful for learning, but they do not establish a general ranking of the methods. Generative enhancement can produce plausible details that were not present in the source image.

## Limitations and Model Terms

- The GUI currently provides no controls for resize dimensions, crop coordinates, or save format.
- Images are loaded using OpenCV's color mode, so alpha transparency is not retained by the current workflow.
- Real-ESRGAN inference uses the CPU in the current configuration and can be slow.
- Review the model and dataset terms before redistributing weights or datasets.

See `ROADMAP.md` for planned work and `PROGRESS.md` for recorded progress.
