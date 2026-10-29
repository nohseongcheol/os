#include <ABIArchivo.h>
#include "FronteraLlamada.h"

int númeroError;
int resultadoInvocación(int resultado) {
    if (resultado < 0) { númeroError = -resultado; return -1; }
    return resultado;
}
int open(const char *nombreEntradaElementoArchivo, int abrirAjustes, ...) {
    mode_t concederPermiso = 0;
    if (abrirAjustes & O_CREAT) {
        __builtin_va_list argumentos;
        __builtin_va_start(argumentos, abrirAjustes);
        concederPermiso = __builtin_va_arg(argumentos, mode_t);
        __builtin_va_end(argumentos);
    }
    return resultadoInvocación(jkoros_syscall(30, (int)nombreEntradaElementoArchivo, abrirAjustes, concederPermiso, 0, 0));
}
int creat(const char *nombreEntradaElementoArchivo, mode_t concederPermiso) { return open(nombreEntradaElementoArchivo, O_WRONLY | O_CREAT | O_TRUNC, concederPermiso); }
ssize_t read(int descriptorArchivo, void *Datos, size_t númeroElementosByte) {
    return resultadoInvocación(jkoros_syscall(31, descriptorArchivo, (int)Datos, númeroElementosByte, 0, 0));
}
ssize_t write(int descriptorArchivo, const void *Datos, size_t númeroElementosByte) {
    return resultadoInvocación(jkoros_syscall(32, descriptorArchivo, (int)Datos, númeroElementosByte, 0, 0));
}
int close(int descriptorArchivo) { return resultadoInvocación(jkoros_syscall(33, descriptorArchivo, 0, 0, 0, 0)); }
off_t lseek(int descriptorArchivo, off_t valorDesfase, int raízProyecto) {
    return resultadoInvocación(jkoros_syscall(34, descriptorArchivo, valorDesfase, raízProyecto, 0, 0));
}
int dup(int descriptorArchivo) { return resultadoInvocación(jkoros_syscall(35, descriptorArchivo, 0, 0, 0, 0)); }
int dup2(int descriptorArchivo, int descriptorNuevo) { return resultadoInvocación(jkoros_syscall(36, descriptorArchivo, descriptorNuevo, 0, 0, 0)); }
int fstat(int descriptorArchivo, struct stat *valorEstadoValor) { return resultadoInvocación(jkoros_syscall(37, descriptorArchivo, (int)valorEstadoValor, 0, 0, 0)); }
int unlink(const char *nombreEntradaElementoArchivo) { return resultadoInvocación(jkoros_syscall(38, (int)nombreEntradaElementoArchivo, 0, 0, 0, 0)); }
int ftruncate(int descriptorArchivo, off_t númeroElementosByte) { return resultadoInvocación(jkoros_syscall(39, descriptorArchivo, númeroElementosByte, 0, 0, 0)); }
int fsync(int descriptorArchivo) { return resultadoInvocación(jkoros_syscall(47, descriptorArchivo, 0, 0, 0, 0)); }
int fcntl(int descriptorArchivo, int comando, ...) {
    int valor = 0;
    if (comando == F_DUPFD || comando == F_DUPFD_CLOEXEC || comando == F_SETFD || comando == F_SETFL) {
        __builtin_va_list argumentos;
        __builtin_va_start(argumentos, comando); valor = __builtin_va_arg(argumentos, int); __builtin_va_end(argumentos);
    }
    return resultadoInvocación(jkoros_syscall(40, descriptorArchivo, comando, valor, 0, 0));
}
