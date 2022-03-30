FROM python:3.9

# This is based on guidance in https://github.com/casework/CASE-Utilities-Python/tree/main
WORKDIR /opt/workspace

# Install dependencies
RUN git clone https://github.com/casework/CASE-Utilities-Python.git
WORKDIR /opt/workspace/CASE-Utilities-Python
RUN python setup.py install

# Delete source files now that package has been installed
WORKDIR /opt/workspace
RUN rm -rf /opt/workspace/CASE-Utilities-Python

# Define the base path for the validation path
ENV CASE_PATH "/opt/json/"
ENV CASE_VERSION "case-0.6.0"

# Define the command to run the validator against any files in the path defined in the
# CASE_PATH environment variable. This will work for either a single file or a directory.
# Note, we can't practically use Docker syntax with the command and the environment variable.
CMD "case_validate" "${CASE_PATH}" "--built-version" "${CASE_VERSION}"
