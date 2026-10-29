#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int Mooss) {
    if (Mooss < 0) { 오류번호 = -Mooss; return -1; }
    return Mooss;
}
int open(const char *Fichier_Agab_Numm, int ariichten_Astellungen, ...) {
    mode_t 허가 = 0;
    if (ariichten_Astellungen & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ariichten_Astellungen);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)Fichier_Agab_Numm, ariichten_Astellungen, 허가, 0, 0));
}
int creat(const char *Fichier_Agab_Numm, mode_t 허가) { return open(Fichier_Agab_Numm, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *Daten, size_t Byte_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)Daten, Byte_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *Daten, size_t Byte_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)Daten, Byte_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int projezéieren_Racinn) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, projezéieren_Racinn, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Status_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Status_VALUE, 0, 0, 0)); }
int unlink(const char *Fichier_Agab_Numm) { return 호출결과(jkoros_syscall(38, (int)Fichier_Agab_Numm, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t Byte_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, Byte_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Befeel, ...) {
    int VALUE = 0;
    if (Befeel == F_DUPFD || Befeel == F_DUPFD_CLOEXEC || Befeel == F_SETFD || Befeel == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Befeel); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Befeel, VALUE, 0, 0));
}
