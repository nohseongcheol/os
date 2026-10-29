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
    struct utsname systeemidentiteit;
    int bestandsdescriptor = Openen("/USER1", O_RDONLY);
    int copy = bestandsdescriptor >= 0 ? dup(bestandsdescriptor) : -1;
    if (copy >= 0) Sluiten(copy);
    if (bestandsdescriptor >= 0) {
        fstat(bestandsdescriptor, &st);
        lseek(bestandsdescriptor, 0, SEEK_SET);
        Sluiten(bestandsdescriptor);
    }
    stat("/", &st);
    uname(&systeemidentiteit);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
