#include "DateiABI.h"
#include "aufrufen.h"
static int initialisiererWert;
static volatile int initialisiererStartwert = 72;
static volatile double fließendPunktStartwert = 1.25;
static int zerstörungAnzahl;
struct initialisierungPrüfung { initialisierungPrüfung() { initialisiererWert = initialisiererStartwert + 1; } } statischerBereichInitialisieren;
class automatischDatei {
    int Nummer;
public:
    explicit automatischDatei(const char *Name) : Nummer(dateiÖffnen(Name, LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600)) {}
    ~automatischDatei() { if (Nummer >= 0) dateiSchließen(Nummer); zerstörungAnzahl++; }
    int deskriptorEintrag() const { return Nummer; }
};
extern "C" int benutzerProgrammStarten(int) {
    if (initialisiererWert != 73 || benutzerAufrufen(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double fließendPunktWert = fließendPunktStartwert * 2.0 + 0.5;
    if (benutzerAufrufen(0, 0, 0, 0, 0, 0, 0) != 1 || fließendPunktWert != 3.0) return 16;
    static const char inhaltswertWert[] = "EL0 C++ → posix-kor → Java Datei · 안녕하세요 😀\n";
    char wertLesen[sizeof(inhaltswertWert)] = {};
    {
        automatischDatei Datei("Benutzer.txt");
        int Nummer = Datei.deskriptorEintrag();
        if (Nummer < 0 || dateiDatenSchreiben(Nummer, inhaltswertWert, sizeof(inhaltswertWert)) != sizeof(inhaltswertWert)) return 2;
        if (dateiPositionieren(Nummer, 0, VonAnfang) || dateiDatenLesen(Nummer, wertLesen, sizeof(wertLesen)) != sizeof(wertLesen)) return 3;
        for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(inhaltswertWert); ordnungszahlIndex++) if (wertLesen[ordnungszahlIndex] != inhaltswertWert[ordnungszahlIndex]) return 4;
    }
    if (zerstörungAnzahl != 1) return 5;
    if (dateiDatenSchreiben(1, inhaltswertWert, sizeof(inhaltswertWert) - 1) != sizeof(inhaltswertWert) - 1) return 6;
    uintptr_t unterkanteEintrag = benutzerSpeicherEnde(0);
    if (unterkanteEintrag != 0x02c00000 || benutzerSpeicherEnde(unterkanteEintrag + 8192) != (intptr_t)(unterkanteEintrag + 8192)) return 7;
    volatile unsigned char *Speicher = (volatile unsigned char *)unterkanteEintrag;
    if (Speicher[0] || Speicher[8191]) return 8;
    Speicher[8191] = 137;
    if (benutzerSpeicherEnde(unterkanteEintrag) != (intptr_t)unterkanteEintrag || benutzerSpeicherEnde(unterkanteEintrag + 8192) != (intptr_t)(unterkanteEintrag + 8192) || Speicher[8191]) return 9;
    // 잘못된 Benutzer zeiger/번호는 오류이며 커널을 중단하지 않는다.
    if (dateiDatenSchreiben(1, (const void *)0x80000, 8) != -1 || fehlerNummer != 14) return 10;
    if (dateiDatenLesen(0, (void *)inhaltswertWert, 1) != -1 || fehlerNummer != 14) return 11;
    if (benutzerAufrufen(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t bildschirmSpannweite = bildschirmBreiteLesen(), bildschirmLänge = bildschirmHöheLesen();
    if (bildschirmSpannweite <= 0 || bildschirmLänge <= 0 || benutzerAufrufen(13, bildschirmSpannweite-1, bildschirmLänge-1, 0, 2, 2, 0) != -22) return 13;
    if (bildschirmRechteck(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 verlassenProzessProgramm 시 열린 서술자가 자동 정리되어야 한다.
    if (dateiÖffnen("Benutzer.txt", ausschließlichWertLesen) < 0) return 15;
    return 0;
}
