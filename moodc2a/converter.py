# author:   bateman
# date:     nov. 13, 2015
# version:  0.1

import csv
import argparse
import string


class Csv2Aiken:
    """
    CSV (input) file must be formatted as follows:

        Question;Answer;Index;Correct
        What is the correct answer to this question?;Is it this one;A;
        ;Maybe this answer;B;
        ;Possibly this one;C;OK

        ...

    Aiken (output) file will look like these:

        What is the correct answer to this question?
        A. Is it this one
        B. Maybe this answer
        C. Possibly this one
        ANSWER: C

        ...
    """

    _ANSWER = 'ANSWER:'
    _INDEX_SEP = '.'
    _INDEX_DICT = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}

    def __init__(self):
        pass

    def convert(self, infile, outfile):
        _out = open(outfile, mode='wb')
        with open(infile, mode='rb') as _in:
            csvreader = csv.DictReader(_in, dialect='excel', delimiter=';')
            i = 0
            for row in csvreader:
                i += 1
                _question = '{0}\n'.format(row['Question'])
                if _question != '\n':
                    _out.write(_question)
                _out.write('{0}{1} {2}\n'.format(row['Index'], self._INDEX_SEP, row['Answer']))
                if string.lower(row['Correct']) == 'ok':
                    _solution = self._INDEX_DICT[str(i)]
                if i == 3:
                    _out.write('{0} {1}\n\n'.format(self._ANSWER, _solution))
                    i = 0
        _in.close()
        _out.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Acquire input CSV and output AIKEN files.')
    parser.add_argument('-i', type=str, nargs=1, action='store', dest='_in', help='CSV input file to convert')
    parser.add_argument('-o', type=str, nargs=1, action='store', dest='_out', help='AIKEN converted output file')

    args = parser.parse_args()
    c2a = Csv2Aiken()
    c2a.convert(infile=args._in[0], outfile=args._out[0])


