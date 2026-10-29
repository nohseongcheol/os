#include "DateiABI.h"
int benutzerProgrammStarten(int argumente) {
    (void)argumente;
    const char gruß[] = "C에서 한글 이름과 posix-kor aufrufen\n";
    int Dokumentation = dateiÖffnen("C인사.txt", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600);
    if (Dokumentation < 0) return 1;
    einAusgabeErgebnisTyp aufgezeichnetAnzahl = dateiDatenSchreiben(Dokumentation, gruß, sizeof(gruß) - 1);
    dateiSchließen(Dokumentation);
    dateiDatenSchreiben(1, gruß, sizeof(gruß) - 1);
    return aufgezeichnetAnzahl == sizeof(gruß) - 1 ? 0 : 2;
}
