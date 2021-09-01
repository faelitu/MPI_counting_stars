import time
import numpy as np
from mpi4py import MPI
import queue
import os
import logging
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

import sys, threading
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world_size = MPI.UNIVERSE_SIZE
name = MPI.Get_processor_name()
print('Hello world from the machine', name, ', my rank is', rank, 'out of', world_size, 'and I am', 'the Master!' if rank == 0 else 'a Slave.')

comm.Barrier()

if rank == 0:
    t1 = time.time()
    t1_mpi = MPI.Wtime()
    total_stars = 0
    slaves_queue = queue.Queue()
    slaves_requests = []
    for slave in range(1, world_size):
        slaves_queue.put(slave)
        # Create a non-blocking receiver for each slave with tag 9 (inform if slave gets free and its result)
        slaves_requests.append(comm.irecv(source=slave, tag=9))

    all_images = os.listdir('../counting-stars/pics')
    for im_name in all_images:
        print('\nStarting to manipulate image', im_name, '...')
        # Opens an image in RGB mode
        im = Image.open('../counting-stars/pics/' + im_name)

        print('Image', im_name, 'opened.')
    
        print('Binarizing image', im_name, '...')
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
        print('Image', im_name, 'binarized.')
        
        # Size of the image in pixels (size of original image)
        height = len(im_bin)
        width = len(im_bin[0])
    
        # Divide image in 100 tiles and send tiles as soon as they are built
        num = 100
        tile_height = height//num
        tile_width = width//num
        print('Starting to crop image', im_name, '...')
        tile_id = 1
        for tile_i in range(0, num):
            for tile_j in range(0, num):
                tile = []
                for i in range(tile_i * tile_height, tile_i * tile_height + tile_height):
                    row = []
                    for j in range(tile_j * tile_width, tile_j * tile_width + tile_width):
                        row.append(im_bin[i][j])
                    assert len(row) == tile_width
                    tile.append(row)
                assert len(tile) == tile_height
    
                print('\nTile', tile_id, 'of image', im_name, 'cropped.')
                
                # Get next slave from queue if it is not empty
                if not slaves_queue.empty:
                    next_slave = slaves_queue.get()
                else:
                    # Fill slaves_queue if it is empty
                    for i in range(0, len(slaves_requests)):
                        [status, response] = slaves_requests[i].test()
                        if status:
                            [slave_rank, result] = response
                            print('\n\tI am the Master and I just found out that Slave', slave_rank, 'got free and counted', result,'stars. Putting it in queue...')
                            total_stars += result
                            slaves_queue.put(slave_rank)
                            slaves_requests[i] = comm.irecv(source=i, tag=9) # Resetting the non-blocking receiver
                    next_slave = slaves_queue.get()
                print('\nNext Slave:', next_slave)
                
                # Send tile to slave process
                data = [tile_id, tile]
                print('Sending Tile', tile_id, 'of image', im_name, 'to Slave', next_slave, '...')
                comm.send(data, dest=next_slave, tag=2)
                print('Master sent Tile', tile_id, 'of image', im_name, 'to Slave', next_slave)
    
                tile_id += 1
            break
        del im_bin # to free memory

    # Send final message to all slaves
    for slave in range(1, world_size):
        comm.send([0, 'DONE'], dest=slave, tag=2)
    
    print('\nMaster finished working. Now going to rest.')

else:
    number_of_stars = 0

    def flood_star(i, j, tile):
        tile[i][j] = 128
        if j+1 < len(tile[0]) and tile[i][j+1] and tile[i][j+1] == 255: # pixel right
            flood_star(i, j+1, tile)
        if i+1 < len(tile) and tile[i+1][j] and tile[i+1][j] == 255: # pixel below
            flood_star(i+1, j, tile)
        if j-1 >= 0 and tile[i][j-1] and tile[i][j-1] == 255: # pixel left
            flood_star(i, j-1, tile)

    done = False
    while not done:
        [id, tile] = comm.recv(source=0, tag=2)
        if id != 0:
            print('\nSlave', rank, 'received Tile', id, 'with dimension', len(tile), 'x', len(tile[0]), 'from Master')

            # Count all stars
            for i in range(0, len(tile)):
                for j in range(0, len(tile[0])):
                    if tile[i][j] == 255:
                        flood_star(i, j, tile)
                        number_of_stars += 1

            del tile # to free memory

            # Send rank with tag 9 to warn master that this slave is now free and it result
            print('\n\tI am Slave', rank, 'and I am free! Now waiting...')
            comm.send([rank, number_of_stars], dest=0, tag=9)
        else:
            done = True
            print('\nSlave', rank, 'finished working. Now going to rest.')

comm.Barrier()
if rank == 0:
    # Sums the remaining results
    for i in range(0, len(slaves_requests)):
        [status, response] = slaves_requests[i].test()
        if status:
            [slave_rank, result] = response
            print('\n\tI am the Master and I just found out that Slave', slave_rank, 'counted', result,'stars.')
            total_stars += result
        else:
            # Free the communication request
            slaves_requests[i].cancel() 
    del slaves_requests
    # Show final result
    print('\nFinal result: There are', total_stars,'stars\n')
    t2 = time.time()
    t2_mpi = MPI.Wtime()
    print(f'Total time of execution: {t2-t1}')
    print(f'Total time of execution(MPI): {t2_mpi-t1_mpi}')

MPI.Finalize()