import logging
import argparse
from pathlib import Path

from source.log_analysis.config import DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_DIR,HOSTS_FILE_NAME, RESOURCES_FILE_NAME, WINDOWS_FILE_NAME, MALFORMED_FILE_NAME

from source.log_analysis.processing import read_log_file,calculate_busiest_windows
from source.log_analysis.validation import  hosts_csv_validate, resources_csv_validate, windows_csv_validate
from source.log_analysis.writers import write_host_csv, write_resource_csv, write_windows_csv, write_malformed_lines_csv

def pars_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze web logs and generate analytics reports.")
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT_FILE, help='Path to the input log file')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT_DIR, help='Directory for output CSV files')
    parser.add_argument("--top-n",type=int,default=10,help="Number of top results to include in each report.")
    parser.add_argument("--write-malformed-lines",action="store_true",help="Write malformed lines to malformed_lines.csv.")
    parser.add_argument("--log-level",default="INFO",choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],help="Logging level.")

    return parser.parse_args()
def configure_logging(log_level: str) -> None:
    logging.basicConfig(level=getattr(logging, log_level.upper()),format="%(asctime)s - %(levelname)s - %(message)s")

def main() -> None:
    
    args = pars_args()
    configure_logging(args.log_level)
    

    input_file: Path = args.input
    output_dir: Path = args.output
    top_n = args.top_n

    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Started processing log file: %s", input_file)
    host_counts, resource_bytes,status_code, timestamps, malformed_lines = read_log_file(input_file)

    host_path = output_dir / HOSTS_FILE_NAME
    resource_path = output_dir / RESOURCES_FILE_NAME
    windows_path = output_dir / WINDOWS_FILE_NAME
    malformed_path = output_dir / MALFORMED_FILE_NAME

    write_host_csv(host_counts, host_path, limit =top_n)
    write_resource_csv(resource_bytes, resource_path, limit =top_n) 
    busiest_windows = calculate_busiest_windows(timestamps)
    write_windows_csv(busiest_windows, windows_path, top_n)
    
    if args.write_malformed_lines:
        write_malformed_lines_csv(malformed_lines, malformed_path) 
        logging.info("Wrote malformed lines file: %s", malformed_path) 
    
    hosts_csv_validate(host_path, limit=top_n)
    resources_csv_validate(resource_path, limit=top_n)
    windows_csv_validate(windows_path, limit=top_n)

    logging.info("Validation passed for all output files.")
    logging.info("Unique hosts: %s", len(host_counts))
    logging.info("Unique resources: %s", len(resource_bytes))
    logging.info("Total parsed timestamps: %s", len(timestamps))
    logging.info("Malformed lines: %s", len(malformed_lines))
    logging.info("Output directory: %s", output_dir)
    logging.info("Log analysis completed successfully.")

if __name__ == "__main__":
    main()