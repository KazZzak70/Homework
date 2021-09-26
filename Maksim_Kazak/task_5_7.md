### Task 4.7*
### 1. Run the module `modules/mod_a.py`. Check its result. Explain why does this happen.

This is possible due to the fact that all modules are located in one directory (folder),
without this fact, we would need to edit PYTHONPATH file or append the full path to the list `sys.path`

```python
import mod_c
import mod_b
print(mod_c.x)
>>> 5
```
### 2. Try to change x to a list `[1,2,3]`. Explain the result.

We can make it "ugly" by "monkey patching" directly from mod_a: 
```python
import mod_c
import mod_b

mod_c.x = [1, 2, 3]
print(mod_c.x)
>>> [1, 2, 3]
```
or we can change the value in mod_b:
```python
import mod_c


mod_c.x = 5
>>> [1, 2, 3]
```
### 3. Try to change import to `from x import *` where x - module names. Explain the result.
```python
from mod_c import *
from mod_b import *
```
When we refer to a variable by name `x`:
```python
from mod_c import *
from mod_b import *

print(x)
>>> [1, 2, 3]
```
but when we refer to a variable by name `mod_c.x`:
```python
from mod_c import *
from mod_b import *

print(mod_c.x)
>>> 5
```
This is due to the fact that they are two different variables.

If we define two variables with the same name in different modules and access this variable without specifying a specific module, the import comes from the last `import`
```python
from mod_b import *
from mod_c import *

print(x)
>>> 5
```
```python
from mod_c import *
from mod_b import *

print(x)
>>> [1, 2, 3]
```