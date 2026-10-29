#define _POSIX_C_SOURCE 200809L
#include "/opt/worldos/posix.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/mman.h>
static void *work(void *value) { return value; }
int main(void) {
    int fd = open("/home/user/workspace/posix.txt", O_CREAT|O_RDWR|O_TRUNC, 0600);
    if (fd < 0 || write(fd,"POSIX",5)!=5 || fsync(fd) || lseek(fd,0,SEEK_SET)<0) return 1;
    char data[6]={0}; if (read(fd,data,5)!=5 || strcmp(data,"POSIX")) return 2;
    close(fd); pthread_t thread; void *answer;
    if (pthread_create(&thread,NULL,work,(void*)42) || pthread_join(thread,&answer) || answer!=(void*)42) return 3;
    int pair[2]; if(socketpair(AF_UNIX,SOCK_STREAM,0,pair))return 4;
    if(write(pair[0],"x",1)!=1 || read(pair[1],data,1)!=1 || data[0]!='x')return 5;
    close(pair[0]);close(pair[1]);
    pid_t child=fork();if(child<0)return 6;if(!child)_exit(17);
    int status;if(waitpid(child,&status,0)!=child || !WIFEXITED(status) || WEXITSTATUS(status)!=17)return 7;
    puts("PASS native-posix-file-pthread-unix-socket-fork-wait");return 0;
}
