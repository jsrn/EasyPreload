#include <stdio.h> 
main() 
{ 
	int euid = geteuid();
	printf("Effective user id: %d\n",euid);
}

