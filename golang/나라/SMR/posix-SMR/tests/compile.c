/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/wait.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct stat st;
    struct utsname identità_del_sistema;
    int descrittore_del_file = Apri("/USER1", O_RDONLY);
    int copy = descrittore_del_file >= 0 ? dup(descrittore_del_file) : -1;
    if (copy >= 0) Chiudi(copy);
    if (descrittore_del_file >= 0) {
        fstat(descrittore_del_file, &st);
        lseek(descrittore_del_file, 0, SEEK_SET);
        Chiudi(descrittore_del_file);
    }
    stat("/", &st);
    uname(&identità_del_sistema);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
