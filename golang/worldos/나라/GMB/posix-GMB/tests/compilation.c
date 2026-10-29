#include <errno.h>
#include <fcntl.h>
#include <system/stat.h>
#include <system/system_identity.h>
#include <system/child_wait.h>
#include <unistd.h>

int interface_compile_test(void)
{
    char working_directory[8];
    struct stat st;
    struct system_identity_2 system_identity;
    int file_descriptor = open("/USER1", open_read_only);
    int copied_value = file_descriptor >= 0 ? dup(file_descriptor) : -1;
    if (copied_value >= 0) close(copied_value);
    if (file_descriptor >= 0) {
        fstat(file_descriptor, &st);
        lseek(file_descriptor, 0, offset_from_start);
        close(file_descriptor);
    }
    stat("/", &st);
    uname(&system_identity);
    getcwd(working_directory, sizeof(working_directory));
    return errno + getpid() + getppid();
}
