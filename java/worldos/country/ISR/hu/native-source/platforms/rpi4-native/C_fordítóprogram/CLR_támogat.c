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
static int HIBA;
int *__errno_location(void){return &HIBA;}
void exit(int Állapot_ÉRTÉK){사용자호출(6,Állapot_ÉRTÉK,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *csekk_kifejezés,const char *Fájl,unsigned Vonal,const char *metódus_bejegyzés_név){fprintf(stderr,"cc assertion: %s %s:%u %s\n",csekk_kifejezés,Fájl,Vonal,metódus_bejegyzés_név);exit(1);}
size_t strlen(const char*sztring_adat){const char*adat_pozíció=sztring_adat;while(*adat_pozíció)adat_pozíció++;return adat_pozíció-sztring_adat;}
int strcmp(const char*첫째값,const char*MPERC_ÉRTÉK){while(*첫째값&&*첫째값==*MPERC_ÉRTÉK){첫째값++;MPERC_ÉRTÉK++;}return (unsigned char)*첫째값-(unsigned char)*MPERC_ÉRTÉK;}
int strncmp(const char*첫째값,const char*MPERC_ÉRTÉK,size_t cikk_DARAB){while(cikk_DARAB--){unsigned char x_koordináta=*첫째값++,Y_koordináta=*MPERC_ÉRTÉK++;if(x_koordináta!=Y_koordináta)return x_koordináta-Y_koordináta;if(!x_koordináta)return 0;}return 0;}
char *strcpy(char*cél_adat,const char*sztring_adat){char*반환값=cél_adat;while((*cél_adat++=*sztring_adat++)){}return 반환값;}
char *strchr(const char*sztring_adat,int kódpont){do{if(*sztring_adat==(char)kódpont)return (char*)sztring_adat;}while(*sztring_adat++);return 0;}
char *strrchr(const char*sztring_adat,int kódpont){const char*반환값=0;do{if(*sztring_adat==(char)kódpont)반환값=sztring_adat;}while(*sztring_adat++);return (char*)반환값;}
char *strstr(const char*sztring_adat,const char*Terminál_bejegyzés){size_t cikk_DARAB=strlen(Terminál_bejegyzés);for(;*sztring_adat;sztring_adat++)if(!strncmp(sztring_adat,Terminál_bejegyzés,cikk_DARAB))return (char*)sztring_adat;return cikk_DARAB?0:(char*)sztring_adat;}
int memcmp(const void*첫째값,const void*MPERC_ÉRTÉK,size_t cikk_DARAB){const unsigned char*x_koordináta=첫째값,*Y_koordináta=MPERC_ÉRTÉK;while(cikk_DARAB--){if(*x_koordináta!=*Y_koordináta)return *x_koordináta-*Y_koordináta;x_koordináta++;Y_koordináta++;}return 0;}
void *memmove(void*cél_adat,const void*sztring_adat,size_t cikk_DARAB){unsigned char*x_koordináta=cél_adat;const unsigned char*Y_koordináta=sztring_adat;if(x_koordináta<Y_koordináta){for(size_t 순번=0;순번<cikk_DARAB;순번++)x_koordináta[순번]=Y_koordináta[순번];}else while(cikk_DARAB){cikk_DARAB--;x_koordináta[cikk_DARAB]=Y_koordináta[cikk_DARAB];}return cél_adat;}
static unsigned char terhelés_Aréna[6*1024*1024] __attribute__((aligned(16)));
typedef struct adatblokk {size_t Méret;struct adatblokk*Tovább_cikk;int 남은공간;int kitöltés;uint64_t igazítás_lecke;} adatblokk;
static adatblokk *첫항목;
void free(void*adat_pozíció){if(!adat_pozíció)return;adatblokk*MPERC_ÉRTÉK=(adatblokk*)adat_pozíció-1;MPERC_ÉRTÉK->남은공간=1;for(adatblokk*Tovább_Ofszet=첫항목;Tovább_Ofszet&&Tovább_Ofszet->Tovább_cikk;){if(Tovább_Ofszet->남은공간&&Tovább_Ofszet->Tovább_cikk->남은공간){Tovább_Ofszet->Méret+=sizeof(adatblokk)+Tovább_Ofszet->Tovább_cikk->Méret;Tovább_Ofszet->Tovább_cikk=Tovább_Ofszet->Tovább_cikk->Tovább_cikk;}else Tovább_Ofszet=Tovább_Ofszet->Tovább_cikk;}}
void *realloc(void*adat_pozíció,size_t cikk_DARAB){
    if(!cikk_DARAB){free(adat_pozíció);return 0;}if(cikk_DARAB>sizeof(terhelés_Aréna)-sizeof(adatblokk))return 0;cikk_DARAB=(cikk_DARAB+15)&~(size_t)15;
    if(!첫항목){첫항목=(adatblokk*)terhelés_Aréna;첫항목->Méret=sizeof(terhelés_Aréna)-sizeof(adatblokk);첫항목->남은공간=1;첫항목->Tovább_cikk=0;}
    adatblokk*Előző_cikk=adat_pozíció?(adatblokk*)adat_pozíció-1:0;if(Előző_cikk&&Előző_cikk->Méret>=cikk_DARAB)return adat_pozíció;
    for(adatblokk*MPERC_ÉRTÉK=첫항목;MPERC_ÉRTÉK;MPERC_ÉRTÉK=MPERC_ÉRTÉK->Tovább_cikk)if(MPERC_ÉRTÉK->남은공간&&MPERC_ÉRTÉK->Méret>=cikk_DARAB){
        if(MPERC_ÉRTÉK->Méret>=cikk_DARAB+sizeof(adatblokk)+16){adatblokk*나머지부분=(adatblokk*)((unsigned char*)(MPERC_ÉRTÉK+1)+cikk_DARAB);나머지부분->Méret=MPERC_ÉRTÉK->Méret-cikk_DARAB-sizeof(adatblokk);나머지부분->Tovább_cikk=MPERC_ÉRTÉK->Tovább_cikk;나머지부분->남은공간=1;MPERC_ÉRTÉK->Tovább_cikk=나머지부분;MPERC_ÉRTÉK->Méret=cikk_DARAB;}
        MPERC_ÉRTÉK->남은공간=0;void*반환값=MPERC_ÉRTÉK+1;if(Előző_cikk){memcpy(반환값,adat_pozíció,Előző_cikk->Méret);free(adat_pozíció);}return 반환값;
    }HIBA=12;return 0;
}
void *malloc(size_t cikk_DARAB){return realloc(0,cikk_DARAB);}
void *calloc(size_t cikk_DARAB,size_t sztring_adat){if(sztring_adat&&cikk_DARAB>SIZE_MAX/sztring_adat)return 0;void*adat_pozíció=malloc(cikk_DARAB*sztring_adat);if(adat_pozíció)memset(adat_pozíció,0,cikk_DARAB*sztring_adat);return adat_pozíció;}
unsigned long long strtoull(const char*sztring_adat,char**megszüntet_Ofszet,int Háttér_ÉRTÉK){
    const char*START_Ofszet=sztring_adat;while(*sztring_adat==' '||(*sztring_adat>=9&&*sztring_adat<=13))sztring_adat++;int 음수여부=0;if(*sztring_adat=='-'||*sztring_adat=='+')음수여부=*sztring_adat++=='-';
    if((!Háttér_ÉRTÉK||Háttér_ÉRTÉK==16)&&sztring_adat[0]=='0'&&(sztring_adat[1]=='x'||sztring_adat[1]=='X')){Háttér_ÉRTÉK=16;sztring_adat+=2;}if(!Háttér_ÉRTÉK)Háttér_ÉRTÉK=*sztring_adat=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kódpont=*sztring_adat,cél_adat=kódpont>='0'&&kódpont<='9'?kódpont-'0':kódpont>='a'&&kódpont<='z'?kódpont-'a'+10:kódpont>='A'&&kódpont<='Z'?kódpont-'A'+10:99;if(cél_adat>=(unsigned)Háttér_ÉRTÉK)break;하나라도=1;sztring_adat++;if(임시값>(~0ull-cél_adat)/(unsigned)Háttér_ÉRTÉK){임시값=~0ull;HIBA=34;}else 임시값=임시값*Háttér_ÉRTÉK+cél_adat;}
    if(megszüntet_Ofszet)*megszüntet_Ofszet=(char*)(하나라도?sztring_adat:START_Ofszet);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*sztring_adat,char**보조항목,int MPERC_ÉRTÉK){return strtoull(sztring_adat,보조항목,MPERC_ÉRTÉK);}
long strtol(const char*sztring_adat,char**보조항목,int MPERC_ÉRTÉK){return (long)strtoull(sztring_adat,보조항목,MPERC_ÉRTÉK);}
int atoi(const char*sztring_adat){return (int)strtol(sztring_adat,0,10);}
long double ldexpl(long double x_koordináta,int cikk_DARAB){while(cikk_DARAB>0){x_koordináta*=2;cikk_DARAB--;}while(cikk_DARAB<0){x_koordináta/=2;cikk_DARAB++;}return x_koordináta;}
long double strtold(const char*sztring_adat,char**megszüntet_Ofszet){
    const char*START_Ofszet=sztring_adat;while(*sztring_adat==' '||(*sztring_adat>=9&&*sztring_adat<=13))sztring_adat++;int 음수여부=0;if(*sztring_adat=='-'||*sztring_adat=='+')음수여부=*sztring_adat++=='-';
    int Háttér_ÉRTÉK=10;if(sztring_adat[0]=='0'&&(sztring_adat[1]=='x'||sztring_adat[1]=='X')){Háttér_ÉRTÉK=16;sztring_adat+=2;}long double 임시값=0,méret=1;int 소수부=0,하나라도=0;
    for(;;){int kódpont=*sztring_adat,cél_adat=kódpont>='0'&&kódpont<='9'?kódpont-'0':kódpont>='a'&&kódpont<='f'?kódpont-'a'+10:kódpont>='A'&&kódpont<='F'?kódpont-'A'+10:99;
        if(kódpont=='.'&&!소수부){소수부=1;sztring_adat++;continue;}if(cél_adat>=Háttér_ÉRTÉK)break;하나라도=1;sztring_adat++;임시값=임시값*Háttér_ÉRTÉK+cél_adat;if(소수부)méret*=Háttér_ÉRTÉK;
    }임시값/=méret;
    if((Háttér_ÉRTÉK==10&&(*sztring_adat=='e'||*sztring_adat=='E'))||(Háttér_ÉRTÉK==16&&(*sztring_adat=='p'||*sztring_adat=='P'))){const char*bemutató_ÉRTÉK=sztring_adat++;int 빼기=0;if(*sztring_adat=='-'||*sztring_adat=='+')빼기=*sztring_adat++=='-';int cikk_DARAB=0,bejegyzés_DARAB=0;while(*sztring_adat>='0'&&*sztring_adat<='9'){bejegyzés_DARAB++;if(cikk_DARAB<20000)cikk_DARAB=cikk_DARAB*10+*sztring_adat-'0';sztring_adat++;}if(!bejegyzés_DARAB)sztring_adat=bemutató_ÉRTÉK;else{long double tényező=Háttér_ÉRTÉK==16?2:10;while(cikk_DARAB-->0&&cikk_DARAB<200000)임시값=빼기?임시값/tényező:임시값*tényező;}}
    if(megszüntet_Ofszet)*megszüntet_Ofszet=(char*)(하나라도?sztring_adat:START_Ofszet);return 음수여부?-임시값:임시값;
}
double strtod(const char*sztring_adat,char**보조항목){return (double)strtold(sztring_adat,보조항목);}float strtof(const char*sztring_adat,char**보조항목){return (float)strtold(sztring_adat,보조항목);}
void qsort(void*Háttér_ÉRTÉK,size_t cikk_DARAB,size_t Méret,int(*Világóra)(const void*,const void*)){
    unsigned char*adat_pozíció=Háttér_ÉRTÉK;for(size_t 순번=1;순번<cikk_DARAB;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Világóra(adat_pozíció+(안쪽순번-1)*Méret,adat_pozíció+안쪽순번*Méret)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Méret;셋째순번++){unsigned char kódpont=adat_pozíció[(안쪽순번-1)*Méret+셋째순번];adat_pozíció[(안쪽순번-1)*Méret+셋째순번]=adat_pozíció[안쪽순번*Méret+셋째순번];adat_pozíció[안쪽순번*Méret+셋째순번]=kódpont;}
}
static struct {int 사용량,KERES_INDEX;size_t Pozíció;} 열림[24];
static unsigned char kimenet[32768];static size_t kimenet_méretez,kimenet_pozíció;static int kimenet_készít;
const unsigned char *C_kimenet(size_t *cikk_DARAB){*cikk_DARAB=kimenet_méretez;return kimenet;}
int open(const char*Név,int konfiguráció_BITS,...){
    if(!strcmp(Név,"/@cc-output")){if(kimenet_készít){HIBA=16;return -1;}kimenet_készít=1;kimenet_méretez=kimenet_pozíció=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(fordítóprogram_Források)/sizeof(fordítóprogram_Források[0]);순번++)if(!strcmp(Név,fordítóprogram_Források[순번].Név)){
        if(konfiguráció_BITS&3){HIBA=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].KERES_INDEX=순번;열림[안쪽순번].Pozíció=0;return 128+안쪽순번;}HIBA=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Név,konfiguráció_BITS,0,0,0,0);if(반환값<0){HIBA=-반환값;return -1;}return 반환값;
}
int close(int fájlleíró){if(fájlleíró==100){kimenet_készít=0;return 0;}if(fájlleíró>=128&&fájlleíró<152){열림[fájlleíró-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fájlleíró,0,0,0,0,0);if(반환값<0){HIBA=-반환값;return -1;}return 0;}
long read(int fájlleíró,void*adat,size_t cikk_DARAB){
    if(fájlleíró>=128&&fájlleíró<152&&열림[fájlleíró-128].사용량){int 순번=fájlleíró-128;const fordítóprogram_erőforrás*반환값=&fordítóprogram_Források[열림[순번].KERES_INDEX];size_t 왼쪽=반환값->Méret-열림[순번].Pozíció;if(cikk_DARAB>왼쪽)cikk_DARAB=왼쪽;memcpy(adat,반환값->adat+열림[순번].Pozíció,cikk_DARAB);열림[순번].Pozíció+=cikk_DARAB;return cikk_DARAB;}
    intptr_t 반환값=사용자호출(2,fájlleíró,(uintptr_t)adat,cikk_DARAB,0,0,0);if(반환값<0){HIBA=-반환값;return -1;}return 반환값;
}
long write(int fájlleíró,const void*adat,size_t cikk_DARAB){
    if(fájlleíró==100){if(cikk_DARAB>sizeof(kimenet)-kimenet_pozíció){HIBA=28;return -1;}memcpy(kimenet+kimenet_pozíció,adat,cikk_DARAB);kimenet_pozíció+=cikk_DARAB;if(kimenet_méretez<kimenet_pozíció)kimenet_méretez=kimenet_pozíció;return cikk_DARAB;}
    intptr_t 반환값=사용자호출(1,fájlleíró,(uintptr_t)adat,cikk_DARAB,0,0,0);if(반환값<0){HIBA=-반환값;return -1;}return 반환값;
}
long lseek(int fájlleíró,long Ofszet_ÉRTÉK,int keres_eredet){
    if(fájlleíró==100){long adat_pozíció=Ofszet_ÉRTÉK+(keres_eredet==0?0:keres_eredet==1?kimenet_pozíció:kimenet_méretez);if(adat_pozíció<0||(size_t)adat_pozíció>sizeof(kimenet)){HIBA=22;return -1;}kimenet_pozíció=adat_pozíció;return adat_pozíció;}
    if(fájlleíró>=128&&fájlleíró<152&&열림[fájlleíró-128].사용량){int 순번=fájlleíró-128;long adat_pozíció=Ofszet_ÉRTÉK+(keres_eredet==0?0:keres_eredet==1?열림[순번].Pozíció:fordítóprogram_Források[열림[순번].KERES_INDEX].Méret);if(adat_pozíció<0||(size_t)adat_pozíció>fordítóprogram_Források[열림[순번].KERES_INDEX].Méret){HIBA=22;return -1;}열림[순번].Pozíció=adat_pozíció;return adat_pozíció;}
    intptr_t 반환값=사용자호출(5,fájlleíró,Ofszet_ÉRTÉK,keres_eredet,0,0,0);if(반환값<0){HIBA=-반환값;return -1;}return 반환값;
}
int unlink(const char*Név){intptr_t 반환값=사용자호출(11,(uintptr_t)Név,0,0,0,0,0);if(반환값<0){HIBA=-반환값;return -1;}return 반환값;}
char *realpath(const char*Név,char*KR_adat){if(!KR_adat){KR_adat=malloc(strlen(Név)+1);if(!KR_adat)return 0;}return strcpy(KR_adat,Név);}
char *getcwd(char*adat_pozíció,size_t cikk_DARAB){if(cikk_DARAB<2){HIBA=34;return 0;}adat_pozíció[0]='/';adat_pozíció[1]=0;return adat_pozíció;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminál_bejegyzés){time_t 임시값=0;if(Terminál_bejegyzés)*Terminál_bejegyzés=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminál_bejegyzés){(void)Terminál_bejegyzés;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE adatfolyamok[18]={{1,0,1},{2,0,1}};FILE*stdout=&adatfolyamok[0],*stderr=&adatfolyamok[1];
FILE*fdopen(int fájlleíró,const char*metódus_mód){(void)metódus_mód;for(unsigned 순번=2;순번<18;순번++)if(!adatfolyamok[순번].사용량){adatfolyamok[순번].사용량=1;adatfolyamok[순번].HIBA=0;adatfolyamok[순번].fájlleíró=fájlleíró;return &adatfolyamok[순번];}HIBA=24;return 0;}
int fflush(FILE*Fájl_bejegyzés){return Fájl_bejegyzés&&Fájl_bejegyzés->HIBA?-1:0;}
int fclose(FILE*Fájl_bejegyzés){int 반환값=close(Fájl_bejegyzés->fájlleíró);if(Fájl_bejegyzés->HIBA)반환값=-1;Fájl_bejegyzés->사용량=0;return 반환값;}
size_t fwrite(const void*adat_pozíció,size_t sztring_adat,size_t cikk_DARAB,FILE*Fájl_bejegyzés){if(!sztring_adat)return 0;if(cikk_DARAB>SIZE_MAX/sztring_adat){Fájl_bejegyzés->HIBA=1;return 0;}long 반환값=write(Fájl_bejegyzés->fájlleíró,adat_pozíció,sztring_adat*cikk_DARAB);if(반환값<0){Fájl_bejegyzés->HIBA=1;return 0;}return (size_t)반환값/sztring_adat;}
int fputc(int kódpont,FILE*Fájl_bejegyzés){unsigned char MPERC_ÉRTÉK=kódpont;return fwrite(&MPERC_ÉRTÉK,1,1,Fájl_bejegyzés)==1?MPERC_ÉRTÉK:EOF;}
int fputs(const char*sztring_adat,FILE*Fájl_bejegyzés){return fwrite(sztring_adat,1,strlen(sztring_adat),Fájl_bejegyzés)==strlen(sztring_adat)?0:EOF;}
static void 넣기(char*KR_adat,size_t 용량한도,size_t*aktuális_pozíció,char kódpont){if(*aktuális_pozíció+1<용량한도)KR_adat[*aktuális_pozíció]=kódpont;(*aktuális_pozíció)++;}
int vsnprintf(char*KR_adat,size_t 용량한도,const char*formáz,va_list 가변인수){
    size_t aktuális_pozíció=0;while(*formáz){if(*formáz!='%'){넣기(KR_adat,용량한도,&aktuális_pozíció,*formáz++);continue;}formáz++;
        int 왼쪽=0,nulla_ÉRTÉK=0,대체값=0;while(*formáz=='-'||*formáz=='0'||*formáz=='#'||*formáz=='+'||*formáz==' '){if(*formáz=='-')왼쪽=1;if(*formáz=='0')nulla_ÉRTÉK=1;if(*formáz=='#')대체값=1;formáz++;}
        int 너비=0,pontosság_ÉRTÉK=-1;if(*formáz=='*'){너비=va_arg(가변인수,int);formáz++;}else while(*formáz>='0'&&*formáz<='9')너비=너비*10+*formáz++-'0';
        if(*formáz=='.'){formáz++;pontosság_ÉRTÉK=0;if(*formáz=='*'){pontosság_ÉRTÉK=va_arg(가변인수,int);formáz++;}else while(*formáz>='0'&&*formáz<='9')pontosság_ÉRTÉK=pontosság_ÉRTÉK*10+*formáz++-'0';}
        int kétbájtos_karakter=0;while(*formáz=='l'||*formáz=='z'||*formáz=='t'||*formáz=='j'||*formáz=='h'){if(*formáz!='h')kétbájtos_karakter=1;formáz++;}
        char beír_terület=*formáz?*formáz++:0,puffertár[80];const char*sztring_adat=puffertár;size_t cikk_DARAB=0;
        if(beír_terület=='s'){sztring_adat=va_arg(가변인수,const char*);if(!sztring_adat)sztring_adat="(null)";cikk_DARAB=strlen(sztring_adat);if(pontosság_ÉRTÉK>=0&&cikk_DARAB>(size_t)pontosság_ÉRTÉK)cikk_DARAB=pontosság_ÉRTÉK;}
        else if(beír_terület=='c'){puffertár[0]=va_arg(가변인수,int);cikk_DARAB=1;}
        else if(beír_terület=='%'){puffertár[0]='%';cikk_DARAB=1;}
        else if(beír_terület=='d'||beír_terület=='i'||beír_terület=='u'||beír_terület=='x'||beír_terület=='X'||beír_terület=='o'||beír_terület=='p'){
            unsigned long long ÉRTÉK;int 음수표시=0;
            if(beír_terület=='d'||beír_terület=='i'){long long 임시값=kétbájtos_karakter?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;ÉRTÉK=음수표시?0-(unsigned long long)임시값:임시값;}
            else ÉRTÉK=beír_terület=='p'?(uintptr_t)va_arg(가변인수,void*):kétbájtos_karakter?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Háttér_ÉRTÉK=beír_terület=='x'||beír_terület=='X'||beír_terület=='p'?16:beír_terület=='o'?8:10;char számjegy_DARAB[64];unsigned 사용량=0;
            do{számjegy_DARAB[사용량++]="0123456789abcdef"[ÉRTÉK%Háttér_ÉRTÉK];ÉRTÉK/=Háttér_ÉRTÉK;}while(ÉRTÉK);
            if(음수표시)puffertár[cikk_DARAB++]='-';if(beír_terület=='p'||(대체값&&Háttér_ÉRTÉK==16)){puffertár[cikk_DARAB++]='0';puffertár[cikk_DARAB++]='x';}
            for(int kitöltés_ÉRTÉK=(int)사용량;pontosság_ÉRTÉK>kitöltés_ÉRTÉK&&cikk_DARAB<sizeof(puffertár)-사용량;kitöltés_ÉRTÉK++)puffertár[cikk_DARAB++]='0';
            if(nulla_ÉRTÉK&&!왼쪽&&pontosság_ÉRTÉK<0)while(너비>(int)(cikk_DARAB+사용량)&&cikk_DARAB<sizeof(puffertár)-사용량)puffertár[cikk_DARAB++]='0';
            while(사용량)puffertár[cikk_DARAB++]=számjegy_DARAB[--사용량];
        }else{puffertár[0]='?';cikk_DARAB=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)cikk_DARAB){넣기(KR_adat,용량한도,&aktuális_pozíció,' ');너비--;}
        for(size_t 순번=0;순번<cikk_DARAB;순번++)넣기(KR_adat,용량한도,&aktuális_pozíció,sztring_adat[순번]);while(왼쪽&&너비>(int)cikk_DARAB){넣기(KR_adat,용량한도,&aktuális_pozíció,' ');너비--;}
    }if(용량한도)KR_adat[aktuális_pozíció<용량한도?aktuális_pozíció:용량한도-1]=0;return aktuális_pozíció;
}
int snprintf(char*KR_adat,size_t 용량한도,const char*Fájl_bejegyzés,...){va_list 첫째값;va_start(첫째값,Fájl_bejegyzés);int 반환값=vsnprintf(KR_adat,용량한도,Fájl_bejegyzés,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_adat,const char*Fájl_bejegyzés,...){va_list 첫째값;va_start(첫째값,Fájl_bejegyzés);int 반환값=vsnprintf(KR_adat,SIZE_MAX,Fájl_bejegyzés,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_ÉRTÉK,const char*Fájl_bejegyzés,va_list 첫째값){char MPERC_ÉRTÉK[2048];int cikk_DARAB=vsnprintf(MPERC_ÉRTÉK,sizeof(MPERC_ÉRTÉK),Fájl_bejegyzés,첫째값);if(cikk_DARAB>2047)cikk_DARAB=2047;return fwrite(MPERC_ÉRTÉK,1,cikk_DARAB,Stream_ÉRTÉK)==(size_t)cikk_DARAB?cikk_DARAB:-1;}
int fprintf(FILE*Stream_ÉRTÉK,const char*Fájl_bejegyzés,...){va_list 첫째값;va_start(첫째값,Fájl_bejegyzés);int 반환값=vfprintf(Stream_ÉRTÉK,Fájl_bejegyzés,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Fájl_bejegyzés,...){va_list 첫째값;va_start(첫째값,Fájl_bejegyzés);int 반환값=vfprintf(stdout,Fájl_bejegyzés,첫째값);va_end(첫째값);return 반환값;}
