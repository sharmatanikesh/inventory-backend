from app.utils.config import Config

# Instantiate singleton config
_config = Config()

def NewConfig() -> Config:
    """Returns the singleton config instance."""
    return _config
