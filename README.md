# CASE Validation Action
_This is an unofficial GitHub Action and not endorsed by the CASE Community or the Linux Foundation. No warranties or guarantees are made to its accuracy or functionality._ 

[![Repository Checks](https://github.com/kchason/case-validation-action/actions/workflows/validate.yml/badge.svg)](https://github.com/kchason/case-validation-action/actions/workflows/validate.yml)
![CASE Version](https://img.shields.io/badge/CASE%20Version-1.2.0-brightgreen.svg)
[![Latest Tag](https://img.shields.io/github/v/tag/kchason/case-validation-action?label=action%20version)](https://github.com/kchason/case-validation-action/tags)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/kchason/case-validator)](https://hub.docker.com/repository/docker/kchason/case-validator)
[![Docker Pulls](https://img.shields.io/docker/pulls/kchason/case-validator)](https://hub.docker.com/repository/docker/kchason/case-validator)


## Overview
A GitHub Action validator for the CASE Cyber Ontology which is available at [https://caseontology.org/](https://caseontology.org/).

This is based on the `case_validate` library included in the CASE Utilities project available at: [https://github.com/casework/CASE-Utilities-Python](https://github.com/casework/CASE-Utilities-Python). 

This is also available as a Docker image at: [https://hub.docker.com/r/kchason/case-validator](https://hub.docker.com/r/kchason/case-validator)

## GitHub Action Usage
Include the validation action in your GitHub action workflow and specify the file or directory to be validated.

```yaml
# Run the CASE validation job to confirm the output is valid
- name: CASE Export Validation
  uses: kchason/case-validation-action@v2.6.1
  with:
    case-path: ./output/
    case-version: "case-1.2.0"
    extension-filter: "jsonld"
```

## Docker Usage

Alternatively, the Docker image can be pulled from [Docker Hub](https://hub.docker.com/repository/docker/kchason/case-validator) and run locally or as part of custom integrations.

The environment variables are defined below in the "Inputs" table, and the below command is an example that can be modified to fit custom use cases.

```bash
# To run the latest image and remove the container after execution. 
docker run --rm \
	-e CASE_PATH="/opt/case/" \
	-e CASE_VERSION="case-1.2.0" \
	-e FILTER_EXTENSION="jsonld" \
	-v "/path/to/local:/opt/case" \
	kchason/case-validator:latest
```

### GitLab CI/CD Usage
The built container image available on Docker Hub can also be integrated into [GitLab CI/CD](https://docs.gitlab.com/ee/ci/) to validate files in the source repository.

Example usage and documentation are available in a demo project on GitLab at [https://gitlab.com/keith.chason/case-validation-example](https://gitlab.com/keith.chason/case-validation-example).


## Inputs

| Action Variable  | Environment Variable | Description                                                  | Options                            | Default      |
| ---------------- | -------------------- | ------------------------------------------------------------ | ---------------------------------- | ------------ |
| case-path        | CASE_PATH            | The path to the file or directory to be validated.           | Any                                | /opt/json    |
| case-version     | CASE_VERSION         | The version of the ontology against which the graph should be validatated. | "none", "case-0.5.0", "case-0.6.0" , "case-0.7.0", "case-0.7.1", "case-1.0.0", "case-1.1.0", "case-1.2.0" | "case-1.2.0" |
| extension-filter | FILTER_EXTENSION     | The extension of only the files against which the validator should be run. Eg. `"json"`, `"jsonld"`, `"case"`. Defaults to `""` to run against all files defined in `case-path`. | Any                                | ""           |
| abort            | CASE_VALIDATE_ABORT  | Whether to abort the validator on the first failure            | "true", "false"   | "false" |

## Example Output

_Output will be listed linearly if multiple files are provided_
### Conforming
```bash
Validating file at ./output/case.json
Validation Report
Conforms: True
```

### Non-Conforming
```
Validating file at ./output/case.json
Validation Report
Conforms: False
Results (2):
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:class core:UcoObject ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:nodeKind sh:BlankNodeOrIRI ; sh:path core:object ]
	Focus Node: kb:provenance-record-58e7566a-a934-4513-93b2-98fd43978a1c
	Result Path: core:object
	Message: Less than 1 values on kb:provenance-record-58e7566a-a934-4513-93b2-98fd43978a1c->core:object
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:class core:UcoObject ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:nodeKind sh:BlankNodeOrIRI ; sh:path core:object ]
	Focus Node: kb:provenance-record-a22fc197-6e53-4bc0-9832-d0b9f2b733d3
	Result Path: core:object
	Message: Less than 1 values on kb:provenance-record-a22fc197-6e53-4bc0-9832-d0b9f2b733d3->core:object
```
