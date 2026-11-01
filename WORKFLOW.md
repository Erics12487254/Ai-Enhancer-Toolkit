# Application Workflow

This document describes the application's workflow and the responsibilities of each module. It also serves as a learning guide while the GUI and image-processing features are developed.

The application separates its core logic from the user interface so that another frontend can be introduced in the future without rewriting the image-processing workflow.

## Intended User Workflow

1. **Drop an Image.** The user drags an image from File Explorer into the GUI's drop area.
2. **Validate the Image.** `gui.py` sends the dropped file path to `main.py`. `main.py` checks whether OpenCV can decode it. If validation fails, the GUI displays the returned error, and the invalid file is not retained as the selected input.
3. **Choose an Operation.** The user selects an available processing operation through the GUI.
4. **Process the Image.** When the user presses Process, `gui.py` sends the selected path and operation to `main.py`. `main.py` validates the request, loads the image, selects the processing function, and coordinates the workflow.
5. **Stage the Result.** `main.py` passes the processed image to `save.py`, which writes it to a temporary staging directory and returns its path.
6. **Register the Image.** `main.py` registers the image's metadata and paths in the SQLite database through `database/database.py`. The record initially has a `pending` status.
7. **Publish the Image.** `main.py` coordinates moving the staged image into the permanent `saved_images/` directory. Once publishing succeeds, the database record is marked `ready`.
8. **Display the Outcome.** The GUI displays a success message and refreshes the gallery. If an operation fails, the GUI displays an appropriate error message.
9. **Browse the Gallery.** The user can view previously processed images stored in the gallery, including images from earlier application sessions.
10. **Download an Image.** The user selects Download for a gallery image and chooses a destination. The application copies the image to that location without removing the original gallery copy.
11. **Delete an Image.** The user selects Delete and confirms the action. The application removes both the image file and its corresponding database record.
12. **Maintain Stored Images.** The application performs maintenance during startup and periodically while running. This includes recovering interrupted saves, synchronizing missing files, removing expired images, and cleaning up orphaned staging files.

## Module Responsibilities

- **`gui.py` — Presentation Layer**
  - Displays the interface, including the image drop area, operation choices, gallery, and result messages.
  - Collects user input and sends application requests to `main.py`.
  - Displays validation results, processing status, and errors returned by `main.py`.
  - Displays gallery thumbnails and provides individual download and delete controls.
  - Uses file dialogs for choosing download destinations and confirmation dialogs for deletion.
  - Contains no image-processing, database, or application-level file-management logic.
  - Must remain replaceable by another frontend without requiring changes to the core application logic.

- **`main.py` — Application Logic and Coordination**
  - Acts as the central coordinator for the application workflow.
  - Provides UI-independent functions for validation, processing, storage coordination, gallery retrieval, downloading, deletion, and maintenance.
  - Validates selected image paths and operation requests.
  - Determines which processing operation to execute based on the user's request.
  - Coordinates image processing and saving by calling the appropriate modules.
  - Coordinates the staging, database registration, and publishing workflow.
  - Recovers interrupted saving operations when possible.
  - Coordinates gallery maintenance, including expiration cleanup and synchronization.
  - Handles results and errors returned by other modules and returns useful results or raises clear errors for the frontend.
  - Must not depend on a specific GUI framework or contain presentation logic.
  - Delegates specialized tasks to their respective modules instead of implementing everything in one file.

- **`loader.py` — Image Loading**
  - Loads image files using OpenCV.
  - Returns decoded image data to the application.
  - Raises a clear error when an image cannot be decoded.
  - Does not depend on the GUI.

- **`resize.py` — Image Resizing**
  - Contains the functions and logic required to resize an image.
  - Receives a decoded image from `main.py` and returns the resized image.
  - Does not load files or depend on the GUI.

- **`enhance.py` — Image Enhancement**
  - Contains the image-enhancement logic when implemented.
  - Receives the required inputs from `main.py`.
  - Returns the processed image or reports a processing failure.
  - Does not depend on the GUI.

- **Other Processing Modules**
  - Modules such as `crop.py`, `blur.py`, and `sharpen.py` contain their respective image-processing functions.
  - Receive decoded image data and return processed image data.
  - Do not load files, manage the gallery, or depend on the GUI.

- **`save.py` — Image File Management**
  - Creates uniquely named staged image files.
  - Provides the paths used to publish staged images into `saved_images/`.
  - Moves staged images into permanent storage.
  - Provides functions for deleting image files and copying images to download destinations.
  - Keeps image file operations separate from database operations.
  - Does not depend on the GUI.

- **`database/database.py` — Gallery Database**
  - Manages the SQLite database and its connection.
  - Initializes the database and handles schema updates.
  - Stores image metadata, including output name, path, operation, dimensions, timestamp, settings, and status.
  - Supports registering images and updating their statuses.
  - Retrieves gallery records and individual image records.
  - Identifies expired images and supports database record deletion.
  - Synchronizes database records with the actual image files.
  - Does not store image data as database blobs or depend on the GUI.

- **`saved_images/` — Permanent Image Storage**
  - Stores the actual processed image files.
  - Keeps gallery images available across application sessions.
  - Does not contain the gallery metadata database.

- **`.staging_images/` — Temporary Image Storage**
  - Holds image files temporarily while they are being saved.
  - Allows the application to recover from certain interrupted saving operations.
  - Unreferenced staging files are removed during maintenance.

- **`tests/` — Automated Tests**
  - Contains automated tests for important application functionality.
  - Tests database operations, file storage, recovery, deletion, and downloading without requiring the GUI to be launched.

## Architecture Rules

1. **Separate presentation from application logic.** The GUI handles display and user interaction; `main.py` handles application logic and workflow coordination.
2. **Keep `main.py` as the coordinator.** It owns the overall workflow but delegates specialized processing, file management, and database tasks to their respective modules.
3. **Keep the frontend replaceable.** The core application must work independently of a specific GUI framework.
4. **Use a clear communication boundary.** The GUI communicates with the application through `main.py` rather than importing processing, saving, or database modules directly.
5. **Keep processing modules independent of the frontend.** Modules such as `resize.py`, `enhance.py`, and `save.py` must not require a GUI to function.
6. **Give each module a clear responsibility.** Avoid duplicating logic or placing unrelated responsibilities in the same module.
7. **Handle errors explicitly.** Failed validation, processing, saving, database operations, or file operations must produce clear errors that the frontend can display.
8. **Protect the original input.** Processed output must not overwrite the source image by default.
9. **Keep modules testable.** Application logic, database operations, and processing functions should be testable without launching the GUI wherever practical.
10. **Keep database and file storage synchronized.** Database records must correspond to actual stored images. Interrupted operations should be recoverable where possible.
11. **Keep image files separate from metadata.** Store image files in `saved_images/` and their metadata in SQLite.
12. **Make maintenance repeatable.** Recovery and cleanup operations should be safe to retry if an earlier maintenance attempt was interrupted.

## Storage and Recovery Workflow

The application uses SQLite for gallery metadata and ordinary files for image storage.

Because SQLite transactions and filesystem operations cannot share one atomic transaction, the application uses image statuses to coordinate saving and deletion.

### Saving an Image

1. `save.py` creates a uniquely named image inside `.staging_images/`.
2. `main.py` registers the image in SQLite with a `pending` status and its staging and final paths.
3. `save.py` moves the staged image into `saved_images/`.
4. `main.py` updates the database record to `ready`.
5. The gallery displays only records with a `ready` status.

### Recovering Interrupted Saves

During maintenance, `main.py` checks pending records:

- If the final image already exists, the record can be marked `ready`.
- If the staged image exists, the application can publish it and mark the record `ready`.
- If neither image exists, the unusable pending record is removed.
- Staging files that are not referenced by pending database records are removed as orphans.

This makes interrupted save operations recoverable without requiring the user to process the image again in every case.

### Deleting an Image

1. The database record is marked `deleting`.
2. The corresponding image file is removed.
3. The database record is deleted.

If file deletion fails, the record remains available for another cleanup attempt.

### Automatic Expiration

- Gallery images are retained for 30 days from their processing timestamp.
- Expired records are marked `deleting`.
- The application removes their image files and database records.
- Failed deletions can be retried during subsequent maintenance.

Maintenance runs when the application starts and periodically while it remains open.

## Current Implementation

Update this section as the implementation evolves.

- **`gui.py`:** Provides drag-and-drop image selection, operation selection, processing controls, result messages, and a gallery with image thumbnails and individual download and delete controls.
- **`main.py`:** Provides UI-independent functions for image validation, processing, saving coordination, recovery, maintenance, gallery retrieval, downloading, and deletion.
- **`loader.py`:** Uses `cv2.imread()` and raises a clear error when OpenCV cannot decode the image.
- **`resize.py`:** Receives an already loaded image and returns its resized version; it does not load files or depend on the GUI.
- **`enhance.py`:** Not implemented yet. The Enhance option is listed in the interface but does not currently perform enhancement.
- **`save.py`:** Creates staged image files, publishes them into permanent storage, and provides file deletion and copying functions.
- **`database/database.py`:** Manages SQLite initialization, schema migration, image metadata, record statuses, gallery retrieval, expiration, and synchronization.
- **`saved_images/`:** Stores the actual processed image files.
- **`.staging_images/`:** Temporarily stores image files before they are published into permanent storage.
- **`tests/`:** Contains automated tests for storage and gallery functionality. The current storage test suite contains seven tests, all of which have passed.
- **Gallery:** Images remain available after application restarts. Downloading copies an image without removing the gallery copy. Deleting removes both the image file and its database record.

Update these notes as behaviors change. Do not mark a workflow step complete merely because its code has been written. Mark it complete only after it works as intended and you can explain how the relevant modules participate.

## Learning Requirements

- Explain the purpose of each new function, method, validation, and module before or while introducing it.
- Prefer guiding the user through the implementation instead of writing the entire solution on their behalf.
- Explain why a particular approach is suitable and discuss reasonable alternatives when relevant.
- Verify that the user understands the changes made during each daily task.
- Keep implementation consistent with `ROADMAP.md` and follow its checklist from top to bottom.