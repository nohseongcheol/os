#include <DateiABI.h>
#include "AufrufVorgangGrenzstelle.h"

int fehlerNummer;
int aufrufErgebnis(int ergebnis) {
    if (ergebnis < 0) { fehlerNummer = -ergebnis; return -1; }
    return ergebnis;
}
int open(const char *dateiEintragName, int einstellungenÖffnen, ...) {
    mode_t erlaubnisGewähren = 0;
    if (einstellungenÖffnen & O_CREAT) {
        __builtin_va_list argumente;
        __builtin_va_start(argumente, einstellungenÖffnen);
        erlaubnisGewähren = __builtin_va_arg(argumente, mode_t);
        __builtin_va_end(argumente);
    }
    return aufrufErgebnis(jkoros_syscall(30, (int)dateiEintragName, einstellungenÖffnen, erlaubnisGewähren, 0, 0));
}
int creat(const char *dateiEintragName, mode_t erlaubnisGewähren) { return open(dateiEintragName, O_WRONLY | O_CREAT | O_TRUNC, erlaubnisGewähren); }
ssize_t read(int dateiDeskriptor, void *Daten, size_t byteAnzahl) {
    return aufrufErgebnis(jkoros_syscall(31, dateiDeskriptor, (int)Daten, byteAnzahl, 0, 0));
}
ssize_t write(int dateiDeskriptor, const void *Daten, size_t byteAnzahl) {
    return aufrufErgebnis(jkoros_syscall(32, dateiDeskriptor, (int)Daten, byteAnzahl, 0, 0));
}
int close(int dateiDeskriptor) { return aufrufErgebnis(jkoros_syscall(33, dateiDeskriptor, 0, 0, 0, 0)); }
off_t lseek(int dateiDeskriptor, off_t versatzwertWert, int projektWurzel) {
    return aufrufErgebnis(jkoros_syscall(34, dateiDeskriptor, versatzwertWert, projektWurzel, 0, 0));
}
int dup(int dateiDeskriptor) { return aufrufErgebnis(jkoros_syscall(35, dateiDeskriptor, 0, 0, 0, 0)); }
int dup2(int dateiDeskriptor, int neuDeskriptor) { return aufrufErgebnis(jkoros_syscall(36, dateiDeskriptor, neuDeskriptor, 0, 0, 0)); }
int fstat(int dateiDeskriptor, struct stat *statuswertWert) { return aufrufErgebnis(jkoros_syscall(37, dateiDeskriptor, (int)statuswertWert, 0, 0, 0)); }
int unlink(const char *dateiEintragName) { return aufrufErgebnis(jkoros_syscall(38, (int)dateiEintragName, 0, 0, 0, 0)); }
int ftruncate(int dateiDeskriptor, off_t byteAnzahl) { return aufrufErgebnis(jkoros_syscall(39, dateiDeskriptor, byteAnzahl, 0, 0, 0)); }
int fsync(int dateiDeskriptor) { return aufrufErgebnis(jkoros_syscall(47, dateiDeskriptor, 0, 0, 0, 0)); }
int fcntl(int dateiDeskriptor, int befehl, ...) {
    int Wert = 0;
    if (befehl == F_DUPFD || befehl == F_DUPFD_CLOEXEC || befehl == F_SETFD || befehl == F_SETFL) {
        __builtin_va_list argumente;
        __builtin_va_start(argumente, befehl); Wert = __builtin_va_arg(argumente, int); __builtin_va_end(argumente);
    }
    return aufrufErgebnis(jkoros_syscall(40, dateiDeskriptor, befehl, Wert, 0, 0));
}
