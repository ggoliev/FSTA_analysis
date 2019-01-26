import csv
import glob
import logging
import os
from collections import Counter


# ToDo To add help (--help)
# ToDo To add config file -https://python-scripts.com/configparser-python-example

format1 = u'%(filename)s'\
          u'[line:%(lineno)d]# '\
          u'%(levelname)-8s '\
          u'[%(asctime)s]  '\
          u'%(message)s'
format2 = '[%(levelname)s]-[%(funcName)s]: %(message)s'

logger = logging.getLogger('FailsCounterLogger')
my_format = format1
# create the handler for the file logger
file_logger = logging.FileHandler('FailedTestsStatistic.log', 'w')  # add filemode="w" to overwrite, without - adding.
file_logger_format = logging.Formatter(my_format)
file_logger.setFormatter(file_logger_format)  # tell the handler to use the above format
logger.addHandler(file_logger)  # finally, add the handler to the base logger
file_logger.setLevel(logging.INFO)

# now we can add the console logging
#my_format2 = format2
console_logger = logging.StreamHandler()
console_logger_format = logging.Formatter(format2)
console_logger.setFormatter(console_logger_format)  # tell the handler to use the new format
logger.addHandler(console_logger)  # Mine version
logger.setLevel(logging.DEBUG)

# adapted for Python 3.4: without type hinting
test_folder: str = r'C:\1Work\Fail\SmokeTestSummary'
smoke_test_summary_folder = os.path.expanduser(
    r'~\Desktop\RovalSimplifier\SmokeTestAutomation\Output\SmokeTestSummary')  # TODO to check with OneCoreSmokeTest
fail_test_result_file_name = 'fail_test_result.csv'

work_folder = test_folder
# This var was added to not change every time arg-s in both total_folders_result and fail_test_result during debugging


def count_total_folders(path_to_folder: str) -> list:
    """ Count all (passed, failed, unfinished) folders in SmokeTest (etc) Summary folder
    :param path_to_folder: string with the path to Summary folder
    :return: list of 'Total folders', number
    """

    try:
        total = len(os.listdir(path_to_folder))
        logger.info('Total quantity of folders in %s is %s\n' % (path_to_folder, total))
        return ['Total folders', total]
    except StopIteration:
        return ['Total folders', 'empty']


def count_fail_tests(path_to_checked_folder: str, file_name_mask: str) -> dict:
    """The function is looking for folders with 'Fail' in name,
    open files by mask and search line with test status 'Fail'
    :param path_to_checked_folder: str. The full path to Summary folder
    :param file_name_mask: str. Must be in this format: '\Smoke*' TODO Leave only test name (Smoke, OneCore, OfflRegr)
    :return: dict. Key - number of test, value - sum of failed tests
    """

    tests_failed: list = []  # list of all failed tests
    # Search folder with "Fail" word, in this folder search file by mask
    list_of_all_failed_files: list = glob.glob(path_to_checked_folder + r'\*Fail*' + file_name_mask)
    logger.info(f'Total files to check {len(list_of_all_failed_files)}')
    for failed_file in list_of_all_failed_files:
        with open(failed_file) as f:
            reader = csv.reader(f)  # reads the file as comma separated values in line
            try:
                for line in reader:  # the cycle is looking for line with test status failed
                    if 'Fail' in line:
                        # if exists - adds number (only) of test (it's [0] position to the "tests_failed" list
                        tests_failed.append(line[0])
                        logger.debug(f'{failed_file} file is checked and added to report.')
            except csv.Error:  # If the file is created not correctly, there is an error 'line contains NULL byte'
                logger.error(f'{failed_file} contains NULL byte and isn\'t counted.\n')  # Todo May be to add it to report
    dict_with_fails = dict(Counter(tests_failed))
    return dict_with_fails


def count_fail_tests_g5(path_to_checked_folder: str, file_name_mask: str) -> dict:
    """The function is looking for folders with 'Fail' in name,
    open files by mask and search line with test status 'Fail'
    :param path_to_checked_folder: str. The full path to Summary folder
    :param file_name_mask: str. Must be in this format: '\Smoke*' TODO Leave only test name (Smoke, OneCore, OfflRegr)
    :return: dict. Key - number of test, value - sum of failed tests
    """

    tests_failed = []  # list of all failed tests
    # Search folder with "Fail" word, in this folder search fil by mask
    for failed_file in glob.glob(path_to_checked_folder + r'\*Fail*' + file_name_mask):
        with open(failed_file) as f:
            reader = csv.reader(f)  # reads the file as comma separated values in line
            logger.debug("%s file is checked.\n" % failed_file)
            try:
                for line in reader:  # the cycle is looking for line with test status failed
                    if 'Failed' in line:
                        # if exists - adds number (only) of test (it's [0] position to the "tests_failed" list
                        tests_failed.append(line[1])
            except csv.Error:  # If the file is created not correctly, there is an error 'line contains NULL byte'
                logger.error('This files contains NULL byte and isn\'t counted.\n')  # Todo May be to add it to report
    dict_with_fails = dict(Counter(tests_failed))
    return dict_with_fails


def write_result_file(file_name: str, total_folders: list, failed_test: dict) -> None:
    """Create csv file with total number of folders in 'Summary' folder, number of failed tests and its quantity
    :param file_name: name of file to create. Predefined in fail_test_result_file_name variable.
    :param total_folders: list. The result of count_total_folders function.
    :param failed_test: dict. The result of count_fail_tests function.
    :return: None. Create csv file in the folder with this script
    """

    with open(file_name, mode='w', newline='') as file:
        file_writer = csv.writer(file, delimiter=',')
        file_writer.writerow(total_folders)
        for k, v in failed_test.items():
            test_number_and_fails = [k, v]
            file_writer.writerow(test_number_and_fails)


logger.debug('Program started')
# ToDo: Argument for total_folders_result and fail_test_result - must be one variable
total_folders_result = count_total_folders(work_folder)
# Intermediate variable with result of function. Just to do help the understanding and visualisation
# fail_test_result: dict = count_fail_tests_g5(test_folder, r'\G5*')
fail_test_result: dict = count_fail_tests(work_folder, r'\SmokeTestSummary*')

write_result_file(fail_test_result_file_name, total_folders_result, fail_test_result)

for key,value in fail_test_result.items():
    logger.info(f'Test number {key} failed  {value} time(s)')
