from zerotk.reraiseit import reraise

try:
    raise RuntimeError('ops')
except Exception as e:
    reraise(e, 'While testing reraise.')
