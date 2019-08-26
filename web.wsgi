import sys, os
sys.path.append(os.path.dirname(__file__))
from web import app as application, setup
setup()
