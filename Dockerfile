FROM python:3.9-slim-bullseye

# This is based on guidance in https://github.com/casework/CASE-Utilities-Python/tree/main
WORKDIR /opt/workspace

# Install dependencies
RUN apt-get update && apt-get install git -y
RUN git clone https://github.com/casework/CASE-Utilities-Python.git
WORKDIR /opt/workspace/CASE-Utilities-Python
RUN python setup.py install

# Delete source files now that package has been installed
WORKDIR /opt/workspace
RUN rm -rf /opt/workspace/CASE-Utilities-Python

# Copy in the entrypoint file
COPY entrypoint.sh /opt/workspace/entrypoint.sh

# Define the base path for the validation path
ENV CASE_PATH "/opt/json/"
ENV CASE_VERSION "case-0.6.0"
ENV FILTER_EXTENSION ""

# Define the command to run the entrypoint.sh script that will detect the type
# of the path that was provided, apply the filter extension (if appropriate) and
# run the `case_validate` command against the CASE file(s) to be validated.
CMD ["bash", "/opt/workspace/entrypoint.sh"]
