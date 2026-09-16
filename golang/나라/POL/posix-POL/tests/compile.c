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
    struct utsname tożsamość_systemu;
    int deskryptor_pliku = Otwórz("/USER1", O_RDONLY);
    int copy = deskryptor_pliku >= 0 ? dup(deskryptor_pliku) : -1;
    if (copy >= 0) Zamknij(copy);
    if (deskryptor_pliku >= 0) {
        fstat(deskryptor_pliku, &st);
        lseek(deskryptor_pliku, 0, SEEK_SET);
        Zamknij(deskryptor_pliku);
    }
    stat("/", &st);
    uname(&tożsamość_systemu);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
