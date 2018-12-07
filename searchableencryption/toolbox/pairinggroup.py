try:
    from charm.toolbox.pairingcurves import params as param_info
    from charm.core.math.pairing import pairing, ZR, G1, G2, GT, init, pair, hashPair,\
        H, random, serialize, deserialize, ismember, order
    import charm.core.math.pairing as pg
    from charm.config import libs, pairing_lib
except Exception as err:
    print(err)
    exit(-1)


class PairingGroup(object):
    """ Replace the same class in Charm toolbox
    """

    def __init__(self, secparam=512, verbose=False):
        self.Pairing = None
        self.secparam = secparam  # number of bits
        self._verbose = verbose

    def init_from_id(self, inParamId):
        """ Initialize pairing from pre-defined ID
        """
        if type(inParamId) == str:
            pairID = param_info.get(inParamId)
            assert pairID is not None, \
                "'%s' not recognized! See 'pairingcurves.py' in toolbox." % inParamId
            if pairing_lib == libs.pbc:
                self.Pairing = pairing(string=pairID)
                self.param = inParamId
            elif pairing_lib in [libs.miracl, libs.relic]:
                self.Pairing = pairing(pairID)
                self.param = pairID
        elif type(inParamId) == int:
            self.Pairing = pairing(inParamId)
            self.param = inParamId

    def init_from_str(self, inParamId):
        """ Initialize pairing from content as a string.
        Only work with PBC pairing lib
        """
        if type(inParamId) == str and pairing_lib == libs.pbc:
            self.Pairing = pairing(string=inParamId)
            self.param = inParamId

    def init_from_file(self, paramFile):
        """ Initialize pairing from a param file.

        Currently doing nothing due to error in C code of Charm which does not close file pointer.
        See 'init_pbc_param' function in 'pairingmodule.c' (line 328)
        """
        pass
        # self.Pairing = pairing(file=param_id)

    def __str__(self):
        return str(self.Pairing)

    def order(self):
        """returns the order of the group"""
        return order(self.Pairing)

    def paramgen(self, qbits, rbits):
        return None

    def ismember(self, obj):
        """membership test for a pairing object"""
        return ismember(self.Pairing, obj)

    def ismemberList(self, obj):
        """membership test for a list of pairing objects"""
        for i in range(len(obj)):
            if not ismember(self.Pairing, obj[i]):
                return False
        return True

    def ismemberDict(self, obj):
        """membership test for a dict of pairing objects"""
        for i in obj.keys():
            if not ismember(self.Pairing, obj[i]):
                return False
        return True

    def groupSetting(self):
        return 'pairing'

    def groupType(self):
        return self.param

    def messageSize(self):
        return self.secparam / 8

    def init(self, type, value=None):
        """initializes an object with a specified type and value"""
        if value is not None:
            return init(self.Pairing, type, value)
        return init(self.Pairing, type)

    def random(self, _type=ZR, count=1, seed=None):
        """selects a random element in ZR, G1, G2 and GT"""
        if _type == GT:
            return self.__randomGT()
        elif _type in [ZR, G1, G2]:
            if seed is not None and count == 1:
                return random(self.Pairing, _type, seed)
            elif count > 1:
                return tuple([random(self.Pairing, _type) for i in range(count)])
            return random(self.Pairing, _type)
        return None

    def __randomGT(self):
        if not hasattr(self, 'gt'):
            self.gt = pair(self.random(G1), self.random(G2))
        z = self.random(ZR)
        return self.gt ** z

    def encode(self, message):
        raise NotImplementedError

    def decode(self, element):
        raise NotImplementedError

    def hash(self, args, type=ZR):
        """hashes objects into ZR, G1 or G2 depending on the pairing curve"""
        return H(self.Pairing, args, type)

    def serialize(self, obj, compression=True):
        """Serialize a pairing object into bytes.

           :param compression: serialize the compressed representation of the
                curve element, taking about half the space but potentially
                incurring in non-negligible computation costs when
                deserializing. Default is True for compatibility with previous
                versions of charm.

            >>> p = PairingGroup('SS512')
            >>> v1 = p.random(G1)
            >>> b1 = p.serialize(v1)
            >>> b1 == p.serialize(v1, compression=True)
            True
            >>> v1 == p.deserialize(b1)
            True
            >>> b1 = p.serialize(v1, compression=False)
            >>> v1 == p.deserialize(b1, compression=False)
            True
        """
        return serialize(obj, compression)

    def deserialize(self, obj, compression=True):
        """Deserialize a bytes serialized element into a pairing object.

           :param compression: must be used for objects serialized with the
                compression parameter set to True. Default is True for
                compatibility with previous versions of charm.
        """
        return deserialize(self.Pairing, obj, compression)

    def debug(self, data, prefix=None):
        if not self._verbose:
            return
        if type(data) == dict:
            for k, v in data.items():
                print(k, v)
        elif type(data) == list:
            for i in range(0, len(data)):
                print(prefix, (i + 1), ':', data[i])
            print('')
        elif type(data) == str:
            print(data)
        else:
            print(type(data), ':', data)
        return

    def pair_prod(self, lhs, rhs):
        """takes two lists of G1 & G2 and computes a pairing product"""
        return pair(lhs, rhs, self.Pairing)

    def InitBenchmark(self):
        """initiates the benchmark state"""
        return pg.InitBenchmark(self.Pairing)

    def StartBenchmark(self, options):
        """starts the benchmark with any of these options:
        RealTime, CpuTime, Mul, Div, Add, Sub, Exp, Pair, Granular"""
        return pg.StartBenchmark(self.Pairing, options)

    def EndBenchmark(self):
        """ends an ongoing benchmark"""
        return pg.EndBenchmark(self.Pairing)

    def GetGeneralBenchmarks(self):
        """retrieves benchmark count for all group operations"""
        return pg.GetGeneralBenchmarks(self.Pairing)

    def GetGranularBenchmarks(self):
        """retrieves group operation count per type: ZR, G1, G2, and GT"""
        return pg.GetGranularBenchmarks(self.Pairing)

    def GetBenchmark(self, option):
        """retrieves benchmark results for any of these options:
        RealTime, CpuTime, Mul, Div, Add, Sub, Exp, Pair, Granular"""
        return pg.GetBenchmark(self.Pairing, option)


def convert_params_to_string(params: dict) -> str:
    """ Create a string representation of parameters in PBC format
    """
    return '\n'.join(['%s %s' % (key, value) for (key, value) in params.items()])


def parse_params_from_string(paramStr: str) -> dict:
    """ Create a dictionary representation of parameters in PBC format
    """
    params = dict()
    lines = paramStr.split('\n')
    for line in lines:
        if line:
            name, value = parse_param_line(line)
            add_param(params, name, value)
    return params


def parse_param_line(line: str) -> tuple:
    """
    """
    replacements = (',', '-', ':')
    for r in replacements:
        line = line.replace(r, ' ')
    elements = line.split()
    name = elements[0]
    value = elements[1]

    return (name, value)


def add_param(params: dict, name: str, value: str):
    """ Add (name, value) params to dict. Value is converted to int value if needed
    """
    if name == 'type':
        params[name] = value
    else:
        params[name] = int(value)


def parse_params_from_file(filePath: str) -> dict:
    """
    """
    params = dict()
    with open(filePath, 'r') as inFile:
        for line in inFile:
            name, value = parse_param_line(line)
            add_param(params, name, value)
    return params


def extract_key(g):
    """
    Given a group element, extract a symmetric key
    :param g:
    :return:
    """
    g_in_hex = hashPair(g).decode('utf-8')
    return bytes(bytearray.fromhex(g_in_hex))
