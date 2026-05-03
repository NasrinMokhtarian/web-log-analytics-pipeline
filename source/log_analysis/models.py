from dataclasses import dataclass
from datetime import datetime

@dataclass( frozen=True)
class LogRecord:
    host : str
    timestamp :datetime
    resource : str
    response_size :int
    status_code : int

@dataclass(frozen = True)
class MalformedLine:
    line_number : int
    reason : str
    line_content : str
    
