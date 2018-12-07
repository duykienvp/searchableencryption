""" Execute tasks
"""
import argparse
import sys

TASK_TEST = 'test'
TASK_BENCHMARK = 'benchmark'
TASKS = [TASK_TEST, TASK_BENCHMARK]

SCHEME_HVE = 'hve'
SCHEME_HVE_HE = 'hvehe'
SCHEME_HVE_GE = 'hvege'
SCHEME_HVE_PRIME = 'hveprime'
SCHEME_IPE = 'ipe'
SCHEME_TIFE = 'tife'
SCHEME_BINEXPRMIN = 'binexprmin'
SCHEMES = [SCHEME_HVE, SCHEME_HVE_HE, SCHEME_HVE_GE, SCHEME_HVE_PRIME, SCHEME_IPE, SCHEME_TIFE, SCHEME_BINEXPRMIN]


class MyParser(argparse.ArgumentParser):
    """ An parse to print help whenever an error occurred to the parsing process
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    parser = MyParser(description='Execute a task')
    parser.add_argument('-t',
                        '--task',
                        help='Task name',
                        choices=TASKS,
                        required=True)
    parser.add_argument('-s',
                        '--scheme',
                        help='Encryption scheme',
                        choices=SCHEMES,
                        required=True)
    parser.add_argument('-v',
                        '--verbose',
                        help='increase output verbosity',
                        action='store_true')

    # print help if no argument is provided.
    # This may be necessary if no provisional arguement is declared
    # if len(sys.argv) == 1:
    #     parser.print_help(sys.stderr)
    #     sys.exit(1)
    args = parser.parse_args()

    if args.task == TASK_TEST:
        if args.scheme == SCHEME_HVE:
            import tests.test_hve as test
            test.test_hve_simple()
            test.test_hve_multiple()

        if args.scheme == SCHEME_HVE_HE:
            import tests.test_hvehe as test
            test.test_hve_he_simple()

        if args.scheme == SCHEME_HVE_GE:
            import tests.test_hvege as test
            test.test_hve_ge_simple()

        if args.scheme == SCHEME_HVE_PRIME:
            import tests.test_hveprime as test
            test.test_hve_simple()
            test.test_hve_multiple()

        if args.scheme == SCHEME_IPE:
            import tests.test_ipe as test
            test.test_ipe()

        if args.scheme == SCHEME_TIFE:
            import tests.test_ipe as test
            test.test_tife()

        if args.scheme == SCHEME_BINEXPRMIN:
            import tests.test_binexprmin as test
            test.test_binexprmin()

    if args.task == TASK_BENCHMARK:
        if args.scheme == SCHEME_HVE:
            import tests.benchmark_hve as benchmark_hve
            # benchmark_hve.benchmark_hve()
            benchmark_hve.benchmark_hve_sigle_operation()

