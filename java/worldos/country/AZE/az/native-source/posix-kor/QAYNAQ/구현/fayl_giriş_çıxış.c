#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ölçü) {
    if (ölçü < 0) { 오류번호 = -ölçü; return -1; }
    return ölçü;
}
int open(const char *fayl_daxiletmə_ad, int açmaq_Parametrlər, ...) {
    mode_t 허가 = 0;
    if (açmaq_Parametrlər & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, açmaq_Parametrlər);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)fayl_daxiletmə_ad, açmaq_Parametrlər, 허가, 0, 0));
}
int creat(const char *fayl_daxiletmə_ad, mode_t 허가) { return open(fayl_daxiletmə_ad, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *verilənlər, size_t bayt_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)verilənlər, bayt_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *verilənlər, size_t bayt_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)verilənlər, bayt_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Project_kök) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, Project_kök, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *vəziyyət_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)vəziyyət_VALUE, 0, 0, 0)); }
int unlink(const char *fayl_daxiletmə_ad) { return 호출결과(jkoros_syscall(38, (int)fayl_daxiletmə_ad, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bayt_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bayt_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Əmr, ...) {
    int VALUE = 0;
    if (Əmr == F_DUPFD || Əmr == F_DUPFD_CLOEXEC || Əmr == F_SETFD || Əmr == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Əmr); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Əmr, VALUE, 0, 0));
}
