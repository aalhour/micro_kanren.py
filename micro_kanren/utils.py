from itertools import islice


def interleave(*iterators):
    '''Given a list of iterators, interleave between them'''
    iters = list(iterators)
    while iters:
        try:
            it = iters.pop(0)
            yield next(it)
            iters.append(it)
        except StopIteration:
            continue
        except TypeError:
            yield None


def take(n, iterable):
    '''Return first n items of the iterable as a list'''
    return list(islice(iterable, n))

