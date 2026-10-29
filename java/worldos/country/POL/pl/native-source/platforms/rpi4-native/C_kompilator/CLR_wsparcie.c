#include "../명명/기계연결이름.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "호출.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int błąd;
int *__errno_location(void){return &błąd;}
void exit(int Stan_WARTOŚĆ){사용자호출(6,Stan_WARTOŚĆ,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *czek_wyrażenie,const char *nazwa_pliku,unsigned wiersz_wejścia,const char *metoda_wpis_nazwa){fprintf(stderr,"cc assertion: %s %s:%u %s\n",czek_wyrażenie,nazwa_pliku,wiersz_wejścia,metoda_wpis_nazwa);exit(1);}
size_t strlen(const char*ciąg_dane){const char*dane_stanowisko=ciąg_dane;while(*dane_stanowisko)dane_stanowisko++;return dane_stanowisko-ciąg_dane;}
int strcmp(const char*첫째값,const char*SEKUNDA_WARTOŚĆ){while(*첫째값&&*첫째값==*SEKUNDA_WARTOŚĆ){첫째값++;SEKUNDA_WARTOŚĆ++;}return (unsigned char)*첫째값-(unsigned char)*SEKUNDA_WARTOŚĆ;}
int strncmp(const char*첫째값,const char*SEKUNDA_WARTOŚĆ,size_t towar_ILE_LICZB){while(towar_ILE_LICZB--){unsigned char współrzędna_X=*첫째값++,Y_współrzędna=*SEKUNDA_WARTOŚĆ++;if(współrzędna_X!=Y_współrzędna)return współrzędna_X-Y_współrzędna;if(!współrzędna_X)return 0;}return 0;}
char *strcpy(char*cel_dane,const char*ciąg_dane){char*반환값=cel_dane;while((*cel_dane++=*ciąg_dane++)){}return 반환값;}
char *strchr(const char*ciąg_dane,int kod_znaku){do{if(*ciąg_dane==(char)kod_znaku)return (char*)ciąg_dane;}while(*ciąg_dane++);return 0;}
char *strrchr(const char*ciąg_dane,int kod_znaku){const char*반환값=0;do{if(*ciąg_dane==(char)kod_znaku)반환값=ciąg_dane;}while(*ciąg_dane++);return (char*)반환값;}
char *strstr(const char*ciąg_dane,const char*Terminal_wpis){size_t towar_ILE_LICZB=strlen(Terminal_wpis);for(;*ciąg_dane;ciąg_dane++)if(!strncmp(ciąg_dane,Terminal_wpis,towar_ILE_LICZB))return (char*)ciąg_dane;return towar_ILE_LICZB?0:(char*)ciąg_dane;}
int memcmp(const void*첫째값,const void*SEKUNDA_WARTOŚĆ,size_t towar_ILE_LICZB){const unsigned char*współrzędna_X=첫째값,*Y_współrzędna=SEKUNDA_WARTOŚĆ;while(towar_ILE_LICZB--){if(*współrzędna_X!=*Y_współrzędna)return *współrzędna_X-*Y_współrzędna;współrzędna_X++;Y_współrzędna++;}return 0;}
void *memmove(void*cel_dane,const void*ciąg_dane,size_t towar_ILE_LICZB){unsigned char*współrzędna_X=cel_dane;const unsigned char*Y_współrzędna=ciąg_dane;if(współrzędna_X<Y_współrzędna){for(size_t 순번=0;순번<towar_ILE_LICZB;순번++)współrzędna_X[순번]=Y_współrzędna[순번];}else while(towar_ILE_LICZB){towar_ILE_LICZB--;współrzędna_X[towar_ILE_LICZB]=Y_współrzędna[towar_ILE_LICZB];}return cel_dane;}
static unsigned char alokacja_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct blok_danych {size_t Rozmiar;struct blok_danych*Dalej_towar;int 남은공간;int wypełnienie;uint64_t wyrównanie_lekcja;} blok_danych;
static blok_danych *첫항목;
void free(void*dane_stanowisko){if(!dane_stanowisko)return;blok_danych*SEKUNDA_WARTOŚĆ=(blok_danych*)dane_stanowisko-1;SEKUNDA_WARTOŚĆ->남은공간=1;for(blok_danych*Dalej_przesunąć=첫항목;Dalej_przesunąć&&Dalej_przesunąć->Dalej_towar;){if(Dalej_przesunąć->남은공간&&Dalej_przesunąć->Dalej_towar->남은공간){Dalej_przesunąć->Rozmiar+=sizeof(blok_danych)+Dalej_przesunąć->Dalej_towar->Rozmiar;Dalej_przesunąć->Dalej_towar=Dalej_przesunąć->Dalej_towar->Dalej_towar;}else Dalej_przesunąć=Dalej_przesunąć->Dalej_towar;}}
void *realloc(void*dane_stanowisko,size_t towar_ILE_LICZB){
    if(!towar_ILE_LICZB){free(dane_stanowisko);return 0;}if(towar_ILE_LICZB>sizeof(alokacja_Arena)-sizeof(blok_danych))return 0;towar_ILE_LICZB=(towar_ILE_LICZB+15)&~(size_t)15;
    if(!첫항목){첫항목=(blok_danych*)alokacja_Arena;첫항목->Rozmiar=sizeof(alokacja_Arena)-sizeof(blok_danych);첫항목->남은공간=1;첫항목->Dalej_towar=0;}
    blok_danych*Wstecz_towar=dane_stanowisko?(blok_danych*)dane_stanowisko-1:0;if(Wstecz_towar&&Wstecz_towar->Rozmiar>=towar_ILE_LICZB)return dane_stanowisko;
    for(blok_danych*SEKUNDA_WARTOŚĆ=첫항목;SEKUNDA_WARTOŚĆ;SEKUNDA_WARTOŚĆ=SEKUNDA_WARTOŚĆ->Dalej_towar)if(SEKUNDA_WARTOŚĆ->남은공간&&SEKUNDA_WARTOŚĆ->Rozmiar>=towar_ILE_LICZB){
        if(SEKUNDA_WARTOŚĆ->Rozmiar>=towar_ILE_LICZB+sizeof(blok_danych)+16){blok_danych*나머지부분=(blok_danych*)((unsigned char*)(SEKUNDA_WARTOŚĆ+1)+towar_ILE_LICZB);나머지부분->Rozmiar=SEKUNDA_WARTOŚĆ->Rozmiar-towar_ILE_LICZB-sizeof(blok_danych);나머지부분->Dalej_towar=SEKUNDA_WARTOŚĆ->Dalej_towar;나머지부분->남은공간=1;SEKUNDA_WARTOŚĆ->Dalej_towar=나머지부분;SEKUNDA_WARTOŚĆ->Rozmiar=towar_ILE_LICZB;}
        SEKUNDA_WARTOŚĆ->남은공간=0;void*반환값=SEKUNDA_WARTOŚĆ+1;if(Wstecz_towar){memcpy(반환값,dane_stanowisko,Wstecz_towar->Rozmiar);free(dane_stanowisko);}return 반환값;
    }błąd=12;return 0;
}
void *malloc(size_t towar_ILE_LICZB){return realloc(0,towar_ILE_LICZB);}
void *calloc(size_t towar_ILE_LICZB,size_t ciąg_dane){if(ciąg_dane&&towar_ILE_LICZB>SIZE_MAX/ciąg_dane)return 0;void*dane_stanowisko=malloc(towar_ILE_LICZB*ciąg_dane);if(dane_stanowisko)memset(dane_stanowisko,0,towar_ILE_LICZB*ciąg_dane);return dane_stanowisko;}
unsigned long long strtoull(const char*ciąg_dane,char**Koniec_przesunąć,int Tło_WARTOŚĆ){
    const char*START_przesunąć=ciąg_dane;while(*ciąg_dane==' '||(*ciąg_dane>=9&&*ciąg_dane<=13))ciąg_dane++;int systemy_informacyjne_negatywny=0;if(*ciąg_dane=='-'||*ciąg_dane=='+')systemy_informacyjne_negatywny=*ciąg_dane++=='-';
    if((!Tło_WARTOŚĆ||Tło_WARTOŚĆ==16)&&ciąg_dane[0]=='0'&&(ciąg_dane[1]=='x'||ciąg_dane[1]=='X')){Tło_WARTOŚĆ=16;ciąg_dane+=2;}if(!Tło_WARTOŚĆ)Tło_WARTOŚĆ=*ciąg_dane=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kod_znaku=*ciąg_dane,cel_dane=kod_znaku>='0'&&kod_znaku<='9'?kod_znaku-'0':kod_znaku>='a'&&kod_znaku<='z'?kod_znaku-'a'+10:kod_znaku>='A'&&kod_znaku<='Z'?kod_znaku-'A'+10:99;if(cel_dane>=(unsigned)Tło_WARTOŚĆ)break;하나라도=1;ciąg_dane++;if(임시값>(~0ull-cel_dane)/(unsigned)Tło_WARTOŚĆ){임시값=~0ull;błąd=34;}else 임시값=임시값*Tło_WARTOŚĆ+cel_dane;}
    if(Koniec_przesunąć)*Koniec_przesunąć=(char*)(하나라도?ciąg_dane:START_przesunąć);return systemy_informacyjne_negatywny?0-임시값:임시값;
}
unsigned long strtoul(const char*ciąg_dane,char**보조항목,int SEKUNDA_WARTOŚĆ){return strtoull(ciąg_dane,보조항목,SEKUNDA_WARTOŚĆ);}
long strtol(const char*ciąg_dane,char**보조항목,int SEKUNDA_WARTOŚĆ){return (long)strtoull(ciąg_dane,보조항목,SEKUNDA_WARTOŚĆ);}
int atoi(const char*ciąg_dane){return (int)strtol(ciąg_dane,0,10);}
long double ldexpl(long double współrzędna_X,int towar_ILE_LICZB){while(towar_ILE_LICZB>0){współrzędna_X*=2;towar_ILE_LICZB--;}while(towar_ILE_LICZB<0){współrzędna_X/=2;towar_ILE_LICZB++;}return współrzędna_X;}
long double strtold(const char*ciąg_dane,char**Koniec_przesunąć){
    const char*START_przesunąć=ciąg_dane;while(*ciąg_dane==' '||(*ciąg_dane>=9&&*ciąg_dane<=13))ciąg_dane++;int systemy_informacyjne_negatywny=0;if(*ciąg_dane=='-'||*ciąg_dane=='+')systemy_informacyjne_negatywny=*ciąg_dane++=='-';
    int Tło_WARTOŚĆ=10;if(ciąg_dane[0]=='0'&&(ciąg_dane[1]=='x'||ciąg_dane[1]=='X')){Tło_WARTOŚĆ=16;ciąg_dane+=2;}long double 임시값=0,skala=1;int 소수부=0,하나라도=0;
    for(;;){int kod_znaku=*ciąg_dane,cel_dane=kod_znaku>='0'&&kod_znaku<='9'?kod_znaku-'0':kod_znaku>='a'&&kod_znaku<='f'?kod_znaku-'a'+10:kod_znaku>='A'&&kod_znaku<='F'?kod_znaku-'A'+10:99;
        if(kod_znaku=='.'&&!소수부){소수부=1;ciąg_dane++;continue;}if(cel_dane>=Tło_WARTOŚĆ)break;하나라도=1;ciąg_dane++;임시값=임시값*Tło_WARTOŚĆ+cel_dane;if(소수부)skala*=Tło_WARTOŚĆ;
    }임시값/=skala;
    if((Tło_WARTOŚĆ==10&&(*ciąg_dane=='e'||*ciąg_dane=='E'))||(Tło_WARTOŚĆ==16&&(*ciąg_dane=='p'||*ciąg_dane=='P'))){const char*program_WARTOŚĆ=ciąg_dane++;int 빼기=0;if(*ciąg_dane=='-'||*ciąg_dane=='+')빼기=*ciąg_dane++=='-';int towar_ILE_LICZB=0,wpis_ILE_LICZB=0;while(*ciąg_dane>='0'&&*ciąg_dane<='9'){wpis_ILE_LICZB++;if(towar_ILE_LICZB<20000)towar_ILE_LICZB=towar_ILE_LICZB*10+*ciąg_dane-'0';ciąg_dane++;}if(!wpis_ILE_LICZB)ciąg_dane=program_WARTOŚĆ;else{long double czynnik=Tło_WARTOŚĆ==16?2:10;while(towar_ILE_LICZB-->0&&towar_ILE_LICZB<200000)임시값=빼기?임시값/czynnik:임시값*czynnik;}}
    if(Koniec_przesunąć)*Koniec_przesunąć=(char*)(하나라도?ciąg_dane:START_przesunąć);return systemy_informacyjne_negatywny?-임시값:임시값;
}
double strtod(const char*ciąg_dane,char**보조항목){return (double)strtold(ciąg_dane,보조항목);}float strtof(const char*ciąg_dane,char**보조항목){return (float)strtold(ciąg_dane,보조항목);}
void qsort(void*Tło_WARTOŚĆ,size_t towar_ILE_LICZB,size_t Rozmiar,int(*Porównaj)(const void*,const void*)){
    unsigned char*dane_stanowisko=Tło_WARTOŚĆ;for(size_t 순번=1;순번<towar_ILE_LICZB;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Porównaj(dane_stanowisko+(안쪽순번-1)*Rozmiar,dane_stanowisko+안쪽순번*Rozmiar)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Rozmiar;셋째순번++){unsigned char kod_znaku=dane_stanowisko[(안쪽순번-1)*Rozmiar+셋째순번];dane_stanowisko[(안쪽순번-1)*Rozmiar+셋째순번]=dane_stanowisko[안쪽순번*Rozmiar+셋째순번];dane_stanowisko[안쪽순번*Rozmiar+셋째순번]=kod_znaku;}
}
static struct {int 사용량,WYSZUKAJ_INDEKS;size_t pozycja;} 열림[24];
static unsigned char produkt_wyjściowy[32768];static size_t produkt_wyjściowy_zmienić_rozmiar,produkt_wyjściowy_stanowisko;static int produkt_wyjściowy_otwarty;
const unsigned char *C_produkt_wyjściowy(size_t *towar_ILE_LICZB){*towar_ILE_LICZB=produkt_wyjściowy_zmienić_rozmiar;return produkt_wyjściowy;}
int open(const char*Nazwa,int konfiguracja_BITS,...){
    if(!strcmp(Nazwa,"/@cc-output")){if(produkt_wyjściowy_otwarty){błąd=16;return -1;}produkt_wyjściowy_otwarty=1;produkt_wyjściowy_zmienić_rozmiar=produkt_wyjściowy_stanowisko=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompilator_Zasoby)/sizeof(kompilator_Zasoby[0]);순번++)if(!strcmp(Nazwa,kompilator_Zasoby[순번].Nazwa)){
        if(konfiguracja_BITS&3){błąd=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].WYSZUKAJ_INDEKS=순번;열림[안쪽순번].pozycja=0;return 128+안쪽순번;}błąd=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nazwa,konfiguracja_BITS,0,0,0,0);if(반환값<0){błąd=-반환값;return -1;}return 반환값;
}
int close(int dojście_do_pliku){if(dojście_do_pliku==100){produkt_wyjściowy_otwarty=0;return 0;}if(dojście_do_pliku>=128&&dojście_do_pliku<152){열림[dojście_do_pliku-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,dojście_do_pliku,0,0,0,0,0);if(반환값<0){błąd=-반환값;return -1;}return 0;}
long read(int dojście_do_pliku,void*dane,size_t towar_ILE_LICZB){
    if(dojście_do_pliku>=128&&dojście_do_pliku<152&&열림[dojście_do_pliku-128].사용량){int 순번=dojście_do_pliku-128;const kompilator_zasób*반환값=&kompilator_Zasoby[열림[순번].WYSZUKAJ_INDEKS];size_t 왼쪽=반환값->Rozmiar-열림[순번].pozycja;if(towar_ILE_LICZB>왼쪽)towar_ILE_LICZB=왼쪽;memcpy(dane,반환값->dane+열림[순번].pozycja,towar_ILE_LICZB);열림[순번].pozycja+=towar_ILE_LICZB;return towar_ILE_LICZB;}
    intptr_t 반환값=사용자호출(2,dojście_do_pliku,(uintptr_t)dane,towar_ILE_LICZB,0,0,0);if(반환값<0){błąd=-반환값;return -1;}return 반환값;
}
long write(int dojście_do_pliku,const void*dane,size_t towar_ILE_LICZB){
    if(dojście_do_pliku==100){if(towar_ILE_LICZB>sizeof(produkt_wyjściowy)-produkt_wyjściowy_stanowisko){błąd=28;return -1;}memcpy(produkt_wyjściowy+produkt_wyjściowy_stanowisko,dane,towar_ILE_LICZB);produkt_wyjściowy_stanowisko+=towar_ILE_LICZB;if(produkt_wyjściowy_zmienić_rozmiar<produkt_wyjściowy_stanowisko)produkt_wyjściowy_zmienić_rozmiar=produkt_wyjściowy_stanowisko;return towar_ILE_LICZB;}
    intptr_t 반환값=사용자호출(1,dojście_do_pliku,(uintptr_t)dane,towar_ILE_LICZB,0,0,0);if(반환값<0){błąd=-반환값;return -1;}return 반환값;
}
long lseek(int dojście_do_pliku,long przesunąć_WARTOŚĆ_450fc799,int szukać_źródło){
    if(dojście_do_pliku==100){long dane_stanowisko=przesunąć_WARTOŚĆ_450fc799+(szukać_źródło==0?0:szukać_źródło==1?produkt_wyjściowy_stanowisko:produkt_wyjściowy_zmienić_rozmiar);if(dane_stanowisko<0||(size_t)dane_stanowisko>sizeof(produkt_wyjściowy)){błąd=22;return -1;}produkt_wyjściowy_stanowisko=dane_stanowisko;return dane_stanowisko;}
    if(dojście_do_pliku>=128&&dojście_do_pliku<152&&열림[dojście_do_pliku-128].사용량){int 순번=dojście_do_pliku-128;long dane_stanowisko=przesunąć_WARTOŚĆ_450fc799+(szukać_źródło==0?0:szukać_źródło==1?열림[순번].pozycja:kompilator_Zasoby[열림[순번].WYSZUKAJ_INDEKS].Rozmiar);if(dane_stanowisko<0||(size_t)dane_stanowisko>kompilator_Zasoby[열림[순번].WYSZUKAJ_INDEKS].Rozmiar){błąd=22;return -1;}열림[순번].pozycja=dane_stanowisko;return dane_stanowisko;}
    intptr_t 반환값=사용자호출(5,dojście_do_pliku,przesunąć_WARTOŚĆ_450fc799,szukać_źródło,0,0,0);if(반환값<0){błąd=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nazwa){intptr_t 반환값=사용자호출(11,(uintptr_t)Nazwa,0,0,0,0,0);if(반환값<0){błąd=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nazwa,char*KR_dane){if(!KR_dane){KR_dane=malloc(strlen(Nazwa)+1);if(!KR_dane)return 0;}return strcpy(KR_dane,Nazwa);}
char *getcwd(char*dane_stanowisko,size_t towar_ILE_LICZB){if(towar_ILE_LICZB<2){błąd=34;return 0;}dane_stanowisko[0]='/';dane_stanowisko[1]=0;return dane_stanowisko;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_wpis){time_t 임시값=0;if(Terminal_wpis)*Terminal_wpis=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_wpis){(void)Terminal_wpis;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Strumienie[18]={{1,0,1},{2,0,1}};FILE*stdout=&Strumienie[0],*stderr=&Strumienie[1];
FILE*fdopen(int dojście_do_pliku,const char*metoda_tryb){(void)metoda_tryb;for(unsigned 순번=2;순번<18;순번++)if(!Strumienie[순번].사용량){Strumienie[순번].사용량=1;Strumienie[순번].błąd=0;Strumienie[순번].dojście_do_pliku=dojście_do_pliku;return &Strumienie[순번];}błąd=24;return 0;}
int fflush(FILE*Plik_wpis){return Plik_wpis&&Plik_wpis->błąd?-1:0;}
int fclose(FILE*Plik_wpis){int 반환값=close(Plik_wpis->dojście_do_pliku);if(Plik_wpis->błąd)반환값=-1;Plik_wpis->사용량=0;return 반환값;}
size_t fwrite(const void*dane_stanowisko,size_t ciąg_dane,size_t towar_ILE_LICZB,FILE*Plik_wpis){if(!ciąg_dane)return 0;if(towar_ILE_LICZB>SIZE_MAX/ciąg_dane){Plik_wpis->błąd=1;return 0;}long 반환값=write(Plik_wpis->dojście_do_pliku,dane_stanowisko,ciąg_dane*towar_ILE_LICZB);if(반환값<0){Plik_wpis->błąd=1;return 0;}return (size_t)반환값/ciąg_dane;}
int fputc(int kod_znaku,FILE*Plik_wpis){unsigned char SEKUNDA_WARTOŚĆ=kod_znaku;return fwrite(&SEKUNDA_WARTOŚĆ,1,1,Plik_wpis)==1?SEKUNDA_WARTOŚĆ:EOF;}
int fputs(const char*ciąg_dane,FILE*Plik_wpis){return fwrite(ciąg_dane,1,strlen(ciąg_dane),Plik_wpis)==strlen(ciąg_dane)?0:EOF;}
static void 넣기(char*KR_dane,size_t 용량한도,size_t*bieżący_stanowisko,char kod_znaku){if(*bieżący_stanowisko+1<용량한도)KR_dane[*bieżący_stanowisko]=kod_znaku;(*bieżący_stanowisko)++;}
int vsnprintf(char*KR_dane,size_t 용량한도,const char*format,va_list 가변인수){
    size_t bieżący_stanowisko=0;while(*format){if(*format!='%'){넣기(KR_dane,용량한도,&bieżący_stanowisko,*format++);continue;}format++;
        int 왼쪽=0,wartość_zerowa=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')wartość_zerowa=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,precyzja_WARTOŚĆ=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;precyzja_WARTOŚĆ=0;if(*format=='*'){precyzja_WARTOŚĆ=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')precyzja_WARTOŚĆ=precyzja_WARTOŚĆ*10+*format++-'0';}
        int znak_dwubajtowy=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')znak_dwubajtowy=1;format++;}
        char TYP_obszar=*format?*format++:0,magazyn_buforowy[80];const char*ciąg_dane=magazyn_buforowy;size_t towar_ILE_LICZB=0;
        if(TYP_obszar=='s'){ciąg_dane=va_arg(가변인수,const char*);if(!ciąg_dane)ciąg_dane="(null)";towar_ILE_LICZB=strlen(ciąg_dane);if(precyzja_WARTOŚĆ>=0&&towar_ILE_LICZB>(size_t)precyzja_WARTOŚĆ)towar_ILE_LICZB=precyzja_WARTOŚĆ;}
        else if(TYP_obszar=='c'){magazyn_buforowy[0]=va_arg(가변인수,int);towar_ILE_LICZB=1;}
        else if(TYP_obszar=='%'){magazyn_buforowy[0]='%';towar_ILE_LICZB=1;}
        else if(TYP_obszar=='d'||TYP_obszar=='i'||TYP_obszar=='u'||TYP_obszar=='x'||TYP_obszar=='X'||TYP_obszar=='o'||TYP_obszar=='p'){
            unsigned long long WARTOŚĆ;int negatywny=0;
            if(TYP_obszar=='d'||TYP_obszar=='i'){long long 임시값=znak_dwubajtowy?va_arg(가변인수,long long):va_arg(가변인수,int);negatywny=임시값<0;WARTOŚĆ=negatywny?0-(unsigned long long)임시값:임시값;}
            else WARTOŚĆ=TYP_obszar=='p'?(uintptr_t)va_arg(가변인수,void*):znak_dwubajtowy?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Tło_WARTOŚĆ=TYP_obszar=='x'||TYP_obszar=='X'||TYP_obszar=='p'?16:TYP_obszar=='o'?8:10;char cyfra_ILE_LICZB[64];unsigned 사용량=0;
            do{cyfra_ILE_LICZB[사용량++]="0123456789abcdef"[WARTOŚĆ%Tło_WARTOŚĆ];WARTOŚĆ/=Tło_WARTOŚĆ;}while(WARTOŚĆ);
            if(negatywny)magazyn_buforowy[towar_ILE_LICZB++]='-';if(TYP_obszar=='p'||(대체값&&Tło_WARTOŚĆ==16)){magazyn_buforowy[towar_ILE_LICZB++]='0';magazyn_buforowy[towar_ILE_LICZB++]='x';}
            for(int Wypełnij_WARTOŚĆ=(int)사용량;precyzja_WARTOŚĆ>Wypełnij_WARTOŚĆ&&towar_ILE_LICZB<sizeof(magazyn_buforowy)-사용량;Wypełnij_WARTOŚĆ++)magazyn_buforowy[towar_ILE_LICZB++]='0';
            if(wartość_zerowa&&!왼쪽&&precyzja_WARTOŚĆ<0)while(너비>(int)(towar_ILE_LICZB+사용량)&&towar_ILE_LICZB<sizeof(magazyn_buforowy)-사용량)magazyn_buforowy[towar_ILE_LICZB++]='0';
            while(사용량)magazyn_buforowy[towar_ILE_LICZB++]=cyfra_ILE_LICZB[--사용량];
        }else{magazyn_buforowy[0]='?';towar_ILE_LICZB=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)towar_ILE_LICZB){넣기(KR_dane,용량한도,&bieżący_stanowisko,' ');너비--;}
        for(size_t 순번=0;순번<towar_ILE_LICZB;순번++)넣기(KR_dane,용량한도,&bieżący_stanowisko,ciąg_dane[순번]);while(왼쪽&&너비>(int)towar_ILE_LICZB){넣기(KR_dane,용량한도,&bieżący_stanowisko,' ');너비--;}
    }if(용량한도)KR_dane[bieżący_stanowisko<용량한도?bieżący_stanowisko:용량한도-1]=0;return bieżący_stanowisko;
}
int snprintf(char*KR_dane,size_t 용량한도,const char*Plik_wpis,...){va_list 첫째값;va_start(첫째값,Plik_wpis);int 반환값=vsnprintf(KR_dane,용량한도,Plik_wpis,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_dane,const char*Plik_wpis,...){va_list 첫째값;va_start(첫째값,Plik_wpis);int 반환값=vsnprintf(KR_dane,SIZE_MAX,Plik_wpis,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_WARTOŚĆ,const char*Plik_wpis,va_list 첫째값){char SEKUNDA_WARTOŚĆ[2048];int towar_ILE_LICZB=vsnprintf(SEKUNDA_WARTOŚĆ,sizeof(SEKUNDA_WARTOŚĆ),Plik_wpis,첫째값);if(towar_ILE_LICZB>2047)towar_ILE_LICZB=2047;return fwrite(SEKUNDA_WARTOŚĆ,1,towar_ILE_LICZB,Stream_WARTOŚĆ)==(size_t)towar_ILE_LICZB?towar_ILE_LICZB:-1;}
int fprintf(FILE*Stream_WARTOŚĆ,const char*Plik_wpis,...){va_list 첫째값;va_start(첫째값,Plik_wpis);int 반환값=vfprintf(Stream_WARTOŚĆ,Plik_wpis,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Plik_wpis,...){va_list 첫째값;va_start(첫째값,Plik_wpis);int 반환값=vfprintf(stdout,Plik_wpis,첫째값);va_end(첫째값);return 반환값;}
