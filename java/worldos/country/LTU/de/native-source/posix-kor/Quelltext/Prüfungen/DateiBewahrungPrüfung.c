#include <DateiABI.h>
#include <stdio.h>
int main(int elementeintragAnzahl, char **eintragListe) {
    (void)elementeintragAnzahl; (void)eintragListe;
    int Datei = dateiÖffnen("stored.txt", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
    if (Datei < 0 || dateiDatenSchreiben(Datei, "saved-from-C", 12) != 12) return 1;
    if (bestätigenDateiSpeichergerät(Datei) < 0) return 2;
    if (dateiSchließen(Datei) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
