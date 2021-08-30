import time
import numpy as np
from mpi4py import MPI

from PIL import Image
Image.MAX_IMAGE_PIXELS = None

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
    print('Starting to manipulate image...')
    # Opens a image in RGB mode
    im = Image.open('images/2.png')
    print('Image opened')

    print('Binarizing image...')
    # Convert to grayscale
    im_gray = np.array(im.convert('L'))
    del im

    # Binarizing image:
    thresh = 128
    im_bool = (im_gray > thresh)
    del im_gray

    maxval = 255
    im_bin = im_bool * maxval
    del im_bool
    # Image.fromarray(np.uint8(im_bin)).save('test.png')
    print('Image binarized')
    
    # Size of the image in pixels (size of original image)
    height = len(im_bin)
    width = len(im_bin[0])
    
    # Setting the points for cropped image
    # left = 5
    # top = height / 4
    # right = 164
    # bottom = 3 * height / 4
    
    # Cropped image of above dimension
    # (It will not change original image)
    # im1 = im.crop((left, top, right, bottom))

    # Divide image in 100 tiles
    num = 10
    tile_height = height//num
    tile_width = width//num
    tiles = []
    print('Cropping image...')
    for tile in range(0, num * num):
        t = []
        for i in range(tile * tile_height, tile * tile_height + tile_height):
            row = []
            for j in range(tile * tile_width, tile * tile_width + tile_width):
                row.append(im_bin[i][j])
            t.append(row)
        tiles.append(t)
    print('Image cropped')

    data = [tiles[i] for i in range(num * num)]
else:
    data = None

data = comm.scatter(data, root=0)
# assert data == rank
print('Process', rank, 'received message', data, 'from process 0')

MPI.Finalize()