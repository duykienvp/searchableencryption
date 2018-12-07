""" HVE with gray encoding.
Section 3.3 of 'An Efficient Privacy-Preserving System for Monitoring Mobile Users:
Making Searchable Encryption Practical'

Link: https://dl.acm.org/citation.cfm?id=2557559
"""


def get_encoding_vector(dim: int) -> list:
    """ Get grey encoding binary representation of vector dimension dim.
    See Section 3.3 in `https://dl.acm.org/citation.cfm?id=2557559`

    :param int dim: dimension of the vector

    :returns: a list of binary representation
    """
    if dim == 1:
        return [[0], [1]]

    g_prev = get_encoding_vector(dim - 1)

    rep = []

    for val in g_prev:
        rep.append([0] + val)

    for val in reversed(g_prev):
        rep.append([1] + val)

    return rep


def encode_cell_id(dim: int, row: int, col: int) -> list:
    """ Get grey encoding binary representation of cell (row, col) with the grid of dim x dim.
    See Section 3.3 in `https://dl.acm.org/citation.cfm?id=2557559`

    :param int dim: dimension of the grid
    :param int row: row index
    :param int col: col index

    :returns: a list of binary representation
    """
    g_dim = get_encoding_vector(dim)

    rep = g_dim[row] + g_dim[col]

    return rep
