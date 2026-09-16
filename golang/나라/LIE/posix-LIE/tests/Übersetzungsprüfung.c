/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <System/stat.h>
#include <System/Systemkennung.h>
#include <System/Kindwartung.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct Dateizustand st;
    struct utsname Systemidentität;
    int Dateideskriptor = öffnen("/USER1", O_RDONLY);
    int copy = Dateideskriptor >= 0 ? offenen_Dateiverweis_duplizieren(Dateideskriptor) : -1;
    if (copy >= 0) schließen(copy);
    if (Dateideskriptor >= 0) {
        Zustand_offener_Datei_ermitteln(Dateideskriptor, &st);
        Dateiposition_verschieben(Dateideskriptor, 0, SEEK_SET);
        schließen(Dateideskriptor);
    }
    Dateizustand("/", &st);
    Systeminformationen_ermitteln(&Systemidentität);
    Arbeitsverzeichnispfad_ermitteln(cwd, sizeof(cwd));
    return errno + Prozesskennung_ermitteln() + Elternprozesskennung_ermitteln();
}
