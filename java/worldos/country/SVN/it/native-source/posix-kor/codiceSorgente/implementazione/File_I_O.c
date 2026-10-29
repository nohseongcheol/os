#include <File_ABI.h>
#include "Chiama_limite.h"

int numero_errore;
int 호출결과(int risultato) {
    if (risultato < 0) { numero_errore = -risultato; return -1; }
    return risultato;
}
int open(const char *File_voce_nome, int aperto_Impostazioni, ...) {
    mode_t concessione_privilegio = 0;
    if (aperto_Impostazioni & O_CREAT) {
        __builtin_va_list argomenti;
        __builtin_va_start(argomenti, aperto_Impostazioni);
        concessione_privilegio = __builtin_va_arg(argomenti, mode_t);
        __builtin_va_end(argomenti);
    }
    return 호출결과(jkoros_syscall(30, (int)File_voce_nome, aperto_Impostazioni, concessione_privilegio, 0, 0));
}
int creat(const char *File_voce_nome, mode_t concessione_privilegio) { return open(File_voce_nome, O_WRONLY | O_CREAT | O_TRUNC, concessione_privilegio); }
ssize_t read(int File_descrittore, void *dati, size_t byte_CONTA_NUMERI) {
    return 호출결과(jkoros_syscall(31, File_descrittore, (int)dati, byte_CONTA_NUMERI, 0, 0));
}
ssize_t write(int File_descrittore, const void *dati, size_t byte_CONTA_NUMERI) {
    return 호출결과(jkoros_syscall(32, File_descrittore, (int)dati, byte_CONTA_NUMERI, 0, 0));
}
int close(int File_descrittore) { return 호출결과(jkoros_syscall(33, File_descrittore, 0, 0, 0, 0)); }
off_t lseek(int File_descrittore, off_t SCARTO_VALORE, int azione_radice) {
    return 호출결과(jkoros_syscall(34, File_descrittore, SCARTO_VALORE, azione_radice, 0, 0));
}
int dup(int File_descrittore) { return 호출결과(jkoros_syscall(35, File_descrittore, 0, 0, 0, 0)); }
int dup2(int File_descrittore, int 새서술자) { return 호출결과(jkoros_syscall(36, File_descrittore, 새서술자, 0, 0, 0)); }
int fstat(int File_descrittore, struct stat *Stato_VALORE) { return 호출결과(jkoros_syscall(37, File_descrittore, (int)Stato_VALORE, 0, 0, 0)); }
int unlink(const char *File_voce_nome) { return 호출결과(jkoros_syscall(38, (int)File_voce_nome, 0, 0, 0, 0)); }
int ftruncate(int File_descrittore, off_t byte_CONTA_NUMERI) { return 호출결과(jkoros_syscall(39, File_descrittore, byte_CONTA_NUMERI, 0, 0, 0)); }
int fsync(int File_descrittore) { return 호출결과(jkoros_syscall(47, File_descrittore, 0, 0, 0, 0)); }
int fcntl(int File_descrittore, int comando, ...) {
    int VALORE = 0;
    if (comando == F_DUPFD || comando == F_DUPFD_CLOEXEC || comando == F_SETFD || comando == F_SETFL) {
        __builtin_va_list argomenti;
        __builtin_va_start(argomenti, comando); VALORE = __builtin_va_arg(argomenti, int); __builtin_va_end(argomenti);
    }
    return 호출결과(jkoros_syscall(40, File_descrittore, comando, VALORE, 0, 0));
}
