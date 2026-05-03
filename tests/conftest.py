import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "source"
# This makes log_analysis importable in pytest.
sys.path.insert(0, str(SRC_PATH))    