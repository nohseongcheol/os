#include <파일규약.h>
#include "호출경계.h"

int número_d_error;
int 호출결과(int RESULTAT) {
    if (RESULTAT < 0) { número_d_error = -RESULTAT; return -1; }
    return RESULTAT;
}
int open(const char *arxiu_introducció_nom, int crear_Configuració, ...) {
    mode_t 허가 = 0;
    if (crear_Configuració & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, crear_Configuració);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)arxiu_introducció_nom, crear_Configuració, 허가, 0, 0));
}
int creat(const char *arxiu_introducció_nom, mode_t 허가) { return open(arxiu_introducció_nom, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *dades, size_t byte_COMPT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)dades, byte_COMPT, 0, 0));
}
ssize_t write(int 파일서술자, const void *dades, size_t byte_COMPT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)dades, byte_COMPT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t DESPLAÇAMENT_VALOR, int Project_rel) {
    return 호출결과(jkoros_syscall(34, 파일서술자, DESPLAÇAMENT_VALOR, Project_rel, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Estat_VALOR) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Estat_VALOR, 0, 0, 0)); }
int unlink(const char *arxiu_introducció_nom) { return 호출결과(jkoros_syscall(38, (int)arxiu_introducció_nom, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_COMPT) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_COMPT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Ordre, ...) {
    int VALOR = 0;
    if (Ordre == F_DUPFD || Ordre == F_DUPFD_CLOEXEC || Ordre == F_SETFD || Ordre == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Ordre); VALOR = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Ordre, VALOR, 0, 0));
}
