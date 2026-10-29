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
static int GRESKA;
int *__errno_location(void){return &GRESKA;}
void exit(int stanje_VALUE){사용자호출(6,stanje_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *ček_izraz,const char *Fajl,unsigned Linija,const char *metoda_unos_naziv){fprintf(stderr,"cc assertion: %s %s:%u %s\n",ček_izraz,Fajl,Linija,metoda_unos_naziv);exit(1);}
size_t strlen(const char*string_podaci){const char*podaci_položaj=string_podaci;while(*podaci_položaj)podaci_položaj++;return podaci_položaj-string_podaci;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t stavka_COUNT){while(stavka_COUNT--){unsigned char koordinata_x=*첫째값++,Y_koordinata=*SECOND_VALUE++;if(koordinata_x!=Y_koordinata)return koordinata_x-Y_koordinata;if(!koordinata_x)return 0;}return 0;}
char *strcpy(char*odredište_podaci,const char*string_podaci){char*반환값=odredište_podaci;while((*odredište_podaci++=*string_podaci++)){}return 반환값;}
char *strchr(const char*string_podaci,int kôd_znaka){do{if(*string_podaci==(char)kôd_znaka)return (char*)string_podaci;}while(*string_podaci++);return 0;}
char *strrchr(const char*string_podaci,int kôd_znaka){const char*반환값=0;do{if(*string_podaci==(char)kôd_znaka)반환값=string_podaci;}while(*string_podaci++);return (char*)반환값;}
char *strstr(const char*string_podaci,const char*Terminal_unos){size_t stavka_COUNT=strlen(Terminal_unos);for(;*string_podaci;string_podaci++)if(!strncmp(string_podaci,Terminal_unos,stavka_COUNT))return (char*)string_podaci;return stavka_COUNT?0:(char*)string_podaci;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t stavka_COUNT){const unsigned char*koordinata_x=첫째값,*Y_koordinata=SECOND_VALUE;while(stavka_COUNT--){if(*koordinata_x!=*Y_koordinata)return *koordinata_x-*Y_koordinata;koordinata_x++;Y_koordinata++;}return 0;}
void *memmove(void*odredište_podaci,const void*string_podaci,size_t stavka_COUNT){unsigned char*koordinata_x=odredište_podaci;const unsigned char*Y_koordinata=string_podaci;if(koordinata_x<Y_koordinata){for(size_t 순번=0;순번<stavka_COUNT;순번++)koordinata_x[순번]=Y_koordinata[순번];}else while(stavka_COUNT){stavka_COUNT--;koordinata_x[stavka_COUNT]=Y_koordinata[stavka_COUNT];}return odredište_podaci;}
static unsigned char dodjela_pohrane_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct podaci_blokirati {size_t Veličina;struct podaci_blokirati*Dalje_stavka;int 남은공간;int 채울크기;uint64_t poravnanje_lekcija;} podaci_blokirati;
static podaci_blokirati *첫항목;
void free(void*podaci_položaj){if(!podaci_položaj)return;podaci_blokirati*SECOND_VALUE=(podaci_blokirati*)podaci_položaj-1;SECOND_VALUE->남은공간=1;for(podaci_blokirati*Dalje_Pomak=첫항목;Dalje_Pomak&&Dalje_Pomak->Dalje_stavka;){if(Dalje_Pomak->남은공간&&Dalje_Pomak->Dalje_stavka->남은공간){Dalje_Pomak->Veličina+=sizeof(podaci_blokirati)+Dalje_Pomak->Dalje_stavka->Veličina;Dalje_Pomak->Dalje_stavka=Dalje_Pomak->Dalje_stavka->Dalje_stavka;}else Dalje_Pomak=Dalje_Pomak->Dalje_stavka;}}
void *realloc(void*podaci_položaj,size_t stavka_COUNT){
    if(!stavka_COUNT){free(podaci_položaj);return 0;}if(stavka_COUNT>sizeof(dodjela_pohrane_Arena)-sizeof(podaci_blokirati))return 0;stavka_COUNT=(stavka_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(podaci_blokirati*)dodjela_pohrane_Arena;첫항목->Veličina=sizeof(dodjela_pohrane_Arena)-sizeof(podaci_blokirati);첫항목->남은공간=1;첫항목->Dalje_stavka=0;}
    podaci_blokirati*이전=podaci_položaj?(podaci_blokirati*)podaci_položaj-1:0;if(이전&&이전->Veličina>=stavka_COUNT)return podaci_položaj;
    for(podaci_blokirati*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Dalje_stavka)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Veličina>=stavka_COUNT){
        if(SECOND_VALUE->Veličina>=stavka_COUNT+sizeof(podaci_blokirati)+16){podaci_blokirati*나머지부분=(podaci_blokirati*)((unsigned char*)(SECOND_VALUE+1)+stavka_COUNT);나머지부분->Veličina=SECOND_VALUE->Veličina-stavka_COUNT-sizeof(podaci_blokirati);나머지부분->Dalje_stavka=SECOND_VALUE->Dalje_stavka;나머지부분->남은공간=1;SECOND_VALUE->Dalje_stavka=나머지부분;SECOND_VALUE->Veličina=stavka_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,podaci_položaj,이전->Veličina);free(podaci_položaj);}return 반환값;
    }GRESKA=12;return 0;
}
void *malloc(size_t stavka_COUNT){return realloc(0,stavka_COUNT);}
void *calloc(size_t stavka_COUNT,size_t string_podaci){if(string_podaci&&stavka_COUNT>SIZE_MAX/string_podaci)return 0;void*podaci_položaj=malloc(stavka_COUNT*string_podaci);if(podaci_položaj)memset(podaci_položaj,0,stavka_COUNT*string_podaci);return podaci_položaj;}
unsigned long long strtoull(const char*string_podaci,char**završiti_Pomak,int poster_VALUE){
    const char*START_Pomak=string_podaci;while(*string_podaci==' '||(*string_podaci>=9&&*string_podaci<=13))string_podaci++;int 음수여부=0;if(*string_podaci=='-'||*string_podaci=='+')음수여부=*string_podaci++=='-';
    if((!poster_VALUE||poster_VALUE==16)&&string_podaci[0]=='0'&&(string_podaci[1]=='x'||string_podaci[1]=='X')){poster_VALUE=16;string_podaci+=2;}if(!poster_VALUE)poster_VALUE=*string_podaci=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kôd_znaka=*string_podaci,odredište_podaci=kôd_znaka>='0'&&kôd_znaka<='9'?kôd_znaka-'0':kôd_znaka>='a'&&kôd_znaka<='z'?kôd_znaka-'a'+10:kôd_znaka>='A'&&kôd_znaka<='Z'?kôd_znaka-'A'+10:99;if(odredište_podaci>=(unsigned)poster_VALUE)break;하나라도=1;string_podaci++;if(임시값>(~0ull-odredište_podaci)/(unsigned)poster_VALUE){임시값=~0ull;GRESKA=34;}else 임시값=임시값*poster_VALUE+odredište_podaci;}
    if(završiti_Pomak)*završiti_Pomak=(char*)(하나라도?string_podaci:START_Pomak);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*string_podaci,char**보조항목,int SECOND_VALUE){return strtoull(string_podaci,보조항목,SECOND_VALUE);}
long strtol(const char*string_podaci,char**보조항목,int SECOND_VALUE){return (long)strtoull(string_podaci,보조항목,SECOND_VALUE);}
int atoi(const char*string_podaci){return (int)strtol(string_podaci,0,10);}
long double ldexpl(long double koordinata_x,int stavka_COUNT){while(stavka_COUNT>0){koordinata_x*=2;stavka_COUNT--;}while(stavka_COUNT<0){koordinata_x/=2;stavka_COUNT++;}return koordinata_x;}
long double strtold(const char*string_podaci,char**završiti_Pomak){
    const char*START_Pomak=string_podaci;while(*string_podaci==' '||(*string_podaci>=9&&*string_podaci<=13))string_podaci++;int 음수여부=0;if(*string_podaci=='-'||*string_podaci=='+')음수여부=*string_podaci++=='-';
    int poster_VALUE=10;if(string_podaci[0]=='0'&&(string_podaci[1]=='x'||string_podaci[1]=='X')){poster_VALUE=16;string_podaci+=2;}long double 임시값=0,skala=1;int 소수부=0,하나라도=0;
    for(;;){int kôd_znaka=*string_podaci,odredište_podaci=kôd_znaka>='0'&&kôd_znaka<='9'?kôd_znaka-'0':kôd_znaka>='a'&&kôd_znaka<='f'?kôd_znaka-'a'+10:kôd_znaka>='A'&&kôd_znaka<='F'?kôd_znaka-'A'+10:99;
        if(kôd_znaka=='.'&&!소수부){소수부=1;string_podaci++;continue;}if(odredište_podaci>=poster_VALUE)break;하나라도=1;string_podaci++;임시값=임시값*poster_VALUE+odredište_podaci;if(소수부)skala*=poster_VALUE;
    }임시값/=skala;
    if((poster_VALUE==10&&(*string_podaci=='e'||*string_podaci=='E'))||(poster_VALUE==16&&(*string_podaci=='p'||*string_podaci=='P'))){const char*program_VALUE=string_podaci++;int 빼기=0;if(*string_podaci=='-'||*string_podaci=='+')빼기=*string_podaci++=='-';int stavka_COUNT=0,unos_COUNT=0;while(*string_podaci>='0'&&*string_podaci<='9'){unos_COUNT++;if(stavka_COUNT<20000)stavka_COUNT=stavka_COUNT*10+*string_podaci-'0';string_podaci++;}if(!unos_COUNT)string_podaci=program_VALUE;else{long double faktor=poster_VALUE==16?2:10;while(stavka_COUNT-->0&&stavka_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(završiti_Pomak)*završiti_Pomak=(char*)(하나라도?string_podaci:START_Pomak);return 음수여부?-임시값:임시값;
}
double strtod(const char*string_podaci,char**보조항목){return (double)strtold(string_podaci,보조항목);}float strtof(const char*string_podaci,char**보조항목){return (float)strtold(string_podaci,보조항목);}
void qsort(void*poster_VALUE,size_t stavka_COUNT,size_t Veličina,int(*Poređenje)(const void*,const void*)){
    unsigned char*podaci_položaj=poster_VALUE;for(size_t 순번=1;순번<stavka_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Poređenje(podaci_položaj+(안쪽순번-1)*Veličina,podaci_položaj+안쪽순번*Veličina)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Veličina;셋째순번++){unsigned char kôd_znaka=podaci_položaj[(안쪽순번-1)*Veličina+셋째순번];podaci_položaj[(안쪽순번-1)*Veličina+셋째순번]=podaci_položaj[안쪽순번*Veličina+셋째순번];podaci_položaj[안쪽순번*Veličina+셋째순번]=kôd_znaka;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Pozicija;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *stavka_COUNT){*stavka_COUNT=출력크기;return 출력결과;}
int open(const char*Naziv,int 설정비트,...){
    if(!strcmp(Naziv,"/@cc-output")){if(출력열림){GRESKA=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Naziv,번역기자원들[순번].Naziv)){
        if(설정비트&3){GRESKA=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Pozicija=0;return 128+안쪽순번;}GRESKA=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Naziv,설정비트,0,0,0,0);if(반환값<0){GRESKA=-반환값;return -1;}return 반환값;
}
int close(int fajl_hvatište){if(fajl_hvatište==100){출력열림=0;return 0;}if(fajl_hvatište>=128&&fajl_hvatište<152){열림[fajl_hvatište-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fajl_hvatište,0,0,0,0,0);if(반환값<0){GRESKA=-반환값;return -1;}return 0;}
long read(int fajl_hvatište,void*podaci,size_t stavka_COUNT){
    if(fajl_hvatište>=128&&fajl_hvatište<152&&열림[fajl_hvatište-128].사용량){int 순번=fajl_hvatište-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Veličina-열림[순번].Pozicija;if(stavka_COUNT>왼쪽)stavka_COUNT=왼쪽;memcpy(podaci,반환값->podaci+열림[순번].Pozicija,stavka_COUNT);열림[순번].Pozicija+=stavka_COUNT;return stavka_COUNT;}
    intptr_t 반환값=사용자호출(2,fajl_hvatište,(uintptr_t)podaci,stavka_COUNT,0,0,0);if(반환값<0){GRESKA=-반환값;return -1;}return 반환값;
}
long write(int fajl_hvatište,const void*podaci,size_t stavka_COUNT){
    if(fajl_hvatište==100){if(stavka_COUNT>sizeof(출력결과)-출력위치){GRESKA=28;return -1;}memcpy(출력결과+출력위치,podaci,stavka_COUNT);출력위치+=stavka_COUNT;if(출력크기<출력위치)출력크기=출력위치;return stavka_COUNT;}
    intptr_t 반환값=사용자호출(1,fajl_hvatište,(uintptr_t)podaci,stavka_COUNT,0,0,0);if(반환값<0){GRESKA=-반환값;return -1;}return 반환값;
}
long lseek(int fajl_hvatište,long Pomak_VALUE,int 기준점){
    if(fajl_hvatište==100){long podaci_položaj=Pomak_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(podaci_položaj<0||(size_t)podaci_položaj>sizeof(출력결과)){GRESKA=22;return -1;}출력위치=podaci_položaj;return podaci_položaj;}
    if(fajl_hvatište>=128&&fajl_hvatište<152&&열림[fajl_hvatište-128].사용량){int 순번=fajl_hvatište-128;long podaci_položaj=Pomak_VALUE+(기준점==0?0:기준점==1?열림[순번].Pozicija:번역기자원들[열림[순번].LOOKUP_INDEX].Veličina);if(podaci_položaj<0||(size_t)podaci_položaj>번역기자원들[열림[순번].LOOKUP_INDEX].Veličina){GRESKA=22;return -1;}열림[순번].Pozicija=podaci_položaj;return podaci_položaj;}
    intptr_t 반환값=사용자호출(5,fajl_hvatište,Pomak_VALUE,기준점,0,0,0);if(반환값<0){GRESKA=-반환값;return -1;}return 반환값;
}
int unlink(const char*Naziv){intptr_t 반환값=사용자호출(11,(uintptr_t)Naziv,0,0,0,0,0);if(반환값<0){GRESKA=-반환값;return -1;}return 반환값;}
char *realpath(const char*Naziv,char*mjera_podaci){if(!mjera_podaci){mjera_podaci=malloc(strlen(Naziv)+1);if(!mjera_podaci)return 0;}return strcpy(mjera_podaci,Naziv);}
char *getcwd(char*podaci_položaj,size_t stavka_COUNT){if(stavka_COUNT<2){GRESKA=34;return 0;}podaci_položaj[0]='/';podaci_položaj[1]=0;return podaci_položaj;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_unos){time_t 임시값=0;if(Terminal_unos)*Terminal_unos=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_unos){(void)Terminal_unos;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int fajl_hvatište,const char*metoda_mod){(void)metoda_mod;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].GRESKA=0;흐름목록[순번].fajl_hvatište=fajl_hvatište;return &흐름목록[순번];}GRESKA=24;return 0;}
int fflush(FILE*fajl_unos){return fajl_unos&&fajl_unos->GRESKA?-1:0;}
int fclose(FILE*fajl_unos){int 반환값=close(fajl_unos->fajl_hvatište);if(fajl_unos->GRESKA)반환값=-1;fajl_unos->사용량=0;return 반환값;}
size_t fwrite(const void*podaci_položaj,size_t string_podaci,size_t stavka_COUNT,FILE*fajl_unos){if(!string_podaci)return 0;if(stavka_COUNT>SIZE_MAX/string_podaci){fajl_unos->GRESKA=1;return 0;}long 반환값=write(fajl_unos->fajl_hvatište,podaci_položaj,string_podaci*stavka_COUNT);if(반환값<0){fajl_unos->GRESKA=1;return 0;}return (size_t)반환값/string_podaci;}
int fputc(int kôd_znaka,FILE*fajl_unos){unsigned char SECOND_VALUE=kôd_znaka;return fwrite(&SECOND_VALUE,1,1,fajl_unos)==1?SECOND_VALUE:EOF;}
int fputs(const char*string_podaci,FILE*fajl_unos){return fwrite(string_podaci,1,strlen(string_podaci),fajl_unos)==strlen(string_podaci)?0:EOF;}
static void 넣기(char*mjera_podaci,size_t 용량한도,size_t*trenutno_položaj,char kôd_znaka){if(*trenutno_položaj+1<용량한도)mjera_podaci[*trenutno_položaj]=kôd_znaka;(*trenutno_položaj)++;}
int vsnprintf(char*mjera_podaci,size_t 용량한도,const char*format,va_list 가변인수){
    size_t trenutno_položaj=0;while(*format){if(*format!='%'){넣기(mjera_podaci,용량한도,&trenutno_položaj,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,정밀도=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;정밀도=0;if(*format=='*'){정밀도=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')정밀도=정밀도*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TYPE_oblast=*format?*format++:0,bafer_Pohrana[80];const char*string_podaci=bafer_Pohrana;size_t stavka_COUNT=0;
        if(TYPE_oblast=='s'){string_podaci=va_arg(가변인수,const char*);if(!string_podaci)string_podaci="(null)";stavka_COUNT=strlen(string_podaci);if(정밀도>=0&&stavka_COUNT>(size_t)정밀도)stavka_COUNT=정밀도;}
        else if(TYPE_oblast=='c'){bafer_Pohrana[0]=va_arg(가변인수,int);stavka_COUNT=1;}
        else if(TYPE_oblast=='%'){bafer_Pohrana[0]='%';stavka_COUNT=1;}
        else if(TYPE_oblast=='d'||TYPE_oblast=='i'||TYPE_oblast=='u'||TYPE_oblast=='x'||TYPE_oblast=='X'||TYPE_oblast=='o'||TYPE_oblast=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_oblast=='d'||TYPE_oblast=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_oblast=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned poster_VALUE=TYPE_oblast=='x'||TYPE_oblast=='X'||TYPE_oblast=='p'?16:TYPE_oblast=='o'?8:10;char cifra_COUNT[64];unsigned 사용량=0;
            do{cifra_COUNT[사용량++]="0123456789abcdef"[VALUE%poster_VALUE];VALUE/=poster_VALUE;}while(VALUE);
            if(음수표시)bafer_Pohrana[stavka_COUNT++]='-';if(TYPE_oblast=='p'||(대체값&&poster_VALUE==16)){bafer_Pohrana[stavka_COUNT++]='0';bafer_Pohrana[stavka_COUNT++]='x';}
            for(int ispuniti_VALUE=(int)사용량;정밀도>ispuniti_VALUE&&stavka_COUNT<sizeof(bafer_Pohrana)-사용량;ispuniti_VALUE++)bafer_Pohrana[stavka_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(stavka_COUNT+사용량)&&stavka_COUNT<sizeof(bafer_Pohrana)-사용량)bafer_Pohrana[stavka_COUNT++]='0';
            while(사용량)bafer_Pohrana[stavka_COUNT++]=cifra_COUNT[--사용량];
        }else{bafer_Pohrana[0]='?';stavka_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)stavka_COUNT){넣기(mjera_podaci,용량한도,&trenutno_položaj,' ');너비--;}
        for(size_t 순번=0;순번<stavka_COUNT;순번++)넣기(mjera_podaci,용량한도,&trenutno_položaj,string_podaci[순번]);while(왼쪽&&너비>(int)stavka_COUNT){넣기(mjera_podaci,용량한도,&trenutno_položaj,' ');너비--;}
    }if(용량한도)mjera_podaci[trenutno_položaj<용량한도?trenutno_položaj:용량한도-1]=0;return trenutno_položaj;
}
int snprintf(char*mjera_podaci,size_t 용량한도,const char*fajl_unos,...){va_list 첫째값;va_start(첫째값,fajl_unos);int 반환값=vsnprintf(mjera_podaci,용량한도,fajl_unos,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*mjera_podaci,const char*fajl_unos,...){va_list 첫째값;va_start(첫째값,fajl_unos);int 반환값=vsnprintf(mjera_podaci,SIZE_MAX,fajl_unos,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*tok_VALUE,const char*fajl_unos,va_list 첫째값){char SECOND_VALUE[2048];int stavka_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),fajl_unos,첫째값);if(stavka_COUNT>2047)stavka_COUNT=2047;return fwrite(SECOND_VALUE,1,stavka_COUNT,tok_VALUE)==(size_t)stavka_COUNT?stavka_COUNT:-1;}
int fprintf(FILE*tok_VALUE,const char*fajl_unos,...){va_list 첫째값;va_start(첫째값,fajl_unos);int 반환값=vfprintf(tok_VALUE,fajl_unos,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fajl_unos,...){va_list 첫째값;va_start(첫째값,fajl_unos);int 반환값=vfprintf(stdout,fajl_unos,첫째값);va_end(첫째값);return 반환값;}
