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
static int IKOSA;
int *__errno_location(void){return &IKOSA;}
void exit(int imimerere_agaciro){사용자호출(6,imimerere_agaciro,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *sheki_imvugo,const char *Idosiye,unsigned umurongo,const char *uburyo_icyinjizwa_izina){fprintf(stderr,"cc assertion: %s %s:%u %s\n",sheki_imvugo,Idosiye,umurongo,uburyo_icyinjizwa_izina);exit(1);}
size_t strlen(const char*igicenteruro_amakurushingiro){const char*자료위치=igicenteruro_amakurushingiro;while(*자료위치)자료위치++;return 자료위치-igicenteruro_amakurushingiro;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char Ihuza_rya_x=*첫째값++,세로좌표=*둘째값++;if(Ihuza_rya_x!=세로좌표)return Ihuza_rya_x-세로좌표;if(!Ihuza_rya_x)return 0;}return 0;}
char *strcpy(char*aho_ijya_amakurushingiro,const char*igicenteruro_amakurushingiro){char*반환값=aho_ijya_amakurushingiro;while((*aho_ijya_amakurushingiro++=*igicenteruro_amakurushingiro++)){}return 반환값;}
char *strchr(const char*igicenteruro_amakurushingiro,int 문자값){do{if(*igicenteruro_amakurushingiro==(char)문자값)return (char*)igicenteruro_amakurushingiro;}while(*igicenteruro_amakurushingiro++);return 0;}
char *strrchr(const char*igicenteruro_amakurushingiro,int 문자값){const char*반환값=0;do{if(*igicenteruro_amakurushingiro==(char)문자값)반환값=igicenteruro_amakurushingiro;}while(*igicenteruro_amakurushingiro++);return (char*)반환값;}
char *strstr(const char*igicenteruro_amakurushingiro,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*igicenteruro_amakurushingiro;igicenteruro_amakurushingiro++)if(!strncmp(igicenteruro_amakurushingiro,터미널항목,개수))return (char*)igicenteruro_amakurushingiro;return 개수?0:(char*)igicenteruro_amakurushingiro;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*Ihuza_rya_x=첫째값,*세로좌표=둘째값;while(개수--){if(*Ihuza_rya_x!=*세로좌표)return *Ihuza_rya_x-*세로좌표;Ihuza_rya_x++;세로좌표++;}return 0;}
void *memmove(void*aho_ijya_amakurushingiro,const void*igicenteruro_amakurushingiro,size_t 개수){unsigned char*Ihuza_rya_x=aho_ijya_amakurushingiro;const unsigned char*세로좌표=igicenteruro_amakurushingiro;if(Ihuza_rya_x<세로좌표){for(size_t 순번=0;순번<개수;순번++)Ihuza_rya_x[순번]=세로좌표[순번];}else while(개수){개수--;Ihuza_rya_x[개수]=세로좌표[개수];}return aho_ijya_amakurushingiro;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct amakurushingiro_guheza {size_t Ingano;struct amakurushingiro_guheza*다음;int 남은공간;int 채울크기;uint64_t umitondekere_ibinyabumwe;} amakurushingiro_guheza;
static amakurushingiro_guheza *첫항목;
void free(void*자료위치){if(!자료위치)return;amakurushingiro_guheza*둘째값=(amakurushingiro_guheza*)자료위치-1;둘째값->남은공간=1;for(amakurushingiro_guheza*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->Ingano+=sizeof(amakurushingiro_guheza)+다음위치->다음->Ingano;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(amakurushingiro_guheza))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(amakurushingiro_guheza*)할당마당;첫항목->Ingano=sizeof(할당마당)-sizeof(amakurushingiro_guheza);첫항목->남은공간=1;첫항목->다음=0;}
    amakurushingiro_guheza*이전=자료위치?(amakurushingiro_guheza*)자료위치-1:0;if(이전&&이전->Ingano>=개수)return 자료위치;
    for(amakurushingiro_guheza*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->Ingano>=개수){
        if(둘째값->Ingano>=개수+sizeof(amakurushingiro_guheza)+16){amakurushingiro_guheza*나머지부분=(amakurushingiro_guheza*)((unsigned char*)(둘째값+1)+개수);나머지부분->Ingano=둘째값->Ingano-개수-sizeof(amakurushingiro_guheza);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->Ingano=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->Ingano);free(자료위치);}return 반환값;
    }IKOSA=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t igicenteruro_amakurushingiro){if(igicenteruro_amakurushingiro&&개수>SIZE_MAX/igicenteruro_amakurushingiro)return 0;void*자료위치=malloc(개수*igicenteruro_amakurushingiro);if(자료위치)memset(자료위치,0,개수*igicenteruro_amakurushingiro);return 자료위치;}
unsigned long long strtoull(const char*igicenteruro_amakurushingiro,char**kurangiza_Ofuseti,int Imbuganyuma_agaciro){
    const char*Itangira_Ofuseti=igicenteruro_amakurushingiro;while(*igicenteruro_amakurushingiro==' '||(*igicenteruro_amakurushingiro>=9&&*igicenteruro_amakurushingiro<=13))igicenteruro_amakurushingiro++;int 음수여부=0;if(*igicenteruro_amakurushingiro=='-'||*igicenteruro_amakurushingiro=='+')음수여부=*igicenteruro_amakurushingiro++=='-';
    if((!Imbuganyuma_agaciro||Imbuganyuma_agaciro==16)&&igicenteruro_amakurushingiro[0]=='0'&&(igicenteruro_amakurushingiro[1]=='x'||igicenteruro_amakurushingiro[1]=='X')){Imbuganyuma_agaciro=16;igicenteruro_amakurushingiro+=2;}if(!Imbuganyuma_agaciro)Imbuganyuma_agaciro=*igicenteruro_amakurushingiro=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned 문자값=*igicenteruro_amakurushingiro,aho_ijya_amakurushingiro=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='z'?문자값-'a'+10:문자값>='A'&&문자값<='Z'?문자값-'A'+10:99;if(aho_ijya_amakurushingiro>=(unsigned)Imbuganyuma_agaciro)break;하나라도=1;igicenteruro_amakurushingiro++;if(임시값>(~0ull-aho_ijya_amakurushingiro)/(unsigned)Imbuganyuma_agaciro){임시값=~0ull;IKOSA=34;}else 임시값=임시값*Imbuganyuma_agaciro+aho_ijya_amakurushingiro;}
    if(kurangiza_Ofuseti)*kurangiza_Ofuseti=(char*)(하나라도?igicenteruro_amakurushingiro:Itangira_Ofuseti);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*igicenteruro_amakurushingiro,char**보조항목,int 둘째값){return strtoull(igicenteruro_amakurushingiro,보조항목,둘째값);}
long strtol(const char*igicenteruro_amakurushingiro,char**보조항목,int 둘째값){return (long)strtoull(igicenteruro_amakurushingiro,보조항목,둘째값);}
int atoi(const char*igicenteruro_amakurushingiro){return (int)strtol(igicenteruro_amakurushingiro,0,10);}
long double ldexpl(long double Ihuza_rya_x,int 개수){while(개수>0){Ihuza_rya_x*=2;개수--;}while(개수<0){Ihuza_rya_x/=2;개수++;}return Ihuza_rya_x;}
long double strtold(const char*igicenteruro_amakurushingiro,char**kurangiza_Ofuseti){
    const char*Itangira_Ofuseti=igicenteruro_amakurushingiro;while(*igicenteruro_amakurushingiro==' '||(*igicenteruro_amakurushingiro>=9&&*igicenteruro_amakurushingiro<=13))igicenteruro_amakurushingiro++;int 음수여부=0;if(*igicenteruro_amakurushingiro=='-'||*igicenteruro_amakurushingiro=='+')음수여부=*igicenteruro_amakurushingiro++=='-';
    int Imbuganyuma_agaciro=10;if(igicenteruro_amakurushingiro[0]=='0'&&(igicenteruro_amakurushingiro[1]=='x'||igicenteruro_amakurushingiro[1]=='X')){Imbuganyuma_agaciro=16;igicenteruro_amakurushingiro+=2;}long double 임시값=0,kuringanyiza=1;int 소수부=0,하나라도=0;
    for(;;){int 문자값=*igicenteruro_amakurushingiro,aho_ijya_amakurushingiro=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='f'?문자값-'a'+10:문자값>='A'&&문자값<='F'?문자값-'A'+10:99;
        if(문자값=='.'&&!소수부){소수부=1;igicenteruro_amakurushingiro++;continue;}if(aho_ijya_amakurushingiro>=Imbuganyuma_agaciro)break;하나라도=1;igicenteruro_amakurushingiro++;임시값=임시값*Imbuganyuma_agaciro+aho_ijya_amakurushingiro;if(소수부)kuringanyiza*=Imbuganyuma_agaciro;
    }임시값/=kuringanyiza;
    if((Imbuganyuma_agaciro==10&&(*igicenteruro_amakurushingiro=='e'||*igicenteruro_amakurushingiro=='E'))||(Imbuganyuma_agaciro==16&&(*igicenteruro_amakurushingiro=='p'||*igicenteruro_amakurushingiro=='P'))){const char*kugaragaza_agaciro=igicenteruro_amakurushingiro++;int 빼기=0;if(*igicenteruro_amakurushingiro=='-'||*igicenteruro_amakurushingiro=='+')빼기=*igicenteruro_amakurushingiro++=='-';int 개수=0,항목수=0;while(*igicenteruro_amakurushingiro>='0'&&*igicenteruro_amakurushingiro<='9'){항목수++;if(개수<20000)개수=개수*10+*igicenteruro_amakurushingiro-'0';igicenteruro_amakurushingiro++;}if(!항목수)igicenteruro_amakurushingiro=kugaragaza_agaciro;else{long double umubare_56e6e1bc=Imbuganyuma_agaciro==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/umubare_56e6e1bc:임시값*umubare_56e6e1bc;}}
    if(kurangiza_Ofuseti)*kurangiza_Ofuseti=(char*)(하나라도?igicenteruro_amakurushingiro:Itangira_Ofuseti);return 음수여부?-임시값:임시값;
}
double strtod(const char*igicenteruro_amakurushingiro,char**보조항목){return (double)strtold(igicenteruro_amakurushingiro,보조항목);}float strtof(const char*igicenteruro_amakurushingiro,char**보조항목){return (float)strtold(igicenteruro_amakurushingiro,보조항목);}
void qsort(void*Imbuganyuma_agaciro,size_t 개수,size_t Ingano,int(*Kugereranya)(const void*,const void*)){
    unsigned char*자료위치=Imbuganyuma_agaciro;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Kugereranya(자료위치+(안쪽순번-1)*Ingano,자료위치+안쪽순번*Ingano)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Ingano;셋째순번++){unsigned char 문자값=자료위치[(안쪽순번-1)*Ingano+셋째순번];자료위치[(안쪽순번-1)*Ingano+셋째순번]=자료위치[안쪽순번*Ingano+셋째순번];자료위치[안쪽순번*Ingano+셋째순번]=문자값;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Izina,int 설정비트,...){
    if(!strcmp(Izina,"/@cc-output")){if(출력열림){IKOSA=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Izina,번역기자원들[순번].Izina)){
        if(설정비트&3){IKOSA=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}IKOSA=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Izina,설정비트,0,0,0,0);if(반환값<0){IKOSA=-반환값;return -1;}return 반환값;
}
int close(int dosiye_umukondo){if(dosiye_umukondo==100){출력열림=0;return 0;}if(dosiye_umukondo>=128&&dosiye_umukondo<152){열림[dosiye_umukondo-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,dosiye_umukondo,0,0,0,0,0);if(반환값<0){IKOSA=-반환값;return -1;}return 0;}
long read(int dosiye_umukondo,void*amakurushingiro,size_t 개수){
    if(dosiye_umukondo>=128&&dosiye_umukondo<152&&열림[dosiye_umukondo-128].사용량){int 순번=dosiye_umukondo-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->Ingano-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(amakurushingiro,반환값->amakurushingiro+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,dosiye_umukondo,(uintptr_t)amakurushingiro,개수,0,0,0);if(반환값<0){IKOSA=-반환값;return -1;}return 반환값;
}
long write(int dosiye_umukondo,const void*amakurushingiro,size_t 개수){
    if(dosiye_umukondo==100){if(개수>sizeof(출력결과)-출력위치){IKOSA=28;return -1;}memcpy(출력결과+출력위치,amakurushingiro,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,dosiye_umukondo,(uintptr_t)amakurushingiro,개수,0,0,0);if(반환값<0){IKOSA=-반환값;return -1;}return 반환값;
}
long lseek(int dosiye_umukondo,long Ofuseti_agaciro,int 기준점){
    if(dosiye_umukondo==100){long 자료위치=Ofuseti_agaciro+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){IKOSA=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(dosiye_umukondo>=128&&dosiye_umukondo<152&&열림[dosiye_umukondo-128].사용량){int 순번=dosiye_umukondo-128;long 자료위치=Ofuseti_agaciro+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].Ingano);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].Ingano){IKOSA=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,dosiye_umukondo,Ofuseti_agaciro,기준점,0,0,0);if(반환값<0){IKOSA=-반환값;return -1;}return 반환값;
}
int unlink(const char*Izina){intptr_t 반환값=사용자호출(11,(uintptr_t)Izina,0,0,0,0,0);if(반환값<0){IKOSA=-반환값;return -1;}return 반환값;}
char *realpath(const char*Izina,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Izina)+1);if(!결과자료)return 0;}return strcpy(결과자료,Izina);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){IKOSA=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int dosiye_umukondo,const char*uburyo_uburyo){(void)uburyo_uburyo;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].IKOSA=0;흐름목록[순번].dosiye_umukondo=dosiye_umukondo;return &흐름목록[순번];}IKOSA=24;return 0;}
int fflush(FILE*dosiye_icyinjizwa){return dosiye_icyinjizwa&&dosiye_icyinjizwa->IKOSA?-1:0;}
int fclose(FILE*dosiye_icyinjizwa){int 반환값=close(dosiye_icyinjizwa->dosiye_umukondo);if(dosiye_icyinjizwa->IKOSA)반환값=-1;dosiye_icyinjizwa->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t igicenteruro_amakurushingiro,size_t 개수,FILE*dosiye_icyinjizwa){if(!igicenteruro_amakurushingiro)return 0;if(개수>SIZE_MAX/igicenteruro_amakurushingiro){dosiye_icyinjizwa->IKOSA=1;return 0;}long 반환값=write(dosiye_icyinjizwa->dosiye_umukondo,자료위치,igicenteruro_amakurushingiro*개수);if(반환값<0){dosiye_icyinjizwa->IKOSA=1;return 0;}return (size_t)반환값/igicenteruro_amakurushingiro;}
int fputc(int 문자값,FILE*dosiye_icyinjizwa){unsigned char 둘째값=문자값;return fwrite(&둘째값,1,1,dosiye_icyinjizwa)==1?둘째값:EOF;}
int fputs(const char*igicenteruro_amakurushingiro,FILE*dosiye_icyinjizwa){return fwrite(igicenteruro_amakurushingiro,1,strlen(igicenteruro_amakurushingiro),dosiye_icyinjizwa)==strlen(igicenteruro_amakurushingiro)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char 문자값){if(*현재위치+1<용량한도)결과자료[*현재위치]=문자값;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*imiterere,va_list 가변인수){
    size_t 현재위치=0;while(*imiterere){if(*imiterere!='%'){넣기(결과자료,용량한도,&현재위치,*imiterere++);continue;}imiterere++;
        int 왼쪽=0,영값=0,대체값=0;while(*imiterere=='-'||*imiterere=='0'||*imiterere=='#'||*imiterere=='+'||*imiterere==' '){if(*imiterere=='-')왼쪽=1;if(*imiterere=='0')영값=1;if(*imiterere=='#')대체값=1;imiterere++;}
        int 너비=0,정밀도=-1;if(*imiterere=='*'){너비=va_arg(가변인수,int);imiterere++;}else while(*imiterere>='0'&&*imiterere<='9')너비=너비*10+*imiterere++-'0';
        if(*imiterere=='.'){imiterere++;정밀도=0;if(*imiterere=='*'){정밀도=va_arg(가변인수,int);imiterere++;}else while(*imiterere>='0'&&*imiterere<='9')정밀도=정밀도*10+*imiterere++-'0';}
        int 넓은글자=0;while(*imiterere=='l'||*imiterere=='z'||*imiterere=='t'||*imiterere=='j'||*imiterere=='h'){if(*imiterere!='h')넓은글자=1;imiterere++;}
        char 유형=*imiterere?*imiterere++:0,ububiko_gateganyo_Ububiko[80];const char*igicenteruro_amakurushingiro=ububiko_gateganyo_Ububiko;size_t 개수=0;
        if(유형=='s'){igicenteruro_amakurushingiro=va_arg(가변인수,const char*);if(!igicenteruro_amakurushingiro)igicenteruro_amakurushingiro="(null)";개수=strlen(igicenteruro_amakurushingiro);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(유형=='c'){ububiko_gateganyo_Ububiko[0]=va_arg(가변인수,int);개수=1;}
        else if(유형=='%'){ububiko_gateganyo_Ububiko[0]='%';개수=1;}
        else if(유형=='d'||유형=='i'||유형=='u'||유형=='x'||유형=='X'||유형=='o'||유형=='p'){
            unsigned long long agaciro;int 음수표시=0;
            if(유형=='d'||유형=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;agaciro=음수표시?0-(unsigned long long)임시값:임시값;}
            else agaciro=유형=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Imbuganyuma_agaciro=유형=='x'||유형=='X'||유형=='p'?16:유형=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[agaciro%Imbuganyuma_agaciro];agaciro/=Imbuganyuma_agaciro;}while(agaciro);
            if(음수표시)ububiko_gateganyo_Ububiko[개수++]='-';if(유형=='p'||(대체값&&Imbuganyuma_agaciro==16)){ububiko_gateganyo_Ububiko[개수++]='0';ububiko_gateganyo_Ububiko[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(ububiko_gateganyo_Ububiko)-사용량;채움++)ububiko_gateganyo_Ububiko[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(ububiko_gateganyo_Ububiko)-사용량)ububiko_gateganyo_Ububiko[개수++]='0';
            while(사용량)ububiko_gateganyo_Ububiko[개수++]=숫자수[--사용량];
        }else{ububiko_gateganyo_Ububiko[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,igicenteruro_amakurushingiro[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*dosiye_icyinjizwa,...){va_list 첫째값;va_start(첫째값,dosiye_icyinjizwa);int 반환값=vsnprintf(결과자료,용량한도,dosiye_icyinjizwa,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*dosiye_icyinjizwa,...){va_list 첫째값;va_start(첫째값,dosiye_icyinjizwa);int 반환값=vsnprintf(결과자료,SIZE_MAX,dosiye_icyinjizwa,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_agaciro,const char*dosiye_icyinjizwa,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),dosiye_icyinjizwa,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,Stream_agaciro)==(size_t)개수?개수:-1;}
int fprintf(FILE*Stream_agaciro,const char*dosiye_icyinjizwa,...){va_list 첫째값;va_start(첫째값,dosiye_icyinjizwa);int 반환값=vfprintf(Stream_agaciro,dosiye_icyinjizwa,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*dosiye_icyinjizwa,...){va_list 첫째값;va_start(첫째값,dosiye_icyinjizwa);int 반환값=vfprintf(stdout,dosiye_icyinjizwa,첫째값);va_end(첫째값);return 반환값;}
