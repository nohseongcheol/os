#include <DateiABI.h>
#include <stdio.h>
#include <string.h>
int main(int elementeintragAnzahl, char **eintragListe) {
    (void)elementeintragAnzahl; (void)eintragListe;
    char Daten[6]; int Länge = 0;
    puts("POSIX INPUT READY");
    while (Länge < 6) {
        int ergebnis = dateiDatenLesen(0, Daten + Länge, 6 - Länge);
        if (ergebnis <= 0) return 1;
        Länge += ergebnis;
    }
    if (memcmp(Daten, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
