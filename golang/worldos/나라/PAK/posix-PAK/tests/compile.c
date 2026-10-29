#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/wait.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct stat st;
    struct utsname نظام_کی_شناخت;
    int فائل_کا_وصف_کنندہ = کھولیں("/USER1", O_RDONLY);
    int copy = فائل_کا_وصف_کنندہ >= 0 ? dup(فائل_کا_وصف_کنندہ) : -1;
    if (copy >= 0) بندکریں(copy);
    if (فائل_کا_وصف_کنندہ >= 0) {
        fstat(فائل_کا_وصف_کنندہ, &st);
        lseek(فائل_کا_وصف_کنندہ, 0, SEEK_SET);
        بندکریں(فائل_کا_وصف_کنندہ);
    }
    stat("/", &st);
    uname(&نظام_کی_شناخت);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
