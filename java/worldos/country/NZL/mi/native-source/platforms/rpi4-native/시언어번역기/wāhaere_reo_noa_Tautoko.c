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
static int Pōhēhē;
int *__errno_location(void){return &Pōhēhē;}
void exit(int tūnga_uara){사용자호출(6,tūnga_uara,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *taki_kīanga,const char *Kōnae,unsigned hononga,const char *aratuka_tāurunga_ingoa){fprintf(stderr,"cc assertion: %s %s:%u %s\n",taki_kīanga,Kōnae,hononga,aratuka_tāurunga_ingoa);exit(1);}
size_t strlen(const char*aho_raraunga){const char*raraunga_tūranga=aho_raraunga;while(*raraunga_tūranga)raraunga_tūranga++;return raraunga_tūranga-aho_raraunga;}
int strcmp(const char*첫째값,const char*SECOND_uara){while(*첫째값&&*첫째값==*SECOND_uara){첫째값++;SECOND_uara++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_uara;}
int strncmp(const char*첫째값,const char*SECOND_uara,size_t tuemi_COUNT){while(tuemi_COUNT--){unsigned char taunga_x=*첫째값++,세로좌표=*SECOND_uara++;if(taunga_x!=세로좌표)return taunga_x-세로좌표;if(!taunga_x)return 0;}return 0;}
char *strcpy(char*ūnga_raraunga,const char*aho_raraunga){char*반환값=ūnga_raraunga;while((*ūnga_raraunga++=*aho_raraunga++)){}return 반환값;}
char *strchr(const char*aho_raraunga,int waehere_pūāhua){do{if(*aho_raraunga==(char)waehere_pūāhua)return (char*)aho_raraunga;}while(*aho_raraunga++);return 0;}
char *strrchr(const char*aho_raraunga,int waehere_pūāhua){const char*반환값=0;do{if(*aho_raraunga==(char)waehere_pūāhua)반환값=aho_raraunga;}while(*aho_raraunga++);return (char*)반환값;}
char *strstr(const char*aho_raraunga,const char*Tauranga_tāurunga){size_t tuemi_COUNT=strlen(Tauranga_tāurunga);for(;*aho_raraunga;aho_raraunga++)if(!strncmp(aho_raraunga,Tauranga_tāurunga,tuemi_COUNT))return (char*)aho_raraunga;return tuemi_COUNT?0:(char*)aho_raraunga;}
int memcmp(const void*첫째값,const void*SECOND_uara,size_t tuemi_COUNT){const unsigned char*taunga_x=첫째값,*세로좌표=SECOND_uara;while(tuemi_COUNT--){if(*taunga_x!=*세로좌표)return *taunga_x-*세로좌표;taunga_x++;세로좌표++;}return 0;}
void *memmove(void*ūnga_raraunga,const void*aho_raraunga,size_t tuemi_COUNT){unsigned char*taunga_x=ūnga_raraunga;const unsigned char*세로좌표=aho_raraunga;if(taunga_x<세로좌표){for(size_t 순번=0;순번<tuemi_COUNT;순번++)taunga_x[순번]=세로좌표[순번];}else while(tuemi_COUNT){tuemi_COUNT--;taunga_x[tuemi_COUNT]=세로좌표[tuemi_COUNT];}return ūnga_raraunga;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct raraunga_aukati {size_t rahi;struct raraunga_aukati*Panuku_tuemi;int 남은공간;int 채울크기;uint64_t tiaronga_ngā_wae;} raraunga_aukati;
static raraunga_aukati *첫항목;
void free(void*raraunga_tūranga){if(!raraunga_tūranga)return;raraunga_aukati*SECOND_uara=(raraunga_aukati*)raraunga_tūranga-1;SECOND_uara->남은공간=1;for(raraunga_aukati*Panuku_OFFSET=첫항목;Panuku_OFFSET&&Panuku_OFFSET->Panuku_tuemi;){if(Panuku_OFFSET->남은공간&&Panuku_OFFSET->Panuku_tuemi->남은공간){Panuku_OFFSET->rahi+=sizeof(raraunga_aukati)+Panuku_OFFSET->Panuku_tuemi->rahi;Panuku_OFFSET->Panuku_tuemi=Panuku_OFFSET->Panuku_tuemi->Panuku_tuemi;}else Panuku_OFFSET=Panuku_OFFSET->Panuku_tuemi;}}
void *realloc(void*raraunga_tūranga,size_t tuemi_COUNT){
    if(!tuemi_COUNT){free(raraunga_tūranga);return 0;}if(tuemi_COUNT>sizeof(할당마당)-sizeof(raraunga_aukati))return 0;tuemi_COUNT=(tuemi_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(raraunga_aukati*)할당마당;첫항목->rahi=sizeof(할당마당)-sizeof(raraunga_aukati);첫항목->남은공간=1;첫항목->Panuku_tuemi=0;}
    raraunga_aukati*이전=raraunga_tūranga?(raraunga_aukati*)raraunga_tūranga-1:0;if(이전&&이전->rahi>=tuemi_COUNT)return raraunga_tūranga;
    for(raraunga_aukati*SECOND_uara=첫항목;SECOND_uara;SECOND_uara=SECOND_uara->Panuku_tuemi)if(SECOND_uara->남은공간&&SECOND_uara->rahi>=tuemi_COUNT){
        if(SECOND_uara->rahi>=tuemi_COUNT+sizeof(raraunga_aukati)+16){raraunga_aukati*나머지부분=(raraunga_aukati*)((unsigned char*)(SECOND_uara+1)+tuemi_COUNT);나머지부분->rahi=SECOND_uara->rahi-tuemi_COUNT-sizeof(raraunga_aukati);나머지부분->Panuku_tuemi=SECOND_uara->Panuku_tuemi;나머지부분->남은공간=1;SECOND_uara->Panuku_tuemi=나머지부분;SECOND_uara->rahi=tuemi_COUNT;}
        SECOND_uara->남은공간=0;void*반환값=SECOND_uara+1;if(이전){memcpy(반환값,raraunga_tūranga,이전->rahi);free(raraunga_tūranga);}return 반환값;
    }Pōhēhē=12;return 0;
}
void *malloc(size_t tuemi_COUNT){return realloc(0,tuemi_COUNT);}
void *calloc(size_t tuemi_COUNT,size_t aho_raraunga){if(aho_raraunga&&tuemi_COUNT>SIZE_MAX/aho_raraunga)return 0;void*raraunga_tūranga=malloc(tuemi_COUNT*aho_raraunga);if(raraunga_tūranga)memset(raraunga_tūranga,0,tuemi_COUNT*aho_raraunga);return raraunga_tūranga;}
unsigned long long strtoull(const char*aho_raraunga,char**mutu_OFFSET,int Papamuri_uara){
    const char*Start_OFFSET=aho_raraunga;while(*aho_raraunga==' '||(*aho_raraunga>=9&&*aho_raraunga<=13))aho_raraunga++;int 음수여부=0;if(*aho_raraunga=='-'||*aho_raraunga=='+')음수여부=*aho_raraunga++=='-';
    if((!Papamuri_uara||Papamuri_uara==16)&&aho_raraunga[0]=='0'&&(aho_raraunga[1]=='x'||aho_raraunga[1]=='X')){Papamuri_uara=16;aho_raraunga+=2;}if(!Papamuri_uara)Papamuri_uara=*aho_raraunga=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned waehere_pūāhua=*aho_raraunga,ūnga_raraunga=waehere_pūāhua>='0'&&waehere_pūāhua<='9'?waehere_pūāhua-'0':waehere_pūāhua>='a'&&waehere_pūāhua<='z'?waehere_pūāhua-'a'+10:waehere_pūāhua>='A'&&waehere_pūāhua<='Z'?waehere_pūāhua-'A'+10:99;if(ūnga_raraunga>=(unsigned)Papamuri_uara)break;하나라도=1;aho_raraunga++;if(임시값>(~0ull-ūnga_raraunga)/(unsigned)Papamuri_uara){임시값=~0ull;Pōhēhē=34;}else 임시값=임시값*Papamuri_uara+ūnga_raraunga;}
    if(mutu_OFFSET)*mutu_OFFSET=(char*)(하나라도?aho_raraunga:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*aho_raraunga,char**보조항목,int SECOND_uara){return strtoull(aho_raraunga,보조항목,SECOND_uara);}
long strtol(const char*aho_raraunga,char**보조항목,int SECOND_uara){return (long)strtoull(aho_raraunga,보조항목,SECOND_uara);}
int atoi(const char*aho_raraunga){return (int)strtol(aho_raraunga,0,10);}
long double ldexpl(long double taunga_x,int tuemi_COUNT){while(tuemi_COUNT>0){taunga_x*=2;tuemi_COUNT--;}while(tuemi_COUNT<0){taunga_x/=2;tuemi_COUNT++;}return taunga_x;}
long double strtold(const char*aho_raraunga,char**mutu_OFFSET){
    const char*Start_OFFSET=aho_raraunga;while(*aho_raraunga==' '||(*aho_raraunga>=9&&*aho_raraunga<=13))aho_raraunga++;int 음수여부=0;if(*aho_raraunga=='-'||*aho_raraunga=='+')음수여부=*aho_raraunga++=='-';
    int Papamuri_uara=10;if(aho_raraunga[0]=='0'&&(aho_raraunga[1]=='x'||aho_raraunga[1]=='X')){Papamuri_uara=16;aho_raraunga+=2;}long double 임시값=0,tauine=1;int 소수부=0,하나라도=0;
    for(;;){int waehere_pūāhua=*aho_raraunga,ūnga_raraunga=waehere_pūāhua>='0'&&waehere_pūāhua<='9'?waehere_pūāhua-'0':waehere_pūāhua>='a'&&waehere_pūāhua<='f'?waehere_pūāhua-'a'+10:waehere_pūāhua>='A'&&waehere_pūāhua<='F'?waehere_pūāhua-'A'+10:99;
        if(waehere_pūāhua=='.'&&!소수부){소수부=1;aho_raraunga++;continue;}if(ūnga_raraunga>=Papamuri_uara)break;하나라도=1;aho_raraunga++;임시값=임시값*Papamuri_uara+ūnga_raraunga;if(소수부)tauine*=Papamuri_uara;
    }임시값/=tauine;
    if((Papamuri_uara==10&&(*aho_raraunga=='e'||*aho_raraunga=='E'))||(Papamuri_uara==16&&(*aho_raraunga=='p'||*aho_raraunga=='P'))){const char*whakaatu_uara=aho_raraunga++;int 빼기=0;if(*aho_raraunga=='-'||*aho_raraunga=='+')빼기=*aho_raraunga++=='-';int tuemi_COUNT=0,tāurunga_COUNT=0;while(*aho_raraunga>='0'&&*aho_raraunga<='9'){tāurunga_COUNT++;if(tuemi_COUNT<20000)tuemi_COUNT=tuemi_COUNT*10+*aho_raraunga-'0';aho_raraunga++;}if(!tāurunga_COUNT)aho_raraunga=whakaatu_uara;else{long double tauwehe=Papamuri_uara==16?2:10;while(tuemi_COUNT-->0&&tuemi_COUNT<200000)임시값=빼기?임시값/tauwehe:임시값*tauwehe;}}
    if(mutu_OFFSET)*mutu_OFFSET=(char*)(하나라도?aho_raraunga:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*aho_raraunga,char**보조항목){return (double)strtold(aho_raraunga,보조항목);}float strtof(const char*aho_raraunga,char**보조항목){return (float)strtold(aho_raraunga,보조항목);}
void qsort(void*Papamuri_uara,size_t tuemi_COUNT,size_t rahi,int(*Whakatairite)(const void*,const void*)){
    unsigned char*raraunga_tūranga=Papamuri_uara;for(size_t 순번=1;순번<tuemi_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Whakatairite(raraunga_tūranga+(안쪽순번-1)*rahi,raraunga_tūranga+안쪽순번*rahi)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<rahi;셋째순번++){unsigned char waehere_pūāhua=raraunga_tūranga[(안쪽순번-1)*rahi+셋째순번];raraunga_tūranga[(안쪽순번-1)*rahi+셋째순번]=raraunga_tūranga[안쪽순번*rahi+셋째순번];raraunga_tūranga[안쪽순번*rahi+셋째순번]=waehere_pūāhua;}
}
static struct {int 사용량,Rapu_INDEX;size_t tūranga;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *tuemi_COUNT){*tuemi_COUNT=출력크기;return 출력결과;}
int open(const char*Ingoa,int 설정비트,...){
    if(!strcmp(Ingoa,"/@cc-output")){if(출력열림){Pōhēhē=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Ingoa,번역기자원들[순번].Ingoa)){
        if(설정비트&3){Pōhēhē=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].Rapu_INDEX=순번;열림[안쪽순번].tūranga=0;return 128+안쪽순번;}Pōhēhē=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Ingoa,설정비트,0,0,0,0);if(반환값<0){Pōhēhē=-반환값;return -1;}return 반환값;
}
int close(int kōnae_raweke){if(kōnae_raweke==100){출력열림=0;return 0;}if(kōnae_raweke>=128&&kōnae_raweke<152){열림[kōnae_raweke-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,kōnae_raweke,0,0,0,0,0);if(반환값<0){Pōhēhē=-반환값;return -1;}return 0;}
long read(int kōnae_raweke,void*raraunga,size_t tuemi_COUNT){
    if(kōnae_raweke>=128&&kōnae_raweke<152&&열림[kōnae_raweke-128].사용량){int 순번=kōnae_raweke-128;const 번역기자원*반환값=&번역기자원들[열림[순번].Rapu_INDEX];size_t 왼쪽=반환값->rahi-열림[순번].tūranga;if(tuemi_COUNT>왼쪽)tuemi_COUNT=왼쪽;memcpy(raraunga,반환값->raraunga+열림[순번].tūranga,tuemi_COUNT);열림[순번].tūranga+=tuemi_COUNT;return tuemi_COUNT;}
    intptr_t 반환값=사용자호출(2,kōnae_raweke,(uintptr_t)raraunga,tuemi_COUNT,0,0,0);if(반환값<0){Pōhēhē=-반환값;return -1;}return 반환값;
}
long write(int kōnae_raweke,const void*raraunga,size_t tuemi_COUNT){
    if(kōnae_raweke==100){if(tuemi_COUNT>sizeof(출력결과)-출력위치){Pōhēhē=28;return -1;}memcpy(출력결과+출력위치,raraunga,tuemi_COUNT);출력위치+=tuemi_COUNT;if(출력크기<출력위치)출력크기=출력위치;return tuemi_COUNT;}
    intptr_t 반환값=사용자호출(1,kōnae_raweke,(uintptr_t)raraunga,tuemi_COUNT,0,0,0);if(반환값<0){Pōhēhē=-반환값;return -1;}return 반환값;
}
long lseek(int kōnae_raweke,long OFFSET_uara,int 기준점){
    if(kōnae_raweke==100){long raraunga_tūranga=OFFSET_uara+(기준점==0?0:기준점==1?출력위치:출력크기);if(raraunga_tūranga<0||(size_t)raraunga_tūranga>sizeof(출력결과)){Pōhēhē=22;return -1;}출력위치=raraunga_tūranga;return raraunga_tūranga;}
    if(kōnae_raweke>=128&&kōnae_raweke<152&&열림[kōnae_raweke-128].사용량){int 순번=kōnae_raweke-128;long raraunga_tūranga=OFFSET_uara+(기준점==0?0:기준점==1?열림[순번].tūranga:번역기자원들[열림[순번].Rapu_INDEX].rahi);if(raraunga_tūranga<0||(size_t)raraunga_tūranga>번역기자원들[열림[순번].Rapu_INDEX].rahi){Pōhēhē=22;return -1;}열림[순번].tūranga=raraunga_tūranga;return raraunga_tūranga;}
    intptr_t 반환값=사용자호출(5,kōnae_raweke,OFFSET_uara,기준점,0,0,0);if(반환값<0){Pōhēhē=-반환값;return -1;}return 반환값;
}
int unlink(const char*Ingoa){intptr_t 반환값=사용자호출(11,(uintptr_t)Ingoa,0,0,0,0,0);if(반환값<0){Pōhēhē=-반환값;return -1;}return 반환값;}
char *realpath(const char*Ingoa,char*mēhua_raraunga){if(!mēhua_raraunga){mēhua_raraunga=malloc(strlen(Ingoa)+1);if(!mēhua_raraunga)return 0;}return strcpy(mēhua_raraunga,Ingoa);}
char *getcwd(char*raraunga_tūranga,size_t tuemi_COUNT){if(tuemi_COUNT<2){Pōhēhē=34;return 0;}raraunga_tūranga[0]='/';raraunga_tūranga[1]=0;return raraunga_tūranga;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Tauranga_tāurunga){time_t 임시값=0;if(Tauranga_tāurunga)*Tauranga_tāurunga=임시값;return 임시값;}
struct tm *localtime(const time_t*Tauranga_tāurunga){(void)Tauranga_tāurunga;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int kōnae_raweke,const char*aratuka_MODE){(void)aratuka_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Pōhēhē=0;흐름목록[순번].kōnae_raweke=kōnae_raweke;return &흐름목록[순번];}Pōhēhē=24;return 0;}
int fflush(FILE*kōnae_tāurunga){return kōnae_tāurunga&&kōnae_tāurunga->Pōhēhē?-1:0;}
int fclose(FILE*kōnae_tāurunga){int 반환값=close(kōnae_tāurunga->kōnae_raweke);if(kōnae_tāurunga->Pōhēhē)반환값=-1;kōnae_tāurunga->사용량=0;return 반환값;}
size_t fwrite(const void*raraunga_tūranga,size_t aho_raraunga,size_t tuemi_COUNT,FILE*kōnae_tāurunga){if(!aho_raraunga)return 0;if(tuemi_COUNT>SIZE_MAX/aho_raraunga){kōnae_tāurunga->Pōhēhē=1;return 0;}long 반환값=write(kōnae_tāurunga->kōnae_raweke,raraunga_tūranga,aho_raraunga*tuemi_COUNT);if(반환값<0){kōnae_tāurunga->Pōhēhē=1;return 0;}return (size_t)반환값/aho_raraunga;}
int fputc(int waehere_pūāhua,FILE*kōnae_tāurunga){unsigned char SECOND_uara=waehere_pūāhua;return fwrite(&SECOND_uara,1,1,kōnae_tāurunga)==1?SECOND_uara:EOF;}
int fputs(const char*aho_raraunga,FILE*kōnae_tāurunga){return fwrite(aho_raraunga,1,strlen(aho_raraunga),kōnae_tāurunga)==strlen(aho_raraunga)?0:EOF;}
static void 넣기(char*mēhua_raraunga,size_t 용량한도,size_t*현재위치,char waehere_pūāhua){if(*현재위치+1<용량한도)mēhua_raraunga[*현재위치]=waehere_pūāhua;(*현재위치)++;}
int vsnprintf(char*mēhua_raraunga,size_t 용량한도,const char*hōputu,va_list 가변인수){
    size_t 현재위치=0;while(*hōputu){if(*hōputu!='%'){넣기(mēhua_raraunga,용량한도,&현재위치,*hōputu++);continue;}hōputu++;
        int 왼쪽=0,영값=0,대체값=0;while(*hōputu=='-'||*hōputu=='0'||*hōputu=='#'||*hōputu=='+'||*hōputu==' '){if(*hōputu=='-')왼쪽=1;if(*hōputu=='0')영값=1;if(*hōputu=='#')대체값=1;hōputu++;}
        int 너비=0,정밀도=-1;if(*hōputu=='*'){너비=va_arg(가변인수,int);hōputu++;}else while(*hōputu>='0'&&*hōputu<='9')너비=너비*10+*hōputu++-'0';
        if(*hōputu=='.'){hōputu++;정밀도=0;if(*hōputu=='*'){정밀도=va_arg(가변인수,int);hōputu++;}else while(*hōputu>='0'&&*hōputu<='9')정밀도=정밀도*10+*hōputu++-'0';}
        int 넓은글자=0;while(*hōputu=='l'||*hōputu=='z'||*hōputu=='t'||*hōputu=='j'||*hōputu=='h'){if(*hōputu!='h')넓은글자=1;hōputu++;}
        char TYPE_kāwai=*hōputu?*hōputu++:0,pūreirei_Rokiroki[80];const char*aho_raraunga=pūreirei_Rokiroki;size_t tuemi_COUNT=0;
        if(TYPE_kāwai=='s'){aho_raraunga=va_arg(가변인수,const char*);if(!aho_raraunga)aho_raraunga="(null)";tuemi_COUNT=strlen(aho_raraunga);if(정밀도>=0&&tuemi_COUNT>(size_t)정밀도)tuemi_COUNT=정밀도;}
        else if(TYPE_kāwai=='c'){pūreirei_Rokiroki[0]=va_arg(가변인수,int);tuemi_COUNT=1;}
        else if(TYPE_kāwai=='%'){pūreirei_Rokiroki[0]='%';tuemi_COUNT=1;}
        else if(TYPE_kāwai=='d'||TYPE_kāwai=='i'||TYPE_kāwai=='u'||TYPE_kāwai=='x'||TYPE_kāwai=='X'||TYPE_kāwai=='o'||TYPE_kāwai=='p'){
            unsigned long long uara;int 음수표시=0;
            if(TYPE_kāwai=='d'||TYPE_kāwai=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;uara=음수표시?0-(unsigned long long)임시값:임시값;}
            else uara=TYPE_kāwai=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Papamuri_uara=TYPE_kāwai=='x'||TYPE_kāwai=='X'||TYPE_kāwai=='p'?16:TYPE_kāwai=='o'?8:10;char mati_COUNT[64];unsigned 사용량=0;
            do{mati_COUNT[사용량++]="0123456789abcdef"[uara%Papamuri_uara];uara/=Papamuri_uara;}while(uara);
            if(음수표시)pūreirei_Rokiroki[tuemi_COUNT++]='-';if(TYPE_kāwai=='p'||(대체값&&Papamuri_uara==16)){pūreirei_Rokiroki[tuemi_COUNT++]='0';pūreirei_Rokiroki[tuemi_COUNT++]='x';}
            for(int whakakī_uara=(int)사용량;정밀도>whakakī_uara&&tuemi_COUNT<sizeof(pūreirei_Rokiroki)-사용량;whakakī_uara++)pūreirei_Rokiroki[tuemi_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(tuemi_COUNT+사용량)&&tuemi_COUNT<sizeof(pūreirei_Rokiroki)-사용량)pūreirei_Rokiroki[tuemi_COUNT++]='0';
            while(사용량)pūreirei_Rokiroki[tuemi_COUNT++]=mati_COUNT[--사용량];
        }else{pūreirei_Rokiroki[0]='?';tuemi_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)tuemi_COUNT){넣기(mēhua_raraunga,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<tuemi_COUNT;순번++)넣기(mēhua_raraunga,용량한도,&현재위치,aho_raraunga[순번]);while(왼쪽&&너비>(int)tuemi_COUNT){넣기(mēhua_raraunga,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)mēhua_raraunga[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*mēhua_raraunga,size_t 용량한도,const char*kōnae_tāurunga,...){va_list 첫째값;va_start(첫째값,kōnae_tāurunga);int 반환값=vsnprintf(mēhua_raraunga,용량한도,kōnae_tāurunga,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*mēhua_raraunga,const char*kōnae_tāurunga,...){va_list 첫째값;va_start(첫째값,kōnae_tāurunga);int 반환값=vsnprintf(mēhua_raraunga,SIZE_MAX,kōnae_tāurunga,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*roma_uara,const char*kōnae_tāurunga,va_list 첫째값){char SECOND_uara[2048];int tuemi_COUNT=vsnprintf(SECOND_uara,sizeof(SECOND_uara),kōnae_tāurunga,첫째값);if(tuemi_COUNT>2047)tuemi_COUNT=2047;return fwrite(SECOND_uara,1,tuemi_COUNT,roma_uara)==(size_t)tuemi_COUNT?tuemi_COUNT:-1;}
int fprintf(FILE*roma_uara,const char*kōnae_tāurunga,...){va_list 첫째값;va_start(첫째값,kōnae_tāurunga);int 반환값=vfprintf(roma_uara,kōnae_tāurunga,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*kōnae_tāurunga,...){va_list 첫째값;va_start(첫째값,kōnae_tāurunga);int 반환값=vfprintf(stdout,kōnae_tāurunga,첫째값);va_end(첫째값);return 반환값;}
