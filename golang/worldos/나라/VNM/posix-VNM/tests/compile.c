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
    struct utsname thông_tin_hệ_thống;
    int bộ_mô_tả_tệp = Mở("/USER1", O_RDONLY);
    int copy = bộ_mô_tả_tệp >= 0 ? dup(bộ_mô_tả_tệp) : -1;
    if (copy >= 0) Đóng(copy);
    if (bộ_mô_tả_tệp >= 0) {
        fstat(bộ_mô_tả_tệp, &st);
        lseek(bộ_mô_tả_tệp, 0, SEEK_SET);
        Đóng(bộ_mô_tả_tệp);
    }
    stat("/", &st);
    uname(&thông_tin_hệ_thống);
    getcwd(cwd, sizeof(cwd));
    return errno + getpid() + getppid();
}
