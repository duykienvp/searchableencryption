""" Helper module to run HVE scheme
"""
from searchableencryption.hve import util


def run_hve_multiple(hve_quadruple: tuple,
                     indices: list,
                     queries: list,
                     groupParam: dict):
    """ Run HVE with multiple indices and queries

    :param tuple hve_quadruple: quadruple of HVE functions (setup, encrypt, gen_token, query)
    :param list indices: list of indices with 0 or 1 entries where 1s indicates locations
    :param list queries: list of queries with 0, 1, or `WILDCARD`
    :param dict groupParam: group parameters

    :returns: list of list of matched indices of each query
    """
    setup = hve_quadruple[0]
    encrypt = hve_quadruple[1]
    gen_token = hve_quadruple[2]
    query = hve_quadruple[3]

    width = util.check_size(indices, queries)
    print('width:', width)

    (pk, sk) = setup(width=width, group_param=groupParam)
    print('Done setup')

    C = []

    for index in indices:
        C.append(encrypt(pk, index))
    print('Done encrypt')

    matches = []
    for qi, I_star in enumerate(queries):
        token = gen_token(sk, I_star)
        print('Done gen token')

        matched_items = list()

        for ci, cipher in enumerate(C):
            matched = query(token, cipher, predicate_only=True, group=pk['group'])
            if matched:
                # matched
                matched_items.append(ci)

        matches.append(matched_items)

    return matches
