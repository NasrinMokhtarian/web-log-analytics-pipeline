import csv
from datetime import datetime
from source.log_analysis.models import MalformedLine
from source.log_analysis.config import TIMESTAMP_FORMAT
from pathlib import Path


def write_host_csv (hosts, output_path: Path, limit:int=10) -> None:
    with open (output_path,'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Host', 'Number of Requests'])

        for host, count in hosts.most_common(limit):
            writer.writerow([host,count])

def write_resource_csv (resources, output_path:Path, limit:int=10):
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Resources','Number of Byte'])

        for resource, byte in resources.most_common(limit):
            writer.writerow([resource,byte])

def write_windows_csv(windows: list[tuple[datetime,int]], output_path:Path, limit:int=10)-> None:
    with open(output_path,'w',newline = '',encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Windows Start Time', 'Number of Requests'])

        for window_start,count in windows[:limit]:
            writer.writerow([window_start.strftime(TIMESTAMP_FORMAT),count])

def write_malformed_lines_csv(malformed_lines:list[MalformedLine], output_path:Path) -> None:
    with open(output_path,'w',newline='',encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Line Number','Reason','Line Content'])

        for item in malformed_lines:
            writer.writerow([item.line_number,item.reason,item.line_content])

     
