""" Hidden Vector Encryption based on the Appendix of
'An Efficient Privacy-Preserving System for Monitoring Mobile Users:
Making Searchable Encryption Practical'

Link: https://dl.acm.org/citation.cfm?id=2557559

Names of variables follows the naming of the Appendix.

Even though in this implementation, the same group object is passed around
(it does not contain any private information),
one can easily adapt to only pass the parameters around
"""

from charm.toolbox.integergroup import IntegerGroup

from searchableencryption.hve.util import PARAM_KEY_N0, PARAM_KEY_N1, get_unit_element
from searchableencryption.toolbox.pairinggroup \
    import PairingGroup, G1, GT, pair, convert_params_to_string


def setup(width: int, group_param: dict):
    """
    Performs the setup algorithm for HVE.

    The group params should:
    - 'type': 'a1'
    - contain values for 'p', 'n', 'l'
    - contain 2 primes 'n0', 'n1' where n = n0 * n1

    :param int width: the length of attribute vector
    :param dict group_param: group parameters

    :returns: (publicKey, secretKey) pair
    """
    int_group = IntegerGroup()

    p = group_param[PARAM_KEY_N0]
    q = group_param[PARAM_KEY_N1]

    group_param_copy = group_param.copy()  # remove private components of the group parameters
    group_param_copy.pop(PARAM_KEY_N0, None)
    group_param_copy.pop(PARAM_KEY_N1, None)

    group = PairingGroup()
    group.init_from_str(convert_params_to_string(group_param_copy))

    g_q = random_gq(group, p, q)
    a = int(random_zr(int_group, p))

    u = {}
    h = {}
    w = {}
    for i in range(width):
        u[i] = random_gp(group, p, q)
        h[i] = random_gp(group, p, q)
        w[i] = random_gp(group, p, q)

    g = random_gp(group, p, q)
    v = random_gp(group, p, q)
    assert g.initPP(), "ERROR: Failed to init pre-computation table for g."
    assert v.initPP(), "ERROR: Failed to init pre-computation table for v."

    V = v * random_gq(group, p, q)
    A = pair(g, v) ** a
    U = {}
    H = {}
    W = {}
    for i in range(width):
        U[i] = u[i] * random_gq(group, p, q)
        H[i] = h[i] * random_gq(group, p, q)
        W[i] = w[i] * random_gq(group, p, q)

    pk = {'group': group,
          'g_q': g_q,
          'V': V,
          'A': A,
          'U': U,
          'H': H,
          'W': W}

    sk = {'group': group,
          'g_q': g_q,
          'a': a,
          'u': u,
          'h': h,
          'w': w,
          'g': g,
          'v': v,
          'p': p,
          'q': q}

    return (pk, sk)


def encrypt(pk, I, M=None):
    """ Encrypt a index vector I with values of components as 0 or 1, with optional message M

    The message is an element in GT. If it is not provided, the identity element of GT is used

    :param pk: public key
    :param I: a index vector
    :param M: message
    :returns: cipher text for I (and M if any)
    """
    int_group = IntegerGroup()
    g_q = pk['g_q']
    group = pk['group']
    n = group.order()
    s = int(random_zr(int_group, n))
    if M is None:
        M = get_unit_element(group, GT)
    C_prime = (pk['A'] ** s) * M

    Z = g_q ** int(random_zr(int_group, n))
    C_0 = (pk['V'] ** s) * Z

    C_1 = {}
    C_2 = {}
    U = pk['U']
    H = pk['H']
    W = pk['W']
    for i in range(len(I)):
        Z_1_i = g_q ** int(random_zr(int_group, n))
        C_1[i] = (((U[i] ** I[i]) * H[i]) ** s) * Z_1_i

        Z_2_i = g_q ** int(random_zr(int_group, n))
        C_2[i] = (W[i] ** s) * Z_2_i

    C = {'C_prime': C_prime,
         'C_0': C_0,
         'C_1': C_1,
         'C_2': C_2}

    return C


def gen_token(sk, I_star):
    """ Create search token for a given query I_star.
    Elements of I_star is 0, 1, or a `WILDCARD`.

    :param sk: secret key
    :param I_star: query
    :returns: search token
    """
    intGroup = IntegerGroup()

    u = sk['u']
    h = sk['h']
    w = sk['w']
    v = sk['v']
    g = sk['g']
    a = sk['a']
    p = sk['p']

    K_0 = g ** a
    r_1 = {}
    r_2 = {}
    for i in range(len(I_star)):
        r_1[i] = int(random_zr(intGroup, p))
        r_2[i] = int(random_zr(intGroup, p))

    for i in range(len(I_star)):
        if I_star[i] != 0 and I_star[i] != 1:
            continue
        tmp = u[i] ** I_star[i]
        tmp = tmp * h[i]
        tmp = tmp ** r_1[i]
        tmp = tmp * (w[i] ** r_2[i])
        K_0 = K_0 * tmp

    K_1 = {}
    K_2 = {}
    for i in range(len(I_star)):
        K_1[i] = v ** r_1[i]
        K_2[i] = v ** r_2[i]

    token = {'I_star': I_star,
             'K_0': K_0,
             'K_1': K_1,
             'K_2': K_2}

    return token


def query(token, cipher, predicate_only=False, group=None):
    """ Evaluates if the predicate represented by `token` holds for ciphertext `cipher`.
    If evaluating predicate only
    (i.e. only check if `token` holds for ciphertext `cipher`
    and do not care about message in the cipher text),
    the group should be passed because the output of decryption will be compared
    to the identity element of GT in the group

    :param token: search token
    :param cipher: cipher text
    :param bool predicate_only: whether or not only evaluates predicate
    :param PairingGroup group: the pairing group, only needed if predicateOnly
    :returns: if predicateOnly, return whether the predicate represented by `token`
              holds for cipher text `cipher`;
              otherwise, return the decrypted message
              (which is the orginal message if the decryption succeeded
              or just a random element in GT)
    """
    I_star = token['I_star']
    C_prime = cipher['C_prime']
    C_0 = cipher['C_0']
    C_1 = cipher['C_1']
    C_2 = cipher['C_2']
    K_0 = token['K_0']
    K_1 = token['K_1']
    K_2 = token['K_2']

    tmp = 1
    for i in range(len(I_star)):
        if I_star[i] != 0 and I_star[i] != 1:
            continue
        tmp = tmp * pair(C_1[i], K_1[i]) * pair(C_2[i], K_2[i])
    tmp = pair(C_0, K_0) / tmp
    M_prime = C_prime / tmp

    if predicate_only:
        assert group is not None, "Error: group must be provided when evaluate predicate only"
        M_identity = get_unit_element(group, GT)
        return M_identity == M_prime

    return M_prime


def random_gp(group: PairingGroup, p, q):
    return group.random(G1) ** q


def random_gq(group: PairingGroup, p, q):
    return group.random(G1) ** p


def random_zr(group: IntegerGroup, r):
    """ Generate a random element in Zr
    """
    return group.random(max=int(r))
