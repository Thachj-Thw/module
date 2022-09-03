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
lst_note1 = module.Window.from_pid(p1.pid)
lst_note2 = module.Window.from_pid(p2.pid)
print(lst_note1)
print(lst_note2)
for note1 in lst_note1:
    if note1.is_visible():
        for note2 in lst_note2:
            note2.position = (0, 0)
            note2.size = (500, 300)
            note1.attachments(note2)
        break
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

a = 1 / 0

```

### alert

a window message box, return button clicked

```python
import module


button = module.alert("this is a title", "this is a message", module.TypesButtons.OK_CANCEL)
print(button == module.Buttons.OK)
```
