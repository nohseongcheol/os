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
static int تېروتنه;
int *__errno_location(void){return &تېروتنه;}
void exit(int انکړ_ارزښت){사용자호출(6,انکړ_ارزښت,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *کتل_څرګندنه,const char *دوتنه,unsigned ليکه,const char *함수이름){fprintf(stderr,"cc assertion: %s %s:%u %s\n",کتل_څرګندنه,دوتنه,ليکه,함수이름);exit(1);}
size_t strlen(const char*مزى_اومتوک){const char*자료위치=مزى_اومتوک;while(*자료위치)자료위치++;return 자료위치-مزى_اومتوک;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char 가로좌표=*첫째값++,세로좌표=*둘째값++;if(가로좌표!=세로좌표)return 가로좌표-세로좌표;if(!가로좌표)return 0;}return 0;}
char *strcpy(char*موخه_اومتوک,const char*مزى_اومتوک){char*반환값=موخه_اومتوک;while((*موخه_اومتوک++=*مزى_اومتوک++)){}return 반환값;}
char *strchr(const char*مزى_اومتوک,int 문자값){do{if(*مزى_اومتوک==(char)문자값)return (char*)مزى_اومتوک;}while(*مزى_اومتوک++);return 0;}
char *strrchr(const char*مزى_اومتوک,int 문자값){const char*반환값=0;do{if(*مزى_اومتوک==(char)문자값)반환값=مزى_اومتوک;}while(*مزى_اومتوک++);return (char*)반환값;}
char *strstr(const char*مزى_اومتوک,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*مزى_اومتوک;مزى_اومتوک++)if(!strncmp(مزى_اومتوک,터미널항목,개수))return (char*)مزى_اومتوک;return 개수?0:(char*)مزى_اومتوک;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*가로좌표=첫째값,*세로좌표=둘째값;while(개수--){if(*가로좌표!=*세로좌표)return *가로좌표-*세로좌표;가로좌표++;세로좌표++;}return 0;}
void *memmove(void*موخه_اومتوک,const void*مزى_اومتوک,size_t 개수){unsigned char*가로좌표=موخه_اومتوک;const unsigned char*세로좌표=مزى_اومتوک;if(가로좌표<세로좌표){for(size_t 순번=0;순번<개수;순번++)가로좌표[순번]=세로좌표[순번];}else while(개수){개수--;가로좌표[개수]=세로좌표[개수];}return موخه_اومتوک;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct 자료덩이 {size_t کچ;struct 자료덩이*다음;int 남은공간;int 채울크기;uint64_t 맞춤단위;} 자료덩이;
static 자료덩이 *첫항목;
void free(void*자료위치){if(!자료위치)return;자료덩이*둘째값=(자료덩이*)자료위치-1;둘째값->남은공간=1;for(자료덩이*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->کچ+=sizeof(자료덩이)+다음위치->다음->کچ;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(자료덩이))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(자료덩이*)할당마당;첫항목->کچ=sizeof(할당마당)-sizeof(자료덩이);첫항목->남은공간=1;첫항목->다음=0;}
    자료덩이*이전=자료위치?(자료덩이*)자료위치-1:0;if(이전&&이전->کچ>=개수)return 자료위치;
    for(자료덩이*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->کچ>=개수){
        if(둘째값->کچ>=개수+sizeof(자료덩이)+16){자료덩이*나머지부분=(자료덩이*)((unsigned char*)(둘째값+1)+개수);나머지부분->کچ=둘째값->کچ-개수-sizeof(자료덩이);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->کچ=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->کچ);free(자료위치);}return 반환값;
    }تېروتنه=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t مزى_اومتوک){if(مزى_اومتوک&&개수>SIZE_MAX/مزى_اومتوک)return 0;void*자료위치=malloc(개수*مزى_اومتوک);if(자료위치)memset(자료위치,0,개수*مزى_اومتوک);return 자료위치;}
unsigned long long strtoull(const char*مزى_اومتوک,char**끝위치,int شاليد_ارزښت){
    const char*시작위치=مزى_اومتوک;while(*مزى_اومتوک==' '||(*مزى_اومتوک>=9&&*مزى_اومتوک<=13))مزى_اومتوک++;int 음수여부=0;if(*مزى_اومتوک=='-'||*مزى_اومتوک=='+')음수여부=*مزى_اومتوک++=='-';
    if((!شاليد_ارزښت||شاليد_ارزښت==16)&&مزى_اومتوک[0]=='0'&&(مزى_اومتوک[1]=='x'||مزى_اومتوک[1]=='X')){شاليد_ارزښت=16;مزى_اومتوک+=2;}if(!شاليد_ارزښت)شاليد_ارزښت=*مزى_اومتوک=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned 문자값=*مزى_اومتوک,موخه_اومتوک=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='z'?문자값-'a'+10:문자값>='A'&&문자값<='Z'?문자값-'A'+10:99;if(موخه_اومتوک>=(unsigned)شاليد_ارزښت)break;하나라도=1;مزى_اومتوک++;if(임시값>(~0ull-موخه_اومتوک)/(unsigned)شاليد_ارزښت){임시값=~0ull;تېروتنه=34;}else 임시값=임시값*شاليد_ارزښت+موخه_اومتوک;}
    if(끝위치)*끝위치=(char*)(하나라도?مزى_اومتوک:시작위치);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*مزى_اومتوک,char**보조항목,int 둘째값){return strtoull(مزى_اومتوک,보조항목,둘째값);}
long strtol(const char*مزى_اومتوک,char**보조항목,int 둘째값){return (long)strtoull(مزى_اومتوک,보조항목,둘째값);}
int atoi(const char*مزى_اومتوک){return (int)strtol(مزى_اومتوک,0,10);}
long double ldexpl(long double 가로좌표,int 개수){while(개수>0){가로좌표*=2;개수--;}while(개수<0){가로좌표/=2;개수++;}return 가로좌표;}
long double strtold(const char*مزى_اومتوک,char**끝위치){
    const char*시작위치=مزى_اومتوک;while(*مزى_اومتوک==' '||(*مزى_اومتوک>=9&&*مزى_اومتوک<=13))مزى_اومتوک++;int 음수여부=0;if(*مزى_اومتوک=='-'||*مزى_اومتوک=='+')음수여부=*مزى_اومتوک++=='-';
    int شاليد_ارزښت=10;if(مزى_اومتوک[0]=='0'&&(مزى_اومتوک[1]=='x'||مزى_اومتوک[1]=='X')){شاليد_ارزښت=16;مزى_اومتوک+=2;}long double 임시값=0,مېچ=1;int 소수부=0,하나라도=0;
    for(;;){int 문자값=*مزى_اومتوک,موخه_اومتوک=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='f'?문자값-'a'+10:문자값>='A'&&문자값<='F'?문자값-'A'+10:99;
        if(문자값=='.'&&!소수부){소수부=1;مزى_اومتوک++;continue;}if(موخه_اومتوک>=شاليد_ارزښت)break;하나라도=1;مزى_اومتوک++;임시값=임시값*شاليد_ارزښت+موخه_اومتوک;if(소수부)مېچ*=شاليد_ارزښت;
    }임시값/=مېچ;
    if((شاليد_ارزښت==10&&(*مزى_اومتوک=='e'||*مزى_اومتوک=='E'))||(شاليد_ارزښت==16&&(*مزى_اومتوک=='p'||*مزى_اومتوک=='P'))){const char*표시=مزى_اومتوک++;int 빼기=0;if(*مزى_اومتوک=='-'||*مزى_اومتوک=='+')빼기=*مزى_اومتوک++=='-';int 개수=0,항목수=0;while(*مزى_اومتوک>='0'&&*مزى_اومتوک<='9'){항목수++;if(개수<20000)개수=개수*10+*مزى_اومتوک-'0';مزى_اومتوک++;}if(!항목수)مزى_اومتوک=표시;else{long double 배율=شاليد_ارزښت==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/배율:임시값*배율;}}
    if(끝위치)*끝위치=(char*)(하나라도?مزى_اومتوک:시작위치);return 음수여부?-임시값:임시값;
}
double strtod(const char*مزى_اومتوک,char**보조항목){return (double)strtold(مزى_اومتوک,보조항목);}float strtof(const char*مزى_اومتوک,char**보조항목){return (float)strtold(مزى_اومتوک,보조항목);}
void qsort(void*شاليد_ارزښت,size_t 개수,size_t کچ,int(*پرتلل)(const void*,const void*)){
    unsigned char*자료위치=شاليد_ارزښت;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&پرتلل(자료위치+(안쪽순번-1)*کچ,자료위치+안쪽순번*کچ)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<کچ;셋째순번++){unsigned char 문자값=자료위치[(안쪽순번-1)*کچ+셋째순번];자료위치[(안쪽순번-1)*کچ+셋째순번]=자료위치[안쪽순번*کچ+셋째순번];자료위치[안쪽순번*کچ+셋째순번]=문자값;}
}
static struct {int 사용량,색인;size_t ځای;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*نوم,int 설정비트,...){
    if(!strcmp(نوم,"/@cc-output")){if(출력열림){تېروتنه=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(نوم,번역기자원들[순번].نوم)){
        if(설정비트&3){تېروتنه=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].ځای=0;return 128+안쪽순번;}تېروتنه=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)نوم,설정비트,0,0,0,0);if(반환값<0){تېروتنه=-반환값;return -1;}return 반환값;
}
int close(int دوتنه_لاستى){if(دوتنه_لاستى==100){출력열림=0;return 0;}if(دوتنه_لاستى>=128&&دوتنه_لاستى<152){열림[دوتنه_لاستى-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,دوتنه_لاستى,0,0,0,0,0);if(반환값<0){تېروتنه=-반환값;return -1;}return 0;}
long read(int دوتنه_لاستى,void*اومتوک,size_t 개수){
    if(دوتنه_لاستى>=128&&دوتنه_لاستى<152&&열림[دوتنه_لاستى-128].사용량){int 순번=دوتنه_لاستى-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->کچ-열림[순번].ځای;if(개수>왼쪽)개수=왼쪽;memcpy(اومتوک,반환값->اومتوک+열림[순번].ځای,개수);열림[순번].ځای+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,دوتنه_لاستى,(uintptr_t)اومتوک,개수,0,0,0);if(반환값<0){تېروتنه=-반환값;return -1;}return 반환값;
}
long write(int دوتنه_لاستى,const void*اومتوک,size_t 개수){
    if(دوتنه_لاستى==100){if(개수>sizeof(출력결과)-출력위치){تېروتنه=28;return -1;}memcpy(출력결과+출력위치,اومتوک,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,دوتنه_لاستى,(uintptr_t)اومتوک,개수,0,0,0);if(반환값<0){تېروتنه=-반환값;return -1;}return 반환값;
}
long lseek(int دوتنه_لاستى,long 변위,int 기준점){
    if(دوتنه_لاستى==100){long 자료위치=변위+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){تېروتنه=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(دوتنه_لاستى>=128&&دوتنه_لاستى<152&&열림[دوتنه_لاستى-128].사용량){int 순번=دوتنه_لاستى-128;long 자료위치=변위+(기준점==0?0:기준점==1?열림[순번].ځای:번역기자원들[열림[순번].색인].کچ);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].کچ){تېروتنه=22;return -1;}열림[순번].ځای=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,دوتنه_لاستى,변위,기준점,0,0,0);if(반환값<0){تېروتنه=-반환값;return -1;}return 반환값;
}
int unlink(const char*نوم){intptr_t 반환값=사용자호출(11,(uintptr_t)نوم,0,0,0,0,0);if(반환값<0){تېروتنه=-반환값;return -1;}return 반환값;}
char *realpath(const char*نوم,char*결과자료){if(!결과자료){결과자료=malloc(strlen(نوم)+1);if(!결과자료)return 0;}return strcpy(결과자료,نوم);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){تېروتنه=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int دوتنه_لاستى,const char*방식){(void)방식;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].تېروتنه=0;흐름목록[순번].دوتنه_لاستى=دوتنه_لاستى;return &흐름목록[순번];}تېروتنه=24;return 0;}
int fflush(FILE*دوتنه_ننوت){return دوتنه_ننوت&&دوتنه_ننوت->تېروتنه?-1:0;}
int fclose(FILE*دوتنه_ننوت){int 반환값=close(دوتنه_ننوت->دوتنه_لاستى);if(دوتنه_ننوت->تېروتنه)반환값=-1;دوتنه_ننوت->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t مزى_اومتوک,size_t 개수,FILE*دوتنه_ننوت){if(!مزى_اومتوک)return 0;if(개수>SIZE_MAX/مزى_اومتوک){دوتنه_ننوت->تېروتنه=1;return 0;}long 반환값=write(دوتنه_ننوت->دوتنه_لاستى,자료위치,مزى_اومتوک*개수);if(반환값<0){دوتنه_ننوت->تېروتنه=1;return 0;}return (size_t)반환값/مزى_اومتوک;}
int fputc(int 문자값,FILE*دوتنه_ننوت){unsigned char 둘째값=문자값;return fwrite(&둘째값,1,1,دوتنه_ننوت)==1?둘째값:EOF;}
int fputs(const char*مزى_اومتوک,FILE*دوتنه_ننوت){return fwrite(مزى_اومتوک,1,strlen(مزى_اومتوک),دوتنه_ننوت)==strlen(مزى_اومتوک)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char 문자값){if(*현재위치+1<용량한도)결과자료[*현재위치]=문자값;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*بڼه,va_list 가변인수){
    size_t 현재위치=0;while(*بڼه){if(*بڼه!='%'){넣기(결과자료,용량한도,&현재위치,*بڼه++);continue;}بڼه++;
        int 왼쪽=0,영값=0,대체값=0;while(*بڼه=='-'||*بڼه=='0'||*بڼه=='#'||*بڼه=='+'||*بڼه==' '){if(*بڼه=='-')왼쪽=1;if(*بڼه=='0')영값=1;if(*بڼه=='#')대체값=1;بڼه++;}
        int 너비=0,정밀도=-1;if(*بڼه=='*'){너비=va_arg(가변인수,int);بڼه++;}else while(*بڼه>='0'&&*بڼه<='9')너비=너비*10+*بڼه++-'0';
        if(*بڼه=='.'){بڼه++;정밀도=0;if(*بڼه=='*'){정밀도=va_arg(가변인수,int);بڼه++;}else while(*بڼه>='0'&&*بڼه<='9')정밀도=정밀도*10+*بڼه++-'0';}
        int 넓은글자=0;while(*بڼه=='l'||*بڼه=='z'||*بڼه=='t'||*بڼه=='j'||*بڼه=='h'){if(*بڼه!='h')넓은글자=1;بڼه++;}
        char 유형=*بڼه?*بڼه++:0,완충공간[80];const char*مزى_اومتوک=완충공간;size_t 개수=0;
        if(유형=='s'){مزى_اومتوک=va_arg(가변인수,const char*);if(!مزى_اومتوک)مزى_اومتوک="(null)";개수=strlen(مزى_اومتوک);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(유형=='c'){완충공간[0]=va_arg(가변인수,int);개수=1;}
        else if(유형=='%'){완충공간[0]='%';개수=1;}
        else if(유형=='d'||유형=='i'||유형=='u'||유형=='x'||유형=='X'||유형=='o'||유형=='p'){
            unsigned long long ارزښت;int 음수표시=0;
            if(유형=='d'||유형=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;ارزښت=음수표시?0-(unsigned long long)임시값:임시값;}
            else ارزښت=유형=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned شاليد_ارزښت=유형=='x'||유형=='X'||유형=='p'?16:유형=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[ارزښت%شاليد_ارزښت];ارزښت/=شاليد_ارزښت;}while(ارزښت);
            if(음수표시)완충공간[개수++]='-';if(유형=='p'||(대체값&&شاليد_ارزښت==16)){완충공간[개수++]='0';완충공간[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(완충공간)-사용량;채움++)완충공간[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(완충공간)-사용량)완충공간[개수++]='0';
            while(사용량)완충공간[개수++]=숫자수[--사용량];
        }else{완충공간[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,مزى_اومتوک[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*دوتنه_ننوت,...){va_list 첫째값;va_start(첫째값,دوتنه_ننوت);int 반환값=vsnprintf(결과자료,용량한도,دوتنه_ننوت,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*دوتنه_ننوت,...){va_list 첫째값;va_start(첫째값,دوتنه_ننوت);int 반환값=vsnprintf(결과자료,SIZE_MAX,دوتنه_ننوت,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*بهنګ_ارزښت,const char*دوتنه_ننوت,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),دوتنه_ننوت,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,بهنګ_ارزښت)==(size_t)개수?개수:-1;}
int fprintf(FILE*بهنګ_ارزښت,const char*دوتنه_ننوت,...){va_list 첫째값;va_start(첫째값,دوتنه_ننوت);int 반환값=vfprintf(بهنګ_ارزښت,دوتنه_ننوت,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*دوتنه_ننوت,...){va_list 첫째값;va_start(첫째값,دوتنه_ننوت);int 반환값=vfprintf(stdout,دوتنه_ننوت,첫째값);va_end(첫째값);return 반환값;}
