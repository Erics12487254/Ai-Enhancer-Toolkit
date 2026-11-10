
import queue
import threading


class TaskRunner:
    """Execute application tasks without blocking the GUI."""

    def __init__(self):
        # Store completed task results for the GUI to retrieve.
        self.results = queue.Queue()

    def run(self, task_name, function, *args, **kwargs):
        """Execute a supplied function in a background thread."""

        def worker():
            try:
                # Execute the requested application function.
                result = function(*args, **kwargs)

            except Exception as error:
                # Send the exception back to the GUI.
                self.results.put((task_name, None, error))

            else:
                # Send the successful result back to the GUI.
                self.results.put((task_name, result, None))

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()
