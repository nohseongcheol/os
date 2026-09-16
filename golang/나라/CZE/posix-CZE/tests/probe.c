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
    char vyrovnávací_paměť_přenosu_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int deskriptor_souboru = Otevřít("/USER2", O_RDONLY);
    struct stat st;
    if (deskriptor_souboru < 0 || fstat(deskriptor_souboru, &st) < 0 || Čtení(deskriptor_souboru, vyrovnávací_paměť_přenosu_2, 4) != 4 ||
        (unsigned char)vyrovnávací_paměť_přenosu_2[0] != 0x7f || vyrovnávací_paměť_přenosu_2[1] != 'E' || vyrovnávací_paměť_přenosu_2[2] != 'L' || vyrovnávací_paměť_přenosu_2[3] != 'F' ||
        lseek(deskriptor_souboru, 0, SEEK_SET) != 0 || Zavřít(deskriptor_souboru) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Čtení(-1, vyrovnávací_paměť_přenosu_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Zápis(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Zápis(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
