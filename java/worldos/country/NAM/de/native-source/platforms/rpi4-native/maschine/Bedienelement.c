#include "../benennung/maschineBindenNamen.h"
#include "bildschirmInformation.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t platineBildpunkt(uintptr_t,uintptr_t,uintptr_t),platineTerminal(uintptr_t);
extern void terminalSchriftzeichen(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kategorieWert,elternknoten,waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert,angefordertHöheWert,istAngezeigt,handbuchAnordnung,anordnungRichtlinie;unsigned Text[128],Länge; } bedienelementStatuswert;
static bedienelementStatuswert knotenliste[4][32];
static int fokussiert[4],ereignisListe[4][16];static unsigned ersterEintrag[4],eintragAnzahl[4],vorzeichenlosErgebnis[4],vorzeichenlosLangWert[4];
static void ereignis(int eigentümerObjekt,int Wert){if(eintragAnzahl[eigentümerObjekt]<16){ereignisListe[eigentümerObjekt][(ersterEintrag[eigentümerObjekt]+eintragAnzahl[eigentümerObjekt])%16]=Wert;eintragAnzahl[eigentümerObjekt]++;}}
static bedienelementStatuswert *elementWert(int eigentümerObjekt,int bezeichnerWert){return eigentümerObjekt>=0&&eigentümerObjekt<4&&bezeichnerWert>0&&bezeichnerWert<=32&&knotenliste[eigentümerObjekt][bezeichnerWert-1].kategorieWert?&knotenliste[eigentümerObjekt][bezeichnerWert-1]:0;}
static void rechteckigGebiet(int waagerechteKoordinateKoordinate,int senkrechteKoordinateKoordinate,int angefordertBreiteWert,int angefordertHöheWert,unsigned bildpunktFarbe){platineRechteckFüllen(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert,angefordertHöheWert,bildpunktFarbe);}
int bildschirmSichtbar(int eigentümerObjekt){if(eigentümerObjekt<0||eigentümerObjekt>=4)return 0;for(int ordnungszahlIndex=0;ordnungszahlIndex<32;ordnungszahlIndex++)if(knotenliste[eigentümerObjekt][ordnungszahlIndex].kategorieWert==1&&knotenliste[eigentümerObjekt][ordnungszahlIndex].istAngezeigt)return 1;return 0;}
void bildschirmInitialisieren(int eigentümerObjekt){memset(knotenliste[eigentümerObjekt],0,sizeof(knotenliste[eigentümerObjekt]));eintragAnzahl[eigentümerObjekt]=ersterEintrag[eigentümerObjekt]=fokussiert[eigentümerObjekt]=vorzeichenlosLangWert[eigentümerObjekt]=0;}
static void position(int eigentümerObjekt,bedienelementStatuswert *angefordertBreiteWert,int *waagerechteKoordinateKoordinate,int *senkrechteKoordinateKoordinate){*waagerechteKoordinateKoordinate=angefordertBreiteWert->waagerechteKoordinateKoordinate;*senkrechteKoordinateKoordinate=angefordertBreiteWert->senkrechteKoordinateKoordinate;int datenPosition=angefordertBreiteWert->elternknoten;for(int elementeintragAnzahl=0;datenPosition&&elementeintragAnzahl<32;elementeintragAnzahl++){bedienelementStatuswert *obererSeiteRand=elementWert(eigentümerObjekt,datenPosition);if(!obererSeiteRand)break;*waagerechteKoordinateKoordinate+=obererSeiteRand->waagerechteKoordinateKoordinate;*senkrechteKoordinateKoordinate+=obererSeiteRand->senkrechteKoordinateKoordinate+(obererSeiteRand->kategorieWert==1?30:0);datenPosition=obererSeiteRand->elternknoten;}}
static int istDargestellt(int eigentümerObjekt,bedienelementStatuswert *angefordertBreiteWert){for(int elementeintragAnzahl=0;elementeintragAnzahl<32;elementeintragAnzahl++){if(!angefordertBreiteWert->istAngezeigt)return 0;if(angefordertBreiteWert->kategorieWert==1)return 1;angefordertBreiteWert=elementWert(eigentümerObjekt,angefordertBreiteWert->elternknoten);if(!angefordertBreiteWert)return 0;}return 0;}
static void Text(int waagerechteKoordinateKoordinate,int senkrechteKoordinateKoordinate,bedienelementStatuswert *angefordertBreiteWert,int höchstwertDaten,unsigned bildpunktFarbe,unsigned hintergrundFarbe){int aktuellPosition=0;for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<angefordertBreiteWert->Länge;ordnungszahlIndex++){unsigned zeichenKodierung=angefordertBreiteWert->Text[ordnungszahlIndex],breiteWert=zeichenKodierung>=256?16:8;if(aktuellPosition+(int)breiteWert>höchstwertDaten)break;terminalSchriftzeichen(waagerechteKoordinateKoordinate+aktuellPosition,senkrechteKoordinateKoordinate,zeichenKodierung,bildpunktFarbe,hintergrundFarbe);aktuellPosition+=breiteWert;}}
void neuzeichnenBildschirm(int eigentümerObjekt){
    if(!bildschirmSichtbar(eigentümerObjekt))return;
    for(int verarbeitungReihenfolge=1;verarbeitungReihenfolge<=5;verarbeitungReihenfolge++)for(int ordnungszahlIndex=0;ordnungszahlIndex<32;ordnungszahlIndex++){
        bedienelementStatuswert *angefordertBreiteWert=&knotenliste[eigentümerObjekt][ordnungszahlIndex];if(angefordertBreiteWert->kategorieWert!=verarbeitungReihenfolge||!istDargestellt(eigentümerObjekt,angefordertBreiteWert))continue;int waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate;position(eigentümerObjekt,angefordertBreiteWert,&waagerechteKoordinateKoordinate,&senkrechteKoordinateKoordinate);
        if(verarbeitungReihenfolge==1){rechteckigGebiet(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert->angefordertBreiteWert,angefordertBreiteWert->angefordertHöheWert,0xeee9e0);rechteckigGebiet(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert->angefordertBreiteWert,30,0x905020);Text(waagerechteKoordinateKoordinate+10,senkrechteKoordinateKoordinate+7,angefordertBreiteWert,angefordertBreiteWert->angefordertBreiteWert-50,0xffffff,0x905020);rechteckigGebiet(waagerechteKoordinateKoordinate+angefordertBreiteWert->angefordertBreiteWert-28,senkrechteKoordinateKoordinate+4,24,22,0x5555b8);terminalSchriftzeichen(waagerechteKoordinateKoordinate+angefordertBreiteWert->angefordertBreiteWert-20,senkrechteKoordinateKoordinate+7,'X',0xffffff,0x5555b8);}
        if(verarbeitungReihenfolge==2)rechteckigGebiet(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert->angefordertBreiteWert,angefordertBreiteWert->angefordertHöheWert,0xeee9e0);
        if(verarbeitungReihenfolge>=3){unsigned hintergrundFarbe=verarbeitungReihenfolge==4?0xc0ab86:verarbeitungReihenfolge==5?0xffffff:0xeee9e0;if(verarbeitungReihenfolge!=3)rechteckigGebiet(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert->angefordertBreiteWert,angefordertBreiteWert->angefordertHöheWert,hintergrundFarbe);Text(waagerechteKoordinateKoordinate+4,senkrechteKoordinateKoordinate+4,angefordertBreiteWert,angefordertBreiteWert->angefordertBreiteWert-8,0x201a15,hintergrundFarbe);if(verarbeitungReihenfolge==5&&fokussiert[eigentümerObjekt]==ordnungszahlIndex+1)rechteckigGebiet(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate+angefordertBreiteWert->angefordertHöheWert-2,angefordertBreiteWert->angefordertBreiteWert,2,0x905020);}
    }
}
int bildschirmÜberlagern(int eigentümerObjekt,int waagerechteKoordinateKoordinate,int senkrechteKoordinateKoordinate){
    if(!bildschirmSichtbar(eigentümerObjekt))return 0;
    for(int ordnungszahlIndex=0;ordnungszahlIndex<32;ordnungszahlIndex++){
        bedienelementStatuswert *fenster=&knotenliste[eigentümerObjekt][ordnungszahlIndex];
        if(fenster->kategorieWert==1&&fenster->istAngezeigt&&waagerechteKoordinateKoordinate>=fenster->waagerechteKoordinateKoordinate&&senkrechteKoordinateKoordinate>=fenster->senkrechteKoordinateKoordinate&&
           waagerechteKoordinateKoordinate<fenster->waagerechteKoordinateKoordinate+fenster->angefordertBreiteWert&&senkrechteKoordinateKoordinate<fenster->senkrechteKoordinateKoordinate+fenster->angefordertHöheWert)return 1;
    }return 0;
}
int bildschirmZeiger(int eigentümerObjekt,unsigned istGedrückt,int waagerechteKoordinateKoordinate,int senkrechteKoordinateKoordinate){
    if(!bildschirmSichtbar(eigentümerObjekt))return 0;
    if(istGedrückt&1)for(int ordnungszahlIndex=31;ordnungszahlIndex>=0;ordnungszahlIndex--){bedienelementStatuswert *angefordertBreiteWert=&knotenliste[eigentümerObjekt][ordnungszahlIndex];if(!angefordertBreiteWert->kategorieWert||!istDargestellt(eigentümerObjekt,angefordertBreiteWert))continue;int fensterWaagerechteKoordinate,fensterSenkrechteKoordinate;position(eigentümerObjekt,angefordertBreiteWert,&fensterWaagerechteKoordinate,&fensterSenkrechteKoordinate);
        if(waagerechteKoordinateKoordinate<fensterWaagerechteKoordinate||senkrechteKoordinateKoordinate<fensterSenkrechteKoordinate||waagerechteKoordinateKoordinate>=fensterWaagerechteKoordinate+angefordertBreiteWert->angefordertBreiteWert||senkrechteKoordinateKoordinate>=fensterSenkrechteKoordinate+angefordertBreiteWert->angefordertHöheWert)continue;
        if(angefordertBreiteWert->kategorieWert==1&&senkrechteKoordinateKoordinate<fensterSenkrechteKoordinate+30&&waagerechteKoordinateKoordinate>=fensterWaagerechteKoordinate+angefordertBreiteWert->angefordertBreiteWert-28){if(angefordertBreiteWert->anordnungRichtlinie!=0)angefordertBreiteWert->istAngezeigt=0;ereignis(eigentümerObjekt,0x10000+ordnungszahlIndex+1);platineTerminal(3);return 1;}
        if(angefordertBreiteWert->kategorieWert==4){ereignis(eigentümerObjekt,ordnungszahlIndex+1);return 1;}if(angefordertBreiteWert->kategorieWert==5){fokussiert[eigentümerObjekt]=ordnungszahlIndex+1;platineTerminal(3);return 1;}
        if(angefordertBreiteWert->kategorieWert==1)return 1;
    }return 0;
}
void bildschirmDrücken(int eigentümerObjekt,unsigned zweiterWert){
    bedienelementStatuswert *angefordertBreiteWert=elementWert(eigentümerObjekt,fokussiert[eigentümerObjekt]);if(!angefordertBreiteWert||angefordertBreiteWert->kategorieWert!=5)return;
    if(zweiterWert==13||zweiterWert==10){ereignis(eigentümerObjekt,fokussiert[eigentümerObjekt]);return;}
    if(zweiterWert==8||zweiterWert==127){if(angefordertBreiteWert->Länge)angefordertBreiteWert->Länge--;vorzeichenlosLangWert[eigentümerObjekt]=0;}
    else{
        unsigned zeichenKodierung=zweiterWert;
        if(vorzeichenlosLangWert[eigentümerObjekt]){if((zweiterWert&192)!=128){vorzeichenlosLangWert[eigentümerObjekt]=0;return;}vorzeichenlosErgebnis[eigentümerObjekt]=(vorzeichenlosErgebnis[eigentümerObjekt]<<6)|(zweiterWert&63);if(--vorzeichenlosLangWert[eigentümerObjekt])return;zeichenKodierung=vorzeichenlosErgebnis[eigentümerObjekt];}
        else if(zweiterWert>=0xc2&&zweiterWert<=0xf4){vorzeichenlosLangWert[eigentümerObjekt]=zweiterWert<0xe0?1:zweiterWert<0xf0?2:3;vorzeichenlosErgebnis[eigentümerObjekt]=zweiterWert&((1u<<(6-vorzeichenlosLangWert[eigentümerObjekt]))-1);return;}
        else if(zweiterWert<32||zweiterWert>=128)return;
        if(zeichenKodierung>0x10ffff||(zeichenKodierung>=0xd800&&zeichenKodierung<=0xdfff))return;if(angefordertBreiteWert->Länge<127)angefordertBreiteWert->Text[angefordertBreiteWert->Länge++]=zeichenKodierung;
    }
    platineTerminal(3);
}
int bildschirmAufrufen(int eigentümerObjekt,unsigned aktion,int bezeichnerWert,int ersterWert,int zweiterWert,int zeichenKode,int zielDaten){
    if(eigentümerObjekt<0||eigentümerObjekt>=4)return -22;bedienelementStatuswert *angefordertBreiteWert=elementWert(eigentümerObjekt,bezeichnerWert);
    if(aktion==0){if(bezeichnerWert<1||bezeichnerWert>5)return -22;for(int ordnungszahlIndex=0;ordnungszahlIndex<32;ordnungszahlIndex++)if(knotenliste[eigentümerObjekt][ordnungszahlIndex].kategorieWert==0){angefordertBreiteWert=&knotenliste[eigentümerObjekt][ordnungszahlIndex];memset(angefordertBreiteWert,0,sizeof(*angefordertBreiteWert));angefordertBreiteWert->kategorieWert=bezeichnerWert;angefordertBreiteWert->istAngezeigt=bezeichnerWert!=1;angefordertBreiteWert->angefordertBreiteWert=bezeichnerWert==1?380:220;angefordertBreiteWert->angefordertHöheWert=bezeichnerWert==1?240:28;angefordertBreiteWert->anordnungRichtlinie=1;angefordertBreiteWert->waagerechteKoordinateKoordinate=bezeichnerWert==1?130:16;angefordertBreiteWert->senkrechteKoordinateKoordinate=bezeichnerWert==1?110:16;return ordnungszahlIndex+1;}return -28;}
    if(aktion==5){if(!eintragAnzahl[eigentümerObjekt])return 0;int zurückgegebenWert=ereignisListe[eigentümerObjekt][ersterEintrag[eigentümerObjekt]];ersterEintrag[eigentümerObjekt]=(ersterEintrag[eigentümerObjekt]+1)%16;eintragAnzahl[eigentümerObjekt]--;return zurückgegebenWert;}
    if(aktion==6)return bildschirmSichtbar(eigentümerObjekt);
    if(!angefordertBreiteWert)return -9;
    int warAngezeigt=istDargestellt(eigentümerObjekt,angefordertBreiteWert);
    if(aktion==1){int hintergrundBreite=platineBildschirmBreite(),hintergrundHöhe=platineBildschirmHöhe();if(ersterWert<0||zweiterWert<0||zeichenKode<1||zielDaten<1||ersterWert>hintergrundBreite||zweiterWert>hintergrundHöhe||zeichenKode>hintergrundBreite-ersterWert||zielDaten>hintergrundHöhe-zweiterWert)return -22;angefordertBreiteWert->waagerechteKoordinateKoordinate=ersterWert;angefordertBreiteWert->senkrechteKoordinateKoordinate=zweiterWert;angefordertBreiteWert->angefordertBreiteWert=zeichenKode;angefordertBreiteWert->angefordertHöheWert=zielDaten;angefordertBreiteWert->handbuchAnordnung=1;}
    else if(aktion==2){bedienelementStatuswert *kindElement=elementWert(eigentümerObjekt,ersterWert);if(!kindElement||kindElement==angefordertBreiteWert||kindElement->kategorieWert==1)return -22;int datenPosition=bezeichnerWert;for(int tiefeWert=0;datenPosition&&tiefeWert<32;tiefeWert++){if(datenPosition==ersterWert)return -22;bedienelementStatuswert *obererSeiteRand=elementWert(eigentümerObjekt,datenPosition);datenPosition=obererSeiteRand?obererSeiteRand->elternknoten:0;}kindElement->elternknoten=bezeichnerWert;if(!kindElement->handbuchAnordnung){int geschwisterknoten=0;for(int ordnungszahlIndex=0;ordnungszahlIndex<32;ordnungszahlIndex++)if(&knotenliste[eigentümerObjekt][ordnungszahlIndex]!=kindElement&&knotenliste[eigentümerObjekt][ordnungszahlIndex].elternknoten==bezeichnerWert)geschwisterknoten++;kindElement->senkrechteKoordinateKoordinate=16+geschwisterknoten*36;}}
    else if(aktion==3)angefordertBreiteWert->istAngezeigt=ersterWert!=0;
    else if(aktion==4)angefordertBreiteWert->istAngezeigt=0;
    else if(aktion==7)angefordertBreiteWert->anordnungRichtlinie=ersterWert;
    else if(aktion==8)return angefordertBreiteWert->Länge;
    else if(aktion==9)return ersterWert>=0&&(unsigned)ersterWert<angefordertBreiteWert->Länge?angefordertBreiteWert->Text[ersterWert]:-22;
    else return -22;
    if(warAngezeigt||istDargestellt(eigentümerObjekt,angefordertBreiteWert))platineTerminal(3);return 0;
}
int bildschirmText(int eigentümerObjekt,int bezeichnerWert,const uint32_t *Daten,unsigned elementeintragAnzahl){bedienelementStatuswert *angefordertBreiteWert=elementWert(eigentümerObjekt,bezeichnerWert);if(!angefordertBreiteWert)return -9;if(elementeintragAnzahl>127)return -22;for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++){unsigned zeichenKodierung=Daten[ordnungszahlIndex];if(zeichenKodierung>0x10ffff||(zeichenKodierung>=0xd800&&zeichenKodierung<=0xdfff))return -22;}for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)angefordertBreiteWert->Text[ordnungszahlIndex]=Daten[ordnungszahlIndex];angefordertBreiteWert->Länge=elementeintragAnzahl;if(istDargestellt(eigentümerObjekt,angefordertBreiteWert))platineTerminal(3);return 0;}
