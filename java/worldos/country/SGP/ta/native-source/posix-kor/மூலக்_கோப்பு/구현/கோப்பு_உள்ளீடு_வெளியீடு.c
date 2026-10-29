#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int அளவிடக்கூடியது) {
    if (அளவிடக்கூடியது < 0) { 오류번호 = -அளவிடக்கூடியது; return -1; }
    return அளவிடக்கூடியது;
}
int open(const char *கோப்பு_உள்ளீடு_பெயர், int திற_அமைப்புகள், ...) {
    mode_t 허가 = 0;
    if (திற_அமைப்புகள் & O_CREAT) {
        __builtin_va_list செயலுருபுகள்;
        __builtin_va_start(செயலுருபுகள், திற_அமைப்புகள்);
        허가 = __builtin_va_arg(செயலுருபுகள், mode_t);
        __builtin_va_end(செயலுருபுகள்);
    }
    return 호출결과(jkoros_syscall(30, (int)கோப்பு_உள்ளீடு_பெயர், திற_அமைப்புகள், 허가, 0, 0));
}
int creat(const char *கோப்பு_உள்ளீடு_பெயர், mode_t 허가) { return open(கோப்பு_உள்ளீடு_பெயர், O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *தரவு, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)தரவு, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *தரவு, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)தரவு, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ஆஃப்செட்_மதிப்பு, int திட்டப்பணி_மூலம்) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ஆஃப்செட்_மதிப்பு, திட்டப்பணி_மூலம், 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *நிலை_மதிப்பு_e10195a1) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)நிலை_மதிப்பு_e10195a1, 0, 0, 0)); }
int unlink(const char *கோப்பு_உள்ளீடு_பெயர்) { return 호출결과(jkoros_syscall(38, (int)கோப்பு_உள்ளீடு_பெயர், 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int கட்டளை, ...) {
    int மதிப்பு = 0;
    if (கட்டளை == F_DUPFD || கட்டளை == F_DUPFD_CLOEXEC || கட்டளை == F_SETFD || கட்டளை == F_SETFL) {
        __builtin_va_list செயலுருபுகள்;
        __builtin_va_start(செயலுருபுகள், கட்டளை); மதிப்பு = __builtin_va_arg(செயலுருபுகள், int); __builtin_va_end(செயலுருபுகள்);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, கட்டளை, மதிப்பு, 0, 0));
}
