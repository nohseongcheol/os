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
static int ГРЕШКА;
int *__errno_location(void){return &ГРЕШКА;}
void exit(int статус_VALUE){사용자호출(6,статус_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *провери_израз,const char *Датотека,unsigned ред,const char *метод_внес_име){fprintf(stderr,"cc assertion: %s %s:%u %s\n",провери_израз,Датотека,ред,метод_внес_име);exit(1);}
size_t strlen(const char*низа_податоци){const char*податоци_позиционирање=низа_податоци;while(*податоци_позиционирање)податоци_позиционирање++;return податоци_позиционирање-низа_податоци;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t ставка_COUNT){while(ставка_COUNT--){unsigned char координата_х=*첫째값++,세로좌표=*SECOND_VALUE++;if(координата_х!=세로좌표)return координата_х-세로좌표;if(!координата_х)return 0;}return 0;}
char *strcpy(char*одредиште_податоци,const char*низа_податоци){char*반환값=одредиште_податоци;while((*одредиште_податоци++=*низа_податоци++)){}return 반환값;}
char *strchr(const char*низа_податоци,int кодна_точка){do{if(*низа_податоци==(char)кодна_точка)return (char*)низа_податоци;}while(*низа_податоци++);return 0;}
char *strrchr(const char*низа_податоци,int кодна_точка){const char*반환값=0;do{if(*низа_податоци==(char)кодна_точка)반환값=низа_податоци;}while(*низа_податоци++);return (char*)반환값;}
char *strstr(const char*низа_податоци,const char*Терминал_внес){size_t ставка_COUNT=strlen(Терминал_внес);for(;*низа_податоци;низа_податоци++)if(!strncmp(низа_податоци,Терминал_внес,ставка_COUNT))return (char*)низа_податоци;return ставка_COUNT?0:(char*)низа_податоци;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t ставка_COUNT){const unsigned char*координата_х=첫째값,*세로좌표=SECOND_VALUE;while(ставка_COUNT--){if(*координата_х!=*세로좌표)return *координата_х-*세로좌표;координата_х++;세로좌표++;}return 0;}
void *memmove(void*одредиште_податоци,const void*низа_податоци,size_t ставка_COUNT){unsigned char*координата_х=одредиште_податоци;const unsigned char*세로좌표=низа_податоци;if(координата_х<세로좌표){for(size_t 순번=0;순번<ставка_COUNT;순번++)координата_х[순번]=세로좌표[순번];}else while(ставка_COUNT){ставка_COUNT--;координата_х[ставка_COUNT]=세로좌표[ставка_COUNT];}return одредиште_податоци;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct податоци_блокирај {size_t Големина;struct податоци_блокирај*Следно_ставка;int 남은공간;int 채울크기;uint64_t порамнување_единици;} податоци_блокирај;
static податоци_блокирај *첫항목;
void free(void*податоци_позиционирање){if(!податоци_позиционирање)return;податоци_блокирај*SECOND_VALUE=(податоци_блокирај*)податоци_позиционирање-1;SECOND_VALUE->남은공간=1;for(податоци_блокирај*Следно_OFFSET=첫항목;Следно_OFFSET&&Следно_OFFSET->Следно_ставка;){if(Следно_OFFSET->남은공간&&Следно_OFFSET->Следно_ставка->남은공간){Следно_OFFSET->Големина+=sizeof(податоци_блокирај)+Следно_OFFSET->Следно_ставка->Големина;Следно_OFFSET->Следно_ставка=Следно_OFFSET->Следно_ставка->Следно_ставка;}else Следно_OFFSET=Следно_OFFSET->Следно_ставка;}}
void *realloc(void*податоци_позиционирање,size_t ставка_COUNT){
    if(!ставка_COUNT){free(податоци_позиционирање);return 0;}if(ставка_COUNT>sizeof(할당마당)-sizeof(податоци_блокирај))return 0;ставка_COUNT=(ставка_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(податоци_блокирај*)할당마당;첫항목->Големина=sizeof(할당마당)-sizeof(податоци_блокирај);첫항목->남은공간=1;첫항목->Следно_ставка=0;}
    податоци_блокирај*이전=податоци_позиционирање?(податоци_блокирај*)податоци_позиционирање-1:0;if(이전&&이전->Големина>=ставка_COUNT)return податоци_позиционирање;
    for(податоци_блокирај*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Следно_ставка)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Големина>=ставка_COUNT){
        if(SECOND_VALUE->Големина>=ставка_COUNT+sizeof(податоци_блокирај)+16){податоци_блокирај*나머지부분=(податоци_блокирај*)((unsigned char*)(SECOND_VALUE+1)+ставка_COUNT);나머지부분->Големина=SECOND_VALUE->Големина-ставка_COUNT-sizeof(податоци_блокирај);나머지부분->Следно_ставка=SECOND_VALUE->Следно_ставка;나머지부분->남은공간=1;SECOND_VALUE->Следно_ставка=나머지부분;SECOND_VALUE->Големина=ставка_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,податоци_позиционирање,이전->Големина);free(податоци_позиционирање);}return 반환값;
    }ГРЕШКА=12;return 0;
}
void *malloc(size_t ставка_COUNT){return realloc(0,ставка_COUNT);}
void *calloc(size_t ставка_COUNT,size_t низа_податоци){if(низа_податоци&&ставка_COUNT>SIZE_MAX/низа_податоци)return 0;void*податоци_позиционирање=malloc(ставка_COUNT*низа_податоци);if(податоци_позиционирање)memset(податоци_позиционирање,0,ставка_COUNT*низа_податоци);return податоци_позиционирање;}
unsigned long long strtoull(const char*низа_податоци,char**крај_OFFSET,int тапет_VALUE){
    const char*Start_OFFSET=низа_податоци;while(*низа_податоци==' '||(*низа_податоци>=9&&*низа_податоци<=13))низа_податоци++;int 음수여부=0;if(*низа_податоци=='-'||*низа_податоци=='+')음수여부=*низа_податоци++=='-';
    if((!тапет_VALUE||тапет_VALUE==16)&&низа_податоци[0]=='0'&&(низа_податоци[1]=='x'||низа_податоци[1]=='X')){тапет_VALUE=16;низа_податоци+=2;}if(!тапет_VALUE)тапет_VALUE=*низа_податоци=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned кодна_точка=*низа_податоци,одредиште_податоци=кодна_точка>='0'&&кодна_точка<='9'?кодна_точка-'0':кодна_точка>='a'&&кодна_точка<='z'?кодна_точка-'a'+10:кодна_точка>='A'&&кодна_точка<='Z'?кодна_точка-'A'+10:99;if(одредиште_податоци>=(unsigned)тапет_VALUE)break;하나라도=1;низа_податоци++;if(임시값>(~0ull-одредиште_податоци)/(unsigned)тапет_VALUE){임시값=~0ull;ГРЕШКА=34;}else 임시값=임시값*тапет_VALUE+одредиште_податоци;}
    if(крај_OFFSET)*крај_OFFSET=(char*)(하나라도?низа_податоци:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*низа_податоци,char**보조항목,int SECOND_VALUE){return strtoull(низа_податоци,보조항목,SECOND_VALUE);}
long strtol(const char*низа_податоци,char**보조항목,int SECOND_VALUE){return (long)strtoull(низа_податоци,보조항목,SECOND_VALUE);}
int atoi(const char*низа_податоци){return (int)strtol(низа_податоци,0,10);}
long double ldexpl(long double координата_х,int ставка_COUNT){while(ставка_COUNT>0){координата_х*=2;ставка_COUNT--;}while(ставка_COUNT<0){координата_х/=2;ставка_COUNT++;}return координата_х;}
long double strtold(const char*низа_податоци,char**крај_OFFSET){
    const char*Start_OFFSET=низа_податоци;while(*низа_податоци==' '||(*низа_податоци>=9&&*низа_податоци<=13))низа_податоци++;int 음수여부=0;if(*низа_податоци=='-'||*низа_податоци=='+')음수여부=*низа_податоци++=='-';
    int тапет_VALUE=10;if(низа_податоци[0]=='0'&&(низа_податоци[1]=='x'||низа_податоци[1]=='X')){тапет_VALUE=16;низа_податоци+=2;}long double 임시값=0,скалира=1;int 소수부=0,하나라도=0;
    for(;;){int кодна_точка=*низа_податоци,одредиште_податоци=кодна_точка>='0'&&кодна_точка<='9'?кодна_точка-'0':кодна_точка>='a'&&кодна_точка<='f'?кодна_точка-'a'+10:кодна_точка>='A'&&кодна_точка<='F'?кодна_точка-'A'+10:99;
        if(кодна_точка=='.'&&!소수부){소수부=1;низа_податоци++;continue;}if(одредиште_податоци>=тапет_VALUE)break;하나라도=1;низа_податоци++;임시값=임시값*тапет_VALUE+одредиште_податоци;if(소수부)скалира*=тапет_VALUE;
    }임시값/=скалира;
    if((тапет_VALUE==10&&(*низа_податоци=='e'||*низа_податоци=='E'))||(тапет_VALUE==16&&(*низа_податоци=='p'||*низа_податоци=='P'))){const char*прикажи_VALUE=низа_податоци++;int 빼기=0;if(*низа_податоци=='-'||*низа_податоци=='+')빼기=*низа_податоци++=='-';int ставка_COUNT=0,внес_COUNT=0;while(*низа_податоци>='0'&&*низа_податоци<='9'){внес_COUNT++;if(ставка_COUNT<20000)ставка_COUNT=ставка_COUNT*10+*низа_податоци-'0';низа_податоци++;}if(!внес_COUNT)низа_податоци=прикажи_VALUE;else{long double фактор=тапет_VALUE==16?2:10;while(ставка_COUNT-->0&&ставка_COUNT<200000)임시값=빼기?임시값/фактор:임시값*фактор;}}
    if(крај_OFFSET)*крај_OFFSET=(char*)(하나라도?низа_податоци:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*низа_податоци,char**보조항목){return (double)strtold(низа_податоци,보조항목);}float strtof(const char*низа_податоци,char**보조항목){return (float)strtold(низа_податоци,보조항목);}
void qsort(void*тапет_VALUE,size_t ставка_COUNT,size_t Големина,int(*Спореди)(const void*,const void*)){
    unsigned char*податоци_позиционирање=тапет_VALUE;for(size_t 순번=1;순번<ставка_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Спореди(податоци_позиционирање+(안쪽순번-1)*Големина,податоци_позиционирање+안쪽순번*Големина)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Големина;셋째순번++){unsigned char кодна_точка=податоци_позиционирање[(안쪽순번-1)*Големина+셋째순번];податоци_позиционирање[(안쪽순번-1)*Големина+셋째순번]=податоци_позиционирање[안쪽순번*Големина+셋째순번];податоци_позиционирање[안쪽순번*Големина+셋째순번]=кодна_точка;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Позиција;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *ставка_COUNT){*ставка_COUNT=출력크기;return 출력결과;}
int open(const char*Име,int конфигурација_Услуга_за_интелигентен_пренос_во_заднина,...){
    if(!strcmp(Име,"/@cc-output")){if(출력열림){ГРЕШКА=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Име,번역기자원들[순번].Име)){
        if(конфигурација_Услуга_за_интелигентен_пренос_во_заднина&3){ГРЕШКА=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Позиција=0;return 128+안쪽순번;}ГРЕШКА=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Име,конфигурација_Услуга_за_интелигентен_пренос_во_заднина,0,0,0,0);if(반환값<0){ГРЕШКА=-반환값;return -1;}return 반환값;
}
int close(int датотека_рачка){if(датотека_рачка==100){출력열림=0;return 0;}if(датотека_рачка>=128&&датотека_рачка<152){열림[датотека_рачка-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,датотека_рачка,0,0,0,0,0);if(반환값<0){ГРЕШКА=-반환값;return -1;}return 0;}
long read(int датотека_рачка,void*податоци,size_t ставка_COUNT){
    if(датотека_рачка>=128&&датотека_рачка<152&&열림[датотека_рачка-128].사용량){int 순번=датотека_рачка-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Големина-열림[순번].Позиција;if(ставка_COUNT>왼쪽)ставка_COUNT=왼쪽;memcpy(податоци,반환값->податоци+열림[순번].Позиција,ставка_COUNT);열림[순번].Позиција+=ставка_COUNT;return ставка_COUNT;}
    intptr_t 반환값=사용자호출(2,датотека_рачка,(uintptr_t)податоци,ставка_COUNT,0,0,0);if(반환값<0){ГРЕШКА=-반환값;return -1;}return 반환값;
}
long write(int датотека_рачка,const void*податоци,size_t ставка_COUNT){
    if(датотека_рачка==100){if(ставка_COUNT>sizeof(출력결과)-출력위치){ГРЕШКА=28;return -1;}memcpy(출력결과+출력위치,податоци,ставка_COUNT);출력위치+=ставка_COUNT;if(출력크기<출력위치)출력크기=출력위치;return ставка_COUNT;}
    intptr_t 반환값=사용자호출(1,датотека_рачка,(uintptr_t)податоци,ставка_COUNT,0,0,0);if(반환값<0){ГРЕШКА=-반환값;return -1;}return 반환값;
}
long lseek(int датотека_рачка,long OFFSET_VALUE,int 기준점){
    if(датотека_рачка==100){long податоци_позиционирање=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(податоци_позиционирање<0||(size_t)податоци_позиционирање>sizeof(출력결과)){ГРЕШКА=22;return -1;}출력위치=податоци_позиционирање;return податоци_позиционирање;}
    if(датотека_рачка>=128&&датотека_рачка<152&&열림[датотека_рачка-128].사용량){int 순번=датотека_рачка-128;long податоци_позиционирање=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].Позиција:번역기자원들[열림[순번].LOOKUP_INDEX].Големина);if(податоци_позиционирање<0||(size_t)податоци_позиционирање>번역기자원들[열림[순번].LOOKUP_INDEX].Големина){ГРЕШКА=22;return -1;}열림[순번].Позиција=податоци_позиционирање;return податоци_позиционирање;}
    intptr_t 반환값=사용자호출(5,датотека_рачка,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){ГРЕШКА=-반환값;return -1;}return 반환값;
}
int unlink(const char*Име){intptr_t 반환값=사용자호출(11,(uintptr_t)Име,0,0,0,0,0);if(반환값<0){ГРЕШКА=-반환값;return -1;}return 반환값;}
char *realpath(const char*Име,char*мерка_податоци){if(!мерка_податоци){мерка_податоци=malloc(strlen(Име)+1);if(!мерка_податоци)return 0;}return strcpy(мерка_податоци,Име);}
char *getcwd(char*податоци_позиционирање,size_t ставка_COUNT){if(ставка_COUNT<2){ГРЕШКА=34;return 0;}податоци_позиционирање[0]='/';податоци_позиционирање[1]=0;return податоци_позиционирање;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Терминал_внес){time_t 임시값=0;if(Терминал_внес)*Терминал_внес=임시값;return 임시값;}
struct tm *localtime(const time_t*Терминал_внес){(void)Терминал_внес;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int датотека_рачка,const char*метод_MODE){(void)метод_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].ГРЕШКА=0;흐름목록[순번].датотека_рачка=датотека_рачка;return &흐름목록[순번];}ГРЕШКА=24;return 0;}
int fflush(FILE*датотека_внес){return датотека_внес&&датотека_внес->ГРЕШКА?-1:0;}
int fclose(FILE*датотека_внес){int 반환값=close(датотека_внес->датотека_рачка);if(датотека_внес->ГРЕШКА)반환값=-1;датотека_внес->사용량=0;return 반환값;}
size_t fwrite(const void*податоци_позиционирање,size_t низа_податоци,size_t ставка_COUNT,FILE*датотека_внес){if(!низа_податоци)return 0;if(ставка_COUNT>SIZE_MAX/низа_податоци){датотека_внес->ГРЕШКА=1;return 0;}long 반환값=write(датотека_внес->датотека_рачка,податоци_позиционирање,низа_податоци*ставка_COUNT);if(반환값<0){датотека_внес->ГРЕШКА=1;return 0;}return (size_t)반환값/низа_податоци;}
int fputc(int кодна_точка,FILE*датотека_внес){unsigned char SECOND_VALUE=кодна_точка;return fwrite(&SECOND_VALUE,1,1,датотека_внес)==1?SECOND_VALUE:EOF;}
int fputs(const char*низа_податоци,FILE*датотека_внес){return fwrite(низа_податоци,1,strlen(низа_податоци),датотека_внес)==strlen(низа_податоци)?0:EOF;}
static void 넣기(char*мерка_податоци,size_t 용량한도,size_t*현재위치,char кодна_точка){if(*현재위치+1<용량한도)мерка_податоци[*현재위치]=кодна_точка;(*현재위치)++;}
int vsnprintf(char*мерка_податоци,size_t 용량한도,const char*формат,va_list 가변인수){
    size_t 현재위치=0;while(*формат){if(*формат!='%'){넣기(мерка_податоци,용량한도,&현재위치,*формат++);continue;}формат++;
        int 왼쪽=0,영값=0,대체값=0;while(*формат=='-'||*формат=='0'||*формат=='#'||*формат=='+'||*формат==' '){if(*формат=='-')왼쪽=1;if(*формат=='0')영값=1;if(*формат=='#')대체값=1;формат++;}
        int 너비=0,정밀도=-1;if(*формат=='*'){너비=va_arg(가변인수,int);формат++;}else while(*формат>='0'&&*формат<='9')너비=너비*10+*формат++-'0';
        if(*формат=='.'){формат++;정밀도=0;if(*формат=='*'){정밀도=va_arg(가변인수,int);формат++;}else while(*формат>='0'&&*формат<='9')정밀도=정밀도*10+*формат++-'0';}
        int 넓은글자=0;while(*формат=='l'||*формат=='z'||*формат=='t'||*формат=='j'||*формат=='h'){if(*формат!='h')넓은글자=1;формат++;}
        char TYPE_област=*формат?*формат++:0,меѓумеморија_Склад[80];const char*низа_податоци=меѓумеморија_Склад;size_t ставка_COUNT=0;
        if(TYPE_област=='s'){низа_податоци=va_arg(가변인수,const char*);if(!низа_податоци)низа_податоци="(null)";ставка_COUNT=strlen(низа_податоци);if(정밀도>=0&&ставка_COUNT>(size_t)정밀도)ставка_COUNT=정밀도;}
        else if(TYPE_област=='c'){меѓумеморија_Склад[0]=va_arg(가변인수,int);ставка_COUNT=1;}
        else if(TYPE_област=='%'){меѓумеморија_Склад[0]='%';ставка_COUNT=1;}
        else if(TYPE_област=='d'||TYPE_област=='i'||TYPE_област=='u'||TYPE_област=='x'||TYPE_област=='X'||TYPE_област=='o'||TYPE_област=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_област=='d'||TYPE_област=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_област=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned тапет_VALUE=TYPE_област=='x'||TYPE_област=='X'||TYPE_област=='p'?16:TYPE_област=='o'?8:10;char цифра_COUNT[64];unsigned 사용량=0;
            do{цифра_COUNT[사용량++]="0123456789abcdef"[VALUE%тапет_VALUE];VALUE/=тапет_VALUE;}while(VALUE);
            if(음수표시)меѓумеморија_Склад[ставка_COUNT++]='-';if(TYPE_област=='p'||(대체값&&тапет_VALUE==16)){меѓумеморија_Склад[ставка_COUNT++]='0';меѓумеморија_Склад[ставка_COUNT++]='x';}
            for(int исполни_VALUE=(int)사용량;정밀도>исполни_VALUE&&ставка_COUNT<sizeof(меѓумеморија_Склад)-사용량;исполни_VALUE++)меѓумеморија_Склад[ставка_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(ставка_COUNT+사용량)&&ставка_COUNT<sizeof(меѓумеморија_Склад)-사용량)меѓумеморија_Склад[ставка_COUNT++]='0';
            while(사용량)меѓумеморија_Склад[ставка_COUNT++]=цифра_COUNT[--사용량];
        }else{меѓумеморија_Склад[0]='?';ставка_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)ставка_COUNT){넣기(мерка_податоци,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<ставка_COUNT;순번++)넣기(мерка_податоци,용량한도,&현재위치,низа_податоци[순번]);while(왼쪽&&너비>(int)ставка_COUNT){넣기(мерка_податоци,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)мерка_податоци[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*мерка_податоци,size_t 용량한도,const char*датотека_внес,...){va_list 첫째값;va_start(첫째값,датотека_внес);int 반환값=vsnprintf(мерка_податоци,용량한도,датотека_внес,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*мерка_податоци,const char*датотека_внес,...){va_list 첫째값;va_start(첫째값,датотека_внес);int 반환값=vsnprintf(мерка_податоци,SIZE_MAX,датотека_внес,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*датотека_внес,va_list 첫째값){char SECOND_VALUE[2048];int ставка_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),датотека_внес,첫째값);if(ставка_COUNT>2047)ставка_COUNT=2047;return fwrite(SECOND_VALUE,1,ставка_COUNT,Stream_VALUE)==(size_t)ставка_COUNT?ставка_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*датотека_внес,...){va_list 첫째값;va_start(첫째값,датотека_внес);int 반환값=vfprintf(Stream_VALUE,датотека_внес,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*датотека_внес,...){va_list 첫째값;va_start(첫째값,датотека_внес);int 반환값=vfprintf(stdout,датотека_внес,첫째값);va_end(첫째값);return 반환값;}
