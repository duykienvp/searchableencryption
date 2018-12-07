""" Benchmark HVE component
"""
import csv
import time
import math
from collections import defaultdict
from .context import hve, hvehelper, util, parse_params_from_string, \
    pairingcurves, pairinggroup
from .test_hve import create_random_test

from charm.toolbox.integergroup import IntegerGroup

METHOD_SET_UP = 'setup'
METHOD_ENCRYPT = 'encrypt'
METHOD_GEN_TOKEN = 'gen_token'
METHOD_QUERY = 'query'
CIPHER_TEXT_SIZE = 'ctx_size'
TOKEN_SIZE = 'token_size'


def benchmark_hve_sigle_set(
        indices: list,
        queries: list,
        groupParam: dict):
    """ Benchmark HVE with simple set of indices and queries

    :param list indices: list of indices with 0 or 1 entries where 1s indicates locations
    :param list queries: list of queries with 0, 1, or `WILDCARD`
    :param dict groupParam: group parameters

    :returns: dictionary of: method name => list of running times of this method
    """
    bm_values = defaultdict(list)
    width = util.check_size(indices, queries)

    start_time = time.time()
    (pk, sk) = hve.setup(width=width, group_param=groupParam)
    end_time = time.time()
    bm_values[METHOD_SET_UP].append(end_time - start_time)

    C = []

    for index in indices:
        start_time = time.time()
        C_i = hve.encrypt(pk, index)
        end_time = time.time()
        bm_values[METHOD_ENCRYPT].append(end_time - start_time)

        bm_values[CIPHER_TEXT_SIZE].append(get_ctx_size(C_i))

        C.append(C_i)

    for qi, query in enumerate(queries):
        start_time = time.time()
        token = hve.gen_token(sk, query)
        end_time = time.time()
        bm_values[METHOD_GEN_TOKEN].append(end_time - start_time)
        bm_values[TOKEN_SIZE].append(get_ctx_size(token))

        for ci, cipher in enumerate(C):
            start_time = time.time()
            hve.query(token, cipher, predicate_only=True, group=pk['group'])
            end_time = time.time()
            bm_values[METHOD_QUERY].append(end_time - start_time)

    return bm_values


def get_ctx_size(cipher_text):
    """
    """
    ct_sizeinbytes = 0
    for key, elem in cipher_text.items():
        if type(elem) == list:
            # 1 byte for each element in the list
            ct_sizeinbytes += len(elem)
        elif type(elem) == dict:
            # 1 byte for each element in the dict
            ct_sizeinbytes += len(elem)
            for val in elem.values():
                ct_sizeinbytes += get_element_size(val)
        else:
            # this is an Element type
            ct_sizeinbytes += get_element_size(elem)

    return ct_sizeinbytes


def get_element_size(element):
    """
    """
    # this is an Element type
    elem_sizeinbytes = 0
    # extract integers from elem
    str_rep = ''.join(filter(lambda c: c == ' ' or c.isdigit(), str(element)))
    delim_size = len(str(element)) - len(str_rep)  # number of delimiter characters
    elem_sizeinbytes += delim_size
    L = [int(s) for s in str_rep.split()]
    for x in L:
        intsize = int(math.ceil(math.log2(x) / 8))
        elem_sizeinbytes += intsize
    return elem_sizeinbytes


def benchmark_hve_sigle_operation():
    """
    """
    group_params = dict()
    group_params[256] = parse_params_from_string(pairingcurves.PAIRING_CURVE_TYPE_A1_256_SAMPLE)
    group_params[512] = parse_params_from_string(pairingcurves.PAIRING_CURVE_TYPE_A1_512_SAMPLE)
    group_params[1024] = parse_params_from_string(pairingcurves.PAIRING_CURVE_TYPE_A1_1024_SAMPLE)
    group_params[2048] = parse_params_from_string(pairingcurves.PAIRING_CURVE_TYPE_A1_2048_SAMPLE)

    num_runs = 10
    headers = ['bitLen', 'time_random_element', 'time_power_g', 'time_random_element_subgroup',
               'time_random_element_zr', 'time_pair',
               'time_power_gt', 'time_mul_two_subgroup', 'time_div_gt']
    with open('benchmark_operation.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for bitLen, groupParam in group_params.items():
            print('--------------------------------------------')
            print('bitLen=', bitLen)
            int_group = IntegerGroup()

            p = int(groupParam[hvehelper.PARAM_KEY_N0])
            q = int(groupParam[hvehelper.PARAM_KEY_N1])

            group = pairinggroup.PairingGroup()
            group.init_from_str(pairinggroup.convert_params_to_string(groupParam))

            start_time = time.time()
            for _ in range(num_runs):
                tmp = group.random(pairinggroup.G1)
            end_time = time.time()
            time_random_element = (end_time - start_time) / num_runs
            print('time_random_element=', time_random_element)
            tmp = group.random(pairinggroup.G1)
            print('base_1:', tmp)

            start_time = time.time()
            for i in range(num_runs):
                _ = tmp ** p
            end_time = time.time()
            time_power_g = (end_time - start_time) / num_runs
            print('time_power_g=', time_power_g)
            time_random_element_subgroup = time_random_element + time_power_g
            print('time_random_element_subgroup=', time_random_element_subgroup)

            start_time = time.time()
            for _ in range(num_runs):
                a = int_group.random(max=int(p))
            end_time = time.time()
            time_random_element_zr = (end_time - start_time) / num_runs
            print('time_random_element_zr=', time_random_element_zr)
            a = int(hve.random_zr(int_group, p))

            g = hve.random_gp(group, p, q)
            v = hve.random_gp(group, p, q)

            start_time = time.time()
            for _ in range(num_runs):
                tmp = hve.pair(g, v)
            end_time = time.time()
            time_pair = (end_time - start_time) / num_runs
            print('time_pair=', time_pair)
            A = hve.pair(g, v)
            print('base_2:', A)

            start_time = time.time()
            for _ in range(num_runs):
                tmp = A ** p
            end_time = time.time()
            time_power_gt = (end_time - start_time) / num_runs
            print('time_power_gt=', time_power_gt)

            tmp = hve.random_gq(group, p, q)
            start_time = time.time()
            for _ in range(num_runs):
                v * tmp
            end_time = time.time()
            time_mul_two_subgroup = (end_time - start_time) / num_runs
            print('time_mul_two_subgroup=', time_mul_two_subgroup)

            g = hve.random_gp(group, p, q)
            v = hve.random_gp(group, p, q)
            t1 = hve.pair(g, v)
            g = hve.random_gp(group, p, q)
            v = hve.random_gp(group, p, q)
            t2 = hve.pair(g, v)

            start_time = time.time()
            for _ in range(num_runs):
                t1 / t2
            end_time = time.time()
            time_div_gt = (end_time - start_time) / num_runs
            print('time_div_gt=', time_div_gt)

            writer.writerow([
                bitLen,
                time_random_element,
                time_power_g,
                time_random_element_subgroup,
                time_random_element_zr,
                time_pair,
                time_power_gt,
                time_mul_two_subgroup,
                time_div_gt])


def benchmark_hve():
    """ Benchmark HVE with different configuration
    """
    group_params = dict()
    group_params[256] = parseParamsFromString(pairingcurves.PAIRING_CURVE_TYPE_A1_256_SAMPLE)
    group_params[512] = parseParamsFromString(pairingcurves.PAIRING_CURVE_TYPE_A1_512_SAMPLE)
    group_params[1024] = parseParamsFromString(pairingcurves.PAIRING_CURVE_TYPE_A1_1024_SAMPLE)
    group_params[2048] = parse_params_from_string(pairingcurves.PAIRING_CURVE_TYPE_A1_2048_SAMPLE)

    widths = [r * r for r in range(4, 10)]

    num_indices = 5
    num_queries = 5

    output_str_format = '{bitLen} {width} {num_indices} {num_queries} {num_wildcards}' \
        + ' {setup_avg} {encrypt_avg} {gen_token_avg} {query_avg} {ctx_avg} {token_avg}'

    headers = ['bitLen', 'width', 'num_indices', 'num_queries', 'num_wildcards', 'setup_avg',
               'encrypt_avg', 'gen_token_avg', 'query_avg', 'ctx_avg', 'token_avg']
    with open('benchmark.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for bitLen, groupParam in group_params.items():
            for width in widths:
                tmp = list(range(0, int(width / 2) + 1, 5))
                # make sure that the last element is always int(width / 2)
                if tmp[-1] != int(width / 2):
                    tmp.append(int(width / 2))

                for num_wildcards in tmp:
                    # for num_wildcards in range(1):
                    (indices, queries, results) = \
                        create_random_test(width, num_indices, num_queries, num_wildcards)

                    bm_values = benchmark_hve_sigle_set(indices, queries, groupParam)
                    setup_avg = sum(bm_values[METHOD_SET_UP]) / len(bm_values[METHOD_SET_UP])
                    encrypt_avg = sum(bm_values[METHOD_ENCRYPT]) / len(bm_values[METHOD_ENCRYPT])
                    gen_token_avg = sum(bm_values[METHOD_GEN_TOKEN]) / len(bm_values[METHOD_GEN_TOKEN])
                    query_avg = sum(bm_values[METHOD_QUERY]) / len(bm_values[METHOD_QUERY])
                    ctx_avg = sum(bm_values[CIPHER_TEXT_SIZE]) / len(bm_values[CIPHER_TEXT_SIZE])
                    token_avg = sum(bm_values[TOKEN_SIZE]) / len(bm_values[TOKEN_SIZE])
                    print(output_str_format.format(
                        bitLen=bitLen,
                        width=width,
                        num_indices=num_indices,
                        num_queries=num_queries,
                        num_wildcards=num_wildcards,
                        setup_avg=setup_avg,
                        encrypt_avg=encrypt_avg,
                        gen_token_avg=gen_token_avg,
                        query_avg=query_avg,
                        ctx_avg=ctx_avg,
                        token_avg=token_avg
                    ))

                    writer.writerow([bitLen, width, num_indices, num_queries, num_wildcards, setup_avg,
                                    encrypt_avg, gen_token_avg, query_avg, ctx_avg, token_avg])




