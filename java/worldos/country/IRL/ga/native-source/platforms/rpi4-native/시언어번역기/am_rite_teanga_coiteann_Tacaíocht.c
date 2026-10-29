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
static int ERREÁID;
int *__errno_location(void){return &ERREÁID;}
void exit(int staid_VALUE){사용자호출(6,staid_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *seic_slonn,const char *Comhad,unsigned Líne,const char *modh_iontráil_ainm){fprintf(stderr,"cc assertion: %s %s:%u %s\n",seic_slonn,Comhad,Líne,modh_iontráil_ainm);exit(1);}
size_t strlen(const char*teaghrán_sonraí){const char*sonraí_suíomh=teaghrán_sonraí;while(*sonraí_suíomh)sonraí_suíomh++;return sonraí_suíomh-teaghrán_sonraí;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t mír_COUNT){while(mír_COUNT--){unsigned char x_chomhordanáid=*첫째값++,세로좌표=*SECOND_VALUE++;if(x_chomhordanáid!=세로좌표)return x_chomhordanáid-세로좌표;if(!x_chomhordanáid)return 0;}return 0;}
char *strcpy(char*sprioc_sonraí,const char*teaghrán_sonraí){char*반환값=sprioc_sonraí;while((*sprioc_sonraí++=*teaghrán_sonraí++)){}return 반환값;}
char *strchr(const char*teaghrán_sonraí,int pointe_cóid){do{if(*teaghrán_sonraí==(char)pointe_cóid)return (char*)teaghrán_sonraí;}while(*teaghrán_sonraí++);return 0;}
char *strrchr(const char*teaghrán_sonraí,int pointe_cóid){const char*반환값=0;do{if(*teaghrán_sonraí==(char)pointe_cóid)반환값=teaghrán_sonraí;}while(*teaghrán_sonraí++);return (char*)반환값;}
char *strstr(const char*teaghrán_sonraí,const char*Teirminéal_iontráil){size_t mír_COUNT=strlen(Teirminéal_iontráil);for(;*teaghrán_sonraí;teaghrán_sonraí++)if(!strncmp(teaghrán_sonraí,Teirminéal_iontráil,mír_COUNT))return (char*)teaghrán_sonraí;return mír_COUNT?0:(char*)teaghrán_sonraí;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t mír_COUNT){const unsigned char*x_chomhordanáid=첫째값,*세로좌표=SECOND_VALUE;while(mír_COUNT--){if(*x_chomhordanáid!=*세로좌표)return *x_chomhordanáid-*세로좌표;x_chomhordanáid++;세로좌표++;}return 0;}
void *memmove(void*sprioc_sonraí,const void*teaghrán_sonraí,size_t mír_COUNT){unsigned char*x_chomhordanáid=sprioc_sonraí;const unsigned char*세로좌표=teaghrán_sonraí;if(x_chomhordanáid<세로좌표){for(size_t 순번=0;순번<mír_COUNT;순번++)x_chomhordanáid[순번]=세로좌표[순번];}else while(mír_COUNT){mír_COUNT--;x_chomhordanáid[mír_COUNT]=세로좌표[mír_COUNT];}return sprioc_sonraí;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct sonraí_bac {size_t Méid;struct sonraí_bac*Ar_aghaidh_mír;int 남은공간;int 채울크기;uint64_t ailíniú_aonaid;} sonraí_bac;
static sonraí_bac *첫항목;
void free(void*sonraí_suíomh){if(!sonraí_suíomh)return;sonraí_bac*SECOND_VALUE=(sonraí_bac*)sonraí_suíomh-1;SECOND_VALUE->남은공간=1;for(sonraí_bac*Ar_aghaidh_OFFSET=첫항목;Ar_aghaidh_OFFSET&&Ar_aghaidh_OFFSET->Ar_aghaidh_mír;){if(Ar_aghaidh_OFFSET->남은공간&&Ar_aghaidh_OFFSET->Ar_aghaidh_mír->남은공간){Ar_aghaidh_OFFSET->Méid+=sizeof(sonraí_bac)+Ar_aghaidh_OFFSET->Ar_aghaidh_mír->Méid;Ar_aghaidh_OFFSET->Ar_aghaidh_mír=Ar_aghaidh_OFFSET->Ar_aghaidh_mír->Ar_aghaidh_mír;}else Ar_aghaidh_OFFSET=Ar_aghaidh_OFFSET->Ar_aghaidh_mír;}}
void *realloc(void*sonraí_suíomh,size_t mír_COUNT){
    if(!mír_COUNT){free(sonraí_suíomh);return 0;}if(mír_COUNT>sizeof(할당마당)-sizeof(sonraí_bac))return 0;mír_COUNT=(mír_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(sonraí_bac*)할당마당;첫항목->Méid=sizeof(할당마당)-sizeof(sonraí_bac);첫항목->남은공간=1;첫항목->Ar_aghaidh_mír=0;}
    sonraí_bac*이전=sonraí_suíomh?(sonraí_bac*)sonraí_suíomh-1:0;if(이전&&이전->Méid>=mír_COUNT)return sonraí_suíomh;
    for(sonraí_bac*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Ar_aghaidh_mír)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Méid>=mír_COUNT){
        if(SECOND_VALUE->Méid>=mír_COUNT+sizeof(sonraí_bac)+16){sonraí_bac*나머지부분=(sonraí_bac*)((unsigned char*)(SECOND_VALUE+1)+mír_COUNT);나머지부분->Méid=SECOND_VALUE->Méid-mír_COUNT-sizeof(sonraí_bac);나머지부분->Ar_aghaidh_mír=SECOND_VALUE->Ar_aghaidh_mír;나머지부분->남은공간=1;SECOND_VALUE->Ar_aghaidh_mír=나머지부분;SECOND_VALUE->Méid=mír_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,sonraí_suíomh,이전->Méid);free(sonraí_suíomh);}return 반환값;
    }ERREÁID=12;return 0;
}
void *malloc(size_t mír_COUNT){return realloc(0,mír_COUNT);}
void *calloc(size_t mír_COUNT,size_t teaghrán_sonraí){if(teaghrán_sonraí&&mír_COUNT>SIZE_MAX/teaghrán_sonraí)return 0;void*sonraí_suíomh=malloc(mír_COUNT*teaghrán_sonraí);if(sonraí_suíomh)memset(sonraí_suíomh,0,mír_COUNT*teaghrán_sonraí);return sonraí_suíomh;}
unsigned long long strtoull(const char*teaghrán_sonraí,char**cuir_deireadh_le_OFFSET,int Cúlra_VALUE){
    const char*Start_OFFSET=teaghrán_sonraí;while(*teaghrán_sonraí==' '||(*teaghrán_sonraí>=9&&*teaghrán_sonraí<=13))teaghrán_sonraí++;int 음수여부=0;if(*teaghrán_sonraí=='-'||*teaghrán_sonraí=='+')음수여부=*teaghrán_sonraí++=='-';
    if((!Cúlra_VALUE||Cúlra_VALUE==16)&&teaghrán_sonraí[0]=='0'&&(teaghrán_sonraí[1]=='x'||teaghrán_sonraí[1]=='X')){Cúlra_VALUE=16;teaghrán_sonraí+=2;}if(!Cúlra_VALUE)Cúlra_VALUE=*teaghrán_sonraí=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned pointe_cóid=*teaghrán_sonraí,sprioc_sonraí=pointe_cóid>='0'&&pointe_cóid<='9'?pointe_cóid-'0':pointe_cóid>='a'&&pointe_cóid<='z'?pointe_cóid-'a'+10:pointe_cóid>='A'&&pointe_cóid<='Z'?pointe_cóid-'A'+10:99;if(sprioc_sonraí>=(unsigned)Cúlra_VALUE)break;하나라도=1;teaghrán_sonraí++;if(임시값>(~0ull-sprioc_sonraí)/(unsigned)Cúlra_VALUE){임시값=~0ull;ERREÁID=34;}else 임시값=임시값*Cúlra_VALUE+sprioc_sonraí;}
    if(cuir_deireadh_le_OFFSET)*cuir_deireadh_le_OFFSET=(char*)(하나라도?teaghrán_sonraí:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*teaghrán_sonraí,char**보조항목,int SECOND_VALUE){return strtoull(teaghrán_sonraí,보조항목,SECOND_VALUE);}
long strtol(const char*teaghrán_sonraí,char**보조항목,int SECOND_VALUE){return (long)strtoull(teaghrán_sonraí,보조항목,SECOND_VALUE);}
int atoi(const char*teaghrán_sonraí){return (int)strtol(teaghrán_sonraí,0,10);}
long double ldexpl(long double x_chomhordanáid,int mír_COUNT){while(mír_COUNT>0){x_chomhordanáid*=2;mír_COUNT--;}while(mír_COUNT<0){x_chomhordanáid/=2;mír_COUNT++;}return x_chomhordanáid;}
long double strtold(const char*teaghrán_sonraí,char**cuir_deireadh_le_OFFSET){
    const char*Start_OFFSET=teaghrán_sonraí;while(*teaghrán_sonraí==' '||(*teaghrán_sonraí>=9&&*teaghrán_sonraí<=13))teaghrán_sonraí++;int 음수여부=0;if(*teaghrán_sonraí=='-'||*teaghrán_sonraí=='+')음수여부=*teaghrán_sonraí++=='-';
    int Cúlra_VALUE=10;if(teaghrán_sonraí[0]=='0'&&(teaghrán_sonraí[1]=='x'||teaghrán_sonraí[1]=='X')){Cúlra_VALUE=16;teaghrán_sonraí+=2;}long double 임시값=0,scálaigh=1;int 소수부=0,하나라도=0;
    for(;;){int pointe_cóid=*teaghrán_sonraí,sprioc_sonraí=pointe_cóid>='0'&&pointe_cóid<='9'?pointe_cóid-'0':pointe_cóid>='a'&&pointe_cóid<='f'?pointe_cóid-'a'+10:pointe_cóid>='A'&&pointe_cóid<='F'?pointe_cóid-'A'+10:99;
        if(pointe_cóid=='.'&&!소수부){소수부=1;teaghrán_sonraí++;continue;}if(sprioc_sonraí>=Cúlra_VALUE)break;하나라도=1;teaghrán_sonraí++;임시값=임시값*Cúlra_VALUE+sprioc_sonraí;if(소수부)scálaigh*=Cúlra_VALUE;
    }임시값/=scálaigh;
    if((Cúlra_VALUE==10&&(*teaghrán_sonraí=='e'||*teaghrán_sonraí=='E'))||(Cúlra_VALUE==16&&(*teaghrán_sonraí=='p'||*teaghrán_sonraí=='P'))){const char*seó_VALUE=teaghrán_sonraí++;int 빼기=0;if(*teaghrán_sonraí=='-'||*teaghrán_sonraí=='+')빼기=*teaghrán_sonraí++=='-';int mír_COUNT=0,iontráil_COUNT=0;while(*teaghrán_sonraí>='0'&&*teaghrán_sonraí<='9'){iontráil_COUNT++;if(mír_COUNT<20000)mír_COUNT=mír_COUNT*10+*teaghrán_sonraí-'0';teaghrán_sonraí++;}if(!iontráil_COUNT)teaghrán_sonraí=seó_VALUE;else{long double fachtóir=Cúlra_VALUE==16?2:10;while(mír_COUNT-->0&&mír_COUNT<200000)임시값=빼기?임시값/fachtóir:임시값*fachtóir;}}
    if(cuir_deireadh_le_OFFSET)*cuir_deireadh_le_OFFSET=(char*)(하나라도?teaghrán_sonraí:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*teaghrán_sonraí,char**보조항목){return (double)strtold(teaghrán_sonraí,보조항목);}float strtof(const char*teaghrán_sonraí,char**보조항목){return (float)strtold(teaghrán_sonraí,보조항목);}
void qsort(void*Cúlra_VALUE,size_t mír_COUNT,size_t Méid,int(*cóimheas)(const void*,const void*)){
    unsigned char*sonraí_suíomh=Cúlra_VALUE;for(size_t 순번=1;순번<mír_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&cóimheas(sonraí_suíomh+(안쪽순번-1)*Méid,sonraí_suíomh+안쪽순번*Méid)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Méid;셋째순번++){unsigned char pointe_cóid=sonraí_suíomh[(안쪽순번-1)*Méid+셋째순번];sonraí_suíomh[(안쪽순번-1)*Méid+셋째순번]=sonraí_suíomh[안쪽순번*Méid+셋째순번];sonraí_suíomh[안쪽순번*Méid+셋째순번]=pointe_cóid;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t suíomh;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *mír_COUNT){*mír_COUNT=출력크기;return 출력결과;}
int open(const char*Ainm,int 설정비트,...){
    if(!strcmp(Ainm,"/@cc-output")){if(출력열림){ERREÁID=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Ainm,번역기자원들[순번].Ainm)){
        if(설정비트&3){ERREÁID=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].suíomh=0;return 128+안쪽순번;}ERREÁID=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Ainm,설정비트,0,0,0,0);if(반환값<0){ERREÁID=-반환값;return -1;}return 반환값;
}
int close(int comhad_hanla){if(comhad_hanla==100){출력열림=0;return 0;}if(comhad_hanla>=128&&comhad_hanla<152){열림[comhad_hanla-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,comhad_hanla,0,0,0,0,0);if(반환값<0){ERREÁID=-반환값;return -1;}return 0;}
long read(int comhad_hanla,void*sonraí,size_t mír_COUNT){
    if(comhad_hanla>=128&&comhad_hanla<152&&열림[comhad_hanla-128].사용량){int 순번=comhad_hanla-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Méid-열림[순번].suíomh;if(mír_COUNT>왼쪽)mír_COUNT=왼쪽;memcpy(sonraí,반환값->sonraí+열림[순번].suíomh,mír_COUNT);열림[순번].suíomh+=mír_COUNT;return mír_COUNT;}
    intptr_t 반환값=사용자호출(2,comhad_hanla,(uintptr_t)sonraí,mír_COUNT,0,0,0);if(반환값<0){ERREÁID=-반환값;return -1;}return 반환값;
}
long write(int comhad_hanla,const void*sonraí,size_t mír_COUNT){
    if(comhad_hanla==100){if(mír_COUNT>sizeof(출력결과)-출력위치){ERREÁID=28;return -1;}memcpy(출력결과+출력위치,sonraí,mír_COUNT);출력위치+=mír_COUNT;if(출력크기<출력위치)출력크기=출력위치;return mír_COUNT;}
    intptr_t 반환값=사용자호출(1,comhad_hanla,(uintptr_t)sonraí,mír_COUNT,0,0,0);if(반환값<0){ERREÁID=-반환값;return -1;}return 반환값;
}
long lseek(int comhad_hanla,long OFFSET_VALUE,int 기준점){
    if(comhad_hanla==100){long sonraí_suíomh=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(sonraí_suíomh<0||(size_t)sonraí_suíomh>sizeof(출력결과)){ERREÁID=22;return -1;}출력위치=sonraí_suíomh;return sonraí_suíomh;}
    if(comhad_hanla>=128&&comhad_hanla<152&&열림[comhad_hanla-128].사용량){int 순번=comhad_hanla-128;long sonraí_suíomh=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].suíomh:번역기자원들[열림[순번].LOOKUP_INDEX].Méid);if(sonraí_suíomh<0||(size_t)sonraí_suíomh>번역기자원들[열림[순번].LOOKUP_INDEX].Méid){ERREÁID=22;return -1;}열림[순번].suíomh=sonraí_suíomh;return sonraí_suíomh;}
    intptr_t 반환값=사용자호출(5,comhad_hanla,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){ERREÁID=-반환값;return -1;}return 반환값;
}
int unlink(const char*Ainm){intptr_t 반환값=사용자호출(11,(uintptr_t)Ainm,0,0,0,0,0);if(반환값<0){ERREÁID=-반환값;return -1;}return 반환값;}
char *realpath(const char*Ainm,char*tomhas_sonraí){if(!tomhas_sonraí){tomhas_sonraí=malloc(strlen(Ainm)+1);if(!tomhas_sonraí)return 0;}return strcpy(tomhas_sonraí,Ainm);}
char *getcwd(char*sonraí_suíomh,size_t mír_COUNT){if(mír_COUNT<2){ERREÁID=34;return 0;}sonraí_suíomh[0]='/';sonraí_suíomh[1]=0;return sonraí_suíomh;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Teirminéal_iontráil){time_t 임시값=0;if(Teirminéal_iontráil)*Teirminéal_iontráil=임시값;return 임시값;}
struct tm *localtime(const time_t*Teirminéal_iontráil){(void)Teirminéal_iontráil;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int comhad_hanla,const char*modh_mód){(void)modh_mód;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].ERREÁID=0;흐름목록[순번].comhad_hanla=comhad_hanla;return &흐름목록[순번];}ERREÁID=24;return 0;}
int fflush(FILE*comhad_iontráil){return comhad_iontráil&&comhad_iontráil->ERREÁID?-1:0;}
int fclose(FILE*comhad_iontráil){int 반환값=close(comhad_iontráil->comhad_hanla);if(comhad_iontráil->ERREÁID)반환값=-1;comhad_iontráil->사용량=0;return 반환값;}
size_t fwrite(const void*sonraí_suíomh,size_t teaghrán_sonraí,size_t mír_COUNT,FILE*comhad_iontráil){if(!teaghrán_sonraí)return 0;if(mír_COUNT>SIZE_MAX/teaghrán_sonraí){comhad_iontráil->ERREÁID=1;return 0;}long 반환값=write(comhad_iontráil->comhad_hanla,sonraí_suíomh,teaghrán_sonraí*mír_COUNT);if(반환값<0){comhad_iontráil->ERREÁID=1;return 0;}return (size_t)반환값/teaghrán_sonraí;}
int fputc(int pointe_cóid,FILE*comhad_iontráil){unsigned char SECOND_VALUE=pointe_cóid;return fwrite(&SECOND_VALUE,1,1,comhad_iontráil)==1?SECOND_VALUE:EOF;}
int fputs(const char*teaghrán_sonraí,FILE*comhad_iontráil){return fwrite(teaghrán_sonraí,1,strlen(teaghrán_sonraí),comhad_iontráil)==strlen(teaghrán_sonraí)?0:EOF;}
static void 넣기(char*tomhas_sonraí,size_t 용량한도,size_t*현재위치,char pointe_cóid){if(*현재위치+1<용량한도)tomhas_sonraí[*현재위치]=pointe_cóid;(*현재위치)++;}
int vsnprintf(char*tomhas_sonraí,size_t 용량한도,const char*formáid,va_list 가변인수){
    size_t 현재위치=0;while(*formáid){if(*formáid!='%'){넣기(tomhas_sonraí,용량한도,&현재위치,*formáid++);continue;}formáid++;
        int 왼쪽=0,영값=0,대체값=0;while(*formáid=='-'||*formáid=='0'||*formáid=='#'||*formáid=='+'||*formáid==' '){if(*formáid=='-')왼쪽=1;if(*formáid=='0')영값=1;if(*formáid=='#')대체값=1;formáid++;}
        int 너비=0,정밀도=-1;if(*formáid=='*'){너비=va_arg(가변인수,int);formáid++;}else while(*formáid>='0'&&*formáid<='9')너비=너비*10+*formáid++-'0';
        if(*formáid=='.'){formáid++;정밀도=0;if(*formáid=='*'){정밀도=va_arg(가변인수,int);formáid++;}else while(*formáid>='0'&&*formáid<='9')정밀도=정밀도*10+*formáid++-'0';}
        int 넓은글자=0;while(*formáid=='l'||*formáid=='z'||*formáid=='t'||*formáid=='j'||*formáid=='h'){if(*formáid!='h')넓은글자=1;formáid++;}
        char TYPE_catagóir=*formáid?*formáid++:0,maolán_Stóras[80];const char*teaghrán_sonraí=maolán_Stóras;size_t mír_COUNT=0;
        if(TYPE_catagóir=='s'){teaghrán_sonraí=va_arg(가변인수,const char*);if(!teaghrán_sonraí)teaghrán_sonraí="(null)";mír_COUNT=strlen(teaghrán_sonraí);if(정밀도>=0&&mír_COUNT>(size_t)정밀도)mír_COUNT=정밀도;}
        else if(TYPE_catagóir=='c'){maolán_Stóras[0]=va_arg(가변인수,int);mír_COUNT=1;}
        else if(TYPE_catagóir=='%'){maolán_Stóras[0]='%';mír_COUNT=1;}
        else if(TYPE_catagóir=='d'||TYPE_catagóir=='i'||TYPE_catagóir=='u'||TYPE_catagóir=='x'||TYPE_catagóir=='X'||TYPE_catagóir=='o'||TYPE_catagóir=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_catagóir=='d'||TYPE_catagóir=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_catagóir=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Cúlra_VALUE=TYPE_catagóir=='x'||TYPE_catagóir=='X'||TYPE_catagóir=='p'?16:TYPE_catagóir=='o'?8:10;char digit_COUNT[64];unsigned 사용량=0;
            do{digit_COUNT[사용량++]="0123456789abcdef"[VALUE%Cúlra_VALUE];VALUE/=Cúlra_VALUE;}while(VALUE);
            if(음수표시)maolán_Stóras[mír_COUNT++]='-';if(TYPE_catagóir=='p'||(대체값&&Cúlra_VALUE==16)){maolán_Stóras[mír_COUNT++]='0';maolán_Stóras[mír_COUNT++]='x';}
            for(int líon_VALUE=(int)사용량;정밀도>líon_VALUE&&mír_COUNT<sizeof(maolán_Stóras)-사용량;líon_VALUE++)maolán_Stóras[mír_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(mír_COUNT+사용량)&&mír_COUNT<sizeof(maolán_Stóras)-사용량)maolán_Stóras[mír_COUNT++]='0';
            while(사용량)maolán_Stóras[mír_COUNT++]=digit_COUNT[--사용량];
        }else{maolán_Stóras[0]='?';mír_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)mír_COUNT){넣기(tomhas_sonraí,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<mír_COUNT;순번++)넣기(tomhas_sonraí,용량한도,&현재위치,teaghrán_sonraí[순번]);while(왼쪽&&너비>(int)mír_COUNT){넣기(tomhas_sonraí,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)tomhas_sonraí[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*tomhas_sonraí,size_t 용량한도,const char*comhad_iontráil,...){va_list 첫째값;va_start(첫째값,comhad_iontráil);int 반환값=vsnprintf(tomhas_sonraí,용량한도,comhad_iontráil,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*tomhas_sonraí,const char*comhad_iontráil,...){va_list 첫째값;va_start(첫째값,comhad_iontráil);int 반환값=vsnprintf(tomhas_sonraí,SIZE_MAX,comhad_iontráil,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*sruth_VALUE,const char*comhad_iontráil,va_list 첫째값){char SECOND_VALUE[2048];int mír_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),comhad_iontráil,첫째값);if(mír_COUNT>2047)mír_COUNT=2047;return fwrite(SECOND_VALUE,1,mír_COUNT,sruth_VALUE)==(size_t)mír_COUNT?mír_COUNT:-1;}
int fprintf(FILE*sruth_VALUE,const char*comhad_iontráil,...){va_list 첫째값;va_start(첫째값,comhad_iontráil);int 반환값=vfprintf(sruth_VALUE,comhad_iontráil,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*comhad_iontráil,...){va_list 첫째값;va_start(첫째값,comhad_iontráil);int 반환값=vfprintf(stdout,comhad_iontráil,첫째값);va_end(첫째값);return 반환값;}
