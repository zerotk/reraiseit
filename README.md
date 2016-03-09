[![PyPI](https://img.shields.io/pypi/v/zerotk.reraiseit.svg?style=flat-square)](https://pypi.python.org/pypi/zerotk.reraiseit)
[![Travis](https://img.shields.io/travis/zerotk/reraiseit.svg?style=flat-square)](https://travis-ci.org/zerotk/reraiseit)
[![Coveralls](https://img.shields.io/coveralls/zerotk/reraiseit.svg?style=flat-square)](https://coveralls.io/github/zerotk/reraiseit)

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
