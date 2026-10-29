#include <Arquivo_ABI.h>
#include "Ligar_limite.h"

int número_do_erro;
int 호출결과(int resultado) {
    if (resultado < 0) { número_do_erro = -resultado; return -1; }
    return resultado;
}
int open(const char *Arquivo_entrada_nome, int abrir_Configurações, ...) {
    mode_t concessão_Permissão = 0;
    if (abrir_Configurações & O_CREAT) {
        __builtin_va_list argumentos;
        __builtin_va_start(argumentos, abrir_Configurações);
        concessão_Permissão = __builtin_va_arg(argumentos, mode_t);
        __builtin_va_end(argumentos);
    }
    return 호출결과(jkoros_syscall(30, (int)Arquivo_entrada_nome, abrir_Configurações, concessão_Permissão, 0, 0));
}
int creat(const char *Arquivo_entrada_nome, mode_t concessão_Permissão) { return open(Arquivo_entrada_nome, O_WRONLY | O_CREAT | O_TRUNC, concessão_Permissão); }
ssize_t read(int Arquivo_descritor, void *dados, size_t byte_CONT_NÚM) {
    return 호출결과(jkoros_syscall(31, Arquivo_descritor, (int)dados, byte_CONT_NÚM, 0, 0));
}
ssize_t write(int Arquivo_descritor, const void *dados, size_t byte_CONT_NÚM) {
    return 호출결과(jkoros_syscall(32, Arquivo_descritor, (int)dados, byte_CONT_NÚM, 0, 0));
}
int close(int Arquivo_descritor) { return 호출결과(jkoros_syscall(33, Arquivo_descritor, 0, 0, 0, 0)); }
off_t lseek(int Arquivo_descritor, off_t DESLOC_VALOR, int ação_raiz) {
    return 호출결과(jkoros_syscall(34, Arquivo_descritor, DESLOC_VALOR, ação_raiz, 0, 0));
}
int dup(int Arquivo_descritor) { return 호출결과(jkoros_syscall(35, Arquivo_descritor, 0, 0, 0, 0)); }
int dup2(int Arquivo_descritor, int 새서술자) { return 호출결과(jkoros_syscall(36, Arquivo_descritor, 새서술자, 0, 0, 0)); }
int fstat(int Arquivo_descritor, struct stat *Estado_VALOR) { return 호출결과(jkoros_syscall(37, Arquivo_descritor, (int)Estado_VALOR, 0, 0, 0)); }
int unlink(const char *Arquivo_entrada_nome) { return 호출결과(jkoros_syscall(38, (int)Arquivo_entrada_nome, 0, 0, 0, 0)); }
int ftruncate(int Arquivo_descritor, off_t byte_CONT_NÚM) { return 호출결과(jkoros_syscall(39, Arquivo_descritor, byte_CONT_NÚM, 0, 0, 0)); }
int fsync(int Arquivo_descritor) { return 호출결과(jkoros_syscall(47, Arquivo_descritor, 0, 0, 0, 0)); }
int fcntl(int Arquivo_descritor, int comando, ...) {
    int VALOR = 0;
    if (comando == F_DUPFD || comando == F_DUPFD_CLOEXEC || comando == F_SETFD || comando == F_SETFL) {
        __builtin_va_list argumentos;
        __builtin_va_start(argumentos, comando); VALOR = __builtin_va_arg(argumentos, int); __builtin_va_end(argumentos);
    }
    return 호출결과(jkoros_syscall(40, Arquivo_descritor, comando, VALOR, 0, 0));
}
