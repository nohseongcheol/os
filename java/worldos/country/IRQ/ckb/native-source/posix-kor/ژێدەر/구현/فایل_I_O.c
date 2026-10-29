#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int 결과) {
    if (결과 < 0) { 오류번호 = -결과; return -1; }
    return 결과;
}
int open(const char *فایل_تێنووسین_ناو, int کردنەوە_ڕێكبەندەكان, ...) {
    mode_t 허가 = 0;
    if (کردنەوە_ڕێكبەندەكان & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, کردنەوە_ڕێكبەندەكان);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)فایل_تێنووسین_ناو, کردنەوە_ڕێكبەندەكان, 허가, 0, 0));
}
int creat(const char *فایل_تێنووسین_ناو, mode_t 허가) { return open(فایل_تێنووسین_ناو, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *دەیتا, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)دەیتا, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *دەیتا, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)دەیتا, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ئۆفسێت_نرخ, int 기준) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ئۆفسێت_نرخ, 기준, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *دۆخ_نرخ) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)دۆخ_نرخ, 0, 0, 0)); }
int unlink(const char *فایل_تێنووسین_ناو) { return 호출결과(jkoros_syscall(38, (int)فایل_تێنووسین_ناو, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int فەرمان, ...) {
    int نرخ = 0;
    if (فەرمان == F_DUPFD || فەرمان == F_DUPFD_CLOEXEC || فەرمان == F_SETFD || فەرمان == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, فەرمان); نرخ = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, فەرمان, نرخ, 0, 0));
}
