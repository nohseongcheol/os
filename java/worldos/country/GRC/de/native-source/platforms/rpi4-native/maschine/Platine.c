#include "../benennung/maschineBindenNamen.h"
#include "bildschirmInformation.h"
#include <stdint.h>
#include <stddef.h>
#include "Benutzer.h"
#include "../Netzwerkstapel/Netzwerkstapel.h"
typedef uintptr_t maschineMaschinenwort;
#define maschineRegister(ersterWert) (*(volatile uint32_t *)(uintptr_t)(ersterWert))
#define seriellGerät 0xfe201000u
#define allgemeinZweckEinAusgabe 0xfe200000u
#define postfachAdresse 0xfe00b880u
static inline void speicherSchranke(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t uhrAnzahl(void) { uint64_t vorläufigDaten; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(vorläufigDaten)); return vorläufigDaten; }
static uint64_t frequenz;
static volatile uint32_t postfachDaten[64] __attribute__((aligned(16)));
static unsigned bildschirmBereit;
static uint32_t aRMSpeicherKibiByteeinheit;

void *memset(void *datenPosition, int zeichenKode, size_t elementeintragAnzahl) { unsigned char *nächsterVersatzwert = datenPosition; while (elementeintragAnzahl--) *nächsterVersatzwert++ = zeichenKode; return datenPosition; }
void *memcpy(void *zielDaten, const void *zeichenketteDaten, size_t elementeintragAnzahl) { unsigned char *ersterWert = zielDaten; const unsigned char *zweiterWert = zeichenketteDaten; while (elementeintragAnzahl--) *ersterWert++ = *zweiterWert++; return zielDaten; }

static int postfach(void) {
    uint32_t anfrage = (uint32_t)(uintptr_t)postfachDaten | 8;
    uint64_t ausführenVorgang = uhrAnzahl();
    speicherSchranke();
    while (maschineRegister(postfachAdresse + 0x38) & 0x80000000u)
        if (uhrAnzahl() - ausführenVorgang > frequenz) return 0;
    maschineRegister(postfachAdresse + 0x20) = anfrage;
    for (;;) {
        if (!(maschineRegister(postfachAdresse + 0x18) & 0x40000000u)) {
            uint32_t antwort = maschineRegister(postfachAdresse);
            if (antwort == anfrage) { speicherSchranke(); return postfachDaten[1] == 0x80000000u; }
        }
        if (uhrAnzahl() - ausführenVorgang > frequenz) return 0;
    }
}

extern int32_t javaKonsoleAusgabe(int32_t, int32_t), javaKonsoleEingabe(void);
extern void terminalByte(unsigned);
extern int terminalAusstehend(void);
extern void terminalZeiger(unsigned,int,int),terminalTastenkürzel(unsigned);
extern void terminalEingabeBetriebsart(unsigned);
#include "../entferntWert/entferntWert.h"
static int datenströme;
static unsigned uARTVorherig;
maschineMaschinenwort platineDatenströme(maschineMaschinenwort istBenutzt) { datenströme=istBenutzt!=0; return 0; }
maschineMaschinenwort platineKanal(maschineMaschinenwort kanal, maschineMaschinenwort zeichenKode) {
    if(datenströme && javaKonsoleAusgabe((int32_t)kanal,(int32_t)(zeichenKode&255))) return 0;
    terminalByte(zeichenKode&255);
    entferntAusgabe(zeichenKode&255);
    if ((zeichenKode&255)==10 && uARTVorherig!=13) {
        while (maschineRegister(seriellGerät + 0x18) & 0x20) __asm__ volatile("yield");
        maschineRegister(seriellGerät)=13;
    }
    uARTVorherig=zeichenKode&255;
    while (maschineRegister(seriellGerät + 0x18) & 0x20) __asm__ volatile("yield");
    maschineRegister(seriellGerät) = (uint32_t)zeichenKode & 255;
    return 0;
}
maschineMaschinenwort platineZeichenSchreiben(maschineMaschinenwort zeichenKode) { return platineKanal(1,zeichenKode); }
maschineMaschinenwort platineRohZeichenHolen(void) {
    int entferntZeichen=entferntEingabe();if(entferntZeichen>=0)return entferntZeichen;
    if (maschineRegister(seriellGerät + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t Wert = maschineRegister(seriellGerät);
    if (Wert & 0xf00) { maschineRegister(seriellGerät + 4) = 0; return (uint32_t)-1; }
    return Wert & 255;
}
maschineMaschinenwort platineZeichenHolen(void) {
    network_poll();
    static unsigned eingehendPaket,benutztKapazität; static unsigned char paketDaten[6];
    if(terminalAusstehend())return (uint32_t)-4096;
    if(datenströme){int32_t zeichenKode=javaKonsoleEingabe();if(zeichenKode!=-3)return (uint32_t)zeichenKode;}
    for(;;){
        int zeichenKode=(int32_t)platineRohZeichenHolen();if(zeichenKode<0)return (uint32_t)zeichenKode;
        if(!eingehendPaket){if(zeichenKode!=30)return zeichenKode;eingehendPaket=1;benutztKapazität=0;continue;}
        paketDaten[benutztKapazität++]=zeichenKode;if(benutztKapazität<6)continue;eingehendPaket=0;
        if(paketDaten[0]==1)terminalZeiger(paketDaten[1],paketDaten[2]+paketDaten[3]*256,paketDaten[4]+paketDaten[5]*256);
        if(paketDaten[0]==2)terminalTastenkürzel(paketDaten[1]);
        if(paketDaten[0]==3)terminalEingabeBetriebsart(paketDaten[1]);
        if(terminalAusstehend())return (uint32_t)-4096;
    }
}
maschineMaschinenwort platineVergangeneMillisekunden(void) { return (uint32_t)(uhrAnzahl() / (frequenz / 1000)); }
maschineMaschinenwort platineAusnahmeebene(void) { uint64_t vorläufigDaten; __asm__ volatile("mrs %0, CurrentEL" : "=r"(vorläufigDaten)); return vorläufigDaten >> 2; }
static void zeileAusgebenUART(const char *zeichenketteDaten) { while (*zeichenketteDaten) platineZeichenSchreiben((unsigned char)*zeichenketteDaten++); }
static void hexUART(maschineMaschinenwort elementeintragAnzahl) { const char *hexadezimalZiffern = "0123456789abcdef"; for (int zeichenketteDaten = 60; zeichenketteDaten >= 0; zeichenketteDaten -= 4) platineZeichenSchreiben(hexadezimalZiffern[(elementeintragAnzahl >> zeichenketteDaten) & 15]); }
maschineMaschinenwort platineStoppen(maschineMaschinenwort statuswertWert) {
    zeileAusgebenUART("\r\nHALTED "); hexUART(statuswertWert); zeileAusgebenUART("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void betriebskernNotstopp(const char *ursacheWert) __attribute__((noreturn));
void betriebskernNotstopp(const char *ursacheWert) { zeileAusgebenUART("\r\nPANIC: "); zeileAusgebenUART(ursacheWert); platineStoppen(1); __builtin_unreachable(); }
void platineAusnahme(maschineMaschinenwort ausnahmeStatuswert, maschineMaschinenwort befehlPosition, maschineMaschinenwort ungültigAdresse) {
    zeileAusgebenUART("\r\nEXCEPTION ESR="); hexUART(ausnahmeStatuswert);
    zeileAusgebenUART(" PC="); hexUART(befehlPosition); zeileAusgebenUART(" FAR="); hexUART(ungültigAdresse);
    platineStoppen(2);
}
int platinePhysischHardware(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postfachDaten[0]=32;postfachDaten[1]=0;postfachDaten[2]=0x10004;postfachDaten[3]=8;postfachDaten[4]=0;
    postfachDaten[5]=postfachDaten[6]=postfachDaten[7]=0;
    return postfach()&&postfachDaten[4]==0x80000008u&&(postfachDaten[5]||postfachDaten[6]);
}
int platineMaschineAdresse(unsigned char *adresse) {
    postfachDaten[0]=32;postfachDaten[1]=0;postfachDaten[2]=0x10003;postfachDaten[3]=8;postfachDaten[4]=0;
    postfachDaten[5]=postfachDaten[6]=postfachDaten[7]=0;
    if(!postfach()||(postfachDaten[4]&0x80000000u)==0||(postfachDaten[4]&0xffff)!=6)return 0;
    const unsigned char *Daten=(const unsigned char*)&postfachDaten[5];unsigned summeWert=0;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<6;ordnungszahlIndex++){adresse[ordnungszahlIndex]=Daten[ordnungszahlIndex];summeWert|=Daten[ordnungszahlIndex];}return summeWert&&!(adresse[0]&1);
}
void platineInitialisierungsvorgang(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(frequenz));
    maschineRegister(seriellGerät + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    maschineRegister(allgemeinZweckEinAusgabe + 4) = (maschineRegister(allgemeinZweckEinAusgabe + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    maschineRegister(allgemeinZweckEinAusgabe + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. fehlschlagWert 시 config.txt의 48MHz를 사용한다.
    postfachDaten[0] = 36; postfachDaten[1] = 0; postfachDaten[2] = 0x38002; postfachDaten[3] = 12;
    postfachDaten[4] = 0; postfachDaten[5] = 2; postfachDaten[6] = 48000000; postfachDaten[7] = 0; postfachDaten[8] = 0;
    int uhrFunktionsfähig = postfach();
    uint32_t geschwindigkeitWert = uhrFunktionsfähig && postfachDaten[6] >= 1843200 ? postfachDaten[6] : 48000000;
    postfachDaten[0]=32; postfachDaten[1]=0; postfachDaten[2]=0x10005; postfachDaten[3]=8; postfachDaten[4]=0;
    postfachDaten[5]=postfachDaten[6]=postfachDaten[7]=0;
    if (postfach() && postfachDaten[4]==0x80000008u) aRMSpeicherKibiByteeinheit=postfachDaten[6]/1024;
    uint32_t teiler64 = (uint32_t)(((uint64_t)geschwindigkeitWert * 4 + 57600) / 115200);
    maschineRegister(seriellGerät + 0x44) = 0x7ff;
    maschineRegister(seriellGerät + 0x24) = teiler64 / 64;
    maschineRegister(seriellGerät + 0x28) = teiler64 % 64;
    maschineRegister(seriellGerät + 0x2c) = (3u << 5) | (1u << 4);
    maschineRegister(seriellGerät + 0x38) = 0;
    maschineRegister(seriellGerät + 0x30) = 0x301;
    speicherSchranke();
    zeileAusgebenUART("JKOROS AARCH64 BARE METAL\r\n");
    benutzerSystemInitialisierungsvorgang();
    network_init();
}
maschineMaschinenwort platineFTP(maschineMaschinenwort aktion) { return (uint32_t)ftp_control((int)aktion); }
maschineMaschinenwort platineNetzwerkZustand(maschineMaschinenwort eintragWert, maschineMaschinenwort Nummer) { return netzwerkZustandLesen(eintragWert, Nummer); }
maschineMaschinenwort platineNetzwerkEinstellungen(maschineMaschinenwort aktion, maschineMaschinenwort adresse, maschineMaschinenwort maskeWert, maschineMaschinenwort netzübergangWert) { return (uint32_t)netzwerkKonfigurieren(aktion, adresse, maskeWert, netzübergangWert); }
maschineMaschinenwort platineSendenRückmeldung(maschineMaschinenwort adresse, maschineMaschinenwort reihenfolgeWert) { return (uint32_t)rückmeldungPrüfungStarten(adresse, reihenfolgeWert); }
maschineMaschinenwort platineLesenRückmeldung(maschineMaschinenwort eintragWert) { return (uint32_t)rückmeldungPrüfungLesen(eintragWert); }
maschineMaschinenwort platineStromversorgungAusgeschaltet(void) {
    ftp_control(0);
    for (unsigned Nummer=0; Nummer<32; Nummer++) netzwerkSchließen(Nummer);
    for (unsigned Nummer=0; Nummer<4; Nummer++) platineBenutzerSteuerung(32+Nummer);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    zeileAusgebenUART("\r\nPOWER OFF\r\n");
    while (maschineRegister(seriellGerät+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    maschineRegister(0xfe100020ul)=0x5a000000u | (maschineRegister(0xfe100020ul)&~0xfffu) | 0x555;
    maschineRegister(0xfe100024ul)=0x5a000000u | 10;
    maschineRegister(0xfe10001cul)=0x5a000000u | (maschineRegister(0xfe10001cul)&~0x30u) | 0x20;
    speicherSchranke();
    for (;;) __asm__ volatile("wfe");
}

maschineMaschinenwort platineBildpuffer(void) {
    if (bildschirmBereit) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 aktuellElementeintrag 크기를 읽는다. */
    const uint32_t abfragenWert[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t angefordertBreite = 640, angefordertHöhe = 480;
    for (size_t ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(abfragenWert)/4; ordnungszahlIndex++) postfachDaten[ordnungszahlIndex] = abfragenWert[ordnungszahlIndex];
    if (postfach() && postfachDaten[4] == 0x80000008u &&
        postfachDaten[5] >= 640 && postfachDaten[5] <= 1920 &&
        postfachDaten[6] >= 480 && postfachDaten[6] <= 1080) {
        angefordertBreite = postfachDaten[5]; angefordertHöhe = postfachDaten[6];
    }
    const uint32_t anfrage[] = {
        35 * 4, 0,
        0x48003, 8, 0, angefordertBreite, angefordertHöhe,
        0x48004, 8, 0, angefordertBreite, angefordertHöhe,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(anfrage)/4; ordnungszahlIndex++) postfachDaten[ordnungszahlIndex] = anfrage[ordnungszahlIndex];
    // oberkanteWert 메시지의 tatsächlichDaten 길이를 benutzenWert: 태그 eintragAnhängen 시 Länge 불일치를 방지한다.
    postfachDaten[0] = sizeof(anfrage);
    if (!postfach()) return 0;
    const unsigned rückmeldungen[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned rückmeldungLänge[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < sizeof(rückmeldungen)/sizeof(rückmeldungen[0]); ordnungszahlIndex++)
        if (postfachDaten[rückmeldungen[ordnungszahlIndex]] != (0x80000000u | rückmeldungLänge[ordnungszahlIndex])) return 0;
    uint32_t hintergrundWert = postfachDaten[28] & 0x3fffffffu;
    uint32_t größe = postfachDaten[29];
    uint32_t empfangenWertBreite = postfachDaten[5], empfangenWertHöhe = postfachDaten[6], empfangenWertZeileAbstand = postfachDaten[33];
    if (postfachDaten[15] != 32 || postfachDaten[19] != 1 ||
        empfangenWertBreite < 640 || empfangenWertBreite > 1920 || empfangenWertHöhe < 480 || empfangenWertHöhe > 1080 ||
        postfachDaten[10] < empfangenWertBreite || postfachDaten[11] < empfangenWertHöhe || postfachDaten[23] || postfachDaten[24] ||
        !hintergrundWert || hintergrundWert < 0x1000000 || (hintergrundWert & 3) || empfangenWertZeileAbstand < empfangenWertBreite * 4 || (empfangenWertZeileAbstand & 3) ||
        (uint64_t)empfangenWertZeileAbstand * empfangenWertHöhe > größe || (uint64_t)hintergrundWert + größe > 0x40000000u)
        return 0;
    platineVorbereitenZeichnung((volatile uint32_t *)(uintptr_t)hintergrundWert, empfangenWertBreite, empfangenWertHöhe, empfangenWertZeileAbstand);
    bildschirmBereit = 1;
    return 1;
}

// 단일 코어의 협력식 ausführungsfadenWert. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t gespeichert[13]; } kontext;
static kontext kontexte[3];
static unsigned char stapelliste[2][65536] __attribute__((aligned(16)));
static int istLaufend[3] = {1, 0, 0};
static int aktuellAufgabe;
extern void kontextUmschalten(kontext *, kontext *);
extern void javaAufgabe(int32_t);
maschineMaschinenwort platineAbgeben(void) {
    network_poll();
    int vorherigElementeintrag = aktuellAufgabe, nächsterElementeintrag = (vorherigElementeintrag + 1) % 3;
    while (nächsterElementeintrag != vorherigElementeintrag && !istLaufend[nächsterElementeintrag]) nächsterElementeintrag = (nächsterElementeintrag + 1) % 3;
    if (nächsterElementeintrag != vorherigElementeintrag) {
        for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < 2; ordnungszahlIndex++)
            if (istLaufend[ordnungszahlIndex + 1] && *(uint64_t *)stapelliste[ordnungszahlIndex] != 0x6b6f726f7373746bull)
                betriebskernNotstopp("task stack guard");
        aktuellAufgabe = nächsterElementeintrag;
        kontextUmschalten(&kontexte[vorherigElementeintrag], &kontexte[nächsterElementeintrag]);
    }
    return 0;
}
static void aufgabeUrlader(void) {
    javaAufgabe(aktuellAufgabe);
    istLaufend[aktuellAufgabe] = 0;
    platineAbgeben();
    betriebskernNotstopp("finished task resumed");
}
maschineMaschinenwort platineAufgabeErstellen(maschineMaschinenwort bezeichnerWert) {
    if (bezeichnerWert < 1 || bezeichnerWert > 2 || istLaufend[bezeichnerWert]) return (uint32_t)-1;
    memset(&kontexte[bezeichnerWert], 0, sizeof(kontext));
    *(uint64_t *)stapelliste[bezeichnerWert - 1] = 0x6b6f726f7373746bull;
    kontexte[bezeichnerWert].gespeichert[11] = (uintptr_t)aufgabeUrlader;
    kontexte[bezeichnerWert].gespeichert[12] = (uintptr_t)(stapelliste[bezeichnerWert - 1] + sizeof(stapelliste[0]));
    istLaufend[bezeichnerWert] = 1;
    return 0;
}
maschineMaschinenwort platineAufgabeStatuswert(maschineMaschinenwort bezeichnerWert) { return bezeichnerWert < 3 ? istLaufend[bezeichnerWert] : (uint32_t)-1; }
extern maschineMaschinenwort vorabübersetzungSpeicherNachschlagen(maschineMaschinenwort);
extern uint32_t benutzerStatuswertLesen(unsigned, unsigned);
extern unsigned char StapelOberkante[];
maschineMaschinenwort platineAbfragenSystem(maschineMaschinenwort eintragWert, maschineMaschinenwort Nummer) {
    if (eintragWert==0) return aRMSpeicherKibiByteeinheit;
    if (eintragWert==1) return ((uintptr_t)StapelOberkante-0x80000+1023)/1024;
    if (eintragWert==2 || eintragWert==3) return vorabübersetzungSpeicherNachschlagen(eintragWert==3);
    if (eintragWert==4) return bildschirmBereit ? (platineBildschirmBreite()*platineBildschirmHöhe()*4+1023)/1024 : 0;
    if (eintragWert==5) return 80*1024; /* befehlAusführen adresseGebiet 16 MiB + 네 세션 wertBewahren adresseGebiet. */
    if (eintragWert>=20) return benutzerStatuswertLesen(eintragWert-20, Nummer);
    return 0;
}
int *pk_errno_location(void) { static int fehlerliste[3]; return &fehlerliste[aktuellAufgabe]; }
