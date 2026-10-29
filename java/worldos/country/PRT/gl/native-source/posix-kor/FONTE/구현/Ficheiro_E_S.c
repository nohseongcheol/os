#include <파일규약.h>
#include "호출경계.h"

int número_de_erro;
int 호출결과(int RESULTANTE) {
    if (RESULTANTE < 0) { número_de_erro = -RESULTANTE; return -1; }
    return RESULTANTE;
}
int open(const char *Ficheiro_introdución_nome, int abrir_Configuración, ...) {
    mode_t 허가 = 0;
    if (abrir_Configuración & O_CREAT) {
        __builtin_va_list Argumentos;
        __builtin_va_start(Argumentos, abrir_Configuración);
        허가 = __builtin_va_arg(Argumentos, mode_t);
        __builtin_va_end(Argumentos);
    }
    return 호출결과(jkoros_syscall(30, (int)Ficheiro_introdución_nome, abrir_Configuración, 허가, 0, 0));
}
int creat(const char *Ficheiro_introdución_nome, mode_t 허가) { return open(Ficheiro_introdución_nome, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *datos, size_t byte_CONTAR) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)datos, byte_CONTAR, 0, 0));
}
ssize_t write(int 파일서술자, const void *datos, size_t byte_CONTAR) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)datos, byte_CONTAR, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t DESPRAZAMENTO_VALOR, int Project_raíz) {
    return 호출결과(jkoros_syscall(34, 파일서술자, DESPRAZAMENTO_VALOR, Project_raíz, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Estado_VALOR) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Estado_VALOR, 0, 0, 0)); }
int unlink(const char *Ficheiro_introdución_nome) { return 호출결과(jkoros_syscall(38, (int)Ficheiro_introdución_nome, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_CONTAR) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_CONTAR, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Orde, ...) {
    int VALOR = 0;
    if (Orde == F_DUPFD || Orde == F_DUPFD_CLOEXEC || Orde == F_SETFD || Orde == F_SETFL) {
        __builtin_va_list Argumentos;
        __builtin_va_start(Argumentos, Orde); VALOR = __builtin_va_arg(Argumentos, int); __builtin_va_end(Argumentos);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Orde, VALOR, 0, 0));
}
