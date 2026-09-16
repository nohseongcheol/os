/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <System/stat.h>
#include <System/Kindwartung.h>
#include <unistd.h>
#include <System/syscall.h>

enum {
    SYS_sofort_beenden = 1,
    SYS_Prozess_verzweigen = 2,
    SYS_lesen = 3,
    SYS_schreiben = 4,
    SYS_schließen = 6,
    SYS_Programmbild_ersetzen = 11,
    SYS_Arbeitsverzeichnis_wechseln = 12,
    SYS_Dateiposition_verschieben = 19,
    SYS_Prozesskennung_ermitteln = 20,
    SYS_Benutzerkennung_ermitteln = 24,
    SYS_Zugriffsrechte_prüfen = 33,
    SYS_alle_Dateidaten_synchronisieren = 36,
    SYS_offenen_Dateiverweis_duplizieren = 41,
    SYS_Speicherende_setzen = 45,
    SYS_Gruppenkennung_ermitteln = 47,
    SYS_wirksame_Benutzerkennung_ermitteln = 49,
    SYS_wirksame_Gruppenkennung_ermitteln = 50,
    SYS_Dateiverweis_auf_Kennung_duplizieren = 63,
    SYS_Elternprozesskennung_ermitteln = 64,
    SYS_Dateidaten_synchronisieren = 118,
    SYS_Arbeitsverzeichnispfad_ermitteln = 183
};

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void sofort_beenden(int Status)
{
    SC1(SYS_sofort_beenden, Status);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t lesen(int Dateideskriptor, void *Übertragungspuffer, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_lesen, Dateideskriptor, Übertragungspuffer, count));
}

ssize_t schreiben(int Dateideskriptor, const void *Übertragungspuffer, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_schreiben, Dateideskriptor, Übertragungspuffer, count));
}

int schließen(int Dateideskriptor)
{
    return (int)__syscall_result(SC1(SYS_schließen, Dateideskriptor));
}

off_t Dateiposition_verschieben(int Dateideskriptor, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_Dateiposition_verschieben, Dateideskriptor, offset, whence));
}

pid_t Prozess_verzweigen(void)
{
    return (pid_t)__syscall_result(SC0(SYS_Prozess_verzweigen));
}

int Programmbild_ersetzen(const char *Pfad, char *const Argumente_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_Programmbild_ersetzen, Pfad, Argumente_2, envp));
}

pid_t Prozesskennung_ermitteln(void) { return (pid_t)SC0(SYS_Prozesskennung_ermitteln); }
pid_t Elternprozesskennung_ermitteln(void) { return (pid_t)SC0(SYS_Elternprozesskennung_ermitteln); }
uid_t Benutzerkennung_ermitteln(void) { return (uid_t)SC0(SYS_Benutzerkennung_ermitteln); }
uid_t wirksame_Benutzerkennung_ermitteln(void) { return (uid_t)SC0(SYS_wirksame_Benutzerkennung_ermitteln); }
gid_t Gruppenkennung_ermitteln(void) { return (gid_t)SC0(SYS_Gruppenkennung_ermitteln); }
gid_t wirksame_Gruppenkennung_ermitteln(void) { return (gid_t)SC0(SYS_wirksame_Gruppenkennung_ermitteln); }

int Zugriffsrechte_prüfen(const char *Pfad, int mode)
{
    return (int)__syscall_result(SC2(SYS_Zugriffsrechte_prüfen, Pfad, mode));
}

int Arbeitsverzeichnis_wechseln(const char *Pfad)
{
    return (int)__syscall_result(SC1(SYS_Arbeitsverzeichnis_wechseln, Pfad));
}

char *Arbeitsverzeichnispfad_ermitteln(char *Übertragungspuffer, size_t Ziffernanzahl)
{
    long result = __syscall_result(SC2(SYS_Arbeitsverzeichnispfad_ermitteln, Übertragungspuffer, Ziffernanzahl));
    return result < 0 ? (char *)0 : Übertragungspuffer;
}

int offenen_Dateiverweis_duplizieren(int Dateideskriptor)
{
    return (int)__syscall_result(SC1(SYS_offenen_Dateiverweis_duplizieren, Dateideskriptor));
}

int Dateiverweis_auf_Kennung_duplizieren(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_Dateiverweis_auf_Kennung_duplizieren, oldfd, newfd));
}

int Dateidaten_synchronisieren(int Dateideskriptor)
{
    return (int)__syscall_result(SC1(SYS_Dateidaten_synchronisieren, Dateideskriptor));
}

void alle_Dateidaten_synchronisieren(void)
{
    SC0(SYS_alle_Dateidaten_synchronisieren);
}

int Terminal_prüfen(int Dateideskriptor)
{
    struct Dateizustand st;
    if (Zustand_offener_Datei_ermitteln(Dateideskriptor, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int Speicherende_setzen(void *address)
{
    long result = SC1(SYS_Speicherende_setzen, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *Speicherende_verschieben(int increment)
{
    long current = SC1(SYS_Speicherende_setzen, 0);
    long requested = current + increment;
    if (increment != 0 && Speicherende_setzen((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t bestimmtes_Kind_abwarten(pid_t pid, int *Status, int options)
{
    long result;
    do {
        result = SC3(7, pid, Status, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t Kind_abwarten(int *Status)
{
    return bestimmtes_Kind_abwarten(-1, Status, 0);
}
