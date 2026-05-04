from datetime import datetime
from pathlib import Path
from collections  import Counter

from source.log_analysis.writers import write_host_csv, write_resource_csv, write_windows_csv, write_malformed_lines_csv
from source.log_analysis.models import MalformedLine
from source.log_analysis.config import TIMESTAMP_FORMAT

def test_write_host_csv(tmp_path: Path):
    hosts =Counter({'a.com':5 , 'b.com':3,'c.com':1})
    output_file = tmp_path / 'hosts.csv'
    write_host_csv(hosts,output_file,limit =10)
    
    content = output_file.read_text(encoding = 'utf-8')
    assert 'Host,Number of Requests' in content
    assert 'a.com,5' in content
    assert 'b.com,3' in content
    assert 'c.com,1' in content


def test_write_resource_csv (tmp_path:Path):
    resources = Counter({'/a':5000,'/b':3000,'/c':1000})
    output_file = tmp_path/ 'resources.csv'
    write_resource_csv(resources,output_file,limit=10)
    content = output_file.read_text(encoding='utf-8')
    assert 'Resources,Number of Byte' in content
    assert '/a,5000' in content
    assert '/b,3000' in content
    assert '/c,1000' in content

def test_write_windows_csv(tmp_path:Path):
    windows = [
        (datetime.strptime("01/Jul/1995:00:00:01 -0400", TIMESTAMP_FORMAT), 3),
    ]
    output_file = tmp_path / 'windows.csv'
    write_windows_csv(windows,output_file)
    content = output_file.read_text(encoding='utf-8')
    assert 'Windows Start Time,Number of Requests' in content
    assert '01/Jul/1995:00:00:01 -0400,3' in content

def test_write_malformed_lines_csv(tmp_path:Path):
    malformed_lines = [MalformedLine(line_number=1,reason='Invalid format',line_content='INVALID LOG LINE')]
    output_file = tmp_path / 'malformed_lines.csv'
    write_malformed_lines_csv(malformed_lines,output_file)

    content = output_file.read_text(encoding='utf-8')
    assert 'Line Number,Reason,Line Content' in content
    assert '1,Invalid format,INVALID LOG LINE' in content
 
