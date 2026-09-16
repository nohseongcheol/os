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
    struct utsname відомості_про_систему;
    int дескриптор_файла = Відкрити("/USER1", O_RDONLY);
    int copy = дескриптор_файла >= 0 ? dup(дескриптор_файла) : -1;
    if (copy >= 0) Закрити(copy);
    if (дескриптор_файла >= 0) {
        fstat(дескриптор_файла, &st);
        lseek(дескриптор_файла, 0, SEEK_SET);
        Закрити(дескриптор_файла);
    }
    stat("/", &st);
    uname(&відомості_про_систему);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
