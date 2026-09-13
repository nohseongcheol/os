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
    struct utsname name;
    int fd = Åbn("/USER1", O_RDONLY);
    int copy = fd >= 0 ? dup(fd) : -1;
    if (copy >= 0) Luk(copy);
    if (fd >= 0) {
        fstat(fd, &st);
        lseek(fd, 0, SEEK_SET);
        Luk(fd);
    }
    stat("/", &st);
    uname(&name);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
