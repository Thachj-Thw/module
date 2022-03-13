import subprocess
import module
import time


p = subprocess.Popen("C:\\WINDOWS\\system32\\notepad.exe")
time.sleep(.1)
note = module.Window.from_pid(p.pid)
print(note)
