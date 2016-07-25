import os, sys, argparse, shutil
from datetime import timedelta
from datetime import datetime as dt
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib.tools import buildDatesFromFolders

def delete(directory, days):
    dates = [ dt.strptime(f, '%Y/%m/%d') for f in buildDatesFromFolders(directory) ]
    time_limit = dt.today() - timedelta(days=days)
    for date in dates:
        if date <= time_limit:
            shutil.rmtree(os.path.join(directory, date.strftime('%Y/%m/%d')))

parser = argparse.ArgumentParser(description='pasty - tool to cleanup old pasty posts')
parser.add_argument('days', type=int, help='Specifies how many days of posts should be kept')
parser.add_argument('--which', type=str, help='Specifies which posts should be deleted', choices=['posts', 'autosave'], required=True)

args = parser.parse_args()
delete(os.path.join(os.path.dirname(__file__), args.which), args.days)
