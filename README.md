# Web Log Analytics Pipeline

This project is a production-minded Python implementation for processing web server access logs and generating analytics reports. It focuses not only on correctness, but also on engineering quality through structured project organization, typed data models, parser validation, malformed-record quarantine, automated tests, and output validation checks.

The pipeline produces reports for top hosts, top bandwidth-consuming resources, and busiest 60-minute traffic windows, while preserving malformed input lines for inspection and debugging.