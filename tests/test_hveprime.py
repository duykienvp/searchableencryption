from .context import hvehelper, pairingcurves, parse_params_from_string
from .context import hveprime
from . import test_hve


def test_hve_simple():
    """ A simple test
    """
    print("Start test_hve_simple()")
    hve_quadruple = (hveprime.setup, hveprime.encrypt, hveprime.gen_token, hveprime.query)
    test_hve.run_test_hve_simple(hve_quadruple)


def test_hve_multiple():
    """
    Runs a test on HVE for toy parameters.
    """
    print("Start test_hve()")
    hve_quadruple = (hveprime.setup, hveprime.encrypt, hveprime.gen_token, hveprime.query)

    group_param = parse_params_from_string(pairingcurves.PAIRING_CURVE_TYPE_A1_256_SAMPLE)

    tests = test_hve.create_test()
    for t in tests:
        expected_results = t[2]
        results = hvehelper.run_hve_multiple(hve_quadruple, t[0], t[1], group_param)
        for i, expectedResult in enumerate(expected_results):
            assert set(expectedResult) == set(results[i]), 'Incorrect matched items'
