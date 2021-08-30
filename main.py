import time
import numpy as np
from mpi4py import MPI
from mpi4py.util import dtlib

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world_size = MPI.UNIVERSE_SIZE
name = MPI.Get_processor_name()
print('Hello world from processor', name, ', my rank is', rank, 'out of', world_size)

if rank == 0:
    time.sleep(1)
    print('All processes are waiting')
    for i in range(1, world_size):
        data = np.empty(1, dtype='i')
        comm.Irecv([data, MPI.INT], source=i, tag=77)
    print('All processes are sincronized')
else:
    data = np.arange(1, dtype='i')
    data[0] = rank
    comm.Ssend([data, MPI.INT], dest=0, tag=77)
    print('Process', rank, 'sended message', data, 'to process 0')