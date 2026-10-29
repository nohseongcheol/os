#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
int __posix_library_test(void);

int main(void)
{
    char memoria_intermedia_di_trasferimento_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int descrittore_del_file = Apri("/USER2", O_RDONLY);
    struct stat st;
    if (descrittore_del_file < 0 || fstat(descrittore_del_file, &st) < 0 || Lettura(descrittore_del_file, memoria_intermedia_di_trasferimento_2, 4) != 4 ||
        (unsigned char)memoria_intermedia_di_trasferimento_2[0] != 0x7f || memoria_intermedia_di_trasferimento_2[1] != 'E' || memoria_intermedia_di_trasferimento_2[2] != 'L' || memoria_intermedia_di_trasferimento_2[3] != 'F' ||
        lseek(descrittore_del_file, 0, SEEK_SET) != 0 || Chiudi(descrittore_del_file) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Lettura(-1, memoria_intermedia_di_trasferimento_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Scrittura(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Scrittura(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
