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
static int Хата;
int *__errno_location(void){return &Хата;}
void exit(int халәт_VALUE){사용자호출(6,халәт_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *чек_аңлатма,const char *Birem,unsigned юл,const char *ысул_кертү_исем){fprintf(stderr,"cc assertion: %s %s:%u %s\n",чек_аңлатма,Birem,юл,ысул_кертү_исем);exit(1);}
size_t strlen(const char*юл_мәгълүмат){const char*мәгълүмат_урнаштыру=юл_мәгълүмат;while(*мәгълүмат_урнаштыру)мәгълүмат_урнаштыру++;return мәгълүмат_урнаштыру-юл_мәгълүмат;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t элемент_COUNT){while(элемент_COUNT--){unsigned char X_координатасы=*첫째값++,세로좌표=*SECOND_VALUE++;if(X_координатасы!=세로좌표)return X_координатасы-세로좌표;if(!X_координатасы)return 0;}return 0;}
char *strcpy(char*күчерү_урыны_мәгълүмат,const char*юл_мәгълүмат){char*반환값=күчерү_урыны_мәгълүмат;while((*күчерү_урыны_мәгълүмат++=*юл_мәгълүмат++)){}return 반환값;}
char *strchr(const char*юл_мәгълүмат,int символ_коды){do{if(*юл_мәгълүмат==(char)символ_коды)return (char*)юл_мәгълүмат;}while(*юл_мәгълүмат++);return 0;}
char *strrchr(const char*юл_мәгълүмат,int символ_коды){const char*반환값=0;do{if(*юл_мәгълүмат==(char)символ_коды)반환값=юл_мәгълүмат;}while(*юл_мәгълүмат++);return (char*)반환값;}
char *strstr(const char*юл_мәгълүмат,const char*Терминал_кертү){size_t элемент_COUNT=strlen(Терминал_кертү);for(;*юл_мәгълүмат;юл_мәгълүмат++)if(!strncmp(юл_мәгълүмат,Терминал_кертү,элемент_COUNT))return (char*)юл_мәгълүмат;return элемент_COUNT?0:(char*)юл_мәгълүмат;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t элемент_COUNT){const unsigned char*X_координатасы=첫째값,*세로좌표=SECOND_VALUE;while(элемент_COUNT--){if(*X_координатасы!=*세로좌표)return *X_координатасы-*세로좌표;X_координатасы++;세로좌표++;}return 0;}
void *memmove(void*күчерү_урыны_мәгълүмат,const void*юл_мәгълүмат,size_t элемент_COUNT){unsigned char*X_координатасы=күчерү_урыны_мәгълүмат;const unsigned char*세로좌표=юл_мәгълүмат;if(X_координатасы<세로좌표){for(size_t 순번=0;순번<элемент_COUNT;순번++)X_координатасы[순번]=세로좌표[순번];}else while(элемент_COUNT){элемент_COUNT--;X_координатасы[элемент_COUNT]=세로좌표[элемент_COUNT];}return күчерү_урыны_мәгълүмат;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct мәгълүмат_тыю {size_t үлчәмен_үзгәртү;struct мәгълүмат_тыю*Киләсе_элемент;int 남은공간;int 채울크기;uint64_t тигезләү_дәрес;} мәгълүмат_тыю;
static мәгълүмат_тыю *첫항목;
void free(void*мәгълүмат_урнаштыру){if(!мәгълүмат_урнаштыру)return;мәгълүмат_тыю*SECOND_VALUE=(мәгълүмат_тыю*)мәгълүмат_урнаштыру-1;SECOND_VALUE->남은공간=1;for(мәгълүмат_тыю*Киләсе_OFFSET=첫항목;Киләсе_OFFSET&&Киләсе_OFFSET->Киләсе_элемент;){if(Киләсе_OFFSET->남은공간&&Киләсе_OFFSET->Киләсе_элемент->남은공간){Киләсе_OFFSET->үлчәмен_үзгәртү+=sizeof(мәгълүмат_тыю)+Киләсе_OFFSET->Киләсе_элемент->үлчәмен_үзгәртү;Киләсе_OFFSET->Киләсе_элемент=Киләсе_OFFSET->Киләсе_элемент->Киләсе_элемент;}else Киләсе_OFFSET=Киләсе_OFFSET->Киләсе_элемент;}}
void *realloc(void*мәгълүмат_урнаштыру,size_t элемент_COUNT){
    if(!элемент_COUNT){free(мәгълүмат_урнаштыру);return 0;}if(элемент_COUNT>sizeof(할당마당)-sizeof(мәгълүмат_тыю))return 0;элемент_COUNT=(элемент_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(мәгълүмат_тыю*)할당마당;첫항목->үлчәмен_үзгәртү=sizeof(할당마당)-sizeof(мәгълүмат_тыю);첫항목->남은공간=1;첫항목->Киләсе_элемент=0;}
    мәгълүмат_тыю*이전=мәгълүмат_урнаштыру?(мәгълүмат_тыю*)мәгълүмат_урнаштыру-1:0;if(이전&&이전->үлчәмен_үзгәртү>=элемент_COUNT)return мәгълүмат_урнаштыру;
    for(мәгълүмат_тыю*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Киләсе_элемент)if(SECOND_VALUE->남은공간&&SECOND_VALUE->үлчәмен_үзгәртү>=элемент_COUNT){
        if(SECOND_VALUE->үлчәмен_үзгәртү>=элемент_COUNT+sizeof(мәгълүмат_тыю)+16){мәгълүмат_тыю*나머지부분=(мәгълүмат_тыю*)((unsigned char*)(SECOND_VALUE+1)+элемент_COUNT);나머지부분->үлчәмен_үзгәртү=SECOND_VALUE->үлчәмен_үзгәртү-элемент_COUNT-sizeof(мәгълүмат_тыю);나머지부분->Киләсе_элемент=SECOND_VALUE->Киләсе_элемент;나머지부분->남은공간=1;SECOND_VALUE->Киләсе_элемент=나머지부분;SECOND_VALUE->үлчәмен_үзгәртү=элемент_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,мәгълүмат_урнаштыру,이전->үлчәмен_үзгәртү);free(мәгълүмат_урнаштыру);}return 반환값;
    }Хата=12;return 0;
}
void *malloc(size_t элемент_COUNT){return realloc(0,элемент_COUNT);}
void *calloc(size_t элемент_COUNT,size_t юл_мәгълүмат){if(юл_мәгълүмат&&элемент_COUNT>SIZE_MAX/юл_мәгълүмат)return 0;void*мәгълүмат_урнаштыру=malloc(элемент_COUNT*юл_мәгълүмат);if(мәгълүмат_урнаштыру)memset(мәгълүмат_урнаштыру,0,элемент_COUNT*юл_мәгълүмат);return мәгълүмат_урнаштыру;}
unsigned long long strtoull(const char*юл_мәгълүмат,char**тәмамлау_OFFSET,int Фон_VALUE){
    const char*Start_OFFSET=юл_мәгълүмат;while(*юл_мәгълүмат==' '||(*юл_мәгълүмат>=9&&*юл_мәгълүмат<=13))юл_мәгълүмат++;int 음수여부=0;if(*юл_мәгълүмат=='-'||*юл_мәгълүмат=='+')음수여부=*юл_мәгълүмат++=='-';
    if((!Фон_VALUE||Фон_VALUE==16)&&юл_мәгълүмат[0]=='0'&&(юл_мәгълүмат[1]=='x'||юл_мәгълүмат[1]=='X')){Фон_VALUE=16;юл_мәгълүмат+=2;}if(!Фон_VALUE)Фон_VALUE=*юл_мәгълүмат=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned символ_коды=*юл_мәгълүмат,күчерү_урыны_мәгълүмат=символ_коды>='0'&&символ_коды<='9'?символ_коды-'0':символ_коды>='a'&&символ_коды<='z'?символ_коды-'a'+10:символ_коды>='A'&&символ_коды<='Z'?символ_коды-'A'+10:99;if(күчерү_урыны_мәгълүмат>=(unsigned)Фон_VALUE)break;하나라도=1;юл_мәгълүмат++;if(임시값>(~0ull-күчерү_урыны_мәгълүмат)/(unsigned)Фон_VALUE){임시값=~0ull;Хата=34;}else 임시값=임시값*Фон_VALUE+күчерү_урыны_мәгълүмат;}
    if(тәмамлау_OFFSET)*тәмамлау_OFFSET=(char*)(하나라도?юл_мәгълүмат:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*юл_мәгълүмат,char**보조항목,int SECOND_VALUE){return strtoull(юл_мәгълүмат,보조항목,SECOND_VALUE);}
long strtol(const char*юл_мәгълүмат,char**보조항목,int SECOND_VALUE){return (long)strtoull(юл_мәгълүмат,보조항목,SECOND_VALUE);}
int atoi(const char*юл_мәгълүмат){return (int)strtol(юл_мәгълүмат,0,10);}
long double ldexpl(long double X_координатасы,int элемент_COUNT){while(элемент_COUNT>0){X_координатасы*=2;элемент_COUNT--;}while(элемент_COUNT<0){X_координатасы/=2;элемент_COUNT++;}return X_координатасы;}
long double strtold(const char*юл_мәгълүмат,char**тәмамлау_OFFSET){
    const char*Start_OFFSET=юл_мәгълүмат;while(*юл_мәгълүмат==' '||(*юл_мәгълүмат>=9&&*юл_мәгълүмат<=13))юл_мәгълүмат++;int 음수여부=0;if(*юл_мәгълүмат=='-'||*юл_мәгълүмат=='+')음수여부=*юл_мәгълүмат++=='-';
    int Фон_VALUE=10;if(юл_мәгълүмат[0]=='0'&&(юл_мәгълүмат[1]=='x'||юл_мәгълүмат[1]=='X')){Фон_VALUE=16;юл_мәгълүмат+=2;}long double 임시값=0,масштаблау=1;int 소수부=0,하나라도=0;
    for(;;){int символ_коды=*юл_мәгълүмат,күчерү_урыны_мәгълүмат=символ_коды>='0'&&символ_коды<='9'?символ_коды-'0':символ_коды>='a'&&символ_коды<='f'?символ_коды-'a'+10:символ_коды>='A'&&символ_коды<='F'?символ_коды-'A'+10:99;
        if(символ_коды=='.'&&!소수부){소수부=1;юл_мәгълүмат++;continue;}if(күчерү_урыны_мәгълүмат>=Фон_VALUE)break;하나라도=1;юл_мәгълүмат++;임시값=임시값*Фон_VALUE+күчерү_урыны_мәгълүмат;if(소수부)масштаблау*=Фон_VALUE;
    }임시값/=масштаблау;
    if((Фон_VALUE==10&&(*юл_мәгълүмат=='e'||*юл_мәгълүмат=='E'))||(Фон_VALUE==16&&(*юл_мәгълүмат=='p'||*юл_мәгълүмат=='P'))){const char*күрсәтү_VALUE=юл_мәгълүмат++;int 빼기=0;if(*юл_мәгълүмат=='-'||*юл_мәгълүмат=='+')빼기=*юл_мәгълүмат++=='-';int элемент_COUNT=0,кертү_COUNT=0;while(*юл_мәгълүмат>='0'&&*юл_мәгълүмат<='9'){кертү_COUNT++;if(элемент_COUNT<20000)элемент_COUNT=элемент_COUNT*10+*юл_мәгълүмат-'0';юл_мәгълүмат++;}if(!кертү_COUNT)юл_мәгълүмат=күрсәтү_VALUE;else{long double тапкырлаучы=Фон_VALUE==16?2:10;while(элемент_COUNT-->0&&элемент_COUNT<200000)임시값=빼기?임시값/тапкырлаучы:임시값*тапкырлаучы;}}
    if(тәмамлау_OFFSET)*тәмамлау_OFFSET=(char*)(하나라도?юл_мәгълүмат:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*юл_мәгълүмат,char**보조항목){return (double)strtold(юл_мәгълүмат,보조항목);}float strtof(const char*юл_мәгълүмат,char**보조항목){return (float)strtold(юл_мәгълүмат,보조항목);}
void qsort(void*Фон_VALUE,size_t элемент_COUNT,size_t үлчәмен_үзгәртү,int(*Чагыштыру)(const void*,const void*)){
    unsigned char*мәгълүмат_урнаштыру=Фон_VALUE;for(size_t 순번=1;순번<элемент_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Чагыштыру(мәгълүмат_урнаштыру+(안쪽순번-1)*үлчәмен_үзгәртү,мәгълүмат_урнаштыру+안쪽순번*үлчәмен_үзгәртү)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<үлчәмен_үзгәртү;셋째순번++){unsigned char символ_коды=мәгълүмат_урнаштыру[(안쪽순번-1)*үлчәмен_үзгәртү+셋째순번];мәгълүмат_урнаштыру[(안쪽순번-1)*үлчәмен_үзгәртү+셋째순번]=мәгълүмат_урнаштыру[안쪽순번*үлчәмен_үзгәртү+셋째순번];мәгълүмат_урнаштыру[안쪽순번*үлчәмен_үзгәртү+셋째순번]=символ_коды;}
}
static struct {int 사용량,Эзләү_INDEX;size_t урнаштыру;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *элемент_COUNT){*элемент_COUNT=출력크기;return 출력결과;}
int open(const char*исем,int 설정비트,...){
    if(!strcmp(исем,"/@cc-output")){if(출력열림){Хата=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(исем,번역기자원들[순번].исем)){
        if(설정비트&3){Хата=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].Эзләү_INDEX=순번;열림[안쪽순번].урнаштыру=0;return 128+안쪽순번;}Хата=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)исем,설정비트,0,0,0,0);if(반환값<0){Хата=-반환값;return -1;}return 반환값;
}
int close(int файл_дескриптор){if(файл_дескриптор==100){출력열림=0;return 0;}if(файл_дескриптор>=128&&файл_дескриптор<152){열림[файл_дескриптор-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,файл_дескриптор,0,0,0,0,0);if(반환값<0){Хата=-반환값;return -1;}return 0;}
long read(int файл_дескриптор,void*мәгълүмат,size_t элемент_COUNT){
    if(файл_дескриптор>=128&&файл_дескриптор<152&&열림[файл_дескриптор-128].사용량){int 순번=файл_дескриптор-128;const 번역기자원*반환값=&번역기자원들[열림[순번].Эзләү_INDEX];size_t 왼쪽=반환값->үлчәмен_үзгәртү-열림[순번].урнаштыру;if(элемент_COUNT>왼쪽)элемент_COUNT=왼쪽;memcpy(мәгълүмат,반환값->мәгълүмат+열림[순번].урнаштыру,элемент_COUNT);열림[순번].урнаштыру+=элемент_COUNT;return элемент_COUNT;}
    intptr_t 반환값=사용자호출(2,файл_дескриптор,(uintptr_t)мәгълүмат,элемент_COUNT,0,0,0);if(반환값<0){Хата=-반환값;return -1;}return 반환값;
}
long write(int файл_дескриптор,const void*мәгълүмат,size_t элемент_COUNT){
    if(файл_дескриптор==100){if(элемент_COUNT>sizeof(출력결과)-출력위치){Хата=28;return -1;}memcpy(출력결과+출력위치,мәгълүмат,элемент_COUNT);출력위치+=элемент_COUNT;if(출력크기<출력위치)출력크기=출력위치;return элемент_COUNT;}
    intptr_t 반환값=사용자호출(1,файл_дескриптор,(uintptr_t)мәгълүмат,элемент_COUNT,0,0,0);if(반환값<0){Хата=-반환값;return -1;}return 반환값;
}
long lseek(int файл_дескриптор,long OFFSET_VALUE,int 기준점){
    if(файл_дескриптор==100){long мәгълүмат_урнаштыру=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(мәгълүмат_урнаштыру<0||(size_t)мәгълүмат_урнаштыру>sizeof(출력결과)){Хата=22;return -1;}출력위치=мәгълүмат_урнаштыру;return мәгълүмат_урнаштыру;}
    if(файл_дескриптор>=128&&файл_дескриптор<152&&열림[файл_дескриптор-128].사용량){int 순번=файл_дескриптор-128;long мәгълүмат_урнаштыру=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].урнаштыру:번역기자원들[열림[순번].Эзләү_INDEX].үлчәмен_үзгәртү);if(мәгълүмат_урнаштыру<0||(size_t)мәгълүмат_урнаштыру>번역기자원들[열림[순번].Эзләү_INDEX].үлчәмен_үзгәртү){Хата=22;return -1;}열림[순번].урнаштыру=мәгълүмат_урнаштыру;return мәгълүмат_урнаштыру;}
    intptr_t 반환값=사용자호출(5,файл_дескриптор,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){Хата=-반환값;return -1;}return 반환값;
}
int unlink(const char*исем){intptr_t 반환값=사용자호출(11,(uintptr_t)исем,0,0,0,0,0);if(반환값<0){Хата=-반환값;return -1;}return 반환값;}
char *realpath(const char*исем,char*үлчәм_мәгълүмат){if(!үлчәм_мәгълүмат){үлчәм_мәгълүмат=malloc(strlen(исем)+1);if(!үлчәм_мәгълүмат)return 0;}return strcpy(үлчәм_мәгълүмат,исем);}
char *getcwd(char*мәгълүмат_урнаштыру,size_t элемент_COUNT){if(элемент_COUNT<2){Хата=34;return 0;}мәгълүмат_урнаштыру[0]='/';мәгълүмат_урнаштыру[1]=0;return мәгълүмат_урнаштыру;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Терминал_кертү){time_t 임시값=0;if(Терминал_кертү)*Терминал_кертү=임시값;return 임시값;}
struct tm *localtime(const time_t*Терминал_кертү){(void)Терминал_кертү;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int файл_дескриптор,const char*ысул_MODE){(void)ысул_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Хата=0;흐름목록[순번].файл_дескриптор=файл_дескриптор;return &흐름목록[순번];}Хата=24;return 0;}
int fflush(FILE*файл_кертү){return файл_кертү&&файл_кертү->Хата?-1:0;}
int fclose(FILE*файл_кертү){int 반환값=close(файл_кертү->файл_дескриптор);if(файл_кертү->Хата)반환값=-1;файл_кертү->사용량=0;return 반환값;}
size_t fwrite(const void*мәгълүмат_урнаштыру,size_t юл_мәгълүмат,size_t элемент_COUNT,FILE*файл_кертү){if(!юл_мәгълүмат)return 0;if(элемент_COUNT>SIZE_MAX/юл_мәгълүмат){файл_кертү->Хата=1;return 0;}long 반환값=write(файл_кертү->файл_дескриптор,мәгълүмат_урнаштыру,юл_мәгълүмат*элемент_COUNT);if(반환값<0){файл_кертү->Хата=1;return 0;}return (size_t)반환값/юл_мәгълүмат;}
int fputc(int символ_коды,FILE*файл_кертү){unsigned char SECOND_VALUE=символ_коды;return fwrite(&SECOND_VALUE,1,1,файл_кертү)==1?SECOND_VALUE:EOF;}
int fputs(const char*юл_мәгълүмат,FILE*файл_кертү){return fwrite(юл_мәгълүмат,1,strlen(юл_мәгълүмат),файл_кертү)==strlen(юл_мәгълүмат)?0:EOF;}
static void 넣기(char*үлчәм_мәгълүмат,size_t 용량한도,size_t*현재위치,char символ_коды){if(*현재위치+1<용량한도)үлчәм_мәгълүмат[*현재위치]=символ_коды;(*현재위치)++;}
int vsnprintf(char*үлчәм_мәгълүмат,size_t 용량한도,const char*формат,va_list 가변인수){
    size_t 현재위치=0;while(*формат){if(*формат!='%'){넣기(үлчәм_мәгълүмат,용량한도,&현재위치,*формат++);continue;}формат++;
        int 왼쪽=0,영값=0,대체값=0;while(*формат=='-'||*формат=='0'||*формат=='#'||*формат=='+'||*формат==' '){if(*формат=='-')왼쪽=1;if(*формат=='0')영값=1;if(*формат=='#')대체값=1;формат++;}
        int 너비=0,정밀도=-1;if(*формат=='*'){너비=va_arg(가변인수,int);формат++;}else while(*формат>='0'&&*формат<='9')너비=너비*10+*формат++-'0';
        if(*формат=='.'){формат++;정밀도=0;if(*формат=='*'){정밀도=va_arg(가변인수,int);формат++;}else while(*формат>='0'&&*формат<='9')정밀도=정밀도*10+*формат++-'0';}
        int 넓은글자=0;while(*формат=='l'||*формат=='z'||*формат=='t'||*формат=='j'||*формат=='h'){if(*формат!='h')넓은글자=1;формат++;}
        char TYPE_категория=*формат?*формат++:0,буфер_Саклагыч[80];const char*юл_мәгълүмат=буфер_Саклагыч;size_t элемент_COUNT=0;
        if(TYPE_категория=='s'){юл_мәгълүмат=va_arg(가변인수,const char*);if(!юл_мәгълүмат)юл_мәгълүмат="(null)";элемент_COUNT=strlen(юл_мәгълүмат);if(정밀도>=0&&элемент_COUNT>(size_t)정밀도)элемент_COUNT=정밀도;}
        else if(TYPE_категория=='c'){буфер_Саклагыч[0]=va_arg(가변인수,int);элемент_COUNT=1;}
        else if(TYPE_категория=='%'){буфер_Саклагыч[0]='%';элемент_COUNT=1;}
        else if(TYPE_категория=='d'||TYPE_категория=='i'||TYPE_категория=='u'||TYPE_категория=='x'||TYPE_категория=='X'||TYPE_категория=='o'||TYPE_категория=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_категория=='d'||TYPE_категория=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_категория=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Фон_VALUE=TYPE_категория=='x'||TYPE_категория=='X'||TYPE_категория=='p'?16:TYPE_категория=='o'?8:10;char сан_COUNT[64];unsigned 사용량=0;
            do{сан_COUNT[사용량++]="0123456789abcdef"[VALUE%Фон_VALUE];VALUE/=Фон_VALUE;}while(VALUE);
            if(음수표시)буфер_Саклагыч[элемент_COUNT++]='-';if(TYPE_категория=='p'||(대체값&&Фон_VALUE==16)){буфер_Саклагыч[элемент_COUNT++]='0';буфер_Саклагыч[элемент_COUNT++]='x';}
            for(int буяу_VALUE=(int)사용량;정밀도>буяу_VALUE&&элемент_COUNT<sizeof(буфер_Саклагыч)-사용량;буяу_VALUE++)буфер_Саклагыч[элемент_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(элемент_COUNT+사용량)&&элемент_COUNT<sizeof(буфер_Саклагыч)-사용량)буфер_Саклагыч[элемент_COUNT++]='0';
            while(사용량)буфер_Саклагыч[элемент_COUNT++]=сан_COUNT[--사용량];
        }else{буфер_Саклагыч[0]='?';элемент_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)элемент_COUNT){넣기(үлчәм_мәгълүмат,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<элемент_COUNT;순번++)넣기(үлчәм_мәгълүмат,용량한도,&현재위치,юл_мәгълүмат[순번]);while(왼쪽&&너비>(int)элемент_COUNT){넣기(үлчәм_мәгълүмат,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)үлчәм_мәгълүмат[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*үлчәм_мәгълүмат,size_t 용량한도,const char*файл_кертү,...){va_list 첫째값;va_start(첫째값,файл_кертү);int 반환값=vsnprintf(үлчәм_мәгълүмат,용량한도,файл_кертү,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*үлчәм_мәгълүмат,const char*файл_кертү,...){va_list 첫째값;va_start(첫째값,файл_кертү);int 반환값=vsnprintf(үлчәм_мәгълүмат,SIZE_MAX,файл_кертү,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*агым_VALUE,const char*файл_кертү,va_list 첫째값){char SECOND_VALUE[2048];int элемент_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),файл_кертү,첫째값);if(элемент_COUNT>2047)элемент_COUNT=2047;return fwrite(SECOND_VALUE,1,элемент_COUNT,агым_VALUE)==(size_t)элемент_COUNT?элемент_COUNT:-1;}
int fprintf(FILE*агым_VALUE,const char*файл_кертү,...){va_list 첫째값;va_start(첫째값,файл_кертү);int 반환값=vfprintf(агым_VALUE,файл_кертү,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*файл_кертү,...){va_list 첫째값;va_start(첫째값,файл_кертү);int 반환값=vfprintf(stdout,файл_кертү,첫째값);va_end(첫째값);return 반환값;}
