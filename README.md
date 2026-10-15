# AI Image Enhancer Toolkit

A Python image-processing project that is being developed into a portfolio application for AI-powered image enhancement. The current prototype includes a basic OpenCV resize workflow. Pretrained AI enhancement, evaluation, and a complete user interface are planned; they are not implemented yet.

## Current status

- Basic image resizing with OpenCV
- A small Tkinter interface scaffold
- AI enhancement and the portfolio application workflow are still in development

See [WORKFLOW.md](WORKFLOW.md) for the intended app flow, [AI_IMAGE_ENHANCER_ROADMAP.md](AI_IMAGE_ENHANCER_ROADMAP.md) for the week-by-week plan, and [ROADMAP.md](ROADMAP.md) for the learning checklist and recorded progress.

## Requirements

- Python 3.10 or newer
- Tkinter, for the planned graphical interface (usually included with standard Python installations; on some Linux systems it is a separate OS package)
- Packages listed in `requirements.txt`

## Setup

From the repository root, create and activate a virtual environment, then install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source .venv/bin/activate` instead.

## Run the current prototype

```powershell
python "Project Ai Enhancer Toolkit\main.py"
```

The current command-line prototype asks for an image path. Choose option 1 to resize it to 800 × 600 and save `saved_image.jpg` in the current working directory. The other menu choices are unfinished, and the AI enhancement workflow is not available yet.

## Project layout

```text
Project Ai Enhancer Toolkit/   Python application modules
resource/                      Sample project resources
ROADMAP.md                     Learning checklist and progress record
AI_IMAGE_ENHANCER_ROADMAP.md   Weekly portfolio release plan
requirements.txt               Python package dependencies
```

## Limitations

This is an early prototype. The resize workflow currently uses fixed output dimensions, and the planned AI model integration, complete interface, robust input validation, evaluation, and release documentation remain to be built. Check the roadmap for planned milestones.

## Credits and licensing

No AI model is bundled or used by the current prototype. When a model or external dataset is added, its license and attribution will be documented here. A project license should be added once the author chooses the reuse terms.
