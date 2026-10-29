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
static int greška;
int *__errno_location(void){return &greška;}
void exit(int Status_VALUE){사용자호출(6,Status_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *proveriti_izraz,const char *Datoteka,unsigned red,const char *metod_stavka_ime){fprintf(stderr,"cc assertion: %s %s:%u %s\n",proveriti_izraz,Datoteka,red,metod_stavka_ime);exit(1);}
size_t strlen(const char*niska_podaci){const char*podaci_pozicija=niska_podaci;while(*podaci_pozicija)podaci_pozicija++;return podaci_pozicija-niska_podaci;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t stavka_COUNT){while(stavka_COUNT--){unsigned char x_koordinata=*첫째값++,세로좌표=*SECOND_VALUE++;if(x_koordinata!=세로좌표)return x_koordinata-세로좌표;if(!x_koordinata)return 0;}return 0;}
char *strcpy(char*odredište_podaci,const char*niska_podaci){char*반환값=odredište_podaci;while((*odredište_podaci++=*niska_podaci++)){}return 반환값;}
char *strchr(const char*niska_podaci,int kôd_znaka){do{if(*niska_podaci==(char)kôd_znaka)return (char*)niska_podaci;}while(*niska_podaci++);return 0;}
char *strrchr(const char*niska_podaci,int kôd_znaka){const char*반환값=0;do{if(*niska_podaci==(char)kôd_znaka)반환값=niska_podaci;}while(*niska_podaci++);return (char*)반환값;}
char *strstr(const char*niska_podaci,const char*Terminal_stavka){size_t stavka_COUNT=strlen(Terminal_stavka);for(;*niska_podaci;niska_podaci++)if(!strncmp(niska_podaci,Terminal_stavka,stavka_COUNT))return (char*)niska_podaci;return stavka_COUNT?0:(char*)niska_podaci;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t stavka_COUNT){const unsigned char*x_koordinata=첫째값,*세로좌표=SECOND_VALUE;while(stavka_COUNT--){if(*x_koordinata!=*세로좌표)return *x_koordinata-*세로좌표;x_koordinata++;세로좌표++;}return 0;}
void *memmove(void*odredište_podaci,const void*niska_podaci,size_t stavka_COUNT){unsigned char*x_koordinata=odredište_podaci;const unsigned char*세로좌표=niska_podaci;if(x_koordinata<세로좌표){for(size_t 순번=0;순번<stavka_COUNT;순번++)x_koordinata[순번]=세로좌표[순번];}else while(stavka_COUNT){stavka_COUNT--;x_koordinata[stavka_COUNT]=세로좌표[stavka_COUNT];}return odredište_podaci;}
static unsigned char dodela_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct blok_podataka {size_t promeniti_veličinu;struct blok_podataka*Dalje_stavka;int 남은공간;int 채울크기;uint64_t poravnanje_lekcija;} blok_podataka;
static blok_podataka *첫항목;
void free(void*podaci_pozicija){if(!podaci_pozicija)return;blok_podataka*SECOND_VALUE=(blok_podataka*)podaci_pozicija-1;SECOND_VALUE->남은공간=1;for(blok_podataka*Dalje_Pomak=첫항목;Dalje_Pomak&&Dalje_Pomak->Dalje_stavka;){if(Dalje_Pomak->남은공간&&Dalje_Pomak->Dalje_stavka->남은공간){Dalje_Pomak->promeniti_veličinu+=sizeof(blok_podataka)+Dalje_Pomak->Dalje_stavka->promeniti_veličinu;Dalje_Pomak->Dalje_stavka=Dalje_Pomak->Dalje_stavka->Dalje_stavka;}else Dalje_Pomak=Dalje_Pomak->Dalje_stavka;}}
void *realloc(void*podaci_pozicija,size_t stavka_COUNT){
    if(!stavka_COUNT){free(podaci_pozicija);return 0;}if(stavka_COUNT>sizeof(dodela_Arena)-sizeof(blok_podataka))return 0;stavka_COUNT=(stavka_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(blok_podataka*)dodela_Arena;첫항목->promeniti_veličinu=sizeof(dodela_Arena)-sizeof(blok_podataka);첫항목->남은공간=1;첫항목->Dalje_stavka=0;}
    blok_podataka*이전=podaci_pozicija?(blok_podataka*)podaci_pozicija-1:0;if(이전&&이전->promeniti_veličinu>=stavka_COUNT)return podaci_pozicija;
    for(blok_podataka*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Dalje_stavka)if(SECOND_VALUE->남은공간&&SECOND_VALUE->promeniti_veličinu>=stavka_COUNT){
        if(SECOND_VALUE->promeniti_veličinu>=stavka_COUNT+sizeof(blok_podataka)+16){blok_podataka*나머지부분=(blok_podataka*)((unsigned char*)(SECOND_VALUE+1)+stavka_COUNT);나머지부분->promeniti_veličinu=SECOND_VALUE->promeniti_veličinu-stavka_COUNT-sizeof(blok_podataka);나머지부분->Dalje_stavka=SECOND_VALUE->Dalje_stavka;나머지부분->남은공간=1;SECOND_VALUE->Dalje_stavka=나머지부분;SECOND_VALUE->promeniti_veličinu=stavka_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,podaci_pozicija,이전->promeniti_veličinu);free(podaci_pozicija);}return 반환값;
    }greška=12;return 0;
}
void *malloc(size_t stavka_COUNT){return realloc(0,stavka_COUNT);}
void *calloc(size_t stavka_COUNT,size_t niska_podaci){if(niska_podaci&&stavka_COUNT>SIZE_MAX/niska_podaci)return 0;void*podaci_pozicija=malloc(stavka_COUNT*niska_podaci);if(podaci_pozicija)memset(podaci_pozicija,0,stavka_COUNT*niska_podaci);return podaci_pozicija;}
unsigned long long strtoull(const char*niska_podaci,char**završiti_razgovor_Pomak,int poster_VALUE){
    const char*START_Pomak=niska_podaci;while(*niska_podaci==' '||(*niska_podaci>=9&&*niska_podaci<=13))niska_podaci++;int 음수여부=0;if(*niska_podaci=='-'||*niska_podaci=='+')음수여부=*niska_podaci++=='-';
    if((!poster_VALUE||poster_VALUE==16)&&niska_podaci[0]=='0'&&(niska_podaci[1]=='x'||niska_podaci[1]=='X')){poster_VALUE=16;niska_podaci+=2;}if(!poster_VALUE)poster_VALUE=*niska_podaci=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kôd_znaka=*niska_podaci,odredište_podaci=kôd_znaka>='0'&&kôd_znaka<='9'?kôd_znaka-'0':kôd_znaka>='a'&&kôd_znaka<='z'?kôd_znaka-'a'+10:kôd_znaka>='A'&&kôd_znaka<='Z'?kôd_znaka-'A'+10:99;if(odredište_podaci>=(unsigned)poster_VALUE)break;하나라도=1;niska_podaci++;if(임시값>(~0ull-odredište_podaci)/(unsigned)poster_VALUE){임시값=~0ull;greška=34;}else 임시값=임시값*poster_VALUE+odredište_podaci;}
    if(završiti_razgovor_Pomak)*završiti_razgovor_Pomak=(char*)(하나라도?niska_podaci:START_Pomak);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*niska_podaci,char**보조항목,int SECOND_VALUE){return strtoull(niska_podaci,보조항목,SECOND_VALUE);}
long strtol(const char*niska_podaci,char**보조항목,int SECOND_VALUE){return (long)strtoull(niska_podaci,보조항목,SECOND_VALUE);}
int atoi(const char*niska_podaci){return (int)strtol(niska_podaci,0,10);}
long double ldexpl(long double x_koordinata,int stavka_COUNT){while(stavka_COUNT>0){x_koordinata*=2;stavka_COUNT--;}while(stavka_COUNT<0){x_koordinata/=2;stavka_COUNT++;}return x_koordinata;}
long double strtold(const char*niska_podaci,char**završiti_razgovor_Pomak){
    const char*START_Pomak=niska_podaci;while(*niska_podaci==' '||(*niska_podaci>=9&&*niska_podaci<=13))niska_podaci++;int 음수여부=0;if(*niska_podaci=='-'||*niska_podaci=='+')음수여부=*niska_podaci++=='-';
    int poster_VALUE=10;if(niska_podaci[0]=='0'&&(niska_podaci[1]=='x'||niska_podaci[1]=='X')){poster_VALUE=16;niska_podaci+=2;}long double 임시값=0,skalirati=1;int 소수부=0,하나라도=0;
    for(;;){int kôd_znaka=*niska_podaci,odredište_podaci=kôd_znaka>='0'&&kôd_znaka<='9'?kôd_znaka-'0':kôd_znaka>='a'&&kôd_znaka<='f'?kôd_znaka-'a'+10:kôd_znaka>='A'&&kôd_znaka<='F'?kôd_znaka-'A'+10:99;
        if(kôd_znaka=='.'&&!소수부){소수부=1;niska_podaci++;continue;}if(odredište_podaci>=poster_VALUE)break;하나라도=1;niska_podaci++;임시값=임시값*poster_VALUE+odredište_podaci;if(소수부)skalirati*=poster_VALUE;
    }임시값/=skalirati;
    if((poster_VALUE==10&&(*niska_podaci=='e'||*niska_podaci=='E'))||(poster_VALUE==16&&(*niska_podaci=='p'||*niska_podaci=='P'))){const char*emisija_VALUE=niska_podaci++;int 빼기=0;if(*niska_podaci=='-'||*niska_podaci=='+')빼기=*niska_podaci++=='-';int stavka_COUNT=0,stavka_COUNT_8f7753a1=0;while(*niska_podaci>='0'&&*niska_podaci<='9'){stavka_COUNT_8f7753a1++;if(stavka_COUNT<20000)stavka_COUNT=stavka_COUNT*10+*niska_podaci-'0';niska_podaci++;}if(!stavka_COUNT_8f7753a1)niska_podaci=emisija_VALUE;else{long double faktor=poster_VALUE==16?2:10;while(stavka_COUNT-->0&&stavka_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(završiti_razgovor_Pomak)*završiti_razgovor_Pomak=(char*)(하나라도?niska_podaci:START_Pomak);return 음수여부?-임시값:임시값;
}
double strtod(const char*niska_podaci,char**보조항목){return (double)strtold(niska_podaci,보조항목);}float strtof(const char*niska_podaci,char**보조항목){return (float)strtold(niska_podaci,보조항목);}
void qsort(void*poster_VALUE,size_t stavka_COUNT,size_t promeniti_veličinu,int(*Uporedi)(const void*,const void*)){
    unsigned char*podaci_pozicija=poster_VALUE;for(size_t 순번=1;순번<stavka_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Uporedi(podaci_pozicija+(안쪽순번-1)*promeniti_veličinu,podaci_pozicija+안쪽순번*promeniti_veličinu)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<promeniti_veličinu;셋째순번++){unsigned char kôd_znaka=podaci_pozicija[(안쪽순번-1)*promeniti_veličinu+셋째순번];podaci_pozicija[(안쪽순번-1)*promeniti_veličinu+셋째순번]=podaci_pozicija[안쪽순번*promeniti_veličinu+셋째순번];podaci_pozicija[안쪽순번*promeniti_veličinu+셋째순번]=kôd_znaka;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t pozicija;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *stavka_COUNT){*stavka_COUNT=출력크기;return 출력결과;}
int open(const char*ime,int konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini,...){
    if(!strcmp(ime,"/@cc-output")){if(출력열림){greška=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompajler_Izvori)/sizeof(kompajler_Izvori[0]);순번++)if(!strcmp(ime,kompajler_Izvori[순번].ime)){
        if(konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini&3){greška=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].pozicija=0;return 128+안쪽순번;}greška=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)ime,konfiguracija_Usluga_inteligentnog_prenosa_u_pozadini,0,0,0,0);if(반환값<0){greška=-반환값;return -1;}return 반환값;
}
int close(int Datoteka_pokazivač){if(Datoteka_pokazivač==100){출력열림=0;return 0;}if(Datoteka_pokazivač>=128&&Datoteka_pokazivač<152){열림[Datoteka_pokazivač-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Datoteka_pokazivač,0,0,0,0,0);if(반환값<0){greška=-반환값;return -1;}return 0;}
long read(int Datoteka_pokazivač,void*podaci,size_t stavka_COUNT){
    if(Datoteka_pokazivač>=128&&Datoteka_pokazivač<152&&열림[Datoteka_pokazivač-128].사용량){int 순번=Datoteka_pokazivač-128;const kompajler_resurs*반환값=&kompajler_Izvori[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->promeniti_veličinu-열림[순번].pozicija;if(stavka_COUNT>왼쪽)stavka_COUNT=왼쪽;memcpy(podaci,반환값->podaci+열림[순번].pozicija,stavka_COUNT);열림[순번].pozicija+=stavka_COUNT;return stavka_COUNT;}
    intptr_t 반환값=사용자호출(2,Datoteka_pokazivač,(uintptr_t)podaci,stavka_COUNT,0,0,0);if(반환값<0){greška=-반환값;return -1;}return 반환값;
}
long write(int Datoteka_pokazivač,const void*podaci,size_t stavka_COUNT){
    if(Datoteka_pokazivač==100){if(stavka_COUNT>sizeof(출력결과)-출력위치){greška=28;return -1;}memcpy(출력결과+출력위치,podaci,stavka_COUNT);출력위치+=stavka_COUNT;if(출력크기<출력위치)출력크기=출력위치;return stavka_COUNT;}
    intptr_t 반환값=사용자호출(1,Datoteka_pokazivač,(uintptr_t)podaci,stavka_COUNT,0,0,0);if(반환값<0){greška=-반환값;return -1;}return 반환값;
}
long lseek(int Datoteka_pokazivač,long Pomak_VALUE,int 기준점){
    if(Datoteka_pokazivač==100){long podaci_pozicija=Pomak_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(podaci_pozicija<0||(size_t)podaci_pozicija>sizeof(출력결과)){greška=22;return -1;}출력위치=podaci_pozicija;return podaci_pozicija;}
    if(Datoteka_pokazivač>=128&&Datoteka_pokazivač<152&&열림[Datoteka_pokazivač-128].사용량){int 순번=Datoteka_pokazivač-128;long podaci_pozicija=Pomak_VALUE+(기준점==0?0:기준점==1?열림[순번].pozicija:kompajler_Izvori[열림[순번].LOOKUP_INDEX].promeniti_veličinu);if(podaci_pozicija<0||(size_t)podaci_pozicija>kompajler_Izvori[열림[순번].LOOKUP_INDEX].promeniti_veličinu){greška=22;return -1;}열림[순번].pozicija=podaci_pozicija;return podaci_pozicija;}
    intptr_t 반환값=사용자호출(5,Datoteka_pokazivač,Pomak_VALUE,기준점,0,0,0);if(반환값<0){greška=-반환값;return -1;}return 반환값;
}
int unlink(const char*ime){intptr_t 반환값=사용자호출(11,(uintptr_t)ime,0,0,0,0,0);if(반환값<0){greška=-반환값;return -1;}return 반환값;}
char *realpath(const char*ime,char*KR_podaci){if(!KR_podaci){KR_podaci=malloc(strlen(ime)+1);if(!KR_podaci)return 0;}return strcpy(KR_podaci,ime);}
char *getcwd(char*podaci_pozicija,size_t stavka_COUNT){if(stavka_COUNT<2){greška=34;return 0;}podaci_pozicija[0]='/';podaci_pozicija[1]=0;return podaci_pozicija;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_stavka){time_t 임시값=0;if(Terminal_stavka)*Terminal_stavka=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_stavka){(void)Terminal_stavka;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Tokovi[18]={{1,0,1},{2,0,1}};FILE*stdout=&Tokovi[0],*stderr=&Tokovi[1];
FILE*fdopen(int Datoteka_pokazivač,const char*metod_MODE){(void)metod_MODE;for(unsigned 순번=2;순번<18;순번++)if(!Tokovi[순번].사용량){Tokovi[순번].사용량=1;Tokovi[순번].greška=0;Tokovi[순번].Datoteka_pokazivač=Datoteka_pokazivač;return &Tokovi[순번];}greška=24;return 0;}
int fflush(FILE*Datoteka_stavka){return Datoteka_stavka&&Datoteka_stavka->greška?-1:0;}
int fclose(FILE*Datoteka_stavka){int 반환값=close(Datoteka_stavka->Datoteka_pokazivač);if(Datoteka_stavka->greška)반환값=-1;Datoteka_stavka->사용량=0;return 반환값;}
size_t fwrite(const void*podaci_pozicija,size_t niska_podaci,size_t stavka_COUNT,FILE*Datoteka_stavka){if(!niska_podaci)return 0;if(stavka_COUNT>SIZE_MAX/niska_podaci){Datoteka_stavka->greška=1;return 0;}long 반환값=write(Datoteka_stavka->Datoteka_pokazivač,podaci_pozicija,niska_podaci*stavka_COUNT);if(반환값<0){Datoteka_stavka->greška=1;return 0;}return (size_t)반환값/niska_podaci;}
int fputc(int kôd_znaka,FILE*Datoteka_stavka){unsigned char SECOND_VALUE=kôd_znaka;return fwrite(&SECOND_VALUE,1,1,Datoteka_stavka)==1?SECOND_VALUE:EOF;}
int fputs(const char*niska_podaci,FILE*Datoteka_stavka){return fwrite(niska_podaci,1,strlen(niska_podaci),Datoteka_stavka)==strlen(niska_podaci)?0:EOF;}
static void 넣기(char*KR_podaci,size_t 용량한도,size_t*aktuelno_pozicija,char kôd_znaka){if(*aktuelno_pozicija+1<용량한도)KR_podaci[*aktuelno_pozicija]=kôd_znaka;(*aktuelno_pozicija)++;}
int vsnprintf(char*KR_podaci,size_t 용량한도,const char*format,va_list 가변인수){
    size_t aktuelno_pozicija=0;while(*format){if(*format!='%'){넣기(KR_podaci,용량한도,&aktuelno_pozicija,*format++);continue;}format++;
        int 왼쪽=0,nula_VALUE=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')nula_VALUE=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,preciznost_VALUE=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;preciznost_VALUE=0;if(*format=='*'){preciznost_VALUE=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')preciznost_VALUE=preciznost_VALUE*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char tip_oblast=*format?*format++:0,skladište_bafera[80];const char*niska_podaci=skladište_bafera;size_t stavka_COUNT=0;
        if(tip_oblast=='s'){niska_podaci=va_arg(가변인수,const char*);if(!niska_podaci)niska_podaci="(null)";stavka_COUNT=strlen(niska_podaci);if(preciznost_VALUE>=0&&stavka_COUNT>(size_t)preciznost_VALUE)stavka_COUNT=preciznost_VALUE;}
        else if(tip_oblast=='c'){skladište_bafera[0]=va_arg(가변인수,int);stavka_COUNT=1;}
        else if(tip_oblast=='%'){skladište_bafera[0]='%';stavka_COUNT=1;}
        else if(tip_oblast=='d'||tip_oblast=='i'||tip_oblast=='u'||tip_oblast=='x'||tip_oblast=='X'||tip_oblast=='o'||tip_oblast=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(tip_oblast=='d'||tip_oblast=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=tip_oblast=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned poster_VALUE=tip_oblast=='x'||tip_oblast=='X'||tip_oblast=='p'?16:tip_oblast=='o'?8:10;char cifra_COUNT[64];unsigned 사용량=0;
            do{cifra_COUNT[사용량++]="0123456789abcdef"[VALUE%poster_VALUE];VALUE/=poster_VALUE;}while(VALUE);
            if(음수표시)skladište_bafera[stavka_COUNT++]='-';if(tip_oblast=='p'||(대체값&&poster_VALUE==16)){skladište_bafera[stavka_COUNT++]='0';skladište_bafera[stavka_COUNT++]='x';}
            for(int popuna_VALUE=(int)사용량;preciznost_VALUE>popuna_VALUE&&stavka_COUNT<sizeof(skladište_bafera)-사용량;popuna_VALUE++)skladište_bafera[stavka_COUNT++]='0';
            if(nula_VALUE&&!왼쪽&&preciznost_VALUE<0)while(너비>(int)(stavka_COUNT+사용량)&&stavka_COUNT<sizeof(skladište_bafera)-사용량)skladište_bafera[stavka_COUNT++]='0';
            while(사용량)skladište_bafera[stavka_COUNT++]=cifra_COUNT[--사용량];
        }else{skladište_bafera[0]='?';stavka_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)stavka_COUNT){넣기(KR_podaci,용량한도,&aktuelno_pozicija,' ');너비--;}
        for(size_t 순번=0;순번<stavka_COUNT;순번++)넣기(KR_podaci,용량한도,&aktuelno_pozicija,niska_podaci[순번]);while(왼쪽&&너비>(int)stavka_COUNT){넣기(KR_podaci,용량한도,&aktuelno_pozicija,' ');너비--;}
    }if(용량한도)KR_podaci[aktuelno_pozicija<용량한도?aktuelno_pozicija:용량한도-1]=0;return aktuelno_pozicija;
}
int snprintf(char*KR_podaci,size_t 용량한도,const char*Datoteka_stavka,...){va_list 첫째값;va_start(첫째값,Datoteka_stavka);int 반환값=vsnprintf(KR_podaci,용량한도,Datoteka_stavka,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_podaci,const char*Datoteka_stavka,...){va_list 첫째값;va_start(첫째값,Datoteka_stavka);int 반환값=vsnprintf(KR_podaci,SIZE_MAX,Datoteka_stavka,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*tok_VALUE,const char*Datoteka_stavka,va_list 첫째값){char SECOND_VALUE[2048];int stavka_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Datoteka_stavka,첫째값);if(stavka_COUNT>2047)stavka_COUNT=2047;return fwrite(SECOND_VALUE,1,stavka_COUNT,tok_VALUE)==(size_t)stavka_COUNT?stavka_COUNT:-1;}
int fprintf(FILE*tok_VALUE,const char*Datoteka_stavka,...){va_list 첫째값;va_start(첫째값,Datoteka_stavka);int 반환값=vfprintf(tok_VALUE,Datoteka_stavka,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Datoteka_stavka,...){va_list 첫째값;va_start(첫째값,Datoteka_stavka);int 반환값=vfprintf(stdout,Datoteka_stavka,첫째값);va_end(첫째값);return 반환값;}
