#include <파일규약.h>
#include "호출경계.h"

int त्रुटि_संख्या;
int 호출결과(int परिणाम) {
    if (परिणाम < 0) { त्रुटि_संख्या = -परिणाम; return -1; }
    return परिणाम;
}
int open(const char *फ़ाइल_एन्ट्री_नाम, int जारी_सेटिंग, ...) {
    mode_t 허가 = 0;
    if (जारी_सेटिंग & O_CREAT) {
        __builtin_va_list तर्क;
        __builtin_va_start(तर्क, जारी_सेटिंग);
        허가 = __builtin_va_arg(तर्क, mode_t);
        __builtin_va_end(तर्क);
    }
    return 호출결과(jkoros_syscall(30, (int)फ़ाइल_एन्ट्री_नाम, जारी_सेटिंग, 허가, 0, 0));
}
int creat(const char *फ़ाइल_एन्ट्री_नाम, mode_t 허가) { return open(फ़ाइल_एन्ट्री_नाम, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *आँकड़े, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)आँकड़े, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *आँकड़े, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)आँकड़े, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ऑफ़सेट_मान, int प्रोजेक्ट_करें_मूल) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ऑफ़सेट_मान, प्रोजेक्ट_करें_मूल, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *अवस्था_मान) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)अवस्था_मान, 0, 0, 0)); }
int unlink(const char *फ़ाइल_एन्ट्री_नाम) { return 호출결과(jkoros_syscall(38, (int)फ़ाइल_एन्ट्री_नाम, 0, 0, 0, 0)); }
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
