#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ልኬት) {
    if (ልኬት < 0) { 오류번호 = -ልኬት; return -1; }
    return ልኬት;
}
int open(const char *ፋይል_ምዝግብ_ስም, int ክፈት_ቅንብሮች, ...) {
    mode_t 허가 = 0;
    if (ክፈት_ቅንብሮች & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ክፈት_ቅንብሮች);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ፋይል_ምዝግብ_ስም, ክፈት_ቅንብሮች, 허가, 0, 0));
}
int creat(const char *ፋይል_ምዝግብ_ስም, mode_t 허가) { return open(ፋይል_ምዝግብ_ስም, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ውሂብ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ውሂብ, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ውሂብ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ውሂብ, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ዝንፍ_እሴት, int አሳይ_ስር) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ዝንፍ_እሴት, አሳይ_ስር, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *ዞን_እሴት) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)ዞን_እሴት, 0, 0, 0)); }
int unlink(const char *ፋይል_ምዝግብ_ስም) { return 호출결과(jkoros_syscall(38, (int)ፋይል_ምዝግብ_ስም, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ትእዛዝ, ...) {
    int እሴት = 0;
    if (ትእዛዝ == F_DUPFD || ትእዛዝ == F_DUPFD_CLOEXEC || ትእዛዝ == F_SETFD || ትእዛዝ == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ትእዛዝ); እሴት = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ትእዛዝ, እሴት, 0, 0));
}
