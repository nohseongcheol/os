/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>
int __posix_library_test(void);

int main(void)
{
    char siirtopuskuri_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int tiedostokuvaaja = Avaa("/USER2", O_RDONLY);
    struct stat st;
    if (tiedostokuvaaja < 0 || fstat(tiedostokuvaaja, &st) < 0 || Luku(tiedostokuvaaja, siirtopuskuri_2, 4) != 4 ||
        (unsigned char)siirtopuskuri_2[0] != 0x7f || siirtopuskuri_2[1] != 'E' || siirtopuskuri_2[2] != 'L' || siirtopuskuri_2[3] != 'F' ||
        lseek(tiedostokuvaaja, 0, SEEK_SET) != 0 || Sulje(tiedostokuvaaja) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Luku(-1, siirtopuskuri_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Kirjoitus(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Kirjoitus(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
