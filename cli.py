import argparse
import subprocess
import os
from pathlib import Path

def _acquire_sar():
    old_wd = os.getcwd()
    _output_path = 'data/autostats'
    Path(_output_path).mkdir(parents=True, exist_ok=True)
    os.chdir(_output_path)
    subprocess.run(f"python {old_wd}/autocontents.py --custom", shell=True)
    os.chdir(old_wd)

def _insights():
    old_wd = os.getcwd()
    os.chdir('data/')
    subprocess.run(f"python {old_wd}/insights.py", shell=True)
    os.chdir(old_wd)

def _insights_plot():
    old_wd = os.getcwd()
    os.chdir('data/')
    subprocess.run(f"python {old_wd}/insights-plot.py", shell=True)
    os.chdir(old_wd)

def _codechecker():
    old_wd = os.getcwd()
    os.chdir('data/')
    subprocess.run(f"python {old_wd}/codechecker.py", shell=True)
    os.chdir(old_wd)

def _samfinder():
    old_wd = os.getcwd()
    os.chdir('data/')
    subprocess.run(f"python {old_wd}/samfinder/samfinder.py --copy", shell=True)
    os.chdir(old_wd)

def _github_contents():
    old_wd = os.getcwd()
    _output_path = 'data/github-contents'
    Path(_output_path).mkdir(parents=True, exist_ok=True)
    os.chdir(_output_path)
    subprocess.run(f"python {old_wd}/github-contents.py ../autostats/autocontents-*.csv", shell=True)
    os.chdir(old_wd)

cli = argparse.ArgumentParser(description='AWS SAR Analysis')

cli.add_argument(
    "task",
    choices=['acquire-sar', 'insights', 'insights-plot', 'github-contents', 'codechecker', 'samfinder', 'all'],
    default='all',
    nargs='?',
    help='Running without parameters will execute all tasks.'
    )

args = cli.parse_args()
if args.task == 'acquire-sar':
    # get metadata from SAR
    _acquire_sar()
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
    _acquire_sar()
    _insights()
    _insights_plot()
    #_github_contents()
    _codechecker()
    _samfinder()