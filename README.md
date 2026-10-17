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
- `ROADMAP.md` — learning checklist
- `PROGRESS.md` — session progress and next learning plan
- `WORKFLOW.md` — application flow and module responsibilities
- `AI_IMAGE_ENHANCER_ROADMAP.md` — portfolio development plan

No AI model is currently bundled or used. Model and dataset licensing will be documented if they are added.
