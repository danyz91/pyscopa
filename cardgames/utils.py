import random
import string

def generate_random_string(stringLength=4):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def subsets_with_sum(lst, target, with_replacement=False):
    x = 0 if with_replacement else 1

    def _a(idx, l, r, t):
        if t == sum(el.value for el in l):
            r.append(l)
        elif t < sum(el.value for el in l):
            return
        for u in range(idx, len(lst)):
            _a(u + x, l + [lst[u]], r, t)
        return r

    return _a(0, [], [], target)