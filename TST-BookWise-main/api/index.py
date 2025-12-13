import sys
from pathlib import Path

# Add parent directory to sys.path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from mangum import Mangum
    from main import app
    
    # Create handler with Mangum
    handler = Mangum(app, lifespan="off")
    
except Exception as e:
    print(f"Error initializing handler: {e}")
    raise
