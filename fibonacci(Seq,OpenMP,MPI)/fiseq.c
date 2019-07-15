#include <stdio.h>
#include <sys/time.h>

void main(void) {
	struct timeval  tv1, tv2;
	double fi,sum = 0.0,execTime;
    const int N = 1000000000;
    const double a=5;
    double b=a;
	int i;
	gettimeofday(&tv1, NULL);
	for (i = 0; i < N; i++) {
		b=(b+a/b)/2;
	}
	fi = (1+b)/2;
	gettimeofday(&tv2, NULL);
	execTime = (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 + (double) (tv2.tv_sec - tv1.tv_sec);
	printf("Fi=%.10lf Time=%lf\n", fi, execTime);
	return;
}
