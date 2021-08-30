# MPI_counting_stars

## Install dependencies

`sudo apt-get install lam-runtime`
`sudo apt install lam4-dev`

## Start the LAM/MPI runtime environment

`lamboot`

## Compile project

`mpicc main.c -o main`

## Run project

Change the number 4 to the number of processes desired

`mpirun -np 4 ./main`
