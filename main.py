import time
import numpy as np
from mpi4py import MPI

from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import image_slicer

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world_size = MPI.UNIVERSE_SIZE
name = MPI.Get_processor_name()
print('Hello world from processor', name, ', my rank is', rank, 'out of', world_size)

comm.Barrier()

# if rank == 0:
#     print('All processes are waiting')
#     for i in range(1, world_size):
#         data = np.empty(1, dtype='i')
#         comm.Send([data, MPI.INT], source=i, tag=77)
#     print('All processes are sincronized')
# else:
#     data = np.arange(1, dtype='i')
#     data[0] = rank
#     comm.Ssend([data, MPI.INT], dest=0, tag=77)
#     print('Process', rank, 'sent message', data, 'to process 0')

# amode = MPI.MODE_WRONLY|MPI.MODE_CREATE
# fh = MPI.File.Open(comm, "./images/1.png", amode)

# item_count = 10

# buffer = np.empty(item_count, dtype='i')
# buffer[:] = rank

# filetype = MPI.INT.Create_vector(item_count, 1, world_size)
# filetype.Commit()

# displacement = MPI.INT.Get_size()*rank
# fh.Set_view(displacement, filetype=filetype)

# fh.Write_all(buffer)
# filetype.Free()
# fh.Close()

if rank == 0:
    tiles = image_slicer.slice('images/2.png', 14, save=False)
    data = [tiles[i] for i in range(world_size)]
else:
    data = None

data = comm.scatter(data, root=0)
# assert data == rank
print('Process', rank, 'received message', data, 'from process 0')

MPI.Finalize()