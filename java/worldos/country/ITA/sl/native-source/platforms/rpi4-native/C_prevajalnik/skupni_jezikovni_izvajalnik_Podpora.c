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
static int NAPAKA;
int *__errno_location(void){return &NAPAKA;}
void exit(int stanje_VALUE){사용자호출(6,stanje_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *preveriti_izraz,const char *Datoteka,unsigned Črtni,const char *metoda_vnos_ime){fprintf(stderr,"cc assertion: %s %s:%u %s\n",preveriti_izraz,Datoteka,Črtni,metoda_vnos_ime);exit(1);}
size_t strlen(const char*niz_podatki){const char*podatki_položaj=niz_podatki;while(*podatki_položaj)podatki_položaj++;return podatki_položaj-niz_podatki;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t element_COUNT){while(element_COUNT--){unsigned char koordinata_x=*첫째값++,세로좌표=*SECOND_VALUE++;if(koordinata_x!=세로좌표)return koordinata_x-세로좌표;if(!koordinata_x)return 0;}return 0;}
char *strcpy(char*cilj_podatki,const char*niz_podatki){char*반환값=cilj_podatki;while((*cilj_podatki++=*niz_podatki++)){}return 반환값;}
char *strchr(const char*niz_podatki,int koda_znaka){do{if(*niz_podatki==(char)koda_znaka)return (char*)niz_podatki;}while(*niz_podatki++);return 0;}
char *strrchr(const char*niz_podatki,int koda_znaka){const char*반환값=0;do{if(*niz_podatki==(char)koda_znaka)반환값=niz_podatki;}while(*niz_podatki++);return (char*)반환값;}
char *strstr(const char*niz_podatki,const char*Terminal_vnos){size_t element_COUNT=strlen(Terminal_vnos);for(;*niz_podatki;niz_podatki++)if(!strncmp(niz_podatki,Terminal_vnos,element_COUNT))return (char*)niz_podatki;return element_COUNT?0:(char*)niz_podatki;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t element_COUNT){const unsigned char*koordinata_x=첫째값,*세로좌표=SECOND_VALUE;while(element_COUNT--){if(*koordinata_x!=*세로좌표)return *koordinata_x-*세로좌표;koordinata_x++;세로좌표++;}return 0;}
void *memmove(void*cilj_podatki,const void*niz_podatki,size_t element_COUNT){unsigned char*koordinata_x=cilj_podatki;const unsigned char*세로좌표=niz_podatki;if(koordinata_x<세로좌표){for(size_t 순번=0;순번<element_COUNT;순번++)koordinata_x[순번]=세로좌표[순번];}else while(element_COUNT){element_COUNT--;koordinata_x[element_COUNT]=세로좌표[element_COUNT];}return cilj_podatki;}
static unsigned char dodelitev_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct blok_podatkov {size_t Velikost;struct blok_podatkov*Naprej_element;int 남은공간;int 채울크기;uint64_t poravnava_enota;} blok_podatkov;
static blok_podatkov *첫항목;
void free(void*podatki_položaj){if(!podatki_položaj)return;blok_podatkov*SECOND_VALUE=(blok_podatkov*)podatki_položaj-1;SECOND_VALUE->남은공간=1;for(blok_podatkov*Naprej_odmik=첫항목;Naprej_odmik&&Naprej_odmik->Naprej_element;){if(Naprej_odmik->남은공간&&Naprej_odmik->Naprej_element->남은공간){Naprej_odmik->Velikost+=sizeof(blok_podatkov)+Naprej_odmik->Naprej_element->Velikost;Naprej_odmik->Naprej_element=Naprej_odmik->Naprej_element->Naprej_element;}else Naprej_odmik=Naprej_odmik->Naprej_element;}}
void *realloc(void*podatki_položaj,size_t element_COUNT){
    if(!element_COUNT){free(podatki_položaj);return 0;}if(element_COUNT>sizeof(dodelitev_Arena)-sizeof(blok_podatkov))return 0;element_COUNT=(element_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(blok_podatkov*)dodelitev_Arena;첫항목->Velikost=sizeof(dodelitev_Arena)-sizeof(blok_podatkov);첫항목->남은공간=1;첫항목->Naprej_element=0;}
    blok_podatkov*이전=podatki_položaj?(blok_podatkov*)podatki_položaj-1:0;if(이전&&이전->Velikost>=element_COUNT)return podatki_položaj;
    for(blok_podatkov*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Naprej_element)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Velikost>=element_COUNT){
        if(SECOND_VALUE->Velikost>=element_COUNT+sizeof(blok_podatkov)+16){blok_podatkov*나머지부분=(blok_podatkov*)((unsigned char*)(SECOND_VALUE+1)+element_COUNT);나머지부분->Velikost=SECOND_VALUE->Velikost-element_COUNT-sizeof(blok_podatkov);나머지부분->Naprej_element=SECOND_VALUE->Naprej_element;나머지부분->남은공간=1;SECOND_VALUE->Naprej_element=나머지부분;SECOND_VALUE->Velikost=element_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,podatki_položaj,이전->Velikost);free(podatki_položaj);}return 반환값;
    }NAPAKA=12;return 0;
}
void *malloc(size_t element_COUNT){return realloc(0,element_COUNT);}
void *calloc(size_t element_COUNT,size_t niz_podatki){if(niz_podatki&&element_COUNT>SIZE_MAX/niz_podatki)return 0;void*podatki_položaj=malloc(element_COUNT*niz_podatki);if(podatki_položaj)memset(podatki_položaj,0,element_COUNT*niz_podatki);return podatki_položaj;}
unsigned long long strtoull(const char*niz_podatki,char**končati_klic_odmik,int Ozadje_VALUE){
    const char*Start_odmik=niz_podatki;while(*niz_podatki==' '||(*niz_podatki>=9&&*niz_podatki<=13))niz_podatki++;int 음수여부=0;if(*niz_podatki=='-'||*niz_podatki=='+')음수여부=*niz_podatki++=='-';
    if((!Ozadje_VALUE||Ozadje_VALUE==16)&&niz_podatki[0]=='0'&&(niz_podatki[1]=='x'||niz_podatki[1]=='X')){Ozadje_VALUE=16;niz_podatki+=2;}if(!Ozadje_VALUE)Ozadje_VALUE=*niz_podatki=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned koda_znaka=*niz_podatki,cilj_podatki=koda_znaka>='0'&&koda_znaka<='9'?koda_znaka-'0':koda_znaka>='a'&&koda_znaka<='z'?koda_znaka-'a'+10:koda_znaka>='A'&&koda_znaka<='Z'?koda_znaka-'A'+10:99;if(cilj_podatki>=(unsigned)Ozadje_VALUE)break;하나라도=1;niz_podatki++;if(임시값>(~0ull-cilj_podatki)/(unsigned)Ozadje_VALUE){임시값=~0ull;NAPAKA=34;}else 임시값=임시값*Ozadje_VALUE+cilj_podatki;}
    if(končati_klic_odmik)*končati_klic_odmik=(char*)(하나라도?niz_podatki:Start_odmik);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*niz_podatki,char**보조항목,int SECOND_VALUE){return strtoull(niz_podatki,보조항목,SECOND_VALUE);}
long strtol(const char*niz_podatki,char**보조항목,int SECOND_VALUE){return (long)strtoull(niz_podatki,보조항목,SECOND_VALUE);}
int atoi(const char*niz_podatki){return (int)strtol(niz_podatki,0,10);}
long double ldexpl(long double koordinata_x,int element_COUNT){while(element_COUNT>0){koordinata_x*=2;element_COUNT--;}while(element_COUNT<0){koordinata_x/=2;element_COUNT++;}return koordinata_x;}
long double strtold(const char*niz_podatki,char**končati_klic_odmik){
    const char*Start_odmik=niz_podatki;while(*niz_podatki==' '||(*niz_podatki>=9&&*niz_podatki<=13))niz_podatki++;int 음수여부=0;if(*niz_podatki=='-'||*niz_podatki=='+')음수여부=*niz_podatki++=='-';
    int Ozadje_VALUE=10;if(niz_podatki[0]=='0'&&(niz_podatki[1]=='x'||niz_podatki[1]=='X')){Ozadje_VALUE=16;niz_podatki+=2;}long double 임시값=0,prilagoditi=1;int 소수부=0,하나라도=0;
    for(;;){int koda_znaka=*niz_podatki,cilj_podatki=koda_znaka>='0'&&koda_znaka<='9'?koda_znaka-'0':koda_znaka>='a'&&koda_znaka<='f'?koda_znaka-'a'+10:koda_znaka>='A'&&koda_znaka<='F'?koda_znaka-'A'+10:99;
        if(koda_znaka=='.'&&!소수부){소수부=1;niz_podatki++;continue;}if(cilj_podatki>=Ozadje_VALUE)break;하나라도=1;niz_podatki++;임시값=임시값*Ozadje_VALUE+cilj_podatki;if(소수부)prilagoditi*=Ozadje_VALUE;
    }임시값/=prilagoditi;
    if((Ozadje_VALUE==10&&(*niz_podatki=='e'||*niz_podatki=='E'))||(Ozadje_VALUE==16&&(*niz_podatki=='p'||*niz_podatki=='P'))){const char*oddaja_VALUE_487749b8=niz_podatki++;int 빼기=0;if(*niz_podatki=='-'||*niz_podatki=='+')빼기=*niz_podatki++=='-';int element_COUNT=0,vnos_COUNT=0;while(*niz_podatki>='0'&&*niz_podatki<='9'){vnos_COUNT++;if(element_COUNT<20000)element_COUNT=element_COUNT*10+*niz_podatki-'0';niz_podatki++;}if(!vnos_COUNT)niz_podatki=oddaja_VALUE_487749b8;else{long double faktor=Ozadje_VALUE==16?2:10;while(element_COUNT-->0&&element_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(končati_klic_odmik)*končati_klic_odmik=(char*)(하나라도?niz_podatki:Start_odmik);return 음수여부?-임시값:임시값;
}
double strtod(const char*niz_podatki,char**보조항목){return (double)strtold(niz_podatki,보조항목);}float strtof(const char*niz_podatki,char**보조항목){return (float)strtold(niz_podatki,보조항목);}
void qsort(void*Ozadje_VALUE,size_t element_COUNT,size_t Velikost,int(*Primerjaj)(const void*,const void*)){
    unsigned char*podatki_položaj=Ozadje_VALUE;for(size_t 순번=1;순번<element_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Primerjaj(podatki_položaj+(안쪽순번-1)*Velikost,podatki_položaj+안쪽순번*Velikost)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Velikost;셋째순번++){unsigned char koda_znaka=podatki_položaj[(안쪽순번-1)*Velikost+셋째순번];podatki_položaj[(안쪽순번-1)*Velikost+셋째순번]=podatki_položaj[안쪽순번*Velikost+셋째순번];podatki_položaj[안쪽순번*Velikost+셋째순번]=koda_znaka;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Položaj;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *element_COUNT){*element_COUNT=출력크기;return 출력결과;}
int open(const char*Ime,int konfiguracija_storitev_Background_Intelligent_Transfer_Service,...){
    if(!strcmp(Ime,"/@cc-output")){if(출력열림){NAPAKA=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(prevajalnik_Viri)/sizeof(prevajalnik_Viri[0]);순번++)if(!strcmp(Ime,prevajalnik_Viri[순번].Ime)){
        if(konfiguracija_storitev_Background_Intelligent_Transfer_Service&3){NAPAKA=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Položaj=0;return 128+안쪽순번;}NAPAKA=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Ime,konfiguracija_storitev_Background_Intelligent_Transfer_Service,0,0,0,0);if(반환값<0){NAPAKA=-반환값;return -1;}return 반환값;
}
int close(int Datoteka_ročica){if(Datoteka_ročica==100){출력열림=0;return 0;}if(Datoteka_ročica>=128&&Datoteka_ročica<152){열림[Datoteka_ročica-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Datoteka_ročica,0,0,0,0,0);if(반환값<0){NAPAKA=-반환값;return -1;}return 0;}
long read(int Datoteka_ročica,void*podatki,size_t element_COUNT){
    if(Datoteka_ročica>=128&&Datoteka_ročica<152&&열림[Datoteka_ročica-128].사용량){int 순번=Datoteka_ročica-128;const prevajalnik_vir*반환값=&prevajalnik_Viri[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Velikost-열림[순번].Položaj;if(element_COUNT>왼쪽)element_COUNT=왼쪽;memcpy(podatki,반환값->podatki+열림[순번].Položaj,element_COUNT);열림[순번].Položaj+=element_COUNT;return element_COUNT;}
    intptr_t 반환값=사용자호출(2,Datoteka_ročica,(uintptr_t)podatki,element_COUNT,0,0,0);if(반환값<0){NAPAKA=-반환값;return -1;}return 반환값;
}
long write(int Datoteka_ročica,const void*podatki,size_t element_COUNT){
    if(Datoteka_ročica==100){if(element_COUNT>sizeof(출력결과)-출력위치){NAPAKA=28;return -1;}memcpy(출력결과+출력위치,podatki,element_COUNT);출력위치+=element_COUNT;if(출력크기<출력위치)출력크기=출력위치;return element_COUNT;}
    intptr_t 반환값=사용자호출(1,Datoteka_ročica,(uintptr_t)podatki,element_COUNT,0,0,0);if(반환값<0){NAPAKA=-반환값;return -1;}return 반환값;
}
long lseek(int Datoteka_ročica,long odmik_VALUE,int 기준점){
    if(Datoteka_ročica==100){long podatki_položaj=odmik_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(podatki_položaj<0||(size_t)podatki_položaj>sizeof(출력결과)){NAPAKA=22;return -1;}출력위치=podatki_položaj;return podatki_položaj;}
    if(Datoteka_ročica>=128&&Datoteka_ročica<152&&열림[Datoteka_ročica-128].사용량){int 순번=Datoteka_ročica-128;long podatki_položaj=odmik_VALUE+(기준점==0?0:기준점==1?열림[순번].Položaj:prevajalnik_Viri[열림[순번].LOOKUP_INDEX].Velikost);if(podatki_položaj<0||(size_t)podatki_položaj>prevajalnik_Viri[열림[순번].LOOKUP_INDEX].Velikost){NAPAKA=22;return -1;}열림[순번].Položaj=podatki_položaj;return podatki_položaj;}
    intptr_t 반환값=사용자호출(5,Datoteka_ročica,odmik_VALUE,기준점,0,0,0);if(반환값<0){NAPAKA=-반환값;return -1;}return 반환값;
}
int unlink(const char*Ime){intptr_t 반환값=사용자호출(11,(uintptr_t)Ime,0,0,0,0,0);if(반환값<0){NAPAKA=-반환값;return -1;}return 반환값;}
char *realpath(const char*Ime,char*KR_podatki){if(!KR_podatki){KR_podatki=malloc(strlen(Ime)+1);if(!KR_podatki)return 0;}return strcpy(KR_podatki,Ime);}
char *getcwd(char*podatki_položaj,size_t element_COUNT){if(element_COUNT<2){NAPAKA=34;return 0;}podatki_položaj[0]='/';podatki_položaj[1]=0;return podatki_položaj;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_vnos){time_t 임시값=0;if(Terminal_vnos)*Terminal_vnos=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_vnos){(void)Terminal_vnos;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Tokovi[18]={{1,0,1},{2,0,1}};FILE*stdout=&Tokovi[0],*stderr=&Tokovi[1];
FILE*fdopen(int Datoteka_ročica,const char*metoda_MODE){(void)metoda_MODE;for(unsigned 순번=2;순번<18;순번++)if(!Tokovi[순번].사용량){Tokovi[순번].사용량=1;Tokovi[순번].NAPAKA=0;Tokovi[순번].Datoteka_ročica=Datoteka_ročica;return &Tokovi[순번];}NAPAKA=24;return 0;}
int fflush(FILE*Datoteka_vnos){return Datoteka_vnos&&Datoteka_vnos->NAPAKA?-1:0;}
int fclose(FILE*Datoteka_vnos){int 반환값=close(Datoteka_vnos->Datoteka_ročica);if(Datoteka_vnos->NAPAKA)반환값=-1;Datoteka_vnos->사용량=0;return 반환값;}
size_t fwrite(const void*podatki_položaj,size_t niz_podatki,size_t element_COUNT,FILE*Datoteka_vnos){if(!niz_podatki)return 0;if(element_COUNT>SIZE_MAX/niz_podatki){Datoteka_vnos->NAPAKA=1;return 0;}long 반환값=write(Datoteka_vnos->Datoteka_ročica,podatki_položaj,niz_podatki*element_COUNT);if(반환값<0){Datoteka_vnos->NAPAKA=1;return 0;}return (size_t)반환값/niz_podatki;}
int fputc(int koda_znaka,FILE*Datoteka_vnos){unsigned char SECOND_VALUE=koda_znaka;return fwrite(&SECOND_VALUE,1,1,Datoteka_vnos)==1?SECOND_VALUE:EOF;}
int fputs(const char*niz_podatki,FILE*Datoteka_vnos){return fwrite(niz_podatki,1,strlen(niz_podatki),Datoteka_vnos)==strlen(niz_podatki)?0:EOF;}
static void 넣기(char*KR_podatki,size_t 용량한도,size_t*sprotno_položaj,char koda_znaka){if(*sprotno_položaj+1<용량한도)KR_podatki[*sprotno_položaj]=koda_znaka;(*sprotno_položaj)++;}
int vsnprintf(char*KR_podatki,size_t 용량한도,const char*oblika,va_list 가변인수){
    size_t sprotno_položaj=0;while(*oblika){if(*oblika!='%'){넣기(KR_podatki,용량한도,&sprotno_položaj,*oblika++);continue;}oblika++;
        int 왼쪽=0,ničelna_vrednost=0,대체값=0;while(*oblika=='-'||*oblika=='0'||*oblika=='#'||*oblika=='+'||*oblika==' '){if(*oblika=='-')왼쪽=1;if(*oblika=='0')ničelna_vrednost=1;if(*oblika=='#')대체값=1;oblika++;}
        int 너비=0,natančnost_VALUE=-1;if(*oblika=='*'){너비=va_arg(가변인수,int);oblika++;}else while(*oblika>='0'&&*oblika<='9')너비=너비*10+*oblika++-'0';
        if(*oblika=='.'){oblika++;natančnost_VALUE=0;if(*oblika=='*'){natančnost_VALUE=va_arg(가변인수,int);oblika++;}else while(*oblika>='0'&&*oblika<='9')natančnost_VALUE=natančnost_VALUE*10+*oblika++-'0';}
        int širok_znak=0;while(*oblika=='l'||*oblika=='z'||*oblika=='t'||*oblika=='j'||*oblika=='h'){if(*oblika!='h')širok_znak=1;oblika++;}
        char Tip_območje=*oblika?*oblika++:0,medpomnilnik_Senzor_prostora[80];const char*niz_podatki=medpomnilnik_Senzor_prostora;size_t element_COUNT=0;
        if(Tip_območje=='s'){niz_podatki=va_arg(가변인수,const char*);if(!niz_podatki)niz_podatki="(null)";element_COUNT=strlen(niz_podatki);if(natančnost_VALUE>=0&&element_COUNT>(size_t)natančnost_VALUE)element_COUNT=natančnost_VALUE;}
        else if(Tip_območje=='c'){medpomnilnik_Senzor_prostora[0]=va_arg(가변인수,int);element_COUNT=1;}
        else if(Tip_območje=='%'){medpomnilnik_Senzor_prostora[0]='%';element_COUNT=1;}
        else if(Tip_območje=='d'||Tip_območje=='i'||Tip_območje=='u'||Tip_območje=='x'||Tip_območje=='X'||Tip_območje=='o'||Tip_območje=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(Tip_območje=='d'||Tip_območje=='i'){long long 임시값=širok_znak?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=Tip_območje=='p'?(uintptr_t)va_arg(가변인수,void*):širok_znak?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Ozadje_VALUE=Tip_območje=='x'||Tip_območje=='X'||Tip_območje=='p'?16:Tip_območje=='o'?8:10;char številka_COUNT[64];unsigned 사용량=0;
            do{številka_COUNT[사용량++]="0123456789abcdef"[VALUE%Ozadje_VALUE];VALUE/=Ozadje_VALUE;}while(VALUE);
            if(음수표시)medpomnilnik_Senzor_prostora[element_COUNT++]='-';if(Tip_območje=='p'||(대체값&&Ozadje_VALUE==16)){medpomnilnik_Senzor_prostora[element_COUNT++]='0';medpomnilnik_Senzor_prostora[element_COUNT++]='x';}
            for(int polnilo_VALUE=(int)사용량;natančnost_VALUE>polnilo_VALUE&&element_COUNT<sizeof(medpomnilnik_Senzor_prostora)-사용량;polnilo_VALUE++)medpomnilnik_Senzor_prostora[element_COUNT++]='0';
            if(ničelna_vrednost&&!왼쪽&&natančnost_VALUE<0)while(너비>(int)(element_COUNT+사용량)&&element_COUNT<sizeof(medpomnilnik_Senzor_prostora)-사용량)medpomnilnik_Senzor_prostora[element_COUNT++]='0';
            while(사용량)medpomnilnik_Senzor_prostora[element_COUNT++]=številka_COUNT[--사용량];
        }else{medpomnilnik_Senzor_prostora[0]='?';element_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)element_COUNT){넣기(KR_podatki,용량한도,&sprotno_položaj,' ');너비--;}
        for(size_t 순번=0;순번<element_COUNT;순번++)넣기(KR_podatki,용량한도,&sprotno_položaj,niz_podatki[순번]);while(왼쪽&&너비>(int)element_COUNT){넣기(KR_podatki,용량한도,&sprotno_položaj,' ');너비--;}
    }if(용량한도)KR_podatki[sprotno_položaj<용량한도?sprotno_položaj:용량한도-1]=0;return sprotno_položaj;
}
int snprintf(char*KR_podatki,size_t 용량한도,const char*Datoteka_vnos,...){va_list 첫째값;va_start(첫째값,Datoteka_vnos);int 반환값=vsnprintf(KR_podatki,용량한도,Datoteka_vnos,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_podatki,const char*Datoteka_vnos,...){va_list 첫째값;va_start(첫째값,Datoteka_vnos);int 반환값=vsnprintf(KR_podatki,SIZE_MAX,Datoteka_vnos,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*tok_VALUE,const char*Datoteka_vnos,va_list 첫째값){char SECOND_VALUE[2048];int element_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Datoteka_vnos,첫째값);if(element_COUNT>2047)element_COUNT=2047;return fwrite(SECOND_VALUE,1,element_COUNT,tok_VALUE)==(size_t)element_COUNT?element_COUNT:-1;}
int fprintf(FILE*tok_VALUE,const char*Datoteka_vnos,...){va_list 첫째값;va_start(첫째값,Datoteka_vnos);int 반환값=vfprintf(tok_VALUE,Datoteka_vnos,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Datoteka_vnos,...){va_list 첫째값;va_start(첫째값,Datoteka_vnos);int 반환값=vfprintf(stdout,Datoteka_vnos,첫째값);va_end(첫째값);return 반환값;}
