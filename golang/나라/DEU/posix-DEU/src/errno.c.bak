#include <errno.h>
#include <System/syscall.h>

int errno;
char **environ;

long __syscall_result(long result)
{
    if ((unsigned long)result >= (unsigned long)-4095) {
        errno = (int)-result;
        return -1;
    }
    return result;
}
