import argparse
import subprocess
import os
import shutil
from pathlib import Path
from datetime import datetime

timestamp = False
light = False
output_dir = 'data'

def _run_cmd_datadir(cmd, output_dir):
    old_wd = os.getcwd()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    os.chdir(output_dir)
    subprocess.run(f"python {old_wd}/{cmd}", shell=True)
    os.chdir(old_wd)

def _autocontents():
    _output_path = f'{output_dir}/autostats'
    _run_cmd_datadir("autocontents.py --custom", _output_path)

def _insights():
    _run_cmd_datadir("insights.py", output_dir)

def _insights_plot():
    _run_cmd_datadir("insights-plot.py", output_dir)

def _codechecker():
    _run_cmd_datadir("codechecker.py", output_dir)

def _samfinder():
    _run_cmd_datadir("samfinder/samfinder.py --copy", output_dir)

def _github_contents():
    _output_path = f'{output_dir}/github-contents'
    _run_cmd_datadir("github-contents.py ../autostats/autocontents-*.csv", _output_path)

def _remove_large_results():
    _rm_dirs = ['_codechecker', '_codefolders', '_codestamp']
    for dir in _rm_dirs:
        dirpath = Path(f'{output_dir}/{dir}')
        # check if path exists
        if dirpath.exists() and dirpath.is_dir():
            # remove files recursively
            shutil.rmtree(dirpath)

cli = argparse.ArgumentParser(description='AWS SAR Analysis')

cli.add_argument(
    "task",
    choices=['autocontents', 'insights', 'insights-plot', 'github-contents', 'codechecker', 'samfinder', 'all'],
    default='all',
    nargs='?',
    help='Running without parameters will execute all tasks.'
    )

cli.add_argument('--timestamp', dest='timestamp', action='store_true', default=False, help='non CSV output data will be generated in a timestamped subfolder (e.g. 2021-01-01/)')
cli.add_argument('--light', dest='light', action='store_true', default=False, help='remove large cache files from data dir after execution')

args = cli.parse_args()

if args.task == 'autocontents':
    # get metadata from SAR
    _autocontents()
elif args.task == 'insights':
    # generate insights from SAR data
    _insights()
elif args.task == 'insights-plot':
    # generate insights from SAR data
    _insights_plot()
elif args.task == 'github-contents':
    # generate insights from SAR data
    _github_contents()
elif args.task == 'codechecker':
    _codechecker()
elif args.task == 'samfinder':
    _samfinder()
elif args.task == 'all':
    # generate insights from SAR data
    _autocontents()
    _insights()
    _insights_plot()
    #_github_contents()
    _codechecker()
    _samfinder()

if args.timestamp:
    timestamp = True
    timestamp_dir = f"{output_dir}/{datetime.today().strftime('%Y-%m-%d')}"
    Path(timestamp_dir).mkdir(parents=True, exist_ok=True)
    _to_move = [
        'codecheckerfolders.json',
        'codecheckernamedfolders.json',
        'codecheckerrepos.json',
        'plots',
        '_sams'
    ]
    for path in _to_move:
        shutil.move(f'{output_dir}/{path}', f'{timestamp_dir}/{path}')

if args.light:
    light = True
    _remove_large_results()