#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int അളവ്) {
    if (അളവ് < 0) { 오류번호 = -അളവ്; return -1; }
    return അളവ്;
}
int open(const char *ഫയല്_എന്_ട്രി_നാ_മം, int തുറക്കുക_ക്രമീകരണം, ...) {
    mode_t 허가 = 0;
    if (തുറക്കുക_ക്രമീകരണം & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, തുറക്കുക_ക്രമീകരണം);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ഫയല്_എന്_ട്രി_നാ_മം, തുറക്കുക_ക്രമീകരണം, 허가, 0, 0));
}
int creat(const char *ഫയല്_എന്_ട്രി_നാ_മം, mode_t 허가) { return open(ഫയല്_എന്_ട്രി_നാ_മം, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ഡാറ്റാ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ഡാറ്റാ, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ഡാറ്റാ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ഡാറ്റാ, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ഓഫ്_സെറ്റ്_മൂല്യം, int പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ഓഫ്_സെറ്റ്_മൂല്യം, പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *അവസ്ഥ_മൂല്യം) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)അവസ്ഥ_മൂല്യം, 0, 0, 0)); }
int unlink(const char *ഫയല്_എന്_ട്രി_നാ_മം) { return 호출결과(jkoros_syscall(38, (int)ഫയല്_എന്_ട്രി_നാ_മം, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ആജ്ഞ, ...) {
    int മൂല്യം = 0;
    if (ആജ്ഞ == F_DUPFD || ആജ്ഞ == F_DUPFD_CLOEXEC || ആജ്ഞ == F_SETFD || ആജ്ഞ == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ആജ്ഞ); മൂല്യം = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ആജ്ഞ, മൂല്യം, 0, 0));
}
