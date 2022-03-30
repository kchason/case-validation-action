# CASE Validation Action
_This is an unofficial GitHub Action and not endorsed by the CASE Community or the Linux Foundation._

### Overview
A validator for the CASE Cyber Ontology which is available at [https://caseontology.org/](https://caseontology.org/).

This is based on the validator included in the CASE Utilities project available at: [https://github.com/casework/CASE-Utilities-Python](https://github.com/casework/CASE-Utilities-Python). 

### Usage
Include the validation action in your GitHub action workflow and specify the file or directory to be validated.

```yaml
# Run the CASE validation job to confirm the output is valid
- name: CASE Export Validation
  uses: kchason/case-validation-action@v1
  with:
    case-path: ./output/case.json
    case-version: 0.6.0
```

**Inputs:**
| Variable     | Description                                                                | Options                            | Default       |
|--------------|----------------------------------------------------------------------------|------------------------------------|---------------|
| case-path    | The path to the file or directory to be validated.                         |                                    | /opt/json     |
| case-version | The version of the ontology against which the graph should be validatated. | "none", "case-0.5.0", "case-0.6.0" | "case-0.6.0"  |

