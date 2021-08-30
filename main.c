#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);

    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    //Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    //GET the NAME of the process
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    // Print off a hello world message
    printf("Hello world from processor %s, rank %d out of %d processors\n",
                processor_name, world_rank, world_size);

    int number, i;
    number = world_rank;

    if (world_rank == 0) {
        sleep(1);
        printf("All processes are waiting\n");
        for (i = 1; i < world_size; i++){
            MPI_Recv(&number, 1, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            printf("All processes are sincronized\n");   
        }
    }
    else {
        MPI_Ssend(&number, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        printf("Process %d sended message to process 0\n", world_rank);
    }

    //Finalize the MPI environment
    MPI_Finalize();
}