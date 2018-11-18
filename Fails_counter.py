import glob
import csv
from collections import Counter
import os


def check_fail_folders(path: str, test: str) -> dict:
    """test must be in this format: '\Smoke*'
    the cycle is looking for Fail folders and for SmokeTestSummary*.csv file
    """
    tests_failed = []  # list of all failed tests
    for f in glob.glob(path+'\*Fail*'+test):
        with open(f) as fi:
            reader = csv.reader(fi)  # reads the file as comma separated values in line
            for line in reader:  # the cycle is looking for line with test status failed
                if 'Fail' in line:
                    tests_failed.append(line[0])  # if exists - adds number (only) of test to the "tests_failed" list
    return dict(Counter(tests_failed))


st_folder = os.path.expanduser(r'~\Desktop\RovalSimplifier\SmokeTestAutomation\Output\SmokeTestSummary')

result = check_fail_folders(st_folder, '\Smoke*')
folders_total = len(next(os.walk(st_folder))[1])  # to add exception for an empty folder
folders_for_file = ['Total folders:', folders_total]

with open('Result.csv', mode='w', newline='') as file:
    file_writer = csv.writer(file, delimiter=',')
    file_writer.writerow(folders_for_file)
    for k, v in result.items():
        temp = [k, v]
        file_writer.writerow(temp)

print(folders_for_file)
print(result)
print('Done')
