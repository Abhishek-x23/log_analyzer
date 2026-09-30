from analyzer.parser import analyze_logs, parse_log_line


def test_parse_valid_line():
    line = (
        "2026-09-18 10:23:45 ERROR "
        "payment-service Connection timeout after 30s"
    )

    result = parse_log_line(line)

    assert result is not None
    assert result["level"] == "ERROR"
    assert result["service"] == "payment-service"


def test_parse_invalid_line():
    line = "error billing-service No Auth token"

    assert parse_log_line(line) is None


def test_analyze_logs():
    logs = [
        "2026-09-18 10:23:45 ERROR payment-service Connection timeout",
        "2026-09-18 10:23:46 INFO auth-service User login successful",
        "2026-09-18 10:23:47 ERROR payment-service Connection refused",
        "2026-09-18 10:24:01 WARN auth-service Response time degraded",
        "2026-09-18 10:24:15 ERROR billing-service Invalid account state",
        "2026-09-18 10:24:30 INFO payment-service Retry succeeded",
        "error billing-service No Auth token"
    ]

    result = analyze_logs(logs)

    assert result["total_lines"] == 7
    assert result["unparseable_lines"] == 1

    assert result["error_count_per_service"] == {
        "auth-service": 0,
        "billing-service": 1,
        "payment-service": 2
    }

    assert result["top_offender"] == "payment-service"
    