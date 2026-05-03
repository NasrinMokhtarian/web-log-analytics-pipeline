import logging
import argparse

parser = argparse.ArgumentParser(description="Log Analyzer CLI")
parser.add_argument("--log-level", default="INFO", help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
args = parser.parse_args()

logging.basicConfig(
    level=getattr(logging, args.log_level.upper(), None),
    format='%(asctime)s - %(levelname)s - %(message)s')