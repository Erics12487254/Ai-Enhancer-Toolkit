from pathlib import Path


# Find the backend directory so the model path works
# regardless of where the application is launched.
BASE_DIR = Path(__file__).resolve().parent.parent

# Location of the pretrained Real-ESRGAN x2 model.
MODEL_PATH = BASE_DIR / "models" / "RealESRGAN_x2plus.pth"


class EnhancementEngine:
    """Initialize and manage the Real-ESRGAN enhancement engine."""

    def __init__(self):
        # Import heavy dependencies here instead of at the top of the file.
        # This delays their loading until the user starts enhancement preparation.
        from basicsr.archs.rrdbnet_arch import RRDBNet
        from realesrgan import RealESRGANer

        # Make sure the pretrained model file exists before initialization.
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Pretrained model not found: {MODEL_PATH}"
            )

        # Create the RRDBNet neural network architecture.
        # These parameters must match the RealESRGAN_x2plus model.
        model = RRDBNet(
            num_in_ch=3,       # Number of input color channels (BGR).
            num_out_ch=3,      # Number of output color channels.
            num_feat=64,       # Number of feature channels.
            num_block=23,      # Number of RRDB blocks.
            num_grow_ch=32,    # Growth channels inside each dense block.
            scale=2,           # Model upscaling factor: 2×.
        )

        # Connect the neural network architecture with the pretrained weights.
        # RealESRGANer manages the model inference process.
        self.upsampler = RealESRGANer(
            scale=2,
            model_path=str(MODEL_PATH),
            model=model,
            tile=0,            # Process the image without splitting it into tiles.
            tile_pad=10,       # Padding used when tile processing is enabled.
            pre_pad=0,         # Additional padding before inference.
            half=False,        # Use full precision (FP32).
            gpu_id=None,       # Automatically select the available device.
        )

    def enhance(self, image):
        """Run Real-ESRGAN inference on the supplied image."""

        # Perform 2× upscaling using the initialized enhancement engine.
        enhanced_image, _ = self.upsampler.enhance(
            image,
            outscale=2,
        )

        # Return the processed image to the application layer.
        return enhanced_image


# Store one shared enhancement engine.
# None means the engine has not been initialized yet.
_engine = None


def prepare_enhancement():
    """Initialize the enhancement engine if it has not been loaded."""

    global _engine

    # Create the engine only once.
    # Subsequent calls reuse the existing model and loaded weights.
    if _engine is None:
        _engine = EnhancementEngine()


def enhance_image(image):
    """Enhance an image using the initialized engine."""

    # Safety check: prepare the engine if it hasn't been initialized.
    # This also allows enhance_image() to work independently.
    prepare_enhancement()

    # Reuse the cached engine to perform inference.
    return _engine.enhance(image)
