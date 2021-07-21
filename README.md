# AWS Serverless Application Repository Analysis

Collection of analysis functions around the AWS Serverless Application Repository.

> README in progress - currently only covers CLI

## CLI

A cli is available that helps with the execution of a subset of analysis functions available in this repository:

```
usage: cli.py [-h] [--timestamp] [--light] [{autocontents,insights,insights-plot,github-contents,codechecker,samfinder,all}]

AWS SAR Analysis

positional arguments:
  {autocontents,insights,insights-plot,github-contents,codechecker,samfinder,all}
                        Running without parameters will execute all tasks.

optional arguments:
  -h, --help            show this help message and exit
  --timestamp           non CSV output data will be generated in a timestamped subfolder (e.g. 2021-01-01/)
  --light               remove large cache files from data dir after execution
```

Positional Arguments:

- `autocontents`: collects general and meta-information from the AWS SAR
- `insights`: generates several metrics from the information gathered by the `autocontents` function
- `insights-plot`: generates plots from the insight metrics
- `github-contents`: collects repository metrics for GitHub repos found by the `autocontents` function
- `codechecker`: acquires actual code repositories from linked git repos if possible
- `samfinder`: extracts sam yaml's from `codechecker` run and generates metrics around findings
- `all`: run all steps intertwined in correct order of dependencies