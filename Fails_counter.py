import glob
import csv
from collections import Counter
import os

path = os.path.expanduser(r'~\Desktop\RovalSimplifier\SmokeTestAutomation\Output\SmokeTestSummary')
tests_failed = []  # list of all failed tests

# in the "SmokeTestSummary_HCarmel_Fail-2018-10-17-15-02-45" folder there are 3 files:
# - Dfl_AlternativeFw_App_Fail-2018-10-17-15-07-08.txt
# - Dfl_AlternativeFw_Cmd_Fail-2018-10-17-15-07-08.txt
# - and SmokeTestSummary_HCarmel_Fail-2018-10-17-15-07-08.csv
for f in glob.glob(path+'\*Fail*\Smoke*'):  # the cycle is looking for Fail folders and for SmokeSummary file
    with open(f) as file:
        reader = csv.reader(file)  # reads the file as comma separated values in line
        for line in reader:  # the cycle is looking for line with test status failed
            if 'Fail' in line:
                tests_failed.append(line[0])  # if exists - adds number (only) of test to the "tests_failed" list


result = dict(Counter(tests_failed))
folders_total = len(next(os.walk(path))[1])  # to add exception for an empty folder
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




