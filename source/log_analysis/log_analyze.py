

from datetime import datetime, timedelta
from collections import Counter
import csv
import logging


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)



def extract_resource(request):

   parts = request.split()
   if len(parts) >= 2 and parts[1].startswith("/"):
       return parts[1]
   
   else:
      return None
   
def parse_line(line):     
    # Host is the first value before the first space
    
    try:
        host = line.split()[0]

        # Timestamp is between [ and ]
        time_string = line.split("[",1)[1].split("]",1)[0]
        timestamp = datetime.strptime(time_string, TIMESTAMP_FORMAT)
        # Request is between " and "
        request = line.split('"',2)[1]
        # After request we expect: response code and  size
        response_parts = line.split('"',2)[2].strip().split()
        
        if len(response_parts) < 2:
            return None , "missing status code or response size"
        
        status_code = response_parts[0]
        response_size = response_parts[1]

        if not status_code.isdigit() or len(status_code) != 3:
            return None, f"Invalid status_code: {status_code}"
        
        if response_size == '-':
            response_size = 0
        else:
            response_size = int(response_size)
        
        # Extract resource from request
        resource = extract_resource(request) 
        if resource is None:
                return None, f"Invalid resource in request:{request}"
       
        return{
            "host": host,
            "timestamp": timestamp,
            "response_size": response_size,
            "resource": resource,
            "status_code": status_code
        }, None
    except (IndexError, ValueError) as e:
        return None, str(e)

       
def read_log_file(filepath):   
    host_counts = Counter()
    resource_size = Counter()
    status_code = Counter()
    timestamps = []
    skipped_lines = 0
    malformed_lines = []

    with open (filepath,'r', encoding = 'ascii', errors = 'replace') as file:
        for line_number,line in enumerate(file, start=1):
            parsed, error_reason = parse_line(line)
            if parsed is  None:
                skipped_lines +=1
                malformed_lines.append((line_number,error_reason,line.strip() ))
                continue
            host_counts[parsed["host"]] +=1
            resource_size [parsed["resource"]] += parsed["response_size"]
            status_code[parsed["status_code"]] +=1
            timestamps.append(parsed["timestamp"])
    return host_counts,resource_size,status_code,timestamps,skipped_lines, malformed_lines
    

def calculate_busiest_windows (timestamps,limit =10):
    if not timestamps:
        return []
    sorted_timestamps = sorted(timestamps)
    results = []
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

def write_hosts_csv(hosts,output_path):
    with open(output_path,'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Host","Number of Requests"])

        for host, count in hosts.most_common(10):
            writer.writerow([host, count])  
    logging.info("hosts.csv written successfully.")
def write_resources_csv(resources, output_path):
    with open (output_path,'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Resource","Number of Bytes"])

        for resource, byte in resources.most_common(10):
            writer.writerow([resource,byte])
    
    logging.info("resources.csv written successfully.")

def write_status_code_csv(status_code, output_path):
    with open(output_path, 'w', encoding = 'utf-8',newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(["status_codes","Number of Occurances"])
        for status_code, count in status_code.most_common(10):
            writer.writerow([status_code,count])

def write_windows_csv(windows, output_path):
    with open(output_path,'w',encoding = 'utf-8', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(["Window Start Time","Number of Requests"])
        for start_time, count in windows:
            writer.writerow([start_time.strftime(TIMESTAMP_FORMAT), count])
    logging.info("windows.csv written successfully.")

def write_malformed_line_csv(malformed_lines, output_path):
        with open (output_path,'w',encoding = 'utf-8', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(["Line Number","Error Reason","Line Content"])
            for line_number, error_reason, line_count in malformed_lines:
                writer.writerow([line_number,error_reason,line_count])
        logging.info("malformed_lines.csv written successfully.")
    
def main():
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Started Processing log file.")
    host_counts, resource_bytes, status_code,timestamps, skipped_lines, malformed_lines = read_log_file(INPUT_FILE)
    write_hosts_csv(host_counts, OUTPUT_DIR / "hosts.csv")
    write_resources_csv(resource_bytes, OUTPUT_DIR / "resources.csv")
    windows = calculate_busiest_windows(timestamps)
    write_windows_csv(windows, OUTPUT_DIR / "windows.csv")
    write_status_code_csv(status_code,OUTPUT_DIR / "status_codes.csv")
    write_malformed_line_csv(malformed_lines, OUTPUT_DIR / "malformed_lines.csv")
    logging.info("Skipped %s malformed Lines",skipped_lines)
    logging.info("Output Directory : %s", OUTPUT_DIR)

    # print("hosts.csv written successfully.")
    # print("resources.csv written successfully.")
    # print("windows.csv written successfully.")
    # print(f"Number of Hosts : {len(host_counts)}")
    # print(f"Number of UniqueResources: {len(resource_bytes)}")
    # print(f"Number of Timestamps: {len(timestamps)}")
    # print(f"Number of Skipped Lines: {skipped_lines}")
    
    
    
    
    
    
if __name__ == "__main__":
    main()

