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
    char স্থানান্তরের_অস্থায়ী_ভান্ডার_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int নথি_নির্দেশক = open("/USER2", O_RDONLY);
    struct stat st;
    if (নথি_নির্দেশক < 0 || fstat(নথি_নির্দেশক, &st) < 0 || pora(নথি_নির্দেশক, স্থানান্তরের_অস্থায়ী_ভান্ডার_2, 4) != 4 ||
        (unsigned char)স্থানান্তরের_অস্থায়ী_ভান্ডার_2[0] != 0x7f || স্থানান্তরের_অস্থায়ী_ভান্ডার_2[1] != 'E' || স্থানান্তরের_অস্থায়ী_ভান্ডার_2[2] != 'L' || স্থানান্তরের_অস্থায়ী_ভান্ডার_2[3] != 'F' ||
        lseek(নথি_নির্দেশক, 0, SEEK_SET) != 0 || close(নথি_নির্দেশক) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (pora(-1, স্থানান্তরের_অস্থায়ী_ভান্ডার_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (lekha(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    lekha(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
