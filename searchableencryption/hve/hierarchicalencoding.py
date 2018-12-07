""" HVE with hierarchical encoding.
Section 3.2 of 'An Efficient Privacy-Preserving System for Monitoring Mobile Users:
Making Searchable Encryption Practical'

Link: https://dl.acm.org/citation.cfm?id=2557559
"""


def encode_cell_id(dim: int, row: int, col: int) -> list:
    """ Get hierarchical encoding binary representation of cell (row, col) with the grid of dim x dim.
    See Section 3.2 in `https://dl.acm.org/citation.cfm?id=2557559`

    :param int dim: dimension of the grid
    :param int row: row index
    :param int col: col index

    :returns: a list of binary representation
    """
    rep = []
    mid = int(dim / 2)

    if col < mid:
        rep.append(0)
    else:
        rep.append(1)
        col -= mid

    if row < mid:
        rep.append(0)
    else:
        rep.append(1)
        row -= mid

    if 1 < mid:
        rep.extend(encode_cell_id(mid, row, col))

    return rep
