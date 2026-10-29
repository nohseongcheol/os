#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t einAusgabeErgebnisTyp;
typedef size_t byteAnzahlTyp;
typedef int64_t dateiVersatzwertTyp;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
einAusgabeErgebnisTyp pk_read(int fd, void *buffer, size_t count);
einAusgabeErgebnisTyp pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
dateiVersatzwertTyp pk_lseek(int fd, dateiVersatzwertTyp offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, dateiVersatzwertTyp size);
int pk_fsync(int fd);
int pk_size(int fd);
int dateiÖffnen(const char *pfad, int methodeBetriebsart, ...);
einAusgabeErgebnisTyp dateiDatenLesen(int Datei, void *Daten, size_t elementeintragAnzahl);
einAusgabeErgebnisTyp dateiDatenSchreiben(int Datei, const void *Daten, size_t elementeintragAnzahl);
int dateiSchließen(int Datei);
dateiVersatzwertTyp dateiPositionieren(int Datei, dateiVersatzwertTyp entfernungWert, int projektWurzel);
int dateiEintragNameEntfernen(const char *pfad);
int dateiLängeSetzen(int Datei, dateiVersatzwertTyp größe);
int bestätigenDateiSpeichergerät(int Datei);
int dateiGröße(int Datei);
#ifdef __cplusplus
}
#endif
#define fehlerNummer (*pk_errno_location())
#define ausschließlichWertLesen 0
#define ausschließlichWertSchreiben 1
#define LesenSchreiben 2
#define ErstellenFallsFehlend 0x40
#define neuDateiErstellen 0xc0
#define KürzenInhalt 0x200
#define anStelleEndeAnhängen 0x400
#define VonAnfang 0
#define aktuellWurzel 1
#define endeUrsprung 2
#endif
