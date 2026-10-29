#include <파일규약.h>
#include "호출경계.h"

int מספר_שגיאה;
int 호출결과(int תוצאה) {
    if (תוצאה < 0) { מספר_שגיאה = -תוצאה; return -1; }
    return תוצאה;
}
int open(const char *קובץ_ערך_שם, int פתח_הגדרות, ...) {
    mode_t 허가 = 0;
    if (פתח_הגדרות & O_CREAT) {
        __builtin_va_list ארגומנטים;
        __builtin_va_start(ארגומנטים, פתח_הגדרות);
        허가 = __builtin_va_arg(ארגומנטים, mode_t);
        __builtin_va_end(ארגומנטים);
    }
    return 호출결과(jkoros_syscall(30, (int)קובץ_ערך_שם, פתח_הגדרות, 허가, 0, 0));
}
int creat(const char *קובץ_ערך_שם, mode_t 허가) { return open(קובץ_ערך_שם, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *נתונים, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)נתונים, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *נתונים, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)נתונים, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t היסט_ערך, int לשקף_בסיס) {
    return 호출결과(jkoros_syscall(34, 파일서술자, היסט_ערך, לשקף_בסיס, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *מצב_ערך) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)מצב_ערך, 0, 0, 0)); }
int unlink(const char *קובץ_ערך_שם) { return 호출결과(jkoros_syscall(38, (int)קובץ_ערך_שם, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int פקודה, ...) {
    int ערך = 0;
    if (פקודה == F_DUPFD || פקודה == F_DUPFD_CLOEXEC || פקודה == F_SETFD || פקודה == F_SETFL) {
        __builtin_va_list ארגומנטים;
        __builtin_va_start(ארגומנטים, פקודה); ערך = __builtin_va_arg(ארגומנטים, int); __builtin_va_end(ארגומנטים);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, פקודה, ערך, 0, 0));
}
