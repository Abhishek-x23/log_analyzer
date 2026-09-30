import re
from datetime import datetime
from collections import defaultdict


LOG_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) "
    r"(\d{2}:\d{2}:\d{2}) "
    r"(DEBUG|INFO|WARN|ERROR|FATAL) "
    r"(\S+) "
    r"(.+)$"
)


def parse_log_line(line):
    """
    Parse a single log line.
    Return a dictionary if valid, otherwise None.
    """

    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    date, time, level, service, message = match.groups()

    try:
        datetime.strptime(
            f"{date} {time}",
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return None

    return {
        "date": date,
        "time": time,
        "level": level,
        "service": service,
        "message": message
    }


def analyze_logs(lines):
    """
    Analyze log lines and return a summary.
    """

    total_lines = 0
    unparseable_lines = 0
    error_counts = defaultdict(int)

    for line in lines:
        total_lines += 1

        log = parse_log_line(line)

        if log is None:
            unparseable_lines += 1
            continue

        service = log["service"]
        level = log["level"]

        # Include every valid service, even if it has no errors.
        error_counts[service] += 0

        # Treat both ERROR and FATAL as errors.
        if level in ("ERROR", "FATAL"):
            error_counts[service] += 1

    if error_counts and any(error_counts.values()):
        top_offender = min(
            error_counts,
            key=lambda service: (-error_counts[service], service)
        )
    else:
        top_offender = None

    return {
        "total_lines": total_lines,
        "unparseable_lines": unparseable_lines,
        "error_count_per_service": dict(sorted(error_counts.items())),
        "top_offender": top_offender
    }