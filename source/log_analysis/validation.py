import csv
from pathlib import Path


def _read_csv_row(file_path:Path) -> list[list[str]]:
    with open (file_path,'r', encoding = 'utf-8', newline = '') as file:
        reader =csv.reader(file)
        return list(reader)

def hosts_csv_validate(file_path:Path, limit:int=10) -> None:
    rows = _read_csv_row(file_path)
    if not rows:
        raise ValueError("hosts.csv is empty")
    header = rows[0]
    expected_header = ['Host', 'Number of Requests']
    if header != expected_header:
        raise ValueError(f"hosts.csv header is incorrect. Expected: {expected_header}, Found: {header}")
    raw_data = rows[1:]
    if len(raw_data) > limit:
        raise ValueError(f"hosts.csv has more than {limit} entries")
    previous_count = None
    for row in raw_data :
        if len(row) != 2:
            raise ValueError("hosts.csv has incorrect number of columns {row}")
        host, count_text = row
        count = int(count_text)
        if count < 0:
            raise ValueError(f"hosts.csv has negative count for host {host}")
        if previous_count is not None and count > previous_count:
            raise ValueError("hosts.csv is not sorted in descending order")
        previous_count = count


def resources_csv_validate(file_path:Path, limit:int=10) -> None: 
    rows = _read_csv_row(file_path)
    if not rows:
        raise ValueError("resources.csv is empty")
    header = rows[0]
    expected_header = ['Resources', 'Number of Byte']
    if header != expected_header:
        raise ValueError(f"resources.csv header is incorrect. Expected: {expected_header}, Found: {header}")
    raw_data = rows[1:]
    if len(raw_data) > limit:
        raise ValueError(f"resources.csv has more than {limit} entries")
    previous_byte = None
    for row in raw_data:
        if len(row) != 2:
            raise ValueError(f"resources.csv has incorrect number of columns {row}")
        resource, byte_text = row
        byte = int(byte_text)
        if byte < 0:
            raise ValueError(f"resources.csv has negative byte count for resource {resource}")
        if previous_byte is not None and byte > previous_byte:
            raise ValueError("resources.csv is not sorted in descending order")
        previous_byte = byte

def windows_csv_validate(file_path:Path, limit:int=10) -> None:
    rows = _read_csv_row(file_path)
    if not rows:
        raise ValueError("windows.csv is empty")
    header = rows[0]
    expected_header = ['Windows Start Time', 'Number of Requests']
    if header != expected_header:
        raise ValueError(f"windows.csv header is incorrect. Expected: {expected_header}, Found: {header}")
    raw_data = rows[1:]
    if len(raw_data) > limit:
        raise ValueError(f"windows.csv has more than {limit} entries")
    previous_count = None
    seen_timestamps = set()

    for row in raw_data:
        if len(row) != 2:
            raise ValueError(f"windows.csv has incorrect number of columns {row}")
        window_start, count_text = row
        count = int(count_text)
        if count < 0:
            raise ValueError(f"windows.csv has negative count for window starting at {window_start}")
        if window_start in seen_timestamps:
            raise ValueError(f"windows.csv contains duplicate window start time: {window_start}")
        if previous_count is not None and count > previous_count:
            raise ValueError("windows.csv is not sorted in descending order")
        previous_count = count
        seen_timestamps.add(window_start)