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
static int tammarniq;
int *__errno_location(void){return &tammarniq;}
void exit(int qanuilinganiq_atuutilik){사용자호출(6,qanuilinganiq_atuutilik,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *qaujigiarli_uqarusiq,const char *ini,unsigned titikutaak,const char *함수이름){fprintf(stderr,"cc assertion: %s %s:%u %s\n",qaujigiarli_uqarusiq,ini,titikutaak,함수이름);exit(1);}
size_t strlen(const char*qimiaq_titiqqat){const char*자료위치=qimiaq_titiqqat;while(*자료위치)자료위치++;return 자료위치-qimiaq_titiqqat;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char 가로좌표=*첫째값++,세로좌표=*둘째값++;if(가로좌표!=세로좌표)return 가로좌표-세로좌표;if(!가로좌표)return 0;}return 0;}
char *strcpy(char*namunngarvik_titiqqat,const char*qimiaq_titiqqat){char*반환값=namunngarvik_titiqqat;while((*namunngarvik_titiqqat++=*qimiaq_titiqqat++)){}return 반환값;}
char *strchr(const char*qimiaq_titiqqat,int immikkuuqtumut_nalunaikkut){do{if(*qimiaq_titiqqat==(char)immikkuuqtumut_nalunaikkut)return (char*)qimiaq_titiqqat;}while(*qimiaq_titiqqat++);return 0;}
char *strrchr(const char*qimiaq_titiqqat,int immikkuuqtumut_nalunaikkut){const char*반환값=0;do{if(*qimiaq_titiqqat==(char)immikkuuqtumut_nalunaikkut)반환값=qimiaq_titiqqat;}while(*qimiaq_titiqqat++);return (char*)반환값;}
char *strstr(const char*qimiaq_titiqqat,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*qimiaq_titiqqat;qimiaq_titiqqat++)if(!strncmp(qimiaq_titiqqat,터미널항목,개수))return (char*)qimiaq_titiqqat;return 개수?0:(char*)qimiaq_titiqqat;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*가로좌표=첫째값,*세로좌표=둘째값;while(개수--){if(*가로좌표!=*세로좌표)return *가로좌표-*세로좌표;가로좌표++;세로좌표++;}return 0;}
void *memmove(void*namunngarvik_titiqqat,const void*qimiaq_titiqqat,size_t 개수){unsigned char*가로좌표=namunngarvik_titiqqat;const unsigned char*세로좌표=qimiaq_titiqqat;if(가로좌표<세로좌표){for(size_t 순번=0;순번<개수;순번++)가로좌표[순번]=세로좌표[순번];}else while(개수){개수--;가로좌표[개수]=세로좌표[개수];}return namunngarvik_titiqqat;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct titiqqat_sapummili {size_t anininga;struct titiqqat_sapummili*다음;int 남은공간;int 채울크기;uint64_t nalimunninga_atauttimiittut;} titiqqat_sapummili;
static titiqqat_sapummili *첫항목;
void free(void*자료위치){if(!자료위치)return;titiqqat_sapummili*둘째값=(titiqqat_sapummili*)자료위치-1;둘째값->남은공간=1;for(titiqqat_sapummili*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->anininga+=sizeof(titiqqat_sapummili)+다음위치->다음->anininga;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(할당마당)-sizeof(titiqqat_sapummili))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(titiqqat_sapummili*)할당마당;첫항목->anininga=sizeof(할당마당)-sizeof(titiqqat_sapummili);첫항목->남은공간=1;첫항목->다음=0;}
    titiqqat_sapummili*이전=자료위치?(titiqqat_sapummili*)자료위치-1:0;if(이전&&이전->anininga>=개수)return 자료위치;
    for(titiqqat_sapummili*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->anininga>=개수){
        if(둘째값->anininga>=개수+sizeof(titiqqat_sapummili)+16){titiqqat_sapummili*나머지부분=(titiqqat_sapummili*)((unsigned char*)(둘째값+1)+개수);나머지부분->anininga=둘째값->anininga-개수-sizeof(titiqqat_sapummili);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->anininga=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->anininga);free(자료위치);}return 반환값;
    }tammarniq=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t qimiaq_titiqqat){if(qimiaq_titiqqat&&개수>SIZE_MAX/qimiaq_titiqqat)return 0;void*자료위치=malloc(개수*qimiaq_titiqqat);if(자료위치)memset(자료위치,0,개수*qimiaq_titiqqat);return 자료위치;}
unsigned long long strtoull(const char*qimiaq_titiqqat,char**끝위치,int ungataa_atuutilik){
    const char*시작위치=qimiaq_titiqqat;while(*qimiaq_titiqqat==' '||(*qimiaq_titiqqat>=9&&*qimiaq_titiqqat<=13))qimiaq_titiqqat++;int 음수여부=0;if(*qimiaq_titiqqat=='-'||*qimiaq_titiqqat=='+')음수여부=*qimiaq_titiqqat++=='-';
    if((!ungataa_atuutilik||ungataa_atuutilik==16)&&qimiaq_titiqqat[0]=='0'&&(qimiaq_titiqqat[1]=='x'||qimiaq_titiqqat[1]=='X')){ungataa_atuutilik=16;qimiaq_titiqqat+=2;}if(!ungataa_atuutilik)ungataa_atuutilik=*qimiaq_titiqqat=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned immikkuuqtumut_nalunaikkut=*qimiaq_titiqqat,namunngarvik_titiqqat=immikkuuqtumut_nalunaikkut>='0'&&immikkuuqtumut_nalunaikkut<='9'?immikkuuqtumut_nalunaikkut-'0':immikkuuqtumut_nalunaikkut>='a'&&immikkuuqtumut_nalunaikkut<='z'?immikkuuqtumut_nalunaikkut-'a'+10:immikkuuqtumut_nalunaikkut>='A'&&immikkuuqtumut_nalunaikkut<='Z'?immikkuuqtumut_nalunaikkut-'A'+10:99;if(namunngarvik_titiqqat>=(unsigned)ungataa_atuutilik)break;하나라도=1;qimiaq_titiqqat++;if(임시값>(~0ull-namunngarvik_titiqqat)/(unsigned)ungataa_atuutilik){임시값=~0ull;tammarniq=34;}else 임시값=임시값*ungataa_atuutilik+namunngarvik_titiqqat;}
    if(끝위치)*끝위치=(char*)(하나라도?qimiaq_titiqqat:시작위치);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*qimiaq_titiqqat,char**보조항목,int 둘째값){return strtoull(qimiaq_titiqqat,보조항목,둘째값);}
long strtol(const char*qimiaq_titiqqat,char**보조항목,int 둘째값){return (long)strtoull(qimiaq_titiqqat,보조항목,둘째값);}
int atoi(const char*qimiaq_titiqqat){return (int)strtol(qimiaq_titiqqat,0,10);}
long double ldexpl(long double 가로좌표,int 개수){while(개수>0){가로좌표*=2;개수--;}while(개수<0){가로좌표/=2;개수++;}return 가로좌표;}
long double strtold(const char*qimiaq_titiqqat,char**끝위치){
    const char*시작위치=qimiaq_titiqqat;while(*qimiaq_titiqqat==' '||(*qimiaq_titiqqat>=9&&*qimiaq_titiqqat<=13))qimiaq_titiqqat++;int 음수여부=0;if(*qimiaq_titiqqat=='-'||*qimiaq_titiqqat=='+')음수여부=*qimiaq_titiqqat++=='-';
    int ungataa_atuutilik=10;if(qimiaq_titiqqat[0]=='0'&&(qimiaq_titiqqat[1]=='x'||qimiaq_titiqqat[1]=='X')){ungataa_atuutilik=16;qimiaq_titiqqat+=2;}long double 임시값=0,surragiarli_angininga=1;int 소수부=0,하나라도=0;
    for(;;){int immikkuuqtumut_nalunaikkut=*qimiaq_titiqqat,namunngarvik_titiqqat=immikkuuqtumut_nalunaikkut>='0'&&immikkuuqtumut_nalunaikkut<='9'?immikkuuqtumut_nalunaikkut-'0':immikkuuqtumut_nalunaikkut>='a'&&immikkuuqtumut_nalunaikkut<='f'?immikkuuqtumut_nalunaikkut-'a'+10:immikkuuqtumut_nalunaikkut>='A'&&immikkuuqtumut_nalunaikkut<='F'?immikkuuqtumut_nalunaikkut-'A'+10:99;
        if(immikkuuqtumut_nalunaikkut=='.'&&!소수부){소수부=1;qimiaq_titiqqat++;continue;}if(namunngarvik_titiqqat>=ungataa_atuutilik)break;하나라도=1;qimiaq_titiqqat++;임시값=임시값*ungataa_atuutilik+namunngarvik_titiqqat;if(소수부)surragiarli_angininga*=ungataa_atuutilik;
    }임시값/=surragiarli_angininga;
    if((ungataa_atuutilik==10&&(*qimiaq_titiqqat=='e'||*qimiaq_titiqqat=='E'))||(ungataa_atuutilik==16&&(*qimiaq_titiqqat=='p'||*qimiaq_titiqqat=='P'))){const char*saqqilli_atuutilik=qimiaq_titiqqat++;int 빼기=0;if(*qimiaq_titiqqat=='-'||*qimiaq_titiqqat=='+')빼기=*qimiaq_titiqqat++=='-';int 개수=0,항목수=0;while(*qimiaq_titiqqat>='0'&&*qimiaq_titiqqat<='9'){항목수++;if(개수<20000)개수=개수*10+*qimiaq_titiqqat-'0';qimiaq_titiqqat++;}if(!항목수)qimiaq_titiqqat=saqqilli_atuutilik;else{long double 배율=ungataa_atuutilik==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/배율:임시값*배율;}}
    if(끝위치)*끝위치=(char*)(하나라도?qimiaq_titiqqat:시작위치);return 음수여부?-임시값:임시값;
}
double strtod(const char*qimiaq_titiqqat,char**보조항목){return (double)strtold(qimiaq_titiqqat,보조항목);}float strtof(const char*qimiaq_titiqqat,char**보조항목){return (float)strtold(qimiaq_titiqqat,보조항목);}
void qsort(void*ungataa_atuutilik,size_t 개수,size_t anininga,int(*ajjigiinngittuqsiurli)(const void*,const void*)){
    unsigned char*자료위치=ungataa_atuutilik;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&ajjigiinngittuqsiurli(자료위치+(안쪽순번-1)*anininga,자료위치+안쪽순번*anininga)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<anininga;셋째순번++){unsigned char immikkuuqtumut_nalunaikkut=자료위치[(안쪽순번-1)*anininga+셋째순번];자료위치[(안쪽순번-1)*anininga+셋째순번]=자료위치[안쪽순번*anininga+셋째순번];자료위치[안쪽순번*anininga+셋째순번]=immikkuuqtumut_nalunaikkut;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*atiq,int 설정비트,...){
    if(!strcmp(atiq,"/@cc-output")){if(출력열림){tammarniq=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(atiq,번역기자원들[순번].atiq)){
        if(설정비트&3){tammarniq=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}tammarniq=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)atiq,설정비트,0,0,0,0);if(반환값<0){tammarniq=-반환값;return -1;}return 반환값;
}
int close(int ini_nuuttarut){if(ini_nuuttarut==100){출력열림=0;return 0;}if(ini_nuuttarut>=128&&ini_nuuttarut<152){열림[ini_nuuttarut-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,ini_nuuttarut,0,0,0,0,0);if(반환값<0){tammarniq=-반환값;return -1;}return 0;}
long read(int ini_nuuttarut,void*titiqqat,size_t 개수){
    if(ini_nuuttarut>=128&&ini_nuuttarut<152&&열림[ini_nuuttarut-128].사용량){int 순번=ini_nuuttarut-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->anininga-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(titiqqat,반환값->titiqqat+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,ini_nuuttarut,(uintptr_t)titiqqat,개수,0,0,0);if(반환값<0){tammarniq=-반환값;return -1;}return 반환값;
}
long write(int ini_nuuttarut,const void*titiqqat,size_t 개수){
    if(ini_nuuttarut==100){if(개수>sizeof(출력결과)-출력위치){tammarniq=28;return -1;}memcpy(출력결과+출력위치,titiqqat,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,ini_nuuttarut,(uintptr_t)titiqqat,개수,0,0,0);if(반환값<0){tammarniq=-반환값;return -1;}return 반환값;
}
long lseek(int ini_nuuttarut,long 변위,int 기준점){
    if(ini_nuuttarut==100){long 자료위치=변위+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){tammarniq=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(ini_nuuttarut>=128&&ini_nuuttarut<152&&열림[ini_nuuttarut-128].사용량){int 순번=ini_nuuttarut-128;long 자료위치=변위+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].anininga);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].anininga){tammarniq=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,ini_nuuttarut,변위,기준점,0,0,0);if(반환값<0){tammarniq=-반환값;return -1;}return 반환값;
}
int unlink(const char*atiq){intptr_t 반환값=사용자호출(11,(uintptr_t)atiq,0,0,0,0,0);if(반환값<0){tammarniq=-반환값;return -1;}return 반환값;}
char *realpath(const char*atiq,char*결과자료){if(!결과자료){결과자료=malloc(strlen(atiq)+1);if(!결과자료)return 0;}return strcpy(결과자료,atiq);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){tammarniq=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int ini_nuuttarut,const char*방식){(void)방식;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].tammarniq=0;흐름목록[순번].ini_nuuttarut=ini_nuuttarut;return &흐름목록[순번];}tammarniq=24;return 0;}
int fflush(FILE*ini_Iliniku){return ini_Iliniku&&ini_Iliniku->tammarniq?-1:0;}
int fclose(FILE*ini_Iliniku){int 반환값=close(ini_Iliniku->ini_nuuttarut);if(ini_Iliniku->tammarniq)반환값=-1;ini_Iliniku->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t qimiaq_titiqqat,size_t 개수,FILE*ini_Iliniku){if(!qimiaq_titiqqat)return 0;if(개수>SIZE_MAX/qimiaq_titiqqat){ini_Iliniku->tammarniq=1;return 0;}long 반환값=write(ini_Iliniku->ini_nuuttarut,자료위치,qimiaq_titiqqat*개수);if(반환값<0){ini_Iliniku->tammarniq=1;return 0;}return (size_t)반환값/qimiaq_titiqqat;}
int fputc(int immikkuuqtumut_nalunaikkut,FILE*ini_Iliniku){unsigned char 둘째값=immikkuuqtumut_nalunaikkut;return fwrite(&둘째값,1,1,ini_Iliniku)==1?둘째값:EOF;}
int fputs(const char*qimiaq_titiqqat,FILE*ini_Iliniku){return fwrite(qimiaq_titiqqat,1,strlen(qimiaq_titiqqat),ini_Iliniku)==strlen(qimiaq_titiqqat)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char immikkuuqtumut_nalunaikkut){if(*현재위치+1<용량한도)결과자료[*현재위치]=immikkuuqtumut_nalunaikkut;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*aaqqisurli,va_list 가변인수){
    size_t 현재위치=0;while(*aaqqisurli){if(*aaqqisurli!='%'){넣기(결과자료,용량한도,&현재위치,*aaqqisurli++);continue;}aaqqisurli++;
        int 왼쪽=0,영값=0,대체값=0;while(*aaqqisurli=='-'||*aaqqisurli=='0'||*aaqqisurli=='#'||*aaqqisurli=='+'||*aaqqisurli==' '){if(*aaqqisurli=='-')왼쪽=1;if(*aaqqisurli=='0')영값=1;if(*aaqqisurli=='#')대체값=1;aaqqisurli++;}
        int 너비=0,정밀도=-1;if(*aaqqisurli=='*'){너비=va_arg(가변인수,int);aaqqisurli++;}else while(*aaqqisurli>='0'&&*aaqqisurli<='9')너비=너비*10+*aaqqisurli++-'0';
        if(*aaqqisurli=='.'){aaqqisurli++;정밀도=0;if(*aaqqisurli=='*'){정밀도=va_arg(가변인수,int);aaqqisurli++;}else while(*aaqqisurli>='0'&&*aaqqisurli<='9')정밀도=정밀도*10+*aaqqisurli++-'0';}
        int 넓은글자=0;while(*aaqqisurli=='l'||*aaqqisurli=='z'||*aaqqisurli=='t'||*aaqqisurli=='j'||*aaqqisurli=='h'){if(*aaqqisurli!='h')넓은글자=1;aaqqisurli++;}
        char qanuittuuninga_Ataqatigiivvik=*aaqqisurli?*aaqqisurli++:0,완충공간[80];const char*qimiaq_titiqqat=완충공간;size_t 개수=0;
        if(qanuittuuninga_Ataqatigiivvik=='s'){qimiaq_titiqqat=va_arg(가변인수,const char*);if(!qimiaq_titiqqat)qimiaq_titiqqat="(null)";개수=strlen(qimiaq_titiqqat);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(qanuittuuninga_Ataqatigiivvik=='c'){완충공간[0]=va_arg(가변인수,int);개수=1;}
        else if(qanuittuuninga_Ataqatigiivvik=='%'){완충공간[0]='%';개수=1;}
        else if(qanuittuuninga_Ataqatigiivvik=='d'||qanuittuuninga_Ataqatigiivvik=='i'||qanuittuuninga_Ataqatigiivvik=='u'||qanuittuuninga_Ataqatigiivvik=='x'||qanuittuuninga_Ataqatigiivvik=='X'||qanuittuuninga_Ataqatigiivvik=='o'||qanuittuuninga_Ataqatigiivvik=='p'){
            unsigned long long atuutilik;int 음수표시=0;
            if(qanuittuuninga_Ataqatigiivvik=='d'||qanuittuuninga_Ataqatigiivvik=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;atuutilik=음수표시?0-(unsigned long long)임시값:임시값;}
            else atuutilik=qanuittuuninga_Ataqatigiivvik=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned ungataa_atuutilik=qanuittuuninga_Ataqatigiivvik=='x'||qanuittuuninga_Ataqatigiivvik=='X'||qanuittuuninga_Ataqatigiivvik=='p'?16:qanuittuuninga_Ataqatigiivvik=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[atuutilik%ungataa_atuutilik];atuutilik/=ungataa_atuutilik;}while(atuutilik);
            if(음수표시)완충공간[개수++]='-';if(qanuittuuninga_Ataqatigiivvik=='p'||(대체값&&ungataa_atuutilik==16)){완충공간[개수++]='0';완충공간[개수++]='x';}
            for(int 채움=(int)사용량;정밀도>채움&&개수<sizeof(완충공간)-사용량;채움++)완충공간[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(완충공간)-사용량)완충공간[개수++]='0';
            while(사용량)완충공간[개수++]=숫자수[--사용량];
        }else{완충공간[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,qimiaq_titiqqat[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*ini_Iliniku,...){va_list 첫째값;va_start(첫째값,ini_Iliniku);int 반환값=vsnprintf(결과자료,용량한도,ini_Iliniku,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*ini_Iliniku,...){va_list 첫째값;va_start(첫째값,ini_Iliniku);int 반환값=vsnprintf(결과자료,SIZE_MAX,ini_Iliniku,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*ingirrania_aulataup_atuutilik,const char*ini_Iliniku,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),ini_Iliniku,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,ingirrania_aulataup_atuutilik)==(size_t)개수?개수:-1;}
int fprintf(FILE*ingirrania_aulataup_atuutilik,const char*ini_Iliniku,...){va_list 첫째값;va_start(첫째값,ini_Iliniku);int 반환값=vfprintf(ingirrania_aulataup_atuutilik,ini_Iliniku,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*ini_Iliniku,...){va_list 첫째값;va_start(첫째값,ini_Iliniku);int 반환값=vfprintf(stdout,ini_Iliniku,첫째값);va_end(첫째값);return 반환값;}
