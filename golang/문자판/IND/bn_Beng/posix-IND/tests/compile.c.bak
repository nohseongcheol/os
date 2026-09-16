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
    struct utsname ব্যবস্থার_পরিচয়;
    int নথি_নির্দেশক = open("/USER1", O_RDONLY);
    int copy = নথি_নির্দেশক >= 0 ? dup(নথি_নির্দেশক) : -1;
    if (copy >= 0) close(copy);
    if (নথি_নির্দেশক >= 0) {
        fstat(নথি_নির্দেশক, &st);
        lseek(নথি_নির্দেশক, 0, SEEK_SET);
        close(নথি_নির্দেশক);
    }
    stat("/", &st);
    uname(&ব্যবস্থার_পরিচয়);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
