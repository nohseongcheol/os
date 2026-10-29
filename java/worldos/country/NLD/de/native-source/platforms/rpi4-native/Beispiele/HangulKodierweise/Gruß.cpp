#include "DateiABI.h"
class DokumentVerwalter {
    int Nummer;
public:
    DokumentVerwalter(const char *Name) : Nummer(dateiÖffnen(Name, LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600)) {}
    ~DokumentVerwalter() { if (Nummer >= 0) dateiSchließen(Nummer); }
    einAusgabeErgebnisTyp schreiben(const char *Daten, byteAnzahlTyp größe) { return dateiDatenSchreiben(Nummer, Daten, größe); }
};
extern "C" int benutzerProgrammStarten(int argumente) {
    (void)argumente;
    const char gruß[] = "C++에서 한글 클래스와 posix-kor aufrufen\n";
    DokumentVerwalter Dokumentation("C++Gruß.txt");
    dateiDatenSchreiben(1, gruß, sizeof(gruß) - 1);
    return Dokumentation.schreiben(gruß, sizeof(gruß) - 1) == sizeof(gruß) - 1 ? 0 : 1;
}
