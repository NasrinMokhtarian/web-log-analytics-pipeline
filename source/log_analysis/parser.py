from typing import Optional
from datetime import datetime

from log_analysis.config import TIMESTAMP_FORMAT
from log_analysis.models import LogRecord

def extract_resource(request: str) -> Optional[str]:
    parts = request.split()
    if len(parts) >= 2 and parts[1].startswith("/"):
        return parts[1]
    return None

def parse_line(line:str) -> tuple[Optional[LogRecord], Optional[str]]:
    try:
        host = line.split()[0]
        timestamp_text = line.split("[",1)[1].split("]",1)[0]
        timestamp = datetime.strptime(timestamp_text, TIMESTAMP_FORMAT)
        request = line.split('"',2)[1]
        response = line.split('"',2)[2].strip().split()
        if len(response) < 2:
            return None, "missing status code or response byte"
        
        status_code_text = response[0]
        response_byte_text = response[1]
        

        if not status_code_text.isdigit() or len(status_code_text) != 3:
            return None, f"invalid status_code: {status_code_text}"
        status_code = int(status_code_text)
        if response_byte_text == "-":
            response_byte = 0
        else:
            response_byte = int(response_byte_text)

        resource =  extract_resource(request)
        if resource is None:
            return None, f"invalid resource in request:{request}"
        record = LogRecord(
            host = host,
            timestamp = timestamp,
            resource = resource,
            response_size =response_byte,
            status_code = status_code
        )
        return record, None

    except (IndexError, ValueError) as e:
        return None, str(e)

