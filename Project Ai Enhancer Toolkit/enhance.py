from pathlib import Path

# Import the neural network architecture.
from basicsr.archs.rrdbnet_arch import RRDBNet

# Import the Real-ESRGAN inference engine.
from realesrgan import RealESRGANer


# Get the directory containing this Python file.
BASE_DIR = Path(__file__).resolve().parent

# Locate the pretrained Real-ESRGAN x2plus weights.
MODEL_PATH = BASE_DIR / "models" / "RealESRGAN_x2plus.pth"


class EnhancementEngine:

    def __init__(self):
        # Store the Real-ESRGAN engine here.
        self.upsampler = None

        # Make sure the pretrained model file exists.
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Pretrained model not found: {MODEL_PATH}"
            )

        # Define the neural network architecture.
        # These parameters must match the pretrained x2plus weights.
        model = RRDBNet(
            num_in_ch=3,       # Number of input image channels.
            num_out_ch=3,      # Number of output image channels.
            num_feat=64,       # Number of internal feature channels.
            num_block=23,      # Number of RRDB blocks.
            num_grow_ch=32,    # Growth channels inside dense blocks.
            scale=2            # Native upscaling factor.
        )

        # Initialize the Real-ESRGAN engine and load pretrained weights.
        self.upsampler = RealESRGANer(
            scale=2,
            model_path=str(MODEL_PATH),
            model=model,
            tile=0,            # Disable tiled processing.
            tile_pad=10,       # Padding used when tiled processing is enabled.
            pre_pad=0,         # No additional padding before processing.
            half=False,        # Use full precision.
            gpu_id=None        # Use CPU.
        )

    def enhance(self, image):
        # Receive an already-loaded image from main.py.

        # Run AI enhancement at 2x the original resolution.
        enhanced_image, _ = self.upsampler.enhance(
            image,
            outscale=2
        )

        # Return the enhanced image to main.py.
        return enhanced_image


# Create the engine only when enhancement is first requested.
# Reuse it for subsequent images instead of loading the model again.
_engine = None


def enhance_image(image):
    global _engine

    if _engine is None:
        _engine = EnhancementEngine()

    return _engine.enhance(image)