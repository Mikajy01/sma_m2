
import sys
import traceback

original_import = __import__

def debug_import(name, *args, **kwargs):
    print(f"Importing: {name}")
    print("Stack trace:")
    traceback.print_stack()
    return original_import(name, *args, **kwargs)

__builtins__.__import__ = debug_import

# Now import our main module
import main
