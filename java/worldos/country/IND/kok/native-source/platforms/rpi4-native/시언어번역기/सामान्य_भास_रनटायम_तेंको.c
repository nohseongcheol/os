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
static int चूक;
int *__errno_location(void){return &चूक;}
void exit(int स्थिती_मोल_e10195a1){사용자호출(6,स्थिती_मोल_e10195a1,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *तपासचें_ऍक्सप्रॅशन,const char *फायल,unsigned रेग,const char *पद्दत_प्रवेश_नांव){fprintf(stderr,"cc assertion: %s %s:%u %s\n",तपासचें_ऍक्सप्रॅशन,फायल,रेग,पद्दत_प्रवेश_नांव);exit(1);}
size_t strlen(const char*स्ट्रिंग_डेटा){const char*डेटा_स्थिती=स्ट्रिंग_डेटा;while(*डेटा_स्थिती)डेटा_स्थिती++;return डेटा_स्थिती-स्ट्रिंग_डेटा;}
int strcmp(const char*첫째값,const char*SECOND_मोल){while(*첫째값&&*첫째값==*SECOND_मोल){첫째값++;SECOND_मोल++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_मोल;}
int strncmp(const char*첫째값,const char*SECOND_मोल,size_t आयटम_COUNT){while(आयटम_COUNT--){unsigned char x_coordinate=*첫째값++,세로좌표=*SECOND_मोल++;if(x_coordinate!=세로좌표)return x_coordinate-세로좌표;if(!x_coordinate)return 0;}return 0;}
char *strcpy(char*नियुक्त_स्थान_डेटा,const char*स्ट्रिंग_डेटा){char*반환값=नियुक्त_स्थान_डेटा;while((*नियुक्त_स्थान_डेटा++=*स्ट्रिंग_डेटा++)){}return 반환값;}
char *strchr(const char*स्ट्रिंग_डेटा,int वर्ण_कोड){do{if(*स्ट्रिंग_डेटा==(char)वर्ण_कोड)return (char*)स्ट्रिंग_डेटा;}while(*स्ट्रिंग_डेटा++);return 0;}
char *strrchr(const char*स्ट्रिंग_डेटा,int वर्ण_कोड){const char*반환값=0;do{if(*स्ट्रिंग_डेटा==(char)वर्ण_कोड)반환값=स्ट्रिंग_डेटा;}while(*स्ट्रिंग_डेटा++);return (char*)반환값;}
char *strstr(const char*स्ट्रिंग_डेटा,const char*टर्मिनल_प्रवेश){size_t आयटम_COUNT=strlen(टर्मिनल_प्रवेश);for(;*स्ट्रिंग_डेटा;स्ट्रिंग_डेटा++)if(!strncmp(स्ट्रिंग_डेटा,टर्मिनल_प्रवेश,आयटम_COUNT))return (char*)स्ट्रिंग_डेटा;return आयटम_COUNT?0:(char*)स्ट्रिंग_डेटा;}
int memcmp(const void*첫째값,const void*SECOND_मोल,size_t आयटम_COUNT){const unsigned char*x_coordinate=첫째값,*세로좌표=SECOND_मोल;while(आयटम_COUNT--){if(*x_coordinate!=*세로좌표)return *x_coordinate-*세로좌표;x_coordinate++;세로좌표++;}return 0;}
void *memmove(void*नियुक्त_स्थान_डेटा,const void*स्ट्रिंग_डेटा,size_t आयटम_COUNT){unsigned char*x_coordinate=नियुक्त_स्थान_डेटा;const unsigned char*세로좌표=स्ट्रिंग_डेटा;if(x_coordinate<세로좌표){for(size_t 순번=0;순번<आयटम_COUNT;순번++)x_coordinate[순번]=세로좌표[순번];}else while(आयटम_COUNT){आयटम_COUNT--;x_coordinate[आयटम_COUNT]=세로좌표[आयटम_COUNT];}return नियुक्त_स्थान_डेटा;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct डेटा_आडावचें {size_t आवाठ;struct डेटा_आडावचें*फुडलें_आयटम;int 남은공간;int 채울크기;uint64_t आंखणी_एकक;} डेटा_आडावचें;
static डेटा_आडावचें *첫항목;
void free(void*डेटा_स्थिती){if(!डेटा_स्थिती)return;डेटा_आडावचें*SECOND_मोल=(डेटा_आडावचें*)डेटा_स्थिती-1;SECOND_मोल->남은공간=1;for(डेटा_आडावचें*फुडलें_ऑफसॅट=첫항목;फुडलें_ऑफसॅट&&फुडलें_ऑफसॅट->फुडलें_आयटम;){if(फुडलें_ऑफसॅट->남은공간&&फुडलें_ऑफसॅट->फुडलें_आयटम->남은공간){फुडलें_ऑफसॅट->आवाठ+=sizeof(डेटा_आडावचें)+फुडलें_ऑफसॅट->फुडलें_आयटम->आवाठ;फुडलें_ऑफसॅट->फुडलें_आयटम=फुडलें_ऑफसॅट->फुडलें_आयटम->फुडलें_आयटम;}else फुडलें_ऑफसॅट=फुडलें_ऑफसॅट->फुडलें_आयटम;}}
void *realloc(void*डेटा_स्थिती,size_t आयटम_COUNT){
    if(!आयटम_COUNT){free(डेटा_स्थिती);return 0;}if(आयटम_COUNT>sizeof(할당마당)-sizeof(डेटा_आडावचें))return 0;आयटम_COUNT=(आयटम_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(डेटा_आडावचें*)할당마당;첫항목->आवाठ=sizeof(할당마당)-sizeof(डेटा_आडावचें);첫항목->남은공간=1;첫항목->फुडलें_आयटम=0;}
    डेटा_आडावचें*이전=डेटा_स्थिती?(डेटा_आडावचें*)डेटा_स्थिती-1:0;if(이전&&이전->आवाठ>=आयटम_COUNT)return डेटा_स्थिती;
    for(डेटा_आडावचें*SECOND_मोल=첫항목;SECOND_मोल;SECOND_मोल=SECOND_मोल->फुडलें_आयटम)if(SECOND_मोल->남은공간&&SECOND_मोल->आवाठ>=आयटम_COUNT){
        if(SECOND_मोल->आवाठ>=आयटम_COUNT+sizeof(डेटा_आडावचें)+16){डेटा_आडावचें*나머지부분=(डेटा_आडावचें*)((unsigned char*)(SECOND_मोल+1)+आयटम_COUNT);나머지부분->आवाठ=SECOND_मोल->आवाठ-आयटम_COUNT-sizeof(डेटा_आडावचें);나머지부분->फुडलें_आयटम=SECOND_मोल->फुडलें_आयटम;나머지부분->남은공간=1;SECOND_मोल->फुडलें_आयटम=나머지부분;SECOND_मोल->आवाठ=आयटम_COUNT;}
        SECOND_मोल->남은공간=0;void*반환값=SECOND_मोल+1;if(이전){memcpy(반환값,डेटा_स्थिती,이전->आवाठ);free(डेटा_स्थिती);}return 반환값;
    }चूक=12;return 0;
}
void *malloc(size_t आयटम_COUNT){return realloc(0,आयटम_COUNT);}
void *calloc(size_t आयटम_COUNT,size_t स्ट्रिंग_डेटा){if(स्ट्रिंग_डेटा&&आयटम_COUNT>SIZE_MAX/स्ट्रिंग_डेटा)return 0;void*डेटा_स्थिती=malloc(आयटम_COUNT*स्ट्रिंग_डेटा);if(डेटा_स्थिती)memset(डेटा_स्थिती,0,आयटम_COUNT*स्ट्रिंग_डेटा);return डेटा_स्थिती;}
unsigned long long strtoull(const char*स्ट्रिंग_डेटा,char**सोपोवचें_ऑफसॅट,int फाटभूंय_मोल){
    const char*Start_ऑफसॅट=स्ट्रिंग_डेटा;while(*स्ट्रिंग_डेटा==' '||(*स्ट्रिंग_डेटा>=9&&*स्ट्रिंग_डेटा<=13))स्ट्रिंग_डेटा++;int 음수여부=0;if(*स्ट्रिंग_डेटा=='-'||*स्ट्रिंग_डेटा=='+')음수여부=*स्ट्रिंग_डेटा++=='-';
    if((!फाटभूंय_मोल||फाटभूंय_मोल==16)&&स्ट्रिंग_डेटा[0]=='0'&&(स्ट्रिंग_डेटा[1]=='x'||स्ट्रिंग_डेटा[1]=='X')){फाटभूंय_मोल=16;स्ट्रिंग_डेटा+=2;}if(!फाटभूंय_मोल)फाटभूंय_मोल=*स्ट्रिंग_डेटा=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned वर्ण_कोड=*स्ट्रिंग_डेटा,नियुक्त_स्थान_डेटा=वर्ण_कोड>='0'&&वर्ण_कोड<='9'?वर्ण_कोड-'0':वर्ण_कोड>='a'&&वर्ण_कोड<='z'?वर्ण_कोड-'a'+10:वर्ण_कोड>='A'&&वर्ण_कोड<='Z'?वर्ण_कोड-'A'+10:99;if(नियुक्त_स्थान_डेटा>=(unsigned)फाटभूंय_मोल)break;하나라도=1;स्ट्रिंग_डेटा++;if(임시값>(~0ull-नियुक्त_स्थान_डेटा)/(unsigned)फाटभूंय_मोल){임시값=~0ull;चूक=34;}else 임시값=임시값*फाटभूंय_मोल+नियुक्त_स्थान_डेटा;}
    if(सोपोवचें_ऑफसॅट)*सोपोवचें_ऑफसॅट=(char*)(하나라도?स्ट्रिंग_डेटा:Start_ऑफसॅट);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*स्ट्रिंग_डेटा,char**보조항목,int SECOND_मोल){return strtoull(स्ट्रिंग_डेटा,보조항목,SECOND_मोल);}
long strtol(const char*स्ट्रिंग_डेटा,char**보조항목,int SECOND_मोल){return (long)strtoull(स्ट्रिंग_डेटा,보조항목,SECOND_मोल);}
int atoi(const char*स्ट्रिंग_डेटा){return (int)strtol(स्ट्रिंग_डेटा,0,10);}
long double ldexpl(long double x_coordinate,int आयटम_COUNT){while(आयटम_COUNT>0){x_coordinate*=2;आयटम_COUNT--;}while(आयटम_COUNT<0){x_coordinate/=2;आयटम_COUNT++;}return x_coordinate;}
long double strtold(const char*स्ट्रिंग_डेटा,char**सोपोवचें_ऑफसॅट){
    const char*Start_ऑफसॅट=स्ट्रिंग_डेटा;while(*स्ट्रिंग_डेटा==' '||(*स्ट्रिंग_डेटा>=9&&*स्ट्रिंग_डेटा<=13))स्ट्रिंग_डेटा++;int 음수여부=0;if(*स्ट्रिंग_डेटा=='-'||*स्ट्रिंग_डेटा=='+')음수여부=*स्ट्रिंग_डेटा++=='-';
    int फाटभूंय_मोल=10;if(स्ट्रिंग_डेटा[0]=='0'&&(स्ट्रिंग_डेटा[1]=='x'||स्ट्रिंग_डेटा[1]=='X')){फाटभूंय_मोल=16;स्ट्रिंग_डेटा+=2;}long double 임시값=0,स्केल=1;int 소수부=0,하나라도=0;
    for(;;){int वर्ण_कोड=*स्ट्रिंग_डेटा,नियुक्त_स्थान_डेटा=वर्ण_कोड>='0'&&वर्ण_कोड<='9'?वर्ण_कोड-'0':वर्ण_कोड>='a'&&वर्ण_कोड<='f'?वर्ण_कोड-'a'+10:वर्ण_कोड>='A'&&वर्ण_कोड<='F'?वर्ण_कोड-'A'+10:99;
        if(वर्ण_कोड=='.'&&!소수부){소수부=1;स्ट्रिंग_डेटा++;continue;}if(नियुक्त_स्थान_डेटा>=फाटभूंय_मोल)break;하나라도=1;स्ट्रिंग_डेटा++;임시값=임시값*फाटभूंय_मोल+नियुक्त_स्थान_डेटा;if(소수부)स्केल*=फाटभूंय_मोल;
    }임시값/=स्केल;
    if((फाटभूंय_मोल==10&&(*स्ट्रिंग_डेटा=='e'||*स्ट्रिंग_डेटा=='E'))||(फाटभूंय_मोल==16&&(*स्ट्रिंग_डेटा=='p'||*स्ट्रिंग_डेटा=='P'))){const char*शो_मोल=स्ट्रिंग_डेटा++;int 빼기=0;if(*स्ट्रिंग_डेटा=='-'||*स्ट्रिंग_डेटा=='+')빼기=*स्ट्रिंग_डेटा++=='-';int आयटम_COUNT=0,प्रवेश_COUNT=0;while(*स्ट्रिंग_डेटा>='0'&&*स्ट्रिंग_डेटा<='9'){प्रवेश_COUNT++;if(आयटम_COUNT<20000)आयटम_COUNT=आयटम_COUNT*10+*स्ट्रिंग_डेटा-'0';स्ट्रिंग_डेटा++;}if(!प्रवेश_COUNT)स्ट्रिंग_डेटा=शो_मोल;else{long double फॅक्टर=फाटभूंय_मोल==16?2:10;while(आयटम_COUNT-->0&&आयटम_COUNT<200000)임시값=빼기?임시값/फॅक्टर:임시값*फॅक्टर;}}
    if(सोपोवचें_ऑफसॅट)*सोपोवचें_ऑफसॅट=(char*)(하나라도?स्ट्रिंग_डेटा:Start_ऑफसॅट);return 음수여부?-임시값:임시값;
}
double strtod(const char*स्ट्रिंग_डेटा,char**보조항목){return (double)strtold(स्ट्रिंग_डेटा,보조항목);}float strtof(const char*स्ट्रिंग_डेटा,char**보조항목){return (float)strtold(स्ट्रिंग_डेटा,보조항목);}
void qsort(void*फाटभूंय_मोल,size_t आयटम_COUNT,size_t आवाठ,int(*तुळा)(const void*,const void*)){
    unsigned char*डेटा_स्थिती=फाटभूंय_मोल;for(size_t 순번=1;순번<आयटम_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&तुळा(डेटा_स्थिती+(안쪽순번-1)*आवाठ,डेटा_स्थिती+안쪽순번*आवाठ)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<आवाठ;셋째순번++){unsigned char वर्ण_कोड=डेटा_स्थिती[(안쪽순번-1)*आवाठ+셋째순번];डेटा_स्थिती[(안쪽순번-1)*आवाठ+셋째순번]=डेटा_स्थिती[안쪽순번*आवाठ+셋째순번];डेटा_स्थिती[안쪽순번*आवाठ+셋째순번]=वर्ण_कोड;}
}
static struct {int 사용량,लूकअप_INDEX;size_t स्थिती;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *आयटम_COUNT){*आयटम_COUNT=출력크기;return 출력결과;}
int open(const char*नांव,int 설정비트,...){
    if(!strcmp(नांव,"/@cc-output")){if(출력열림){चूक=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(नांव,번역기자원들[순번].नांव)){
        if(설정비트&3){चूक=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].लूकअप_INDEX=순번;열림[안쪽순번].स्थिती=0;return 128+안쪽순번;}चूक=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)नांव,설정비트,0,0,0,0);if(반환값<0){चूक=-반환값;return -1;}return 반환값;
}
int close(int फायल_हँडल){if(फायल_हँडल==100){출력열림=0;return 0;}if(फायल_हँडल>=128&&फायल_हँडल<152){열림[फायल_हँडल-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,फायल_हँडल,0,0,0,0,0);if(반환값<0){चूक=-반환값;return -1;}return 0;}
long read(int फायल_हँडल,void*डेटा,size_t आयटम_COUNT){
    if(फायल_हँडल>=128&&फायल_हँडल<152&&열림[फायल_हँडल-128].사용량){int 순번=फायल_हँडल-128;const 번역기자원*반환값=&번역기자원들[열림[순번].लूकअप_INDEX];size_t 왼쪽=반환값->आवाठ-열림[순번].स्थिती;if(आयटम_COUNT>왼쪽)आयटम_COUNT=왼쪽;memcpy(डेटा,반환값->डेटा+열림[순번].स्थिती,आयटम_COUNT);열림[순번].स्थिती+=आयटम_COUNT;return आयटम_COUNT;}
    intptr_t 반환값=사용자호출(2,फायल_हँडल,(uintptr_t)डेटा,आयटम_COUNT,0,0,0);if(반환값<0){चूक=-반환값;return -1;}return 반환값;
}
long write(int फायल_हँडल,const void*डेटा,size_t आयटम_COUNT){
    if(फायल_हँडल==100){if(आयटम_COUNT>sizeof(출력결과)-출력위치){चूक=28;return -1;}memcpy(출력결과+출력위치,डेटा,आयटम_COUNT);출력위치+=आयटम_COUNT;if(출력크기<출력위치)출력크기=출력위치;return आयटम_COUNT;}
    intptr_t 반환값=사용자호출(1,फायल_हँडल,(uintptr_t)डेटा,आयटम_COUNT,0,0,0);if(반환값<0){चूक=-반환값;return -1;}return 반환값;
}
long lseek(int फायल_हँडल,long ऑफसॅट_मोल,int 기준점){
    if(फायल_हँडल==100){long डेटा_स्थिती=ऑफसॅट_मोल+(기준점==0?0:기준점==1?출력위치:출력크기);if(डेटा_स्थिती<0||(size_t)डेटा_स्थिती>sizeof(출력결과)){चूक=22;return -1;}출력위치=डेटा_स्थिती;return डेटा_स्थिती;}
    if(फायल_हँडल>=128&&फायल_हँडल<152&&열림[फायल_हँडल-128].사용량){int 순번=फायल_हँडल-128;long डेटा_स्थिती=ऑफसॅट_मोल+(기준점==0?0:기준점==1?열림[순번].स्थिती:번역기자원들[열림[순번].लूकअप_INDEX].आवाठ);if(डेटा_स्थिती<0||(size_t)डेटा_स्थिती>번역기자원들[열림[순번].लूकअप_INDEX].आवाठ){चूक=22;return -1;}열림[순번].स्थिती=डेटा_स्थिती;return डेटा_स्थिती;}
    intptr_t 반환값=사용자호출(5,फायल_हँडल,ऑफसॅट_मोल,기준점,0,0,0);if(반환값<0){चूक=-반환값;return -1;}return 반환값;
}
int unlink(const char*नांव){intptr_t 반환값=사용자호출(11,(uintptr_t)नांव,0,0,0,0,0);if(반환값<0){चूक=-반환값;return -1;}return 반환값;}
char *realpath(const char*नांव,char*मेजप_डेटा){if(!मेजप_डेटा){मेजप_डेटा=malloc(strlen(नांव)+1);if(!मेजप_डेटा)return 0;}return strcpy(मेजप_डेटा,नांव);}
char *getcwd(char*डेटा_स्थिती,size_t आयटम_COUNT){if(आयटम_COUNT<2){चूक=34;return 0;}डेटा_स्थिती[0]='/';डेटा_स्थिती[1]=0;return डेटा_स्थिती;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*टर्मिनल_प्रवेश){time_t 임시값=0;if(टर्मिनल_प्रवेश)*टर्मिनल_प्रवेश=임시값;return 임시값;}
struct tm *localtime(const time_t*टर्मिनल_प्रवेश){(void)टर्मिनल_प्रवेश;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int फायल_हँडल,const char*पद्दत_मोड){(void)पद्दत_मोड;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].चूक=0;흐름목록[순번].फायल_हँडल=फायल_हँडल;return &흐름목록[순번];}चूक=24;return 0;}
int fflush(FILE*फायल_प्रवेश){return फायल_प्रवेश&&फायल_प्रवेश->चूक?-1:0;}
int fclose(FILE*फायल_प्रवेश){int 반환값=close(फायल_प्रवेश->फायल_हँडल);if(फायल_प्रवेश->चूक)반환값=-1;फायल_प्रवेश->사용량=0;return 반환값;}
size_t fwrite(const void*डेटा_स्थिती,size_t स्ट्रिंग_डेटा,size_t आयटम_COUNT,FILE*फायल_प्रवेश){if(!स्ट्रिंग_डेटा)return 0;if(आयटम_COUNT>SIZE_MAX/स्ट्रिंग_डेटा){फायल_प्रवेश->चूक=1;return 0;}long 반환값=write(फायल_प्रवेश->फायल_हँडल,डेटा_स्थिती,स्ट्रिंग_डेटा*आयटम_COUNT);if(반환값<0){फायल_प्रवेश->चूक=1;return 0;}return (size_t)반환값/स्ट्रिंग_डेटा;}
int fputc(int वर्ण_कोड,FILE*फायल_प्रवेश){unsigned char SECOND_मोल=वर्ण_कोड;return fwrite(&SECOND_मोल,1,1,फायल_प्रवेश)==1?SECOND_मोल:EOF;}
int fputs(const char*स्ट्रिंग_डेटा,FILE*फायल_प्रवेश){return fwrite(स्ट्रिंग_डेटा,1,strlen(स्ट्रिंग_डेटा),फायल_प्रवेश)==strlen(स्ट्रिंग_डेटा)?0:EOF;}
static void 넣기(char*मेजप_डेटा,size_t 용량한도,size_t*현재위치,char वर्ण_कोड){if(*현재위치+1<용량한도)मेजप_डेटा[*현재위치]=वर्ण_कोड;(*현재위치)++;}
int vsnprintf(char*मेजप_डेटा,size_t 용량한도,const char*स्वरूप,va_list 가변인수){
    size_t 현재위치=0;while(*स्वरूप){if(*स्वरूप!='%'){넣기(मेजप_डेटा,용량한도,&현재위치,*स्वरूप++);continue;}स्वरूप++;
        int 왼쪽=0,영값=0,대체값=0;while(*स्वरूप=='-'||*स्वरूप=='0'||*स्वरूप=='#'||*स्वरूप=='+'||*स्वरूप==' '){if(*स्वरूप=='-')왼쪽=1;if(*स्वरूप=='0')영값=1;if(*स्वरूप=='#')대체값=1;स्वरूप++;}
        int 너비=0,정밀도=-1;if(*स्वरूप=='*'){너비=va_arg(가변인수,int);स्वरूप++;}else while(*स्वरूप>='0'&&*स्वरूप<='9')너비=너비*10+*स्वरूप++-'0';
        if(*स्वरूप=='.'){स्वरूप++;정밀도=0;if(*स्वरूप=='*'){정밀도=va_arg(가변인수,int);स्वरूप++;}else while(*स्वरूप>='0'&&*स्वरूप<='9')정밀도=정밀도*10+*स्वरूप++-'0';}
        int 넓은글자=0;while(*स्वरूप=='l'||*स्वरूप=='z'||*स्वरूप=='t'||*स्वरूप=='j'||*स्वरूप=='h'){if(*स्वरूप!='h')넓은글자=1;स्वरूप++;}
        char TYPE_वर्ग=*स्वरूप?*स्वरूप++:0,बफर_सांठवण[80];const char*स्ट्रिंग_डेटा=बफर_सांठवण;size_t आयटम_COUNT=0;
        if(TYPE_वर्ग=='s'){स्ट्रिंग_डेटा=va_arg(가변인수,const char*);if(!स्ट्रिंग_डेटा)स्ट्रिंग_डेटा="(null)";आयटम_COUNT=strlen(स्ट्रिंग_डेटा);if(정밀도>=0&&आयटम_COUNT>(size_t)정밀도)आयटम_COUNT=정밀도;}
        else if(TYPE_वर्ग=='c'){बफर_सांठवण[0]=va_arg(가변인수,int);आयटम_COUNT=1;}
        else if(TYPE_वर्ग=='%'){बफर_सांठवण[0]='%';आयटम_COUNT=1;}
        else if(TYPE_वर्ग=='d'||TYPE_वर्ग=='i'||TYPE_वर्ग=='u'||TYPE_वर्ग=='x'||TYPE_वर्ग=='X'||TYPE_वर्ग=='o'||TYPE_वर्ग=='p'){
            unsigned long long मोल;int 음수표시=0;
            if(TYPE_वर्ग=='d'||TYPE_वर्ग=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;मोल=음수표시?0-(unsigned long long)임시값:임시값;}
            else मोल=TYPE_वर्ग=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned फाटभूंय_मोल=TYPE_वर्ग=='x'||TYPE_वर्ग=='X'||TYPE_वर्ग=='p'?16:TYPE_वर्ग=='o'?8:10;char अंक_COUNT[64];unsigned 사용량=0;
            do{अंक_COUNT[사용량++]="0123456789abcdef"[मोल%फाटभूंय_मोल];मोल/=फाटभूंय_मोल;}while(मोल);
            if(음수표시)बफर_सांठवण[आयटम_COUNT++]='-';if(TYPE_वर्ग=='p'||(대체값&&फाटभूंय_मोल==16)){बफर_सांठवण[आयटम_COUNT++]='0';बफर_सांठवण[आयटम_COUNT++]='x';}
            for(int भरण_मोल=(int)사용량;정밀도>भरण_मोल&&आयटम_COUNT<sizeof(बफर_सांठवण)-사용량;भरण_मोल++)बफर_सांठवण[आयटम_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(आयटम_COUNT+사용량)&&आयटम_COUNT<sizeof(बफर_सांठवण)-사용량)बफर_सांठवण[आयटम_COUNT++]='0';
            while(사용량)बफर_सांठवण[आयटम_COUNT++]=अंक_COUNT[--사용량];
        }else{बफर_सांठवण[0]='?';आयटम_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)आयटम_COUNT){넣기(मेजप_डेटा,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<आयटम_COUNT;순번++)넣기(मेजप_डेटा,용량한도,&현재위치,स्ट्रिंग_डेटा[순번]);while(왼쪽&&너비>(int)आयटम_COUNT){넣기(मेजप_डेटा,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)मेजप_डेटा[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*मेजप_डेटा,size_t 용량한도,const char*फायल_प्रवेश,...){va_list 첫째값;va_start(첫째값,फायल_प्रवेश);int 반환값=vsnprintf(मेजप_डेटा,용량한도,फायल_प्रवेश,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*मेजप_डेटा,const char*फायल_प्रवेश,...){va_list 첫째값;va_start(첫째값,फायल_प्रवेश);int 반환값=vsnprintf(मेजप_डेटा,SIZE_MAX,फायल_प्रवेश,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_मोल,const char*फायल_प्रवेश,va_list 첫째값){char SECOND_मोल[2048];int आयटम_COUNT=vsnprintf(SECOND_मोल,sizeof(SECOND_मोल),फायल_प्रवेश,첫째값);if(आयटम_COUNT>2047)आयटम_COUNT=2047;return fwrite(SECOND_मोल,1,आयटम_COUNT,Stream_मोल)==(size_t)आयटम_COUNT?आयटम_COUNT:-1;}
int fprintf(FILE*Stream_मोल,const char*फायल_प्रवेश,...){va_list 첫째값;va_start(첫째값,फायल_प्रवेश);int 반환값=vfprintf(Stream_मोल,फायल_प्रवेश,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*फायल_प्रवेश,...){va_list 첫째값;va_start(첫째값,फायल_प्रवेश);int 반환값=vfprintf(stdout,फायल_प्रवेश,첫째값);va_end(첫째값);return 반환값;}
