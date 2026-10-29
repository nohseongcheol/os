#include <파일규약.h>
#include "호출경계.h"

int қате_нөмірі;
int 호출결과(int НӘТИЖЕ) {
    if (НӘТИЖЕ < 0) { қате_нөмірі = -НӘТИЖЕ; return -1; }
    return НӘТИЖЕ;
}
int open(const char *файл_енгізу_аты, int ашу_Параметрлер, ...) {
    mode_t 허가 = 0;
    if (ашу_Параметрлер & O_CREAT) {
        __builtin_va_list Аргументтер;
        __builtin_va_start(Аргументтер, ашу_Параметрлер);
        허가 = __builtin_va_arg(Аргументтер, mode_t);
        __builtin_va_end(Аргументтер);
    }
    return 호출결과(jkoros_syscall(30, (int)файл_енгізу_аты, ашу_Параметрлер, 허가, 0, 0));
}
int creat(const char *файл_енгізу_аты, mode_t 허가) { return open(файл_енгізу_аты, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *деректер, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)деректер, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *деректер, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)деректер, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t жылжыту_мән_450fc799, int жоба_түбір) {
    return 호출결과(jkoros_syscall(34, 파일서술자, жылжыту_мән_450fc799, жоба_түбір, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *күй_мән) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)күй_мән, 0, 0, 0)); }
int unlink(const char *файл_енгізу_аты) { return 호출결과(jkoros_syscall(38, (int)файл_енгізу_аты, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Команда, ...) {
    int мән = 0;
    if (Команда == F_DUPFD || Команда == F_DUPFD_CLOEXEC || Команда == F_SETFD || Команда == F_SETFL) {
        __builtin_va_list Аргументтер;
        __builtin_va_start(Аргументтер, Команда); мән = __builtin_va_arg(Аргументтер, int); __builtin_va_end(Аргументтер);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Команда, мән, 0, 0));
}
