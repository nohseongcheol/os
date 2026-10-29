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
static int Gwall;
int *__errno_location(void){return &Gwall;}
void exit(int cyflwr_VALUE){사용자호출(6,cyflwr_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *gwirio_mynegiad,const char *Ffeil,unsigned llinell,const char *dull_cofnod_enw){fprintf(stderr,"cc assertion: %s %s:%u %s\n",gwirio_mynegiad,Ffeil,llinell,dull_cofnod_enw);exit(1);}
size_t strlen(const char*testun_data){const char*data_safle=testun_data;while(*data_safle)data_safle++;return data_safle-testun_data;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t eitem_COUNT){while(eitem_COUNT--){unsigned char cyfesuryn_x=*첫째값++,Y_cyfesuryn=*SECOND_VALUE++;if(cyfesuryn_x!=Y_cyfesuryn)return cyfesuryn_x-Y_cyfesuryn;if(!cyfesuryn_x)return 0;}return 0;}
char *strcpy(char*cyrchfan_data,const char*testun_data){char*반환값=cyrchfan_data;while((*cyrchfan_data++=*testun_data++)){}return 반환값;}
char *strchr(const char*testun_data,int cod_nod){do{if(*testun_data==(char)cod_nod)return (char*)testun_data;}while(*testun_data++);return 0;}
char *strrchr(const char*testun_data,int cod_nod){const char*반환값=0;do{if(*testun_data==(char)cod_nod)반환값=testun_data;}while(*testun_data++);return (char*)반환값;}
char *strstr(const char*testun_data,const char*Terfynell_cofnod){size_t eitem_COUNT=strlen(Terfynell_cofnod);for(;*testun_data;testun_data++)if(!strncmp(testun_data,Terfynell_cofnod,eitem_COUNT))return (char*)testun_data;return eitem_COUNT?0:(char*)testun_data;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t eitem_COUNT){const unsigned char*cyfesuryn_x=첫째값,*Y_cyfesuryn=SECOND_VALUE;while(eitem_COUNT--){if(*cyfesuryn_x!=*Y_cyfesuryn)return *cyfesuryn_x-*Y_cyfesuryn;cyfesuryn_x++;Y_cyfesuryn++;}return 0;}
void *memmove(void*cyrchfan_data,const void*testun_data,size_t eitem_COUNT){unsigned char*cyfesuryn_x=cyrchfan_data;const unsigned char*Y_cyfesuryn=testun_data;if(cyfesuryn_x<Y_cyfesuryn){for(size_t 순번=0;순번<eitem_COUNT;순번++)cyfesuryn_x[순번]=Y_cyfesuryn[순번];}else while(eitem_COUNT){eitem_COUNT--;cyfesuryn_x[eitem_COUNT]=Y_cyfesuryn[eitem_COUNT];}return cyrchfan_data;}
static unsigned char cadw_lle_Are[6*1024*1024] __attribute__((aligned(16)));
typedef struct data_rhwystro {size_t Maint;struct data_rhwystro*Nesaf_eitem;int 남은공간;int 채울크기;uint64_t aliniad_gwers;} data_rhwystro;
static data_rhwystro *첫항목;
void free(void*data_safle){if(!data_safle)return;data_rhwystro*SECOND_VALUE=(data_rhwystro*)data_safle-1;SECOND_VALUE->남은공간=1;for(data_rhwystro*Nesaf_OFFSET=첫항목;Nesaf_OFFSET&&Nesaf_OFFSET->Nesaf_eitem;){if(Nesaf_OFFSET->남은공간&&Nesaf_OFFSET->Nesaf_eitem->남은공간){Nesaf_OFFSET->Maint+=sizeof(data_rhwystro)+Nesaf_OFFSET->Nesaf_eitem->Maint;Nesaf_OFFSET->Nesaf_eitem=Nesaf_OFFSET->Nesaf_eitem->Nesaf_eitem;}else Nesaf_OFFSET=Nesaf_OFFSET->Nesaf_eitem;}}
void *realloc(void*data_safle,size_t eitem_COUNT){
    if(!eitem_COUNT){free(data_safle);return 0;}if(eitem_COUNT>sizeof(cadw_lle_Are)-sizeof(data_rhwystro))return 0;eitem_COUNT=(eitem_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(data_rhwystro*)cadw_lle_Are;첫항목->Maint=sizeof(cadw_lle_Are)-sizeof(data_rhwystro);첫항목->남은공간=1;첫항목->Nesaf_eitem=0;}
    data_rhwystro*이전=data_safle?(data_rhwystro*)data_safle-1:0;if(이전&&이전->Maint>=eitem_COUNT)return data_safle;
    for(data_rhwystro*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Nesaf_eitem)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Maint>=eitem_COUNT){
        if(SECOND_VALUE->Maint>=eitem_COUNT+sizeof(data_rhwystro)+16){data_rhwystro*나머지부분=(data_rhwystro*)((unsigned char*)(SECOND_VALUE+1)+eitem_COUNT);나머지부분->Maint=SECOND_VALUE->Maint-eitem_COUNT-sizeof(data_rhwystro);나머지부분->Nesaf_eitem=SECOND_VALUE->Nesaf_eitem;나머지부분->남은공간=1;SECOND_VALUE->Nesaf_eitem=나머지부분;SECOND_VALUE->Maint=eitem_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,data_safle,이전->Maint);free(data_safle);}return 반환값;
    }Gwall=12;return 0;
}
void *malloc(size_t eitem_COUNT){return realloc(0,eitem_COUNT);}
void *calloc(size_t eitem_COUNT,size_t testun_data){if(testun_data&&eitem_COUNT>SIZE_MAX/testun_data)return 0;void*data_safle=malloc(eitem_COUNT*testun_data);if(data_safle)memset(data_safle,0,eitem_COUNT*testun_data);return data_safle;}
unsigned long long strtoull(const char*testun_data,char**gorffen_OFFSET,int Cefndir_VALUE){
    const char*START_OFFSET=testun_data;while(*testun_data==' '||(*testun_data>=9&&*testun_data<=13))testun_data++;int 음수여부=0;if(*testun_data=='-'||*testun_data=='+')음수여부=*testun_data++=='-';
    if((!Cefndir_VALUE||Cefndir_VALUE==16)&&testun_data[0]=='0'&&(testun_data[1]=='x'||testun_data[1]=='X')){Cefndir_VALUE=16;testun_data+=2;}if(!Cefndir_VALUE)Cefndir_VALUE=*testun_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned cod_nod=*testun_data,cyrchfan_data=cod_nod>='0'&&cod_nod<='9'?cod_nod-'0':cod_nod>='a'&&cod_nod<='z'?cod_nod-'a'+10:cod_nod>='A'&&cod_nod<='Z'?cod_nod-'A'+10:99;if(cyrchfan_data>=(unsigned)Cefndir_VALUE)break;하나라도=1;testun_data++;if(임시값>(~0ull-cyrchfan_data)/(unsigned)Cefndir_VALUE){임시값=~0ull;Gwall=34;}else 임시값=임시값*Cefndir_VALUE+cyrchfan_data;}
    if(gorffen_OFFSET)*gorffen_OFFSET=(char*)(하나라도?testun_data:START_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*testun_data,char**보조항목,int SECOND_VALUE){return strtoull(testun_data,보조항목,SECOND_VALUE);}
long strtol(const char*testun_data,char**보조항목,int SECOND_VALUE){return (long)strtoull(testun_data,보조항목,SECOND_VALUE);}
int atoi(const char*testun_data){return (int)strtol(testun_data,0,10);}
long double ldexpl(long double cyfesuryn_x,int eitem_COUNT){while(eitem_COUNT>0){cyfesuryn_x*=2;eitem_COUNT--;}while(eitem_COUNT<0){cyfesuryn_x/=2;eitem_COUNT++;}return cyfesuryn_x;}
long double strtold(const char*testun_data,char**gorffen_OFFSET){
    const char*START_OFFSET=testun_data;while(*testun_data==' '||(*testun_data>=9&&*testun_data<=13))testun_data++;int 음수여부=0;if(*testun_data=='-'||*testun_data=='+')음수여부=*testun_data++=='-';
    int Cefndir_VALUE=10;if(testun_data[0]=='0'&&(testun_data[1]=='x'||testun_data[1]=='X')){Cefndir_VALUE=16;testun_data+=2;}long double 임시값=0,graddio=1;int 소수부=0,하나라도=0;
    for(;;){int cod_nod=*testun_data,cyrchfan_data=cod_nod>='0'&&cod_nod<='9'?cod_nod-'0':cod_nod>='a'&&cod_nod<='f'?cod_nod-'a'+10:cod_nod>='A'&&cod_nod<='F'?cod_nod-'A'+10:99;
        if(cod_nod=='.'&&!소수부){소수부=1;testun_data++;continue;}if(cyrchfan_data>=Cefndir_VALUE)break;하나라도=1;testun_data++;임시값=임시값*Cefndir_VALUE+cyrchfan_data;if(소수부)graddio*=Cefndir_VALUE;
    }임시값/=graddio;
    if((Cefndir_VALUE==10&&(*testun_data=='e'||*testun_data=='E'))||(Cefndir_VALUE==16&&(*testun_data=='p'||*testun_data=='P'))){const char*sioe_VALUE=testun_data++;int 빼기=0;if(*testun_data=='-'||*testun_data=='+')빼기=*testun_data++=='-';int eitem_COUNT=0,cofnod_COUNT=0;while(*testun_data>='0'&&*testun_data<='9'){cofnod_COUNT++;if(eitem_COUNT<20000)eitem_COUNT=eitem_COUNT*10+*testun_data-'0';testun_data++;}if(!cofnod_COUNT)testun_data=sioe_VALUE;else{long double ffactor=Cefndir_VALUE==16?2:10;while(eitem_COUNT-->0&&eitem_COUNT<200000)임시값=빼기?임시값/ffactor:임시값*ffactor;}}
    if(gorffen_OFFSET)*gorffen_OFFSET=(char*)(하나라도?testun_data:START_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*testun_data,char**보조항목){return (double)strtold(testun_data,보조항목);}float strtof(const char*testun_data,char**보조항목){return (float)strtold(testun_data,보조항목);}
void qsort(void*Cefndir_VALUE,size_t eitem_COUNT,size_t Maint,int(*Cymharu)(const void*,const void*)){
    unsigned char*data_safle=Cefndir_VALUE;for(size_t 순번=1;순번<eitem_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Cymharu(data_safle+(안쪽순번-1)*Maint,data_safle+안쪽순번*Maint)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Maint;셋째순번++){unsigned char cod_nod=data_safle[(안쪽순번-1)*Maint+셋째순번];data_safle[(안쪽순번-1)*Maint+셋째순번]=data_safle[안쪽순번*Maint+셋째순번];data_safle[안쪽순번*Maint+셋째순번]=cod_nod;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t safle;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *eitem_COUNT){*eitem_COUNT=출력크기;return 출력결과;}
int open(const char*Enw,int 설정비트,...){
    if(!strcmp(Enw,"/@cc-output")){if(출력열림){Gwall=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Enw,번역기자원들[순번].Enw)){
        if(설정비트&3){Gwall=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].safle=0;return 128+안쪽순번;}Gwall=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Enw,설정비트,0,0,0,0);if(반환값<0){Gwall=-반환값;return -1;}return 반환값;
}
int close(int ffeil_dolen){if(ffeil_dolen==100){출력열림=0;return 0;}if(ffeil_dolen>=128&&ffeil_dolen<152){열림[ffeil_dolen-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,ffeil_dolen,0,0,0,0,0);if(반환값<0){Gwall=-반환값;return -1;}return 0;}
long read(int ffeil_dolen,void*data,size_t eitem_COUNT){
    if(ffeil_dolen>=128&&ffeil_dolen<152&&열림[ffeil_dolen-128].사용량){int 순번=ffeil_dolen-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Maint-열림[순번].safle;if(eitem_COUNT>왼쪽)eitem_COUNT=왼쪽;memcpy(data,반환값->data+열림[순번].safle,eitem_COUNT);열림[순번].safle+=eitem_COUNT;return eitem_COUNT;}
    intptr_t 반환값=사용자호출(2,ffeil_dolen,(uintptr_t)data,eitem_COUNT,0,0,0);if(반환값<0){Gwall=-반환값;return -1;}return 반환값;
}
long write(int ffeil_dolen,const void*data,size_t eitem_COUNT){
    if(ffeil_dolen==100){if(eitem_COUNT>sizeof(출력결과)-출력위치){Gwall=28;return -1;}memcpy(출력결과+출력위치,data,eitem_COUNT);출력위치+=eitem_COUNT;if(출력크기<출력위치)출력크기=출력위치;return eitem_COUNT;}
    intptr_t 반환값=사용자호출(1,ffeil_dolen,(uintptr_t)data,eitem_COUNT,0,0,0);if(반환값<0){Gwall=-반환값;return -1;}return 반환값;
}
long lseek(int ffeil_dolen,long OFFSET_VALUE,int 기준점){
    if(ffeil_dolen==100){long data_safle=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(data_safle<0||(size_t)data_safle>sizeof(출력결과)){Gwall=22;return -1;}출력위치=data_safle;return data_safle;}
    if(ffeil_dolen>=128&&ffeil_dolen<152&&열림[ffeil_dolen-128].사용량){int 순번=ffeil_dolen-128;long data_safle=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].safle:번역기자원들[열림[순번].LOOKUP_INDEX].Maint);if(data_safle<0||(size_t)data_safle>번역기자원들[열림[순번].LOOKUP_INDEX].Maint){Gwall=22;return -1;}열림[순번].safle=data_safle;return data_safle;}
    intptr_t 반환값=사용자호출(5,ffeil_dolen,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){Gwall=-반환값;return -1;}return 반환값;
}
int unlink(const char*Enw){intptr_t 반환값=사용자호출(11,(uintptr_t)Enw,0,0,0,0,0);if(반환값<0){Gwall=-반환값;return -1;}return 반환값;}
char *realpath(const char*Enw,char*mesur_data){if(!mesur_data){mesur_data=malloc(strlen(Enw)+1);if(!mesur_data)return 0;}return strcpy(mesur_data,Enw);}
char *getcwd(char*data_safle,size_t eitem_COUNT){if(eitem_COUNT<2){Gwall=34;return 0;}data_safle[0]='/';data_safle[1]=0;return data_safle;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terfynell_cofnod){time_t 임시값=0;if(Terfynell_cofnod)*Terfynell_cofnod=임시값;return 임시값;}
struct tm *localtime(const time_t*Terfynell_cofnod){(void)Terfynell_cofnod;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int ffeil_dolen,const char*dull_MODE){(void)dull_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Gwall=0;흐름목록[순번].ffeil_dolen=ffeil_dolen;return &흐름목록[순번];}Gwall=24;return 0;}
int fflush(FILE*ffeil_cofnod){return ffeil_cofnod&&ffeil_cofnod->Gwall?-1:0;}
int fclose(FILE*ffeil_cofnod){int 반환값=close(ffeil_cofnod->ffeil_dolen);if(ffeil_cofnod->Gwall)반환값=-1;ffeil_cofnod->사용량=0;return 반환값;}
size_t fwrite(const void*data_safle,size_t testun_data,size_t eitem_COUNT,FILE*ffeil_cofnod){if(!testun_data)return 0;if(eitem_COUNT>SIZE_MAX/testun_data){ffeil_cofnod->Gwall=1;return 0;}long 반환값=write(ffeil_cofnod->ffeil_dolen,data_safle,testun_data*eitem_COUNT);if(반환값<0){ffeil_cofnod->Gwall=1;return 0;}return (size_t)반환값/testun_data;}
int fputc(int cod_nod,FILE*ffeil_cofnod){unsigned char SECOND_VALUE=cod_nod;return fwrite(&SECOND_VALUE,1,1,ffeil_cofnod)==1?SECOND_VALUE:EOF;}
int fputs(const char*testun_data,FILE*ffeil_cofnod){return fwrite(testun_data,1,strlen(testun_data),ffeil_cofnod)==strlen(testun_data)?0:EOF;}
static void 넣기(char*mesur_data,size_t 용량한도,size_t*현재위치,char cod_nod){if(*현재위치+1<용량한도)mesur_data[*현재위치]=cod_nod;(*현재위치)++;}
int vsnprintf(char*mesur_data,size_t 용량한도,const char*fformat,va_list 가변인수){
    size_t 현재위치=0;while(*fformat){if(*fformat!='%'){넣기(mesur_data,용량한도,&현재위치,*fformat++);continue;}fformat++;
        int 왼쪽=0,영값=0,대체값=0;while(*fformat=='-'||*fformat=='0'||*fformat=='#'||*fformat=='+'||*fformat==' '){if(*fformat=='-')왼쪽=1;if(*fformat=='0')영값=1;if(*fformat=='#')대체값=1;fformat++;}
        int 너비=0,정밀도=-1;if(*fformat=='*'){너비=va_arg(가변인수,int);fformat++;}else while(*fformat>='0'&&*fformat<='9')너비=너비*10+*fformat++-'0';
        if(*fformat=='.'){fformat++;정밀도=0;if(*fformat=='*'){정밀도=va_arg(가변인수,int);fformat++;}else while(*fformat>='0'&&*fformat<='9')정밀도=정밀도*10+*fformat++-'0';}
        int 넓은글자=0;while(*fformat=='l'||*fformat=='z'||*fformat=='t'||*fformat=='j'||*fformat=='h'){if(*fformat!='h')넓은글자=1;fformat++;}
        char TYPE_ardal=*fformat?*fformat++:0,byffer_Storio[80];const char*testun_data=byffer_Storio;size_t eitem_COUNT=0;
        if(TYPE_ardal=='s'){testun_data=va_arg(가변인수,const char*);if(!testun_data)testun_data="(null)";eitem_COUNT=strlen(testun_data);if(정밀도>=0&&eitem_COUNT>(size_t)정밀도)eitem_COUNT=정밀도;}
        else if(TYPE_ardal=='c'){byffer_Storio[0]=va_arg(가변인수,int);eitem_COUNT=1;}
        else if(TYPE_ardal=='%'){byffer_Storio[0]='%';eitem_COUNT=1;}
        else if(TYPE_ardal=='d'||TYPE_ardal=='i'||TYPE_ardal=='u'||TYPE_ardal=='x'||TYPE_ardal=='X'||TYPE_ardal=='o'||TYPE_ardal=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_ardal=='d'||TYPE_ardal=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_ardal=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Cefndir_VALUE=TYPE_ardal=='x'||TYPE_ardal=='X'||TYPE_ardal=='p'?16:TYPE_ardal=='o'?8:10;char digid_COUNT[64];unsigned 사용량=0;
            do{digid_COUNT[사용량++]="0123456789abcdef"[VALUE%Cefndir_VALUE];VALUE/=Cefndir_VALUE;}while(VALUE);
            if(음수표시)byffer_Storio[eitem_COUNT++]='-';if(TYPE_ardal=='p'||(대체값&&Cefndir_VALUE==16)){byffer_Storio[eitem_COUNT++]='0';byffer_Storio[eitem_COUNT++]='x';}
            for(int llenwi_VALUE=(int)사용량;정밀도>llenwi_VALUE&&eitem_COUNT<sizeof(byffer_Storio)-사용량;llenwi_VALUE++)byffer_Storio[eitem_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(eitem_COUNT+사용량)&&eitem_COUNT<sizeof(byffer_Storio)-사용량)byffer_Storio[eitem_COUNT++]='0';
            while(사용량)byffer_Storio[eitem_COUNT++]=digid_COUNT[--사용량];
        }else{byffer_Storio[0]='?';eitem_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)eitem_COUNT){넣기(mesur_data,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<eitem_COUNT;순번++)넣기(mesur_data,용량한도,&현재위치,testun_data[순번]);while(왼쪽&&너비>(int)eitem_COUNT){넣기(mesur_data,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)mesur_data[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*mesur_data,size_t 용량한도,const char*ffeil_cofnod,...){va_list 첫째값;va_start(첫째값,ffeil_cofnod);int 반환값=vsnprintf(mesur_data,용량한도,ffeil_cofnod,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*mesur_data,const char*ffeil_cofnod,...){va_list 첫째값;va_start(첫째값,ffeil_cofnod);int 반환값=vsnprintf(mesur_data,SIZE_MAX,ffeil_cofnod,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*ffrwd_VALUE,const char*ffeil_cofnod,va_list 첫째값){char SECOND_VALUE[2048];int eitem_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),ffeil_cofnod,첫째값);if(eitem_COUNT>2047)eitem_COUNT=2047;return fwrite(SECOND_VALUE,1,eitem_COUNT,ffrwd_VALUE)==(size_t)eitem_COUNT?eitem_COUNT:-1;}
int fprintf(FILE*ffrwd_VALUE,const char*ffeil_cofnod,...){va_list 첫째값;va_start(첫째값,ffeil_cofnod);int 반환값=vfprintf(ffrwd_VALUE,ffeil_cofnod,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*ffeil_cofnod,...){va_list 첫째값;va_start(첫째값,ffeil_cofnod);int 반환값=vfprintf(stdout,ffeil_cofnod,첫째값);va_end(첫째값);return 반환값;}
