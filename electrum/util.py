import os, sys, re, json
import platform
import shutil
from datetime import datetime
is_verbose = True

def set_verbosity(b):
    global is_verbose
    is_verbose = b

def print_error(*args):
    if not is_verbose: return
    args = [str(item) for item in args]
    sys.stderr.write(" ".join(args) + "\n")
    sys.stderr.flush()

def print_msg(*args):
    # Stringify args
    args = [str(item) for item in args]
    sys.stdout.write(" ".join(args) + "\n")
    sys.stdout.flush()

def user_dir():
    if "HOME" in os.environ:
        return os.path.join(os.environ["HOME"], ".electrum")
    elif "APPDATA" in os.environ:
        return os.path.join(os.environ["APPDATA"], "Electrum")
    elif "LOCALAPPDATA" in os.environ:
        return os.path.join(os.environ["LOCALAPPDATA"], "Electrum")
    elif 'ANDROID_DATA' in os.environ:
        return "/sdcard/electrum/"
    else:
        #raise BaseException("No home directory found in environment variables.")
        return 

# Python bug (http://bugs.python.org/issue1927) causes raw_input
# to be redirected improperly between stdin/stderr on Unix systems
def raw_input(prompt=None):
    if prompt:
        sys.stdout.write(prompt)
    return builtin_raw_input()
import __builtin__
builtin_raw_input = __builtin__.raw_input
__builtin__.raw_input = raw_input
