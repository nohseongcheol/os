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
static int Mearachd;
int *__errno_location(void){return &Mearachd;}
void exit(int cor_VALUE){사용자호출(6,cor_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *seic_eas_preisean,const char *faidhle,unsigned loidhne,const char *dòigh_cur_a_steach_ainm){fprintf(stderr,"cc assertion: %s %s:%u %s\n",seic_eas_preisean,faidhle,loidhne,dòigh_cur_a_steach_ainm);exit(1);}
size_t strlen(const char*sreang_dàta){const char*dàta_suidhich=sreang_dàta;while(*dàta_suidhich)dàta_suidhich++;return dàta_suidhich-sreang_dàta;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t nì_COUNT){while(nì_COUNT--){unsigned char co_chomharra_x=*첫째값++,세로좌표=*SECOND_VALUE++;if(co_chomharra_x!=세로좌표)return co_chomharra_x-세로좌표;if(!co_chomharra_x)return 0;}return 0;}
char *strcpy(char*ceann_uidhe_dàta,const char*sreang_dàta){char*반환값=ceann_uidhe_dàta;while((*ceann_uidhe_dàta++=*sreang_dàta++)){}return 반환값;}
char *strchr(const char*sreang_dàta,int còd_a_charactair){do{if(*sreang_dàta==(char)còd_a_charactair)return (char*)sreang_dàta;}while(*sreang_dàta++);return 0;}
char *strrchr(const char*sreang_dàta,int còd_a_charactair){const char*반환값=0;do{if(*sreang_dàta==(char)còd_a_charactair)반환값=sreang_dàta;}while(*sreang_dàta++);return (char*)반환값;}
char *strstr(const char*sreang_dàta,const char*tèirmineal_cur_a_steach){size_t nì_COUNT=strlen(tèirmineal_cur_a_steach);for(;*sreang_dàta;sreang_dàta++)if(!strncmp(sreang_dàta,tèirmineal_cur_a_steach,nì_COUNT))return (char*)sreang_dàta;return nì_COUNT?0:(char*)sreang_dàta;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t nì_COUNT){const unsigned char*co_chomharra_x=첫째값,*세로좌표=SECOND_VALUE;while(nì_COUNT--){if(*co_chomharra_x!=*세로좌표)return *co_chomharra_x-*세로좌표;co_chomharra_x++;세로좌표++;}return 0;}
void *memmove(void*ceann_uidhe_dàta,const void*sreang_dàta,size_t nì_COUNT){unsigned char*co_chomharra_x=ceann_uidhe_dàta;const unsigned char*세로좌표=sreang_dàta;if(co_chomharra_x<세로좌표){for(size_t 순번=0;순번<nì_COUNT;순번++)co_chomharra_x[순번]=세로좌표[순번];}else while(nì_COUNT){nì_COUNT--;co_chomharra_x[nì_COUNT]=세로좌표[nì_COUNT];}return ceann_uidhe_dàta;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct dàta_bac {size_t atharraich_am_meud;struct dàta_bac*air_adhart_nì;int 남은공간;int 채울크기;uint64_t co_thaobhadh_leasan;} dàta_bac;
static dàta_bac *첫항목;
void free(void*dàta_suidhich){if(!dàta_suidhich)return;dàta_bac*SECOND_VALUE=(dàta_bac*)dàta_suidhich-1;SECOND_VALUE->남은공간=1;for(dàta_bac*air_adhart_OFFSET=첫항목;air_adhart_OFFSET&&air_adhart_OFFSET->air_adhart_nì;){if(air_adhart_OFFSET->남은공간&&air_adhart_OFFSET->air_adhart_nì->남은공간){air_adhart_OFFSET->atharraich_am_meud+=sizeof(dàta_bac)+air_adhart_OFFSET->air_adhart_nì->atharraich_am_meud;air_adhart_OFFSET->air_adhart_nì=air_adhart_OFFSET->air_adhart_nì->air_adhart_nì;}else air_adhart_OFFSET=air_adhart_OFFSET->air_adhart_nì;}}
void *realloc(void*dàta_suidhich,size_t nì_COUNT){
    if(!nì_COUNT){free(dàta_suidhich);return 0;}if(nì_COUNT>sizeof(할당마당)-sizeof(dàta_bac))return 0;nì_COUNT=(nì_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(dàta_bac*)할당마당;첫항목->atharraich_am_meud=sizeof(할당마당)-sizeof(dàta_bac);첫항목->남은공간=1;첫항목->air_adhart_nì=0;}
    dàta_bac*이전=dàta_suidhich?(dàta_bac*)dàta_suidhich-1:0;if(이전&&이전->atharraich_am_meud>=nì_COUNT)return dàta_suidhich;
    for(dàta_bac*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->air_adhart_nì)if(SECOND_VALUE->남은공간&&SECOND_VALUE->atharraich_am_meud>=nì_COUNT){
        if(SECOND_VALUE->atharraich_am_meud>=nì_COUNT+sizeof(dàta_bac)+16){dàta_bac*나머지부분=(dàta_bac*)((unsigned char*)(SECOND_VALUE+1)+nì_COUNT);나머지부분->atharraich_am_meud=SECOND_VALUE->atharraich_am_meud-nì_COUNT-sizeof(dàta_bac);나머지부분->air_adhart_nì=SECOND_VALUE->air_adhart_nì;나머지부분->남은공간=1;SECOND_VALUE->air_adhart_nì=나머지부분;SECOND_VALUE->atharraich_am_meud=nì_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,dàta_suidhich,이전->atharraich_am_meud);free(dàta_suidhich);}return 반환값;
    }Mearachd=12;return 0;
}
void *malloc(size_t nì_COUNT){return realloc(0,nì_COUNT);}
void *calloc(size_t nì_COUNT,size_t sreang_dàta){if(sreang_dàta&&nì_COUNT>SIZE_MAX/sreang_dàta)return 0;void*dàta_suidhich=malloc(nì_COUNT*sreang_dàta);if(dàta_suidhich)memset(dàta_suidhich,0,nì_COUNT*sreang_dàta);return dàta_suidhich;}
unsigned long long strtoull(const char*sreang_dàta,char**crìochnaich_OFFSET,int cùlaibh_VALUE){
    const char*Start_OFFSET=sreang_dàta;while(*sreang_dàta==' '||(*sreang_dàta>=9&&*sreang_dàta<=13))sreang_dàta++;int 음수여부=0;if(*sreang_dàta=='-'||*sreang_dàta=='+')음수여부=*sreang_dàta++=='-';
    if((!cùlaibh_VALUE||cùlaibh_VALUE==16)&&sreang_dàta[0]=='0'&&(sreang_dàta[1]=='x'||sreang_dàta[1]=='X')){cùlaibh_VALUE=16;sreang_dàta+=2;}if(!cùlaibh_VALUE)cùlaibh_VALUE=*sreang_dàta=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned còd_a_charactair=*sreang_dàta,ceann_uidhe_dàta=còd_a_charactair>='0'&&còd_a_charactair<='9'?còd_a_charactair-'0':còd_a_charactair>='a'&&còd_a_charactair<='z'?còd_a_charactair-'a'+10:còd_a_charactair>='A'&&còd_a_charactair<='Z'?còd_a_charactair-'A'+10:99;if(ceann_uidhe_dàta>=(unsigned)cùlaibh_VALUE)break;하나라도=1;sreang_dàta++;if(임시값>(~0ull-ceann_uidhe_dàta)/(unsigned)cùlaibh_VALUE){임시값=~0ull;Mearachd=34;}else 임시값=임시값*cùlaibh_VALUE+ceann_uidhe_dàta;}
    if(crìochnaich_OFFSET)*crìochnaich_OFFSET=(char*)(하나라도?sreang_dàta:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*sreang_dàta,char**보조항목,int SECOND_VALUE){return strtoull(sreang_dàta,보조항목,SECOND_VALUE);}
long strtol(const char*sreang_dàta,char**보조항목,int SECOND_VALUE){return (long)strtoull(sreang_dàta,보조항목,SECOND_VALUE);}
int atoi(const char*sreang_dàta){return (int)strtol(sreang_dàta,0,10);}
long double ldexpl(long double co_chomharra_x,int nì_COUNT){while(nì_COUNT>0){co_chomharra_x*=2;nì_COUNT--;}while(nì_COUNT<0){co_chomharra_x/=2;nì_COUNT++;}return co_chomharra_x;}
long double strtold(const char*sreang_dàta,char**crìochnaich_OFFSET){
    const char*Start_OFFSET=sreang_dàta;while(*sreang_dàta==' '||(*sreang_dàta>=9&&*sreang_dàta<=13))sreang_dàta++;int 음수여부=0;if(*sreang_dàta=='-'||*sreang_dàta=='+')음수여부=*sreang_dàta++=='-';
    int cùlaibh_VALUE=10;if(sreang_dàta[0]=='0'&&(sreang_dàta[1]=='x'||sreang_dàta[1]=='X')){cùlaibh_VALUE=16;sreang_dàta+=2;}long double 임시값=0,sgèilich=1;int 소수부=0,하나라도=0;
    for(;;){int còd_a_charactair=*sreang_dàta,ceann_uidhe_dàta=còd_a_charactair>='0'&&còd_a_charactair<='9'?còd_a_charactair-'0':còd_a_charactair>='a'&&còd_a_charactair<='f'?còd_a_charactair-'a'+10:còd_a_charactair>='A'&&còd_a_charactair<='F'?còd_a_charactair-'A'+10:99;
        if(còd_a_charactair=='.'&&!소수부){소수부=1;sreang_dàta++;continue;}if(ceann_uidhe_dàta>=cùlaibh_VALUE)break;하나라도=1;sreang_dàta++;임시값=임시값*cùlaibh_VALUE+ceann_uidhe_dàta;if(소수부)sgèilich*=cùlaibh_VALUE;
    }임시값/=sgèilich;
    if((cùlaibh_VALUE==10&&(*sreang_dàta=='e'||*sreang_dàta=='E'))||(cùlaibh_VALUE==16&&(*sreang_dàta=='p'||*sreang_dàta=='P'))){const char*show_VALUE=sreang_dàta++;int 빼기=0;if(*sreang_dàta=='-'||*sreang_dàta=='+')빼기=*sreang_dàta++=='-';int nì_COUNT=0,cur_a_steach_COUNT=0;while(*sreang_dàta>='0'&&*sreang_dàta<='9'){cur_a_steach_COUNT++;if(nì_COUNT<20000)nì_COUNT=nì_COUNT*10+*sreang_dàta-'0';sreang_dàta++;}if(!cur_a_steach_COUNT)sreang_dàta=show_VALUE;else{long double factar=cùlaibh_VALUE==16?2:10;while(nì_COUNT-->0&&nì_COUNT<200000)임시값=빼기?임시값/factar:임시값*factar;}}
    if(crìochnaich_OFFSET)*crìochnaich_OFFSET=(char*)(하나라도?sreang_dàta:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*sreang_dàta,char**보조항목){return (double)strtold(sreang_dàta,보조항목);}float strtof(const char*sreang_dàta,char**보조항목){return (float)strtold(sreang_dàta,보조항목);}
void qsort(void*cùlaibh_VALUE,size_t nì_COUNT,size_t atharraich_am_meud,int(*dèan_coimeas)(const void*,const void*)){
    unsigned char*dàta_suidhich=cùlaibh_VALUE;for(size_t 순번=1;순번<nì_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&dèan_coimeas(dàta_suidhich+(안쪽순번-1)*atharraich_am_meud,dàta_suidhich+안쪽순번*atharraich_am_meud)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<atharraich_am_meud;셋째순번++){unsigned char còd_a_charactair=dàta_suidhich[(안쪽순번-1)*atharraich_am_meud+셋째순번];dàta_suidhich[(안쪽순번-1)*atharraich_am_meud+셋째순번]=dàta_suidhich[안쪽순번*atharraich_am_meud+셋째순번];dàta_suidhich[안쪽순번*atharraich_am_meud+셋째순번]=còd_a_charactair;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t suidhich;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *nì_COUNT){*nì_COUNT=출력크기;return 출력결과;}
int open(const char*Ainm,int 설정비트,...){
    if(!strcmp(Ainm,"/@cc-output")){if(출력열림){Mearachd=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Ainm,번역기자원들[순번].Ainm)){
        if(설정비트&3){Mearachd=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].suidhich=0;return 128+안쪽순번;}Mearachd=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Ainm,설정비트,0,0,0,0);if(반환값<0){Mearachd=-반환값;return -1;}return 반환값;
}
int close(int faidhle_làmhrachan){if(faidhle_làmhrachan==100){출력열림=0;return 0;}if(faidhle_làmhrachan>=128&&faidhle_làmhrachan<152){열림[faidhle_làmhrachan-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,faidhle_làmhrachan,0,0,0,0,0);if(반환값<0){Mearachd=-반환값;return -1;}return 0;}
long read(int faidhle_làmhrachan,void*dàta,size_t nì_COUNT){
    if(faidhle_làmhrachan>=128&&faidhle_làmhrachan<152&&열림[faidhle_làmhrachan-128].사용량){int 순번=faidhle_làmhrachan-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->atharraich_am_meud-열림[순번].suidhich;if(nì_COUNT>왼쪽)nì_COUNT=왼쪽;memcpy(dàta,반환값->dàta+열림[순번].suidhich,nì_COUNT);열림[순번].suidhich+=nì_COUNT;return nì_COUNT;}
    intptr_t 반환값=사용자호출(2,faidhle_làmhrachan,(uintptr_t)dàta,nì_COUNT,0,0,0);if(반환값<0){Mearachd=-반환값;return -1;}return 반환값;
}
long write(int faidhle_làmhrachan,const void*dàta,size_t nì_COUNT){
    if(faidhle_làmhrachan==100){if(nì_COUNT>sizeof(출력결과)-출력위치){Mearachd=28;return -1;}memcpy(출력결과+출력위치,dàta,nì_COUNT);출력위치+=nì_COUNT;if(출력크기<출력위치)출력크기=출력위치;return nì_COUNT;}
    intptr_t 반환값=사용자호출(1,faidhle_làmhrachan,(uintptr_t)dàta,nì_COUNT,0,0,0);if(반환값<0){Mearachd=-반환값;return -1;}return 반환값;
}
long lseek(int faidhle_làmhrachan,long OFFSET_VALUE,int 기준점){
    if(faidhle_làmhrachan==100){long dàta_suidhich=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(dàta_suidhich<0||(size_t)dàta_suidhich>sizeof(출력결과)){Mearachd=22;return -1;}출력위치=dàta_suidhich;return dàta_suidhich;}
    if(faidhle_làmhrachan>=128&&faidhle_làmhrachan<152&&열림[faidhle_làmhrachan-128].사용량){int 순번=faidhle_làmhrachan-128;long dàta_suidhich=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].suidhich:번역기자원들[열림[순번].LOOKUP_INDEX].atharraich_am_meud);if(dàta_suidhich<0||(size_t)dàta_suidhich>번역기자원들[열림[순번].LOOKUP_INDEX].atharraich_am_meud){Mearachd=22;return -1;}열림[순번].suidhich=dàta_suidhich;return dàta_suidhich;}
    intptr_t 반환값=사용자호출(5,faidhle_làmhrachan,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){Mearachd=-반환값;return -1;}return 반환값;
}
int unlink(const char*Ainm){intptr_t 반환값=사용자호출(11,(uintptr_t)Ainm,0,0,0,0,0);if(반환값<0){Mearachd=-반환값;return -1;}return 반환값;}
char *realpath(const char*Ainm,char*tomhas_dàta){if(!tomhas_dàta){tomhas_dàta=malloc(strlen(Ainm)+1);if(!tomhas_dàta)return 0;}return strcpy(tomhas_dàta,Ainm);}
char *getcwd(char*dàta_suidhich,size_t nì_COUNT){if(nì_COUNT<2){Mearachd=34;return 0;}dàta_suidhich[0]='/';dàta_suidhich[1]=0;return dàta_suidhich;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*tèirmineal_cur_a_steach){time_t 임시값=0;if(tèirmineal_cur_a_steach)*tèirmineal_cur_a_steach=임시값;return 임시값;}
struct tm *localtime(const time_t*tèirmineal_cur_a_steach){(void)tèirmineal_cur_a_steach;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int faidhle_làmhrachan,const char*dòigh_MODE){(void)dòigh_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Mearachd=0;흐름목록[순번].faidhle_làmhrachan=faidhle_làmhrachan;return &흐름목록[순번];}Mearachd=24;return 0;}
int fflush(FILE*faidhle_cur_a_steach){return faidhle_cur_a_steach&&faidhle_cur_a_steach->Mearachd?-1:0;}
int fclose(FILE*faidhle_cur_a_steach){int 반환값=close(faidhle_cur_a_steach->faidhle_làmhrachan);if(faidhle_cur_a_steach->Mearachd)반환값=-1;faidhle_cur_a_steach->사용량=0;return 반환값;}
size_t fwrite(const void*dàta_suidhich,size_t sreang_dàta,size_t nì_COUNT,FILE*faidhle_cur_a_steach){if(!sreang_dàta)return 0;if(nì_COUNT>SIZE_MAX/sreang_dàta){faidhle_cur_a_steach->Mearachd=1;return 0;}long 반환값=write(faidhle_cur_a_steach->faidhle_làmhrachan,dàta_suidhich,sreang_dàta*nì_COUNT);if(반환값<0){faidhle_cur_a_steach->Mearachd=1;return 0;}return (size_t)반환값/sreang_dàta;}
int fputc(int còd_a_charactair,FILE*faidhle_cur_a_steach){unsigned char SECOND_VALUE=còd_a_charactair;return fwrite(&SECOND_VALUE,1,1,faidhle_cur_a_steach)==1?SECOND_VALUE:EOF;}
int fputs(const char*sreang_dàta,FILE*faidhle_cur_a_steach){return fwrite(sreang_dàta,1,strlen(sreang_dàta),faidhle_cur_a_steach)==strlen(sreang_dàta)?0:EOF;}
static void 넣기(char*tomhas_dàta,size_t 용량한도,size_t*현재위치,char còd_a_charactair){if(*현재위치+1<용량한도)tomhas_dàta[*현재위치]=còd_a_charactair;(*현재위치)++;}
int vsnprintf(char*tomhas_dàta,size_t 용량한도,const char*fòrmat,va_list 가변인수){
    size_t 현재위치=0;while(*fòrmat){if(*fòrmat!='%'){넣기(tomhas_dàta,용량한도,&현재위치,*fòrmat++);continue;}fòrmat++;
        int 왼쪽=0,영값=0,대체값=0;while(*fòrmat=='-'||*fòrmat=='0'||*fòrmat=='#'||*fòrmat=='+'||*fòrmat==' '){if(*fòrmat=='-')왼쪽=1;if(*fòrmat=='0')영값=1;if(*fòrmat=='#')대체값=1;fòrmat++;}
        int 너비=0,정밀도=-1;if(*fòrmat=='*'){너비=va_arg(가변인수,int);fòrmat++;}else while(*fòrmat>='0'&&*fòrmat<='9')너비=너비*10+*fòrmat++-'0';
        if(*fòrmat=='.'){fòrmat++;정밀도=0;if(*fòrmat=='*'){정밀도=va_arg(가변인수,int);fòrmat++;}else while(*fòrmat>='0'&&*fòrmat<='9')정밀도=정밀도*10+*fòrmat++-'0';}
        int 넓은글자=0;while(*fòrmat=='l'||*fòrmat=='z'||*fòrmat=='t'||*fòrmat=='j'||*fòrmat=='h'){if(*fòrmat!='h')넓은글자=1;fòrmat++;}
        char TYPE_roinn_seòrsa=*fòrmat?*fòrmat++:0,bufair_stòras[80];const char*sreang_dàta=bufair_stòras;size_t nì_COUNT=0;
        if(TYPE_roinn_seòrsa=='s'){sreang_dàta=va_arg(가변인수,const char*);if(!sreang_dàta)sreang_dàta="(null)";nì_COUNT=strlen(sreang_dàta);if(정밀도>=0&&nì_COUNT>(size_t)정밀도)nì_COUNT=정밀도;}
        else if(TYPE_roinn_seòrsa=='c'){bufair_stòras[0]=va_arg(가변인수,int);nì_COUNT=1;}
        else if(TYPE_roinn_seòrsa=='%'){bufair_stòras[0]='%';nì_COUNT=1;}
        else if(TYPE_roinn_seòrsa=='d'||TYPE_roinn_seòrsa=='i'||TYPE_roinn_seòrsa=='u'||TYPE_roinn_seòrsa=='x'||TYPE_roinn_seòrsa=='X'||TYPE_roinn_seòrsa=='o'||TYPE_roinn_seòrsa=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_roinn_seòrsa=='d'||TYPE_roinn_seòrsa=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_roinn_seòrsa=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned cùlaibh_VALUE=TYPE_roinn_seòrsa=='x'||TYPE_roinn_seòrsa=='X'||TYPE_roinn_seòrsa=='p'?16:TYPE_roinn_seòrsa=='o'?8:10;char figear_COUNT[64];unsigned 사용량=0;
            do{figear_COUNT[사용량++]="0123456789abcdef"[VALUE%cùlaibh_VALUE];VALUE/=cùlaibh_VALUE;}while(VALUE);
            if(음수표시)bufair_stòras[nì_COUNT++]='-';if(TYPE_roinn_seòrsa=='p'||(대체값&&cùlaibh_VALUE==16)){bufair_stòras[nì_COUNT++]='0';bufair_stòras[nì_COUNT++]='x';}
            for(int lìonadh_VALUE=(int)사용량;정밀도>lìonadh_VALUE&&nì_COUNT<sizeof(bufair_stòras)-사용량;lìonadh_VALUE++)bufair_stòras[nì_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(nì_COUNT+사용량)&&nì_COUNT<sizeof(bufair_stòras)-사용량)bufair_stòras[nì_COUNT++]='0';
            while(사용량)bufair_stòras[nì_COUNT++]=figear_COUNT[--사용량];
        }else{bufair_stòras[0]='?';nì_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)nì_COUNT){넣기(tomhas_dàta,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<nì_COUNT;순번++)넣기(tomhas_dàta,용량한도,&현재위치,sreang_dàta[순번]);while(왼쪽&&너비>(int)nì_COUNT){넣기(tomhas_dàta,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)tomhas_dàta[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*tomhas_dàta,size_t 용량한도,const char*faidhle_cur_a_steach,...){va_list 첫째값;va_start(첫째값,faidhle_cur_a_steach);int 반환값=vsnprintf(tomhas_dàta,용량한도,faidhle_cur_a_steach,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*tomhas_dàta,const char*faidhle_cur_a_steach,...){va_list 첫째값;va_start(첫째값,faidhle_cur_a_steach);int 반환값=vsnprintf(tomhas_dàta,SIZE_MAX,faidhle_cur_a_steach,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*sruth_VALUE,const char*faidhle_cur_a_steach,va_list 첫째값){char SECOND_VALUE[2048];int nì_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),faidhle_cur_a_steach,첫째값);if(nì_COUNT>2047)nì_COUNT=2047;return fwrite(SECOND_VALUE,1,nì_COUNT,sruth_VALUE)==(size_t)nì_COUNT?nì_COUNT:-1;}
int fprintf(FILE*sruth_VALUE,const char*faidhle_cur_a_steach,...){va_list 첫째값;va_start(첫째값,faidhle_cur_a_steach);int 반환값=vfprintf(sruth_VALUE,faidhle_cur_a_steach,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*faidhle_cur_a_steach,...){va_list 첫째값;va_start(첫째값,faidhle_cur_a_steach);int 반환값=vfprintf(stdout,faidhle_cur_a_steach,첫째값);va_end(첫째값);return 반환값;}
