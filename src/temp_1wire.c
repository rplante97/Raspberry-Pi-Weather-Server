#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <fcntl.h>

#define SENSOR_NAME "/sys/bus/w1/devices/28-000006b56307/w1_slave"

static double read_temp(char *filename) {
	
	double result=0.0;
	int fd;
	char buffer[256];
	char *s;
	char temp[6];
	int tempstart;
	int temp_int;

	//open our temp sensor connection
	fd = open(SENSOR_NAME, O_RDONLY);
	if(fd<0){
		printf("Error in sensor file open\n");
		exit(1);
		}
	//read the output into our buffer
	read(fd, buffer, 256);
	if(fd<0){
		printf("Error in sensor file read\n");
		exit(1);
		}
		
		//find YES
		s = strstr(buffer, "YES"); //Search for string "YES" in our buffer
		if (s != NULL){ //if successful s now points to begginning of our string
											//printf("Found YES at index %d\n", s - buffer);
			}
		else{
			printf("Error, YES not found\n");
			exit(1);
			}
		
		//find t=	
		s = strstr(buffer, "t="); //Search for string "t=" in our buffer
		if (s != NULL){ //if successful s now points to beginning of our string
											//printf("Found t= at index %d\n", s - buffer);
			}
		else{
			printf("Error, t= not found\n");
			exit(1);
		}
		
		//read the temp value into a seperate buffer
		int i;
		tempstart = (s-buffer)+2;
		for(i = 0; i<5; i++){
			temp[i] = buffer[tempstart + i];
			}
			temp[5] = '\0';
										//printf("%s\n", temp);
			
			//convert our temp into an integer then a float
			temp_int = atoi(temp);
			result = temp_int/1000.0;
			
			
	

	return result;
}

int main(int argc, char **argv) {
	double temp1;

		temp1=read_temp(SENSOR_NAME);
		printf("%.2lf\n",temp1);
		sleep(1);
		return 0;
		
}
