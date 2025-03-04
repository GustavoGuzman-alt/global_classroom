import warnings
warnings.filterwarnings(
    "ignore",
    message="You are using `torch.load` with `weights_only=False`",
    category=FutureWarning,
    module="whisper"
)

from gui.app import run_app

if __name__ == "__main__":
    run_app()
