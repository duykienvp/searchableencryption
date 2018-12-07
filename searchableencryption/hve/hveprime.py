""" Hidden Vector Encryption with Groups of Prime Order

Link: https://dl.acm.org/citation.cfm?id=1431889

"""
from searchableencryption.hve.util import get_unit_element
from searchableencryption.toolbox.pairinggroup \
    import PairingGroup, ZR, G1, GT, pair, convert_params_to_string


def setup(width: int, group_param: dict):
    """
    Performs the setup algorithm for HVE.

    The group params should:
    - 'type': 'a'
    - contain values for 'q', 'h', 'r', 'exp2', 'exp1', 'sign1', 'sign0'

    :param int width: the length of attribute vector
    :param dict group_param: group parameters

    :returns: (public_key, secret_key) pair
    """
    group = PairingGroup()
    group.init_from_str(convert_params_to_string(group_param))

    g = group.random(G1)
    assert g.initPP(), "ERROR: Failed to init pre-computation table for g."

    y = group.random(ZR)
    Y = pair(g, g) ** y

    t = dict()
    v = dict()
    r = dict()
    m = dict()
    T = dict()
    V = dict()
    R = dict()
    M = dict()
    for i in range(width):
        t[i] = group.random(ZR)
        T[i] = g ** t[i]
        v[i] = group.random(ZR)
        V[i] = g ** v[i]
        r[i] = group.random(ZR)
        R[i] = g ** r[i]
        m[i] = group.random(ZR)
        M[i] = g ** m[i]

    pk = {'group': group,
          'g': g,
          'Y': Y,
          'T': T,
          'V': V,
          'R': R,
          'M': M}

    sk = {'group': group,
          'g': g,
          'y': y,
          't': t,
          'v': v,
          'r': r,
          'm': m}

    return (pk, sk)


def encrypt(pk, x, message=None):
    """ Encrypt a vector x with values of components as 0 or 1, with optional message

    The message is an element in GT. If it is not provided, the identity element of GT is used

    :param pk: public key
    :param x: a vector
    :param message: message
    :returns: cipher text for x (and message if any)
    """
    group = pk['group']
    g = pk['g']
    s = group.random(ZR)

    if message is None:
        message = get_unit_element(group, GT)
    omega = (pk['Y'] ** (-s)) * message
    C_0 = g ** s

    X = dict()
    W = dict()
    T = pk['T']
    V = pk['V']
    R = pk['R']
    M = pk['M']
    for i in range(len(x)):
        s_i = group.random(ZR)
        if x[i] == 1:
            X[i] = T[i] ** (s - s_i)
            W[i] = V[i] ** s_i
        else:
            X[i] = R[i] ** (s - s_i)
            W[i] = M[i] ** s_i

    cipher = {'omega': omega,
              'C_0': C_0,
              'X': X,
              'W': W}

    return cipher


def gen_token(sk, I_star):
    """ Create search token for a given query I_star.
    Elements of I_star is 0, 1, or a `WILDCARD`.

    :param sk: secret key
    :param I_star: query
    :returns: search token
    """
    group = sk['group']
    g = sk['g']
    y = sk['y']

    num_non_start = 0
    for val in I_star:
        num_non_start += 1 if val == 0 or val == 1 else 0

    if num_non_start == 0:
        K_y = g ** y
    else:
        # gen a_i
        Y = dict()
        L = dict()
        a = dict()
        count = 0
        sum_a = 0
        for i in range(len(I_star)):
            if I_star[i] == 0 or I_star[i] == 1:
                if count == num_non_start - 1:
                    # this is the last a_i
                    a[i] = y - sum_a
                    break
                else:
                    a[i] = group.random(ZR)
                    sum_a += a[i]
                    count += 1

        t = sk['t']
        v = sk['v']
        r = sk['r']
        m = sk['m']
        Y = dict()
        L = dict()
        for i in range(len(I_star)):
            if I_star[i] == 1:
                Y[i] = g ** (a[i] / t[i])
                L[i] = g ** (a[i] / v[i])
            elif I_star[i] == 0:
                Y[i] = g ** (a[i] / r[i])
                L[i] = g ** (a[i] / m[i])
            else:
                Y[i] = None
                L[i] = None

        K_y = (Y, L)

    token = {'I_star': I_star,
             'K_y': K_y}

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
    omega = cipher['omega']
    C_0 = cipher['C_0']
    I_star = token['I_star']
    K_y = token['K_y']

    num_non_start = 0
    for val in I_star:
        num_non_start += 1 if val == 0 or val == 1 else 0

    if num_non_start == 0:
        message_prime = omega * pair(C_0, K_y)
    else:
        X = cipher['X']
        W = cipher['W']
        Y = K_y[0]
        L = K_y[1]

        tmp = omega
        for i in range(len(I_star)):
            if I_star[i] == 0 or I_star[i] == 1:
                tmp = tmp * pair(X[i], Y[i]) * pair(W[i], L[i])
        message_prime = tmp

    if predicate_only:
        assert group is not None, "Error: group must be provided when evaluate predicate only"
        return get_unit_element(group, GT) == message_prime

    return message_prime


