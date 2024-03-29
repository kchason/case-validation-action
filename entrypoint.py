import os
import sys

from case_utils.case_validate import validate
from case_utils.case_validate.validate_types import ValidationResult
from case_utils.ontology.version_info import CURRENT_CASE_VERSION
from github import Github

# Get the environment variables as the settings for the validation
case_version: str = os.environ.get("CASE_VERSION", CURRENT_CASE_VERSION)
abort_on_failure: bool = (
    os.environ.get("CASE_VALIDATE_ABORT", "false").lower() == "true"
)
case_path: str = os.environ.get("CASE_PATH", "/opt/json/")
extension_filter: str = os.environ.get("CASE_EXTENSION_FILTER", "")
report_in_pr = os.getenv("REPORT_IN_PR", "false").lower() == "true"
github_repo = os.getenv("GITHUB_REPOSITORY")
github_token = os.getenv("GITHUB_TOKEN")
github_pull_request = os.getenv("GITHUB_PULL_REQUEST", 0)
# Convert the github_pull_request to an int if it's numeric, otherwise set it to an empty string
github_pull_request = int(github_pull_request) if github_pull_request.isnumeric() else 0

# Print the variables with their keys for debugging
print(f"CASE_VERSION: {case_version}")
print(f"CASE_VALIDATE_ABORT: {abort_on_failure}")
print(f"CASE_PATH: {case_path}")
print(f"CASE_EXTENSION_FILTER: {extension_filter}")
print(f"REPORT_IN_PR: {report_in_pr}")
print(f"GITHUB_REPOSITORY: {github_repo}")
print(f"GITHUB_TOKEN: {'******' if github_token else ''}")
print(f"GITHUB_PULL_REQUEST: {github_pull_request}")

results: list[dict] = []
success: bool = True


def generate_html_report(reports: list[dict]) -> str:
    """
    Generate an HTML report of the validation results for use in GitHub comments
    :param reports: The list of validation results
    :return: The HTML report
    """
    html = "<!--AUTOMATED VALIDATION RESULTS-->"
    html += "<h1>CASE Validation Results</h1>"
    html += "<h2>Summary</h2>"
    html += "<table>"
    html += "<tr><th>File</th><th>Valid</th></tr>"
    for report in reports:
        html += f'<tr><td>{report["file"]}</td><td>'
        html += (
            "<span>&#x2713;</span>" if report["conforms"] else "<span>&#x2717;</span>"
        )
        html += "</td></tr>"
    html += "</table>"
    html += "<h2>Details</h2>"
    for report in reports:
        html += f'<details><summary><h3>{report["file"]}&nbsp;'
        html += (
            "<span>&#x2713;</span>" if report["conforms"] else "<span>&#x2717;</span>"
        )
        html += f'</h3></summary><pre>{report["output"]}</pre></details>'
    return html


def annotate_pr(message: str) -> None:
    """
    Annotate the GitHub Pull Request with the given message
    :param message: The message to annotate the PR with
    :return: None
    """
    # If we're not reporting in the PR, just print the message and return
    if not report_in_pr:
        print("Not reporting in pull request")
        return

    # Get the GitHub values from the environment
    if not github_repo:
        print("No GitHub repository provided")
        exit(1)
    if not github_token:
        print("No GitHub token provided")
        exit(1)
    if not github_pull_request or github_pull_request == 0:
        print("No GitHub pull request provided; not reporting in pull request")
        return

    # Login to GitHub and get the PR object
    client = Github(github_token)
    repo = client.get_repo(github_repo)
    pr = repo.get_pull(github_pull_request)

    # Delete all existing comments that start with
    # "<!--AUTOMATED VALIDATION RESULTS-->" to avoid duplicates
    for comment in pr.get_issue_comments():
        if comment.body.startswith("<!--AUTOMATED VALIDATION RESULTS-->"):
            comment.delete()

    # Create a new comment with the message
    pr.create_issue_comment(message)


# Determine if the provided path is a directory. If so, then there is filtering
# and other handling to address. If it is a file, then it is assumed it should
# be validated.
if os.path.isdir(case_path):
    # Get the list of files that end with the provided extension
    files: list = [
        os.path.join(case_path, f)
        for f in os.listdir(case_path)
        if f.endswith(extension_filter)
    ]

    print(f"Validating {len(files)} files at: {case_path}")
    # Loop through each file and validate it
    has_failure: bool = False
    for f in files:
        result: ValidationResult = validate(
            f, case_version=case_version, abort_on_first=abort_on_failure
        )

        print(f"Validating file at: {f}")
        print(result.text)
        results.append(
            {"file": f, "conforms": result.conforms, "output": result.text}
        )  # noqa: E501

        if not result.conforms:
            has_failure = True
            if abort_on_failure:
                sys.exit(1)

    # If there was a failure, then exit with a non-zero exit code
    success = not has_failure

elif os.path.isfile(case_path):
    # If the path is a file, then it is assumed it should be validated
    # and ignore the filter
    result: ValidationResult = validate(
        case_path, case_version=case_version, abort_on_first=abort_on_failure
    )

    print(f"Validating file at: {case_path}")
    print(result.text)
    success = result.conforms
    results.append(
        {"file": case_path, "conforms": result.conforms, "output": result.text}
    )

else:
    print(f"${case_path} is not a valid path and the validation cannot continue")
    sys.exit(1)

# Annotate the PR
annotate_pr(generate_html_report(results))

# Exit with a non-zero exit code if there were any failures
if not success:
    exit(1)
