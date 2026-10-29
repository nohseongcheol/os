#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ئۆلچەم) {
    if (ئۆلچەم < 0) { 오류번호 = -ئۆلچەم; return -1; }
    return ئۆلچەم;
}
int open(const char *ھۆججەت_كىرگۈزۈش_نامى, int قۇرۇش_تەڭشەك, ...) {
    mode_t 허가 = 0;
    if (قۇرۇش_تەڭشەك & O_CREAT) {
        __builtin_va_list ئۆزگەرگۈچىلەر;
        __builtin_va_start(ئۆزگەرگۈچىلەر, قۇرۇش_تەڭشەك);
        허가 = __builtin_va_arg(ئۆزگەرگۈچىلەر, mode_t);
        __builtin_va_end(ئۆزگەرگۈچىلەر);
    }
    return 호출결과(jkoros_syscall(30, (int)ھۆججەت_كىرگۈزۈش_نامى, قۇرۇش_تەڭشەك, 허가, 0, 0));
}
int creat(const char *ھۆججەت_كىرگۈزۈش_نامى, mode_t 허가) { return open(ھۆججەت_كىرگۈزۈش_نامى, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *مەلۇمات, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)مەلۇمات, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *مەلۇمات, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)مەلۇمات, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ئاغما_قىممىتى, int كۆرسىتىش_يىلتىز) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ئاغما_قىممىتى, كۆرسىتىش_يىلتىز, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *ھالەت_قىممىتى) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)ھالەت_قىممىتى, 0, 0, 0)); }
int unlink(const char *ھۆججەت_كىرگۈزۈش_نامى) { return 호출결과(jkoros_syscall(38, (int)ھۆججەت_كىرگۈزۈش_نامى, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int بۇيرۇق, ...) {
    int قىممىتى = 0;
    if (بۇيرۇق == F_DUPFD || بۇيرۇق == F_DUPFD_CLOEXEC || بۇيرۇق == F_SETFD || بۇيرۇق == F_SETFL) {
        __builtin_va_list ئۆزگەرگۈچىلەر;
        __builtin_va_start(ئۆزگەرگۈچىلەر, بۇيرۇق); قىممىتى = __builtin_va_arg(ئۆزگەرگۈچىلەر, int); __builtin_va_end(ئۆزگەرگۈچىلەر);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, بۇيرۇق, قىممىتى, 0, 0));
}
