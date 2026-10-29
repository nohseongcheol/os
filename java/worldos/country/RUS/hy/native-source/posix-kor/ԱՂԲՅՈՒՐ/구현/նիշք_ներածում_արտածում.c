#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int չափ) {
    if (չափ < 0) { 오류번호 = -չափ; return -1; }
    return չափ;
}
int open(const char *նիշք_մուտքագրում_անուն, int բացել_Կարգավորումներ, ...) {
    mode_t 허가 = 0;
    if (բացել_Կարգավորումներ & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, բացել_Կարգավորումներ);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)նիշք_մուտքագրում_անուն, բացել_Կարգավորումներ, 허가, 0, 0));
}
int creat(const char *նիշք_մուտքագրում_անուն, mode_t 허가) { return open(նիշք_մուտքագրում_անուն, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *տվյալ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)տվյալ, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *տվյալ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)տվյալ, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Տեղաշարժում_արժեք, int արձակել_արմատ) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Տեղաշարժում_արժեք, արձակել_արմատ, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *վիճակ_արժեք) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)վիճակ_արժեք, 0, 0, 0)); }
int unlink(const char *նիշք_մուտքագրում_անուն) { return 호출결과(jkoros_syscall(38, (int)նիշք_մուտքագրում_անուն, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Հրահանգ, ...) {
    int արժեք = 0;
    if (Հրահանգ == F_DUPFD || Հրահանգ == F_DUPFD_CLOEXEC || Հրահանգ == F_SETFD || Հրահանգ == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Հրահանգ); արժեք = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Հրահանգ, արժեք, 0, 0));
}
