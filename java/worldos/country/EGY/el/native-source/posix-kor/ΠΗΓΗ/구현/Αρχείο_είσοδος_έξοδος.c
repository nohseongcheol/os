#include <파일규약.h>
#include "καλώ_όριο.h"

int αριθμός_σφάλματος;
int 호출결과(int μέτρηση) {
    if (μέτρηση < 0) { αριθμός_σφάλματος = -μέτρηση; return -1; }
    return μέτρηση;
}
int open(const char *Αρχείο_καταχώρηση_όνομα, int ανοίγω_Ρυθμίσεις, ...) {
    mode_t 허가 = 0;
    if (ανοίγω_Ρυθμίσεις & O_CREAT) {
        __builtin_va_list Παράμετροι;
        __builtin_va_start(Παράμετροι, ανοίγω_Ρυθμίσεις);
        허가 = __builtin_va_arg(Παράμετροι, mode_t);
        __builtin_va_end(Παράμετροι);
    }
    return 호출결과(jkoros_syscall(30, (int)Αρχείο_καταχώρηση_όνομα, ανοίγω_Ρυθμίσεις, 허가, 0, 0));
}
int creat(const char *Αρχείο_καταχώρηση_όνομα, mode_t 허가) { return open(Αρχείο_καταχώρηση_όνομα, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *δεδομένα, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)δεδομένα, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *δεδομένα, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)δεδομένα, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Υπέρθεση_τιμή, int έργο_ρίζα) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Υπέρθεση_τιμή, έργο_ρίζα, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Κατάσταση_τιμή) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Κατάσταση_τιμή, 0, 0, 0)); }
int unlink(const char *Αρχείο_καταχώρηση_όνομα) { return 호출결과(jkoros_syscall(38, (int)Αρχείο_καταχώρηση_όνομα, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Εντολή, ...) {
    int τιμή = 0;
    if (Εντολή == F_DUPFD || Εντολή == F_DUPFD_CLOEXEC || Εντολή == F_SETFD || Εντολή == F_SETFL) {
        __builtin_va_list Παράμετροι;
        __builtin_va_start(Παράμετροι, Εντολή); τιμή = __builtin_va_arg(Παράμετροι, int); __builtin_va_end(Παράμετροι);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Εντολή, τιμή, 0, 0));
}
