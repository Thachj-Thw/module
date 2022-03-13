import subprocess
import module
import time


p = subprocess.Popen(r"C:\WINDOWS\system32\notepad.exe")
time.sleep(.1)
print(module.Window.from_pid(p.pid))

