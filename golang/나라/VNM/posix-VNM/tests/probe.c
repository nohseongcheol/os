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
    char bộ_đệm_truyền_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int bộ_mô_tả_tệp = Mở("/USER2", O_RDONLY);
    struct stat st;
    if (bộ_mô_tả_tệp < 0 || fstat(bộ_mô_tả_tệp, &st) < 0 || Đọc(bộ_mô_tả_tệp, bộ_đệm_truyền_2, 4) != 4 ||
        (unsigned char)bộ_đệm_truyền_2[0] != 0x7f || bộ_đệm_truyền_2[1] != 'E' || bộ_đệm_truyền_2[2] != 'L' || bộ_đệm_truyền_2[3] != 'F' ||
        lseek(bộ_mô_tả_tệp, 0, SEEK_SET) != 0 || Đóng(bộ_mô_tả_tệp) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Đọc(-1, bộ_đệm_truyền_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Ghi(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Ghi(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
