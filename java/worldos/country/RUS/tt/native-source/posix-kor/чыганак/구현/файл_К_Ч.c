#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int үлчәм) {
    if (үлчәм < 0) { 오류번호 = -үлчәм; return -1; }
    return үлчәм;
}
int open(const char *файл_кертү_исем, int ачу_Параметрлар, ...) {
    mode_t 허가 = 0;
    if (ачу_Параметрлар & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ачу_Параметрлар);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)файл_кертү_исем, ачу_Параметрлар, 허가, 0, 0));
}
int creat(const char *файл_кертү_исем, mode_t 허가) { return open(файл_кертү_исем, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *мәгълүмат, size_t байт_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)мәгълүмат, байт_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *мәгълүмат, size_t байт_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)мәгълүмат, байт_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int экранга_җибәрү_тамыр) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, экранга_җибәрү_тамыр, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *халәт_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)халәт_VALUE, 0, 0, 0)); }
int unlink(const char *файл_кертү_исем) { return 호출결과(jkoros_syscall(38, (int)файл_кертү_исем, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t байт_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, байт_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int команда, ...) {
    int VALUE = 0;
    if (команда == F_DUPFD || команда == F_DUPFD_CLOEXEC || команда == F_SETFD || команда == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, команда); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, команда, VALUE, 0, 0));
}
