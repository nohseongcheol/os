#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ਮਾਪ) {
    if (ਮਾਪ < 0) { 오류번호 = -ਮਾਪ; return -1; }
    return ਮਾਪ;
}
int open(const char *ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ, int ਖੋਲੋ_ਸੈਟਿੰਗਾਂ, ...) {
    mode_t 허가 = 0;
    if (ਖੋਲੋ_ਸੈਟਿੰਗਾਂ & O_CREAT) {
        __builtin_va_list ਆਰਗੂਮੈਂਟ;
        __builtin_va_start(ਆਰਗੂਮੈਂਟ, ਖੋਲੋ_ਸੈਟਿੰਗਾਂ);
        허가 = __builtin_va_arg(ਆਰਗੂਮੈਂਟ, mode_t);
        __builtin_va_end(ਆਰਗੂਮੈਂਟ);
    }
    return 호출결과(jkoros_syscall(30, (int)ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ, ਖੋਲੋ_ਸੈਟਿੰਗਾਂ, 허가, 0, 0));
}
int creat(const char *ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ, mode_t 허가) { return open(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ਸਮੱਗਰੀ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ਸਮੱਗਰੀ, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ਸਮੱਗਰੀ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ਸਮੱਗਰੀ, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ਔਫਸੈਟ_ਕੀਮਤ, int ਪ੍ਰੋਜੈਕਟ_ਰੂਟ) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ਔਫਸੈਟ_ਕੀਮਤ, ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *ਸਥਿਤੀ_ਕੀਮਤ) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)ਸਥਿਤੀ_ਕੀਮਤ, 0, 0, 0)); }
int unlink(const char *ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ) { return 호출결과(jkoros_syscall(38, (int)ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ਕਮਾਂਡ, ...) {
    int ਕੀਮਤ = 0;
    if (ਕਮਾਂਡ == F_DUPFD || ਕਮਾਂਡ == F_DUPFD_CLOEXEC || ਕਮਾਂਡ == F_SETFD || ਕਮਾਂਡ == F_SETFL) {
        __builtin_va_list ਆਰਗੂਮੈਂਟ;
        __builtin_va_start(ਆਰਗੂਮੈਂਟ, ਕਮਾਂਡ); ਕੀਮਤ = __builtin_va_arg(ਆਰਗੂਮੈਂਟ, int); __builtin_va_end(ਆਰਗੂਮੈਂਟ);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ਕਮਾਂਡ, ਕੀਮਤ, 0, 0));
}
