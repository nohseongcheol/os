#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define dateiÖffnen open
#define dateiErstellen creat
#define dateiDatenLesen read
#define dateiDatenSchreiben write
#define dateiSchließen close
#define dateiPositionieren lseek
#define duplikatDateiDeskriptor dup
#define duplikatDateiDeskriptorAnStelle dup2
#define dateiEintragNameEntfernen unlink
#define dateiLängeSetzen ftruncate
#define bestätigenDateiSpeichergerät fsync
#define dateiZustandLesen fstat
#define steuerungDateiDeskriptor fcntl
#define ausschließlichWertLesen O_RDONLY
#define ausschließlichWertSchreiben O_WRONLY
#define LesenSchreiben O_RDWR
#define ErstellenFallsFehlend O_CREAT
#define neuDateiErstellen (O_CREAT | O_EXCL)
#define KürzenInhalt O_TRUNC
#define anStelleEndeAnhängen O_APPEND
#define tunNichtBedingungWarten O_NONBLOCK
#define VonAnfang SEEK_SET
#define aktuellWurzel SEEK_CUR
#define endeUrsprung SEEK_END
#define dateiZustand stat
typedef size_t byteAnzahlTyp;
typedef ssize_t einAusgabeErgebnisTyp;
typedef off_t dateiVersatzwertTyp;
#endif
