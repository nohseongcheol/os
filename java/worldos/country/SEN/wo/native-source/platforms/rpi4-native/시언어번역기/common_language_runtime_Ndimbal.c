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
static int njumte;
int *__errno_location(void){return &njumte;}
void exit(int nekkin_xëyma){사용자호출(6,nekkin_xëyma,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *sek_guddalinu_méngale,const char *bara_denc,unsigned buum,const char *doxalin_dugal_xabaar_tur){fprintf(stderr,"cc assertion: %s %s:%u %s\n",sek_guddalinu_méngale,bara_denc,buum,doxalin_dugal_xabaar_tur);exit(1);}
size_t strlen(const char*araf_yu_bennoo_mbir){const char*자료위치=araf_yu_bennoo_mbir;while(*자료위치)자료위치++;return 자료위치-araf_yu_bennoo_mbir;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char rëddu_iks_yi=*첫째값++,세로좌표=*둘째값++;if(rëddu_iks_yi!=세로좌표)return rëddu_iks_yi-세로좌표;if(!rëddu_iks_yi)return 0;}return 0;}
char *strcpy(char*jëmmukaay_mbir,const char*araf_yu_bennoo_mbir){char*반환값=jëmmukaay_mbir;while((*jëmmukaay_mbir++=*araf_yu_bennoo_mbir++)){}return 반환값;}
char *strchr(const char*araf_yu_bennoo_mbir,int kotu_araf){do{if(*araf_yu_bennoo_mbir==(char)kotu_araf)return (char*)araf_yu_bennoo_mbir;}while(*araf_yu_bennoo_mbir++);return 0;}
char *strrchr(const char*araf_yu_bennoo_mbir,int kotu_araf){const char*반환값=0;do{if(*araf_yu_bennoo_mbir==(char)kotu_araf)반환값=araf_yu_bennoo_mbir;}while(*araf_yu_bennoo_mbir++);return (char*)반환값;}
char *strstr(const char*araf_yu_bennoo_mbir,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*araf_yu_bennoo_mbir;araf_yu_bennoo_mbir++)if(!strncmp(araf_yu_bennoo_mbir,터미널항목,개수))return (char*)araf_yu_bennoo_mbir;return 개수?0:(char*)araf_yu_bennoo_mbir;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*rëddu_iks_yi=첫째값,*세로좌표=둘째값;while(개수--){if(*rëddu_iks_yi!=*세로좌표)return *rëddu_iks_yi-*세로좌표;rëddu_iks_yi++;세로좌표++;}return 0;}
void *memmove(void*jëmmukaay_mbir,const void*araf_yu_bennoo_mbir,size_t 개수){unsigned char*rëddu_iks_yi=jëmmukaay_mbir;const unsigned char*세로좌표=araf_yu_bennoo_mbir;if(rëddu_iks_yi<세로좌표){for(size_t 순번=0;순번<개수;순번++)rëddu_iks_yi[순번]=세로좌표[순번];}else while(개수){개수--;rëddu_iks_yi[개수]=세로좌표[개수];}return jëmmukaay_mbir;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct mbir_gatandu {size_t tolluwaay;struct mbir_gatandu*다음;int 남은공간;int 채울크기;uint64_t Péete_sa;} mbir_gatandu;
static mbir_gatandu *첫항목;
void free(void*자료위치){if(!자료위치)return;mbir_gatandu*둘째값=(mbir_gatandu*)자료위치-1;둘째값->남은공간=1;for(mbir_gatandu*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->tolluwaay+=sizeof(mbir_gatandu)+다음위치->다음->tolluwaay;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(mbir_gatandu))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(mbir_gatandu*)할당마당;첫항목->tolluwaay=sizeof(할당마당)-sizeof(mbir_gatandu);첫항목->남은공간=1;첫항목->다음=0;}
    mbir_gatandu*이전=자료위치?(mbir_gatandu*)자료위치-1:0;if(이전&&이전->tolluwaay>=개수)return 자료위치;
    for(mbir_gatandu*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->tolluwaay>=개수){
        if(둘째값->tolluwaay>=개수+sizeof(mbir_gatandu)+16){mbir_gatandu*나머지부분=(mbir_gatandu*)((unsigned char*)(둘째값+1)+개수);나머지부분->tolluwaay=둘째값->tolluwaay-개수-sizeof(mbir_gatandu);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->tolluwaay=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->tolluwaay);free(자료위치);}return 반환값;
    }njumte=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t araf_yu_bennoo_mbir){if(araf_yu_bennoo_mbir&&개수>SIZE_MAX/araf_yu_bennoo_mbir)return 0;void*자료위치=malloc(개수*araf_yu_bennoo_mbir);if(자료위치)memset(자료위치,0,개수*araf_yu_bennoo_mbir);return 자료위치;}
unsigned long long strtoull(const char*araf_yu_bennoo_mbir,char**jeexal_Randal,int Njiitlay_xëyma){
    const char*Door_Randal=araf_yu_bennoo_mbir;while(*araf_yu_bennoo_mbir==' '||(*araf_yu_bennoo_mbir>=9&&*araf_yu_bennoo_mbir<=13))araf_yu_bennoo_mbir++;int 음수여부=0;if(*araf_yu_bennoo_mbir=='-'||*araf_yu_bennoo_mbir=='+')음수여부=*araf_yu_bennoo_mbir++=='-';
    if((!Njiitlay_xëyma||Njiitlay_xëyma==16)&&araf_yu_bennoo_mbir[0]=='0'&&(araf_yu_bennoo_mbir[1]=='x'||araf_yu_bennoo_mbir[1]=='X')){Njiitlay_xëyma=16;araf_yu_bennoo_mbir+=2;}if(!Njiitlay_xëyma)Njiitlay_xëyma=*araf_yu_bennoo_mbir=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kotu_araf=*araf_yu_bennoo_mbir,jëmmukaay_mbir=kotu_araf>='0'&&kotu_araf<='9'?kotu_araf-'0':kotu_araf>='a'&&kotu_araf<='z'?kotu_araf-'a'+10:kotu_araf>='A'&&kotu_araf<='Z'?kotu_araf-'A'+10:99;if(jëmmukaay_mbir>=(unsigned)Njiitlay_xëyma)break;하나라도=1;araf_yu_bennoo_mbir++;if(임시값>(~0ull-jëmmukaay_mbir)/(unsigned)Njiitlay_xëyma){임시값=~0ull;njumte=34;}else 임시값=임시값*Njiitlay_xëyma+jëmmukaay_mbir;}
    if(jeexal_Randal)*jeexal_Randal=(char*)(하나라도?araf_yu_bennoo_mbir:Door_Randal);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*araf_yu_bennoo_mbir,char**보조항목,int 둘째값){return strtoull(araf_yu_bennoo_mbir,보조항목,둘째값);}
long strtol(const char*araf_yu_bennoo_mbir,char**보조항목,int 둘째값){return (long)strtoull(araf_yu_bennoo_mbir,보조항목,둘째값);}
int atoi(const char*araf_yu_bennoo_mbir){return (int)strtol(araf_yu_bennoo_mbir,0,10);}
long double ldexpl(long double rëddu_iks_yi,int 개수){while(개수>0){rëddu_iks_yi*=2;개수--;}while(개수<0){rëddu_iks_yi/=2;개수++;}return rëddu_iks_yi;}
long double strtold(const char*araf_yu_bennoo_mbir,char**jeexal_Randal){
    const char*Door_Randal=araf_yu_bennoo_mbir;while(*araf_yu_bennoo_mbir==' '||(*araf_yu_bennoo_mbir>=9&&*araf_yu_bennoo_mbir<=13))araf_yu_bennoo_mbir++;int 음수여부=0;if(*araf_yu_bennoo_mbir=='-'||*araf_yu_bennoo_mbir=='+')음수여부=*araf_yu_bennoo_mbir++=='-';
    int Njiitlay_xëyma=10;if(araf_yu_bennoo_mbir[0]=='0'&&(araf_yu_bennoo_mbir[1]=='x'||araf_yu_bennoo_mbir[1]=='X')){Njiitlay_xëyma=16;araf_yu_bennoo_mbir+=2;}long double 임시값=0,Tolloole=1;int 소수부=0,하나라도=0;
    for(;;){int kotu_araf=*araf_yu_bennoo_mbir,jëmmukaay_mbir=kotu_araf>='0'&&kotu_araf<='9'?kotu_araf-'0':kotu_araf>='a'&&kotu_araf<='f'?kotu_araf-'a'+10:kotu_araf>='A'&&kotu_araf<='F'?kotu_araf-'A'+10:99;
        if(kotu_araf=='.'&&!소수부){소수부=1;araf_yu_bennoo_mbir++;continue;}if(jëmmukaay_mbir>=Njiitlay_xëyma)break;하나라도=1;araf_yu_bennoo_mbir++;임시값=임시값*Njiitlay_xëyma+jëmmukaay_mbir;if(소수부)Tolloole*=Njiitlay_xëyma;
    }임시값/=Tolloole;
    if((Njiitlay_xëyma==10&&(*araf_yu_bennoo_mbir=='e'||*araf_yu_bennoo_mbir=='E'))||(Njiitlay_xëyma==16&&(*araf_yu_bennoo_mbir=='p'||*araf_yu_bennoo_mbir=='P'))){const char*féeñal_xëyma=araf_yu_bennoo_mbir++;int 빼기=0;if(*araf_yu_bennoo_mbir=='-'||*araf_yu_bennoo_mbir=='+')빼기=*araf_yu_bennoo_mbir++=='-';int 개수=0,항목수=0;while(*araf_yu_bennoo_mbir>='0'&&*araf_yu_bennoo_mbir<='9'){항목수++;if(개수<20000)개수=개수*10+*araf_yu_bennoo_mbir-'0';araf_yu_bennoo_mbir++;}if(!항목수)araf_yu_bennoo_mbir=féeñal_xëyma;else{long double faktër=Njiitlay_xëyma==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/faktër:임시값*faktër;}}
    if(jeexal_Randal)*jeexal_Randal=(char*)(하나라도?araf_yu_bennoo_mbir:Door_Randal);return 음수여부?-임시값:임시값;
}
double strtod(const char*araf_yu_bennoo_mbir,char**보조항목){return (double)strtold(araf_yu_bennoo_mbir,보조항목);}float strtof(const char*araf_yu_bennoo_mbir,char**보조항목){return (float)strtold(araf_yu_bennoo_mbir,보조항목);}
void qsort(void*Njiitlay_xëyma,size_t 개수,size_t tolluwaay,int(*Nàtt)(const void*,const void*)){
    unsigned char*자료위치=Njiitlay_xëyma;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Nàtt(자료위치+(안쪽순번-1)*tolluwaay,자료위치+안쪽순번*tolluwaay)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<tolluwaay;셋째순번++){unsigned char kotu_araf=자료위치[(안쪽순번-1)*tolluwaay+셋째순번];자료위치[(안쪽순번-1)*tolluwaay+셋째순번]=자료위치[안쪽순번*tolluwaay+셋째순번];자료위치[안쪽순번*tolluwaay+셋째순번]=kotu_araf;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*tur_253d1510,int 설정비트,...){
    if(!strcmp(tur_253d1510,"/@cc-output")){if(출력열림){njumte=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(tur_253d1510,번역기자원들[순번].tur_253d1510)){
        if(설정비트&3){njumte=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}njumte=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)tur_253d1510,설정비트,0,0,0,0);if(반환값<0){njumte=-반환값;return -1;}return 반환값;
}
int close(int bara_denc_yombal){if(bara_denc_yombal==100){출력열림=0;return 0;}if(bara_denc_yombal>=128&&bara_denc_yombal<152){열림[bara_denc_yombal-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,bara_denc_yombal,0,0,0,0,0);if(반환값<0){njumte=-반환값;return -1;}return 0;}
long read(int bara_denc_yombal,void*mbir,size_t 개수){
    if(bara_denc_yombal>=128&&bara_denc_yombal<152&&열림[bara_denc_yombal-128].사용량){int 순번=bara_denc_yombal-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->tolluwaay-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(mbir,반환값->mbir+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,bara_denc_yombal,(uintptr_t)mbir,개수,0,0,0);if(반환값<0){njumte=-반환값;return -1;}return 반환값;
}
long write(int bara_denc_yombal,const void*mbir,size_t 개수){
    if(bara_denc_yombal==100){if(개수>sizeof(출력결과)-출력위치){njumte=28;return -1;}memcpy(출력결과+출력위치,mbir,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,bara_denc_yombal,(uintptr_t)mbir,개수,0,0,0);if(반환값<0){njumte=-반환값;return -1;}return 반환값;
}
long lseek(int bara_denc_yombal,long Randal_xëyma,int 기준점){
    if(bara_denc_yombal==100){long 자료위치=Randal_xëyma+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){njumte=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(bara_denc_yombal>=128&&bara_denc_yombal<152&&열림[bara_denc_yombal-128].사용량){int 순번=bara_denc_yombal-128;long 자료위치=Randal_xëyma+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].tolluwaay);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].tolluwaay){njumte=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,bara_denc_yombal,Randal_xëyma,기준점,0,0,0);if(반환값<0){njumte=-반환값;return -1;}return 반환값;
}
int unlink(const char*tur_253d1510){intptr_t 반환값=사용자호출(11,(uintptr_t)tur_253d1510,0,0,0,0,0);if(반환값<0){njumte=-반환값;return -1;}return 반환값;}
char *realpath(const char*tur_253d1510,char*결과자료){if(!결과자료){결과자료=malloc(strlen(tur_253d1510)+1);if(!결과자료)return 0;}return strcpy(결과자료,tur_253d1510);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){njumte=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int bara_denc_yombal,const char*doxalin_anam){(void)doxalin_anam;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].njumte=0;흐름목록[순번].bara_denc_yombal=bara_denc_yombal;return &흐름목록[순번];}njumte=24;return 0;}
int fflush(FILE*bara_denc_dugal_xabaar){return bara_denc_dugal_xabaar&&bara_denc_dugal_xabaar->njumte?-1:0;}
int fclose(FILE*bara_denc_dugal_xabaar){int 반환값=close(bara_denc_dugal_xabaar->bara_denc_yombal);if(bara_denc_dugal_xabaar->njumte)반환값=-1;bara_denc_dugal_xabaar->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t araf_yu_bennoo_mbir,size_t 개수,FILE*bara_denc_dugal_xabaar){if(!araf_yu_bennoo_mbir)return 0;if(개수>SIZE_MAX/araf_yu_bennoo_mbir){bara_denc_dugal_xabaar->njumte=1;return 0;}long 반환값=write(bara_denc_dugal_xabaar->bara_denc_yombal,자료위치,araf_yu_bennoo_mbir*개수);if(반환값<0){bara_denc_dugal_xabaar->njumte=1;return 0;}return (size_t)반환값/araf_yu_bennoo_mbir;}
int fputc(int kotu_araf,FILE*bara_denc_dugal_xabaar){unsigned char 둘째값=kotu_araf;return fwrite(&둘째값,1,1,bara_denc_dugal_xabaar)==1?둘째값:EOF;}
int fputs(const char*araf_yu_bennoo_mbir,FILE*bara_denc_dugal_xabaar){return fwrite(araf_yu_bennoo_mbir,1,strlen(araf_yu_bennoo_mbir),bara_denc_dugal_xabaar)==strlen(araf_yu_bennoo_mbir)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char kotu_araf){if(*현재위치+1<용량한도)결과자료[*현재위치]=kotu_araf;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*dayo,va_list 가변인수){
    size_t 현재위치=0;while(*dayo){if(*dayo!='%'){넣기(결과자료,용량한도,&현재위치,*dayo++);continue;}dayo++;
        int 왼쪽=0,영값=0,대체값=0;while(*dayo=='-'||*dayo=='0'||*dayo=='#'||*dayo=='+'||*dayo==' '){if(*dayo=='-')왼쪽=1;if(*dayo=='0')영값=1;if(*dayo=='#')대체값=1;dayo++;}
        int 너비=0,정밀도=-1;if(*dayo=='*'){너비=va_arg(가변인수,int);dayo++;}else while(*dayo>='0'&&*dayo<='9')너비=너비*10+*dayo++-'0';
        if(*dayo=='.'){dayo++;정밀도=0;if(*dayo=='*'){정밀도=va_arg(가변인수,int);dayo++;}else while(*dayo>='0'&&*dayo<='9')정밀도=정밀도*10+*dayo++-'0';}
        int 넓은글자=0;while(*dayo=='l'||*dayo=='z'||*dayo=='t'||*dayo=='j'||*dayo=='h'){if(*dayo!='h')넓은글자=1;dayo++;}
        char xeet_ngiir=*dayo?*dayo++:0,dencandikaay_Dencukaay[80];const char*araf_yu_bennoo_mbir=dencandikaay_Dencukaay;size_t 개수=0;
        if(xeet_ngiir=='s'){araf_yu_bennoo_mbir=va_arg(가변인수,const char*);if(!araf_yu_bennoo_mbir)araf_yu_bennoo_mbir="(null)";개수=strlen(araf_yu_bennoo_mbir);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(xeet_ngiir=='c'){dencandikaay_Dencukaay[0]=va_arg(가변인수,int);개수=1;}
        else if(xeet_ngiir=='%'){dencandikaay_Dencukaay[0]='%';개수=1;}
        else if(xeet_ngiir=='d'||xeet_ngiir=='i'||xeet_ngiir=='u'||xeet_ngiir=='x'||xeet_ngiir=='X'||xeet_ngiir=='o'||xeet_ngiir=='p'){
            unsigned long long xëyma;int 음수표시=0;
            if(xeet_ngiir=='d'||xeet_ngiir=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;xëyma=음수표시?0-(unsigned long long)임시값:임시값;}
            else xëyma=xeet_ngiir=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Njiitlay_xëyma=xeet_ngiir=='x'||xeet_ngiir=='X'||xeet_ngiir=='p'?16:xeet_ngiir=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[xëyma%Njiitlay_xëyma];xëyma/=Njiitlay_xëyma;}while(xëyma);
            if(음수표시)dencandikaay_Dencukaay[개수++]='-';if(xeet_ngiir=='p'||(대체값&&Njiitlay_xëyma==16)){dencandikaay_Dencukaay[개수++]='0';dencandikaay_Dencukaay[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(dencandikaay_Dencukaay)-사용량;채움++)dencandikaay_Dencukaay[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(dencandikaay_Dencukaay)-사용량)dencandikaay_Dencukaay[개수++]='0';
            while(사용량)dencandikaay_Dencukaay[개수++]=숫자수[--사용량];
        }else{dencandikaay_Dencukaay[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,araf_yu_bennoo_mbir[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*bara_denc_dugal_xabaar,...){va_list 첫째값;va_start(첫째값,bara_denc_dugal_xabaar);int 반환값=vsnprintf(결과자료,용량한도,bara_denc_dugal_xabaar,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*bara_denc_dugal_xabaar,...){va_list 첫째값;va_start(첫째값,bara_denc_dugal_xabaar);int 반환값=vsnprintf(결과자료,SIZE_MAX,bara_denc_dugal_xabaar,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*dawal_xëyma,const char*bara_denc_dugal_xabaar,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),bara_denc_dugal_xabaar,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,dawal_xëyma)==(size_t)개수?개수:-1;}
int fprintf(FILE*dawal_xëyma,const char*bara_denc_dugal_xabaar,...){va_list 첫째값;va_start(첫째값,bara_denc_dugal_xabaar);int 반환값=vfprintf(dawal_xëyma,bara_denc_dugal_xabaar,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*bara_denc_dugal_xabaar,...){va_list 첫째값;va_start(첫째값,bara_denc_dugal_xabaar);int 반환값=vfprintf(stdout,bara_denc_dugal_xabaar,첫째값);va_end(첫째값);return 반환값;}
