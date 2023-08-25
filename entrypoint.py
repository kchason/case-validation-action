import os
import sys

from case_utils.case_validate import validate
from case_utils.case_validate.validate_types import ValidationResult

# Get the environment variables as the settings for the validation
case_version: str = os.environ.get("CASE_VERSION", "case-1.2.0")
abort_on_failure: bool = (
    os.environ.get("CASE_VALIDATE_ABORT", "false").lower() == "true"
)  # noqa: E501
case_path: str = os.environ.get("CASE_PATH", "/opt/json/")
extension_filter: str = os.environ.get("CASE_EXTENSION_FILTER", "")

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

        if not result.conforms:
            has_failure = True
            if abort_on_failure:
                sys.exit(1)

    # If there was a failure, then exit with a non-zero exit code
    sys.exit(1) if has_failure else sys.exit(0)

elif os.path.isfile(case_path):
    # If the path is a file, then it is assumed it should be validated
    # and ignore the filter
    result: ValidationResult = validate(
        case_path, case_version=case_version, abort_on_first=abort_on_failure
    )

    print(f"Validating file at: {case_path}")
    print(result.text)
    sys.exit(0) if result.conforms else sys.exit(1)

else:
    print(
        f"${case_path} is not a valid path and the validation cannot continue"
    )  # noqa: E501
    sys.exit(1)
