from collections import Counter
from datetime import datetime, timedelta
from log_analysis.parser import parse_line
from log_analysis.models import LogRecord, MalformedLine
from typing import List
from pathlib import Path




def read_log_file(filepath:Path) -> tuple[Counter,Counter,Counter,List[datetime],List[MalformedLine]]:   
    host_counts : Counter = Counter()
    response_size : Counter = Counter()
    status_code : Counter = Counter()
    timestamps : List[datetime] = []
    malformed_lines : List[MalformedLine] = []

    with open (filepath,'r', encoding = 'ascii', errors = 'replace') as file:
        for line_number,line in enumerate(file, start=1):
            parsed, error_reason = parse_line(line)
            if parsed is  None:
                malformed_lines.append(
                    MalformedLine(
                        line_number=line_number, 
                        reason=error_reason or "unknown parsing error", 
                        line_content=line.strip()
                    )
                )
                continue
            host_counts[parsed["host"]] +=1
            response_size [parsed["resource"]] += parsed["response_size"]
            status_code[parsed["status_code"]] +=1
            timestamps.append(parsed["timestamp"])
    return host_counts,response_size,status_code,timestamps, malformed_lines
    

def calculate_busiest_windows (timestamps : List[datetime],limit : int = 10) -> List[tuple[datetime,int]]:
    if not timestamps:
        return []
    sorted_timestamps = sorted(timestamps)
    results : List[tuple[datetime,int]] = []
    end_index = 0
    one_hour = timedelta(hours=1)
    for start_index in range(len(sorted_timestamps)):
        if start_index > 0 and sorted_timestamps[start_index] == sorted_timestamps[start_index - 1]:
            continue
        start_time = sorted_timestamps[start_index]
        window_end_time = start_time + one_hour
        while end_index < len(sorted_timestamps) and sorted_timestamps[end_index] < window_end_time:
            end_index +=1
        count  = end_index - start_index
        results.append((start_time, count))
    
    results.sort(key=lambda x: (-x[1], x[0]))
    return results[:limit]
