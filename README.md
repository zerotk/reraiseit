[![PyPI](https://img.shields.io/pypi/v/zerotk.reraiseit.svg?style=flat-square)]()
[![Travis](https://img.shields.io/travis/zerotk/easyfs.svg?style=flat-square)]()
[![Coveralls](https://img.shields.io/coveralls/zerotk/reraiseit.svg?style=flat-square)]()

# zerotk.reraiseit

Reraise utility function. Just that!


```python
from zerotk.reraiseit import reraise

try:
  raise RuntimeError('An error occurred')
except Exception as e:
  reraise(e, '')
```

This will produce the following output:

```
(... traceback ...)
RuntimeError:
While testing reraise.
An error occurred
```

As you can see, it added a message to the exception and re-raise it.
