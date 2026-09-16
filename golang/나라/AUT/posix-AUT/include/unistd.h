/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <Grunddefinitionen.h>
#include <System/Datentypen.h>

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define F_OK 0
#define X_OK 1
#define W_OK 2
#define R_OK 4
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void sofort_beenden(int Status) __attribute__((noreturn));
ssize_t lesen(int Dateideskriptor, void *Übertragungspuffer, size_t count);
ssize_t schreiben(int Dateideskriptor, const void *Übertragungspuffer, size_t count);
int schließen(int Dateideskriptor);
off_t Dateiposition_verschieben(int Dateideskriptor, off_t offset, int whence);
pid_t Prozess_verzweigen(void);
int Programmbild_ersetzen(const char *Pfad, char *const Argumente_2[], char *const envp[]);
pid_t Prozesskennung_ermitteln(void);
pid_t Elternprozesskennung_ermitteln(void);
uid_t Benutzerkennung_ermitteln(void);
uid_t wirksame_Benutzerkennung_ermitteln(void);
gid_t Gruppenkennung_ermitteln(void);
gid_t wirksame_Gruppenkennung_ermitteln(void);
int Zugriffsrechte_prüfen(const char *Pfad, int mode);
int Arbeitsverzeichnis_wechseln(const char *Pfad);
char *Arbeitsverzeichnispfad_ermitteln(char *Übertragungspuffer, size_t Ziffernanzahl);
int offenen_Dateiverweis_duplizieren(int Dateideskriptor);
int Dateiverweis_auf_Kennung_duplizieren(int oldfd, int newfd);
int Dateidaten_synchronisieren(int Dateideskriptor);
void alle_Dateidaten_synchronisieren(void);
int Terminal_prüfen(int Dateideskriptor);
int Speicherende_setzen(void *address);
void *Speicherende_verschieben(int increment);
#ifdef __cplusplus
}
#endif

#endif
