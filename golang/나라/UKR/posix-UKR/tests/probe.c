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
    char буфер_передавання_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int дескриптор_файла = Відкрити("/USER2", O_RDONLY);
    struct stat st;
    if (дескриптор_файла < 0 || fstat(дескриптор_файла, &st) < 0 || Читання(дескриптор_файла, буфер_передавання_2, 4) != 4 ||
        (unsigned char)буфер_передавання_2[0] != 0x7f || буфер_передавання_2[1] != 'E' || буфер_передавання_2[2] != 'L' || буфер_передавання_2[3] != 'F' ||
        lseek(дескриптор_файла, 0, SEEK_SET) != 0 || Закрити(дескриптор_файла) < 0 || getpid() <= 0)
        goto failure;
    errno = 0;
    if (Читання(-1, буфер_передавання_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (Запис(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    Запис(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
