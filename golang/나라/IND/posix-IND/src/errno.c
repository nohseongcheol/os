/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <प्रणाली/syscall.h>

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
