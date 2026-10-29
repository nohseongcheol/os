#include "../benennung/maschineBindenNamen.h"
#include "bildschirmInformation.h"
// EL0 befehlAusführen maschine schichtWert. Datei Daten/정책은 기존 AOT Java 커널에 위임한다.
#include "Benutzer.h"
#include "DateiABI.h"
#include "NetzwerkABI.h"
#include "../Netzwerkstapel/Netzwerkstapel.h"
extern int32_t javaNetzEntfernt(int32_t), javaDatenstromAdresse(int32_t);
#define maschineRegister(ersterWert) (*(volatile uint32_t *)(uintptr_t)(ersterWert))
#define unterbrechenVerteiler 0xff841000ul
#define unterbrechenCPUSchnittstelle 0xff842000ul
#define seiteGröße 4096ul
#define zugriffMarkierung (1ul << 10)
#define keinAusführenErlaubnis (1ul << 53)
#define benutzerKeinAusführen (1ul << 54)
#define normalSpeicher ((1ul << 2) | (3ul << 8) | zugriffMarkierung)
#define betriebskernSeite (3ul | normalSpeicher | keinAusführenErlaubnis | benutzerKeinAusführen)
#define benutzerLesenSchreiben (3ul | normalSpeicher | (1ul << 6) | keinAusführenErlaubnis | benutzerKeinAusführen)
#define benutzerLesenAusschließlich (3ul | normalSpeicher | (3ul << 6) | keinAusführenErlaubnis | benutzerKeinAusführen)
#define benutzerLesenAusführen (3ul | normalSpeicher | (3ul << 6) | keinAusführenErlaubnis)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t platineZeichenSchreiben(uintptr_t), platineZeichenHolen(void), platineVergangeneMillisekunden(void);
extern uintptr_t platineBildpunkt(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t platineBildpuffer(void);
extern uintptr_t platineTerminal(uintptr_t);
extern int terminalAusstehend(void);
extern int32_t javaKonsoleInteraktiv(void);
extern int32_t javaPfadStarten(int32_t), javaPfadByte(int32_t,int32_t);
extern int32_t javaErstellenVerzeichnis(void), javaEntfernenVerzeichnis(void), javaEintragArt(void);
extern int bildschirmAufrufen(int,unsigned,int,int,int,int,int),bildschirmText(int,int,const uint32_t *,unsigned);
extern void bildschirmInitialisieren(int),bildschirmDrücken(int,unsigned);
extern int benutzerFortführen(benutzerRahmen *,void *);
extern void benutzerGleitkommaSpeichern(void *);
extern int benutzerEintreten(uintptr_t eintragPunkt, uintptr_t stapelSpeichergerät, uintptr_t weitergeleitetWert);
extern void benutzerZurückkehren(void);
extern void betriebskernNotstopp(const char *) __attribute__((noreturn));
static uint64_t wurzelAdresse[512] __attribute__((aligned(4096)));
static uint64_t mitte[4][512] __attribute__((aligned(4096)));
static uint64_t seiteListe[benutzerSeiteAnzahl] __attribute__((aligned(4096)));
static uint8_t erlaubnisseListe[benutzerSeiteAnzahl];
static int aktiv, dateiListe[16], linuxABI;
static unsigned netzbuchseEndpunkte[24];
extern int32_t javaNetzNetzbuchse(int32_t, int32_t, int32_t), javaNetzZuordnen(int32_t, int32_t, int32_t);
extern int32_t javaNetzAblegen(int32_t, int32_t), javaNetzHolen(int32_t), javaNetzSenden(int32_t, int32_t, int32_t, int32_t);
extern int32_t javaNetzEmpfangsvorgang(int32_t, int32_t), javaNetzPort(int32_t), javaNetzAdresse(int32_t), javaNetzGegenstelle(int32_t), javaNetzSchließen(int32_t);
extern int32_t javaDatenstromErstellen(void),javaDatenstromZuordnen(int32_t,int32_t,int32_t),javaDatenstromLauschen(int32_t,int32_t),javaDatenstromVerbinden(int32_t,int32_t,int32_t),javaDatenstromAnnehmen(int32_t),javaDatenstromLesen(int32_t,int32_t),javaDatenstromSchreiben(int32_t,int32_t),javaDatenstromPort(int32_t),javaDatenstromGegenstelle(int32_t),javaDatenstromSchließen(int32_t);
static int netzbuchseEndpunktSchließen(unsigned dateiKennwert){return dateiKennwert<40?javaNetzSchließen(dateiKennwert):javaDatenstromSchließen(dateiKennwert);}
static uint64_t frequenz, fristZeit;
static uintptr_t speicherhaldeEnde;
// betriebskernWert 셸이 준비한 UTF-8 argumente. EL0에는 wertKopieren 호출만 제공한다.
static unsigned weitergeleitetArgumentAnzahl, weitergeleitetArgumentLänge[8];
static unsigned char weitergeleitetArgument[8][256];
typedef struct {
    int pausiertStatuswert,interaktiv,linuxABI,dateiListe[16]; unsigned netzbuchseEndpunkte[24],argumenteAnzahl,argumentlänge[8];
    unsigned char argumentDatenfeld[8][256],erlaubnisseListe[benutzerSeiteAnzahl];
    uintptr_t speicherhaldeSpeichergerät; benutzerRahmen ausführungRahmen;
    unsigned char fließendPunktStatuswert[528] __attribute__((aligned(16)));
} gespeichertProzess;
static gespeichertProzess gespeichert[4];
static int eigentümerObjekt,interaktiv;
static uint32_t benutzerNummer[4], benutzerStartenZeit[4], benutzerAngesammeltZeit[4], benutzerAusführungZeit[4], nächsterBenutzerNummer=10;
static unsigned char benutzerBefehlName[4][288];
uint32_t benutzerStatuswertLesen(unsigned eintragWert, unsigned Nummer) {
    unsigned positionIndex=Nummer&3;
    int statuswertWert=(aktiv && eigentümerObjekt==(int)positionIndex) ? 1 : gespeichert[positionIndex].pausiertStatuswert ? 2 : 0;
    if (eintragWert==0) return statuswertWert;
    if (!statuswertWert) return 0;
    if (eintragWert==1) return benutzerNummer[positionIndex];
    if (eintragWert==2) {
        unsigned char *seitenListe=statuswertWert==1?erlaubnisseListe:gespeichert[positionIndex].erlaubnisseListe;
        unsigned seiteAnzahl=0; for (unsigned ordnungszahlIndex=0; ordnungszahlIndex<benutzerSeiteAnzahl; ordnungszahlIndex++) if(seitenListe[ordnungszahlIndex]) seiteAnzahl++;
        return seiteAnzahl*4;
    }
    if (eintragWert==3) return (uint32_t)platineVergangeneMillisekunden()-benutzerStartenZeit[positionIndex];
    if (eintragWert==4) return benutzerAngesammeltZeit[positionIndex]+(statuswertWert==1?(uint32_t)platineVergangeneMillisekunden()-benutzerAusführungZeit[positionIndex]:0);
    if (eintragWert==5) return Nummer/4<sizeof(benutzerBefehlName[0])?benutzerBefehlName[positionIndex][Nummer/4]:0;
    return 0;
}
uintptr_t platineAufrufargumenteBeginn(uintptr_t eintragAnzahl) {
    if (aktiv || eintragAnzahl > 8) return (uint32_t)-22;
    weitergeleitetArgumentAnzahl = eintragAnzahl;
    memset(weitergeleitetArgumentLänge, 0, sizeof(weitergeleitetArgumentLänge));
    memset(weitergeleitetArgument, 0, sizeof(weitergeleitetArgument));
    return 0;
}
uintptr_t platineAufrufargumenteByte(uintptr_t nachschlagenIndex, uintptr_t aktuellPosition, uintptr_t byteDaten) {
    if (aktiv || nachschlagenIndex >= weitergeleitetArgumentAnzahl || aktuellPosition >= 255 || aktuellPosition != weitergeleitetArgumentLänge[nachschlagenIndex] || !byteDaten || byteDaten > 255)
        return (uint32_t)-22;
    weitergeleitetArgument[nachschlagenIndex][aktuellPosition] = byteDaten;
    weitergeleitetArgumentLänge[nachschlagenIndex] = aktuellPosition + 1;
    return 0;
}
static void abgleichenTabellen(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t uhrWert(void) { uint64_t vorläufigDaten; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(vorläufigDaten)); return vorläufigDaten; }
static void zeitüberschreitungStoppen(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    maschineRegister(unterbrechenVerteiler + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void zeitüberschreitungStarten(void) {
    uint64_t abstandWert = frequenz * 2, aktivieren = 1;
    fristZeit = uhrWert() + abstandWert;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(abstandWert), "r"(aktivieren) : "memory");
}
void benutzerSystemInitialisierungsvorgang(void) {
    for (unsigned datenBlock = 0; datenBlock < 4; datenBlock++) {
        wurzelAdresse[datenBlock] = (uintptr_t)mitte[datenBlock] | 3;
        for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < 512; ordnungszahlIndex++) {
            uintptr_t adresse = ((uintptr_t)datenBlock << 30) | ((uintptr_t)ordnungszahlIndex << 21);
            mitte[datenBlock][ordnungszahlIndex] = adresse | 1 | zugriffMarkierung | benutzerKeinAusführen;
            if (adresse >= 0xfc000000ul) mitte[datenBlock][ordnungszahlIndex] |= keinAusführenErlaubnis; // Device-nGnRnE
            else mitte[datenBlock][ordnungszahlIndex] |= normalSpeicher; // Normal, non-cacheable
        }
    }
    for (unsigned zweiterWert = 0; zweiterWert < benutzerSeiteAnzahl / 512; zweiterWert++)
        mitte[0][(benutzerBasis >> 21) + zweiterWert] = (uintptr_t)(seiteListe + zweiterWert * 512) | 3;
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < benutzerSeiteAnzahl; ordnungszahlIndex++) seiteListe[ordnungszahlIndex] = (benutzerBasis + ordnungszahlIndex * seiteGröße) | betriebskernSeite;
    uint64_t speicherAttributRegister = 0x4400, adresseÜbersetzungSteuerung = 32 | (3ul << 12) | (1ul << 23), systemsteuerregister;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(speicherAttributRegister), "r"(adresseÜbersetzungSteuerung), "r"((uintptr_t)wurzelAdresse) : "memory");
    abgleichenTabellen();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(systemsteuerregister));
    systemsteuerregister = (systemsteuerregister & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(systemsteuerregister) : "memory");
    uint64_t fließendPunktStatuswert = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(fließendPunktStatuswert) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(frequenz));
    zeitüberschreitungStoppen();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 eintragPunktWert 때만 wertErlauben.
    maschineRegister(unterbrechenVerteiler) = 0;
    maschineRegister(unterbrechenVerteiler + 0x180) = 0xffffffff;
    maschineRegister(unterbrechenVerteiler + 0x80) = 0xffffffff;
    maschineRegister(unterbrechenVerteiler + 0x280) = 1u << 30;
    maschineRegister(unterbrechenVerteiler + 0x41c) = 0x80808080;
    maschineRegister(unterbrechenVerteiler + 0x100) = 1u << 30;
    maschineRegister(unterbrechenCPUSchnittstelle + 4) = 0xff;
    maschineRegister(unterbrechenCPUSchnittstelle + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 istNormal 확인할 Zahl 있다.
    int sicherheit = (maschineRegister(unterbrechenVerteiler + 4) & (1u << 10)) != 0;
    maschineRegister(unterbrechenVerteiler) = sicherheit ? 1 : 3;
    maschineRegister(unterbrechenCPUSchnittstelle) = sicherheit ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char kennung[16]; uint16_t typKategorie, maschineTyp; uint32_t versionNummer;
    uint64_t eintragPunkt, programmKopfVersatzwert, abschnittKopfVersatzwert; uint32_t konfigurationBitliste;
    uint16_t ausführdateiKopfGröße, programmKopfEintragGröße, programmKopfAnzahl, abschnittKopfEintragGröße, abschnittKopfAnzahl, abschnittNameTabelleIndex;
} eLFKopf;
typedef struct { uint32_t typKategorie, konfigurationBitliste; uint64_t versatzwertWert, adresse, physischAdresse, dateibereichsgröße, speicherbereichsgröße, ausrichtenGrenzstelle; } eLFProgramm;
_Static_assert(sizeof(eLFKopf) == 64 && sizeof(eLFProgramm) == 56, "ELF layout");
_Static_assert(sizeof(benutzerRahmen) == 272, "exception assembly layout");
static int enthalten(uint64_t versatzwertWert, uint64_t größe, uint64_t endeVersatzwert) {
    return versatzwertWert <= endeVersatzwert && größe <= endeVersatzwert - versatzwertWert;
}
static int hilfsInformationPrüfen(const unsigned char *datenPosition, size_t größe) {
    size_t aktuellPosition = 0;
    while (enthalten(aktuellPosition, 12, größe)) {
        uint32_t lexikalischWörter[3]; memcpy(lexikalischWörter, datenPosition + aktuellPosition, 12); aktuellPosition += 12;
        uint64_t namensbereichsgröße = ((uint64_t)lexikalischWörter[0] + 3) & ~3ul;
        uint64_t beschreibungsgröße = ((uint64_t)lexikalischWörter[1] + 3) & ~3ul;
        if (!enthalten(aktuellPosition, namensbereichsgröße, größe) || !enthalten(aktuellPosition + namensbereichsgröße, beschreibungsgröße, größe)) return 0;
        const unsigned char Name[] = {'J','K','O','R','O','S',0};
        int istGleich = lexikalischWörter[0] == sizeof(Name) && lexikalischWörter[1] == 4 && lexikalischWörter[2] == 1;
        if (istGleich) for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(Name); ordnungszahlIndex++) if (datenPosition[aktuellPosition + ordnungszahlIndex] != Name[ordnungszahlIndex]) istGleich = 0;
        uint32_t versionNummer = 0;
        if (istGleich) memcpy(&versionNummer, datenPosition + aktuellPosition + namensbereichsgröße, 4);
        if (istGleich && versionNummer == 1) return 1;
        aktuellPosition += namensbereichsgröße + beschreibungsgröße;
    }
    return 0;
}
static int eLFValidieren(const unsigned char *Daten, size_t größe, int linuxBetriebsart) {
    if (größe < sizeof(eLFKopf)) return benutzerAusführdateiFehler;
    eLFKopf ausführdateiKopf; memcpy(&ausführdateiKopf, Daten, sizeof(ausführdateiKopf));
    if (ausführdateiKopf.kennung[0] != 127 || ausführdateiKopf.kennung[1] != 'E' || ausführdateiKopf.kennung[2] != 'L' || ausführdateiKopf.kennung[3] != 'F' ||
        ausführdateiKopf.kennung[4] != 2 || ausführdateiKopf.kennung[5] != 1 || ausführdateiKopf.kennung[6] != 1 || (ausführdateiKopf.kennung[7] != 0 && (!linuxBetriebsart || ausführdateiKopf.kennung[7] != 3)) ||
        ausführdateiKopf.typKategorie != 2 || ausführdateiKopf.maschineTyp != 183 || ausführdateiKopf.versionNummer != 1 || ausführdateiKopf.konfigurationBitliste || ausführdateiKopf.ausführdateiKopfGröße != sizeof(ausführdateiKopf) ||
        ausführdateiKopf.programmKopfEintragGröße != sizeof(eLFProgramm) || !ausführdateiKopf.programmKopfAnzahl || ausführdateiKopf.programmKopfAnzahl > 16 ||
        ausführdateiKopf.programmKopfVersatzwert < sizeof(ausführdateiKopf) || !enthalten(ausführdateiKopf.programmKopfVersatzwert, (uint64_t)ausführdateiKopf.programmKopfAnzahl * sizeof(eLFProgramm), größe)) return benutzerAusführdateiFehler;
    uint8_t benutztKapazität[(benutzerAbbildEnde - benutzerBasis) / seiteGröße] = {0};
    int gültigEintragPunkt = 0, aBIInOrdnung = 0, ladeeinträge = 0;
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < ausführdateiKopf.programmKopfAnzahl; ordnungszahlIndex++) {
        eLFProgramm datenPosition; memcpy(&datenPosition, Daten + ausführdateiKopf.programmKopfVersatzwert + ordnungszahlIndex * sizeof(datenPosition), sizeof(datenPosition));
        if (datenPosition.typKategorie == 4) {
            if (!enthalten(datenPosition.versatzwertWert, datenPosition.dateibereichsgröße, größe)) return benutzerAusführdateiFehler;
            if (hilfsInformationPrüfen(Daten + datenPosition.versatzwertWert, datenPosition.dateibereichsgröße)) aBIInOrdnung = 1;
            continue;
        }
        if (datenPosition.typKategorie == 0 || datenPosition.typKategorie == 6 || (datenPosition.typKategorie == 0x6474e551 && !(datenPosition.konfigurationBitliste & 1))) continue;
        if (datenPosition.typKategorie != 1) return benutzerAusführdateiFehler; // PT_INTERP, DYNAMIC, TLS istNichtUnterstützt
        if (!datenPosition.speicherbereichsgröße) continue;
        if (datenPosition.konfigurationBitliste & ~7u || !(datenPosition.konfigurationBitliste & 4) || (datenPosition.konfigurationBitliste & 3) == 3 || datenPosition.dateibereichsgröße > datenPosition.speicherbereichsgröße ||
            (datenPosition.dateibereichsgröße && !enthalten(datenPosition.versatzwertWert, datenPosition.dateibereichsgröße, größe)) || datenPosition.adresse < benutzerBasis ||
            !enthalten(datenPosition.adresse, datenPosition.speicherbereichsgröße, benutzerAbbildEnde) ||
            (!linuxBetriebsart && ((datenPosition.adresse & (seiteGröße - 1)) || (datenPosition.versatzwertWert & (seiteGröße - 1)) || datenPosition.ausrichtenGrenzstelle != seiteGröße)) ||
            (linuxBetriebsart && (((datenPosition.adresse ^ datenPosition.versatzwertWert) & (seiteGröße - 1)) || !datenPosition.ausrichtenGrenzstelle ||
                (datenPosition.ausrichtenGrenzstelle & (datenPosition.ausrichtenGrenzstelle - 1)) || datenPosition.ausrichtenGrenzstelle > 0x200000 || ((datenPosition.adresse ^ datenPosition.versatzwertWert) & (datenPosition.ausrichtenGrenzstelle - 1))))) return benutzerAusführdateiFehler;
        unsigned ersterEintrag = (datenPosition.adresse - benutzerBasis) / seiteGröße;
        unsigned eintragAnzahl = ((datenPosition.adresse & (seiteGröße - 1)) + datenPosition.speicherbereichsgröße + seiteGröße - 1) / seiteGröße;
        for (unsigned seiteWert = ersterEintrag; seiteWert < ersterEintrag + eintragAnzahl; seiteWert++) {
            if (benutztKapazität[seiteWert]) return benutzerAusführdateiFehler;
            benutztKapazität[seiteWert] = 1;
        }
        if ((datenPosition.konfigurationBitliste & 1) && ausführdateiKopf.eintragPunkt >= datenPosition.adresse && ausführdateiKopf.eintragPunkt < datenPosition.adresse + datenPosition.dateibereichsgröße && !(ausführdateiKopf.eintragPunkt & 3)) gültigEintragPunkt = 1;
        ladeeinträge++;
    }
    return gültigEintragPunkt && (linuxBetriebsart ? !aBIInOrdnung : aBIInOrdnung) && ladeeinträge ? 0 : benutzerAusführdateiFehler;
}
int benutzerValidierenELF(const unsigned char *Daten, size_t größe) { return eLFValidieren(Daten, größe, 0); }
static void seiteAnordnung(uintptr_t adresse, uint64_t konfigurationBitliste, unsigned zugriffErlaubnisse) {
    unsigned nachschlagenIndex = (adresse - benutzerBasis) / seiteGröße;
    seiteListe[nachschlagenIndex] = adresse | konfigurationBitliste;
    erlaubnisseListe[nachschlagenIndex] = zugriffErlaubnisse;
}
static int benutzerBereich(uintptr_t adresse, size_t eintragAnzahl, int schreibend) {
    if (adresse < benutzerBasis || !enthalten(adresse, eintragAnzahl, benutzerEnde)) return 0;
    if (!eintragAnzahl) return 1;
    unsigned ersterEintrag = (adresse - benutzerBasis) / seiteGröße, letzterElementeintrag = (adresse + eintragAnzahl - 1 - benutzerBasis) / seiteGröße;
    for (unsigned ordnungszahlIndex = ersterEintrag; ordnungszahlIndex <= letzterElementeintrag; ordnungszahlIndex++) if (!(erlaubnisseListe[ordnungszahlIndex] & (schreibend ? 2 : 1))) return 0;
    return 1;
}
static int pfadKopieren(uintptr_t adresse, char *pfad) {
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < 65; ordnungszahlIndex++) {
        if (!benutzerBereich(adresse, 1, 0)) return -14;
        pfad[ordnungszahlIndex] = *(const char *)adresse++;
        if (!pfad[ordnungszahlIndex]) return 0;
    }
    return -36;
}
static intptr_t betriebskernErgebnis(intptr_t ergebnis) { return ergebnis < 0 ? -fehlerNummer : ergebnis; }
static int zugeordnetDateideskriptor(uint64_t dateiKennwert) { return dateiKennwert >= 3 && dateiKennwert < 19 ? dateiListe[dateiKennwert - 3] : -1; }
static int netzbuchseEndpunktEigentümer(uint64_t dateiKennwert) { return dateiKennwert >= 32 && dateiKennwert < 56 && netzbuchseEndpunkte[dateiKennwert - 32]; }
static int adresseEingabe(uintptr_t zeigendWert, size_t Länge, struct pk_sockaddr_in *adresse) {
    if (Länge != sizeof(*adresse)) return -22;
    if (!benutzerBereich(zeigendWert, Länge, 0)) return -14;
    memcpy(adresse, (const void *)zeigendWert, sizeof(*adresse));
    return adresse->sin_family == AF_INET ? 0 : -97;
}
static int adresseAusgabePrüfen(uintptr_t zeigendWert, uintptr_t längeZeiger, pk_socklen_t *pufferKapazität) {
    if (!benutzerBereich(längeZeiger, sizeof(*pufferKapazität), 1)) return -14;
    memcpy(pufferKapazität, (const void *)längeZeiger, sizeof(*pufferKapazität));
    if (*pufferKapazität > sizeof(struct pk_sockaddr_in)) *pufferKapazität = sizeof(struct pk_sockaddr_in);
    if (*pufferKapazität && !benutzerBereich(zeigendWert, *pufferKapazität, 1)) return -14;
    return 0;
}
static void adresseAusgabe(uintptr_t zeigendWert, uintptr_t längeZeiger, pk_socklen_t pufferKapazität, int adresse, int portNummer) {
    struct pk_sockaddr_in Wert; memset(&Wert, 0, sizeof(Wert));
    Wert.sin_family = AF_INET; Wert.sin_port = pk_htons(portNummer); Wert.sin_addr.s_addr = pk_htonl(adresse);
    if (pufferKapazität) memcpy((void *)zeigendWert, &Wert, pufferKapazität);
    pk_socklen_t Länge = sizeof(Wert); memcpy((void *)längeZeiger, &Länge, sizeof(Länge));
}
extern uintptr_t platineKanal(uintptr_t, uintptr_t);
static intptr_t systemnahSystemAufrufVorgang(benutzerRahmen *dateiEintrag) {
    uintptr_t ersterWert = dateiEintrag->datenRegister[0], zweiterWert = dateiEintrag->datenRegister[1], zeichenKode = dateiEintrag->datenRegister[2];
    char pfad[65];
    int dateiKennwert, ergebnis;
    switch (dateiEintrag->datenRegister[8]) {
    case 0: return 1; // eigen ABI 버전
    case 1: // write: zeiger 전체를 검사한 rückseiteWert Ausgabe/Datei wertÄndern
        if (zeichenKode > 65536) return -22;
        if (!benutzerBereich(zweiterWert, zeichenKode, 0)) return -14;
        if (ersterWert == 1 || ersterWert == 2) {
            uint64_t ausgabeStarten=uhrWert();
            for (size_t ordnungszahlIndex = 0; ordnungszahlIndex < zeichenKode; ordnungszahlIndex++) platineKanal(ersterWert, ((const unsigned char *)zweiterWert)[ordnungszahlIndex]);
            /* 큰 tty를 그린 betriebskernWert 시간만 돌려준다. EL0 berechnung 기한은 늘리지 않는다. */
            if(interaktiv){
                fristZeit+=uhrWert()-ausgabeStarten;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(fristZeit) : "memory");
            }
            return zeichenKode;
        }
        if(ersterWert>=40&&netzbuchseEndpunktEigentümer(ersterWert)){
            size_t elementeintragAnzahl=zeichenKode>512?512:zeichenKode;for(size_t ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)javaNetzAblegen(ordnungszahlIndex,((const unsigned char *)zweiterWert)[ordnungszahlIndex]);return javaDatenstromSchreiben(ersterWert,elementeintragAnzahl);
        }
        dateiKennwert = zugeordnetDateideskriptor(ersterWert); if (dateiKennwert < 0) return -9;
        return betriebskernErgebnis(pk_write(dateiKennwert, (const void *)zweiterWert, zeichenKode));
    case 2:
        if (zeichenKode > 65536) return -22;
        if (!benutzerBereich(zweiterWert, zeichenKode, 1)) return -14;
        if (ersterWert == 0) {
            size_t elementeintragAnzahl = 0;
            while (elementeintragAnzahl < zeichenKode) {
                int zeichenWert = (int32_t)platineZeichenHolen(); if (zeichenWert == -2) return elementeintragAnzahl; if (zeichenWert < 0) break;
                ((unsigned char *)zweiterWert)[elementeintragAnzahl++] = zeichenWert;
            }
            return elementeintragAnzahl ? (intptr_t)elementeintragAnzahl : (zeichenKode ? -11 : 0);
        }
        if(ersterWert>=40&&netzbuchseEndpunktEigentümer(ersterWert)){
            ergebnis=javaDatenstromLesen(ersterWert,zeichenKode>512?512:zeichenKode);if(ergebnis>0)for(int ordnungszahlIndex=0;ordnungszahlIndex<ergebnis;ordnungszahlIndex++)((unsigned char *)zweiterWert)[ordnungszahlIndex]=javaNetzHolen(ordnungszahlIndex);return ergebnis;
        }
        dateiKennwert = zugeordnetDateideskriptor(ersterWert); if (dateiKennwert < 0) return -9;
        return betriebskernErgebnis(pk_read(dateiKennwert, (void *)zweiterWert, zeichenKode));
    case 3:
        ergebnis = pfadKopieren(ersterWert, pfad); if (ergebnis) return ergebnis;
        if (zweiterWert > 0x7ff) return -22;
        for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < 16; ordnungszahlIndex++) if (dateiListe[ordnungszahlIndex] < 0) {
            dateiKennwert = pk_open(pfad, (int)zweiterWert, 0600);
            if (dateiKennwert < 0) return -fehlerNummer;
            dateiListe[ordnungszahlIndex] = dateiKennwert; return ordnungszahlIndex + 3;
        }
        return -24;
    case 4:
        if (netzbuchseEndpunktEigentümer(ersterWert)) { ergebnis = netzbuchseEndpunktSchließen(ersterWert); if (!ergebnis) netzbuchseEndpunkte[ersterWert - 32] = 0; return ergebnis; }
        dateiKennwert = zugeordnetDateideskriptor(ersterWert); if (dateiKennwert < 0) return -9;
        ergebnis = pk_close(dateiKennwert); if (!ergebnis) dateiListe[ersterWert - 3] = -1;
        return betriebskernErgebnis(ergebnis);
    case 5:
        dateiKennwert = zugeordnetDateideskriptor(ersterWert); if (dateiKennwert < 0) return -9;
        if (zeichenKode > 2) return -22;
        return betriebskernErgebnis(pk_lseek(dateiKennwert, (int64_t)zweiterWert, zeichenKode));
    case 7: return platineVergangeneMillisekunden();
    case 8: { // brk: 별도 Benutzer RW/NX speicherhaldeWert, 새로 노출되는 페이지는 0으로 initialisieren
        if (!ersterWert) return speicherhaldeEnde;
        if (ersterWert < benutzerAbbildEnde || ersterWert > benutzerSpeicherhaldeEnde) return -12;
        uintptr_t altSeiten = (speicherhaldeEnde + seiteGröße - 1) & ~(seiteGröße - 1);
        uintptr_t neuSeiten = (ersterWert + seiteGröße - 1) & ~(seiteGröße - 1);
        if (neuSeiten > altSeiten) {
            for (uintptr_t datenPosition = altSeiten; datenPosition < neuSeiten; datenPosition += seiteGröße) seiteAnordnung(datenPosition, betriebskernSeite, 0);
            abgleichenTabellen();
            memset((void *)altSeiten, 0, neuSeiten - altSeiten);
            for (uintptr_t datenPosition = altSeiten; datenPosition < neuSeiten; datenPosition += seiteGröße) seiteAnordnung(datenPosition, benutzerLesenSchreiben, 3);
        } else {
            for (uintptr_t datenPosition = neuSeiten; datenPosition < altSeiten; datenPosition += seiteGröße) {
                seiteListe[(datenPosition - benutzerBasis) / seiteGröße] = 0; erlaubnisseListe[(datenPosition - benutzerBasis) / seiteGröße] = 0;
            }
        }
        speicherhaldeEnde = ersterWert; abgleichenTabellen(); return ersterWert;
    }
    case 9:
        dateiKennwert = zugeordnetDateideskriptor(ersterWert); return dateiKennwert < 0 ? -9 : betriebskernErgebnis(pk_size(dateiKennwert));
    case 10:
        dateiKennwert = zugeordnetDateideskriptor(ersterWert); return dateiKennwert < 0 ? -9 : betriebskernErgebnis(pk_ftruncate(dateiKennwert, (int64_t)zweiterWert));
    case 11:
        ergebnis = pfadKopieren(ersterWert, pfad); return ergebnis ? ergebnis : betriebskernErgebnis(pk_unlink(pfad));
    case 12:
        dateiKennwert = zugeordnetDateideskriptor(ersterWert); return dateiKennwert < 0 ? -9 : betriebskernErgebnis(pk_fsync(dateiKennwert));
    case 13: { // 그래픽 기초 API: Benutzer 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t angefordertBreiteWert = dateiEintrag->datenRegister[3], angefordertHöheWert = dateiEintrag->datenRegister[4];
        if (!platineBildpuffer()) return -19;
        uintptr_t bildschirmSpannweite = platineBildschirmBreite(), bildschirmLänge = platineBildschirmHöhe();
        if (ersterWert > bildschirmSpannweite || zweiterWert > bildschirmLänge || angefordertBreiteWert > bildschirmSpannweite - ersterWert || angefordertHöheWert > bildschirmLänge - zweiterWert) return -22;
        for (uintptr_t senkrechteKoordinateKoordinate = zweiterWert; senkrechteKoordinateKoordinate < zweiterWert + angefordertHöheWert; senkrechteKoordinateKoordinate++) for (uintptr_t waagerechteKoordinateKoordinate = ersterWert; waagerechteKoordinateKoordinate < ersterWert + angefordertBreiteWert; waagerechteKoordinateKoordinate++) platineBildpunkt(waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate, zeichenKode);
        return 0;
    }
    case 14: return (int32_t)platineZeichenHolen();
    case 15: // args(-1,0,0)=elementeintragAnzahl; args(index,buffer,capacity)=UTF-8 Länge
        if (ersterWert == UINTPTR_MAX) return weitergeleitetArgumentAnzahl;
        if (ersterWert >= weitergeleitetArgumentAnzahl) return -22;
        if (zeichenKode <= weitergeleitetArgumentLänge[ersterWert]) return -36;
        if (!benutzerBereich(zweiterWert, weitergeleitetArgumentLänge[ersterWert] + 1, 1)) return -14;
        memcpy((void *)zweiterWert, weitergeleitetArgument[ersterWert], weitergeleitetArgumentLänge[ersterWert] + 1);
        return weitergeleitetArgumentLänge[ersterWert];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(ersterWert==0){if(!javaKonsoleInteraktiv())return -95;interaktiv=1;return platineTerminal(13);}
        if(ersterWert==2){interaktiv=0;return 0;}
        if(ersterWert==3)return platineTerminal(13);
        if(ersterWert!=1||!interaktiv)return -22;
        ergebnis=(int32_t)platineZeichenHolen();
        if(ergebnis==-4096)return ergebnis;
        zeitüberschreitungStarten();return ergebnis<0?-11:ergebnis;
    case 17: { // 유한한 협력 wertWarten: Kommunikation 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (ersterWert > 100) return -22;
        uint64_t endeZeit = uhrWert() + frequenz * ersterWert / 1000;
        do { netzwerkUntersuchen(); dateiÜbertragungUntersuchen(); __asm__ volatile("yield"); } while (uhrWert() < endeZeit);
        zeitüberschreitungStarten(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 elternknotenWert·빈 폴더를 검사한다.
        if (zweiterWert > 2) return -22;
        ergebnis = pfadKopieren(ersterWert, pfad); if (ergebnis) return ergebnis;
        unsigned Länge = 0; while (pfad[Länge]) Länge++;
        ergebnis = javaPfadStarten(Länge); if (ergebnis < 0) return ergebnis;
        for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < Länge; ordnungszahlIndex++) javaPfadByte(ordnungszahlIndex, (unsigned char)pfad[ordnungszahlIndex]);
        return zweiterWert == 0 ? javaEintragArt() : zweiterWert == 1 ? javaErstellenVerzeichnis() : javaEntfernenVerzeichnis();
    }
    case 20:
        if(ersterWert==5){int zeichenWert=(int32_t)platineZeichenHolen();if(zeichenWert==-4096)return zeichenWert;if(zeichenWert>=0)bildschirmDrücken(eigentümerObjekt,zeichenWert);zeitüberschreitungStarten();}
        if(ersterWert==3&&zeichenKode){if(!javaKonsoleInteraktiv())return -95;interaktiv=1;platineTerminal(300);}
        return bildschirmAufrufen(eigentümerObjekt,ersterWert,zweiterWert,zeichenKode,dateiEintrag->datenRegister[3],dateiEintrag->datenRegister[4],dateiEintrag->datenRegister[5]);
    case 21:
        if(zeichenKode>127)return -22;if(!benutzerBereich(zweiterWert,zeichenKode*sizeof(uint32_t),0))return -14;
        return bildschirmText(eigentümerObjekt,ersterWert,(const uint32_t *)zweiterWert,zeichenKode);
    case 22: // Bildschirm größe abfragenWert: 0=breiteWert, 1=höheWert. 사용자에게 주소를 노출하지 않는다.
        if (ersterWert > 1) return -22;
        if (!platineBildpuffer()) return -19;
        return ersterWert == 0 ? platineBildschirmBreite() : platineBildschirmHöhe();
    case 32:
        if (ersterWert != AF_INET) return -97;
        if(zweiterWert==SOCK_STREAM&&(zeichenKode==0||zeichenKode==6))ergebnis=javaDatenstromErstellen();
        else if(zweiterWert==SOCK_DGRAM&&(zeichenKode==0||zeichenKode==IPPROTO_UDP))ergebnis=javaNetzNetzbuchse(ersterWert,zweiterWert,zeichenKode);
        else return -93;
        if (ergebnis >= 32 && ergebnis < 56) netzbuchseEndpunkte[ergebnis - 32] = 1;
        return ergebnis;
    case 33: {
        if (!netzbuchseEndpunktEigentümer(ersterWert)) return -9;
        struct pk_sockaddr_in adresse;
        ergebnis = adresseEingabe(zweiterWert, zeichenKode, &adresse); if (ergebnis) return ergebnis;
        return ersterWert>=40?javaDatenstromZuordnen(ersterWert,pk_htonl(adresse.sin_addr.s_addr),pk_htons(adresse.sin_port)):javaNetzZuordnen(ersterWert, pk_htonl(adresse.sin_addr.s_addr), pk_htons(adresse.sin_port));
    }
    case 34: {
        if (!netzbuchseEndpunktEigentümer(ersterWert)) return -9;
        if(ersterWert>=40)return -95;
        if (dateiEintrag->datenRegister[3]) return -95;
        if (zeichenKode > 512) return -90;
        if (zeichenKode && !benutzerBereich(zweiterWert, zeichenKode, 0)) return -14;
        struct pk_sockaddr_in adresse;
        ergebnis = adresseEingabe(dateiEintrag->datenRegister[4], dateiEintrag->datenRegister[5], &adresse); if (ergebnis) return ergebnis;
        for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < zeichenKode; ordnungszahlIndex++) javaNetzAblegen(ordnungszahlIndex, ((const unsigned char *)zweiterWert)[ordnungszahlIndex]);
        return javaNetzSenden(ersterWert, pk_htonl(adresse.sin_addr.s_addr), pk_htons(adresse.sin_port), zeichenKode);
    }
    case 35: {
        if (!netzbuchseEndpunktEigentümer(ersterWert)) return -9;
        if(ersterWert>=40)return -95;
        if (dateiEintrag->datenRegister[3]) return -95;
        if (zeichenKode > 512) return -90;
        if (zeichenKode && !benutzerBereich(zweiterWert, zeichenKode, 1)) return -14;
        pk_socklen_t pufferKapazität = 0;
        if (dateiEintrag->datenRegister[4]) { ergebnis = adresseAusgabePrüfen(dateiEintrag->datenRegister[4], dateiEintrag->datenRegister[5], &pufferKapazität); if (ergebnis) return ergebnis; }
        ergebnis = javaNetzEmpfangsvorgang(ersterWert, zeichenKode); if (ergebnis < 0) return ergebnis;
        for (int ordnungszahlIndex = 0; ordnungszahlIndex < ergebnis; ordnungszahlIndex++) ((unsigned char *)zweiterWert)[ordnungszahlIndex] = javaNetzHolen(ordnungszahlIndex);
        if (dateiEintrag->datenRegister[4]) adresseAusgabe(dateiEintrag->datenRegister[4], dateiEintrag->datenRegister[5], pufferKapazität, javaNetzEntfernt(ersterWert), javaNetzGegenstelle(ersterWert));
        return ergebnis;
    }
    case 36: {
        if (!netzbuchseEndpunktEigentümer(ersterWert)) return -9;
        pk_socklen_t pufferKapazität;
        ergebnis = adresseAusgabePrüfen(zweiterWert, zeichenKode, &pufferKapazität); if (ergebnis) return ergebnis;
        adresseAusgabe(zweiterWert,zeichenKode,pufferKapazität,ersterWert>=40?javaDatenstromAdresse(ersterWert):javaNetzAdresse(ersterWert),ersterWert>=40?javaDatenstromPort(ersterWert):javaNetzPort(ersterWert)); return 0;
    }
    case 37: {
        if(ersterWert<40||!netzbuchseEndpunktEigentümer(ersterWert))return -9;struct pk_sockaddr_in adresse;
        ergebnis=adresseEingabe(zweiterWert,zeichenKode,&adresse);if(ergebnis)return ergebnis;
        return javaDatenstromVerbinden(ersterWert,pk_htonl(adresse.sin_addr.s_addr),pk_htons(adresse.sin_port));
    }
    case 38: return ersterWert>=40&&netzbuchseEndpunktEigentümer(ersterWert)?javaDatenstromLauschen(ersterWert,zweiterWert):-9;
    case 39:
        if(ersterWert<40||!netzbuchseEndpunktEigentümer(ersterWert))return -9;
        if(zweiterWert||zeichenKode)return -95;ergebnis=javaDatenstromAnnehmen(ersterWert);if(ergebnis>=40&&ergebnis<56)netzbuchseEndpunkte[ergebnis-32]=1;return ergebnis;
    case 40: return ersterWert>=40&&netzbuchseEndpunktEigentümer(ersterWert)?javaDatenstromGegenstelle(ersterWert):-9;
    default: return -38; // istNichtUnterstützt 기능을 성공으로 가장하지 않음
    }
}
#include "linuxVerträglichkeit.inc"
static intptr_t Systemaufruf(benutzerRahmen *dateiEintrag) {
    network_poll();
    return linuxABI ? linuxSystemAufrufVorgang(dateiEintrag) : systemnahSystemAufrufVorgang(dateiEintrag);
}
static void zurückkehrenBetriebskern(benutzerRahmen *dateiEintrag, int ergebnis) {
    zeitüberschreitungStoppen();
    dateiEintrag->datenRegister[0] = (uint64_t)(int64_t)ergebnis;
    dateiEintrag->befehlPosition = (uintptr_t)benutzerZurückkehren;
    dateiEintrag->statuswertKode = 0x3c5; // EL1h, DAIF masked
}
int benutzerAusnahme(benutzerRahmen *dateiEintrag, unsigned abfangenSignal) {
    if (!aktiv || (dateiEintrag->statuswertKode & 15) != 0) return 0;
    if (abfangenSignal) {
        uint32_t empfangsbestätigungWert = maschineRegister(unterbrechenCPUSchnittstelle + 0xc), bezeichnerWert = empfangsbestätigungWert & 1023;
        if (bezeichnerWert == 30) { zurückkehrenBetriebskern(dateiEintrag, benutzerZeitüberschreitung); maschineRegister(unterbrechenCPUSchnittstelle + 0x10) = empfangsbestätigungWert; return 1; }
        if (bezeichnerWert < 1020) maschineRegister(unterbrechenCPUSchnittstelle + 0x10) = empfangsbestätigungWert;
        return 1;
    }
    uint64_t ausnahmeStatuswert; __asm__ volatile("mrs %0, esr_el1" : "=r"(ausnahmeStatuswert));
    if (uhrWert() >= fristZeit) { zurückkehrenBetriebskern(dateiEintrag, benutzerZeitüberschreitung); return 1; }
    unsigned ausnahmeKategorie = ausnahmeStatuswert >> 26;
    if (ausnahmeKategorie == 0x15 && (ausnahmeStatuswert & 0xffff) == 0) {
        if (linuxABI ? dateiEintrag->datenRegister[8] == 93 || dateiEintrag->datenRegister[8] == 94 : dateiEintrag->datenRegister[8] == 6) zurückkehrenBetriebskern(dateiEintrag, (int)(dateiEintrag->datenRegister[0] & 255));
        else {
            intptr_t ergebnis=Systemaufruf(dateiEintrag);
            if(ergebnis==-4096&&interaktiv){
                gespeichert[eigentümerObjekt].ausführungRahmen=*dateiEintrag;gespeichert[eigentümerObjekt].ausführungRahmen.befehlPosition-=4;
                benutzerGleitkommaSpeichern(gespeichert[eigentümerObjekt].fließendPunktStatuswert);zurückkehrenBetriebskern(dateiEintrag,benutzerUnterbrochen);
            }else dateiEintrag->datenRegister[0]=(uint64_t)ergebnis;
        }
    } else zurückkehrenBetriebskern(dateiEintrag, ausnahmeKategorie == 0x24 ? benutzerDatenFehler : ausnahmeKategorie == 0x20 ? benutzerAusführungFehler : benutzerUngültigBefehlswort);
    return 1;
}

// 생성된 const ELF gruppeWert: 실행은 반드시 Programm 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *Daten; size_t größe; unsigned weitergeleitetWert; } programm;
#include "programs.h"
static void *momentaufnahme(unsigned positionIndex){return (void *)(0x04000000ul+positionIndex*(benutzerEnde-benutzerBasis));}
static int programmBeenden(int ergebnis){
    benutzerAngesammeltZeit[eigentümerObjekt]+=(uint32_t)platineVergangeneMillisekunden()-benutzerAusführungZeit[eigentümerObjekt];
    zeitüberschreitungStoppen();aktiv=0;
    if(ergebnis==benutzerUnterbrochen){
        gespeichertProzess *zeichenketteDaten=&gespeichert[eigentümerObjekt];zeichenketteDaten->pausiertStatuswert=1;zeichenketteDaten->interaktiv=interaktiv;zeichenketteDaten->linuxABI=linuxABI;zeichenketteDaten->speicherhaldeSpeichergerät=speicherhaldeEnde;zeichenketteDaten->argumenteAnzahl=weitergeleitetArgumentAnzahl;
        memcpy(zeichenketteDaten->erlaubnisseListe,erlaubnisseListe,sizeof(erlaubnisseListe));memcpy(zeichenketteDaten->dateiListe,dateiListe,sizeof(dateiListe));memcpy(zeichenketteDaten->netzbuchseEndpunkte,netzbuchseEndpunkte,sizeof(netzbuchseEndpunkte));
        memcpy(zeichenketteDaten->argumentDatenfeld,weitergeleitetArgument,sizeof(weitergeleitetArgument));memcpy(zeichenketteDaten->argumentlänge,weitergeleitetArgumentLänge,sizeof(weitergeleitetArgumentLänge));
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<benutzerSeiteAnzahl;ordnungszahlIndex++)if(erlaubnisseListe[ordnungszahlIndex])memcpy((unsigned char *)momentaufnahme(eigentümerObjekt)+ordnungszahlIndex*seiteGröße,(void *)(benutzerBasis+ordnungszahlIndex*seiteGröße),seiteGröße);
    }else{
        gespeichert[eigentümerObjekt].pausiertStatuswert=0;bildschirmInitialisieren(eigentümerObjekt);
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<16;ordnungszahlIndex++)if(dateiListe[ordnungszahlIndex]>=0)pk_close(dateiListe[ordnungszahlIndex]);
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<24;ordnungszahlIndex++)if(netzbuchseEndpunkte[ordnungszahlIndex])netzbuchseEndpunktSchließen(ordnungszahlIndex+32);
    }
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<benutzerSeiteAnzahl;ordnungszahlIndex++){seiteListe[ordnungszahlIndex]=0;erlaubnisseListe[ordnungszahlIndex]=0;}abgleichenTabellen();return ergebnis;
}
uintptr_t platineBenutzerSteuerung(uintptr_t aktion){
    unsigned positionIndex=aktion&15;if(positionIndex>=4||aktiv)return (uint32_t)-22;
    gespeichertProzess *zeichenketteDaten=&gespeichert[positionIndex];
    if(aktion>=32){if(zeichenketteDaten->pausiertStatuswert){for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<16;ordnungszahlIndex++)if(zeichenketteDaten->dateiListe[ordnungszahlIndex]>=0)pk_close(zeichenketteDaten->dateiListe[ordnungszahlIndex]);for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<24;ordnungszahlIndex++)if(zeichenketteDaten->netzbuchseEndpunkte[ordnungszahlIndex])netzbuchseEndpunktSchließen(ordnungszahlIndex+32);}zeichenketteDaten->pausiertStatuswert=0;bildschirmInitialisieren(positionIndex);return 0;}
    if(aktion>=16)return zeichenketteDaten->pausiertStatuswert;
    if(!zeichenketteDaten->pausiertStatuswert)return (uint32_t)-22;
    eigentümerObjekt=positionIndex;interaktiv=zeichenketteDaten->interaktiv;linuxABI=zeichenketteDaten->linuxABI;speicherhaldeEnde=zeichenketteDaten->speicherhaldeSpeichergerät;weitergeleitetArgumentAnzahl=zeichenketteDaten->argumenteAnzahl;
    memcpy(dateiListe,zeichenketteDaten->dateiListe,sizeof(dateiListe));memcpy(netzbuchseEndpunkte,zeichenketteDaten->netzbuchseEndpunkte,sizeof(netzbuchseEndpunkte));memcpy(weitergeleitetArgument,zeichenketteDaten->argumentDatenfeld,sizeof(weitergeleitetArgument));memcpy(weitergeleitetArgumentLänge,zeichenketteDaten->argumentlänge,sizeof(weitergeleitetArgumentLänge));
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<benutzerSeiteAnzahl;ordnungszahlIndex++)seiteListe[ordnungszahlIndex]=(benutzerBasis+ordnungszahlIndex*seiteGröße)|betriebskernSeite;abgleichenTabellen();
    memset((void *)benutzerBasis,0,benutzerEnde-benutzerBasis);
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<benutzerSeiteAnzahl;ordnungszahlIndex++)if(zeichenketteDaten->erlaubnisseListe[ordnungszahlIndex])memcpy((void *)(benutzerBasis+ordnungszahlIndex*seiteGröße),(unsigned char *)momentaufnahme(positionIndex)+ordnungszahlIndex*seiteGröße,seiteGröße);
    memcpy(erlaubnisseListe,zeichenketteDaten->erlaubnisseListe,sizeof(erlaubnisseListe));
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<benutzerSeiteAnzahl;ordnungszahlIndex++){unsigned datenPosition=erlaubnisseListe[ordnungszahlIndex];seiteListe[ordnungszahlIndex]=datenPosition?(benutzerBasis+ordnungszahlIndex*seiteGröße)|(datenPosition==3?benutzerLesenSchreiben:datenPosition==5?benutzerLesenAusführen:benutzerLesenAusschließlich):0;}
    abgleichenTabellen();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");aktiv=1;zeichenketteDaten->pausiertStatuswert=0;zeitüberschreitungStarten();
    benutzerAusführungZeit[eigentümerObjekt]=platineVergangeneMillisekunden();
    return (uint32_t)programmBeenden(benutzerFortführen(&zeichenketteDaten->ausführungRahmen,zeichenketteDaten->fließendPunktStatuswert));
}
static int programmAusführenVorgang(const unsigned char *Daten, size_t größe, unsigned weitergeleitetWert, int linuxBetriebsart, const char *Name) {
    if (aktiv) return -16;
    eigentümerObjekt=platineTerminal(11);if(eigentümerObjekt<0||eigentümerObjekt>3||gespeichert[eigentümerObjekt].pausiertStatuswert)return -16;interaktiv=0;
    int gültig = eLFValidieren(Daten, größe, linuxBetriebsart); if (gültig) return gültig;
    linuxABI = linuxBetriebsart;
    unsigned nameIndex=0;
    while (*Name && nameIndex<31) benutzerBefehlName[eigentümerObjekt][nameIndex++]=(unsigned char)*Name++;
    if (weitergeleitetArgumentAnzahl && weitergeleitetArgumentLänge[0]) {
        if (nameIndex) benutzerBefehlName[eigentümerObjekt][nameIndex++]=' ';
        for (unsigned positionIndex=0; positionIndex<weitergeleitetArgumentLänge[0]; positionIndex++) benutzerBefehlName[eigentümerObjekt][nameIndex++]=weitergeleitetArgument[0][positionIndex];
    }
    benutzerBefehlName[eigentümerObjekt][nameIndex]=0; benutzerNummer[eigentümerObjekt]=nächsterBenutzerNummer++;
    if (nächsterBenutzerNummer>0x7fffffffu) nächsterBenutzerNummer=10;
    benutzerStartenZeit[eigentümerObjekt]=platineVergangeneMillisekunden(); benutzerAngesammeltZeit[eigentümerObjekt]=0;
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < benutzerSeiteAnzahl; ordnungszahlIndex++) seiteListe[ordnungszahlIndex] = (benutzerBasis + ordnungszahlIndex * seiteGröße) | betriebskernSeite;
    abgleichenTabellen();
    memset((void *)benutzerBasis, 0, benutzerEnde - benutzerBasis);
    memset(erlaubnisseListe, 0, sizeof(erlaubnisseListe));
    eLFKopf ausführdateiKopf; memcpy(&ausführdateiKopf, Daten, sizeof(ausführdateiKopf));
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < ausführdateiKopf.programmKopfAnzahl; ordnungszahlIndex++) {
        eLFProgramm datenPosition; memcpy(&datenPosition, Daten + ausführdateiKopf.programmKopfVersatzwert + ordnungszahlIndex * sizeof(datenPosition), sizeof(datenPosition));
        if (datenPosition.typKategorie != 1 || !datenPosition.speicherbereichsgröße) continue;
        if (datenPosition.dateibereichsgröße) memcpy((void *)(uintptr_t)datenPosition.adresse, Daten + datenPosition.versatzwertWert, datenPosition.dateibereichsgröße);
        for (uintptr_t aktuellPosition = datenPosition.adresse & ~(seiteGröße - 1); aktuellPosition < datenPosition.adresse + datenPosition.speicherbereichsgröße; aktuellPosition += seiteGröße) {
            erlaubnisseListe[(aktuellPosition - benutzerBasis) / seiteGröße] = (datenPosition.konfigurationBitliste & 2) ? 3 : ((datenPosition.konfigurationBitliste & 1) ? 5 : 1);
        }
    }
    for (uintptr_t aktuellPosition = benutzerStapelAdresse; aktuellPosition < benutzerEnde; aktuellPosition += seiteGröße) erlaubnisseListe[(aktuellPosition - benutzerBasis) / seiteGröße] = 3;
    uintptr_t anfänglichStapel = linuxBetriebsart ? linuxStartenStapel(ausführdateiKopf.eintragPunkt) : benutzerEnde;
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < benutzerSeiteAnzahl; ordnungszahlIndex++) {
        unsigned zugriffErlaubnisse = erlaubnisseListe[ordnungszahlIndex];
        seiteListe[ordnungszahlIndex] = zugriffErlaubnisse ? (benutzerBasis + ordnungszahlIndex * seiteGröße) | (zugriffErlaubnisse == 3 ? benutzerLesenSchreiben : zugriffErlaubnisse == 5 ? benutzerLesenAusführen : benutzerLesenAusschließlich) : 0;
    }
    abgleichenTabellen();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < 16; ordnungszahlIndex++) dateiListe[ordnungszahlIndex] = -1;
    memset(netzbuchseEndpunkte, 0, sizeof(netzbuchseEndpunkte));
    speicherhaldeEnde = benutzerAbbildEnde;
    aktiv = 1; zeitüberschreitungStarten();
    benutzerAusführungZeit[eigentümerObjekt]=platineVergangeneMillisekunden();
    int ergebnis = benutzerEintreten(ausführdateiKopf.eintragPunkt, anfänglichStapel, weitergeleitetWert);
    return programmBeenden(ergebnis);
}
uintptr_t platineBenutzerAusführenVorgang(uintptr_t nachschlagenIndex) {
    if (nachschlagenIndex >= sizeof(ausführdateiEinträge) / sizeof(ausführdateiEinträge[0])) return (uint32_t)-22;
    const char *Name=nachschlagenIndex==10?"javac":nachschlagenIndex==11?"java":nachschlagenIndex==12?"python":nachschlagenIndex==13?"vi":nachschlagenIndex==14?"jar":nachschlagenIndex==15?"cc":nachschlagenIndex==16?"jaot":"ELF";
    return (uint32_t)programmAusführenVorgang(ausführdateiEinträge[nachschlagenIndex].Daten, ausführdateiEinträge[nachschlagenIndex].größe, ausführdateiEinträge[nachschlagenIndex].weitergeleitetWert, 0, Name);
}
static uintptr_t dateiAusführen(int linuxBetriebsart) {
    static unsigned char abbild[16384];
    if (aktiv || !weitergeleitetArgumentAnzahl) return (uint32_t)-22;
    int dateiKennwert = pk_open((const char *)weitergeleitetArgument[0], ausschließlichWertLesen, 0);
    if (dateiKennwert < 0) return (uint32_t)-fehlerNummer;
    int größe = pk_size(dateiKennwert);
    if (größe < 0 || (unsigned)größe > sizeof(abbild)) { pk_close(dateiKennwert); return (uint32_t)-27; }
    int empfangenWertAnzahl = pk_read(dateiKennwert, abbild, größe); pk_close(dateiKennwert);
    if (empfangenWertAnzahl != größe) return (uint32_t)-5;
    return (uint32_t)programmAusführenVorgang(abbild, größe, 0, linuxBetriebsart, "");
}
uintptr_t platineBenutzerDatei(void) { return dateiAusführen(0); }
uintptr_t platineBenutzerLinuxDatei(void) { return dateiAusführen(1); }
uintptr_t platineBenutzerValidieren(void) {
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(ungültigAusführdateien) / sizeof(ungültigAusführdateien[0]); ordnungszahlIndex++)
        if (benutzerValidierenELF(ungültigAusführdateien[ordnungszahlIndex].Daten, ungültigAusführdateien[ordnungszahlIndex].größe) != benutzerAusführdateiFehler) return ordnungszahlIndex + 1;
    return 0;
}
