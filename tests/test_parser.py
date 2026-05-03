from source.log_analysis import parser
from source.log_analysis.config import TIMESTAMP_FORMAT
from datetime import datetime


def test_extract_resource_valid():
    request = "GET /history/apollo/ HTTP/1.0"
    assert parser.extract_resource(request) == "/history/apollo/"

def test_extract_resource_invalid():
    request = "INVALID REQUEST"
    assert parser.extract_resource(request) is None

def test_parse_line_valid():
    line = " unicomp6.unicomp.net - - [01/Jul/1995:00:00:06 -0400] \"GET /shuttle/countdown/ HTTP/1.0\" 200 3985 "
    record, error = parser.parse_line(line)
    assert record is not None
    assert error is None
    assert record.host == "unicomp6.unicomp.net"
    assert record.resource == "/shuttle/countdown/"
    assert record.response_size == 3985
    assert record.status_code == 200

def test_parse_line_invalid():
    line = " INVALID LOG LINE!"
    record, error = parser.parse_line(line)
    assert record is None
    assert error is not None
    