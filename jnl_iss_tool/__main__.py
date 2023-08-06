# coding: UTF-8
import sys 
sys.path.append('./')

print(__name__, __package__)

import subprocess
subprocess.Popen('PAUSE', shell=True)

import jnl_iss_tool.window as window

if __name__ == "__main__":

    window.main()
