#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int 결과) {
    if (결과 < 0) { 오류번호 = -결과; return -1; }
    return 결과;
}
int open(const char *فائل_داخلا_نالو, int ٺاھيو_سيٽنگون, ...) {
    mode_t 허가 = 0;
    if (ٺاھيو_سيٽنگون & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ٺاھيو_سيٽنگون);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)فائل_داخلا_نالو, ٺاھيو_سيٽنگون, 허가, 0, 0));
}
int creat(const char *فائل_داخلا_نالو, mode_t 허가) { return open(فائل_داخلا_نالو, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ڪوائف, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ڪوائف, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ڪوائف, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ڪوائف, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t آف_سيٽ_قدر, int 기준) {
    return 호출결과(jkoros_syscall(34, 파일서술자, آف_سيٽ_قدر, 기준, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *حالت_قدر) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)حالت_قدر, 0, 0, 0)); }
int unlink(const char *فائل_داخلا_نالو) { return 호출결과(jkoros_syscall(38, (int)فائل_داخلا_نالو, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int حڪم, ...) {
    int قدر = 0;
    if (حڪم == F_DUPFD || حڪم == F_DUPFD_CLOEXEC || حڪم == F_SETFD || حڪم == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, حڪم); قدر = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, حڪم, قدر, 0, 0));
}
