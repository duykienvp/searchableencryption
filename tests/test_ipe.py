"""
Copyright (c) 2016, Kevin Lewi

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
"""

"""
Tests the correctness of the implementation of IPE and two-input functional
encryption.
"""

import random  # noqa: E402

from .context import ipe, tife  # noqa: E402


def test_ipe():
    """
    Runs a test on IPE for toy parameters.
    """
    print("Start test_ipe()")

    n = 10
    M = 20
    x = [random.randint(0, M) for i in range(n)]
    y = [random.randint(0, M) for i in range(n)]

    # use this test to test for orthogonal vectors
    # x = [0] * n
    # y = [0] * n
    # x[1] = 1
    # y[1] = 1

    checkprod = sum(map(lambda i: x[i] * y[i], range(n)))

    (pp, sk) = ipe.setup(n)
    print('Done setup')
    skx = ipe.keygen(sk, x)
    cty = ipe.encrypt(sk, y)
    prod = ipe.decrypt(pp, skx, cty, M * M * n)
    # need to pass group in to test to unit element
    # prod = ipe.decrypt(sk[3], pp, skx, cty, M * M * n)
    assert prod == checkprod, "Failed test_ipe"
    print("test_ipe PASSED")


def test_tife():
    """
    Runs a test on two-input functional encryption for the comparison function on
    toy parameters.
    """
    print("Start test_tife()")

    def test_f(x, y):
        return 1 if x < y else 0

    N = 30
    f = test_f

    x = random.randint(0, N - 1)
    y = random.randint(0, N - 1)

    (pp, sk) = tife.setup(N, f)
    ctx = tife.encryptL(sk, x)
    cty = tife.encryptR(sk, y)
    result = tife.decrypt(pp, ctx, cty)
    assert result == f(x, y), "Failed test_tife"
    print("test_tife PASSED")
