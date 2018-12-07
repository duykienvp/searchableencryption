""" Binary Expression Minimization using PyEDA package,
which in turn uses a C extension to the famous Berkeley Espresso library.

See: https://pyeda.readthedocs.io/en/latest/2llm.html
"""

from pyeda.inter import exprvars, expr, espresso_exprs


def perform_bin_expr_min(base_tokens: list, wildcard='*'):
    """ Perform binary expression minimization for a list of base tokens

    :param list base_tokens: list of base tokens that have same length.
        Each base token is a list of '0' or '1'.
    :param wildcard: the element to denote "do not care" character

    :returns: list of minimized tokens of '0', '1' or 'wildcard'
    """
    if not base_tokens:
        return []

    dim = len(base_tokens[0])
    X = exprvars('x', dim)
    f = expr(0)  # start of an OR
    for baseToken in base_tokens:
        prod = expr(1)  # start of an AND
        for i in range(dim):
            if baseToken[i] == 1:
                prod = prod & X[i]
            else:
                prod = prod & ~X[i]
        f = f | prod

    # minimize
    fm, = espresso_exprs(f.to_dnf())

    min_tokens = []
    for s in fm.cover:
        min_token = []
        for i in range(dim):
            if X[i] in s:
                min_token.append(1)
            elif ~X[i] in s:
                min_token.append(0)
            else:
                min_token.append(wildcard)

        min_tokens.append(min_token)

    return min_tokens

