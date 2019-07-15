#include <stdio.h>
#include <mpi.h>

int main (int argc, char* argv[])
{
    int rank, size, error, i;
    double result=0.0, begin=0.0, end=0.0;
	double fi=0.0;
    const int N = 1000000000;
    const double a=5;
    double b=a;
    error=MPI_Init (&argc, &argv);

    //Get process ID
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);

    //Get processes Number
    MPI_Comm_size (MPI_COMM_WORLD, &size);

    //Synchronize all processes and get the begin time
    MPI_Barrier(MPI_COMM_WORLD);
    begin = MPI_Wtime();

    //Each process will caculate a part of the sum
	for (i = rank; i < N; i+=size) {
		b = (b+a/b)/2;
	}
	fi=(1+b)/2;

    //Sum up all results
    MPI_Reduce(&fi, &result, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    //Synchronize all processes and get the end time
    MPI_Barrier(MPI_COMM_WORLD);
    end = MPI_Wtime();

    //Caculate and print PI
    if (rank==0)
    {
		printf("Fi=%.10lf Time=%fs\n", result, end-begin);
    }

    error=MPI_Finalize();

    return 0;
}
