#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
int __posix_library_test(void);

int main(void)
{
    char overdrachtsbuffer_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int bestandsdescriptor = Openen("/USER2", O_RDONLY);
    struct stat st;
    if (bestandsdescriptor < 0 || fstat(bestandsdescriptor, &st) < 0 || Lezen(bestandsdescriptor, overdrachtsbuffer_2, 4) != 4 ||
        (unsigned char)overdrachtsbuffer_2[0] != 0x7f || overdrachtsbuffer_2[1] != 'E' || overdrachtsbuffer_2[2] != 'L' || overdrachtsbuffer_2[3] != 'F' ||
        lseek(bestandsdescriptor, 0, SEEK_SET) != 0 || Sluiten(bestandsdescriptor) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Lezen(-1, overdrachtsbuffer_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Schrijven(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Schrijven(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
