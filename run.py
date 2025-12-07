import subprocess
import sys
import time
import signal

processes = []

def signal_handler(sig, frame):
    for proc in processes:
        try:
            proc.terminate()
        except:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

subprocess.Popen([sys.executable, 'server.py'])
time.sleep(0.5)

subprocess.Popen([sys.executable, 'client2.py'])
time.sleep(0.5)

subprocess.Popen([sys.executable, 'client1.py']).wait()

