from time import time

from bpytop import errlog


def timeit_decorator(func):
	def timed(*args, **kw):
		ts = time()
		out = func(*args, **kw)
		errlog.debug(f'{func.__name__} completed in {time() - ts:.6f} seconds')
		return out
	return timed
