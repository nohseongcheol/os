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
    struct utsname järjestelmätiedot;
    int tiedostokuvaaja = Avaa("/USER1", O_RDONLY);
    int copy = tiedostokuvaaja >= 0 ? dup(tiedostokuvaaja) : -1;
    if (copy >= 0) Sulje(copy);
    if (tiedostokuvaaja >= 0) {
        fstat(tiedostokuvaaja, &st);
        lseek(tiedostokuvaaja, 0, SEEK_SET);
        Sulje(tiedostokuvaaja);
    }
    stat("/", &st);
    uname(&järjestelmätiedot);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
