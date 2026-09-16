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
    char överföringsbuffert_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int filbeskrivare = Öppna("/USER2", O_RDONLY);
    struct stat st;
    if (filbeskrivare < 0 || fstat(filbeskrivare, &st) < 0 || Läs(filbeskrivare, överföringsbuffert_2, 4) != 4 ||
        (unsigned char)överföringsbuffert_2[0] != 0x7f || överföringsbuffert_2[1] != 'E' || överföringsbuffert_2[2] != 'L' || överföringsbuffert_2[3] != 'F' ||
        lseek(filbeskrivare, 0, SEEK_SET) != 0 || Stäng(filbeskrivare) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Läs(-1, överföringsbuffert_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Skriv(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Skriv(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
