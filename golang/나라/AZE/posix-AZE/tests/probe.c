#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
int __posix_library_test(void);

int main(void)
{
    char buffer[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int fd = Aç("/USER2", O_RDONLY);
    struct stat st;
    if (fd < 0 || fstat(fd, &st) < 0 || Oxuma(fd, buffer, 4) != 4 ||
        (unsigned char)buffer[0] != 0x7f || buffer[1] != 'E' || buffer[2] != 'L' || buffer[3] != 'F' ||
        lseek(fd, 0, SEEK_SET) != 0 || Bağla(fd) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Oxuma(-1, buffer, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Yazma(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Yazma(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
