import logging
import os


def load_env(env_path=".env", override=False):
    """Load environment variables from .env file

    Args:
        env_path (str): Path to .env file
        override (bool): Whether to override existing environment variables
    """
    if not os.path.exists(env_path):
        logging.warning(f"{env_path} file not found")
        return

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')

            if override or key not in os.environ:
                os.environ[key] = value
