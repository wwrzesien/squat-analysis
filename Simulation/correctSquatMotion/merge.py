import csv
import logging
import sys
import os
import re

###################################
# merge.py is a program that will create final motion file from mot file generated in OpenSim.
# Steps:
#   1. Generate .mot file for each pose.
#   2. Run merge.py.
#   3. Open output file in Excel and add second part of motion.
#   4. Save file with .mot extension.
#
# Input: merge.py <fileDirectory> <outputCsv.csv>
#   fileDirectory - directory which contains .mot files (required)
#   outputCsv.csv - output motion file (required)
# Output:
#   motionMerge.log - log file with debugging information

# Human/natural sorting
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',text) ]

def main():

    # Logging setup
    format = '%(message)s'
    logging.basicConfig(level=logging.DEBUG, filename='motionMerge.log', format=format)

    files = []
    output =[]
    path = sys.argv[1]
    outputCsv = sys.argv[2]

    # Read .mot files from directory
    if not os.listdir(path):
        print('Empty directory.')
    else:
        for filename in os.listdir(path):
            if os.path.isfile(filename) and filename.endswith(".mot") and not filename in files:
                files.append(filename)

    # Sort files
    files.sort(key=natural_keys)

    logging.debug('Start merge:')

    for file in files:
        with open(file) as motFile:
            repChar = ['\t','\r','\n']

            lineH = []
            lineC = []
            lineD = []

            # Head
            for n in range(6):
                head = motFile.readline()
                for char in repChar:
                    head = head.replace(char, '')
                lineH.append([head])
            # Check number of rows
            logging.debug('{file}: Number of headers rows: {rowH}, expected: 6'.format(file=file, rowH=len(lineH)))
            if len(lineH) == 6:
                logging.debug('{file}: {part} processed.'.format(file=file, part='Header'))
                if file == files[0]:
                    for line in lineH:
                        output.append(line)
            else:
                logging.debug('{file}: {part} error'.format(file=file, part='Header'))
                return

            # Column
            column = motFile.readline()
            lineC = column.split('\t')
            for char in repChar:
                lineC[-1] = lineC[-1].replace(char, '')
            # Check number of rows
            logging.debug('{file}: Number of columns: {rowC}, expected: 213'.format(file=file, rowC=len(lineC)))
            if len(lineC) == 213:
                logging.debug('{file}: {part} processed.'.format(file=file, part='Columns'))
                if file == files[0]:
                    output.append(lineC)
            else:
                logging.debug('{file}: {part} error'.format(file=file, part='Columns'))
                return

            # First row
            data = motFile.readline()
            lineD = data.split('\t')
            for char in repChar:
                lineD[-1] = lineD[-1].replace(char, '')
            # Check number of rows
            logging.debug('{file}: Number of data: {rowD}, expected: 213'.format(file=file, rowD=len(lineD)))
            if len(lineD) == 213:
                logging.debug('{file}: {part} processed.'.format(file=file, part='Data'))
                output.append(lineD)
            else:
                logging.debug('{file}: {part} error'.format(file=file, part='Data'))
                return

    logging.debug('Merge finished.')

    # Write to csv
    with open(outputCsv, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        for row in output:
            writer.writerow(row)

if __name__ == "__main__":
    main()