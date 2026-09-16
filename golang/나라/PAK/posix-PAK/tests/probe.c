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
    char منتقلی_کا_عارضی_ذخیرہ_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int فائل_کا_وصف_کنندہ = کھولیں("/USER2", O_RDONLY);
    struct stat st;
    if (فائل_کا_وصف_کنندہ < 0 || fstat(فائل_کا_وصف_کنندہ, &st) < 0 || پڑھیں(فائل_کا_وصف_کنندہ, منتقلی_کا_عارضی_ذخیرہ_2, 4) != 4 ||
        (unsigned char)منتقلی_کا_عارضی_ذخیرہ_2[0] != 0x7f || منتقلی_کا_عارضی_ذخیرہ_2[1] != 'E' || منتقلی_کا_عارضی_ذخیرہ_2[2] != 'L' || منتقلی_کا_عارضی_ذخیرہ_2[3] != 'F' ||
        lseek(فائل_کا_وصف_کنندہ, 0, SEEK_SET) != 0 || بندکریں(فائل_کا_وصف_کنندہ) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (پڑھیں(-1, منتقلی_کا_عارضی_ذخیرہ_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (لکھیں(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    لکھیں(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
