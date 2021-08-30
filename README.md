# MPI_counting_stars

## Install dependencies

`sudo apt-get install lam-runtime`

`sudo apt install lam4-dev`

`python -m pip install mpi4py`

`python -m pip install image_slicer`

## Start the LAM/MPI runtime environment

`lamboot`

## Run project

Change the number 4 to the number of processes desired

`mpirun -np 4 python main.py`
