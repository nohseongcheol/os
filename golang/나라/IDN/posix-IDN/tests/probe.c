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
    char penyangga_transfer_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int deskriptor_berkas = Buka("/USER2", O_RDONLY);
    struct stat st;
    if (deskriptor_berkas < 0 || fstat(deskriptor_berkas, &st) < 0 || Baca(deskriptor_berkas, penyangga_transfer_2, 4) != 4 ||
        (unsigned char)penyangga_transfer_2[0] != 0x7f || penyangga_transfer_2[1] != 'E' || penyangga_transfer_2[2] != 'L' || penyangga_transfer_2[3] != 'F' ||
        lseek(deskriptor_berkas, 0, SEEK_SET) != 0 || Tutup(deskriptor_berkas) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Baca(-1, penyangga_transfer_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Tulis(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Tulis(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
