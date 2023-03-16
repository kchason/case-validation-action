#!/usr/bin/env bash

# Build the arguments for the validator
args="--built-version ${CASE_VERSION}"
if [ ${FAST_FAIL} ]; then
    args="${args} --abort"
fi

# Determine if the provided path is a directory. If so, then there is filtering and other handling
# to address. If it is a file, then it is assumed it should be validated.
if [[ -d "${CASE_PATH}" ]]; then

    # Determine if an extension filter was provided. If so, then only validate files that have the
    # provided extension. 
    if [[ "${EXTENSION_FILTER}" == '' ]]; then
        # No filter was specified, run against all files in path
        for entry in "${CASE_PATH}"/*
        do
            echo "Validating file ${entry} found within ${CASE_PATH}"
            case_validate "${entry} ${args}"
        done
    else 
        # Filter was specified, only run against provided files
        for entry in "${CASE_PATH}"/*."${EXTENSION_FILTER}"
        do
            echo "Validating file ${entry} found within ${CASE_PATH}"
            case_validate "${entry} ${args}"
        done
    fi

elif [[ -f ${CASE_PATH} ]]; then
    echo "Validating file at ${CASE_PATH}"
    case_validate "${CASE_PATH} ${args}"
else
    echo "${CASE_PATH} is not a valid path and the validation cannot continue"
    exit 1
fi