#include <파일규약.h>
#include "호출경계.h"

int kļūdas_numurs;
int 호출결과(int mērs) {
    if (mērs < 0) { kļūdas_numurs = -mērs; return -1; }
    return mērs;
}
int open(const char *Fails_ievade_nosaukums, int atvērt_Iestatījumi, ...) {
    mode_t 허가 = 0;
    if (atvērt_Iestatījumi & O_CREAT) {
        __builtin_va_list Parametri;
        __builtin_va_start(Parametri, atvērt_Iestatījumi);
        허가 = __builtin_va_arg(Parametri, mode_t);
        __builtin_va_end(Parametri);
    }
    return 호출결과(jkoros_syscall(30, (int)Fails_ievade_nosaukums, atvērt_Iestatījumi, 허가, 0, 0));
}
int creat(const char *Fails_ievade_nosaukums, mode_t 허가) { return open(Fails_ievade_nosaukums, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *dati, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)dati, byte_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *dati, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)dati, byte_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Nobīde_VALUE, int Project_sakne) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Nobīde_VALUE, Project_sakne, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Statuss_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Statuss_VALUE, 0, 0, 0)); }
int unlink(const char *Fails_ievade_nosaukums) { return 호출결과(jkoros_syscall(38, (int)Fails_ievade_nosaukums, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Komanda, ...) {
    int VALUE = 0;
    if (Komanda == F_DUPFD || Komanda == F_DUPFD_CLOEXEC || Komanda == F_SETFD || Komanda == F_SETFL) {
        __builtin_va_list Parametri;
        __builtin_va_start(Parametri, Komanda); VALUE = __builtin_va_arg(Parametri, int); __builtin_va_end(Parametri);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Komanda, VALUE, 0, 0));
}
