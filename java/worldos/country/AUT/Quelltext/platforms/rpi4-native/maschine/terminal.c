#include "../benennung/maschineBindenNamen.h"
#include "bildschirmInformation.h"
/* eigen 네 fenster 합성과 UTF-8 terminal. 바뀐 영역의 abgeschlossenWert 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t maschineMaschinenwort;
extern maschineMaschinenwort platineBildpunkt(maschineMaschinenwort,maschineMaschinenwort,maschineMaschinenwort),platineBildpuffer(void);
extern void *memset(void *,int,size_t);
extern const unsigned char terminalSchriftart[];
#define höchstwertSpaltenliste 237
#define verlaufZeileAnzahl 160
typedef struct {
    uint32_t zeichenZeichenzellen[verlaufZeileAnzahl][höchstwertSpaltenliste]; uint8_t formenListe[verlaufZeileAnzahl][höchstwertSpaltenliste];
    unsigned breiteWert,höheWert,spaltenliste,zeilennummerAnzahl,warGrößeGeändert;
    unsigned istLebend,waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,zeilennummerPosition,spaltePosition,oberkanteEintrag,rollen,vordergrundFarbe,hintergrundFarbe,maskieren,parameterWert[4],parameterIndex,gespeichertZeilennummer,gespeichertSpaltennummer;
    unsigned vorzeichenlosErgebnis,vorzeichenlosLangWert,kleinformatWert,alternativ,einfügemarkeSichtbar;
} Terminal;
static Terminal fensterlisteListe[4];
static int fokus=-1,ausgabe,reihenfolgeWert[4],eintragAnzahl,ziehenWert=-1,ziehenWaagerechteKoordinate,ziehenSenkrechteKoordinate;
static unsigned istAusstehend,schaltflächen,arbeitsflächeAnsicht,hangulEingabe;
static const uint32_t bildpunktFarbliste[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int bildschirmSichtbar(int),bildschirmZeiger(int,unsigned,int,int);
extern void neuzeichnenBildschirm(int);
static Terminal *terminalEintrag;
static unsigned breitZeichen(unsigned zeichenKode){return zeichenKode>=256?2:1;}
static void rechteckigGebiet(unsigned waagerechteKoordinateKoordinate,unsigned senkrechteKoordinateKoordinate,unsigned angefordertBreiteWert,unsigned angefordertHöheWert,unsigned bildpunktFarbe){
    platineRechteckFüllen(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert,angefordertHöheWert,bildpunktFarbe);
}
void terminalSchriftzeichen(unsigned waagerechteKoordinateKoordinate,unsigned senkrechteKoordinateKoordinate,unsigned zeichenKode,unsigned vordergrundFarbe,unsigned hintergrundFarbe){
    unsigned breiteWert=breitZeichen(zeichenKode)*8;if(zeichenKode==0xffffffffu)return;
    int linksSeiteRand=waagerechteKoordinateKoordinate,obererSeiteRand=senkrechteKoordinateKoordinate,breiteSpannweite=breiteWert,Länge=16;
    if(!platineZeichnungGrenzen(&linksSeiteRand,&obererSeiteRand,&breiteSpannweite,&Länge))return;
    if(zeichenKode==' '){platineRechteckFüllen(linksSeiteRand,obererSeiteRand,breiteSpannweite,Länge,hintergrundFarbe);return;}
    unsigned nachschlagenIndex=zeichenKode<65536?zeichenKode:zeichenKode>=0x1f600&&zeichenKode<0x1f650?65536+zeichenKode-0x1f600:0xfffd;
    const unsigned char *schriftartWert=terminalSchriftart+nachschlagenIndex*32;
    for(int zeile=obererSeiteRand;zeile<obererSeiteRand+Länge;zeile++){unsigned bitlisteListe=schriftartWert[(zeile-senkrechteKoordinateKoordinate)*2]*256+schriftartWert[(zeile-senkrechteKoordinateKoordinate)*2+1];for(int platzEintrag=linksSeiteRand;platzEintrag<linksSeiteRand+breiteSpannweite;platzEintrag++)platineBildpunkt(platzEintrag,zeile,(bitlisteListe&(0x8000>>(platzEintrag-waagerechteKoordinateKoordinate)))?vordergrundFarbe:hintergrundFarbe);}
}
static void nameTabelle(unsigned waagerechteKoordinateKoordinate,unsigned senkrechteKoordinateKoordinate,const char *zeichenketteDaten,unsigned vordergrundFarbe,unsigned hintergrundFarbe){while(*zeichenketteDaten){unsigned zeichenKode=(unsigned char)*zeichenketteDaten++, verbleibendAnzahl=0;if(zeichenKode>=0xc0){verbleibendAnzahl=zeichenKode<0xe0?1:zeichenKode<0xf0?2:3;zeichenKode&=(1u<<(6-verbleibendAnzahl))-1;while(verbleibendAnzahl--&&*zeichenketteDaten)zeichenKode=(zeichenKode<<6)|((unsigned char)*zeichenketteDaten++&63);}terminalSchriftzeichen(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,zeichenKode,vordergrundFarbe,hintergrundFarbe);waagerechteKoordinateKoordinate+=breitZeichen(zeichenKode)*8;}}
static unsigned ersterEintrag(void){return terminalEintrag->oberkanteEintrag;}
static int istAngezeigt(void){return terminalEintrag->istLebend&&fokus>=0&&terminalEintrag==&fensterlisteListe[fokus]&&!bildschirmSichtbar(fokus);}
static void malenBildschirm(unsigned zeilennummerPosition,unsigned spaltePosition){
    if(!istAngezeigt()||zeilennummerPosition<ersterEintrag()-terminalEintrag->rollen||zeilennummerPosition>=ersterEintrag()-terminalEintrag->rollen+terminalEintrag->zeilennummerAnzahl||spaltePosition>=terminalEintrag->spaltenliste)return;
    unsigned zeichenKode=terminalEintrag->zeichenZeichenzellen[zeilennummerPosition%verlaufZeileAnzahl][spaltePosition],zeichenketteDaten=terminalEintrag->formenListe[zeilennummerPosition%verlaufZeileAnzahl][spaltePosition];
    if(breitZeichen(zeichenKode)==2&&spaltePosition+1>=terminalEintrag->spaltenliste)zeichenKode=' ';
    terminalSchriftzeichen(terminalEintrag->waagerechteKoordinateKoordinate+12+spaltePosition*8,terminalEintrag->senkrechteKoordinateKoordinate+36+(zeilennummerPosition-ersterEintrag()+terminalEintrag->rollen)*16,zeichenKode?zeichenKode:' ',bildpunktFarbliste[zeichenketteDaten&15],bildpunktFarbliste[zeichenketteDaten>>4]);
}
static void einfügemarkeWert(int fensterAnzeigen){if(!istAngezeigt()||terminalEintrag->rollen||terminalEintrag->spaltePosition>=terminalEintrag->spaltenliste||terminalEintrag->zeilennummerPosition<terminalEintrag->oberkanteEintrag||terminalEintrag->zeilennummerPosition>=terminalEintrag->oberkanteEintrag+terminalEintrag->zeilennummerAnzahl)return;
    if(!fensterAnzeigen||!terminalEintrag->einfügemarkeSichtbar)malenBildschirm(terminalEintrag->zeilennummerPosition,terminalEintrag->spaltePosition);else rechteckigGebiet(terminalEintrag->waagerechteKoordinateKoordinate+12+terminalEintrag->spaltePosition*8,terminalEintrag->senkrechteKoordinateKoordinate+36+(terminalEintrag->zeilennummerPosition-terminalEintrag->oberkanteEintrag)*16+14,8,2,bildpunktFarbliste[terminalEintrag->vordergrundFarbe]);}
static void inhaltswertWert(void){
    rechteckigGebiet(terminalEintrag->waagerechteKoordinateKoordinate+12,terminalEintrag->senkrechteKoordinateKoordinate+36,terminalEintrag->spaltenliste*8,terminalEintrag->zeilennummerAnzahl*16,bildpunktFarbliste[0]);
    int waagerechtPosition=terminalEintrag->waagerechteKoordinateKoordinate+12,senkrechtPosition=terminalEintrag->senkrechteKoordinateKoordinate+36,breiteSpannweite=terminalEintrag->spaltenliste*8,Länge=terminalEintrag->zeilennummerAnzahl*16;
    if(platineZeichnungGrenzen(&waagerechtPosition,&senkrechtPosition,&breiteSpannweite,&Länge)){
    unsigned ersterZeile=(senkrechtPosition-terminalEintrag->senkrechteKoordinateKoordinate-36)/16,letzterZeile=(senkrechtPosition+Länge-terminalEintrag->senkrechteKoordinateKoordinate-36+15)/16;
    unsigned ersterPlatz=(waagerechtPosition-terminalEintrag->waagerechteKoordinateKoordinate-12)/8,letzterPlatz=(waagerechtPosition+breiteSpannweite-terminalEintrag->waagerechteKoordinateKoordinate-12+7)/8;
    if(ersterPlatz)ersterPlatz--; /* 잘림 grenzstelleWert 왼쪽에서 시작한 두 platzEintrag 글자도 그린다. */
    for(unsigned zurückgegebenWert=ersterZeile;zurückgegebenWert<letzterZeile;zurückgegebenWert++)for(unsigned zeichenKode=ersterPlatz;zeichenKode<letzterPlatz;zeichenKode++){
        unsigned zeilennummerPosition=ersterEintrag()-terminalEintrag->rollen+zurückgegebenWert,zeichenWert=terminalEintrag->zeichenZeichenzellen[zeilennummerPosition%verlaufZeileAnzahl][zeichenKode],zeichenketteDaten=terminalEintrag->formenListe[zeilennummerPosition%verlaufZeileAnzahl][zeichenKode];
        if(breitZeichen(zeichenWert)==2&&zeichenKode+1>=terminalEintrag->spaltenliste)zeichenWert=' ';
        if((zeichenWert==0||zeichenWert==' ')&&(zeichenketteDaten>>4)==0)continue;
        terminalSchriftzeichen(terminalEintrag->waagerechteKoordinateKoordinate+12+zeichenKode*8,terminalEintrag->senkrechteKoordinateKoordinate+36+zurückgegebenWert*16,zeichenWert?zeichenWert:' ',bildpunktFarbliste[zeichenketteDaten&15],bildpunktFarbliste[zeichenketteDaten>>4]);
    }}
    nameTabelle(terminalEintrag->waagerechteKoordinateKoordinate+12,terminalEintrag->senkrechteKoordinateKoordinate+terminalEintrag->höheWert-18,terminalEintrag->rollen?"PgDn: recent output":terminalEintrag->breiteWert>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);einfügemarkeWert(1);
}
static void ausführungRahmen(int bezeichnerWert){
    terminalEintrag=&fensterlisteListe[bezeichnerWert];
    int waagerechtPosition=terminalEintrag->waagerechteKoordinateKoordinate,senkrechtPosition=terminalEintrag->senkrechteKoordinateKoordinate,breiteSpannweite=terminalEintrag->breiteWert,Länge=terminalEintrag->höheWert;
    if(!platineZeichnungGrenzen(&waagerechtPosition,&senkrechtPosition,&breiteSpannweite,&Länge))return;
    rechteckigGebiet(terminalEintrag->waagerechteKoordinateKoordinate,terminalEintrag->senkrechteKoordinateKoordinate,terminalEintrag->breiteWert,terminalEintrag->höheWert,0x403127);
    unsigned bildpunktFarbe=bezeichnerWert==fokus?0x905020:0x604438;rechteckigGebiet(terminalEintrag->waagerechteKoordinateKoordinate,terminalEintrag->senkrechteKoordinateKoordinate,terminalEintrag->breiteWert,30,bildpunktFarbe);
    nameTabelle(terminalEintrag->waagerechteKoordinateKoordinate+12,terminalEintrag->senkrechteKoordinateKoordinate+7,"JKOROS Terminal",0xffffff,bildpunktFarbe);
    char numerischWert[2]={(char)('1'+bezeichnerWert),0};nameTabelle(terminalEintrag->waagerechteKoordinateKoordinate+148,terminalEintrag->senkrechteKoordinateKoordinate+7,numerischWert,0xffffff,bildpunktFarbe);
    nameTabelle(terminalEintrag->waagerechteKoordinateKoordinate+240,terminalEintrag->senkrechteKoordinateKoordinate+7,terminalEintrag->breiteWert>=500?(hangulEingabe?"[DE] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(hangulEingabe?"[DE]":"[EN]"),0xffffff,bildpunktFarbe);
    rechteckigGebiet(terminalEintrag->waagerechteKoordinateKoordinate+terminalEintrag->breiteWert-32,terminalEintrag->senkrechteKoordinateKoordinate+4,26,22,0x5555b8);nameTabelle(terminalEintrag->waagerechteKoordinateKoordinate+terminalEintrag->breiteWert-24,terminalEintrag->senkrechteKoordinateKoordinate+7,"X",0xffffff,0x5555b8);
    inhaltswertWert();
}
static void szeneZeichnen(void){
    if(!arbeitsflächeAnsicht)return;rechteckigGebiet(0,0,platineBildschirmBreite(),platineBildschirmHöhe(),0x302018);rechteckigGebiet(0,0,platineBildschirmBreite(),32,0x403127);
    rechteckigGebiet(6,4,136,24,0x905020);nameTabelle(14,8,"+ New terminal",0xffffff,0x905020);
    for(int ordnungszahlIndex=0;ordnungszahlIndex<4;ordnungszahlIndex++)if(fensterlisteListe[ordnungszahlIndex].istLebend){unsigned zeichenKode=fokus==ordnungszahlIndex?0x905020:0x604438;rechteckigGebiet(154+ordnungszahlIndex*112,4,106,24,zeichenKode);nameTabelle(160+ordnungszahlIndex*112,8,"Terminal",0xffffff,zeichenKode);char zeichenketteDaten[2]={(char)('1'+ordnungszahlIndex),0};nameTabelle(232+ordnungszahlIndex*112,8,zeichenketteDaten,0xffffff,zeichenKode);}
    if(!eintragAnzahl)nameTabelle(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int ordnungszahlIndex=0;ordnungszahlIndex<eintragAnzahl;ordnungszahlIndex++)ausführungRahmen(reihenfolgeWert[ordnungszahlIndex]);neuzeichnenBildschirm(fokus);terminalEintrag=&fensterlisteListe[ausgabe];
}
static void malenGebiet(int waagerechtPosition,int senkrechtPosition,int breiteSpannweite,int Länge){
    if(!arbeitsflächeAnsicht||!platineZeichnungGrenzen(&waagerechtPosition,&senkrechtPosition,&breiteSpannweite,&Länge))return;
    for(int zeile=senkrechtPosition;zeile<senkrechtPosition+Länge;zeile+=32){
        int bandbreiteHöhe=senkrechtPosition+Länge-zeile;if(bandbreiteHöhe>32)bandbreiteHöhe=32;
        if(platineStartenZeichnung(waagerechtPosition,zeile,breiteSpannweite,bandbreiteHöhe)){szeneZeichnen();platineBeendenZeichnung();}
    }
}
static void neuzeichnen(void){malenGebiet(0,0,platineBildschirmBreite(),platineBildschirmHöhe());}
/* 서로 겹치지 않는 새 fenster 영역과 vorherigElementeintrag 자리의 네 띠를 복구한다. */
static void malenFensterGrenzen(int waagerechtPosition,int senkrechtPosition,int breiteSpannweite,int Länge,Terminal *fenster){
    int linksSeiteRand=waagerechtPosition>(int)fenster->waagerechteKoordinateKoordinate?waagerechtPosition:(int)fenster->waagerechteKoordinateKoordinate;
    int obererSeiteRand=senkrechtPosition>(int)fenster->senkrechteKoordinateKoordinate?senkrechtPosition:(int)fenster->senkrechteKoordinateKoordinate;
    int rechts=waagerechtPosition+breiteSpannweite<(int)(fenster->waagerechteKoordinateKoordinate+fenster->breiteWert)?waagerechtPosition+breiteSpannweite:(int)(fenster->waagerechteKoordinateKoordinate+fenster->breiteWert);
    int untererSeiteRand=senkrechtPosition+Länge<(int)(fenster->senkrechteKoordinateKoordinate+fenster->höheWert)?senkrechtPosition+Länge:(int)(fenster->senkrechteKoordinateKoordinate+fenster->höheWert);
    malenGebiet(fenster->waagerechteKoordinateKoordinate,fenster->senkrechteKoordinateKoordinate,fenster->breiteWert,fenster->höheWert);
    if(linksSeiteRand>=rechts||obererSeiteRand>=untererSeiteRand){malenGebiet(waagerechtPosition,senkrechtPosition,breiteSpannweite,Länge);return;}
    malenGebiet(waagerechtPosition,senkrechtPosition,breiteSpannweite,obererSeiteRand-senkrechtPosition);
    malenGebiet(waagerechtPosition,untererSeiteRand,breiteSpannweite,senkrechtPosition+Länge-untererSeiteRand);
    malenGebiet(waagerechtPosition,obererSeiteRand,linksSeiteRand-waagerechtPosition,untererSeiteRand-obererSeiteRand);
    malenGebiet(rechts,obererSeiteRand,waagerechtPosition+breiteSpannweite-rechts,untererSeiteRand-obererSeiteRand);
}
static void signalFokus(void){istAusstehend=(istAusstehend&~15u)|(unsigned)(fokus+1)|0x10000;}
void terminalEingabeBetriebsart(unsigned koreanisch){
    hangulEingabe=koreanisch!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(fokus>=0){
        Terminal *fensterEintrag=&fensterlisteListe[fokus];
        nameTabelle(fensterEintrag->waagerechteKoordinateKoordinate+240,fensterEintrag->senkrechteKoordinateKoordinate+7,fensterEintrag->breiteWert>=500?(hangulEingabe?"[DE] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(hangulEingabe?"[DE]":"[EN]"),0xffffff,0x905020);
    }
}
static void heranholenNachVorderseite(int bezeichnerWert){if(bezeichnerWert<0||bezeichnerWert>=4||!fensterlisteListe[bezeichnerWert].istLebend)return;int aktuellPosition=0;while(aktuellPosition<eintragAnzahl&&reihenfolgeWert[aktuellPosition]!=bezeichnerWert)aktuellPosition++;for(;aktuellPosition+1<eintragAnzahl;aktuellPosition++)reihenfolgeWert[aktuellPosition]=reihenfolgeWert[aktuellPosition+1];reihenfolgeWert[eintragAnzahl-1]=bezeichnerWert;fokus=bezeichnerWert;signalFokus();neuzeichnen();}
static void leer(unsigned zeilennummerPosition){for(unsigned zeichenKode=0;zeichenKode<höchstwertSpaltenliste;zeichenKode++){terminalEintrag->zeichenZeichenzellen[zeilennummerPosition%verlaufZeileAnzahl][zeichenKode]=0;terminalEintrag->formenListe[zeilennummerPosition%verlaufZeileAnzahl][zeichenKode]=terminalEintrag->vordergrundFarbe|(terminalEintrag->hintergrundFarbe<<4);}}
static void inhaltLöschenInhalt(void){terminalEintrag->zeilennummerPosition=terminalEintrag->spaltePosition=terminalEintrag->oberkanteEintrag=terminalEintrag->rollen=0;for(unsigned zurückgegebenWert=0;zurückgegebenWert<verlaufZeileAnzahl;zurückgegebenWert++)leer(zurückgegebenWert);if(istAngezeigt())inhaltswertWert();}
static int eintragErstellen(void){
    if(!platineBildpuffer())return -19;int bezeichnerWert=0;while(bezeichnerWert<4&&fensterlisteListe[bezeichnerWert].istLebend)bezeichnerWert++;if(bezeichnerWert==4)return -28;
    arbeitsflächeAnsicht=1;terminalEintrag=&fensterlisteListe[bezeichnerWert];memset(terminalEintrag,0,sizeof(*terminalEintrag));terminalEintrag->istLebend=1;terminalEintrag->breiteWert=568;terminalEintrag->höheWert=360;terminalEintrag->spaltenliste=68;terminalEintrag->zeilennummerAnzahl=19;terminalEintrag->waagerechteKoordinateKoordinate=12+bezeichnerWert*16;terminalEintrag->senkrechteKoordinateKoordinate=48+bezeichnerWert*18;terminalEintrag->vordergrundFarbe=7;terminalEintrag->einfügemarkeSichtbar=1;
    for(unsigned zurückgegebenWert=0;zurückgegebenWert<verlaufZeileAnzahl;zurückgegebenWert++)leer(zurückgegebenWert);reihenfolgeWert[eintragAnzahl++]=bezeichnerWert;fokus=bezeichnerWert;istAusstehend|=1u<<(4+bezeichnerWert);signalFokus();neuzeichnen();return bezeichnerWert+1;
}
static void fensterSchließen(int bezeichnerWert){
    if(bezeichnerWert<0||bezeichnerWert>=4||!fensterlisteListe[bezeichnerWert].istLebend)return;fensterlisteListe[bezeichnerWert].istLebend=0;istAusstehend|=1u<<(8+bezeichnerWert);
    int aktuellPosition=0;while(aktuellPosition<eintragAnzahl&&reihenfolgeWert[aktuellPosition]!=bezeichnerWert)aktuellPosition++;for(;aktuellPosition+1<eintragAnzahl;aktuellPosition++)reihenfolgeWert[aktuellPosition]=reihenfolgeWert[aktuellPosition+1];eintragAnzahl--;
    if(fokus==bezeichnerWert)fokus=eintragAnzahl?reihenfolgeWert[eintragAnzahl-1]:-1;signalFokus();neuzeichnen();
}
static void zeilenumbruch(void){terminalEintrag->spaltePosition=0;terminalEintrag->zeilennummerPosition++;if(terminalEintrag->zeilennummerPosition>=terminalEintrag->oberkanteEintrag+terminalEintrag->zeilennummerAnzahl){terminalEintrag->oberkanteEintrag++;leer(terminalEintrag->zeilennummerPosition);if(istAngezeigt())inhaltswertWert();}}
static void kodePunkt(unsigned zeichenKode){
    if(zeichenKode==13){terminalEintrag->spaltePosition=0;return;}if(zeichenKode==10){zeilenumbruch();return;}if(zeichenKode==8){if(terminalEintrag->spaltePosition)terminalEintrag->spaltePosition--;return;}
    if(zeichenKode==9){unsigned elementeintragAnzahl=8-terminalEintrag->spaltePosition%8;while(elementeintragAnzahl--)kodePunkt(' ');return;}if(zeichenKode<32||zeichenKode==127)return;
    unsigned angefordertBreiteWert=breitZeichen(zeichenKode);if(terminalEintrag->spaltePosition+angefordertBreiteWert>terminalEintrag->spaltenliste)zeilenumbruch();
    if(terminalEintrag->zeichenZeichenzellen[terminalEintrag->zeilennummerPosition%verlaufZeileAnzahl][terminalEintrag->spaltePosition]==0xffffffffu&&terminalEintrag->spaltePosition){terminalEintrag->zeichenZeichenzellen[terminalEintrag->zeilennummerPosition%verlaufZeileAnzahl][terminalEintrag->spaltePosition-1]=' ';malenBildschirm(terminalEintrag->zeilennummerPosition,terminalEintrag->spaltePosition-1);}
    if(breitZeichen(terminalEintrag->zeichenZeichenzellen[terminalEintrag->zeilennummerPosition%verlaufZeileAnzahl][terminalEintrag->spaltePosition])==2&&terminalEintrag->spaltePosition+1<terminalEintrag->spaltenliste){terminalEintrag->zeichenZeichenzellen[terminalEintrag->zeilennummerPosition%verlaufZeileAnzahl][terminalEintrag->spaltePosition+1]=' ';malenBildschirm(terminalEintrag->zeilennummerPosition,terminalEintrag->spaltePosition+1);}
    terminalEintrag->zeichenZeichenzellen[terminalEintrag->zeilennummerPosition%verlaufZeileAnzahl][terminalEintrag->spaltePosition]=zeichenKode;terminalEintrag->formenListe[terminalEintrag->zeilennummerPosition%verlaufZeileAnzahl][terminalEintrag->spaltePosition]=terminalEintrag->vordergrundFarbe|(terminalEintrag->hintergrundFarbe<<4);
    if(angefordertBreiteWert==2)terminalEintrag->zeichenZeichenzellen[terminalEintrag->zeilennummerPosition%verlaufZeileAnzahl][terminalEintrag->spaltePosition+1]=0xffffffffu;
    malenBildschirm(terminalEintrag->zeilennummerPosition,terminalEintrag->spaltePosition);terminalEintrag->spaltePosition+=angefordertBreiteWert;
}
static void kennwertSteuerungFolge(unsigned zeichenKode){
    unsigned elementeintragAnzahl=terminalEintrag->parameterWert[0]?terminalEintrag->parameterWert[0]:1;
    if(zeichenKode=='m')for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<=terminalEintrag->parameterIndex;ordnungszahlIndex++){unsigned datenPosition=terminalEintrag->parameterWert[ordnungszahlIndex];if(!datenPosition){terminalEintrag->vordergrundFarbe=7;terminalEintrag->hintergrundFarbe=0;}if(datenPosition==1&&terminalEintrag->vordergrundFarbe<8)terminalEintrag->vordergrundFarbe+=8;if(datenPosition==7){unsigned wertBeibehalten=terminalEintrag->vordergrundFarbe;terminalEintrag->vordergrundFarbe=terminalEintrag->hintergrundFarbe;terminalEintrag->hintergrundFarbe=wertBeibehalten;}if(datenPosition>=30&&datenPosition<=37)terminalEintrag->vordergrundFarbe=datenPosition-30;if(datenPosition>=90&&datenPosition<=97)terminalEintrag->vordergrundFarbe=datenPosition-90+8;if(datenPosition>=40&&datenPosition<=47)terminalEintrag->hintergrundFarbe=datenPosition-40;if(datenPosition>=100&&datenPosition<=107)terminalEintrag->hintergrundFarbe=datenPosition-100+8;if(datenPosition==39)terminalEintrag->vordergrundFarbe=7;if(datenPosition==49)terminalEintrag->hintergrundFarbe=0;}
    if(zeichenKode=='J'&&(terminalEintrag->parameterWert[0]==2||terminalEintrag->parameterWert[0]==3))inhaltLöschenInhalt();
    if(zeichenKode=='K'){unsigned abgangPosition=terminalEintrag->parameterWert[0]==2?0:terminalEintrag->spaltePosition,ankunftPosition=terminalEintrag->parameterWert[0]==1?terminalEintrag->spaltePosition+1:terminalEintrag->spaltenliste;if(terminalEintrag->parameterWert[0]==1)abgangPosition=0;for(unsigned ordnungszahlIndex=abgangPosition;ordnungszahlIndex<ankunftPosition&&ordnungszahlIndex<terminalEintrag->spaltenliste;ordnungszahlIndex++){
        unsigned zeilennummerWert=terminalEintrag->zeilennummerPosition%verlaufZeileAnzahl,zeichenWert=terminalEintrag->zeichenZeichenzellen[zeilennummerWert][ordnungszahlIndex],formWert=terminalEintrag->vordergrundFarbe|(terminalEintrag->hintergrundFarbe<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 schriftartWert 화소를 되풀이해 칠하지 않는다. */
        int istVerändert=(zeichenWert!=0&&zeichenWert!=' ')||terminalEintrag->formenListe[zeilennummerWert][ordnungszahlIndex]!=formWert;
        terminalEintrag->zeichenZeichenzellen[zeilennummerWert][ordnungszahlIndex]=' ';terminalEintrag->formenListe[zeilennummerWert][ordnungszahlIndex]=formWert;
        if(istVerändert)malenBildschirm(terminalEintrag->zeilennummerPosition,ordnungszahlIndex);
    }}
    if(zeichenKode=='D')terminalEintrag->spaltePosition=elementeintragAnzahl>terminalEintrag->spaltePosition?0:terminalEintrag->spaltePosition-elementeintragAnzahl;if(zeichenKode=='C')terminalEintrag->spaltePosition=terminalEintrag->spaltePosition+elementeintragAnzahl>=terminalEintrag->spaltenliste?terminalEintrag->spaltenliste-1:terminalEintrag->spaltePosition+elementeintragAnzahl;
    if(zeichenKode=='G')terminalEintrag->spaltePosition=elementeintragAnzahl>terminalEintrag->spaltenliste?terminalEintrag->spaltenliste-1:elementeintragAnzahl-1;if(zeichenKode=='A')terminalEintrag->zeilennummerPosition=elementeintragAnzahl>terminalEintrag->zeilennummerPosition-terminalEintrag->oberkanteEintrag?terminalEintrag->oberkanteEintrag:terminalEintrag->zeilennummerPosition-elementeintragAnzahl;
    if(zeichenKode=='B')terminalEintrag->zeilennummerPosition=terminalEintrag->zeilennummerPosition+elementeintragAnzahl>=terminalEintrag->oberkanteEintrag+terminalEintrag->zeilennummerAnzahl?terminalEintrag->oberkanteEintrag+terminalEintrag->zeilennummerAnzahl-1:terminalEintrag->zeilennummerPosition+elementeintragAnzahl;
    if(zeichenKode=='H'||zeichenKode=='f'){terminalEintrag->zeilennummerPosition=terminalEintrag->oberkanteEintrag+(elementeintragAnzahl>terminalEintrag->zeilennummerAnzahl?terminalEintrag->zeilennummerAnzahl:elementeintragAnzahl)-1;unsigned waagerechteKoordinateKoordinate=terminalEintrag->parameterWert[1]?terminalEintrag->parameterWert[1]:1;terminalEintrag->spaltePosition=(waagerechteKoordinateKoordinate>terminalEintrag->spaltenliste?terminalEintrag->spaltenliste:waagerechteKoordinateKoordinate)-1;}
    if(zeichenKode=='s'){terminalEintrag->gespeichertZeilennummer=terminalEintrag->zeilennummerPosition;terminalEintrag->gespeichertSpaltennummer=terminalEintrag->spaltePosition;}if(zeichenKode=='u'){terminalEintrag->zeilennummerPosition=terminalEintrag->gespeichertZeilennummer;terminalEintrag->spaltePosition=terminalEintrag->gespeichertSpaltennummer<terminalEintrag->spaltenliste?terminalEintrag->gespeichertSpaltennummer:terminalEintrag->spaltenliste-1;}
    if((zeichenKode=='h'||zeichenKode=='l')&&terminalEintrag->parameterWert[0]==25)terminalEintrag->einfügemarkeSichtbar=zeichenKode=='h';
}
void terminalByte(unsigned zweiterWert){
    terminalEintrag=&fensterlisteListe[ausgabe];if(!terminalEintrag->istLebend)return;einfügemarkeWert(0);if(terminalEintrag->rollen){terminalEintrag->rollen=0;if(istAngezeigt())inhaltswertWert();}
    if(terminalEintrag->maskieren==1){terminalEintrag->maskieren=zweiterWert=='['?2:0;terminalEintrag->parameterIndex=0;for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<4;ordnungszahlIndex++)terminalEintrag->parameterWert[ordnungszahlIndex]=0;}
    else if(terminalEintrag->maskieren==2){if(zweiterWert=='?'){}else if(zweiterWert>='0'&&zweiterWert<='9'){if(terminalEintrag->parameterWert[terminalEintrag->parameterIndex]<10000)terminalEintrag->parameterWert[terminalEintrag->parameterIndex]=terminalEintrag->parameterWert[terminalEintrag->parameterIndex]*10+zweiterWert-'0';}else if(zweiterWert==';'&&terminalEintrag->parameterIndex<3)terminalEintrag->parameterIndex++;else{kennwertSteuerungFolge(zweiterWert);terminalEintrag->maskieren=0;}}
    else if(zweiterWert==27){terminalEintrag->vorzeichenlosLangWert=0;terminalEintrag->maskieren=1;}else{
        if(terminalEintrag->vorzeichenlosLangWert&&(zweiterWert&0xc0)!=0x80){terminalEintrag->vorzeichenlosLangWert=0;kodePunkt(0xfffd);}
        if(terminalEintrag->vorzeichenlosLangWert){terminalEintrag->vorzeichenlosErgebnis=terminalEintrag->vorzeichenlosErgebnis*64+(zweiterWert&63);if(--terminalEintrag->vorzeichenlosLangWert==0)kodePunkt(terminalEintrag->vorzeichenlosErgebnis<terminalEintrag->kleinformatWert||terminalEintrag->vorzeichenlosErgebnis>0x10ffff||(terminalEintrag->vorzeichenlosErgebnis>=0xd800&&terminalEintrag->vorzeichenlosErgebnis<=0xdfff)?0xfffd:terminalEintrag->vorzeichenlosErgebnis);}
        else if(zweiterWert<128)kodePunkt(zweiterWert);else if(zweiterWert>=0xc2&&zweiterWert<=0xf4){terminalEintrag->vorzeichenlosLangWert=zweiterWert<0xe0?1:zweiterWert<0xf0?2:3;terminalEintrag->vorzeichenlosErgebnis=zweiterWert&((1u<<(6-terminalEintrag->vorzeichenlosLangWert))-1);terminalEintrag->kleinformatWert=terminalEintrag->vorzeichenlosLangWert==1?128:terminalEintrag->vorzeichenlosLangWert==2?2048:65536;}else kodePunkt(0xfffd);
    }einfügemarkeWert(1);
}
int terminalAusstehend(void){return istAusstehend!=0;}
/* eckeWert Nummer: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int größeÄndernZiehen=-1,ergriffenEcke,ergriffenWaagerechteKoordinate,ergriffenSenkrechteKoordinate,anfänglichWaagerechtPosition,anfänglichSenkrechtPosition,anfänglichBreiteWert,anfänglichHöheWert;
static int gezeigtFenster(int waagerechtPosition,int senkrechtPosition) {
    for(int folgeWert=eintragAnzahl-1;folgeWert>=0;folgeWert--){
        int bezeichnerWert=reihenfolgeWert[folgeWert];Terminal *fenster=&fensterlisteListe[bezeichnerWert];
        if(waagerechtPosition>=(int)fenster->waagerechteKoordinateKoordinate&&senkrechtPosition>=(int)fenster->senkrechteKoordinateKoordinate&&
           waagerechtPosition<(int)(fenster->waagerechteKoordinateKoordinate+fenster->breiteWert)&&senkrechtPosition<(int)(fenster->senkrechteKoordinateKoordinate+fenster->höheWert))return bezeichnerWert;
    }return -1;
}
static int eckeFinden(int bezeichnerWert,int waagerechtPosition,int senkrechtPosition) {
    if(bezeichnerWert<0)return 0;Terminal *fenster=&fensterlisteListe[bezeichnerWert];
    int linksSeiteRand=waagerechtPosition<(int)fenster->waagerechteKoordinateKoordinate+8,rechts=waagerechtPosition>=(int)(fenster->waagerechteKoordinateKoordinate+fenster->breiteWert)-8;
    int obererSeiteRand=senkrechtPosition<(int)fenster->senkrechteKoordinateKoordinate+8,untererSeiteRand=senkrechtPosition>=(int)(fenster->senkrechteKoordinateKoordinate+fenster->höheWert)-8;
    return (linksSeiteRand||rechts)&&(obererSeiteRand||untererSeiteRand)?1+rechts+untererSeiteRand*2:0;
}
static int trennerWert(int Wert,int mindestwertWert,int höchstwertWert){return Wert<mindestwertWert?mindestwertWert:Wert>höchstwertWert?höchstwertWert:Wert;}
static void bewegenGrößeÄndern(int waagerechtPosition,int senkrechtPosition) {
    Terminal *fenster=&fensterlisteListe[größeÄndernZiehen];int linksSeiteRand=anfänglichWaagerechtPosition,obererSeiteRand=anfänglichSenkrechtPosition,rechts=anfänglichWaagerechtPosition+anfänglichBreiteWert,untererSeiteRand=anfänglichSenkrechtPosition+anfänglichHöheWert;
    if(ergriffenEcke==1||ergriffenEcke==3)linksSeiteRand=trennerWert(anfänglichWaagerechtPosition+waagerechtPosition-ergriffenWaagerechteKoordinate,0,rechts-360);
    else rechts=trennerWert(anfänglichWaagerechtPosition+anfänglichBreiteWert+waagerechtPosition-ergriffenWaagerechteKoordinate,linksSeiteRand+360,platineBildschirmBreite());
    if(ergriffenEcke<=2)obererSeiteRand=trennerWert(anfänglichSenkrechtPosition+senkrechtPosition-ergriffenSenkrechteKoordinate,34,untererSeiteRand-216);
    else untererSeiteRand=trennerWert(anfänglichSenkrechtPosition+anfänglichHöheWert+senkrechtPosition-ergriffenSenkrechteKoordinate,obererSeiteRand+216,platineBildschirmHöhe());
    unsigned spaltenliste=(rechts-linksSeiteRand-24)/8,zeilennummerAnzahl=(untererSeiteRand-obererSeiteRand-56)/16;
    if(fenster->spaltenliste!=spaltenliste||fenster->zeilennummerAnzahl!=zeilennummerAnzahl){
        fenster->warGrößeGeändert=1;fenster->spaltenliste=spaltenliste;fenster->zeilennummerAnzahl=zeilennummerAnzahl;
        if(fenster->spaltePosition>=spaltenliste)fenster->spaltePosition=spaltenliste-1;
        if(fenster->zeilennummerPosition>=fenster->oberkanteEintrag+zeilennummerAnzahl)fenster->oberkanteEintrag=fenster->zeilennummerPosition-zeilennummerAnzahl+1;
        unsigned kapazitätGrenzwert=fenster->oberkanteEintrag;if(kapazitätGrenzwert>verlaufZeileAnzahl-zeilennummerAnzahl)kapazitätGrenzwert=verlaufZeileAnzahl-zeilennummerAnzahl;
        if(fenster->rollen>kapazitätGrenzwert)fenster->rollen=kapazitätGrenzwert;
    }
    int altWaagerechtPosition=fenster->waagerechteKoordinateKoordinate,altSenkrechtPosition=fenster->senkrechteKoordinateKoordinate,altBreite=fenster->breiteWert,altLänge=fenster->höheWert;
    if(altWaagerechtPosition==linksSeiteRand&&altSenkrechtPosition==obererSeiteRand&&altBreite==rechts-linksSeiteRand&&altLänge==untererSeiteRand-obererSeiteRand)return;
    fenster->waagerechteKoordinateKoordinate=linksSeiteRand;fenster->senkrechteKoordinateKoordinate=obererSeiteRand;fenster->breiteWert=rechts-linksSeiteRand;fenster->höheWert=untererSeiteRand-obererSeiteRand;
    malenFensterGrenzen(altWaagerechtPosition,altSenkrechtPosition,altBreite,altLänge,fenster);
}
void terminalZeiger(unsigned nächsterElementeintrag,int waagerechteKoordinateKoordinate,int senkrechteKoordinateKoordinate){
    unsigned istGedrückt=nächsterElementeintrag&~schaltflächen;schaltflächen=nächsterElementeintrag;
    if(!arbeitsflächeAnsicht){ziehenWert=-1;größeÄndernZiehen=-1;platineZeiger(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,1);return;}
    if(!(nächsterElementeintrag&1)){ziehenWert=-1;größeÄndernZiehen=-1;}
    if(größeÄndernZiehen>=0&&!fensterlisteListe[größeÄndernZiehen].istLebend)größeÄndernZiehen=-1;
    if(ziehenWert>=0&&!fensterlisteListe[ziehenWert].istLebend)ziehenWert=-1;
    if(größeÄndernZiehen>=0){
        bewegenGrößeÄndern(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate);platineZeiger(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,ergriffenEcke==1||ergriffenEcke==4?2:3);return;
    }
    platineZeiger(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,1);
    if(ziehenWert>=0){
        Terminal *fenster=&fensterlisteListe[ziehenWert];
        int altWaagerechtPosition=fenster->waagerechteKoordinateKoordinate,altSenkrechtPosition=fenster->senkrechteKoordinateKoordinate;
        fenster->waagerechteKoordinateKoordinate=trennerWert(waagerechteKoordinateKoordinate-ziehenWaagerechteKoordinate,0,platineBildschirmBreite()-fenster->breiteWert);
        fenster->senkrechteKoordinateKoordinate=trennerWert(senkrechteKoordinateKoordinate-ziehenSenkrechteKoordinate,34,platineBildschirmHöhe()-fenster->höheWert);
        if(altWaagerechtPosition!=(int)fenster->waagerechteKoordinateKoordinate||altSenkrechtPosition!=(int)fenster->senkrechteKoordinateKoordinate)malenFensterGrenzen(altWaagerechtPosition,altSenkrechtPosition,fenster->breiteWert,fenster->höheWert,fenster);
        return;
    }
    extern int bildschirmÜberlagern(int,int,int);
    if(bildschirmÜberlagern(fokus,waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate)){bildschirmZeiger(fokus,istGedrückt,waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate);return;}
    int bezeichnerWert=gezeigtFenster(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate),eckeWert=eckeFinden(bezeichnerWert,waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate);
    if(eckeWert)platineZeiger(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,eckeWert==1||eckeWert==4?2:3);
    if(istGedrückt&1){
        if(eckeWert){
            Terminal *fenster=&fensterlisteListe[bezeichnerWert];größeÄndernZiehen=bezeichnerWert;ergriffenEcke=eckeWert;ergriffenWaagerechteKoordinate=waagerechteKoordinateKoordinate;ergriffenSenkrechteKoordinate=senkrechteKoordinateKoordinate;
            anfänglichWaagerechtPosition=fenster->waagerechteKoordinateKoordinate;anfänglichSenkrechtPosition=fenster->senkrechteKoordinateKoordinate;anfänglichBreiteWert=fenster->breiteWert;anfänglichHöheWert=fenster->höheWert;
            if(bezeichnerWert!=fokus)heranholenNachVorderseite(bezeichnerWert);return;
        }
        if(senkrechteKoordinateKoordinate<32&&waagerechteKoordinateKoordinate>=6&&waagerechteKoordinateKoordinate<142){eintragErstellen();return;}
        if(senkrechteKoordinateKoordinate<32&&waagerechteKoordinateKoordinate>=154&&waagerechteKoordinateKoordinate<602){heranholenNachVorderseite((waagerechteKoordinateKoordinate-154)/112);return;}
        if(bezeichnerWert>=0){
            Terminal *fenster=&fensterlisteListe[bezeichnerWert];
            if(senkrechteKoordinateKoordinate<(int)fenster->senkrechteKoordinateKoordinate+30&&waagerechteKoordinateKoordinate>=(int)(fenster->waagerechteKoordinateKoordinate+fenster->breiteWert)-32){fensterSchließen(bezeichnerWert);return;}
            if(bezeichnerWert!=fokus)heranholenNachVorderseite(bezeichnerWert);
            if(senkrechteKoordinateKoordinate<(int)fenster->senkrechteKoordinateKoordinate+30){ziehenWert=bezeichnerWert;ziehenWaagerechteKoordinate=waagerechteKoordinateKoordinate-fenster->waagerechteKoordinateKoordinate;ziehenSenkrechteKoordinate=senkrechteKoordinateKoordinate-fenster->senkrechteKoordinateKoordinate;}return;
        }
    }
    if(fokus>=0&&(istGedrückt&(8|16))){terminalEintrag=&fensterlisteListe[fokus];if(istGedrückt&8){unsigned kapazitätGrenzwert=terminalEintrag->oberkanteEintrag;if(kapazitätGrenzwert>verlaufZeileAnzahl-terminalEintrag->zeilennummerAnzahl)kapazitätGrenzwert=verlaufZeileAnzahl-terminalEintrag->zeilennummerAnzahl;terminalEintrag->rollen=terminalEintrag->rollen+9>kapazitätGrenzwert?kapazitätGrenzwert:terminalEintrag->rollen+9;}else terminalEintrag->rollen=terminalEintrag->rollen<9?0:terminalEintrag->rollen-9;neuzeichnen();}
}
void terminalTastenkürzel(unsigned gedrücktWert){if(gedrücktWert==1)eintragErstellen();if(gedrücktWert==2&&eintragAnzahl)heranholenNachVorderseite(reihenfolgeWert[0]);if(gedrücktWert==3)fensterSchließen(fokus);}
maschineMaschinenwort platineTerminal(maschineMaschinenwort aktion){
    if(aktion==300){if(!fensterlisteListe[ausgabe].istLebend)return eintragErstellen();arbeitsflächeAnsicht=1;neuzeichnen();return 0;}
    if(aktion==0){fensterSchließen(fokus);return 0;}if(aktion==1)return (uint32_t)eintragErstellen();if(aktion==2)return fokus>=0;
    if(aktion==9){arbeitsflächeAnsicht=0;return 0;}if(aktion==7)return eintragAnzahl;if(aktion==10)return fokus+1;if(aktion==11)return ausgabe;
    if(aktion==13){Terminal *fenster=&fensterlisteListe[ausgabe];return fenster->istLebend?(fenster->zeilennummerAnzahl<<16)|fenster->spaltenliste:(19<<16)|68;}
    if(aktion==14){unsigned Wert=fensterlisteListe[ausgabe].warGrößeGeändert;fensterlisteListe[ausgabe].warGrößeGeändert=0;return Wert;}
    if(aktion==12){unsigned Wert=istAusstehend;istAusstehend=0;return Wert;}
    if(aktion>=20&&aktion<24)return fensterlisteListe[aktion-20].istLebend;
    if(aktion>=100&&aktion<104){ausgabe=aktion-100;terminalEintrag=&fensterlisteListe[ausgabe];return 0;}
    if(aktion>=200&&aktion<204){heranholenNachVorderseite(aktion-200);return 0;}
    if(aktion==3){neuzeichnen();return 0;}terminalEintrag=&fensterlisteListe[ausgabe];if(!terminalEintrag->istLebend)return 0;
    if(aktion==4)inhaltLöschenInhalt();if(aktion==5||aktion==6){unsigned vorherigElementeintrag=schaltflächen;terminalZeiger(aktion==5?8:16,0,0);schaltflächen=vorherigElementeintrag;}return 1;
}
