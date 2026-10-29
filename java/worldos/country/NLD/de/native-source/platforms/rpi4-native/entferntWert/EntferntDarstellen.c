/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 verbinden, 제한된 Eingabewert Länge, 비동기 wertSenden, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 Bildschirm Daten 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "entferntWert.h"
#include "kryptographieUnterstützung.h"
#include "profil.h"
#include "../Netzwerkstapel/Netzwerkstapel.h"
#include "../maschine/bildschirmInformation.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(bildschirmPasswort)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t platineVergangeneMillisekunden(void);
extern uintptr_t platineTerminal(uintptr_t);
void entferntTasteStrich(unsigned,int);
void entferntTasteStrichInitialisieren(void);
void bestätigenEntferntTaste(void);
static int lauschendEndpunkt=-1,gegenstelleWert=-1,stufeWert,künftigSchließen;
static uintptr_t verbindungZeit,eingeschaltetEmpfangenErneut;
static unsigned char Eingabewert[8192],Ausgabe[4096],herausforderungWert[16];
static unsigned eingabeAnzahl,ausgabeAnzahl,gesendetAnzahl;
static unsigned breiteWert,höheWert,bildpunktGröße=4,großByteordnungWert,rotHöchstwert=255,grünHöchstwert=255,blauHöchstwert=255,rotVerschieben=16,grünVerschieben=8,blauVerschieben;
static uint32_t vorherigZusammenfassung[60*68];
static unsigned short geändertKachel[60*68];
static unsigned kachelAnzahl,kachelPosition,angefordertWaagerechteKoordinate,angefordertSenkrechteKoordinate,angefordertSpannweite,angefordertHöhe;
static unsigned lesen16Bit(const unsigned char *datenPosition){return(unsigned)datenPosition[0]*256+datenPosition[1];}
static uint32_t lesen32Bit(const unsigned char *datenPosition){return(uint32_t)datenPosition[0]<<24|(uint32_t)datenPosition[1]<<16|(uint32_t)datenPosition[2]<<8|datenPosition[3];}
static void schreiben16Bit(unsigned char *datenPosition,unsigned Wert){datenPosition[0]=Wert>>8;datenPosition[1]=Wert;}
static void schreiben32Bit(unsigned char *datenPosition,uint32_t Wert){datenPosition[0]=Wert>>24;datenPosition[1]=Wert>>16;datenPosition[2]=Wert>>8;datenPosition[3]=Wert;}
static void schließen(void){if(gegenstelleWert>=0)netzwerkSchließen(gegenstelleWert);gegenstelleWert=-1;stufeWert=0;eingabeAnzahl=ausgabeAnzahl=gesendetAnzahl=0;kachelAnzahl=kachelPosition=0;künftigSchließen=0;entferntTasteStrichInitialisieren();eingeschaltetEmpfangenErneut=platineVergangeneMillisekunden()+500;}
static void wertAusgeben(const void *Daten,unsigned Zahl){memcpy(Ausgabe,Daten,Zahl);ausgabeAnzahl=Zahl;gesendetAnzahl=0;}
static void wertVerbrauchen(unsigned Zahl){eingabeAnzahl-=Zahl;memmove(Eingabewert,Eingabewert+Zahl,eingabeAnzahl);}
int steuerungEntferntDarstellen(unsigned aktion){
    if(aktion==0){schließen();if(lauschendEndpunkt>=0)netzwerkSchließen(lauschendEndpunkt);lauschendEndpunkt=-1;return 0;}
    if(aktion!=1)return lauschendEndpunkt>=0;
    if(lauschendEndpunkt>=0)return 0;
    int portWert=netzbuchseEndpunktErstellen(1);if(portWert<0)return portWert;wiederverwendenNetzbuchseAdresse(portWert);
    int ergebnis=netzZuordnen(portWert,0,5900);if(!ergebnis)ergebnis=netzLauschen(portWert);
    if(ergebnis<0){netzwerkSchließen(portWert);return ergebnis;}lauschendEndpunkt=portWert;return 0;
}
static uint32_t kachelZusammenfassung(unsigned waagerechtPosition,unsigned senkrechtPosition){
    uint32_t Wert=2166136261u;
    for(unsigned senkrechteKoordinateKoordinate=senkrechtPosition;senkrechteKoordinateKoordinate<senkrechtPosition+16&&senkrechteKoordinateKoordinate<höheWert;senkrechteKoordinateKoordinate++)for(unsigned waagerechteKoordinateKoordinate=waagerechtPosition;waagerechteKoordinateKoordinate<waagerechtPosition+32&&waagerechteKoordinateKoordinate<breiteWert;waagerechteKoordinateKoordinate++)Wert=(Wert^platineLesenBildschirm(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate))*16777619u;
    return Wert;
}
static void bildschirmAnfrage(const unsigned char *datenPosition){
    angefordertWaagerechteKoordinate=lesen16Bit(datenPosition+2);angefordertSenkrechteKoordinate=lesen16Bit(datenPosition+4);angefordertSpannweite=lesen16Bit(datenPosition+6);angefordertHöhe=lesen16Bit(datenPosition+8);
    if(angefordertWaagerechteKoordinate>=breiteWert||angefordertSenkrechteKoordinate>=höheWert)angefordertSpannweite=angefordertHöhe=0;
    if(angefordertSpannweite>breiteWert-angefordertWaagerechteKoordinate&&angefordertWaagerechteKoordinate<breiteWert)angefordertSpannweite=breiteWert-angefordertWaagerechteKoordinate;
    if(angefordertHöhe>höheWert-angefordertSenkrechteKoordinate&&angefordertSenkrechteKoordinate<höheWert)angefordertHöhe=höheWert-angefordertSenkrechteKoordinate;
    kachelAnzahl=kachelPosition=0;
    if(angefordertSpannweite&&angefordertHöhe)for(unsigned senkrechteKoordinateKoordinate=angefordertSenkrechteKoordinate/16;senkrechteKoordinateKoordinate<=(angefordertSenkrechteKoordinate+angefordertHöhe-1)/16;senkrechteKoordinateKoordinate++)for(unsigned waagerechteKoordinateKoordinate=angefordertWaagerechteKoordinate/32;waagerechteKoordinateKoordinate<=(angefordertWaagerechteKoordinate+angefordertSpannweite-1)/32;waagerechteKoordinateKoordinate++){
        unsigned positionIndex=senkrechteKoordinateKoordinate*60+waagerechteKoordinateKoordinate;uint32_t zusammenfassungWert=kachelZusammenfassung(waagerechteKoordinateKoordinate*32,senkrechteKoordinateKoordinate*16);
        if(!datenPosition[1]||vorherigZusammenfassung[positionIndex]!=zusammenfassungWert)geändertKachel[kachelAnzahl++]=positionIndex;
    }
    Ausgabe[0]=Ausgabe[1]=0;schreiben16Bit(Ausgabe+2,kachelAnzahl);ausgabeAnzahl=4;gesendetAnzahl=0;
}
static void kachelSenden(void){
    unsigned positionIndex=geändertKachel[kachelPosition++],waagerechtPosition=(positionIndex%60)*32,senkrechtPosition=(positionIndex/60)*16;
    unsigned endeWaagerechteKoordinate=waagerechtPosition+32,endeSenkrechteKoordinate=senkrechtPosition+16;if(endeWaagerechteKoordinate>breiteWert)endeWaagerechteKoordinate=breiteWert;if(endeSenkrechteKoordinate>höheWert)endeSenkrechteKoordinate=höheWert;
    /* unterteilWert 타일 anfrage 뒤에도 restwertWert 화소를 보낸 것으로 처리하지 않는다. */
    int alleWerte=waagerechtPosition>=angefordertWaagerechteKoordinate&&senkrechtPosition>=angefordertSenkrechteKoordinate&&endeWaagerechteKoordinate<=angefordertWaagerechteKoordinate+angefordertSpannweite&&endeSenkrechteKoordinate<=angefordertSenkrechteKoordinate+angefordertHöhe;
    if(alleWerte)vorherigZusammenfassung[positionIndex]=kachelZusammenfassung(waagerechtPosition,senkrechtPosition);
    if(waagerechtPosition<angefordertWaagerechteKoordinate)waagerechtPosition=angefordertWaagerechteKoordinate;if(senkrechtPosition<angefordertSenkrechteKoordinate)senkrechtPosition=angefordertSenkrechteKoordinate;
    if(endeWaagerechteKoordinate>angefordertWaagerechteKoordinate+angefordertSpannweite)endeWaagerechteKoordinate=angefordertWaagerechteKoordinate+angefordertSpannweite;if(endeSenkrechteKoordinate>angefordertSenkrechteKoordinate+angefordertHöhe)endeSenkrechteKoordinate=angefordertSenkrechteKoordinate+angefordertHöhe;
    schreiben16Bit(Ausgabe,waagerechtPosition);schreiben16Bit(Ausgabe+2,senkrechtPosition);schreiben16Bit(Ausgabe+4,endeWaagerechteKoordinate-waagerechtPosition);schreiben16Bit(Ausgabe+6,endeSenkrechteKoordinate-senkrechtPosition);schreiben32Bit(Ausgabe+8,0);
    ausgabeAnzahl=12;gesendetAnzahl=0;
    for(unsigned senkrechteKoordinateKoordinate=senkrechtPosition;senkrechteKoordinateKoordinate<endeSenkrechteKoordinate;senkrechteKoordinateKoordinate++)for(unsigned waagerechteKoordinateKoordinate=waagerechtPosition;waagerechteKoordinateKoordinate<endeWaagerechteKoordinate;waagerechteKoordinateKoordinate++){
        uint32_t farbeWert=platineLesenBildschirm(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate),Wert=(((farbeWert>>16)&255)*rotHöchstwert/255)<<rotVerschieben|
            (((farbeWert>>8)&255)*grünHöchstwert/255)<<grünVerschieben|((farbeWert&255)*blauHöchstwert/255)<<blauVerschieben;
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<bildpunktGröße;ordnungszahlIndex++)Ausgabe[ausgabeAnzahl++]=Wert>>(8*(großByteordnungWert?bildpunktGröße-1-ordnungszahlIndex:ordnungszahlIndex));
    }
}
void entferntDarstellenUntersuchen(void){
    if(lauschendEndpunkt<0)return;
    if(gegenstelleWert<0){if(platineVergangeneMillisekunden()<eingeschaltetEmpfangenErneut)return;gegenstelleWert=netzAnnehmen(lauschendEndpunkt);if(gegenstelleWert<0)return;
        verbindungZeit=platineVergangeneMillisekunden();stufeWert=1;wertAusgeben("RFB 003.008\n",12);memset(vorherigZusammenfassung,0,sizeof(vorherigZusammenfassung));
        bildpunktGröße=4;großByteordnungWert=0;rotHöchstwert=grünHöchstwert=blauHöchstwert=255;rotVerschieben=16;grünVerschieben=8;blauVerschieben=0;}
    if(stufeWert<5&&platineVergangeneMillisekunden()-verbindungZeit>15000){schließen();return;}
    if(ausgabeAnzahl){int Zahl=netzSchreiben(gegenstelleWert,Ausgabe+gesendetAnzahl,ausgabeAnzahl-gesendetAnzahl);if(Zahl>0){gesendetAnzahl+=Zahl;if(gesendetAnzahl==ausgabeAnzahl)ausgabeAnzahl=gesendetAnzahl=0;}else if(Zahl!=-11){schließen();return;}}
    if(!ausgabeAnzahl&&künftigSchließen){schließen();return;}
    if(!ausgabeAnzahl&&kachelPosition<kachelAnzahl)kachelSenden();
    if(eingabeAnzahl==sizeof(Eingabewert)){schließen();return;}
    int empfangenWertAnzahl=netzLesen(gegenstelleWert,Eingabewert+eingabeAnzahl,sizeof(Eingabewert)-eingabeAnzahl);
    if(empfangenWertAnzahl==0||(empfangenWertAnzahl<0&&empfangenWertAnzahl!=-11)){schließen();return;}if(empfangenWertAnzahl>0)eingabeAnzahl+=empfangenWertAnzahl;
    if(ausgabeAnzahl||kachelPosition<kachelAnzahl)return;
    if(stufeWert==1&&eingabeAnzahl>=12){if(memcmp(Eingabewert,"RFB 003.008\n",12)){schließen();return;}wertVerbrauchen(12);const unsigned char authentifizierungMethode[]={1,2};wertAusgeben(authentifizierungMethode,2);stufeWert=2;return;}
    if(stufeWert==2&&eingabeAnzahl){if(Eingabewert[0]!=2||entferntZufällig(herausforderungWert,16)){schließen();return;}wertVerbrauchen(1);wertAusgeben(herausforderungWert,16);stufeWert=3;return;}
    if(stufeWert==3&&eingabeAnzahl>=16){unsigned char tasteMaterial[8],richtigErwiderung[16];br_des_ct_cbcenc_keys passwortWert;
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<8;ordnungszahlIndex++){unsigned Wert=bildschirmPasswort[ordnungszahlIndex],istUmgekehrt=0;for(unsigned innerlichOrdnungszahl=0;innerlichOrdnungszahl<8;innerlichOrdnungszahl++){istUmgekehrt=(istUmgekehrt<<1)|(Wert&1);Wert>>=1;}tasteMaterial[ordnungszahlIndex]=istUmgekehrt;}
        br_des_ct_cbcenc_init(&passwortWert,tasteMaterial,8);memcpy(richtigErwiderung,herausforderungWert,16);
        for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<16;ordnungszahlIndex+=8){unsigned char vektorWert[8]={0};br_des_ct_cbcenc_run(&passwortWert,vektorWert,richtigErwiderung+ordnungszahlIndex,8);memset(vektorWert,0,8);}
        unsigned unterschiedWert=0;for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<16;ordnungszahlIndex++)unterschiedWert|=richtigErwiderung[ordnungszahlIndex]^Eingabewert[ordnungszahlIndex];wertVerbrauchen(16);memset(&passwortWert,0,sizeof(passwortWert));memset(tasteMaterial,0,8);memset(richtigErwiderung,0,16);memset(herausforderungWert,0,16);
        schreiben32Bit(Ausgabe,unterschiedWert?1:0);ausgabeAnzahl=4;gesendetAnzahl=0;
        if(unterschiedWert){schreiben32Bit(Ausgabe+4,19);memcpy(Ausgabe+8,"Authentication fail",19);ausgabeAnzahl=27;künftigSchließen=1;}else stufeWert=4;return;}
    if(stufeWert==4&&eingabeAnzahl){wertVerbrauchen(1);breiteWert=platineBildschirmBreite();höheWert=platineBildschirmHöhe();if(!breiteWert||!höheWert||breiteWert>1920||höheWert>1080){schließen();return;}
        if(!platineTerminal(7)){const unsigned char ereignis[]={30,2,1,0,0,0,0};zuführenEntferntEingabe(ereignis,7);}
        memset(Ausgabe,0,40);schreiben16Bit(Ausgabe,breiteWert);schreiben16Bit(Ausgabe+2,höheWert);Ausgabe[4]=32;Ausgabe[5]=24;Ausgabe[7]=1;
        schreiben16Bit(Ausgabe+8,255);schreiben16Bit(Ausgabe+10,255);schreiben16Bit(Ausgabe+12,255);Ausgabe[14]=16;Ausgabe[15]=8;
        const char *Name="jkoros native";schreiben32Bit(Ausgabe+20,strlen(Name));memcpy(Ausgabe+24,Name,strlen(Name));ausgabeAnzahl=24+strlen(Name);gesendetAnzahl=0;stufeWert=5;return;}
    if(stufeWert!=5||!eingabeAnzahl)return;
    unsigned typKategorie=Eingabewert[0],benötigtWert=typKategorie==0?20:typKategorie==2?4:typKategorie==3?10:typKategorie==4?8:typKategorie==5?6:typKategorie==6?8:0;
    if(!benötigtWert){schließen();return;}if(eingabeAnzahl<benötigtWert)return;
    if(typKategorie==2){unsigned Zahl=lesen16Bit(Eingabewert+2);if(Zahl>128){schließen();return;}benötigtWert+=Zahl*4;}
    if(typKategorie==6){unsigned Zahl=lesen32Bit(Eingabewert+4);if(Zahl>4096){schließen();return;}benötigtWert+=Zahl;}
    if(eingabeAnzahl<benötigtWert)return;
    if(typKategorie==0){unsigned bitWert=Eingabewert[4],rotKanalHöchstwert=lesen16Bit(Eingabewert+8),sekundenWert=lesen16Bit(Eingabewert+10),blauKanalHöchstwert=lesen16Bit(Eingabewert+12),rotKanalVerschieben=Eingabewert[14],grünKanalVerschieben=Eingabewert[15],blauKanalVerschieben=Eingabewert[16];
        if((bitWert!=16&&bitWert!=32)||!Eingabewert[7]||Eingabewert[6]>1||!rotKanalHöchstwert||!sekundenWert||!blauKanalHöchstwert||rotKanalHöchstwert>255||sekundenWert>255||blauKanalHöchstwert>255||rotKanalVerschieben>24||grünKanalVerschieben>24||blauKanalVerschieben>24||
           ((uint64_t)rotKanalHöchstwert<<rotKanalVerschieben)>((1ull<<bitWert)-1)||((uint64_t)sekundenWert<<grünKanalVerschieben)>((1ull<<bitWert)-1)||((uint64_t)blauKanalHöchstwert<<blauKanalVerschieben)>((1ull<<bitWert)-1)){schließen();return;}
        bildpunktGröße=bitWert/8;großByteordnungWert=Eingabewert[6];rotHöchstwert=rotKanalHöchstwert;grünHöchstwert=sekundenWert;blauHöchstwert=blauKanalHöchstwert;rotVerschieben=rotKanalVerschieben;grünVerschieben=grünKanalVerschieben;blauVerschieben=blauKanalVerschieben;memset(vorherigZusammenfassung,0,sizeof(vorherigZusammenfassung));
    }else if(typKategorie==3)bildschirmAnfrage(Eingabewert);
    else if(typKategorie==4)entferntTasteStrich(lesen32Bit(Eingabewert+4),Eingabewert[1]!=0);
    else if(typKategorie==5){unsigned waagerechteKoordinateKoordinate=lesen16Bit(Eingabewert+2),senkrechteKoordinateKoordinate=lesen16Bit(Eingabewert+4);if(waagerechteKoordinateKoordinate>=breiteWert)waagerechteKoordinateKoordinate=breiteWert-1;if(senkrechteKoordinateKoordinate>=höheWert)senkrechteKoordinateKoordinate=höheWert-1;
        if(Eingabewert[1])bestätigenEntferntTaste();
        unsigned char ereignis[]={30,1,Eingabewert[1],waagerechteKoordinateKoordinate&255,waagerechteKoordinateKoordinate>>8,senkrechteKoordinateKoordinate&255,senkrechteKoordinateKoordinate>>8};zuführenEntferntEingabe(ereignis,sizeof(ereignis));}
    wertVerbrauchen(benötigtWert);
}
