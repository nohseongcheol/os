#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <system/stat.h>
int __posix_library_test(void);

int main(void)
{
    char transfer_buffer_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int file_descriptor = open("/USER2", open_read_only);
    struct stat st;
    if (file_descriptor < 0 || fstat(file_descriptor, &st) < 0 || read(file_descriptor, transfer_buffer_2, 4) != 4 ||
        (unsigned char)transfer_buffer_2[0] != 0x7f || transfer_buffer_2[1] != 'E' || transfer_buffer_2[2] != 'L' || transfer_buffer_2[3] != 'F' ||
        lseek(file_descriptor, 0, offset_from_start) != 0 || close(file_descriptor) < 0 || getpid() <= 0)
        goto failure_flag;
    errno = 0;
    if (read(-1, transfer_buffer_2, 1) != -1 || errno != invalid_file_descriptor)
        goto failure_flag;
    if (__posix_library_test() != 0)
        goto failure_flag;
    if (write(standard_output_descriptor, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure_flag;
    return 0;
failure_flag:
    write(standard_output_descriptor, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
