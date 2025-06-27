import importlib.util
import os

lib_dir = "tools"

def launch(module_name: str, args: dict):
    module_path = os.path.join(lib_dir, module_name, "run.py")  # <-- FIXED here

    if not os.path.exists(module_path):
        print(f"❌ Module file does not exist: {module_path}")
        return

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        print(f"❌ Failed to load spec for {module_name} at {module_path}")
        return

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "launch"):
        return module.launch(args)
    else:
        print(f"⚠️ The module '{module_name}' does not have a 'launch' function.")
