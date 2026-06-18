import os

def load_env(env_path: str = ".env", example_path: str = ".env_example") -> None:
    """
    Parses key-value pairs from env_path and loads/exports them into os.environ.
    If a key is missing from env_path but exists in example_path,
    we load the default fallback from the example file.
    """
    # 1. Parse example file to get keys/defaults if needed
    example_vars = {}
    if os.path.exists(example_path):
        with open(example_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    example_vars[k.strip()] = v.strip()

    # 2. Parse env file
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()

    # 3. Export to os.environ
    # Combine them (prioritize env_vars, fallback to example_vars)
    all_keys = set(example_vars.keys()) | set(env_vars.keys())
    for key in sorted(all_keys):
        val = env_vars.get(key)
        if val is None:
            val = example_vars.get(key, "")
            print(f"Warning: Environment variable '{key}' not found in {env_path}. Using fallback from {example_path}.")
        
        # Strip outer quotes if present
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
            
        os.environ[key] = val
