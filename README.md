# MPI_counting_stars

## Install dependencies

`sudo apt-get install lam-runtime`

`sudo apt install lam4-dev`

`pip install -r requirements.txt`

## Start the LAM/MPI runtime environment

`lamboot`

## Run project

Change the number 4 to the number of processes desired

`mpirun -np 4 python main.py`
