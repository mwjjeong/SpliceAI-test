#!/extdata6/Doyeon/anaconda3/envs/minu-py2/bin/python2
###############################################################################
'''This parser takes as input the .h5 file produced by create_datafile.py and
outputs a .h5 file with datapoints of the form (X, Y), which can be understood
by Keras models.'''
###############################################################################

import h5py
import numpy as np
import sys
import time
from utils import *
from constants import *

start_time = time.time()

# assert sys.argv[1] in ['train', 'test', 'all']
# assert sys.argv[2] in ['0', '1', 'all']

infile_path = sys.argv[1]  # from create_datafile.py
outfile_path = sys.argv[2]

h5f = h5py.File(infile_path, 'r')

SEQ = h5f['SEQ'][:]
STRAND = h5f['STRAND'][:]
TX_START = h5f['TX_START'][:]
TX_END = h5f['TX_END'][:]
JN_START = h5f['JN_START'][:]
JN_END = h5f['JN_END'][:]
h5f.close()

h5f2 = h5py.File(outfile_path, 'w')

CHUNK_SIZE = 100
CHUNK_NUM = SEQ.shape[0] // CHUNK_SIZE + 1

for i in range(CHUNK_NUM):
    # Each dataset has CHUNK_SIZE genes
    
    if (i+1) == CHUNK_NUM:
        NEW_CHUNK_SIZE = SEQ.shape[0] % CHUNK_SIZE
    else:
        NEW_CHUNK_SIZE = CHUNK_SIZE

    X_batch = []
    Y_batch = [[] for t in range(1)]

    for j in range(NEW_CHUNK_SIZE):

        idx = i*CHUNK_SIZE + j

        X, Y = create_datapoints(SEQ[idx], STRAND[idx],
                                 TX_START[idx], TX_END[idx],
                                 JN_START[idx], JN_END[idx])

        X_batch.extend(X)
        for t in range(1):
            Y_batch[t].extend(Y[t])

    X_batch = np.asarray(X_batch).astype('int8')
    for t in range(1):
        Y_batch[t] = np.asarray(Y_batch[t]).astype('int8')

    h5f2.create_dataset('X' + str(i), data=X_batch)
    h5f2.create_dataset('Y' + str(i), data=Y_batch)

h5f2.close()

print "--- %s seconds ---" % (time.time() - start_time)

###############################################################################         
