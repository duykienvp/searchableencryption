""" Some utility functions
"""

WILDCARD = '*'
PARAM_KEY_N0 = 'n0'
PARAM_KEY_N1 = 'n1'


def shift_left_bit_length(x: int) -> int:
    """ Shift 1 left bit length of x

    :param int x: value to get bit length
    :returns: 1 shifted left bit length of x
    """
    return 1 << (x - 1).bit_length()


def next_power_2(x: int) -> int:
    """ Get the next number that is power of 2 and bigger than x

    :param int x: value to evaluate
    :returns: the next number that is power of 2 and bigger than x or 0 if x < 1
    """
    return 0 if x < 1 else shift_left_bit_length(x)


def check_size(indices: list, queries: list) -> int:
    """ Check whether size of all indices and queries are the same

    :param list indices: list of all indices
    :param list queries: list of all queries
    :returns: the size when size of all indices and queries are the same or -1
              if lists does not have same size
    """
    width = 0
    # get the first length if any
    if indices:
        width = len(indices[0])
    elif queries:
        width = len(queries[0])

    # at this point, width will be the length of 1 of the indices or queries,
    # or will still be 0 if there is no index or query
    for index in indices:
        if len(index) != width:
            print('Indices are not the same width')
            return -1

    for query in queries:
        if len(query) != width:
            print('Queries and indices not the same width')
            return -1

    return width


def get_unit_element(group, component):
    """ Get unit element of a group component (ZR, G1, G2, or GT)

    :param PairingGroup group: a group object
    :param int component: a group component (ZR, G1, G2, or GT)
    """
    return group.random(component) ** 0
