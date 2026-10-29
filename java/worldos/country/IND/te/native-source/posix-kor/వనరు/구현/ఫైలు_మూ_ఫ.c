#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ప్రమాణం) {
    if (ప్రమాణం < 0) { 오류번호 = -ప్రమాణం; return -1; }
    return ప్రమాణం;
}
int open(const char *ఫైలు_ప్రవేశం_పేరు, int తెరువు_సెట్టింగ్_లు, ...) {
    mode_t 허가 = 0;
    if (తెరువు_సెట్టింగ్_లు & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, తెరువు_సెట్టింగ్_లు);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ఫైలు_ప్రవేశం_పేరు, తెరువు_సెట్టింగ్_లు, 허가, 0, 0));
}
int creat(const char *ఫైలు_ప్రవేశం_పేరు, mode_t 허가) { return open(ఫైలు_ప్రవేశం_పేరు, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *డేటా, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)డేటా, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *డేటా, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)డేటా, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ఆఫ్_సెట్_మూల్యం, int ప్రొజెక్ట్_మూలం) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ఆఫ్_సెట్_మూల్యం, ప్రొజెక్ట్_మూలం, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *స్థితి_మూల్యం) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)స్థితి_మూల్యం, 0, 0, 0)); }
int unlink(const char *ఫైలు_ప్రవేశం_పేరు) { return 호출결과(jkoros_syscall(38, (int)ఫైలు_ప్రవేశం_పేరు, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ఆదేశము, ...) {
    int మూల్యం = 0;
    if (ఆదేశము == F_DUPFD || ఆదేశము == F_DUPFD_CLOEXEC || ఆదేశము == F_SETFD || ఆదేశము == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ఆదేశము); మూల్యం = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ఆదేశము, మూల్యం, 0, 0));
}
