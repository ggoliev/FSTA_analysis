import csv
import glob
import os
from collections import Counter

# adapted for Python 3.4: without type hinting
smoke_test_summary_folder = os.path.expanduser(
    r'~\Desktop\RovalSimplifier\SmokeTestAutomation\Output\SmokeTestSummary')  # TODO to check with OneCoreSmokeTest
fail_test_result_file_name = 'fail_test_result.csv'


def count_fail_tests(path_to_checked_folder: str, file_name_mask: str) -> dict:
    """The function is looking for folders with 'Fail' in name,
    open files by mask and search line with test status 'Fail'
    :param path_to_checked_folder: str. The full path to Summary folder
    :param file_name_mask: str. Must be in this format: '\Smoke*' TODO Leave only test name (Smoke, OneCore, OfflRegr)
    :return: dict. Key - number of test, value - sum of failed tests
    """

    tests_failed = []  # list of all failed tests
    for file_by_mask in glob.glob(path_to_checked_folder+r'\*Fail*'+file_name_mask):
        with open(file_by_mask) as f:
            reader = csv.reader(f)  # reads the file as comma separated values in line
            try:
                for line in reader:  # the cycle is looking for line with test status failed
                    if 'Fail' in line:
                        tests_failed.append(line[0])  # if exists - adds number (only) of test to the "tests_failed" list
            except csv.Error:  # If the file is created not correctly, there is an error 'line contains NULL byte'
                print('One of files contains NULL byte and isn\'t counted')  # Todo May be to add it to report
    dict_with_fails = dict(Counter(tests_failed))
    return dict_with_fails


def count_total_folders(path_to_folder: str) -> list:
    """ Count all (passed, failed, unfinished) folders in SmokeTest (etc) Summary folder    
    :param path_to_folder: string with the path to Summary folder
    :return: list of 'Total folders', number
    """

    try:
        total = len(os.listdir(path_to_folder))
        return ['Total folders', total]
    except StopIteration:
        return ['Total folders', 'empty']


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


fail_test_result: dict = count_fail_tests(smoke_test_summary_folder, r'\Smoke*')
# Intermediate variable with result of function. Just to do help the understanding and visualisation

total_folders_result = count_total_folders(smoke_test_summary_folder)
write_result_file(fail_test_result_file_name, total_folders_result, fail_test_result)


print('Print for debugging only! Done.')
print(total_folders_result)
print(fail_test_result)

