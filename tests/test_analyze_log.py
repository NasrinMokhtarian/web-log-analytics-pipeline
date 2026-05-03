from datetime import datetime
from source.log_analysis.log_analyze import (parse_line, calculate_busiest_windows,extract_resource,TIMESTAMP_FORMAT)



def test_extract_resource_valid():
    request = "GET /history/apollo/ HTTP/1.0"
    assert extract_resource(request) == "/history/apollo/"

def test_extract_resource_invalid():
    request = "INVALID REQUEST"
    assert extract_resource(request) is None

def test_parse_line_valid():
    line = 'unicomp6.unicomp.net - - [01/Jul/1995:00:00:06 -0400] "GET /shuttle/countdown/ HTTP/1.0" 200 3985'
    parsed,error = parse_line(line)
    assert parsed["host"] == "unicomp6.unicomp.net"
    assert parsed ["resource"] == "/shuttle/countdown/"
    assert parsed["response_size"] == 3985
    assert error is None

def test_parse_line_size_dash():
    line = 'example.com - - [01/Jul/1995:00:00:01 -0400] "GET / HTTP/1.0" 200 -'
    parsed,error = parse_line(line)
    assert parsed["response_size"] == 0
    assert error is None

def test_parse_line_invalid():
    line = 'invalid log line'
    parsed,error = parse_line(line)
    assert parsed is None
    assert error is not None

def test_calculate_busiest_windows():
    timestamps = [
        datetime.strptime("01/Jul/1995:00:00:01 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:00:10:00 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:00:20:00 -0400", TIMESTAMP_FORMAT),
        datetime.strptime("01/Jul/1995:02:0:00 -0400", TIMESTAMP_FORMAT)
    ]

    results = calculate_busiest_windows(timestamps, limit=2)
    assert results[0][1] == 3



# python -m pytest -v tests/test_analyze_log.py