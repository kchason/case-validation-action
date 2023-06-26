import os
import subprocess

from github import Github

# Define the global variables from the environment variables
case_path = os.getenv('CASE_PATH', './tests/data/')
extension_filter = os.getenv('FILTER_EXTENSION', '')
case_version = os.getenv('CASE_VERSION', 'case-1.2.0')
abort_on_error = os.getenv('CASE_VALIDATE_ABORT', False)
report_in_pr = bool(os.getenv('REPORT_IN_PR', False))


relative_path: str = ''
files: list[str] = []
results: list[dict] = []

def generate_html_report(results: list[dict]) -> str:
    """
    Generate an HTML report of the validation results for use in GitHub comments
    :param results: The list of validation results
    :return: The HTML report
    """
    html = '<h1>CASE Validation Results</h1>'
    html += '<h2>Summary</h2>'
    html += '<table>'
    html += '<tr><th>File</th><th>Valid</th></tr>'
    for result in results:
        html += f'<tr><td>{result["file"]}</td><td>{"<span>&#x2713;</span>" if result["return_code"] == 0 else "<span>&#x2717;</span>"}</td></tr>'
    html += '</table>'
    html += '<h2>Details</h2>'
    for result in results:
        html += f'<details><summary><h3>{result["file"]} {"<span>&#x2713;</span>" if result["return_code"] == 0 else "<span>&#x2717;</span>"}</h3></summary><pre>{result["output"]}</pre></details>'
    return html

def annotate_pr(message: str, success: bool = True) -> None:
    """
    Annotate the GitHub Pull Request with the given message
    :param message: The message to annotate the PR with
    :param success: Whether the check was successful or not
    :return: None
    """
    # If we're not reporting in the PR, just print the message and return
    if not report_in_pr:
        print("Not reporting in pull request")
        return
    
    # Get the GitHub values from the environment
    github_repo = os.getenv('GITHUB_REPOSITORY')
    if not github_repo:
        print("No GitHub repository provided")
        exit(1)
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("No GitHub token provided")
        exit(1)
    github_pull_request = int(os.getenv('GITHUB_PULL_REQUEST', 0))
    if not github_pull_request or github_pull_request == 0:
        print("No GitHub pull request provided; not reporting in pull request")
        return
    
    # Login to GitHub and get the PR object
    client = Github(github_token)
    repo = client.get_repo(github_repo)
    pr = repo.get_pull(github_pull_request)

    # Delete all existing comments that start with "<h1>CASE Validation Results</h1>" to avoid duplicates
    for comment in pr.get_issue_comments():
        if comment.body.startswith('<h1>CASE Validation Results</h1>'):
            comment.delete()

    # Create a new comment with the message
    pr.create_issue_comment(message)


## Main Script ##
# Ensure the path exists
if not os.path.exists(case_path):
    print(f"Path does not exist: {case_path}")
    exit(1)

# If the input is a file, ignore the extension filter and add the file to the list
if os.path.isfile(case_path):
    files.append(case_path)
    relative_path = os.path.dirname(case_path)
else:
    # Get the list of files that match the pattern if the pattern is not empty
    relative_path = case_path
    if extension_filter:
        for file in os.listdir(case_path):
            if file.endswith(extension_filter):
                files.append(file)
    else:
        files = os.listdir(case_path)

# Validate each file
for file in files:
    print(f"Validating file: {file}")
    args = ["case_validate", os.path.join(relative_path, file), "--built-version", case_version]
    if abort_on_error:
        args.append("--abort")
    validation_output = subprocess.run(args, capture_output=True, text=True)
    results.append({
        'file': file,
        'full_path': os.path.join(relative_path, file),
        'return_code': validation_output.returncode,
        'output': validation_output.stdout,
        'error': validation_output.stderr
    })

    print(validation_output.stdout)


# Print the results
print("Validation Results:")
print("========================================")
print(f"Input files: {len(results)}")
print(f"Valid files: {len([result for result in results if result['return_code'] == 0])}")
print(f"Invalid files: {len([result for result in results if result['return_code'] != 0])}")
print("========================================")


# Annotate the PR
success: bool = len([result for result in results if result['return_code'] != 0]) == 0
annotate_pr(generate_html_report(results), success)

# Exit with a non-zero exit code if there were any failures
if not success:
    exit(1)
