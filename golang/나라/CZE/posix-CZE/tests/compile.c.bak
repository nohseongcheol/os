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
    struct utsname identita_systému;
    int deskriptor_souboru = Otevřít("/USER1", O_RDONLY);
    int copy = deskriptor_souboru >= 0 ? dup(deskriptor_souboru) : -1;
    if (copy >= 0) Zavřít(copy);
    if (deskriptor_souboru >= 0) {
        fstat(deskriptor_souboru, &st);
        lseek(deskriptor_souboru, 0, SEEK_SET);
        Zavřít(deskriptor_souboru);
    }
    stat("/", &st);
    uname(&identita_systému);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
