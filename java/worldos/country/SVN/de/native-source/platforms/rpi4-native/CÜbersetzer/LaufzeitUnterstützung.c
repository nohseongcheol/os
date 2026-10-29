#include "../benennung/maschineBindenNamen.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "aufrufen.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int fehler;
int *__errno_location(void){return &fehler;}
void exit(int statuswertWert){benutzerAufrufen(6,statuswertWert,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *ausdruckPrüfen,const char *Datei,unsigned zeile,const char *methodeEintragName){fprintf(stderr,"cc assertion: %s %s:%u %s\n",ausdruckPrüfen,Datei,zeile,methodeEintragName);exit(1);}
size_t strlen(const char*zeichenketteDaten){const char*datenPosition=zeichenketteDaten;while(*datenPosition)datenPosition++;return datenPosition-zeichenketteDaten;}
int strcmp(const char*ersterWert,const char*zweiterWert){while(*ersterWert&&*ersterWert==*zweiterWert){ersterWert++;zweiterWert++;}return (unsigned char)*ersterWert-(unsigned char)*zweiterWert;}
int strncmp(const char*ersterWert,const char*zweiterWert,size_t elementeintragAnzahl){while(elementeintragAnzahl--){unsigned char waagerechteKoordinateKoordinate=*ersterWert++,senkrechteKoordinateKoordinate=*zweiterWert++;if(waagerechteKoordinateKoordinate!=senkrechteKoordinateKoordinate)return waagerechteKoordinateKoordinate-senkrechteKoordinateKoordinate;if(!waagerechteKoordinateKoordinate)return 0;}return 0;}
char *strcpy(char*zielDaten,const char*zeichenketteDaten){char*zurückgegebenWert=zielDaten;while((*zielDaten++=*zeichenketteDaten++)){}return zurückgegebenWert;}
char *strchr(const char*zeichenketteDaten,int zeichenKode){do{if(*zeichenketteDaten==(char)zeichenKode)return (char*)zeichenketteDaten;}while(*zeichenketteDaten++);return 0;}
char *strrchr(const char*zeichenketteDaten,int zeichenKode){const char*zurückgegebenWert=0;do{if(*zeichenketteDaten==(char)zeichenKode)zurückgegebenWert=zeichenketteDaten;}while(*zeichenketteDaten++);return (char*)zurückgegebenWert;}
char *strstr(const char*zeichenketteDaten,const char*terminalEintrag){size_t elementeintragAnzahl=strlen(terminalEintrag);for(;*zeichenketteDaten;zeichenketteDaten++)if(!strncmp(zeichenketteDaten,terminalEintrag,elementeintragAnzahl))return (char*)zeichenketteDaten;return elementeintragAnzahl?0:(char*)zeichenketteDaten;}
int memcmp(const void*ersterWert,const void*zweiterWert,size_t elementeintragAnzahl){const unsigned char*waagerechteKoordinateKoordinate=ersterWert,*senkrechteKoordinateKoordinate=zweiterWert;while(elementeintragAnzahl--){if(*waagerechteKoordinateKoordinate!=*senkrechteKoordinateKoordinate)return *waagerechteKoordinateKoordinate-*senkrechteKoordinateKoordinate;waagerechteKoordinateKoordinate++;senkrechteKoordinateKoordinate++;}return 0;}
void *memmove(void*zielDaten,const void*zeichenketteDaten,size_t elementeintragAnzahl){unsigned char*waagerechteKoordinateKoordinate=zielDaten;const unsigned char*senkrechteKoordinateKoordinate=zeichenketteDaten;if(waagerechteKoordinateKoordinate<senkrechteKoordinateKoordinate){for(size_t ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)waagerechteKoordinateKoordinate[ordnungszahlIndex]=senkrechteKoordinateKoordinate[ordnungszahlIndex];}else while(elementeintragAnzahl){elementeintragAnzahl--;waagerechteKoordinateKoordinate[elementeintragAnzahl]=senkrechteKoordinateKoordinate[elementeintragAnzahl];}return zielDaten;}
static unsigned char zuteilungSammelbereich[6*1024*1024] __attribute__((aligned(16)));
typedef struct datenBlock {size_t größe;struct datenBlock*nächsterElementeintrag;int verbleibendKapazität;int auffüllung;uint64_t ausrichtungEinheit;} datenBlock;
static datenBlock *ersterEintrag;
void free(void*datenPosition){if(!datenPosition)return;datenBlock*zweiterWert=(datenBlock*)datenPosition-1;zweiterWert->verbleibendKapazität=1;for(datenBlock*nächsterVersatzwert=ersterEintrag;nächsterVersatzwert&&nächsterVersatzwert->nächsterElementeintrag;){if(nächsterVersatzwert->verbleibendKapazität&&nächsterVersatzwert->nächsterElementeintrag->verbleibendKapazität){nächsterVersatzwert->größe+=sizeof(datenBlock)+nächsterVersatzwert->nächsterElementeintrag->größe;nächsterVersatzwert->nächsterElementeintrag=nächsterVersatzwert->nächsterElementeintrag->nächsterElementeintrag;}else nächsterVersatzwert=nächsterVersatzwert->nächsterElementeintrag;}}
void *realloc(void*datenPosition,size_t elementeintragAnzahl){
    if(!elementeintragAnzahl){free(datenPosition);return 0;}if(elementeintragAnzahl>sizeof(zuteilungSammelbereich)-sizeof(datenBlock))return 0;elementeintragAnzahl=(elementeintragAnzahl+15)&~(size_t)15;
    if(!ersterEintrag){ersterEintrag=(datenBlock*)zuteilungSammelbereich;ersterEintrag->größe=sizeof(zuteilungSammelbereich)-sizeof(datenBlock);ersterEintrag->verbleibendKapazität=1;ersterEintrag->nächsterElementeintrag=0;}
    datenBlock*vorherigElementeintrag=datenPosition?(datenBlock*)datenPosition-1:0;if(vorherigElementeintrag&&vorherigElementeintrag->größe>=elementeintragAnzahl)return datenPosition;
    for(datenBlock*zweiterWert=ersterEintrag;zweiterWert;zweiterWert=zweiterWert->nächsterElementeintrag)if(zweiterWert->verbleibendKapazität&&zweiterWert->größe>=elementeintragAnzahl){
        if(zweiterWert->größe>=elementeintragAnzahl+sizeof(datenBlock)+16){datenBlock*verbleibendTeil=(datenBlock*)((unsigned char*)(zweiterWert+1)+elementeintragAnzahl);verbleibendTeil->größe=zweiterWert->größe-elementeintragAnzahl-sizeof(datenBlock);verbleibendTeil->nächsterElementeintrag=zweiterWert->nächsterElementeintrag;verbleibendTeil->verbleibendKapazität=1;zweiterWert->nächsterElementeintrag=verbleibendTeil;zweiterWert->größe=elementeintragAnzahl;}
        zweiterWert->verbleibendKapazität=0;void*zurückgegebenWert=zweiterWert+1;if(vorherigElementeintrag){memcpy(zurückgegebenWert,datenPosition,vorherigElementeintrag->größe);free(datenPosition);}return zurückgegebenWert;
    }fehler=12;return 0;
}
void *malloc(size_t elementeintragAnzahl){return realloc(0,elementeintragAnzahl);}
void *calloc(size_t elementeintragAnzahl,size_t zeichenketteDaten){if(zeichenketteDaten&&elementeintragAnzahl>SIZE_MAX/zeichenketteDaten)return 0;void*datenPosition=malloc(elementeintragAnzahl*zeichenketteDaten);if(datenPosition)memset(datenPosition,0,elementeintragAnzahl*zeichenketteDaten);return datenPosition;}
unsigned long long strtoull(const char*zeichenketteDaten,char**endeVersatzwert,int hintergrundWert){
    const char*versatzwertStarten=zeichenketteDaten;while(*zeichenketteDaten==' '||(*zeichenketteDaten>=9&&*zeichenketteDaten<=13))zeichenketteDaten++;int istNegativ=0;if(*zeichenketteDaten=='-'||*zeichenketteDaten=='+')istNegativ=*zeichenketteDaten++=='-';
    if((!hintergrundWert||hintergrundWert==16)&&zeichenketteDaten[0]=='0'&&(zeichenketteDaten[1]=='x'||zeichenketteDaten[1]=='X')){hintergrundWert=16;zeichenketteDaten+=2;}if(!hintergrundWert)hintergrundWert=*zeichenketteDaten=='0'?8:10;
    unsigned long long vorläufigDaten=0;int beliebigWert=0;for(;;){unsigned zeichenKode=*zeichenketteDaten,zielDaten=zeichenKode>='0'&&zeichenKode<='9'?zeichenKode-'0':zeichenKode>='a'&&zeichenKode<='z'?zeichenKode-'a'+10:zeichenKode>='A'&&zeichenKode<='Z'?zeichenKode-'A'+10:99;if(zielDaten>=(unsigned)hintergrundWert)break;beliebigWert=1;zeichenketteDaten++;if(vorläufigDaten>(~0ull-zielDaten)/(unsigned)hintergrundWert){vorläufigDaten=~0ull;fehler=34;}else vorläufigDaten=vorläufigDaten*hintergrundWert+zielDaten;}
    if(endeVersatzwert)*endeVersatzwert=(char*)(beliebigWert?zeichenketteDaten:versatzwertStarten);return istNegativ?0-vorläufigDaten:vorläufigDaten;
}
unsigned long strtoul(const char*zeichenketteDaten,char**hilfsEintrag,int zweiterWert){return strtoull(zeichenketteDaten,hilfsEintrag,zweiterWert);}
long strtol(const char*zeichenketteDaten,char**hilfsEintrag,int zweiterWert){return (long)strtoull(zeichenketteDaten,hilfsEintrag,zweiterWert);}
int atoi(const char*zeichenketteDaten){return (int)strtol(zeichenketteDaten,0,10);}
long double ldexpl(long double waagerechteKoordinateKoordinate,int elementeintragAnzahl){while(elementeintragAnzahl>0){waagerechteKoordinateKoordinate*=2;elementeintragAnzahl--;}while(elementeintragAnzahl<0){waagerechteKoordinateKoordinate/=2;elementeintragAnzahl++;}return waagerechteKoordinateKoordinate;}
long double strtold(const char*zeichenketteDaten,char**endeVersatzwert){
    const char*versatzwertStarten=zeichenketteDaten;while(*zeichenketteDaten==' '||(*zeichenketteDaten>=9&&*zeichenketteDaten<=13))zeichenketteDaten++;int istNegativ=0;if(*zeichenketteDaten=='-'||*zeichenketteDaten=='+')istNegativ=*zeichenketteDaten++=='-';
    int hintergrundWert=10;if(zeichenketteDaten[0]=='0'&&(zeichenketteDaten[1]=='x'||zeichenketteDaten[1]=='X')){hintergrundWert=16;zeichenketteDaten+=2;}long double vorläufigDaten=0,maßstab=1;int gebrochen=0,beliebigWert=0;
    for(;;){int zeichenKode=*zeichenketteDaten,zielDaten=zeichenKode>='0'&&zeichenKode<='9'?zeichenKode-'0':zeichenKode>='a'&&zeichenKode<='f'?zeichenKode-'a'+10:zeichenKode>='A'&&zeichenKode<='F'?zeichenKode-'A'+10:99;
        if(zeichenKode=='.'&&!gebrochen){gebrochen=1;zeichenketteDaten++;continue;}if(zielDaten>=hintergrundWert)break;beliebigWert=1;zeichenketteDaten++;vorläufigDaten=vorläufigDaten*hintergrundWert+zielDaten;if(gebrochen)maßstab*=hintergrundWert;
    }vorläufigDaten/=maßstab;
    if((hintergrundWert==10&&(*zeichenketteDaten=='e'||*zeichenketteDaten=='E'))||(hintergrundWert==16&&(*zeichenketteDaten=='p'||*zeichenketteDaten=='P'))){const char*wertAnzeigen=zeichenketteDaten++;int werteSubtrahieren=0;if(*zeichenketteDaten=='-'||*zeichenketteDaten=='+')werteSubtrahieren=*zeichenketteDaten++=='-';int elementeintragAnzahl=0,eintragAnzahl=0;while(*zeichenketteDaten>='0'&&*zeichenketteDaten<='9'){eintragAnzahl++;if(elementeintragAnzahl<20000)elementeintragAnzahl=elementeintragAnzahl*10+*zeichenketteDaten-'0';zeichenketteDaten++;}if(!eintragAnzahl)zeichenketteDaten=wertAnzeigen;else{long double faktor=hintergrundWert==16?2:10;while(elementeintragAnzahl-->0&&elementeintragAnzahl<200000)vorläufigDaten=werteSubtrahieren?vorläufigDaten/faktor:vorläufigDaten*faktor;}}
    if(endeVersatzwert)*endeVersatzwert=(char*)(beliebigWert?zeichenketteDaten:versatzwertStarten);return istNegativ?-vorläufigDaten:vorläufigDaten;
}
double strtod(const char*zeichenketteDaten,char**hilfsEintrag){return (double)strtold(zeichenketteDaten,hilfsEintrag);}float strtof(const char*zeichenketteDaten,char**hilfsEintrag){return (float)strtold(zeichenketteDaten,hilfsEintrag);}
void qsort(void*hintergrundWert,size_t elementeintragAnzahl,size_t größe,int(*vergleichAnstellen)(const void*,const void*)){
    unsigned char*datenPosition=hintergrundWert;for(size_t ordnungszahlIndex=1;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)for(size_t innerlichOrdnungszahl=ordnungszahlIndex;innerlichOrdnungszahl&&vergleichAnstellen(datenPosition+(innerlichOrdnungszahl-1)*größe,datenPosition+innerlichOrdnungszahl*größe)>0;innerlichOrdnungszahl--)for(size_t dritterIndex=0;dritterIndex<größe;dritterIndex++){unsigned char zeichenKode=datenPosition[(innerlichOrdnungszahl-1)*größe+dritterIndex];datenPosition[(innerlichOrdnungszahl-1)*größe+dritterIndex]=datenPosition[innerlichOrdnungszahl*größe+dritterIndex];datenPosition[innerlichOrdnungszahl*größe+dritterIndex]=zeichenKode;}
}
static struct {int benutztKapazität,nachschlagenIndex;size_t position;} geöffnet[24];
static unsigned char ausgabe[32768];static size_t ausgabeGröße,ausgabePosition;static int ausgabeÖffnen;
const unsigned char *cAusgabe(size_t *elementeintragAnzahl){*elementeintragAnzahl=ausgabeGröße;return ausgabe;}
int open(const char*Name,int konfigurationBitliste,...){
    if(!strcmp(Name,"/@cc-output")){if(ausgabeÖffnen){fehler=16;return -1;}ausgabeÖffnen=1;ausgabeGröße=ausgabePosition=0;return 100;}
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<sizeof(übersetzerBetriebsmittel)/sizeof(übersetzerBetriebsmittel[0]);ordnungszahlIndex++)if(!strcmp(Name,übersetzerBetriebsmittel[ordnungszahlIndex].Name)){
        if(konfigurationBitliste&3){fehler=30;return -1;}for(int innerlichOrdnungszahl=0;innerlichOrdnungszahl<24;innerlichOrdnungszahl++)if(!geöffnet[innerlichOrdnungszahl].benutztKapazität){geöffnet[innerlichOrdnungszahl].benutztKapazität=1;geöffnet[innerlichOrdnungszahl].nachschlagenIndex=ordnungszahlIndex;geöffnet[innerlichOrdnungszahl].position=0;return 128+innerlichOrdnungszahl;}fehler=24;return -1;
    }
    intptr_t zurückgegebenWert=benutzerAufrufen(3,(uintptr_t)Name,konfigurationBitliste,0,0,0,0);if(zurückgegebenWert<0){fehler=-zurückgegebenWert;return -1;}return zurückgegebenWert;
}
int close(int dateiKennwert){if(dateiKennwert==100){ausgabeÖffnen=0;return 0;}if(dateiKennwert>=128&&dateiKennwert<152){geöffnet[dateiKennwert-128].benutztKapazität=0;return 0;}intptr_t zurückgegebenWert=benutzerAufrufen(4,dateiKennwert,0,0,0,0,0);if(zurückgegebenWert<0){fehler=-zurückgegebenWert;return -1;}return 0;}
long read(int dateiKennwert,void*Daten,size_t elementeintragAnzahl){
    if(dateiKennwert>=128&&dateiKennwert<152&&geöffnet[dateiKennwert-128].benutztKapazität){int ordnungszahlIndex=dateiKennwert-128;const übersetzerBetriebsmittelEintrag*zurückgegebenWert=&übersetzerBetriebsmittel[geöffnet[ordnungszahlIndex].nachschlagenIndex];size_t linksSeiteRand=zurückgegebenWert->größe-geöffnet[ordnungszahlIndex].position;if(elementeintragAnzahl>linksSeiteRand)elementeintragAnzahl=linksSeiteRand;memcpy(Daten,zurückgegebenWert->Daten+geöffnet[ordnungszahlIndex].position,elementeintragAnzahl);geöffnet[ordnungszahlIndex].position+=elementeintragAnzahl;return elementeintragAnzahl;}
    intptr_t zurückgegebenWert=benutzerAufrufen(2,dateiKennwert,(uintptr_t)Daten,elementeintragAnzahl,0,0,0);if(zurückgegebenWert<0){fehler=-zurückgegebenWert;return -1;}return zurückgegebenWert;
}
long write(int dateiKennwert,const void*Daten,size_t elementeintragAnzahl){
    if(dateiKennwert==100){if(elementeintragAnzahl>sizeof(ausgabe)-ausgabePosition){fehler=28;return -1;}memcpy(ausgabe+ausgabePosition,Daten,elementeintragAnzahl);ausgabePosition+=elementeintragAnzahl;if(ausgabeGröße<ausgabePosition)ausgabeGröße=ausgabePosition;return elementeintragAnzahl;}
    intptr_t zurückgegebenWert=benutzerAufrufen(1,dateiKennwert,(uintptr_t)Daten,elementeintragAnzahl,0,0,0);if(zurückgegebenWert<0){fehler=-zurückgegebenWert;return -1;}return zurückgegebenWert;
}
long lseek(int dateiKennwert,long versatzwertWert,int ursprungPositionieren){
    if(dateiKennwert==100){long datenPosition=versatzwertWert+(ursprungPositionieren==0?0:ursprungPositionieren==1?ausgabePosition:ausgabeGröße);if(datenPosition<0||(size_t)datenPosition>sizeof(ausgabe)){fehler=22;return -1;}ausgabePosition=datenPosition;return datenPosition;}
    if(dateiKennwert>=128&&dateiKennwert<152&&geöffnet[dateiKennwert-128].benutztKapazität){int ordnungszahlIndex=dateiKennwert-128;long datenPosition=versatzwertWert+(ursprungPositionieren==0?0:ursprungPositionieren==1?geöffnet[ordnungszahlIndex].position:übersetzerBetriebsmittel[geöffnet[ordnungszahlIndex].nachschlagenIndex].größe);if(datenPosition<0||(size_t)datenPosition>übersetzerBetriebsmittel[geöffnet[ordnungszahlIndex].nachschlagenIndex].größe){fehler=22;return -1;}geöffnet[ordnungszahlIndex].position=datenPosition;return datenPosition;}
    intptr_t zurückgegebenWert=benutzerAufrufen(5,dateiKennwert,versatzwertWert,ursprungPositionieren,0,0,0);if(zurückgegebenWert<0){fehler=-zurückgegebenWert;return -1;}return zurückgegebenWert;
}
int unlink(const char*Name){intptr_t zurückgegebenWert=benutzerAufrufen(11,(uintptr_t)Name,0,0,0,0,0);if(zurückgegebenWert<0){fehler=-zurückgegebenWert;return -1;}return zurückgegebenWert;}
char *realpath(const char*Name,char*ergebnisDaten){if(!ergebnisDaten){ergebnisDaten=malloc(strlen(Name)+1);if(!ergebnisDaten)return 0;}return strcpy(ergebnisDaten,Name);}
char *getcwd(char*datenPosition,size_t elementeintragAnzahl){if(elementeintragAnzahl<2){fehler=34;return 0;}datenPosition[0]='/';datenPosition[1]=0;return datenPosition;}
char *strerror(int hilfsEintrag){(void)hilfsEintrag;return "native compiler I/O error";}
time_t time(time_t*terminalEintrag){time_t vorläufigDaten=0;if(terminalEintrag)*terminalEintrag=vorläufigDaten;return vorläufigDaten;}
struct tm *localtime(const time_t*terminalEintrag){(void)terminalEintrag;static struct tm vorläufigDaten={.tm_year=126,.tm_mon=0,.tm_mday=1};return &vorläufigDaten;}
static FILE datenströme[18]={{1,0,1},{2,0,1}};FILE*stdout=&datenströme[0],*stderr=&datenströme[1];
FILE*fdopen(int dateiKennwert,const char*methodeBetriebsart){(void)methodeBetriebsart;for(unsigned ordnungszahlIndex=2;ordnungszahlIndex<18;ordnungszahlIndex++)if(!datenströme[ordnungszahlIndex].benutztKapazität){datenströme[ordnungszahlIndex].benutztKapazität=1;datenströme[ordnungszahlIndex].fehler=0;datenströme[ordnungszahlIndex].dateiKennwert=dateiKennwert;return &datenströme[ordnungszahlIndex];}fehler=24;return 0;}
int fflush(FILE*dateiEintrag){return dateiEintrag&&dateiEintrag->fehler?-1:0;}
int fclose(FILE*dateiEintrag){int zurückgegebenWert=close(dateiEintrag->dateiKennwert);if(dateiEintrag->fehler)zurückgegebenWert=-1;dateiEintrag->benutztKapazität=0;return zurückgegebenWert;}
size_t fwrite(const void*datenPosition,size_t zeichenketteDaten,size_t elementeintragAnzahl,FILE*dateiEintrag){if(!zeichenketteDaten)return 0;if(elementeintragAnzahl>SIZE_MAX/zeichenketteDaten){dateiEintrag->fehler=1;return 0;}long zurückgegebenWert=write(dateiEintrag->dateiKennwert,datenPosition,zeichenketteDaten*elementeintragAnzahl);if(zurückgegebenWert<0){dateiEintrag->fehler=1;return 0;}return (size_t)zurückgegebenWert/zeichenketteDaten;}
int fputc(int zeichenKode,FILE*dateiEintrag){unsigned char zweiterWert=zeichenKode;return fwrite(&zweiterWert,1,1,dateiEintrag)==1?zweiterWert:EOF;}
int fputs(const char*zeichenketteDaten,FILE*dateiEintrag){return fwrite(zeichenketteDaten,1,strlen(zeichenketteDaten),dateiEintrag)==strlen(zeichenketteDaten)?0:EOF;}
static void wertAblegen(char*ergebnisDaten,size_t kapazitätHöchstwert,size_t*aktuellPosition,char zeichenKode){if(*aktuellPosition+1<kapazitätHöchstwert)ergebnisDaten[*aktuellPosition]=zeichenKode;(*aktuellPosition)++;}
int vsnprintf(char*ergebnisDaten,size_t kapazitätHöchstwert,const char*format,va_list variableArgumenteArgumente){
    size_t aktuellPosition=0;while(*format){if(*format!='%'){wertAblegen(ergebnisDaten,kapazitätHöchstwert,&aktuellPosition,*format++);continue;}format++;
        int linksSeiteRand=0,nullwertWert=0,ersatzwegWert=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')linksSeiteRand=1;if(*format=='0')nullwertWert=1;if(*format=='#')ersatzwegWert=1;format++;}
        int breiteWert=0,genauigkeitWert=-1;if(*format=='*'){breiteWert=va_arg(variableArgumenteArgumente,int);format++;}else while(*format>='0'&&*format<='9')breiteWert=breiteWert*10+*format++-'0';
        if(*format=='.'){format++;genauigkeitWert=0;if(*format=='*'){genauigkeitWert=va_arg(variableArgumenteArgumente,int);format++;}else while(*format>='0'&&*format<='9')genauigkeitWert=genauigkeitWert*10+*format++-'0';}
        int breitZeichen=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')breitZeichen=1;format++;}
        char typKategorie=*format?*format++:0,pufferSpeichergerät[80];const char*zeichenketteDaten=pufferSpeichergerät;size_t elementeintragAnzahl=0;
        if(typKategorie=='s'){zeichenketteDaten=va_arg(variableArgumenteArgumente,const char*);if(!zeichenketteDaten)zeichenketteDaten="(null)";elementeintragAnzahl=strlen(zeichenketteDaten);if(genauigkeitWert>=0&&elementeintragAnzahl>(size_t)genauigkeitWert)elementeintragAnzahl=genauigkeitWert;}
        else if(typKategorie=='c'){pufferSpeichergerät[0]=va_arg(variableArgumenteArgumente,int);elementeintragAnzahl=1;}
        else if(typKategorie=='%'){pufferSpeichergerät[0]='%';elementeintragAnzahl=1;}
        else if(typKategorie=='d'||typKategorie=='i'||typKategorie=='u'||typKategorie=='x'||typKategorie=='X'||typKategorie=='o'||typKategorie=='p'){
            unsigned long long Wert;int negativ=0;
            if(typKategorie=='d'||typKategorie=='i'){long long vorläufigDaten=breitZeichen?va_arg(variableArgumenteArgumente,long long):va_arg(variableArgumenteArgumente,int);negativ=vorläufigDaten<0;Wert=negativ?0-(unsigned long long)vorläufigDaten:vorläufigDaten;}
            else Wert=typKategorie=='p'?(uintptr_t)va_arg(variableArgumenteArgumente,void*):breitZeichen?va_arg(variableArgumenteArgumente,unsigned long long):va_arg(variableArgumenteArgumente,unsigned);
            unsigned hintergrundWert=typKategorie=='x'||typKategorie=='X'||typKategorie=='p'?16:typKategorie=='o'?8:10;char zifferAnzahl[64];unsigned benutztKapazität=0;
            do{zifferAnzahl[benutztKapazität++]="0123456789abcdef"[Wert%hintergrundWert];Wert/=hintergrundWert;}while(Wert);
            if(negativ)pufferSpeichergerät[elementeintragAnzahl++]='-';if(typKategorie=='p'||(ersatzwegWert&&hintergrundWert==16)){pufferSpeichergerät[elementeintragAnzahl++]='0';pufferSpeichergerät[elementeintragAnzahl++]='x';}
            for(int wertFüllen=(int)benutztKapazität;genauigkeitWert>wertFüllen&&elementeintragAnzahl<sizeof(pufferSpeichergerät)-benutztKapazität;wertFüllen++)pufferSpeichergerät[elementeintragAnzahl++]='0';
            if(nullwertWert&&!linksSeiteRand&&genauigkeitWert<0)while(breiteWert>(int)(elementeintragAnzahl+benutztKapazität)&&elementeintragAnzahl<sizeof(pufferSpeichergerät)-benutztKapazität)pufferSpeichergerät[elementeintragAnzahl++]='0';
            while(benutztKapazität)pufferSpeichergerät[elementeintragAnzahl++]=zifferAnzahl[--benutztKapazität];
        }else{pufferSpeichergerät[0]='?';elementeintragAnzahl=1;}
        if(breiteWert>4096)breiteWert=4096;while(!linksSeiteRand&&breiteWert>(int)elementeintragAnzahl){wertAblegen(ergebnisDaten,kapazitätHöchstwert,&aktuellPosition,' ');breiteWert--;}
        for(size_t ordnungszahlIndex=0;ordnungszahlIndex<elementeintragAnzahl;ordnungszahlIndex++)wertAblegen(ergebnisDaten,kapazitätHöchstwert,&aktuellPosition,zeichenketteDaten[ordnungszahlIndex]);while(linksSeiteRand&&breiteWert>(int)elementeintragAnzahl){wertAblegen(ergebnisDaten,kapazitätHöchstwert,&aktuellPosition,' ');breiteWert--;}
    }if(kapazitätHöchstwert)ergebnisDaten[aktuellPosition<kapazitätHöchstwert?aktuellPosition:kapazitätHöchstwert-1]=0;return aktuellPosition;
}
int snprintf(char*ergebnisDaten,size_t kapazitätHöchstwert,const char*dateiEintrag,...){va_list ersterWert;va_start(ersterWert,dateiEintrag);int zurückgegebenWert=vsnprintf(ergebnisDaten,kapazitätHöchstwert,dateiEintrag,ersterWert);va_end(ersterWert);return zurückgegebenWert;}
int sprintf(char*ergebnisDaten,const char*dateiEintrag,...){va_list ersterWert;va_start(ersterWert,dateiEintrag);int zurückgegebenWert=vsnprintf(ergebnisDaten,SIZE_MAX,dateiEintrag,ersterWert);va_end(ersterWert);return zurückgegebenWert;}
int vfprintf(FILE*datenstromWert,const char*dateiEintrag,va_list ersterWert){char zweiterWert[2048];int elementeintragAnzahl=vsnprintf(zweiterWert,sizeof(zweiterWert),dateiEintrag,ersterWert);if(elementeintragAnzahl>2047)elementeintragAnzahl=2047;return fwrite(zweiterWert,1,elementeintragAnzahl,datenstromWert)==(size_t)elementeintragAnzahl?elementeintragAnzahl:-1;}
int fprintf(FILE*datenstromWert,const char*dateiEintrag,...){va_list ersterWert;va_start(ersterWert,dateiEintrag);int zurückgegebenWert=vfprintf(datenstromWert,dateiEintrag,ersterWert);va_end(ersterWert);return zurückgegebenWert;}
int printf(const char*dateiEintrag,...){va_list ersterWert;va_start(ersterWert,dateiEintrag);int zurückgegebenWert=vfprintf(stdout,dateiEintrag,ersterWert);va_end(ersterWert);return zurückgegebenWert;}
