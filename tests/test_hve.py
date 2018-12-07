
"""
Tests the correctness of the implementation of HVE encryption.
"""
import random  # noqa: E402
from .context import hve, hvehelper, pairingcurves, GT, parse_params_from_string, WILDCARD


def create_hardcoded_test():
    """ Create a hardcoded sample test
    """
    indices = []
    queries = []
    results = []
    idx = [0, 0, 0, 0,
           0, 0, 1, 0,
           0, 0, 0, 0,
           0, 0, 0, 0]
    indices.append(idx)
    idx = [0, 0, 0, 0,
           0, 0, 0, 0,
           0, 0, 1, 0,
           0, 0, 0, 0]
    indices.append(idx)
    idx = [1, 0, 0, 0,
           0, 0, 0, 0,
           0, 0, 0, 0,
           0, 0, 0, 0]
    indices.append(idx)
    idx = [0, 0, 0, 0,
           0, 0, 0, 0,
           0, 0, 0, 0,
           1, 0, 0, 0]
    indices.append(idx)

    query = [0, 0, 0, 0,
             0, WILDCARD, WILDCARD, 0,
             0, WILDCARD, WILDCARD, 0,
             0, 0, 0, 0]
    queries.append(query)
    query = [0, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0,
             WILDCARD, WILDCARD, 0, 0]
    queries.append(query)

    result = [0, 1]  # matched indices for query 1
    results.append(result)
    result = [3]     # matched indices for query 2
    results.append(result)

    return indices, queries, results


def create_random_test(width: int, num_indices: int, num_queries: int, num_wildcards: int):
    """ Create a random test

    :param int width: the length of the attribute vector (or index)
    :param int num_indices: number of indices to generate
    :param int num_queries: number of queries to generate
    :param int num_wildcards: number of wildcards to in each query
    """
    start_range = 0
    end_range = width

    indices = []
    queries = []
    results = []
    # maxQuerySize = 6  # max number of WILDCARD in a query

    # create indices
    for _ in range(num_indices):
        idx = [0] * end_range

        pos = random.randint(start_range, end_range - 1)
        idx[pos] = 1

        indices.append(idx)

    # create queries
    for _ in range(num_queries):
        query = [0] * end_range

        # querySize = random.randint(0, maxQuerySize)
        for _ in range(num_wildcards):
            pos = random.randint(start_range, end_range - 1)
            query[pos] = WILDCARD

        queries.append(query)

        # find results
        result = []
        for (i, idx) in enumerate(indices):
            matched = True
            for pos in range(end_range):
                if query[pos] == WILDCARD:
                    continue
                if query[pos] != idx[pos]:
                    matched = False
                    break
            if matched:
                result.append(i)

        results.append(result)

    return indices, queries, results


def create_test():
    """ Create a sample test
    """
    tests = list()

    tests.append(create_hardcoded_test())
    tests.append(create_random_test(width=16, num_indices=3, num_queries=3, num_wildcards=5))

    return tests


def run_test_hve_simple(hve_quadruple: tuple):
    """ A simple test
    """
    setup = hve_quadruple[0]
    encrypt = hve_quadruple[1]
    gen_token = hve_quadruple[2]
    query = hve_quadruple[3]

    group_param = parse_params_from_string(pairingcurves.PAIRING_CURVE_TYPE_A1_256_SAMPLE)

    width = 8

    (pk, sk) = setup(width=width, group_param=group_param)

    print('Done setup')

    print('Testing predicate only')
    I = [0, 0, 1, 0, 0]  # noqa: E741
    cipher = encrypt(pk, I)
    print('Done encrypt')

    I_star = [0, WILDCARD, 1, 0, 0]
    token = gen_token(sk, I_star)
    print('Done gen token')

    matched = query(token, cipher, predicate_only=True, group=pk['group'])
    if matched:
        print('Test PASSED')
    else:
        print('Test FAILED.')

    I_star = [0, WILDCARD, 0, 0, 0]
    token = gen_token(sk, I_star)
    print('Done gen token')

    matched = query(token, cipher, predicate_only=True, group=pk['group'])
    if not matched:
        print('Test PASSED.')
    else:
        print('Test FAILED.')

    print('Test with message')
    M = pk['group'].random(GT)
    cipher = encrypt(pk, I, M)

    I_star = [0, WILDCARD, 1, 0, 0]
    token = gen_token(sk, I_star)
    print('Done gen token')

    M_prime = query(token, cipher)
    if M_prime == M:
        print('Test PASSED')
    else:
        print('Test FAILED.')

    I_star = [0, WILDCARD, 0, 0, 0]
    token = gen_token(sk, I_star)
    print('Done gen token')

    M_prime = query(token, cipher)
    if M_prime != M:
        print('Test PASSED.')
    else:
        print('Test FAILED.')

    print("Done test_hve()")


def test_hve_simple():
    """ A simple test
    """
    print("Start test_hve_simple()")
    run_test_hve_simple((hve.setup, hve.encrypt, hve.gen_token, hve.query))


def test_hve_multiple():
    """
    Runs a test on HVE for toy parameters.
    """
    print("Start test_hve()")
    hve_quadruple = (hve.setup, hve.encrypt, hve.gen_token, hve.query)

    group_param = parse_params_from_string(pairingcurves.PAIRING_CURVE_TYPE_A1_256_SAMPLE)

    tests = create_test()
    for t in tests:
        expected_results = t[2]
        results = hvehelper.run_hve_multiple(hve_quadruple, t[0], t[1], group_param)
        for i, expectedResult in enumerate(expected_results):
            assert set(expectedResult) == set(results[i]), 'Incorrect matched items'
