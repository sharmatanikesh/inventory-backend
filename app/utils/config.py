import os
from app.utils.env import load_env

ProdEnv = "prod"
DevEnv = "dev"
LocalEnv = "local"

class Config:
    def __init__(self):
        # 1. Determine paths to .env and .env_example
        # assuming config.py is located at: app/utils/config.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
        
        env_path = os.path.join(project_root, ".env")
        example_path = os.path.join(project_root, ".env_example")
        
        # 2. Load and export env vars into os.environ
        load_env(env_path=env_path, example_path=example_path)

    def get_env_var(self, key: str, default: str = "") -> str:
        """Helper to fetch from os.environ."""
        return os.environ.get(key, default)

    def GetEnvironment(self) -> str:
        return self.get_env_var("ENV", DevEnv)

    def IsLocalEnvironment(self) -> bool:
        return self.GetEnvironment() in (DevEnv, LocalEnv)

    def GetDBHost(self) -> str:
        return self.get_env_var("DB_HOST", "localhost")

    def GetDBPort(self) -> str:
        return self.get_env_var("DB_PORT", "5432")

    def GetDBUser(self) -> str:
        return self.get_env_var("DB_USER", "postgres")

    def GetDBPassword(self) -> str:
        return self.get_env_var("DB_PASSWORD", "postgres")

    def GetDBName(self) -> str:
        return self.get_env_var("DB_NAME", "inventory")

    def GetDBSSLMode(self) -> str:
        return self.get_env_var("DB_SSLMODE", "disable")

    def GetDBTimeZone(self) -> str:
        return self.get_env_var("DB_TIMEZONE", "UTC")

    def GetDBSchema(self) -> str:
        return self.get_env_var("DB_SCHEMA", "public")
