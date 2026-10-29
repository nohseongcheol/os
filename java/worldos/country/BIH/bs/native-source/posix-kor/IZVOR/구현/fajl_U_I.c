#include <파일규약.h>
#include "호출경계.h"

int broj_greške;
int 호출결과(int mjera) {
    if (mjera < 0) { broj_greške = -mjera; return -1; }
    return mjera;
}
int open(const char *fajl_unos_naziv, int kreirati_Postavke, ...) {
    mode_t 허가 = 0;
    if (kreirati_Postavke & O_CREAT) {
        __builtin_va_list Argumenti;
        __builtin_va_start(Argumenti, kreirati_Postavke);
        허가 = __builtin_va_arg(Argumenti, mode_t);
        __builtin_va_end(Argumenti);
    }
    return 호출결과(jkoros_syscall(30, (int)fajl_unos_naziv, kreirati_Postavke, 허가, 0, 0));
}
int creat(const char *fajl_unos_naziv, mode_t 허가) { return open(fajl_unos_naziv, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *podaci, size_t bajt_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)podaci, bajt_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *podaci, size_t bajt_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)podaci, bajt_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Pomak_VALUE, int projicirati_koijen) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Pomak_VALUE, projicirati_koijen, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *stanje_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)stanje_VALUE, 0, 0, 0)); }
int unlink(const char *fajl_unos_naziv) { return 호출결과(jkoros_syscall(38, (int)fajl_unos_naziv, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bajt_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bajt_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Naredba, ...) {
    int VALUE = 0;
    if (Naredba == F_DUPFD || Naredba == F_DUPFD_CLOEXEC || Naredba == F_SETFD || Naredba == F_SETFL) {
        __builtin_va_list Argumenti;
        __builtin_va_start(Argumenti, Naredba); VALUE = __builtin_va_arg(Argumenti, int); __builtin_va_end(Argumenti);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Naredba, VALUE, 0, 0));
}
