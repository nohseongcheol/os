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
    struct utsname systemidentitet;
    int filbeskrivare = Öppna("/USER1", O_RDONLY);
    int copy = filbeskrivare >= 0 ? dup(filbeskrivare) : -1;
    if (copy >= 0) Stäng(copy);
    if (filbeskrivare >= 0) {
        fstat(filbeskrivare, &st);
        lseek(filbeskrivare, 0, SEEK_SET);
        Stäng(filbeskrivare);
    }
    stat("/", &st);
    uname(&systemidentitet);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
