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
static int juumre;
int *__errno_location(void){return &juumre;}
void exit(int ngonka_njaru){사용자호출(6,ngonka_njaru,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *검사식,const char *fiilde,unsigned diidol,const char *함수이름){fprintf(stderr,"cc assertion: %s %s:%u %s\n",검사식,fiilde,diidol,함수이름);exit(1);}
size_t strlen(const char*ɓoggol_keɓe){const char*자료위치=ɓoggol_keɓe;while(*자료위치)자료위치++;return 자료위치-ɓoggol_keɓe;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char 가로좌표=*첫째값++,세로좌표=*둘째값++;if(가로좌표!=세로좌표)return 가로좌표-세로좌표;if(!가로좌표)return 0;}return 0;}
char *strcpy(char*tiindaare_keɓe,const char*ɓoggol_keɓe){char*반환값=tiindaare_keɓe;while((*tiindaare_keɓe++=*ɓoggol_keɓe++)){}return 반환값;}
char *strchr(const char*ɓoggol_keɓe,int 문자값){do{if(*ɓoggol_keɓe==(char)문자값)return (char*)ɓoggol_keɓe;}while(*ɓoggol_keɓe++);return 0;}
char *strrchr(const char*ɓoggol_keɓe,int 문자값){const char*반환값=0;do{if(*ɓoggol_keɓe==(char)문자값)반환값=ɓoggol_keɓe;}while(*ɓoggol_keɓe++);return (char*)반환값;}
char *strstr(const char*ɓoggol_keɓe,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*ɓoggol_keɓe;ɓoggol_keɓe++)if(!strncmp(ɓoggol_keɓe,터미널항목,개수))return (char*)ɓoggol_keɓe;return 개수?0:(char*)ɓoggol_keɓe;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*가로좌표=첫째값,*세로좌표=둘째값;while(개수--){if(*가로좌표!=*세로좌표)return *가로좌표-*세로좌표;가로좌표++;세로좌표++;}return 0;}
void *memmove(void*tiindaare_keɓe,const void*ɓoggol_keɓe,size_t 개수){unsigned char*가로좌표=tiindaare_keɓe;const unsigned char*세로좌표=ɓoggol_keɓe;if(가로좌표<세로좌표){for(size_t 순번=0;순번<개수;순번++)가로좌표[순번]=세로좌표[순번];}else while(개수){개수--;가로좌표[개수]=세로좌표[개수];}return tiindaare_keɓe;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct 자료덩이 {size_t waylude_etannde;struct 자료덩이*다음;int 남은공간;int 채울크기;uint64_t ponndugol_ngootoñ;} 자료덩이;
static 자료덩이 *첫항목;
void free(void*자료위치){if(!자료위치)return;자료덩이*둘째값=(자료덩이*)자료위치-1;둘째값->남은공간=1;for(자료덩이*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->waylude_etannde+=sizeof(자료덩이)+다음위치->다음->waylude_etannde;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(자료덩이))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(자료덩이*)할당마당;첫항목->waylude_etannde=sizeof(할당마당)-sizeof(자료덩이);첫항목->남은공간=1;첫항목->다음=0;}
    자료덩이*이전=자료위치?(자료덩이*)자료위치-1:0;if(이전&&이전->waylude_etannde>=개수)return 자료위치;
    for(자료덩이*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->waylude_etannde>=개수){
        if(둘째값->waylude_etannde>=개수+sizeof(자료덩이)+16){자료덩이*나머지부분=(자료덩이*)((unsigned char*)(둘째값+1)+개수);나머지부분->waylude_etannde=둘째값->waylude_etannde-개수-sizeof(자료덩이);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->waylude_etannde=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->waylude_etannde);free(자료위치);}return 반환값;
    }juumre=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t ɓoggol_keɓe){if(ɓoggol_keɓe&&개수>SIZE_MAX/ɓoggol_keɓe)return 0;void*자료위치=malloc(개수*ɓoggol_keɓe);if(자료위치)memset(자료위치,0,개수*ɓoggol_keɓe);return 자료위치;}
unsigned long long strtoull(const char*ɓoggol_keɓe,char**끝위치,int cakkital_njaru){
    const char*시작위치=ɓoggol_keɓe;while(*ɓoggol_keɓe==' '||(*ɓoggol_keɓe>=9&&*ɓoggol_keɓe<=13))ɓoggol_keɓe++;int 음수여부=0;if(*ɓoggol_keɓe=='-'||*ɓoggol_keɓe=='+')음수여부=*ɓoggol_keɓe++=='-';
    if((!cakkital_njaru||cakkital_njaru==16)&&ɓoggol_keɓe[0]=='0'&&(ɓoggol_keɓe[1]=='x'||ɓoggol_keɓe[1]=='X')){cakkital_njaru=16;ɓoggol_keɓe+=2;}if(!cakkital_njaru)cakkital_njaru=*ɓoggol_keɓe=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned 문자값=*ɓoggol_keɓe,tiindaare_keɓe=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='z'?문자값-'a'+10:문자값>='A'&&문자값<='Z'?문자값-'A'+10:99;if(tiindaare_keɓe>=(unsigned)cakkital_njaru)break;하나라도=1;ɓoggol_keɓe++;if(임시값>(~0ull-tiindaare_keɓe)/(unsigned)cakkital_njaru){임시값=~0ull;juumre=34;}else 임시값=임시값*cakkital_njaru+tiindaare_keɓe;}
    if(끝위치)*끝위치=(char*)(하나라도?ɓoggol_keɓe:시작위치);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*ɓoggol_keɓe,char**보조항목,int 둘째값){return strtoull(ɓoggol_keɓe,보조항목,둘째값);}
long strtol(const char*ɓoggol_keɓe,char**보조항목,int 둘째값){return (long)strtoull(ɓoggol_keɓe,보조항목,둘째값);}
int atoi(const char*ɓoggol_keɓe){return (int)strtol(ɓoggol_keɓe,0,10);}
long double ldexpl(long double 가로좌표,int 개수){while(개수>0){가로좌표*=2;개수--;}while(개수<0){가로좌표/=2;개수++;}return 가로좌표;}
long double strtold(const char*ɓoggol_keɓe,char**끝위치){
    const char*시작위치=ɓoggol_keɓe;while(*ɓoggol_keɓe==' '||(*ɓoggol_keɓe>=9&&*ɓoggol_keɓe<=13))ɓoggol_keɓe++;int 음수여부=0;if(*ɓoggol_keɓe=='-'||*ɓoggol_keɓe=='+')음수여부=*ɓoggol_keɓe++=='-';
    int cakkital_njaru=10;if(ɓoggol_keɓe[0]=='0'&&(ɓoggol_keɓe[1]=='x'||ɓoggol_keɓe[1]=='X')){cakkital_njaru=16;ɓoggol_keɓe+=2;}long double 임시값=0,fonnditde=1;int 소수부=0,하나라도=0;
    for(;;){int 문자값=*ɓoggol_keɓe,tiindaare_keɓe=문자값>='0'&&문자값<='9'?문자값-'0':문자값>='a'&&문자값<='f'?문자값-'a'+10:문자값>='A'&&문자값<='F'?문자값-'A'+10:99;
        if(문자값=='.'&&!소수부){소수부=1;ɓoggol_keɓe++;continue;}if(tiindaare_keɓe>=cakkital_njaru)break;하나라도=1;ɓoggol_keɓe++;임시값=임시값*cakkital_njaru+tiindaare_keɓe;if(소수부)fonnditde*=cakkital_njaru;
    }임시값/=fonnditde;
    if((cakkital_njaru==10&&(*ɓoggol_keɓe=='e'||*ɓoggol_keɓe=='E'))||(cakkital_njaru==16&&(*ɓoggol_keɓe=='p'||*ɓoggol_keɓe=='P'))){const char*hollirde_njaru=ɓoggol_keɓe++;int 빼기=0;if(*ɓoggol_keɓe=='-'||*ɓoggol_keɓe=='+')빼기=*ɓoggol_keɓe++=='-';int 개수=0,항목수=0;while(*ɓoggol_keɓe>='0'&&*ɓoggol_keɓe<='9'){항목수++;if(개수<20000)개수=개수*10+*ɓoggol_keɓe-'0';ɓoggol_keɓe++;}if(!항목수)ɓoggol_keɓe=hollirde_njaru;else{long double 배율=cakkital_njaru==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/배율:임시값*배율;}}
    if(끝위치)*끝위치=(char*)(하나라도?ɓoggol_keɓe:시작위치);return 음수여부?-임시값:임시값;
}
double strtod(const char*ɓoggol_keɓe,char**보조항목){return (double)strtold(ɓoggol_keɓe,보조항목);}float strtof(const char*ɓoggol_keɓe,char**보조항목){return (float)strtold(ɓoggol_keɓe,보조항목);}
void qsort(void*cakkital_njaru,size_t 개수,size_t waylude_etannde,int(*yerondirde)(const void*,const void*)){
    unsigned char*자료위치=cakkital_njaru;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&yerondirde(자료위치+(안쪽순번-1)*waylude_etannde,자료위치+안쪽순번*waylude_etannde)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<waylude_etannde;셋째순번++){unsigned char 문자값=자료위치[(안쪽순번-1)*waylude_etannde+셋째순번];자료위치[(안쪽순번-1)*waylude_etannde+셋째순번]=자료위치[안쪽순번*waylude_etannde+셋째순번];자료위치[안쪽순번*waylude_etannde+셋째순번]=문자값;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*innde,int 설정비트,...){
    if(!strcmp(innde,"/@cc-output")){if(출력열림){juumre=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(innde,번역기자원들[순번].innde)){
        if(설정비트&3){juumre=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}juumre=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)innde,설정비트,0,0,0,0);if(반환값<0){juumre=-반환값;return -1;}return 반환값;
}
int close(int fiilde_jaggoode){if(fiilde_jaggoode==100){출력열림=0;return 0;}if(fiilde_jaggoode>=128&&fiilde_jaggoode<152){열림[fiilde_jaggoode-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fiilde_jaggoode,0,0,0,0,0);if(반환값<0){juumre=-반환값;return -1;}return 0;}
long read(int fiilde_jaggoode,void*keɓe,size_t 개수){
    if(fiilde_jaggoode>=128&&fiilde_jaggoode<152&&열림[fiilde_jaggoode-128].사용량){int 순번=fiilde_jaggoode-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->waylude_etannde-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(keɓe,반환값->keɓe+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,fiilde_jaggoode,(uintptr_t)keɓe,개수,0,0,0);if(반환값<0){juumre=-반환값;return -1;}return 반환값;
}
long write(int fiilde_jaggoode,const void*keɓe,size_t 개수){
    if(fiilde_jaggoode==100){if(개수>sizeof(출력결과)-출력위치){juumre=28;return -1;}memcpy(출력결과+출력위치,keɓe,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,fiilde_jaggoode,(uintptr_t)keɓe,개수,0,0,0);if(반환값<0){juumre=-반환값;return -1;}return 반환값;
}
long lseek(int fiilde_jaggoode,long 변위,int 기준점){
    if(fiilde_jaggoode==100){long 자료위치=변위+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){juumre=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(fiilde_jaggoode>=128&&fiilde_jaggoode<152&&열림[fiilde_jaggoode-128].사용량){int 순번=fiilde_jaggoode-128;long 자료위치=변위+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].waylude_etannde);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].waylude_etannde){juumre=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,fiilde_jaggoode,변위,기준점,0,0,0);if(반환값<0){juumre=-반환값;return -1;}return 반환값;
}
int unlink(const char*innde){intptr_t 반환값=사용자호출(11,(uintptr_t)innde,0,0,0,0,0);if(반환값<0){juumre=-반환값;return -1;}return 반환값;}
char *realpath(const char*innde,char*결과자료){if(!결과자료){결과자료=malloc(strlen(innde)+1);if(!결과자료)return 0;}return strcpy(결과자료,innde);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){juumre=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int fiilde_jaggoode,const char*방식){(void)방식;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].juumre=0;흐름목록[순번].fiilde_jaggoode=fiilde_jaggoode;return &흐름목록[순번];}juumre=24;return 0;}
int fflush(FILE*fiilde_naatnugol){return fiilde_naatnugol&&fiilde_naatnugol->juumre?-1:0;}
int fclose(FILE*fiilde_naatnugol){int 반환값=close(fiilde_naatnugol->fiilde_jaggoode);if(fiilde_naatnugol->juumre)반환값=-1;fiilde_naatnugol->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t ɓoggol_keɓe,size_t 개수,FILE*fiilde_naatnugol){if(!ɓoggol_keɓe)return 0;if(개수>SIZE_MAX/ɓoggol_keɓe){fiilde_naatnugol->juumre=1;return 0;}long 반환값=write(fiilde_naatnugol->fiilde_jaggoode,자료위치,ɓoggol_keɓe*개수);if(반환값<0){fiilde_naatnugol->juumre=1;return 0;}return (size_t)반환값/ɓoggol_keɓe;}
int fputc(int 문자값,FILE*fiilde_naatnugol){unsigned char 둘째값=문자값;return fwrite(&둘째값,1,1,fiilde_naatnugol)==1?둘째값:EOF;}
int fputs(const char*ɓoggol_keɓe,FILE*fiilde_naatnugol){return fwrite(ɓoggol_keɓe,1,strlen(ɓoggol_keɓe),fiilde_naatnugol)==strlen(ɓoggol_keɓe)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char 문자값){if(*현재위치+1<용량한도)결과자료[*현재위치]=문자값;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*formaa,va_list 가변인수){
    size_t 현재위치=0;while(*formaa){if(*formaa!='%'){넣기(결과자료,용량한도,&현재위치,*formaa++);continue;}formaa++;
        int 왼쪽=0,영값=0,대체값=0;while(*formaa=='-'||*formaa=='0'||*formaa=='#'||*formaa=='+'||*formaa==' '){if(*formaa=='-')왼쪽=1;if(*formaa=='0')영값=1;if(*formaa=='#')대체값=1;formaa++;}
        int 너비=0,정밀도=-1;if(*formaa=='*'){너비=va_arg(가변인수,int);formaa++;}else while(*formaa>='0'&&*formaa<='9')너비=너비*10+*formaa++-'0';
        if(*formaa=='.'){formaa++;정밀도=0;if(*formaa=='*'){정밀도=va_arg(가변인수,int);formaa++;}else while(*formaa>='0'&&*formaa<='9')정밀도=정밀도*10+*formaa++-'0';}
        int 넓은글자=0;while(*formaa=='l'||*formaa=='z'||*formaa=='t'||*formaa=='j'||*formaa=='h'){if(*formaa!='h')넓은글자=1;formaa++;}
        char 유형=*formaa?*formaa++:0,완충공간[80];const char*ɓoggol_keɓe=완충공간;size_t 개수=0;
        if(유형=='s'){ɓoggol_keɓe=va_arg(가변인수,const char*);if(!ɓoggol_keɓe)ɓoggol_keɓe="(null)";개수=strlen(ɓoggol_keɓe);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(유형=='c'){완충공간[0]=va_arg(가변인수,int);개수=1;}
        else if(유형=='%'){완충공간[0]='%';개수=1;}
        else if(유형=='d'||유형=='i'||유형=='u'||유형=='x'||유형=='X'||유형=='o'||유형=='p'){
            unsigned long long njaru;int 음수표시=0;
            if(유형=='d'||유형=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;njaru=음수표시?0-(unsigned long long)임시값:임시값;}
            else njaru=유형=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned cakkital_njaru=유형=='x'||유형=='X'||유형=='p'?16:유형=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[njaru%cakkital_njaru];njaru/=cakkital_njaru;}while(njaru);
            if(음수표시)완충공간[개수++]='-';if(유형=='p'||(대체값&&cakkital_njaru==16)){완충공간[개수++]='0';완충공간[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(완충공간)-사용량;채움++)완충공간[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(완충공간)-사용량)완충공간[개수++]='0';
            while(사용량)완충공간[개수++]=숫자수[--사용량];
        }else{완충공간[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,ɓoggol_keɓe[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*fiilde_naatnugol,...){va_list 첫째값;va_start(첫째값,fiilde_naatnugol);int 반환값=vsnprintf(결과자료,용량한도,fiilde_naatnugol,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*fiilde_naatnugol,...){va_list 첫째값;va_start(첫째값,fiilde_naatnugol);int 반환값=vsnprintf(결과자료,SIZE_MAX,fiilde_naatnugol,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*waraango_njaru,const char*fiilde_naatnugol,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),fiilde_naatnugol,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,waraango_njaru)==(size_t)개수?개수:-1;}
int fprintf(FILE*waraango_njaru,const char*fiilde_naatnugol,...){va_list 첫째값;va_start(첫째값,fiilde_naatnugol);int 반환값=vfprintf(waraango_njaru,fiilde_naatnugol,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fiilde_naatnugol,...){va_list 첫째값;va_start(첫째값,fiilde_naatnugol);int 반환값=vfprintf(stdout,fiilde_naatnugol,첫째값);va_end(첫째값);return 반환값;}
