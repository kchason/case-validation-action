#!/usr/bin/env bash

# Build the arguments for the validator
cmd="case_validate --built-version ${CASE_VERSION}"
if [ "${FAIL_FAST}" = true ]; then
    cmd="${cmd} --abort"
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
            eval "${cmd} ${entry}"
        done
    else 
        # Filter was specified, only run against provided files
        for entry in "${CASE_PATH}"/*."${EXTENSION_FILTER}"
        do
            echo "Validating filtered file ${entry} found within ${CASE_PATH}"
            eval "${cmd} ${entry}"
        done
    fi

elif [[ -f ${CASE_PATH} ]]; then
    echo "Validating file at ${CASE_PATH}"
    eval "${cmd} ${CASE_PATH}"
else
    echo "${CASE_PATH} is not a valid path and the validation cannot continue"
    exit 1
fi