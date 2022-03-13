# module

Some module for python

## Installation

```bash
pip install module-thw
```

## Example

```python
import subprocess
import module
import time


p = subprocess.Popen("C:\\WINDOWS\\system32\\notepad.exe")
time.sleep(.1)
notepad = module.Window.from_pid(p.pid)
print(notepad)
notepad.position = (0, 0)
# or
# notepad.set_window_position(0, 0)

```
