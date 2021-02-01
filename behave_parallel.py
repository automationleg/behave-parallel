import argparse
import json
import logging
import multiprocessing
import sys
from datetime import datetime
from functools import partial
from multiprocessing import Pool
from subprocess import call, Popen, PIPE
from timeit import default_timer as timer


def create_logger(filename: str):
    """
    create mlogger to dump execution time and duration of features into a logfile
    :return:
    """
    mlogger = multiprocessing.get_logger()
    mlogger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(processName)s;%(message)s')
    handler = logging.FileHandler(filename=filename)
    handler.setFormatter(formatter)

    # to avoid duplicated messages in the output
    if not len(mlogger.handlers):
        mlogger.addHandler(handler)
    return mlogger


logger = create_logger('multiprocessing_features.log')


def parse_arguments() -> tuple:
    """
    Parses commandline arguments
    :return: (script arguments, behave specific arguments) tuple
    """
    parser = argparse.ArgumentParser('Run python behave test scenarios in parallel.'
                                     ' Example execution with behave parameters:\n'
                                     '"python behave_parallel.py --suite features/tests/smoke '
                                     '-f allure_behave.formatter:AllureFormatter -o test-results"'
                                     )
    parser.add_argument('--suite', '-s',
                        help='Please specify the suite(directory with feature files) you want to run. '
                             'Default directory is "features"', default='features'
                        )
    parser.add_argument('--processes', '-p', type=int, help='Maximum number of processes. Default = 4', default=4)
    parser.add_argument('--tags', '-t', action='append', help='Please specify behave tags to run')
    return parser.parse_known_args()


def execute_parallel_feature(feature, behave_args):
    """
    Runs features in parallel
    :param feature: feature to run
    :param behave_args: behave parameters with respective values
    :type feature: str
    """
    feature_start_time = datetime.now()
    start_timer = timer()
    cmd = f'behave {feature} {" ".join(behave_args)}'
    r = call(cmd, shell=True)
    status = 'Passed' if r == 0 else 'Failed'
    logging.info('{0:50}: {1}!!'.format(feature, status))
    feature_end_time = datetime.now()
    end_timer = timer()
    logger.info(f'{feature.split("/")[-1].split(".")[0]};'
                f'{feature_start_time};'
                f'{feature_end_time};'
                f'{end_timer - start_timer};'
                f'{status}')

    return status


def main():
    """
    Parallel Behave Runner
    """
    args, behave_args = parse_arguments()

    if args.tags:
        parsed_tags = ["--tags " + tag for tag in args.tags]
        cmd = f'behave {args.suite} {" ".join(parsed_tags)} -d -k -f json --no-summary'
        behave_args = parsed_tags + behave_args
    else:
        cmd = f'behave {args.suite} -d -k -f json --no-summary'

    parsed_output = dry_run_parsed_cmd(cmd)
    if not parsed_output:
        sys.exit(f'No json output from executed behave dry run command. Command: {cmd}\nNothing to execute')

    features = list({feature['location'].split(':')[0]
                     for feature in parsed_output
                     })

    pool = Pool(args.processes) if len(features) >= args.processes else Pool(len(features))

    logging.info(f'features to execute in parallel: {features}')
    results = pool.map(partial(execute_parallel_feature, behave_args=behave_args), features)

    # set exit status to 1 in case at least one feature failed
    any_feature_failed = 'Failed' in results
    if any_feature_failed:
        sys.exit(1)
    else:
        sys.exit(0)


def dry_run_parsed_cmd(cmd: str) -> str:
    """
    Execute command and return it's stdout as string
    :param cmd: bash command as str
    :return: stdout from command execution
    """
    p = Popen(cmd, stdout=PIPE, shell=True)
    out, err = p.communicate()

    return json.loads(out.decode())


if __name__ == '__main__':
    main()
