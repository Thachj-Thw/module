# module

Some module for python

## Installation

```bash
pip install module-thw
```

## Example

### Window

```python

import subprocess
import module
import time


p1 = subprocess.Popen("C:\\WINDOWS\\system32\\notepad.exe")
p2 = subprocess.Popen("C:\\WINDOWS\\system32\\notepad.exe")
time.sleep(.1)
note1 = module.Window.from_pid(p1.pid)
note2 = module.Window.from_pid(p2.pid)
print(note1)
print(note2)
if note1 and note2:
    note2.position = (0, 0)
    note2.size = (500, 300)
    note1.size = (600, 600)
    note1.attack_child(note2)

```

### Path

convert to EXE to see the different.

```python
import module


path = module.Path(__file__)
print(path.source)
print(path.source.join("test"))
print(path.app)

```

### ThreadList

list using to get each element from multi thead

```python
import threading
import module


lst = module.ThreadList([1, 2, 3, 4, 5])

def thread(index):
    i = lst.next()
    while i is not None:
        print("Thread", index, "-", i)
        i = lst.next()

threading.Thread(target=thread, args=(0, )).start()
threading.Thread(target=thread, args=(1, )).start()
threading.Thread(target=thread, args=(2, )).start()

```

### hide_console

Hide console of application. It isn't like `--noconsole` in pyinstaller

```python
import module


module.hide_console()

```

### alert_excepthook

Will have a message box about exceptions, not only on the console

```python
import module


module.alert_excepthook()

```
