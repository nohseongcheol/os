#include "../benennung/maschineBindenNamen.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "aufrufen.h"
#include "Paket.h"
#include "uzlib.h"
static unsigned char archiv[16384], entpackt[16385];
static unsigned größe, zentral, einträgeListe;
static char eintragKlasse[256];
static unsigned zweiBytesLesen(unsigned aktuellPosition) { return archiv[aktuellPosition] | archiv[aktuellPosition+1] << 8; }
static uint32_t vierBytesLesen(unsigned aktuellPosition) { return zweiBytesLesen(aktuellPosition) | (uint32_t)zweiBytesLesen(aktuellPosition+2) << 16; }
static int beschneiden(unsigned aktuellPosition, unsigned elementeintragAnzahl, unsigned kapazitätGrenzwert) { return aktuellPosition <= kapazitätGrenzwert && elementeintragAnzahl <= kapazitätGrenzwert-aktuellPosition; }
static size_t Länge(const char *zeichenketteDaten) { size_t elementeintragAnzahl=0; while(zeichenketteDaten[elementeintragAnzahl]) elementeintragAnzahl++; return elementeintragAnzahl; }
static int gleichText(const unsigned char *ersterWert, const unsigned char *zweiterWert, unsigned elementeintragAnzahl) { for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)if(ersterWert[ordnungszahlIndex]!=zweiterWert[ordnungszahlIndex])return 0;return 1; }
static int dateiEnde(void *unbenutzt) { (void)unbenutzt; return -1; }
static int attributDaten(const char *zeile,unsigned benutztKapazität,int *eintragPunktExistiert) {
    if(benutztKapazität>=12 && gleichText((const unsigned char*)zeile,(const unsigned char*)"Class-Path: ",12))return -95;
    if(benutztKapazität>=12 && gleichText((const unsigned char*)zeile,(const unsigned char*)"Main-Class: ",12)) {
        unsigned Wert=benutztKapazität-12;if(*eintragPunktExistiert||!Wert||Wert>=sizeof(eintragKlasse))return -8;
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<Wert;ordnungszahlIndex++){unsigned char zeichenKode=zeile[12+ordnungszahlIndex];if(zeichenKode<=32||zeichenKode=='/'||zeichenKode=='\\')return -8;eintragKlasse[ordnungszahlIndex]=zeichenKode;}
        eintragKlasse[Wert]=0;*eintragPunktExistiert=1;
    }
    return 0;
}
static int mitglied(unsigned aktuellPosition, unsigned char *ergebnisDaten, unsigned kapazitätHöchstwert) {
    unsigned methodeEintrag=zweiBytesLesen(aktuellPosition+10), konfigurationBitliste=zweiBytesLesen(aktuellPosition+8), komprimiert=vierBytesLesen(aktuellPosition+20), größeFreigeben=vierBytesLesen(aktuellPosition+24), lokal=vierBytesLesen(aktuellPosition+42);
    unsigned Name=zweiBytesLesen(aktuellPosition+28);
    if(größeFreigeben>kapazitätHöchstwert || größeFreigeben>16384 || (methodeEintrag!=0 && methodeEintrag!=8) || (konfigurationBitliste&~0x80e))return -8;
    if(!beschneiden(lokal,30,zentral) || vierBytesLesen(lokal)!=0x04034b50 || zweiBytesLesen(lokal+8)!=methodeEintrag || zweiBytesLesen(lokal+6)!=konfigurationBitliste || zweiBytesLesen(lokal+26)!=Name)return -8;
    unsigned versatzwertStarten=lokal+30, zusätzlichGebiet=zweiBytesLesen(lokal+28);
    if(!beschneiden(versatzwertStarten,Name,zentral) || !gleichText(archiv+versatzwertStarten,archiv+aktuellPosition+46,Name))return -8;
    versatzwertStarten+=Name;if(!beschneiden(versatzwertStarten,zusätzlichGebiet,zentral))return -8;versatzwertStarten+=zusätzlichGebiet;
    if(!beschneiden(versatzwertStarten,komprimiert,zentral))return -8;
    if(!(konfigurationBitliste&8) && (vierBytesLesen(lokal+14)!=vierBytesLesen(aktuellPosition+16) || vierBytesLesen(lokal+18)!=komprimiert || vierBytesLesen(lokal+22)!=größeFreigeben))return -8;
    if(methodeEintrag==0) { if(komprimiert!=größeFreigeben)return -8; for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<größeFreigeben;ordnungszahlIndex++)ergebnisDaten[ordnungszahlIndex]=archiv[versatzwertStarten+ordnungszahlIndex]; }
    else {
        uzlib_uncomp_t zielDaten={0};uzlib_uncompress_init(&zielDaten,0,0);
        zielDaten.source=archiv+versatzwertStarten;zielDaten.source_limit=zielDaten.source+komprimiert;zielDaten.source_read_cb=dateiEnde;
        /* One extra output byte lets inflate consume/check the end marker. */
        zielDaten.dest_start=zielDaten.dest=entpackt;zielDaten.dest_limit=entpackt+größeFreigeben+1;
        int zurückgegebenWert=uzlib_uncompress(&zielDaten);
        if(zurückgegebenWert!=UZLIB_DONE || zielDaten.eof || zielDaten.dest!=entpackt+größeFreigeben || zielDaten.source!=zielDaten.source_limit)return -8;
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<größeFreigeben;ordnungszahlIndex++)ergebnisDaten[ordnungszahlIndex]=entpackt[ordnungszahlIndex];
    }
    if((uzlib_crc32(ergebnisDaten,größeFreigeben,0xffffffffu)^0xffffffffu)!=vierBytesLesen(aktuellPosition+16))return -8;
    return größeFreigeben;
}
int jARLesen(const char *Name, unsigned char *ergebnisDaten, unsigned pufferKapazität) {
    if(!einträgeListe)return -2;unsigned elementeintragAnzahl=Länge(Name),aktuellPosition=zentral;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<einträgeListe;ordnungszahlIndex++) {
        unsigned namenlänge=zweiBytesLesen(aktuellPosition+28);
        if(namenlänge==elementeintragAnzahl && gleichText(archiv+aktuellPosition+46,(const unsigned char*)Name,elementeintragAnzahl))return mitglied(aktuellPosition,ergebnisDaten,pufferKapazität);
        aktuellPosition+=46+namenlänge+zweiBytesLesen(aktuellPosition+30)+zweiBytesLesen(aktuellPosition+32);
    }
    return -2;
}
const char *jARHauptvorgang(void) { return eintragKlasse; }
int jARÖffnen(const char *dateiEintragName) {
    einträgeListe=0;eintragKlasse[0]=0;
    intptr_t dateiKennwert=benutzerAufrufen(3,(uintptr_t)dateiEintragName,0,0,0,0,0);if(dateiKennwert<0)return dateiKennwert;
    intptr_t elementeintragAnzahl=benutzerAufrufen(9,dateiKennwert,0,0,0,0,0);
    if(elementeintragAnzahl<22 || elementeintragAnzahl>(intptr_t)sizeof(archiv)) { benutzerAufrufen(4,dateiKennwert,0,0,0,0,0);return -8; }
    intptr_t empfangenWertAnzahl=benutzerAufrufen(2,dateiKennwert,(uintptr_t)archiv,elementeintragAnzahl,0,0,0);benutzerAufrufen(4,dateiKennwert,0,0,0,0,0);
    if(empfangenWertAnzahl!=elementeintragAnzahl)return -5;größe=elementeintragAnzahl;
    unsigned endeVersatzwert=größe-22;
    for(;;) { if(vierBytesLesen(endeVersatzwert)==0x06054b50 && endeVersatzwert+22+zweiBytesLesen(endeVersatzwert+20)==größe)break; if(!endeVersatzwert)return -8;endeVersatzwert--; }
    unsigned eintragAnzahl=zweiBytesLesen(endeVersatzwert+10);zentral=vierBytesLesen(endeVersatzwert+16);
    if(zweiBytesLesen(endeVersatzwert+4)||zweiBytesLesen(endeVersatzwert+6)||zweiBytesLesen(endeVersatzwert+8)!=eintragAnzahl||!eintragAnzahl||eintragAnzahl>256||!beschneiden(zentral,vierBytesLesen(endeVersatzwert+12),endeVersatzwert)||zentral+vierBytesLesen(endeVersatzwert+12)!=endeVersatzwert)return -8;
    unsigned aktuellPosition=zentral;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<eintragAnzahl;ordnungszahlIndex++) {
        if(!beschneiden(aktuellPosition,46,endeVersatzwert)||vierBytesLesen(aktuellPosition)!=0x02014b50||zweiBytesLesen(aktuellPosition+34))return -8;
        unsigned namenlänge=zweiBytesLesen(aktuellPosition+28),nächsterElementeintrag=46+namenlänge+zweiBytesLesen(aktuellPosition+30)+zweiBytesLesen(aktuellPosition+32);
        if(!namenlänge||namenlänge>511||!beschneiden(aktuellPosition,nächsterElementeintrag,endeVersatzwert)||vierBytesLesen(aktuellPosition+24)>16384)return -8;
        for(unsigned innerlichOrdnungszahl=0;innerlichOrdnungszahl<namenlänge;innerlichOrdnungszahl++)if(!archiv[aktuellPosition+46+innerlichOrdnungszahl])return -8;
        unsigned andererEintrag=zentral;
        for(unsigned innerlichOrdnungszahl=0;innerlichOrdnungszahl<ordnungszahlIndex;innerlichOrdnungszahl++){unsigned längeDaten=zweiBytesLesen(andererEintrag+28);if(längeDaten==namenlänge&&gleichText(archiv+andererEintrag+46,archiv+aktuellPosition+46,längeDaten))return -8;andererEintrag+=46+längeDaten+zweiBytesLesen(andererEintrag+30)+zweiBytesLesen(andererEintrag+32);}
        aktuellPosition+=nächsterElementeintrag;
    }
    if(aktuellPosition!=endeVersatzwert)return -8;einträgeListe=eintragAnzahl;
    unsigned char bündelInhaltsverzeichnis[4096];int gruppeGröße=jARLesen("META-INF/MANIFEST.MF",bündelInhaltsverzeichnis,sizeof(bündelInhaltsverzeichnis)-1);if(gruppeGröße<0){einträgeListe=0;return -8;}
    bündelInhaltsverzeichnis[gruppeGröße]=0;
    char logisch[512];unsigned benutztKapazität=0,indexWert=0;int eintragPunktExistiert=0;
    while(indexWert<(unsigned)gruppeGröße) {
        unsigned ausführenVorgang=indexWert;while(indexWert<(unsigned)gruppeGröße && bündelInhaltsverzeichnis[indexWert]!='\n')indexWert++;
        unsigned längeDaten=indexWert-ausführenVorgang;if(indexWert<(unsigned)gruppeGröße)indexWert++;if(längeDaten && bündelInhaltsverzeichnis[ausführenVorgang+längeDaten-1]=='\r')längeDaten--;
        if(benutztKapazität && längeDaten && bündelInhaltsverzeichnis[ausführenVorgang]==' ') {ausführenVorgang++;längeDaten--;}
        else {
            int ergebnis=attributDaten(logisch,benutztKapazität,&eintragPunktExistiert);if(ergebnis)return ergebnis;
            benutztKapazität=0;if(!längeDaten)break;
        }
        if(längeDaten>sizeof(logisch)-benutztKapazität)return -8;
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<längeDaten;ordnungszahlIndex++)logisch[benutztKapazität++]=bündelInhaltsverzeichnis[ausführenVorgang+ordnungszahlIndex];
    }
    /* The last attribute may be followed by only one newline. */
    int ergebnis=attributDaten(logisch,benutztKapazität,&eintragPunktExistiert);if(ergebnis)return ergebnis;
    return eintragPunktExistiert?0:-8;
}
