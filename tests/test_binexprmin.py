""" Test binary expression minimization
"""
from collections import Counter
from .context import binexprminimizer


def test_binexprmin():
    """ Run test binary expression minimization
    """
    tokens = [
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 1, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 1]
    ]

    min_tokens = binexprminimizer.perform_bin_expr_min(tokens)
    exp_results = [
        [1, '*', 1, '*'],
        [1, 0, '*', '*'],
        ['*', 0, 1, 0]
    ]

    assert len(min_tokens) == len(exp_results), 'Incorrect length'
    for exp_result in exp_results:
        found = False
        for minToken in min_tokens:
            if Counter(exp_result) == Counter(minToken):
                found = True
                break
        if not found:
            assert False, 'Expected result not found'
    print('Test PASSED')

