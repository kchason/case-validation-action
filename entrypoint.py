import os
import subprocess

from github import Auth, Github

case_path = os.getenv('CASE_PATH', './tests/data/')
extension_filter = os.getenv('EXTENSION_FILTER', '')
case_version = os.getenv('CASE_VERSION', 'case-1.0.0')

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
        html
        html += f'<details><summary><h3>{result["file"]} {"<span>&#x2713;</span>" if result["return_code"] == 0 else "<span>&#x2717;</span>"}</h3></summary><pre>{result["output"]}</pre></details>'
    return html

def annotate_pr(message: str, success: bool = True) -> None:
    """
    Annotate the GitHub Pull Request with the given message
    :param message: The message to annotate the PR with
    :param success: Whether the check was successful or not
    :return: None
    """
    # Temporarily write this to a file for testing
    with open('pr_comment.html', 'w') as f:
        f.write(message)


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
    validation_output = subprocess.run(["case_validate", os.path.join(relative_path, file), "--built-version", case_version], capture_output=True, text=True)
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
