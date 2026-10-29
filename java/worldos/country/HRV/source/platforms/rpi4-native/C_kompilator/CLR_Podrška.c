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
static int GREŠKA;
int *__errno_location(void){return &GREŠKA;}
void exit(int Stanje_VALUE){사용자호출(6,Stanje_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *검사식,const char *Datoteka,unsigned red,const char *postupak_unos_naziv){fprintf(stderr,"cc assertion: %s %s:%u %s\n",검사식,Datoteka,red,postupak_unos_naziv);exit(1);}
size_t strlen(const char*niz_podaci){const char*podaci_položaj=niz_podaci;while(*podaci_položaj)podaci_položaj++;return podaci_položaj-niz_podaci;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t artikl_COUNT){while(artikl_COUNT--){unsigned char koordinata_x=*첫째값++,세로좌표=*SECOND_VALUE++;if(koordinata_x!=세로좌표)return koordinata_x-세로좌표;if(!koordinata_x)return 0;}return 0;}
char *strcpy(char*odredište_podaci,const char*niz_podaci){char*반환값=odredište_podaci;while((*odredište_podaci++=*niz_podaci++)){}return 반환값;}
char *strchr(const char*niz_podaci,int kodna_točka){do{if(*niz_podaci==(char)kodna_točka)return (char*)niz_podaci;}while(*niz_podaci++);return 0;}
char *strrchr(const char*niz_podaci,int kodna_točka){const char*반환값=0;do{if(*niz_podaci==(char)kodna_točka)반환값=niz_podaci;}while(*niz_podaci++);return (char*)반환값;}
char *strstr(const char*niz_podaci,const char*Terminal_unos){size_t artikl_COUNT=strlen(Terminal_unos);for(;*niz_podaci;niz_podaci++)if(!strncmp(niz_podaci,Terminal_unos,artikl_COUNT))return (char*)niz_podaci;return artikl_COUNT?0:(char*)niz_podaci;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t artikl_COUNT){const unsigned char*koordinata_x=첫째값,*세로좌표=SECOND_VALUE;while(artikl_COUNT--){if(*koordinata_x!=*세로좌표)return *koordinata_x-*세로좌표;koordinata_x++;세로좌표++;}return 0;}
void *memmove(void*odredište_podaci,const void*niz_podaci,size_t artikl_COUNT){unsigned char*koordinata_x=odredište_podaci;const unsigned char*세로좌표=niz_podaci;if(koordinata_x<세로좌표){for(size_t 순번=0;순번<artikl_COUNT;순번++)koordinata_x[순번]=세로좌표[순번];}else while(artikl_COUNT){artikl_COUNT--;koordinata_x[artikl_COUNT]=세로좌표[artikl_COUNT];}return odredište_podaci;}
static unsigned char dodjela_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct podatkovni_blok {size_t Veličina;struct podatkovni_blok*Dalje_artikl;int 남은공간;int ispuna;uint64_t poravnanje_lekcija;} podatkovni_blok;
static podatkovni_blok *첫항목;
void free(void*podaci_položaj){if(!podaci_položaj)return;podatkovni_blok*SECOND_VALUE=(podatkovni_blok*)podaci_položaj-1;SECOND_VALUE->남은공간=1;for(podatkovni_blok*Dalje_pomak=첫항목;Dalje_pomak&&Dalje_pomak->Dalje_artikl;){if(Dalje_pomak->남은공간&&Dalje_pomak->Dalje_artikl->남은공간){Dalje_pomak->Veličina+=sizeof(podatkovni_blok)+Dalje_pomak->Dalje_artikl->Veličina;Dalje_pomak->Dalje_artikl=Dalje_pomak->Dalje_artikl->Dalje_artikl;}else Dalje_pomak=Dalje_pomak->Dalje_artikl;}}
void *realloc(void*podaci_položaj,size_t artikl_COUNT){
    if(!artikl_COUNT){free(podaci_položaj);return 0;}if(artikl_COUNT>sizeof(dodjela_Arena)-sizeof(podatkovni_blok))return 0;artikl_COUNT=(artikl_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(podatkovni_blok*)dodjela_Arena;첫항목->Veličina=sizeof(dodjela_Arena)-sizeof(podatkovni_blok);첫항목->남은공간=1;첫항목->Dalje_artikl=0;}
    podatkovni_blok*이전=podaci_položaj?(podatkovni_blok*)podaci_položaj-1:0;if(이전&&이전->Veličina>=artikl_COUNT)return podaci_položaj;
    for(podatkovni_blok*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Dalje_artikl)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Veličina>=artikl_COUNT){
        if(SECOND_VALUE->Veličina>=artikl_COUNT+sizeof(podatkovni_blok)+16){podatkovni_blok*나머지부분=(podatkovni_blok*)((unsigned char*)(SECOND_VALUE+1)+artikl_COUNT);나머지부분->Veličina=SECOND_VALUE->Veličina-artikl_COUNT-sizeof(podatkovni_blok);나머지부분->Dalje_artikl=SECOND_VALUE->Dalje_artikl;나머지부분->남은공간=1;SECOND_VALUE->Dalje_artikl=나머지부분;SECOND_VALUE->Veličina=artikl_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,podaci_položaj,이전->Veličina);free(podaci_položaj);}return 반환값;
    }GREŠKA=12;return 0;
}
void *malloc(size_t artikl_COUNT){return realloc(0,artikl_COUNT);}
void *calloc(size_t artikl_COUNT,size_t niz_podaci){if(niz_podaci&&artikl_COUNT>SIZE_MAX/niz_podaci)return 0;void*podaci_položaj=malloc(artikl_COUNT*niz_podaci);if(podaci_položaj)memset(podaci_položaj,0,artikl_COUNT*niz_podaci);return podaci_položaj;}
unsigned long long strtoull(const char*niz_podaci,char**završiti_razgovor_pomak,int podloga_VALUE){
    const char*START_pomak=niz_podaci;while(*niz_podaci==' '||(*niz_podaci>=9&&*niz_podaci<=13))niz_podaci++;int 음수여부=0;if(*niz_podaci=='-'||*niz_podaci=='+')음수여부=*niz_podaci++=='-';
    if((!podloga_VALUE||podloga_VALUE==16)&&niz_podaci[0]=='0'&&(niz_podaci[1]=='x'||niz_podaci[1]=='X')){podloga_VALUE=16;niz_podaci+=2;}if(!podloga_VALUE)podloga_VALUE=*niz_podaci=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kodna_točka=*niz_podaci,odredište_podaci=kodna_točka>='0'&&kodna_točka<='9'?kodna_točka-'0':kodna_točka>='a'&&kodna_točka<='z'?kodna_točka-'a'+10:kodna_točka>='A'&&kodna_točka<='Z'?kodna_točka-'A'+10:99;if(odredište_podaci>=(unsigned)podloga_VALUE)break;하나라도=1;niz_podaci++;if(임시값>(~0ull-odredište_podaci)/(unsigned)podloga_VALUE){임시값=~0ull;GREŠKA=34;}else 임시값=임시값*podloga_VALUE+odredište_podaci;}
    if(završiti_razgovor_pomak)*završiti_razgovor_pomak=(char*)(하나라도?niz_podaci:START_pomak);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*niz_podaci,char**보조항목,int SECOND_VALUE){return strtoull(niz_podaci,보조항목,SECOND_VALUE);}
long strtol(const char*niz_podaci,char**보조항목,int SECOND_VALUE){return (long)strtoull(niz_podaci,보조항목,SECOND_VALUE);}
int atoi(const char*niz_podaci){return (int)strtol(niz_podaci,0,10);}
long double ldexpl(long double koordinata_x,int artikl_COUNT){while(artikl_COUNT>0){koordinata_x*=2;artikl_COUNT--;}while(artikl_COUNT<0){koordinata_x/=2;artikl_COUNT++;}return koordinata_x;}
long double strtold(const char*niz_podaci,char**završiti_razgovor_pomak){
    const char*START_pomak=niz_podaci;while(*niz_podaci==' '||(*niz_podaci>=9&&*niz_podaci<=13))niz_podaci++;int 음수여부=0;if(*niz_podaci=='-'||*niz_podaci=='+')음수여부=*niz_podaci++=='-';
    int podloga_VALUE=10;if(niz_podaci[0]=='0'&&(niz_podaci[1]=='x'||niz_podaci[1]=='X')){podloga_VALUE=16;niz_podaci+=2;}long double 임시값=0,skalirati=1;int 소수부=0,하나라도=0;
    for(;;){int kodna_točka=*niz_podaci,odredište_podaci=kodna_točka>='0'&&kodna_točka<='9'?kodna_točka-'0':kodna_točka>='a'&&kodna_točka<='f'?kodna_točka-'a'+10:kodna_točka>='A'&&kodna_točka<='F'?kodna_točka-'A'+10:99;
        if(kodna_točka=='.'&&!소수부){소수부=1;niz_podaci++;continue;}if(odredište_podaci>=podloga_VALUE)break;하나라도=1;niz_podaci++;임시값=임시값*podloga_VALUE+odredište_podaci;if(소수부)skalirati*=podloga_VALUE;
    }임시값/=skalirati;
    if((podloga_VALUE==10&&(*niz_podaci=='e'||*niz_podaci=='E'))||(podloga_VALUE==16&&(*niz_podaci=='p'||*niz_podaci=='P'))){const char*emisija_VALUE=niz_podaci++;int 빼기=0;if(*niz_podaci=='-'||*niz_podaci=='+')빼기=*niz_podaci++=='-';int artikl_COUNT=0,unos_COUNT=0;while(*niz_podaci>='0'&&*niz_podaci<='9'){unos_COUNT++;if(artikl_COUNT<20000)artikl_COUNT=artikl_COUNT*10+*niz_podaci-'0';niz_podaci++;}if(!unos_COUNT)niz_podaci=emisija_VALUE;else{long double faktor=podloga_VALUE==16?2:10;while(artikl_COUNT-->0&&artikl_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(završiti_razgovor_pomak)*završiti_razgovor_pomak=(char*)(하나라도?niz_podaci:START_pomak);return 음수여부?-임시값:임시값;
}
double strtod(const char*niz_podaci,char**보조항목){return (double)strtold(niz_podaci,보조항목);}float strtof(const char*niz_podaci,char**보조항목){return (float)strtold(niz_podaci,보조항목);}
void qsort(void*podloga_VALUE,size_t artikl_COUNT,size_t Veličina,int(*Usporedba)(const void*,const void*)){
    unsigned char*podaci_položaj=podloga_VALUE;for(size_t 순번=1;순번<artikl_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Usporedba(podaci_položaj+(안쪽순번-1)*Veličina,podaci_položaj+안쪽순번*Veličina)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Veličina;셋째순번++){unsigned char kodna_točka=podaci_položaj[(안쪽순번-1)*Veličina+셋째순번];podaci_položaj[(안쪽순번-1)*Veličina+셋째순번]=podaci_položaj[안쪽순번*Veličina+셋째순번];podaci_položaj[안쪽순번*Veličina+셋째순번]=kodna_točka;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Položaj;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *artikl_COUNT){*artikl_COUNT=출력크기;return 출력결과;}
int open(const char*Ime,int konfiguracija_Pozadinski_pametni_servis_za_transfer,...){
    if(!strcmp(Ime,"/@cc-output")){if(출력열림){GREŠKA=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompilator_Resursi)/sizeof(kompilator_Resursi[0]);순번++)if(!strcmp(Ime,kompilator_Resursi[순번].Ime)){
        if(konfiguracija_Pozadinski_pametni_servis_za_transfer&3){GREŠKA=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Položaj=0;return 128+안쪽순번;}GREŠKA=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Ime,konfiguracija_Pozadinski_pametni_servis_za_transfer,0,0,0,0);if(반환값<0){GREŠKA=-반환값;return -1;}return 반환값;
}
int close(int Datoteka_ustroj){if(Datoteka_ustroj==100){출력열림=0;return 0;}if(Datoteka_ustroj>=128&&Datoteka_ustroj<152){열림[Datoteka_ustroj-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Datoteka_ustroj,0,0,0,0,0);if(반환값<0){GREŠKA=-반환값;return -1;}return 0;}
long read(int Datoteka_ustroj,void*podaci,size_t artikl_COUNT){
    if(Datoteka_ustroj>=128&&Datoteka_ustroj<152&&열림[Datoteka_ustroj-128].사용량){int 순번=Datoteka_ustroj-128;const kompilator_resurs*반환값=&kompilator_Resursi[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Veličina-열림[순번].Položaj;if(artikl_COUNT>왼쪽)artikl_COUNT=왼쪽;memcpy(podaci,반환값->podaci+열림[순번].Položaj,artikl_COUNT);열림[순번].Položaj+=artikl_COUNT;return artikl_COUNT;}
    intptr_t 반환값=사용자호출(2,Datoteka_ustroj,(uintptr_t)podaci,artikl_COUNT,0,0,0);if(반환값<0){GREŠKA=-반환값;return -1;}return 반환값;
}
long write(int Datoteka_ustroj,const void*podaci,size_t artikl_COUNT){
    if(Datoteka_ustroj==100){if(artikl_COUNT>sizeof(출력결과)-출력위치){GREŠKA=28;return -1;}memcpy(출력결과+출력위치,podaci,artikl_COUNT);출력위치+=artikl_COUNT;if(출력크기<출력위치)출력크기=출력위치;return artikl_COUNT;}
    intptr_t 반환값=사용자호출(1,Datoteka_ustroj,(uintptr_t)podaci,artikl_COUNT,0,0,0);if(반환값<0){GREŠKA=-반환값;return -1;}return 반환값;
}
long lseek(int Datoteka_ustroj,long pomak_VALUE,int 기준점){
    if(Datoteka_ustroj==100){long podaci_položaj=pomak_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(podaci_položaj<0||(size_t)podaci_položaj>sizeof(출력결과)){GREŠKA=22;return -1;}출력위치=podaci_položaj;return podaci_položaj;}
    if(Datoteka_ustroj>=128&&Datoteka_ustroj<152&&열림[Datoteka_ustroj-128].사용량){int 순번=Datoteka_ustroj-128;long podaci_položaj=pomak_VALUE+(기준점==0?0:기준점==1?열림[순번].Položaj:kompilator_Resursi[열림[순번].LOOKUP_INDEX].Veličina);if(podaci_položaj<0||(size_t)podaci_položaj>kompilator_Resursi[열림[순번].LOOKUP_INDEX].Veličina){GREŠKA=22;return -1;}열림[순번].Položaj=podaci_položaj;return podaci_položaj;}
    intptr_t 반환값=사용자호출(5,Datoteka_ustroj,pomak_VALUE,기준점,0,0,0);if(반환값<0){GREŠKA=-반환값;return -1;}return 반환값;
}
int unlink(const char*Ime){intptr_t 반환값=사용자호출(11,(uintptr_t)Ime,0,0,0,0,0);if(반환값<0){GREŠKA=-반환값;return -1;}return 반환값;}
char *realpath(const char*Ime,char*KR_podaci){if(!KR_podaci){KR_podaci=malloc(strlen(Ime)+1);if(!KR_podaci)return 0;}return strcpy(KR_podaci,Ime);}
char *getcwd(char*podaci_položaj,size_t artikl_COUNT){if(artikl_COUNT<2){GREŠKA=34;return 0;}podaci_položaj[0]='/';podaci_položaj[1]=0;return podaci_položaj;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_unos){time_t 임시값=0;if(Terminal_unos)*Terminal_unos=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_unos){(void)Terminal_unos;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Tokovi[18]={{1,0,1},{2,0,1}};FILE*stdout=&Tokovi[0],*stderr=&Tokovi[1];
FILE*fdopen(int Datoteka_ustroj,const char*postupak_MODE){(void)postupak_MODE;for(unsigned 순번=2;순번<18;순번++)if(!Tokovi[순번].사용량){Tokovi[순번].사용량=1;Tokovi[순번].GREŠKA=0;Tokovi[순번].Datoteka_ustroj=Datoteka_ustroj;return &Tokovi[순번];}GREŠKA=24;return 0;}
int fflush(FILE*Datoteka_unos){return Datoteka_unos&&Datoteka_unos->GREŠKA?-1:0;}
int fclose(FILE*Datoteka_unos){int 반환값=close(Datoteka_unos->Datoteka_ustroj);if(Datoteka_unos->GREŠKA)반환값=-1;Datoteka_unos->사용량=0;return 반환값;}
size_t fwrite(const void*podaci_položaj,size_t niz_podaci,size_t artikl_COUNT,FILE*Datoteka_unos){if(!niz_podaci)return 0;if(artikl_COUNT>SIZE_MAX/niz_podaci){Datoteka_unos->GREŠKA=1;return 0;}long 반환값=write(Datoteka_unos->Datoteka_ustroj,podaci_položaj,niz_podaci*artikl_COUNT);if(반환값<0){Datoteka_unos->GREŠKA=1;return 0;}return (size_t)반환값/niz_podaci;}
int fputc(int kodna_točka,FILE*Datoteka_unos){unsigned char SECOND_VALUE=kodna_točka;return fwrite(&SECOND_VALUE,1,1,Datoteka_unos)==1?SECOND_VALUE:EOF;}
int fputs(const char*niz_podaci,FILE*Datoteka_unos){return fwrite(niz_podaci,1,strlen(niz_podaci),Datoteka_unos)==strlen(niz_podaci)?0:EOF;}
static void 넣기(char*KR_podaci,size_t 용량한도,size_t*redovno_položaj,char kodna_točka){if(*redovno_položaj+1<용량한도)KR_podaci[*redovno_položaj]=kodna_točka;(*redovno_položaj)++;}
int vsnprintf(char*KR_podaci,size_t 용량한도,const char*oblik,va_list 가변인수){
    size_t redovno_položaj=0;while(*oblik){if(*oblik!='%'){넣기(KR_podaci,용량한도,&redovno_položaj,*oblik++);continue;}oblik++;
        int 왼쪽=0,nula_VALUE=0,대체값=0;while(*oblik=='-'||*oblik=='0'||*oblik=='#'||*oblik=='+'||*oblik==' '){if(*oblik=='-')왼쪽=1;if(*oblik=='0')nula_VALUE=1;if(*oblik=='#')대체값=1;oblik++;}
        int 너비=0,preciznost_VALUE=-1;if(*oblik=='*'){너비=va_arg(가변인수,int);oblik++;}else while(*oblik>='0'&&*oblik<='9')너비=너비*10+*oblik++-'0';
        if(*oblik=='.'){oblik++;preciznost_VALUE=0;if(*oblik=='*'){preciznost_VALUE=va_arg(가변인수,int);oblik++;}else while(*oblik>='0'&&*oblik<='9')preciznost_VALUE=preciznost_VALUE*10+*oblik++-'0';}
        int široki_znak=0;while(*oblik=='l'||*oblik=='z'||*oblik=='t'||*oblik=='j'||*oblik=='h'){if(*oblik!='h')široki_znak=1;oblik++;}
        char TYPE_područje=*oblik?*oblik++:0,memorija_međuspremnika[80];const char*niz_podaci=memorija_međuspremnika;size_t artikl_COUNT=0;
        if(TYPE_područje=='s'){niz_podaci=va_arg(가변인수,const char*);if(!niz_podaci)niz_podaci="(null)";artikl_COUNT=strlen(niz_podaci);if(preciznost_VALUE>=0&&artikl_COUNT>(size_t)preciznost_VALUE)artikl_COUNT=preciznost_VALUE;}
        else if(TYPE_područje=='c'){memorija_međuspremnika[0]=va_arg(가변인수,int);artikl_COUNT=1;}
        else if(TYPE_područje=='%'){memorija_međuspremnika[0]='%';artikl_COUNT=1;}
        else if(TYPE_područje=='d'||TYPE_područje=='i'||TYPE_područje=='u'||TYPE_područje=='x'||TYPE_područje=='X'||TYPE_područje=='o'||TYPE_područje=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_područje=='d'||TYPE_područje=='i'){long long 임시값=široki_znak?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_područje=='p'?(uintptr_t)va_arg(가변인수,void*):široki_znak?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned podloga_VALUE=TYPE_područje=='x'||TYPE_područje=='X'||TYPE_područje=='p'?16:TYPE_područje=='o'?8:10;char znamenka_COUNT[64];unsigned 사용량=0;
            do{znamenka_COUNT[사용량++]="0123456789abcdef"[VALUE%podloga_VALUE];VALUE/=podloga_VALUE;}while(VALUE);
            if(음수표시)memorija_međuspremnika[artikl_COUNT++]='-';if(TYPE_područje=='p'||(대체값&&podloga_VALUE==16)){memorija_međuspremnika[artikl_COUNT++]='0';memorija_međuspremnika[artikl_COUNT++]='x';}
            for(int ispuna_VALUE=(int)사용량;preciznost_VALUE>ispuna_VALUE&&artikl_COUNT<sizeof(memorija_međuspremnika)-사용량;ispuna_VALUE++)memorija_međuspremnika[artikl_COUNT++]='0';
            if(nula_VALUE&&!왼쪽&&preciznost_VALUE<0)while(너비>(int)(artikl_COUNT+사용량)&&artikl_COUNT<sizeof(memorija_međuspremnika)-사용량)memorija_međuspremnika[artikl_COUNT++]='0';
            while(사용량)memorija_međuspremnika[artikl_COUNT++]=znamenka_COUNT[--사용량];
        }else{memorija_međuspremnika[0]='?';artikl_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)artikl_COUNT){넣기(KR_podaci,용량한도,&redovno_položaj,' ');너비--;}
        for(size_t 순번=0;순번<artikl_COUNT;순번++)넣기(KR_podaci,용량한도,&redovno_položaj,niz_podaci[순번]);while(왼쪽&&너비>(int)artikl_COUNT){넣기(KR_podaci,용량한도,&redovno_položaj,' ');너비--;}
    }if(용량한도)KR_podaci[redovno_položaj<용량한도?redovno_položaj:용량한도-1]=0;return redovno_položaj;
}
int snprintf(char*KR_podaci,size_t 용량한도,const char*Datoteka_unos,...){va_list 첫째값;va_start(첫째값,Datoteka_unos);int 반환값=vsnprintf(KR_podaci,용량한도,Datoteka_unos,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_podaci,const char*Datoteka_unos,...){va_list 첫째값;va_start(첫째값,Datoteka_unos);int 반환값=vsnprintf(KR_podaci,SIZE_MAX,Datoteka_unos,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*tok_VALUE,const char*Datoteka_unos,va_list 첫째값){char SECOND_VALUE[2048];int artikl_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Datoteka_unos,첫째값);if(artikl_COUNT>2047)artikl_COUNT=2047;return fwrite(SECOND_VALUE,1,artikl_COUNT,tok_VALUE)==(size_t)artikl_COUNT?artikl_COUNT:-1;}
int fprintf(FILE*tok_VALUE,const char*Datoteka_unos,...){va_list 첫째값;va_start(첫째값,Datoteka_unos);int 반환값=vfprintf(tok_VALUE,Datoteka_unos,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Datoteka_unos,...){va_list 첫째값;va_start(첫째값,Datoteka_unos);int 반환값=vfprintf(stdout,Datoteka_unos,첫째값);va_end(첫째값);return 반환값;}
