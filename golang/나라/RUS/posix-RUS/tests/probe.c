/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <система/stat.h>
int __posix_library_test(void);

int main(void)
{
    char буфер_передачи_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int дескриптор_файла = открыть("/USER2", O_RDONLY);
    struct состояние_файла st;
    if (дескриптор_файла < 0 || получить_состояние_открытого_файла(дескриптор_файла, &st) < 0 || читать(дескриптор_файла, буфер_передачи_2, 4) != 4 ||
        (unsigned char)буфер_передачи_2[0] != 0x7f || буфер_передачи_2[1] != 'E' || буфер_передачи_2[2] != 'L' || буфер_передачи_2[3] != 'F' ||
        переместить_позицию_файла(дескриптор_файла, 0, SEEK_SET) != 0 || закрыть(дескриптор_файла) < 0 || получить_номер_процесса() <= 0)
        goto failure;
    errno = 0;
    if (читать(-1, буфер_передачи_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (писать(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    писать(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
