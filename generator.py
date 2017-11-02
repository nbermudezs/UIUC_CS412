import pdb
import random

if __name__ == '__main__':
    with open('new-data2.txt', 'w') as f:
        f.write('0.2, 0.5\n')
        for _ in range(1500):
            count = round(random.random() * 10) + 10
            items = [ str(round(random.random() * 10)) for _ in range(count) ]
            f.write(', '.join(items))
            f.write('\n')
