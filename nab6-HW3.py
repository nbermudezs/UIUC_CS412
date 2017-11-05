from OutlierFP import OutlierFP
import sys, time

if __name__ == '__main__':
    start = time.clock()
    input_filepath = 'data.txt'
    output_filepath = 'nab6-HW3.txt'

    if len(sys.argv) < 3:
        print('Usage: python3.6 ./nab6-HW3.py <input_filepath> <output_filepath>')
        print('Continuing with defaults: input = data.txt, output = nab6-HW3.txt')
    else:
        input_filepath = sys.argv[ 1 ]
        output_filepath = sys.argv[ 2 ]

    miner = OutlierFP()
    miner.mine(input_filepath, output_filepath)

    elapsed = time.clock() - start
    print('Took ' + str(round(elapsed * 1000, 3)) + ' milliseconds to complete')
