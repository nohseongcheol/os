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
static int ajachitia;
int *__errno_location(void){return &ajachitia;}
void exit(int jamakua_iparülein_ajutuu){사용자호출(6,jamakua_iparülein_ajutuu,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *cheeke_ajutukumajiaa,const char *anaajaalaa,unsigned liinia,const char *함수이름){fprintf(stderr,"cc assertion: %s %s:%u %s\n",cheeke_ajutukumajiaa,anaajaalaa,liinia,함수이름);exit(1);}
size_t strlen(const char*kaleena_atijaaya){const char*자료위치=kaleena_atijaaya;while(*자료위치)자료위치++;return 자료위치-kaleena_atijaaya;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char 가로좌표=*첫째값++,세로좌표=*둘째값++;if(가로좌표!=세로좌표)return 가로좌표-세로좌표;if(!가로좌표)return 0;}return 0;}
char *strcpy(char*jalamüinjatü_atijaaya,const char*kaleena_atijaaya){char*반환값=jalamüinjatü_atijaaya;while((*jalamüinjatü_atijaaya++=*kaleena_atijaaya++)){}return 반환값;}
char *strchr(const char*kaleena_atijaaya,int 문자값){do{if(*kaleena_atijaaya==(char)문자값)return (char*)kaleena_atijaaya;}while(*kaleena_atijaaya++);return 0;}
char *strrchr(const char*kaleena_atijaaya,int 문자값){const char*반환값=0;do{if(*kaleena_atijaaya==(char)문자값)반환값=kaleena_atijaaya;}while(*kaleena_atijaaya++);return (char*)반환값;}
char *strstr(const char*kaleena_atijaaya,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*kaleena_atijaaya;kaleena_atijaaya++)if(!strncmp(kaleena_atijaaya,터미널항목,개수))return (char*)kaleena_atijaaya;return 개수?0:(char*)kaleena_atijaaya;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*가로좌표=첫째값,*세로좌표=둘째값;while(개수--){if(*가로좌표!=*세로좌표)return *가로좌표-*세로좌표;가로좌표++;세로좌표++;}return 0;}
void *memmove(void*jalamüinjatü_atijaaya,const void*kaleena_atijaaya,size_t 개수){unsigned char*가로좌표=jalamüinjatü_atijaaya;const unsigned char*세로좌표=kaleena_atijaaya;if(가로좌표<세로좌표){for(size_t 순번=0;순번<개수;순번++)가로좌표[순번]=세로좌표[순번];}else while(개수){개수--;가로좌표[개수]=세로좌표[개수];}return jalamüinjatü_atijaaya;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct 자료덩이 {size_t 크기;struct 자료덩이*다음;int 남은공간;int 채울크기;uint64_t 맞춤단위;} 자료덩이;
static 자료덩이 *첫항목;
void free(void*자료위치){if(!자료위치)return;자료덩이*둘째값=(자료덩이*)자료위치-1;둘째값->남은공간=1;for(자료덩이*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->크기+=sizeof(자료덩이)+다음위치->다음->크기;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(자료덩이))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(자료덩이*)할당마당;첫항목->크기=sizeof(할당마당)-sizeof(자료덩이);첫항목->남은공간=1;첫항목->다음=0;}
    자료덩이*이전=자료위치?(자료덩이*)자료위치-1:0;if(이전&&이전->크기>=개수)return 자료위치;
    for(자료덩이*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->크기>=개수){
        if(둘째값->크기>=개수+sizeof(자료덩이)+16){자료덩이*나머지부분=(자료덩이*)((unsigned char*)(둘째값+1)+개수);나머지부분->크기=둘째값->크기-개수-sizeof(자료덩이);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->크기=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->크기);free(자료위치);}return 반환값;
    }ajachitia=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t kaleena_atijaaya){if(kaleena_atijaaya&&개수>SIZE_MAX/kaleena_atijaaya)return 0;void*자료위치=malloc(개수*kaleena_atijaaya);if(자료위치)memset(자료위치,0,개수*kaleena_atijaaya);return 자료위치;}
unsigned long long strtoull(const char*kaleena_atijaaya,char**끝위치,int apa_ajanaa_ajutuu){
    const char*시작위치=kaleena_atijaaya;while(*kaleena_atijaaya==' '||(*kaleena_atijaaya>=9&&*kaleena_atijaaya<=13))kaleena_atijaaya++;int 음수여부=0;if(*kaleena_atijaaya=='-'||*kaleena_atijaaya=='+')음수여부=*kaleena_atijaaya++=='-';
    if((!apa_ajanaa_ajutuu||apa_ajanaa_ajutuu==16)&&kaleena_atijaaya[0]=='0'&&(kaleena_atijaaya[1]=='x'||kaleena_atijaaya[1]=='X')){apa_ajanaa_ajutuu=16;kaleena_atijaaya+=2;}if(!apa_ajanaa_ajutuu)apa_ajanaa_ajutuu=*kaleena_atijaaya=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned 문자값=*kaleena_atijaaya,jalamüinjatü_atijaaya=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='z'?문자값-'a'+10:문자값>='A'&&문자값<='Z'?문자값-'A'+10:99;if(jalamüinjatü_atijaaya>=(unsigned)apa_ajanaa_ajutuu)break;하나라도=1;kaleena_atijaaya++;if(임시값>(~0ull-jalamüinjatü_atijaaya)/(unsigned)apa_ajanaa_ajutuu){임시값=~0ull;ajachitia=34;}else 임시값=임시값*apa_ajanaa_ajutuu+jalamüinjatü_atijaaya;}
    if(끝위치)*끝위치=(char*)(하나라도?kaleena_atijaaya:시작위치);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*kaleena_atijaaya,char**보조항목,int 둘째값){return strtoull(kaleena_atijaaya,보조항목,둘째값);}
long strtol(const char*kaleena_atijaaya,char**보조항목,int 둘째값){return (long)strtoull(kaleena_atijaaya,보조항목,둘째값);}
int atoi(const char*kaleena_atijaaya){return (int)strtol(kaleena_atijaaya,0,10);}
long double ldexpl(long double 가로좌표,int 개수){while(개수>0){가로좌표*=2;개수--;}while(개수<0){가로좌표/=2;개수++;}return 가로좌표;}
long double strtold(const char*kaleena_atijaaya,char**끝위치){
    const char*시작위치=kaleena_atijaaya;while(*kaleena_atijaaya==' '||(*kaleena_atijaaya>=9&&*kaleena_atijaaya<=13))kaleena_atijaaya++;int 음수여부=0;if(*kaleena_atijaaya=='-'||*kaleena_atijaaya=='+')음수여부=*kaleena_atijaaya++=='-';
    int apa_ajanaa_ajutuu=10;if(kaleena_atijaaya[0]=='0'&&(kaleena_atijaaya[1]=='x'||kaleena_atijaaya[1]=='X')){apa_ajanaa_ajutuu=16;kaleena_atijaaya+=2;}long double 임시값=0,anaataaja_apüin=1;int 소수부=0,하나라도=0;
    for(;;){int 문자값=*kaleena_atijaaya,jalamüinjatü_atijaaya=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='f'?문자값-'a'+10:문자값>='A'&&문자값<='F'?문자값-'A'+10:99;
        if(문자값=='.'&&!소수부){소수부=1;kaleena_atijaaya++;continue;}if(jalamüinjatü_atijaaya>=apa_ajanaa_ajutuu)break;하나라도=1;kaleena_atijaaya++;임시값=임시값*apa_ajanaa_ajutuu+jalamüinjatü_atijaaya;if(소수부)anaataaja_apüin*=apa_ajanaa_ajutuu;
    }임시값/=anaataaja_apüin;
    if((apa_ajanaa_ajutuu==10&&(*kaleena_atijaaya=='e'||*kaleena_atijaaya=='E'))||(apa_ajanaa_ajutuu==16&&(*kaleena_atijaaya=='p'||*kaleena_atijaaya=='P'))){const char*표시=kaleena_atijaaya++;int 빼기=0;if(*kaleena_atijaaya=='-'||*kaleena_atijaaya=='+')빼기=*kaleena_atijaaya++=='-';int 개수=0,항목수=0;while(*kaleena_atijaaya>='0'&&*kaleena_atijaaya<='9'){항목수++;if(개수<20000)개수=개수*10+*kaleena_atijaaya-'0';kaleena_atijaaya++;}if(!항목수)kaleena_atijaaya=표시;else{long double 배율=apa_ajanaa_ajutuu==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/배율:임시값*배율;}}
    if(끝위치)*끝위치=(char*)(하나라도?kaleena_atijaaya:시작위치);return 음수여부?-임시값:임시값;
}
double strtod(const char*kaleena_atijaaya,char**보조항목){return (double)strtold(kaleena_atijaaya,보조항목);}float strtof(const char*kaleena_atijaaya,char**보조항목){return (float)strtold(kaleena_atijaaya,보조항목);}
void qsort(void*apa_ajanaa_ajutuu,size_t 개수,size_t 크기,int(*ayoujire_eraa)(const void*,const void*)){
    unsigned char*자료위치=apa_ajanaa_ajutuu;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&ayoujire_eraa(자료위치+(안쪽순번-1)*크기,자료위치+안쪽순번*크기)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<크기;셋째순번++){unsigned char 문자값=자료위치[(안쪽순번-1)*크기+셋째순번];자료위치[(안쪽순번-1)*크기+셋째순번]=자료위치[안쪽순번*크기+셋째순번];자료위치[안쪽순번*크기+셋째순번]=문자값;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*이름,int 설정비트,...){
    if(!strcmp(이름,"/@cc-output")){if(출력열림){ajachitia=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(이름,번역기자원들[순번].이름)){
        if(설정비트&3){ajachitia=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}ajachitia=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)이름,설정비트,0,0,0,0);if(반환값<0){ajachitia=-반환값;return -1;}return 반환값;
}
int close(int anaajaalaa_aapaaya){if(anaajaalaa_aapaaya==100){출력열림=0;return 0;}if(anaajaalaa_aapaaya>=128&&anaajaalaa_aapaaya<152){열림[anaajaalaa_aapaaya-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,anaajaalaa_aapaaya,0,0,0,0,0);if(반환값<0){ajachitia=-반환값;return -1;}return 0;}
long read(int anaajaalaa_aapaaya,void*atijaaya,size_t 개수){
    if(anaajaalaa_aapaaya>=128&&anaajaalaa_aapaaya<152&&열림[anaajaalaa_aapaaya-128].사용량){int 순번=anaajaalaa_aapaaya-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->크기-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(atijaaya,반환값->atijaaya+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,anaajaalaa_aapaaya,(uintptr_t)atijaaya,개수,0,0,0);if(반환값<0){ajachitia=-반환값;return -1;}return 반환값;
}
long write(int anaajaalaa_aapaaya,const void*atijaaya,size_t 개수){
    if(anaajaalaa_aapaaya==100){if(개수>sizeof(출력결과)-출력위치){ajachitia=28;return -1;}memcpy(출력결과+출력위치,atijaaya,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,anaajaalaa_aapaaya,(uintptr_t)atijaaya,개수,0,0,0);if(반환값<0){ajachitia=-반환값;return -1;}return 반환값;
}
long lseek(int anaajaalaa_aapaaya,long 변위,int 기준점){
    if(anaajaalaa_aapaaya==100){long 자료위치=변위+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){ajachitia=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(anaajaalaa_aapaaya>=128&&anaajaalaa_aapaaya<152&&열림[anaajaalaa_aapaaya-128].사용량){int 순번=anaajaalaa_aapaaya-128;long 자료위치=변위+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].크기);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].크기){ajachitia=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,anaajaalaa_aapaaya,변위,기준점,0,0,0);if(반환값<0){ajachitia=-반환값;return -1;}return 반환값;
}
int unlink(const char*이름){intptr_t 반환값=사용자호출(11,(uintptr_t)이름,0,0,0,0,0);if(반환값<0){ajachitia=-반환값;return -1;}return 반환값;}
char *realpath(const char*이름,char*결과자료){if(!결과자료){결과자료=malloc(strlen(이름)+1);if(!결과자료)return 0;}return strcpy(결과자료,이름);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){ajachitia=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int anaajaalaa_aapaaya,const char*방식){(void)방식;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].ajachitia=0;흐름목록[순번].anaajaalaa_aapaaya=anaajaalaa_aapaaya;return &흐름목록[순번];}ajachitia=24;return 0;}
int fflush(FILE*anaajaalaa_ekeroliaa){return anaajaalaa_ekeroliaa&&anaajaalaa_ekeroliaa->ajachitia?-1:0;}
int fclose(FILE*anaajaalaa_ekeroliaa){int 반환값=close(anaajaalaa_ekeroliaa->anaajaalaa_aapaaya);if(anaajaalaa_ekeroliaa->ajachitia)반환값=-1;anaajaalaa_ekeroliaa->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t kaleena_atijaaya,size_t 개수,FILE*anaajaalaa_ekeroliaa){if(!kaleena_atijaaya)return 0;if(개수>SIZE_MAX/kaleena_atijaaya){anaajaalaa_ekeroliaa->ajachitia=1;return 0;}long 반환값=write(anaajaalaa_ekeroliaa->anaajaalaa_aapaaya,자료위치,kaleena_atijaaya*개수);if(반환값<0){anaajaalaa_ekeroliaa->ajachitia=1;return 0;}return (size_t)반환값/kaleena_atijaaya;}
int fputc(int 문자값,FILE*anaajaalaa_ekeroliaa){unsigned char 둘째값=문자값;return fwrite(&둘째값,1,1,anaajaalaa_ekeroliaa)==1?둘째값:EOF;}
int fputs(const char*kaleena_atijaaya,FILE*anaajaalaa_ekeroliaa){return fwrite(kaleena_atijaaya,1,strlen(kaleena_atijaaya),anaajaalaa_ekeroliaa)==strlen(kaleena_atijaaya)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char 문자값){if(*현재위치+1<용량한도)결과자료[*현재위치]=문자값;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*akua_ipaa,va_list 가변인수){
    size_t 현재위치=0;while(*akua_ipaa){if(*akua_ipaa!='%'){넣기(결과자료,용량한도,&현재위치,*akua_ipaa++);continue;}akua_ipaa++;
        int 왼쪽=0,영값=0,대체값=0;while(*akua_ipaa=='-'||*akua_ipaa=='0'||*akua_ipaa=='#'||*akua_ipaa=='+'||*akua_ipaa==' '){if(*akua_ipaa=='-')왼쪽=1;if(*akua_ipaa=='0')영값=1;if(*akua_ipaa=='#')대체값=1;akua_ipaa++;}
        int 너비=0,정밀도=-1;if(*akua_ipaa=='*'){너비=va_arg(가변인수,int);akua_ipaa++;}else while(*akua_ipaa>='0'&&*akua_ipaa<='9')너비=너비*10+*akua_ipaa++-'0';
        if(*akua_ipaa=='.'){akua_ipaa++;정밀도=0;if(*akua_ipaa=='*'){정밀도=va_arg(가변인수,int);akua_ipaa++;}else while(*akua_ipaa>='0'&&*akua_ipaa<='9')정밀도=정밀도*10+*akua_ipaa++-'0';}
        int 넓은글자=0;while(*akua_ipaa=='l'||*akua_ipaa=='z'||*akua_ipaa=='t'||*akua_ipaa=='j'||*akua_ipaa=='h'){if(*akua_ipaa!='h')넓은글자=1;akua_ipaa++;}
        char 유형=*akua_ipaa?*akua_ipaa++:0,완충공간[80];const char*kaleena_atijaaya=완충공간;size_t 개수=0;
        if(유형=='s'){kaleena_atijaaya=va_arg(가변인수,const char*);if(!kaleena_atijaaya)kaleena_atijaaya="(null)";개수=strlen(kaleena_atijaaya);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(유형=='c'){완충공간[0]=va_arg(가변인수,int);개수=1;}
        else if(유형=='%'){완충공간[0]='%';개수=1;}
        else if(유형=='d'||유형=='i'||유형=='u'||유형=='x'||유형=='X'||유형=='o'||유형=='p'){
            unsigned long long ajutuu;int 음수표시=0;
            if(유형=='d'||유형=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;ajutuu=음수표시?0-(unsigned long long)임시값:임시값;}
            else ajutuu=유형=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned apa_ajanaa_ajutuu=유형=='x'||유형=='X'||유형=='p'?16:유형=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[ajutuu%apa_ajanaa_ajutuu];ajutuu/=apa_ajanaa_ajutuu;}while(ajutuu);
            if(음수표시)완충공간[개수++]='-';if(유형=='p'||(대체값&&apa_ajanaa_ajutuu==16)){완충공간[개수++]='0';완충공간[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(완충공간)-사용량;채움++)완충공간[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(완충공간)-사용량)완충공간[개수++]='0';
            while(사용량)완충공간[개수++]=숫자수[--사용량];
        }else{완충공간[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,kaleena_atijaaya[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*anaajaalaa_ekeroliaa,...){va_list 첫째값;va_start(첫째값,anaajaalaa_ekeroliaa);int 반환값=vsnprintf(결과자료,용량한도,anaajaalaa_ekeroliaa,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*anaajaalaa_ekeroliaa,...){va_list 첫째값;va_start(첫째값,anaajaalaa_ekeroliaa);int 반환값=vsnprintf(결과자료,SIZE_MAX,anaajaalaa_ekeroliaa,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*palantüsü_ajutuu,const char*anaajaalaa_ekeroliaa,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),anaajaalaa_ekeroliaa,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,palantüsü_ajutuu)==(size_t)개수?개수:-1;}
int fprintf(FILE*palantüsü_ajutuu,const char*anaajaalaa_ekeroliaa,...){va_list 첫째값;va_start(첫째값,anaajaalaa_ekeroliaa);int 반환값=vfprintf(palantüsü_ajutuu,anaajaalaa_ekeroliaa,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*anaajaalaa_ekeroliaa,...){va_list 첫째값;va_start(첫째값,anaajaalaa_ekeroliaa);int 반환값=vfprintf(stdout,anaajaalaa_ekeroliaa,첫째값);va_end(첫째값);return 반환값;}
