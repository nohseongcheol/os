/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "aufrufen.h"
#include "DateiABI.h"
#define editorKapazität 16384
static unsigned char Text[editorKapazität],rückgängigDaten[editorKapazität],kopiertDaten[editorKapazität],ergebnisDaten[1024];
static int Länge,indexWert,oberkanteEintrag,linksSeiteRand,warGeändert,einfügen,rückgängigLänge,obererSeiteRand,rückgängigÄnderungsliste,besitzenRückgängig,längeKopieren,benutztKapazität,spaltenliste=68,zeilennummerAnzahl=19;
static char dateiEintragName[64],befehl[128],eintragFinden[128];
static const char *mitteilungText="NORMAL  i:insert  :w:save  :q:quit";
static unsigned ausstehendTaste;
static int hilfeKategorie,statuswertAbbild,statuswertWarteschlange;
static void leeren(void){if(benutztKapazität){benutzerAufrufen(1,1,(uintptr_t)ergebnisDaten,benutztKapazität,0,0,0);benutztKapazität=0;}}
static void byteDaten(unsigned zeichenKode){if(statuswertAbbild){if((zeichenKode&192)!=128){statuswertWarteschlange+=zeichenKode>=196?2:1;}if(statuswertWarteschlange>=spaltenliste)return;}if(benutztKapazität==(int)sizeof(ergebnisDaten))leeren();ergebnisDaten[benutztKapazität++]=zeichenKode;}
static void textAusgeben(const char *zeichenketteDaten){while(*zeichenketteDaten)byteDaten((unsigned char)*zeichenketteDaten++);}
static void numerischWert(unsigned elementeintragAnzahl){char zweiterWert[12];int ordnungszahlIndex=0;do{zweiterWert[ordnungszahlIndex++]='0'+elementeintragAnzahl%10;elementeintragAnzahl/=10;}while(elementeintragAnzahl);while(ordnungszahlIndex)byteDaten(zweiterWert[--ordnungszahlIndex]);}
static void bewegenWert(int zeilennummerPosition,int spaltePosition){textAusgeben("\033[");numerischWert(zeilennummerPosition);byteDaten(';');numerischWert(spaltePosition);byteDaten('H');}
static int vorherig(int datenPosition){if(datenPosition){datenPosition--;while(datenPosition>0&&(Text[datenPosition]&192)==128)datenPosition--;}return datenPosition;}
static int nächsterElementeintrag(int datenPosition){if(datenPosition<Länge){datenPosition++;while(datenPosition<Länge&&(Text[datenPosition]&192)==128)datenPosition++;}return datenPosition;}
static int ausführenVorgang(int datenPosition){while(datenPosition>0&&Text[datenPosition-1]!='\n')datenPosition--;return datenPosition;}
static int endeVersatzwert(int datenPosition){while(datenPosition<Länge&&Text[datenPosition]!='\n')datenPosition++;return datenPosition;}
static int breiteWert(unsigned zeichenKode){return zeichenKode>=196?2:1;}
static int spalte(int datenPosition){int zeichenKode=0;for(int ordnungszahlIndex=ausführenVorgang(datenPosition);ordnungszahlIndex<datenPosition;ordnungszahlIndex=nächsterElementeintrag(ordnungszahlIndex))zeichenKode+=Text[ordnungszahlIndex]=='\t'?4-zeichenKode%4:breiteWert(Text[ordnungszahlIndex]);return zeichenKode;}
static void prüfpunkt(void){for(int ordnungszahlIndex=0;ordnungszahlIndex<Länge;ordnungszahlIndex++)rückgängigDaten[ordnungszahlIndex]=Text[ordnungszahlIndex];rückgängigLänge=Länge;obererSeiteRand=indexWert;rückgängigÄnderungsliste=warGeändert;besitzenRückgängig=1;}
static void bytesLöschenInhalt(int abgangPosition,int ankunftPosition){prüfpunkt();for(int ordnungszahlIndex=ankunftPosition;ordnungszahlIndex<Länge;ordnungszahlIndex++)Text[abgangPosition+ordnungszahlIndex-ankunftPosition]=Text[ordnungszahlIndex];Länge-=ankunftPosition-abgangPosition;indexWert=abgangPosition;warGeändert=1;}
static int wertAnhängen(const unsigned char *zeichenketteDaten,int elementeintragAnzahl){if(elementeintragAnzahl>editorKapazität-Länge){mitteilungText="File full (16384 bytes)";return 0;}prüfpunkt();for(int ordnungszahlIndex=Länge-1;ordnungszahlIndex>=indexWert;ordnungszahlIndex--)Text[ordnungszahlIndex+elementeintragAnzahl]=Text[ordnungszahlIndex];for(int ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)Text[indexWert+ordnungszahlIndex]=zeichenketteDaten[ordnungszahlIndex];Länge+=elementeintragAnzahl;indexWert+=elementeintragAnzahl;warGeändert=1;return 1;}
static void senkrecht(int unterschiedWert){int spaltePosition=spalte(indexWert),datenPosition=ausführenVorgang(indexWert);if(unterschiedWert<0){if(!datenPosition)return;datenPosition=ausführenVorgang(datenPosition-1);}else{datenPosition=endeVersatzwert(datenPosition);if(datenPosition==Länge)return;datenPosition++;}int zeichenKode=0;while(datenPosition<Länge&&Text[datenPosition]!='\n'&&zeichenKode<spaltePosition){zeichenKode+=Text[datenPosition]=='\t'?4-zeichenKode%4:breiteWert(Text[datenPosition]);datenPosition=nächsterElementeintrag(datenPosition);}indexWert=datenPosition;}
static void bildschirmZeichnen(void){
    if(indexWert>Länge)indexWert=Länge;if(oberkanteEintrag>indexWert)oberkanteEintrag=ausführenVorgang(indexWert);oberkanteEintrag=ausführenVorgang(oberkanteEintrag);
    int zeilennummerPosition=0;for(int ordnungszahlIndex=oberkanteEintrag;ordnungszahlIndex<indexWert;ordnungszahlIndex++)if(Text[ordnungszahlIndex]=='\n')zeilennummerPosition++;
    while(zeilennummerPosition>=zeilennummerAnzahl-1){oberkanteEintrag=endeVersatzwert(oberkanteEintrag);if(oberkanteEintrag<Länge)oberkanteEintrag++;zeilennummerPosition--;}
    int spaltePosition=spalte(indexWert);if(spaltePosition<linksSeiteRand)linksSeiteRand=spaltePosition;if(spaltePosition-linksSeiteRand>=spaltenliste-1)linksSeiteRand=spaltePosition-spaltenliste+2;
    textAusgeben("\033[?25l");int datenPosition=oberkanteEintrag;
    for(int zurückgegebenWert=0;zurückgegebenWert<zeilennummerAnzahl-1;zurückgegebenWert++){
        bewegenWert(zurückgegebenWert+1,1);textAusgeben("\033[0m\033[2K");int zeichenKode=0,istGezeichnet=0;
        if(datenPosition>=Länge&&zurückgegebenWert>zeilennummerPosition){textAusgeben("\033[90m~\033[0m");continue;}
        while(datenPosition<Länge&&Text[datenPosition]!='\n'){
            int nächsterVersatzwert=nächsterElementeintrag(datenPosition),angefordertBreiteWert=Text[datenPosition]=='\t'?4-zeichenKode%4:breiteWert(Text[datenPosition]);
            if(zeichenKode>=linksSeiteRand&&zeichenKode-linksSeiteRand+angefordertBreiteWert<spaltenliste){
                if(Text[datenPosition]=='\t'){for(int innerlichOrdnungszahl=0;innerlichOrdnungszahl<angefordertBreiteWert;innerlichOrdnungszahl++)byteDaten(' ');}else if(Text[datenPosition]<32||Text[datenPosition]==127){byteDaten('?');}else for(int innerlichOrdnungszahl=datenPosition;innerlichOrdnungszahl<nächsterVersatzwert;innerlichOrdnungszahl++)byteDaten(Text[innerlichOrdnungszahl]);istGezeichnet+=angefordertBreiteWert;
            }zeichenKode+=angefordertBreiteWert;datenPosition=nächsterVersatzwert;
        }
        (void)istGezeichnet;if(datenPosition<Länge)datenPosition++;
    }
    bewegenWert(zeilennummerAnzahl,1);textAusgeben("\033[7m\033[2K");statuswertAbbild=1;statuswertWarteschlange=0;textAusgeben(einfügen?"INSERT ":"NORMAL ");
    int namensbytes=0;while(dateiEintragName[namensbytes]&&namensbytes<30)byteDaten(dateiEintragName[namensbytes++]);textAusgeben(warGeändert?" [+] ":" ");
    textAusgeben("L");int zeile=1;for(int ordnungszahlIndex=0;ordnungszahlIndex<indexWert;ordnungszahlIndex++)if(Text[ordnungszahlIndex]=='\n')zeile++;numerischWert(zeile);textAusgeben(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(mitteilungText){int elementeintragAnzahl=0;textAusgeben(" | ");while(mitteilungText[elementeintragAnzahl]&&elementeintragAnzahl<20)byteDaten(mitteilungText[elementeintragAnzahl++]);}
    statuswertAbbild=0;textAusgeben("\033[0m");bewegenWert(zeilennummerPosition+1,spaltePosition-linksSeiteRand+1);textAusgeben("\033[?25h");leeren();
}
static int gedrücktWert(void){
    if(ausstehendTaste){int dritterIndex=ausstehendTaste;ausstehendTaste=0;return dritterIndex;}
    for(;;){
        int dritterIndex=benutzerAufrufen(16,1,0,0,0,0,0);
        unsigned größe=benutzerAufrufen(16,3,0,0,0,0,0);
        if(spaltenliste!=(int)(größe&65535)||zeilennummerAnzahl!=(int)(größe>>16)){
            spaltenliste=größe&65535;zeilennummerAnzahl=größe>>16;bildschirmZeichnen();
            if(hilfeKategorie){bewegenWert(zeilennummerAnzahl,1);textAusgeben("\033[0m\033[2K");byteDaten(hilfeKategorie);textAusgeben(befehl);leeren();}
        }
        if(dritterIndex>=0)return dritterIndex;
    }
}
static int maskiert(void){
    unsigned aktuellPosition=benutzerAufrufen(7,0,0,0,0,0,0);int dritterIndex=-1;
    while((unsigned)benutzerAufrufen(7,0,0,0,0,0,0)-aktuellPosition<100){dritterIndex=benutzerAufrufen(16,1,0,0,0,0,0);if(dritterIndex>=0)break;}
    if(dritterIndex<0)return 27;if(dritterIndex!='['&&dritterIndex!='O'){ausstehendTaste=dritterIndex;return 27;}
    int elementeintragAnzahl=0;for(int ordnungszahlIndex=0;ordnungszahlIndex<12;ordnungszahlIndex++){dritterIndex=gedrücktWert();if(dritterIndex>='0'&&dritterIndex<='9'){elementeintragAnzahl=elementeintragAnzahl*10+dritterIndex-'0';continue;}if(dritterIndex=='A')return 1001;if(dritterIndex=='B')return 1002;if(dritterIndex=='C')return 1003;if(dritterIndex=='D')return 1004;if(dritterIndex=='H')return 1005;if(dritterIndex=='F')return 1006;if(dritterIndex=='~')return elementeintragAnzahl==3?1007:elementeintragAnzahl==5?1008:elementeintragAnzahl==6?1009:elementeintragAnzahl==1?1005:elementeintragAnzahl==4?1006:27;return 27;}return 27;
}
static int ablegenDatenWert(void){
    int dateiKennwert=dateiÖffnen(dateiEintragName,LesenSchreiben|ErstellenFallsFehlend|KürzenInhalt,0600);if(dateiKennwert<0){mitteilungText="Cannot open for save";return 0;}
    intptr_t elementeintragAnzahl=dateiDatenSchreiben(dateiKennwert,Text,Länge);dateiSchließen(dateiKennwert);if(elementeintragAnzahl!=Länge){mitteilungText="Write failed";return 0;}warGeändert=0;mitteilungText="Saved (RAM)";return 1;
}
static int gleich(const char *ersterWert,const char *zweiterWert){while(*ersterWert&&*ersterWert==*zweiterWert){ersterWert++;zweiterWert++;}return *ersterWert==*zweiterWert;}
static void nächsterFinden(void){int elementeintragAnzahl=0;while(eintragFinden[elementeintragAnzahl])elementeintragAnzahl++;if(!elementeintragAnzahl){mitteilungText="No search pattern";return;}for(int ordnungszahlIndex=1;ordnungszahlIndex<=Länge;ordnungszahlIndex++){int datenPosition=(indexWert+ordnungszahlIndex)%(Länge?Länge:1),innerlichOrdnungszahl=0;while(innerlichOrdnungszahl<elementeintragAnzahl&&datenPosition+innerlichOrdnungszahl<Länge&&Text[datenPosition+innerlichOrdnungszahl]==(unsigned char)eintragFinden[innerlichOrdnungszahl])innerlichOrdnungszahl++;if(innerlichOrdnungszahl==elementeintragAnzahl){indexWert=datenPosition;mitteilungText="Match";return;}}mitteilungText="Pattern not found";}
static int eingabeaufforderung(int kategorieWert){
    int elementeintragAnzahl=0;befehl[0]=0;
    for(;;){bewegenWert(zeilennummerAnzahl,1);textAusgeben("\033[0m\033[2K");byteDaten(kategorieWert);textAusgeben(befehl);leeren();hilfeKategorie=kategorieWert;int dritterIndex=gedrücktWert();hilfeKategorie=0;
        if(dritterIndex==27||dritterIndex==3)return 0;if(dritterIndex==13||dritterIndex==10)break;
        if(dritterIndex==127||dritterIndex==8){if(elementeintragAnzahl){elementeintragAnzahl--;while(elementeintragAnzahl>0&&((unsigned char)befehl[elementeintragAnzahl]&192)==128)elementeintragAnzahl--;befehl[elementeintragAnzahl]=0;}continue;}
        if(dritterIndex>=32&&dritterIndex<256&&elementeintragAnzahl<120){befehl[elementeintragAnzahl++]=dritterIndex;befehl[elementeintragAnzahl]=0;}
    }
    if(kategorieWert=='/'){for(int ordnungszahlIndex=0;ordnungszahlIndex<=elementeintragAnzahl;ordnungszahlIndex++)eintragFinden[ordnungszahlIndex]=befehl[ordnungszahlIndex];nächsterFinden();return 0;}
    if(gleich(befehl,"q!"))return 1;
    if(gleich(befehl,"q")){if(!warGeändert)return 1;mitteilungText="Unsaved: :w or :q!";return 0;}
    if(gleich(befehl,"wq")||gleich(befehl,"x"))return ablegenDatenWert();
    if(gleich(befehl,"w")){ablegenDatenWert();return 0;}
    if(befehl[0]=='w'&&befehl[1]==' '){int ordnungszahlIndex=2;while(befehl[ordnungszahlIndex]==' ')ordnungszahlIndex++;int größe=elementeintragAnzahl-ordnungszahlIndex;if(größe<1||größe>63){mitteilungText="Invalid file name";return 0;}for(int innerlichOrdnungszahl=0;innerlichOrdnungszahl<größe;innerlichOrdnungszahl++)dateiEintragName[innerlichOrdnungszahl]=befehl[ordnungszahlIndex+innerlichOrdnungszahl];dateiEintragName[größe]=0;ablegenDatenWert();return 0;}
    int zeile=0;for(int ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++){if(befehl[ordnungszahlIndex]<'0'||befehl[ordnungszahlIndex]>'9'){zeile=0;break;}zeile=zeile*10+befehl[ordnungszahlIndex]-'0';if(zeile>16384){zeile=0;break;}}
    if(zeile){indexWert=0;while(--zeile&&indexWert<Länge){indexWert=endeVersatzwert(indexWert);if(indexWert<Länge)indexWert++;}return 0;}
    mitteilungText="Unknown vi command";return 0;
}
int benutzerProgrammStarten(int ignoriertWert){
    (void)ignoriertWert;if(benutzerArgumentAnzahl()!=1||benutzerArgument(0,dateiEintragName,sizeof(dateiEintragName))<0){textAusgeben("Usage: vi FILE\n");leeren();return 2;}
    int dateiKennwert=dateiÖffnen(dateiEintragName,ausschließlichWertLesen,0);
    if(dateiKennwert>=0){int elementeintragAnzahl=dateiGröße(dateiKennwert);if(elementeintragAnzahl<0||elementeintragAnzahl>editorKapazität){dateiSchließen(dateiKennwert);return 1;}Länge=dateiDatenLesen(dateiKennwert,Text,elementeintragAnzahl);dateiSchließen(dateiKennwert);if(Länge!=elementeintragAnzahl)return 1;for(int ordnungszahlIndex=0;ordnungszahlIndex<Länge;ordnungszahlIndex++)if(!Text[ordnungszahlIndex]){textAusgeben("vi: NUL byte in text file\n");leeren();return 1;}}
    else if(fehlerNummer!=2){textAusgeben("vi: cannot read file\n");leeren();return 1;}
    int abdunkelnFarbe=benutzerAufrufen(16,0,0,0,0,0,0);if(abdunkelnFarbe<0){textAusgeben("vi: use a standalone interactive command\n");leeren();return 1;}spaltenliste=abdunkelnFarbe&65535;zeilennummerAnzahl=(unsigned)abdunkelnFarbe>>16;
    textAusgeben("\033[2J\033[H");leeren();
    int voranstehendTeil=0,aufhörenProgramm=0;
    while(!aufhörenProgramm){bildschirmZeichnen();int dritterIndex=gedrücktWert();if(dritterIndex==27)dritterIndex=maskiert();mitteilungText=0;
        if(dritterIndex==1001){senkrecht(-1);continue;}if(dritterIndex==1002){senkrecht(1);continue;}if(dritterIndex==1003){indexWert=nächsterElementeintrag(indexWert);continue;}if(dritterIndex==1004){indexWert=vorherig(indexWert);continue;}
        if(dritterIndex==1005){indexWert=ausführenVorgang(indexWert);continue;}if(dritterIndex==1006){indexWert=endeVersatzwert(indexWert);continue;}
        if(dritterIndex==1008||dritterIndex==1009){for(int ordnungszahlIndex=0;ordnungszahlIndex<zeilennummerAnzahl-2;ordnungszahlIndex++)senkrecht(dritterIndex==1008?-1:1);continue;}
        if(einfügen){
            if(dritterIndex==27||dritterIndex==3){einfügen=0;continue;}
            if(dritterIndex==127||dritterIndex==8){if(indexWert)bytesLöschenInhalt(vorherig(indexWert),indexWert);continue;}
            if(dritterIndex==1007){if(indexWert<Länge)bytesLöschenInhalt(indexWert,nächsterElementeintrag(indexWert));continue;}
            if(dritterIndex==13)dritterIndex=10;if(dritterIndex==10||dritterIndex==9||(dritterIndex>=32&&dritterIndex<256)){
                unsigned char zweiterWert[4];zweiterWert[0]=dritterIndex;int elementeintragAnzahl=dritterIndex<128?1:dritterIndex>=0xc2&&dritterIndex<0xe0?2:dritterIndex<0xf0?3:dritterIndex<=0xf4?4:0;
                if(!elementeintragAnzahl){mitteilungText="Invalid UTF-8";continue;}int gültig=1;for(int ordnungszahlIndex=1;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++){int zeichenKode=gedrücktWert();if(zeichenKode<128||zeichenKode>191){ausstehendTaste=zeichenKode;gültig=0;break;}zweiterWert[ordnungszahlIndex]=zeichenKode;}
                if(gültig)wertAnhängen(zweiterWert,elementeintragAnzahl);
            }continue;
        }
        if(voranstehendTeil){int datenPosition=voranstehendTeil;voranstehendTeil=0;if(datenPosition=='g'&&dritterIndex=='g'){indexWert=0;continue;}if(datenPosition=='Z'&&dritterIndex=='Z'){aufhörenProgramm=ablegenDatenWert();continue;}if((datenPosition=='d'&&dritterIndex=='d')||(datenPosition=='y'&&dritterIndex=='y')){int ersterWert=ausführenVorgang(indexWert),zweiterWert=endeVersatzwert(indexWert);if(zweiterWert<Länge)zweiterWert++;längeKopieren=zweiterWert-ersterWert;for(int ordnungszahlIndex=0;ordnungszahlIndex<längeKopieren;ordnungszahlIndex++)kopiertDaten[ordnungszahlIndex]=Text[ersterWert+ordnungszahlIndex];if(datenPosition=='d')bytesLöschenInhalt(ersterWert,zweiterWert);continue;}}
        if(dritterIndex=='i'){einfügen=1;continue;}if(dritterIndex=='a'){if(indexWert<endeVersatzwert(indexWert))indexWert=nächsterElementeintrag(indexWert);einfügen=1;continue;}
        if(dritterIndex=='I'){indexWert=ausführenVorgang(indexWert);einfügen=1;continue;}if(dritterIndex=='A'){indexWert=endeVersatzwert(indexWert);einfügen=1;continue;}
        if(dritterIndex=='o'||dritterIndex=='O'){unsigned char zeileEnde='\n';indexWert=dritterIndex=='o'?endeVersatzwert(indexWert):ausführenVorgang(indexWert);if(wertAnhängen(&zeileEnde,1)){if(dritterIndex=='O')indexWert--;einfügen=1;}continue;}
        if(dritterIndex=='h'){indexWert=vorherig(indexWert);continue;}if(dritterIndex=='l'){indexWert=nächsterElementeintrag(indexWert);continue;}if(dritterIndex=='j'){senkrecht(1);continue;}if(dritterIndex=='k'){senkrecht(-1);continue;}
        if(dritterIndex=='0'){indexWert=ausführenVorgang(indexWert);continue;}if(dritterIndex=='$'){indexWert=endeVersatzwert(indexWert);continue;}if(dritterIndex=='G'){indexWert=ausführenVorgang(Länge);continue;}
        if(dritterIndex=='g'||dritterIndex=='d'||dritterIndex=='y'||dritterIndex=='Z'){voranstehendTeil=dritterIndex;continue;}
        if(dritterIndex=='x'||dritterIndex==1007){if(indexWert<Länge)bytesLöschenInhalt(indexWert,nächsterElementeintrag(indexWert));continue;}
        if(dritterIndex=='p'&&längeKopieren){indexWert=endeVersatzwert(indexWert);if(indexWert<Länge)indexWert++;wertAnhängen(kopiertDaten,längeKopieren);continue;}
        if(dritterIndex=='u'&&besitzenRückgängig){for(int ordnungszahlIndex=0;ordnungszahlIndex<editorKapazität;ordnungszahlIndex++){unsigned char zweiterWert=Text[ordnungszahlIndex];Text[ordnungszahlIndex]=rückgängigDaten[ordnungszahlIndex];rückgängigDaten[ordnungszahlIndex]=zweiterWert;}int elementeintragAnzahl=Länge;Länge=rückgängigLänge;rückgängigLänge=elementeintragAnzahl;elementeintragAnzahl=indexWert;indexWert=obererSeiteRand;obererSeiteRand=elementeintragAnzahl;elementeintragAnzahl=warGeändert;warGeändert=rückgängigÄnderungsliste;rückgängigÄnderungsliste=elementeintragAnzahl;continue;}
        if(dritterIndex==':'||dritterIndex=='/'){aufhörenProgramm=eingabeaufforderung(dritterIndex);continue;}if(dritterIndex=='n'){nächsterFinden();continue;}
    }
    textAusgeben("\033[0m\033[?25h\033[2J\033[H");leeren();benutzerAufrufen(16,2,0,0,0,0,0);return 0;
}
