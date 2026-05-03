from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_FILE = PROJECT_ROOT / "data" / "log.txt"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"

TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

HOSTS_FILE_NAME = "hosts.csv"
RESOURCES_FILE_NAME = "resources.csv"
WINDOWS_FILE_NAME = "windows.csv"
STATUS_CODES_FILE_NAME = "status_codes.csv"