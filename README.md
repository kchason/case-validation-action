# CASE Validation Action

_This is an unofficial GitHub Action and not endorsed by the CASE Community or the Linux Foundation. No warranties or
guarantees are made to its accuracy or functionality._

[![Repository Checks](https://github.com/kchason/case-validation-action/actions/workflows/validate.yml/badge.svg)](https://github.com/kchason/case-validation-action/actions/workflows/validate.yml)
![CASE Version](https://img.shields.io/badge/CASE%20Version-1.4.0-brightgreen.svg)
[![Latest Tag](https://img.shields.io/github/v/tag/kchason/case-validation-action?label=action%20version)](https://github.com/kchason/case-validation-action/tags)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/kchason/case-validator)](https://hub.docker.com/repository/docker/kchason/case-validator)
[![Docker Pulls](https://img.shields.io/docker/pulls/kchason/case-validator)](https://hub.docker.com/repository/docker/kchason/case-validator)

## Overview

A GitHub Action validator for the CASE Cyber Ontology which is available
at [https://caseontology.org/](https://caseontology.org/).

This is based on the `case_validate` library included in the CASE Utilities project available
at: [https://github.com/casework/CASE-Utilities-Python](https://github.com/casework/CASE-Utilities-Python).

This is also available as a Docker image
at: [https://hub.docker.com/r/kchason/case-validator](https://hub.docker.com/r/kchason/case-validator)

## GitHub Action Usage

Include the validation action in your GitHub action workflow and specify the file or directory to be validated.

```yaml
# Run the CASE validation job to confirm the output is valid
- name: CASE Export Validation
  uses: kchason/case-validation-action@v2.10.0
  with:
    case-path: ./output/
    case-version: "case-1.4.0"
    extension-filter: "jsonld"
    report-in-pr: "true"
    github-token: ${{ secrets.GITHUB_TOKEN }}
    repository: ${{ github.repository }}
    pull-request: ${{ github.event.pull_request.number }}
```

## Docker Usage

Alternatively, the Docker image can be pulled
from [Docker Hub](https://hub.docker.com/repository/docker/kchason/case-validator) and run locally or as part of custom
integrations.

The environment variables are defined below in the "Inputs" table, and the below command is an example that can be
modified to fit custom use cases.

```bash
# To run the latest image and remove the container after execution. 
docker run --rm \
	-e CASE_PATH="/opt/case/" \
	-e CASE_VERSION="case-1.4.0" \
	-e CASE_EXTENSION_FILTER="jsonld" \
	-v "/path/to/local:/opt/case" \
	kchason/case-validator:latest
```

### GitLab CI/CD Usage

The built container image available on Docker Hub can also be integrated
into [GitLab CI/CD](https://docs.gitlab.com/ee/ci/) to validate files in the source repository.

Example usage and documentation are available in a demo project on GitLab
at [https://gitlab.com/keith.chason/case-validation-example](https://gitlab.com/keith.chason/case-validation-example).

## Inputs

| Action Variable  | Environment Variable  | Description                                                                                                                                                                      | Options                                                                                                   | Default      |
|------------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|--------------|
| case-path        | CASE_PATH             | The path to the file or directory to be validated.                                                                                                                               | Any                                                                                                       | /opt/json    |
| case-version     | CASE_VERSION          | The version of the ontology against which the graph should be validatated.                                                                                                       | "none", "case-0.5.0", "case-0.6.0" , "case-0.7.0", "case-0.7.1", "case-1.0.0", "case-1.1.0", "case-1.2.0", "case-1.3.0", "case-1.4.0" | "case-1.4.0" |
| extension-filter | CASE_EXTENSION_FILTER | The extension of only the files against which the validator should be run. Eg. `"json"`, `"jsonld"`, `"case"`. Defaults to `""` to run against all files defined in `case-path`. | Any                                                                                                       | ""           |
| abort            | CASE_VALIDATE_ABORT   | Whether to abort the validator on the first failure                                                                                                                              | "true", "false"                                                                                           | "false"      |
| report-in-pr     | REPORT_IN_PR          | Whether or not to report the validation results in the pull request. Only reports if the action is triggered by a pull request.                                                  | "true", "false"                                                                                           | "false"      |
| github-token     | GITHUB_TOKEN          | The GitHub token used to report the validation results in the pull request.                                                                                                      | Any                                                                                                       | ""           |
| repository       | GITHUB_REPOSITORY     | The GitHub repository used to report the validation results in the pull request.                                                                                                 | Any                                                                                                       | ""           |
| pull-request     | GITHUB_PULL_REQUEST   | The GitHub pull request used to report the validation results in the pull request.                                                                                               | Any                                                                                                       | ""           |

## Example Output

_Output will be listed linearly if multiple files are provided_

### Conforming

```bash
Validating file at ./output/case.json
Validation Report
Conforms: True
```

### Non-Conforming

Supposing a file with these contents:

```json
{
    "@context": {
        "kb": "http://example.org/kb/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    "@graph": [
        {
            "@id": "kb:hash-25940dc2-4db9-4c01-9053-bc31f953fc4a",
            "@type": "uco-types:Hash",
            "rdfs:comment": "This node will pass validation.",
            "uco-types:hashMethod": "SHA3-256",
            "uco-types:hashValue": {
                "@type": "xsd:hexBinary",
                "@value": "c901cf247f1112334f51bdb5385db3b56d935f9fbc844c1b4a161b10c1c86d83"
            }
        },
        {
            "@id": "kb:hash-b896ba81-f07c-4035-9277-a101eb6782c3",
            "@type": "uco-types:Hash",
            "rdfs:comment": "This node will trigger a validation error due to leaving hashValue's value as an untyped string.",
            "uco-types:hashMethod": "SHA3-256",
            "uco-types:hashValue": "4c6e44aab46ce9023dc82a006f18a06be8f3c64a6b12739be51e706b5adffeb5"
        }
    ]
}
```

```
Validation Report
Conforms: False
Results (1):
Constraint Violation in DatatypeConstraintComponent (http://www.w3.org/ns/shacl#DatatypeConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:datatype xsd:hexBinary ; sh:maxCount Literal("1", datatype=xsd:integer) ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:nodeKind sh:Literal ; sh:path types:hashValue ]
	Focus Node: kb:hash-b896ba81-f07c-4035-9277-a101eb6782c3
	Value Node: Literal("4c6e44aab46ce9023dc82a006f18a06be8f3c64a6b12739be51e706b5adffeb5")
	Result Path: types:hashValue
	Message: Value is not Literal with datatype xsd:hexBinary
```

## GitHub Pull Request Decoration
This action allows for the validation results to be reported in the pull request that triggered the action. This is
done by using the GitHub API to create a comment on the pull request with the validation results. This configured with
the following variables: `report-in-pr`, `github-token`, `repository`, and `pull-request`.
