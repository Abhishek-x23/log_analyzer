import argparse
import requests
import sys


API_URL = "http://127.0.0.1:8000/analyze"


def analyze_file(file_path):
    try:
        with open(file_path, "rb") as file:
            response = requests.post(
                API_URL,
                files={"file": (file_path, file, "text/plain")},
                timeout=30
            )

        response.raise_for_status()
        return response.json()

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
        sys.exit(1)

    except requests.exceptions.HTTPError as error:
        print(f"API Error: {error}")
        sys.exit(1)

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")
        sys.exit(1)


def display_summary(result):
    print("\n========== LOG ANALYSIS ==========\n")

    print(f"Lines processed: {result['total_lines']:,}")
    print(f"Unparseable lines: {result['unparseable_lines']}")

    print("\nService Name\t\tError Count")
    print("----------------------------------")

    for service, count in result["error_count_per_service"].items():
        print(f"{service:<24}{count}")

    print("\n----------------------------------")
    print(f"Top offender: {result['top_offender'] or 'None'}")
    print("==================================")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze application log files using a REST API."
    )

    parser.add_argument(
        "file",
        help="Path to the log file"
    )

    args = parser.parse_args()

    result = analyze_file(args.file)
    display_summary(result)


if __name__ == "__main__":
    main()
    