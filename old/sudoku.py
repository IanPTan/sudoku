import numpy as np
from time import time

def chop(puzzle, x, y, s = 3):
    return puzzle[y * s: (y + 1) * s, x * s: (x + 1) * s]

def dif(x, y):
    return x.difference(y)
dif = np.vectorize(dif)

def readPuzzle(dir):
    rawdat = open(dir, 'r')
    dat = rawdat.read()
    rawdat.close()
    dat = dat.split('\n')[:-1]
    pzl = np.full([len(dat), len(dat[0])], None, dtype = object)
    for y in range(len(dat)):
        for x in range(len(dat[0])):
            try:
                pzl[y, x] = set([int(dat[y][x])])
            except:
                pzl[y, x] = set(range(1, 10))
    return pzl
    
def eliminate(pzl, x, y, s = 3):
    c = pzl[y, x]
    pzl[y // s * s: (y // s + 1) * s, x // s * s: (x // s + 1) * s] = dif(pzl[y // s * s: (y // s + 1) * s, x // s * s: (x // s + 1) * s], c)
    pzl[y, :] = dif(pzl[y, :], c)
    pzl[:, x] = dif(pzl[:, x], c)
    # pzl[y, x] = c

def elim1(pzl, sol, s = 3):
    for y in range(len(pzl)):
        for x in range(len(pzl[y])):
            if len(pzl[y, x]) == 1:
                sol[y, x] = list(iter(pzl[y, x]))[0]
                eliminate(pzl, x, y, s)

def disprob(pzl):
    for y in range(3):
        print(f'{len(pzl[y * 3, 0])} {len(pzl[y * 3, 1])} {len(pzl[y * 3, 2])}|{len(pzl[y * 3, 3])} {len(pzl[y * 3, 4])} {len(pzl[y * 3, 5])}|{len(pzl[y * 3, 6])} {len(pzl[y * 3, 7])} {len(pzl[y * 3, 8])}\n{len(pzl[y * 3 + 1, 0])} {len(pzl[y * 3 + 1, 1])} {len(pzl[y * 3 + 1, 2])}|{len(pzl[y * 3 + 1, 3])} {len(pzl[y * 3 + 1, 4])} {len(pzl[y * 3 + 1, 5])}|{len(pzl[y * 3 + 1, 6])} {len(pzl[y * 3 + 1, 7])} {len(pzl[y * 3 + 1, 8])}\n{len(pzl[y * 3 + 2, 0])} {len(pzl[y * 3 + 2, 1])} {len(pzl[y * 3 + 2, 2])}|{len(pzl[y * 3 + 2, 3])} {len(pzl[y * 3 + 2, 4])} {len(pzl[y * 3 + 2, 5])}|{len(pzl[y * 3 + 2, 6])} {len(pzl[y * 3 + 2, 7])} {len(pzl[y * 3 + 2, 8])}')
        if y != 2:
            print('-----|-----|-----')

def dissol(pzl):
    for y in range(3):
        print(f'{pzl[y * 3, 0]} {pzl[y * 3, 1]} {pzl[y * 3, 2]}|{pzl[y * 3, 3]} {pzl[y * 3, 4]} {pzl[y * 3, 5]}|{pzl[y * 3, 6]} {pzl[y * 3, 7]} {pzl[y * 3, 8]}\n{pzl[y * 3 + 1, 0]} {pzl[y * 3 + 1, 1]} {pzl[y * 3 + 1, 2]}|{pzl[y * 3 + 1, 3]} {pzl[y * 3 + 1, 4]} {pzl[y * 3 + 1, 5]}|{pzl[y * 3 + 1, 6]} {pzl[y * 3 + 1, 7]} {pzl[y * 3 + 1, 8]}\n{pzl[y * 3 + 2, 0]} {pzl[y * 3 + 2, 1]} {pzl[y * 3 + 2, 2]}|{pzl[y * 3 + 2, 3]} {pzl[y * 3 + 2, 4]} {pzl[y * 3 + 2, 5]}|{pzl[y * 3 + 2, 6]} {pzl[y * 3 + 2, 7]} {pzl[y * 3 + 2, 8]}')
        if y != 2:
            print('-----|-----|-----')

def solve(pzl, sol):
    elim1(pzl, sol)
    print('\npuzzle:\n')
    dissol(sol)
    while np.prod(sol) == 0:
        elim1(pzl, sol)

sol = np.zeros([9, 9], dtype = int)

pzl = readPuzzle(input('Puzzle dir: '))

start = time()
solve(pzl, sol)
duration = time() - start


print(f'\nsolution in {duration} seconds:\n')
dissol(sol)
