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
    struct utsname identitas_sistem;
    int deskriptor_berkas = Buka("/USER1", O_RDONLY);
    int copy = deskriptor_berkas >= 0 ? dup(deskriptor_berkas) : -1;
    if (copy >= 0) Tutup(copy);
    if (deskriptor_berkas >= 0) {
        fstat(deskriptor_berkas, &st);
        lseek(deskriptor_berkas, 0, SEEK_SET);
        Tutup(deskriptor_berkas);
    }
    stat("/", &st);
    uname(&identitas_sistem);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
