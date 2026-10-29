/* tatsächlichDaten Bildschirm 메모리와 기존 C aufrufen 규약만 연결한다. 합성 구현은 Quelltext/BildpufferZusammensetzer.java. */
#include "../benennung/maschineBindenNamen.h"
#include "bildschirmInformation.h"
static volatile uint32_t *bildpunkteListe;
static unsigned bildschirmZeilennummerMaschinenwortAnzahl, bildschirmBreite, bildschirmHöhe;
extern void javaZeichnungVorbereiten(int,int),javaZeichnungEnde(void),javaZeichnungRechteck(int,int,int,int,int),javaZeichnungZeiger(int,int,int);
extern int javaZeichnungBreite(void),javaZeichnungHöhe(void),javaZeichnungAnzahlNiedrig(void),javaZeichnungAnzahlHoch(void);
extern int javaZeichnungBeschneiden(int,int,int,int),javaZeichnungBeschneidenWert(int),javaZeichnungBeginn(int,int,int,int),javaZeichnungBildpunkt(int,int,int);
uintptr_t platineBildpufferLesen(uintptr_t waagerechtPosition,uintptr_t senkrechtPosition){
    return bildpunkteListe&&waagerechtPosition<bildschirmBreite&&senkrechtPosition<bildschirmHöhe?bildpunkteListe[senkrechtPosition*bildschirmZeilennummerMaschinenwortAnzahl+waagerechtPosition]:0;
}
void platineBildpufferSchreiben(uintptr_t waagerechtPosition,uintptr_t senkrechtPosition,uintptr_t farbeWert){
    if(bildpunkteListe&&waagerechtPosition<bildschirmBreite&&senkrechtPosition<bildschirmHöhe)bildpunkteListe[senkrechtPosition*bildschirmZeilennummerMaschinenwortAnzahl+waagerechtPosition]=(uint32_t)farbeWert;
}
void platineVorbereitenZeichnung(volatile uint32_t *Daten,unsigned breiteSpannweite,unsigned Länge,unsigned zeileAbstandWert){
    bildpunkteListe=Daten;bildschirmBreite=breiteSpannweite;bildschirmHöhe=Länge;bildschirmZeilennummerMaschinenwortAnzahl=zeileAbstandWert/4;javaZeichnungVorbereiten((int)breiteSpannweite,(int)Länge);
}
uintptr_t platineBildschirmBreite(void){return (unsigned)javaZeichnungBreite();}
uintptr_t platineBildschirmHöhe(void){return (unsigned)javaZeichnungHöhe();}
uint64_t platineZeichnungAnzahl(void){return ((uint64_t)(uint32_t)javaZeichnungAnzahlHoch()<<32)|(uint32_t)javaZeichnungAnzahlNiedrig();}
uint32_t platineLesenBildschirm(unsigned waagerechtPosition,unsigned senkrechtPosition){return (uint32_t)platineBildpufferLesen(waagerechtPosition,senkrechtPosition);}
int platineZeichnungGrenzen(int *waagerechtPosition,int *senkrechtPosition,int *breiteSpannweite,int *Länge){
    if(!javaZeichnungBeschneiden(*waagerechtPosition,*senkrechtPosition,*breiteSpannweite,*Länge))return 0;
    *waagerechtPosition=javaZeichnungBeschneidenWert(0);*senkrechtPosition=javaZeichnungBeschneidenWert(1);*breiteSpannweite=javaZeichnungBeschneidenWert(2);*Länge=javaZeichnungBeschneidenWert(3);return 1;
}
int platineStartenZeichnung(int waagerechtPosition,int senkrechtPosition,int breiteSpannweite,int Länge){return javaZeichnungBeginn(waagerechtPosition,senkrechtPosition,breiteSpannweite,Länge);}
void platineBeendenZeichnung(void){javaZeichnungEnde();}
uintptr_t platineBildpunkt(uintptr_t waagerechtPosition,uintptr_t senkrechtPosition,uintptr_t farbeWert){return (unsigned)javaZeichnungBildpunkt((int)waagerechtPosition,(int)senkrechtPosition,(int)farbeWert);}
void platineRechteckFüllen(int waagerechtPosition,int senkrechtPosition,int breiteSpannweite,int Länge,uint32_t farbeWert){javaZeichnungRechteck(waagerechtPosition,senkrechtPosition,breiteSpannweite,Länge,(int)farbeWert);}
void platineZeiger(int waagerechtPosition,int senkrechtPosition,unsigned formWert){javaZeichnungZeiger(waagerechtPosition,senkrechtPosition,(int)formWert);}
