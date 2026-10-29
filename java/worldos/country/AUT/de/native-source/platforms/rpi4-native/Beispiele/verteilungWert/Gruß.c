#include <DateiABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int argumenteAnzahl, char **argumentListe) {
    if (argumenteAnzahl < 1 || !argumentListe[0]) return 2;
    const char gruß[] = "eigen 커널의 C와 Deutsch POSIX\n";
    int Dokumentation = dateiÖffnen("Gruß.txt", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
    if (Dokumentation < 0) return 1;
    einAusgabeErgebnisTyp Länge = dateiDatenSchreiben(Dokumentation, gruß, sizeof(gruß) - 1);
    dateiSchließen(Dokumentation);
    dateiDatenSchreiben(1, gruß, sizeof(gruß) - 1);
    return Länge == sizeof(gruß) - 1 ? 0 : 3;
}
