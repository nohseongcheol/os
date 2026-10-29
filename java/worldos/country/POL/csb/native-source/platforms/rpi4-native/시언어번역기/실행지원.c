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
static int Fela;
int *__errno_location(void){return &Fela;}
void exit(int 상태){사용자호출(6,상태,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *검사식,const char *Lopk,unsigned 줄,const char *함수이름){fprintf(stderr,"cc assertion: %s %s:%u %s\n",검사식,Lopk,줄,함수이름);exit(1);}
size_t strlen(const char*문자열값){const char*자료위치=문자열값;while(*자료위치)자료위치++;return 자료위치-문자열값;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char 가로좌표=*첫째값++,세로좌표=*둘째값++;if(가로좌표!=세로좌표)return 가로좌표-세로좌표;if(!가로좌표)return 0;}return 0;}
char *strcpy(char*목적자료,const char*문자열값){char*반환값=목적자료;while((*목적자료++=*문자열값++)){}return 반환값;}
char *strchr(const char*문자열값,int 문자값){do{if(*문자열값==(char)문자값)return (char*)문자열값;}while(*문자열값++);return 0;}
char *strrchr(const char*문자열값,int 문자값){const char*반환값=0;do{if(*문자열값==(char)문자값)반환값=문자열값;}while(*문자열값++);return (char*)반환값;}
char *strstr(const char*문자열값,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*문자열값;문자열값++)if(!strncmp(문자열값,터미널항목,개수))return (char*)문자열값;return 개수?0:(char*)문자열값;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*가로좌표=첫째값,*세로좌표=둘째값;while(개수--){if(*가로좌표!=*세로좌표)return *가로좌표-*세로좌표;가로좌표++;세로좌표++;}return 0;}
void *memmove(void*목적자료,const void*문자열값,size_t 개수){unsigned char*가로좌표=목적자료;const unsigned char*세로좌표=문자열값;if(가로좌표<세로좌표){for(size_t 순번=0;순번<개수;순번++)가로좌표[순번]=세로좌표[순번];}else while(개수){개수--;가로좌표[개수]=세로좌표[개수];}return 목적자료;}
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
    }Fela=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t 문자열값){if(문자열값&&개수>SIZE_MAX/문자열값)return 0;void*자료위치=malloc(개수*문자열값);if(자료위치)memset(자료위치,0,개수*문자열값);return 자료위치;}
unsigned long long strtoull(const char*문자열값,char**끝위치,int 바탕){
    const char*시작위치=문자열값;while(*문자열값==' '||(*문자열값>=9&&*문자열값<=13))문자열값++;int 음수여부=0;if(*문자열값=='-'||*문자열값=='+')음수여부=*문자열값++=='-';
    if((!바탕||바탕==16)&&문자열값[0]=='0'&&(문자열값[1]=='x'||문자열값[1]=='X')){바탕=16;문자열값+=2;}if(!바탕)바탕=*문자열값=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned 문자값=*문자열값,목적자료=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='z'?문자값-'a'+10:문자값>='A'&&문자값<='Z'?문자값-'A'+10:99;if(목적자료>=(unsigned)바탕)break;하나라도=1;문자열값++;if(임시값>(~0ull-목적자료)/(unsigned)바탕){임시값=~0ull;Fela=34;}else 임시값=임시값*바탕+목적자료;}
    if(끝위치)*끝위치=(char*)(하나라도?문자열값:시작위치);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*문자열값,char**보조항목,int 둘째값){return strtoull(문자열값,보조항목,둘째값);}
long strtol(const char*문자열값,char**보조항목,int 둘째값){return (long)strtoull(문자열값,보조항목,둘째값);}
int atoi(const char*문자열값){return (int)strtol(문자열값,0,10);}
long double ldexpl(long double 가로좌표,int 개수){while(개수>0){가로좌표*=2;개수--;}while(개수<0){가로좌표/=2;개수++;}return 가로좌표;}
long double strtold(const char*문자열값,char**끝위치){
    const char*시작위치=문자열값;while(*문자열값==' '||(*문자열값>=9&&*문자열값<=13))문자열값++;int 음수여부=0;if(*문자열값=='-'||*문자열값=='+')음수여부=*문자열값++=='-';
    int 바탕=10;if(문자열값[0]=='0'&&(문자열값[1]=='x'||문자열값[1]=='X')){바탕=16;문자열값+=2;}long double 임시값=0,크기배율=1;int 소수부=0,하나라도=0;
    for(;;){int 문자값=*문자열값,목적자료=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='f'?문자값-'a'+10:문자값>='A'&&문자값<='F'?문자값-'A'+10:99;
        if(문자값=='.'&&!소수부){소수부=1;문자열값++;continue;}if(목적자료>=바탕)break;하나라도=1;문자열값++;임시값=임시값*바탕+목적자료;if(소수부)크기배율*=바탕;
    }임시값/=크기배율;
    if((바탕==10&&(*문자열값=='e'||*문자열값=='E'))||(바탕==16&&(*문자열값=='p'||*문자열값=='P'))){const char*표시=문자열값++;int 빼기=0;if(*문자열값=='-'||*문자열값=='+')빼기=*문자열값++=='-';int 개수=0,항목수=0;while(*문자열값>='0'&&*문자열값<='9'){항목수++;if(개수<20000)개수=개수*10+*문자열값-'0';문자열값++;}if(!항목수)문자열값=표시;else{long double 배율=바탕==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/배율:임시값*배율;}}
    if(끝위치)*끝위치=(char*)(하나라도?문자열값:시작위치);return 음수여부?-임시값:임시값;
}
double strtod(const char*문자열값,char**보조항목){return (double)strtold(문자열값,보조항목);}float strtof(const char*문자열값,char**보조항목){return (float)strtold(문자열값,보조항목);}
void qsort(void*바탕,size_t 개수,size_t 크기,int(*비교함수)(const void*,const void*)){
    unsigned char*자료위치=바탕;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&비교함수(자료위치+(안쪽순번-1)*크기,자료위치+안쪽순번*크기)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<크기;셋째순번++){unsigned char 문자값=자료위치[(안쪽순번-1)*크기+셋째순번];자료위치[(안쪽순번-1)*크기+셋째순번]=자료위치[안쪽순번*크기+셋째순번];자료위치[안쪽순번*크기+셋째순번]=문자값;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*이름,int 설정비트,...){
    if(!strcmp(이름,"/@cc-output")){if(출력열림){Fela=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(이름,번역기자원들[순번].이름)){
        if(설정비트&3){Fela=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}Fela=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)이름,설정비트,0,0,0,0);if(반환값<0){Fela=-반환값;return -1;}return 반환값;
}
int close(int 파일기술자){if(파일기술자==100){출력열림=0;return 0;}if(파일기술자>=128&&파일기술자<152){열림[파일기술자-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,파일기술자,0,0,0,0,0);if(반환값<0){Fela=-반환값;return -1;}return 0;}
long read(int 파일기술자,void*자료,size_t 개수){
    if(파일기술자>=128&&파일기술자<152&&열림[파일기술자-128].사용량){int 순번=파일기술자-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->크기-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(자료,반환값->자료+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,파일기술자,(uintptr_t)자료,개수,0,0,0);if(반환값<0){Fela=-반환값;return -1;}return 반환값;
}
long write(int 파일기술자,const void*자료,size_t 개수){
    if(파일기술자==100){if(개수>sizeof(출력결과)-출력위치){Fela=28;return -1;}memcpy(출력결과+출력위치,자료,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,파일기술자,(uintptr_t)자료,개수,0,0,0);if(반환값<0){Fela=-반환값;return -1;}return 반환값;
}
long lseek(int 파일기술자,long 변위,int 기준점){
    if(파일기술자==100){long 자료위치=변위+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){Fela=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(파일기술자>=128&&파일기술자<152&&열림[파일기술자-128].사용량){int 순번=파일기술자-128;long 자료위치=변위+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].크기);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].크기){Fela=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,파일기술자,변위,기준점,0,0,0);if(반환값<0){Fela=-반환값;return -1;}return 반환값;
}
int unlink(const char*이름){intptr_t 반환값=사용자호출(11,(uintptr_t)이름,0,0,0,0,0);if(반환값<0){Fela=-반환값;return -1;}return 반환값;}
char *realpath(const char*이름,char*결과자료){if(!결과자료){결과자료=malloc(strlen(이름)+1);if(!결과자료)return 0;}return strcpy(결과자료,이름);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){Fela=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int 파일기술자,const char*방식){(void)방식;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Fela=0;흐름목록[순번].파일기술자=파일기술자;return &흐름목록[순번];}Fela=24;return 0;}
int fflush(FILE*파일항목){return 파일항목&&파일항목->Fela?-1:0;}
int fclose(FILE*파일항목){int 반환값=close(파일항목->파일기술자);if(파일항목->Fela)반환값=-1;파일항목->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t 문자열값,size_t 개수,FILE*파일항목){if(!문자열값)return 0;if(개수>SIZE_MAX/문자열값){파일항목->Fela=1;return 0;}long 반환값=write(파일항목->파일기술자,자료위치,문자열값*개수);if(반환값<0){파일항목->Fela=1;return 0;}return (size_t)반환값/문자열값;}
int fputc(int 문자값,FILE*파일항목){unsigned char 둘째값=문자값;return fwrite(&둘째값,1,1,파일항목)==1?둘째값:EOF;}
int fputs(const char*문자열값,FILE*파일항목){return fwrite(문자열값,1,strlen(문자열값),파일항목)==strlen(문자열값)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char 문자값){if(*현재위치+1<용량한도)결과자료[*현재위치]=문자값;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*서식,va_list 가변인수){
    size_t 현재위치=0;while(*서식){if(*서식!='%'){넣기(결과자료,용량한도,&현재위치,*서식++);continue;}서식++;
        int 왼쪽=0,영값=0,대체값=0;while(*서식=='-'||*서식=='0'||*서식=='#'||*서식=='+'||*서식==' '){if(*서식=='-')왼쪽=1;if(*서식=='0')영값=1;if(*서식=='#')대체값=1;서식++;}
        int 너비=0,정밀도=-1;if(*서식=='*'){너비=va_arg(가변인수,int);서식++;}else while(*서식>='0'&&*서식<='9')너비=너비*10+*서식++-'0';
        if(*서식=='.'){서식++;정밀도=0;if(*서식=='*'){정밀도=va_arg(가변인수,int);서식++;}else while(*서식>='0'&&*서식<='9')정밀도=정밀도*10+*서식++-'0';}
        int 넓은글자=0;while(*서식=='l'||*서식=='z'||*서식=='t'||*서식=='j'||*서식=='h'){if(*서식!='h')넓은글자=1;서식++;}
        char 유형=*서식?*서식++:0,완충공간[80];const char*문자열값=완충공간;size_t 개수=0;
        if(유형=='s'){문자열값=va_arg(가변인수,const char*);if(!문자열값)문자열값="(null)";개수=strlen(문자열값);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(유형=='c'){완충공간[0]=va_arg(가변인수,int);개수=1;}
        else if(유형=='%'){완충공간[0]='%';개수=1;}
        else if(유형=='d'||유형=='i'||유형=='u'||유형=='x'||유형=='X'||유형=='o'||유형=='p'){
            unsigned long long 값;int 음수표시=0;
            if(유형=='d'||유형=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;값=음수표시?0-(unsigned long long)임시값:임시값;}
            else 값=유형=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned 바탕=유형=='x'||유형=='X'||유형=='p'?16:유형=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[값%바탕];값/=바탕;}while(값);
            if(음수표시)완충공간[개수++]='-';if(유형=='p'||(대체값&&바탕==16)){완충공간[개수++]='0';완충공간[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(완충공간)-사용량;채움++)완충공간[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(완충공간)-사용량)완충공간[개수++]='0';
            while(사용량)완충공간[개수++]=숫자수[--사용량];
        }else{완충공간[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,문자열값[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*파일항목,...){va_list 첫째값;va_start(첫째값,파일항목);int 반환값=vsnprintf(결과자료,용량한도,파일항목,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*파일항목,...){va_list 첫째값;va_start(첫째값,파일항목);int 반환값=vsnprintf(결과자료,SIZE_MAX,파일항목,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*흐름,const char*파일항목,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),파일항목,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,흐름)==(size_t)개수?개수:-1;}
int fprintf(FILE*흐름,const char*파일항목,...){va_list 첫째값;va_start(첫째값,파일항목);int 반환값=vfprintf(흐름,파일항목,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*파일항목,...){va_list 첫째값;va_start(첫째값,파일항목);int 반환값=vfprintf(stdout,파일항목,첫째값);va_end(첫째값);return 반환값;}
