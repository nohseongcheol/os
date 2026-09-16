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
    char aktarım_ara_belleği_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int dosya_tanımlayıcısı = Aç("/USER2", O_RDONLY);
    struct stat st;
    if (dosya_tanımlayıcısı < 0 || fstat(dosya_tanımlayıcısı, &st) < 0 || Okuma(dosya_tanımlayıcısı, aktarım_ara_belleği_2, 4) != 4 ||
        (unsigned char)aktarım_ara_belleği_2[0] != 0x7f || aktarım_ara_belleği_2[1] != 'E' || aktarım_ara_belleği_2[2] != 'L' || aktarım_ara_belleği_2[3] != 'F' ||
        lseek(dosya_tanımlayıcısı, 0, SEEK_SET) != 0 || Kapat(dosya_tanımlayıcısı) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Okuma(-1, aktarım_ara_belleği_2, 1) != -1 || errno != EBADF)
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
