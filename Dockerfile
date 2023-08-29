FROM python:3.11-slim-bullseye

# This is based on guidance in https://github.com/casework/CASE-Utilities-Python/tree/main
WORKDIR /opt/workspace

# Install dependencies
RUN python -m pip install case-utils==0.12.0 PyGithub

# Delete source files now that package has been installed
WORKDIR /opt/workspace

# Copy in the entrypoint file
COPY entrypoint.py /opt/workspace/entrypoint.py

# Define the base path for the validation path
ENV CASE_PATH "/opt/json/"
ENV CASE_VERSION "case-1.2.0"
ENV CASE_EXTENSION_FILTER ""
ENV CASE_VALIDATE_ABORT "false"

# Required for annotating the GitHub pull request; optional otherwise
ENV REPORT_IN_PR "false"
ENV GITHUB_TOKEN ""
ENV GITHUB_REPOSITORY ""
ENV GITHUB_PULL_REQUEST ""

# Define the command to run the entrypoint.py script that will detect the type
# of the path that was provided, apply the filter extension (if appropriate) and
# run the `case_validate` function against the CASE file(s) to be validated.
CMD ["python3", "/opt/workspace/entrypoint.py"]
