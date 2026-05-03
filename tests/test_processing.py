from datetime import datetime
from source.log_analysis.processing import  calculate_busiest_windows
from source.log_analysis.models import MalformedLine  
from source.log_analysis.config import  TIMESTAMP_FORMAT

def test_calculate_busiest_windows_basic():
    timestamp = [
        datetime.strptime("01/Jul/1995:00:00:01 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:00:30:00 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:00:50:00 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:02:30:00 -0400", TIMESTAMP_FORMAT),
    ]
    result = calculate_busiest_windows(timestamp, limit=2)
    assert result[0][1] == 3
    assert len(result) == 2

def test_calculate_busiest_windows_empty():
    result = calculate_busiest_windows([], limit=5)
    assert result == []

def test_calculate_busiest_windows_duplicate_timestamps():
    timestamp = [
        datetime.strptime("01/Jul/1995:00:00:01 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:00:00:01 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:00:30:00 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:00:30:00 -0400", TIMESTAMP_FORMAT),
    ]
    result = calculate_busiest_windows(timestamp, limit=10)
    assert result[0][0] == timestamp[0]
    assert result[0][1] == 4  
    