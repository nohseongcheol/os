#include <파일규약.h>
#include "호출경계.h"

int klaidos_numeris;
int 호출결과(int REZULTATAS) {
    if (REZULTATAS < 0) { klaidos_numeris = -REZULTATAS; return -1; }
    return REZULTATAS;
}
int open(const char *Failas_įrašas_pavadinimas, int kurti_Parametrai, ...) {
    mode_t 허가 = 0;
    if (kurti_Parametrai & O_CREAT) {
        __builtin_va_list Argumentai;
        __builtin_va_start(Argumentai, kurti_Parametrai);
        허가 = __builtin_va_arg(Argumentai, mode_t);
        __builtin_va_end(Argumentai);
    }
    return 호출결과(jkoros_syscall(30, (int)Failas_įrašas_pavadinimas, kurti_Parametrai, 허가, 0, 0));
}
int creat(const char *Failas_įrašas_pavadinimas, mode_t 허가) { return open(Failas_įrašas_pavadinimas, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *duomenys, size_t baitas_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)duomenys, baitas_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *duomenys, size_t baitas_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)duomenys, baitas_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Project_šaknis) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, Project_šaknis, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Būsena_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Būsena_VALUE, 0, 0, 0)); }
int unlink(const char *Failas_įrašas_pavadinimas) { return 호출결과(jkoros_syscall(38, (int)Failas_įrašas_pavadinimas, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t baitas_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, baitas_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Komanda, ...) {
    int VALUE = 0;
    if (Komanda == F_DUPFD || Komanda == F_DUPFD_CLOEXEC || Komanda == F_SETFD || Komanda == F_SETFL) {
        __builtin_va_list Argumentai;
        __builtin_va_start(Argumentai, Komanda); VALUE = __builtin_va_arg(Argumentai, int); __builtin_va_end(Argumentai);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Komanda, VALUE, 0, 0));
}
