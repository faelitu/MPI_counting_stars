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

if rank == 0:
    print('\nStarting to manipulate image...')
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
    print('Image binarized')
    
    # Size of the image in pixels (size of original image)
    height = len(im_bin)
    width = len(im_bin[0])

    # Divide image in 100 tiles and send tiles as soon as they are built
    num = 10
    tile_height = height//num
    tile_width = width//num
    print('Cropping image...')
    tile_id = 0
    for tile_i in range(0, num):
        for tile_j in range(0, num):
            tile = []
            for i in range(tile_i * tile_height, tile_i * tile_height + tile_height):
                row = []
                for j in range(tile_j * tile_width, tile_j * tile_width + tile_width):
                    row.append(im_bin[i][j])
                assert len(row) == tile_width
                tile.append(row)
                im_bin[i][j] = 0 # to free memory
            assert len(tile) == tile_height

            print('Tile cropped')
            
            # Send tile size to slave process
            comm.send(len(tile), dest=1, tag=0)
            comm.send(len(tile[0]), dest=1, tag=1)
            # Send tile to slave process
            data = [tile_id, tile]
            comm.send(data, dest=1, tag=2)

            im_bin[i] = 0 # to free memory
            tile_id += 1
            break
        break
    del im_bin # to free memory
elif rank == 1:
    numDataY = comm.recv(source=0, tag=0)
    numDataX = comm.recv(source=0, tag=1)
    data = comm.recv(source=0, tag=2)
    print('\nProcess', rank, 'received Tile', data[0], ' with dimension', numDataY, 'x', numDataX, 'from master process\n')

MPI.Finalize()