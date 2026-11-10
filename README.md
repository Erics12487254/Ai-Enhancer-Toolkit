# AI Enhancer Toolkit

**A desktop image-processing application powered by OpenCV and Real-ESRGAN.**

AI Enhancer Toolkit is a Python desktop application that allows users to resize images and enhance image resolution using Real-ESRGAN x2plus.

## About the Project

Finding high-resolution images isn't always easy. Sometimes, you find the image you want, but its resolution isn't suitable for your needs.

Online AI image-enhancement services can help, but many restrict their features behind paid subscriptions.

That's where this project idea came from.

I wanted to build a desktop application that lets users resize and enhance their images locally, without depending on paid online image-enhancement services.

The project also serves as a practical learning experience in Python, image processing, deep learning, software architecture, and application testing.

## Features

### Image Input
- Browse and select images from your computer.
- Drag and drop images directly into the application.
- Validate image input before processing.

### Image Processing

| Operation | Description | Availability |
|---|---|---|
| Resize | Change image dimensions to a specified width and height. | Available |
| AI Enhancement | Enhance images using Real-ESRGAN x2plus with 2× upscaling. | Available |
| Crop | Select and extract a region of an image. | Future development |
| Blur | Apply blur filters to images. | Future development |
| Sharpen | Improve perceived image sharpness. | Future development |

### AI Enhancement
- Uses the pretrained Real-ESRGAN x2plus model.
- Prepares the enhancement engine once per application session.
- Reuses the prepared engine for subsequent enhancement requests.
- Performs model preparation and image inference in background threads.
- Keeps the interface responsive during enhancement.

### Saved Images
- Automatically saves processed images.
- Displays saved results in a gallery with thumbnails.
- Allows users to download copies to another location.
- Allows users to delete saved results.

## Requirements, Installation & Getting Started

### 1. Prerequisites

| Requirement | Details |
|---|---|
| Python | **3.11.9** (recommended; use 64-bit CPython on Windows) |
| GUI support | Python installation with Tkinter |
| Dependencies | Packages listed in `requirements.txt` |
| Model weights | Real-ESRGAN x2plus checkpoint |

**Model location:**

`Project Ai Enhancer Toolkit/backend/models/RealESRGAN_x2plus.pth`

The model weights are included in the repository. Check the applicable model licensing terms before redistributing the weights or a packaged application containing them.

### 2. Set Up the Environment

Open PowerShell at the repository root. Install 64-bit Python 3.11 first. Use the Python launcher (`py`) to create the virtual environment with Python 3.11 explicitly; plain `python -m venv .venv` may select a different installed version, such as Python 3.14.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Confirm that `python --version` reports Python 3.11.x before installing dependencies. If `py -3.11` is not recognized, install Python 3.11 and reopen PowerShell. You can check which Python versions the launcher can find with `py -0p`.

NumPy, PyTorch, TorchVision, BasicSR, and Real-ESRGAN are pinned to versions that work together in the Python 3.11 environment. NumPy is kept at 1.26.4 because this PyTorch build can fail to bridge to NumPy 2.x, producing errors such as “NumPy is not available.” TorchVision is pinned to 0.16.2 because BasicSR 1.4.2 imports `torchvision.transforms.functional_tensor`, which is absent from newer TorchVision releases. Changing Python or upgrading these packages may require updating and rechecking the pins.

If PowerShell blocks environment activation, use the virtual environment's Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

To confirm which interpreter is active, run:

```powershell
python --version
```

If you already created `.venv` with the wrong Python version, or installed incompatible packages, close any application using it and recreate the environment from the repository root. This removes the existing virtual environment and its installed packages:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -3.11 -m venv .venv
\.venv\Scripts\Activate.ps1
python --version
python -m pip install -r requirements.txt
```

### 3. Launch the Application

From the repository root:

```powershell
python "Project Ai Enhancer Toolkit/gui.py"
```

### 4. Using the Application

| Step | Action |
|---|---|
| 1 | Browse for an image or drag and drop it into the input area. |
| 2 | Select **Resize the image** or **Enhance the image**. |
| 3 | For resizing, enter the target width and height, then select **Apply Resize**. |
| 4 | For enhancement, wait for engine preparation, then select **Apply Enhancement**. |
| 5 | Find the processed image in the saved-images gallery. |
| 6 | Download or delete the result as needed. |

**Note:** Enhancement intentionally has two stages: engine preparation and image processing. The prepared engine is reused throughout the application session.

## Architecture

The application follows a layered architecture that separates the graphical interface, application logic, background task execution, and image-processing backend.

### Application Structure

| Layer / Module | Responsibility |
|---|---|
| `gui.py` | Main frontend orchestrator. Builds the interface, handles user interactions, and communicates with the application layer. |
| `frontend/` | Contains reusable interface components and operation-specific views. |
| `frontend/task_runner.py` | Executes background tasks and returns results or errors through a thread-safe queue. |
| `main.py` | Application-layer orchestrator. Validates requests and coordinates loading, processing, saving, and gallery operations. |
| `backend/Load_Image/` | Handles image loading and validation using OpenCV. |
| `backend/Operate_Image/` | Contains image-processing operations, including resizing and AI enhancement. |
| `backend/Save_Image/` | Handles image storage, gallery listing, previews, downloads, and deletion. |
| `backend/models/` | Stores the pretrained Real-ESRGAN model weights. |

### Processing Workflow

```text
        User
         |
         v
      gui.py
   (Presentation)
         |
         v
      main.py
 (Application Logic)
         |
         v
   Image Loading
         |
         v
  Image Processing
         |
         v
   Image Storage
         |
         v
   Gallery Preview
         |
         v
    GUI Display
```

### Design Principles

| Principle | Implementation |
|---|---|
| Separation of concerns | Each module has a focused responsibility. |
| Backend independence | Backend modules do not depend on Tkinter or GUI components. |
| Centralized orchestration | `gui.py` handles frontend coordination, while `main.py` coordinates application workflows. |
| Responsive interface | Long-running enhancement tasks execute in background threads. |
| Thread safety | Worker threads return results through a queue; Tkinter widget updates happen on the main thread. |
| Reusable components | Frontend components and the prepared enhancement engine can be reused. |

### Error Handling

- Invalid or unsupported image files are rejected during loading or validation.
- Processing errors are returned to the application layer.
- Background task errors are passed back to the GUI through the task queue.
- Storage operations restrict deletion to files inside the managed saved-images directory.

## Saved Images

Processed images are stored locally inside:

`Project Ai Enhancer Toolkit/backend/Save_Image/saved_images/`

| Function | Behavior |
|---|---|
| Save | Stores processed images in the application's saved-images directory. |
| Gallery | Scans the directory and displays available images, newest first. |
| Preview | Generates thumbnails and displays image dimensions. |
| Download | Copies a saved image to a user-selected destination. |
| Delete | Removes a saved image from the managed directory. |

The gallery uses filesystem information rather than a database. Images are saved as JPEG by default.

## Testing

The project uses **pytest** to verify important application behavior.

After activating `.venv` from the setup instructions, install pytest into that environment:

```powershell
python -m pip install pytest
```

Then run the test suite from the repository root:

```powershell
python -m pytest "Project Ai Enhancer Toolkit/tests" -v
```

### Test Coverage

| Test Module | What It Tests |
|---|---|
| `test_main.py` | Application-layer validation, processing delegation, enhancement preparation, gallery operations, downloads, and deletion. |
| `test_task_runner.py` | Background execution, arguments, returned results, exception handling, and non-blocking behavior. |
| `test_application.py` | The application-level image-processing workflow. |

**Testing note:** Automated tests do not replace manual testing with the actual desktop interface, real images, and model weights.

### Manual AI Enhancement Check

Before a release, launch the application and verify the real model workflow:

1. Start the app using the launch command above.
2. Browse for a small, ordinary JPG or PNG image.
3. Select **Enhance the image ✦** and wait until the interface says the enhancement engine is ready.
4. Select **Apply Enhancement** and wait for the success message. CPU processing can take a while.
5. Confirm that a new result appears in the gallery, open or download it to confirm it is a readable image, and verify its dimensions are twice the input dimensions.

This check exercises model loading and real inference; the automated workflow test replaces the enhancement model with a test function and does not verify those steps.

## Limitations & Future Plans

### Current Limitations

| Area | Limitation |
|---|---|
| Enhancement hardware | The current enhancement engine runs on CPU. |
| Large images | Enhancement may consume substantial memory, particularly because tiling is disabled. |
| Image transparency | Images are loaded in OpenCV color mode, so alpha transparency is not retained. |
| Output format | Processed images are saved as JPEG by default. The GUI does not currently provide format selection. |
| Processing methods | Only resizing and AI enhancement are selectable in the current GUI. |
| Enhancement speed | CPU inference can take considerable time, especially with large inputs. |

### Future Development

- [ ] Improve the crop operation and integrate it into the GUI.
- [ ] Improve the resize interface and processing controls.
- [ ] Develop a more flexible sharpening operation.
- [ ] Explore automatic filter selection based on image characteristics.
- [ ] Experiment with brightness, contrast, and color adjustments.
- [ ] Explore additional frontend options while preserving backend independence.
- [ ] Investigate image tiling and hardware acceleration for faster enhancement.
- [ ] Consider output-format selection and improved image transparency support.

## Acknowledgements

This project uses third-party open-source libraries and pretrained model weights, including:

- OpenCV
- PyTorch
- Real-ESRGAN
- BasicSR
- TkinterDnD2

Please refer to the relevant upstream projects and their licence notices for attribution and redistribution requirements.

---

**Built as a personal learning project exploring Python, computer vision, deep learning, and software architecture.**
