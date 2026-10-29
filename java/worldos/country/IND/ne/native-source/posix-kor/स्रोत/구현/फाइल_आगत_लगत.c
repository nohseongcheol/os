#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int मापन) {
    if (मापन < 0) { 오류번호 = -मापन; return -1; }
    return मापन;
}
int open(const char *फाइल_प्रविष्टि_नाम, int सिर्जना_सेटिङहरू, ...) {
    mode_t 허가 = 0;
    if (सिर्जना_सेटिङहरू & O_CREAT) {
        __builtin_va_list तर्क;
        __builtin_va_start(तर्क, सिर्जना_सेटिङहरू);
        허가 = __builtin_va_arg(तर्क, mode_t);
        __builtin_va_end(तर्क);
    }
    return 호출결과(jkoros_syscall(30, (int)फाइल_प्रविष्टि_नाम, सिर्जना_सेटिङहरू, 허가, 0, 0));
}
int creat(const char *फाइल_प्रविष्टि_नाम, mode_t 허가) { return open(फाइल_प्रविष्टि_नाम, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *लगत, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)लगत, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *लगत, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)लगत, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t अफसेट_मान, int परियोजना_रूट) {
    return 호출결과(jkoros_syscall(34, 파일서술자, अफसेट_मान, परियोजना_रूट, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *स्थिति_मान) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)स्थिति_मान, 0, 0, 0)); }
int unlink(const char *फाइल_प्रविष्टि_नाम) { return 호출결과(jkoros_syscall(38, (int)फाइल_प्रविष्टि_नाम, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int आदेश, ...) {
    int मान = 0;
    if (आदेश == F_DUPFD || आदेश == F_DUPFD_CLOEXEC || आदेश == F_SETFD || आदेश == F_SETFL) {
        __builtin_va_list तर्क;
        __builtin_va_start(तर्क, आदेश); मान = __builtin_va_arg(तर्क, int); __builtin_va_end(तर्क);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, आदेश, मान, 0, 0));
}
