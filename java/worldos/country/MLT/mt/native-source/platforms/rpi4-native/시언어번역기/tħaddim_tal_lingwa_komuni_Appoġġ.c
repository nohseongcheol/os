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
static int żball;
int *__errno_location(void){return &żball;}
void exit(int stat_VALUE){사용자호출(6,stat_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *ċekk_espressjoni,const char *fajl,unsigned linja,const char *metodu_entrata_isem){fprintf(stderr,"cc assertion: %s %s:%u %s\n",ċekk_espressjoni,fajl,linja,metodu_entrata_isem);exit(1);}
size_t strlen(const char*string_data){const char*data_pożizzjoni=string_data;while(*data_pożizzjoni)data_pożizzjoni++;return data_pożizzjoni-string_data;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t element_COUNT){while(element_COUNT--){unsigned char koordinat_x=*첫째값++,세로좌표=*SECOND_VALUE++;if(koordinat_x!=세로좌표)return koordinat_x-세로좌표;if(!koordinat_x)return 0;}return 0;}
char *strcpy(char*destinazzjoni_data,const char*string_data){char*반환값=destinazzjoni_data;while((*destinazzjoni_data++=*string_data++)){}return 반환값;}
char *strchr(const char*string_data,int kodiċi_tal_karattru){do{if(*string_data==(char)kodiċi_tal_karattru)return (char*)string_data;}while(*string_data++);return 0;}
char *strrchr(const char*string_data,int kodiċi_tal_karattru){const char*반환값=0;do{if(*string_data==(char)kodiċi_tal_karattru)반환값=string_data;}while(*string_data++);return (char*)반환값;}
char *strstr(const char*string_data,const char*Terminal_entrata){size_t element_COUNT=strlen(Terminal_entrata);for(;*string_data;string_data++)if(!strncmp(string_data,Terminal_entrata,element_COUNT))return (char*)string_data;return element_COUNT?0:(char*)string_data;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t element_COUNT){const unsigned char*koordinat_x=첫째값,*세로좌표=SECOND_VALUE;while(element_COUNT--){if(*koordinat_x!=*세로좌표)return *koordinat_x-*세로좌표;koordinat_x++;세로좌표++;}return 0;}
void *memmove(void*destinazzjoni_data,const void*string_data,size_t element_COUNT){unsigned char*koordinat_x=destinazzjoni_data;const unsigned char*세로좌표=string_data;if(koordinat_x<세로좌표){for(size_t 순번=0;순번<element_COUNT;순번++)koordinat_x[순번]=세로좌표[순번];}else while(element_COUNT){element_COUNT--;koordinat_x[element_COUNT]=세로좌표[element_COUNT];}return destinazzjoni_data;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct data_imblokka {size_t daqqas;struct data_imblokka*Li_Jmiss_element;int 남은공간;int 채울크기;uint64_t allinjament_lezzjoni;} data_imblokka;
static data_imblokka *첫항목;
void free(void*data_pożizzjoni){if(!data_pożizzjoni)return;data_imblokka*SECOND_VALUE=(data_imblokka*)data_pożizzjoni-1;SECOND_VALUE->남은공간=1;for(data_imblokka*Li_Jmiss_OFFSET=첫항목;Li_Jmiss_OFFSET&&Li_Jmiss_OFFSET->Li_Jmiss_element;){if(Li_Jmiss_OFFSET->남은공간&&Li_Jmiss_OFFSET->Li_Jmiss_element->남은공간){Li_Jmiss_OFFSET->daqqas+=sizeof(data_imblokka)+Li_Jmiss_OFFSET->Li_Jmiss_element->daqqas;Li_Jmiss_OFFSET->Li_Jmiss_element=Li_Jmiss_OFFSET->Li_Jmiss_element->Li_Jmiss_element;}else Li_Jmiss_OFFSET=Li_Jmiss_OFFSET->Li_Jmiss_element;}}
void *realloc(void*data_pożizzjoni,size_t element_COUNT){
    if(!element_COUNT){free(data_pożizzjoni);return 0;}if(element_COUNT>sizeof(할당마당)-sizeof(data_imblokka))return 0;element_COUNT=(element_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(data_imblokka*)할당마당;첫항목->daqqas=sizeof(할당마당)-sizeof(data_imblokka);첫항목->남은공간=1;첫항목->Li_Jmiss_element=0;}
    data_imblokka*이전=data_pożizzjoni?(data_imblokka*)data_pożizzjoni-1:0;if(이전&&이전->daqqas>=element_COUNT)return data_pożizzjoni;
    for(data_imblokka*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Li_Jmiss_element)if(SECOND_VALUE->남은공간&&SECOND_VALUE->daqqas>=element_COUNT){
        if(SECOND_VALUE->daqqas>=element_COUNT+sizeof(data_imblokka)+16){data_imblokka*나머지부분=(data_imblokka*)((unsigned char*)(SECOND_VALUE+1)+element_COUNT);나머지부분->daqqas=SECOND_VALUE->daqqas-element_COUNT-sizeof(data_imblokka);나머지부분->Li_Jmiss_element=SECOND_VALUE->Li_Jmiss_element;나머지부분->남은공간=1;SECOND_VALUE->Li_Jmiss_element=나머지부분;SECOND_VALUE->daqqas=element_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,data_pożizzjoni,이전->daqqas);free(data_pożizzjoni);}return 반환값;
    }żball=12;return 0;
}
void *malloc(size_t element_COUNT){return realloc(0,element_COUNT);}
void *calloc(size_t element_COUNT,size_t string_data){if(string_data&&element_COUNT>SIZE_MAX/string_data)return 0;void*data_pożizzjoni=malloc(element_COUNT*string_data);if(data_pożizzjoni)memset(data_pożizzjoni,0,element_COUNT*string_data);return data_pożizzjoni;}
unsigned long long strtoull(const char*string_data,char**ttermina_OFFSET,int Sfond_VALUE){
    const char*Bidu_OFFSET=string_data;while(*string_data==' '||(*string_data>=9&&*string_data<=13))string_data++;int 음수여부=0;if(*string_data=='-'||*string_data=='+')음수여부=*string_data++=='-';
    if((!Sfond_VALUE||Sfond_VALUE==16)&&string_data[0]=='0'&&(string_data[1]=='x'||string_data[1]=='X')){Sfond_VALUE=16;string_data+=2;}if(!Sfond_VALUE)Sfond_VALUE=*string_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kodiċi_tal_karattru=*string_data,destinazzjoni_data=kodiċi_tal_karattru>='0'&&kodiċi_tal_karattru<='9'?kodiċi_tal_karattru-'0':kodiċi_tal_karattru>='a'&&kodiċi_tal_karattru<='z'?kodiċi_tal_karattru-'a'+10:kodiċi_tal_karattru>='A'&&kodiċi_tal_karattru<='Z'?kodiċi_tal_karattru-'A'+10:99;if(destinazzjoni_data>=(unsigned)Sfond_VALUE)break;하나라도=1;string_data++;if(임시값>(~0ull-destinazzjoni_data)/(unsigned)Sfond_VALUE){임시값=~0ull;żball=34;}else 임시값=임시값*Sfond_VALUE+destinazzjoni_data;}
    if(ttermina_OFFSET)*ttermina_OFFSET=(char*)(하나라도?string_data:Bidu_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*string_data,char**보조항목,int SECOND_VALUE){return strtoull(string_data,보조항목,SECOND_VALUE);}
long strtol(const char*string_data,char**보조항목,int SECOND_VALUE){return (long)strtoull(string_data,보조항목,SECOND_VALUE);}
int atoi(const char*string_data){return (int)strtol(string_data,0,10);}
long double ldexpl(long double koordinat_x,int element_COUNT){while(element_COUNT>0){koordinat_x*=2;element_COUNT--;}while(element_COUNT<0){koordinat_x/=2;element_COUNT++;}return koordinat_x;}
long double strtold(const char*string_data,char**ttermina_OFFSET){
    const char*Bidu_OFFSET=string_data;while(*string_data==' '||(*string_data>=9&&*string_data<=13))string_data++;int 음수여부=0;if(*string_data=='-'||*string_data=='+')음수여부=*string_data++=='-';
    int Sfond_VALUE=10;if(string_data[0]=='0'&&(string_data[1]=='x'||string_data[1]=='X')){Sfond_VALUE=16;string_data+=2;}long double 임시값=0,daqqas_2eea83de=1;int 소수부=0,하나라도=0;
    for(;;){int kodiċi_tal_karattru=*string_data,destinazzjoni_data=kodiċi_tal_karattru>='0'&&kodiċi_tal_karattru<='9'?kodiċi_tal_karattru-'0':kodiċi_tal_karattru>='a'&&kodiċi_tal_karattru<='f'?kodiċi_tal_karattru-'a'+10:kodiċi_tal_karattru>='A'&&kodiċi_tal_karattru<='F'?kodiċi_tal_karattru-'A'+10:99;
        if(kodiċi_tal_karattru=='.'&&!소수부){소수부=1;string_data++;continue;}if(destinazzjoni_data>=Sfond_VALUE)break;하나라도=1;string_data++;임시값=임시값*Sfond_VALUE+destinazzjoni_data;if(소수부)daqqas_2eea83de*=Sfond_VALUE;
    }임시값/=daqqas_2eea83de;
    if((Sfond_VALUE==10&&(*string_data=='e'||*string_data=='E'))||(Sfond_VALUE==16&&(*string_data=='p'||*string_data=='P'))){const char*wera_VALUE_487749b8=string_data++;int 빼기=0;if(*string_data=='-'||*string_data=='+')빼기=*string_data++=='-';int element_COUNT=0,entrata_COUNT=0;while(*string_data>='0'&&*string_data<='9'){entrata_COUNT++;if(element_COUNT<20000)element_COUNT=element_COUNT*10+*string_data-'0';string_data++;}if(!entrata_COUNT)string_data=wera_VALUE_487749b8;else{long double fattur=Sfond_VALUE==16?2:10;while(element_COUNT-->0&&element_COUNT<200000)임시값=빼기?임시값/fattur:임시값*fattur;}}
    if(ttermina_OFFSET)*ttermina_OFFSET=(char*)(하나라도?string_data:Bidu_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*string_data,char**보조항목){return (double)strtold(string_data,보조항목);}float strtof(const char*string_data,char**보조항목){return (float)strtold(string_data,보조항목);}
void qsort(void*Sfond_VALUE,size_t element_COUNT,size_t daqqas,int(*Qabbel)(const void*,const void*)){
    unsigned char*data_pożizzjoni=Sfond_VALUE;for(size_t 순번=1;순번<element_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Qabbel(data_pożizzjoni+(안쪽순번-1)*daqqas,data_pożizzjoni+안쪽순번*daqqas)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<daqqas;셋째순번++){unsigned char kodiċi_tal_karattru=data_pożizzjoni[(안쪽순번-1)*daqqas+셋째순번];data_pożizzjoni[(안쪽순번-1)*daqqas+셋째순번]=data_pożizzjoni[안쪽순번*daqqas+셋째순번];data_pożizzjoni[안쪽순번*daqqas+셋째순번]=kodiċi_tal_karattru;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t pożizzjoni;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *element_COUNT){*element_COUNT=출력크기;return 출력결과;}
int open(const char*isem,int 설정비트,...){
    if(!strcmp(isem,"/@cc-output")){if(출력열림){żball=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(isem,번역기자원들[순번].isem)){
        if(설정비트&3){żball=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].pożizzjoni=0;return 128+안쪽순번;}żball=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)isem,설정비트,0,0,0,0);if(반환값<0){żball=-반환값;return -1;}return 반환값;
}
int close(int fajl_handle){if(fajl_handle==100){출력열림=0;return 0;}if(fajl_handle>=128&&fajl_handle<152){열림[fajl_handle-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fajl_handle,0,0,0,0,0);if(반환값<0){żball=-반환값;return -1;}return 0;}
long read(int fajl_handle,void*data,size_t element_COUNT){
    if(fajl_handle>=128&&fajl_handle<152&&열림[fajl_handle-128].사용량){int 순번=fajl_handle-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->daqqas-열림[순번].pożizzjoni;if(element_COUNT>왼쪽)element_COUNT=왼쪽;memcpy(data,반환값->data+열림[순번].pożizzjoni,element_COUNT);열림[순번].pożizzjoni+=element_COUNT;return element_COUNT;}
    intptr_t 반환값=사용자호출(2,fajl_handle,(uintptr_t)data,element_COUNT,0,0,0);if(반환값<0){żball=-반환값;return -1;}return 반환값;
}
long write(int fajl_handle,const void*data,size_t element_COUNT){
    if(fajl_handle==100){if(element_COUNT>sizeof(출력결과)-출력위치){żball=28;return -1;}memcpy(출력결과+출력위치,data,element_COUNT);출력위치+=element_COUNT;if(출력크기<출력위치)출력크기=출력위치;return element_COUNT;}
    intptr_t 반환값=사용자호출(1,fajl_handle,(uintptr_t)data,element_COUNT,0,0,0);if(반환값<0){żball=-반환값;return -1;}return 반환값;
}
long lseek(int fajl_handle,long OFFSET_VALUE,int 기준점){
    if(fajl_handle==100){long data_pożizzjoni=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(data_pożizzjoni<0||(size_t)data_pożizzjoni>sizeof(출력결과)){żball=22;return -1;}출력위치=data_pożizzjoni;return data_pożizzjoni;}
    if(fajl_handle>=128&&fajl_handle<152&&열림[fajl_handle-128].사용량){int 순번=fajl_handle-128;long data_pożizzjoni=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].pożizzjoni:번역기자원들[열림[순번].LOOKUP_INDEX].daqqas);if(data_pożizzjoni<0||(size_t)data_pożizzjoni>번역기자원들[열림[순번].LOOKUP_INDEX].daqqas){żball=22;return -1;}열림[순번].pożizzjoni=data_pożizzjoni;return data_pożizzjoni;}
    intptr_t 반환값=사용자호출(5,fajl_handle,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){żball=-반환값;return -1;}return 반환값;
}
int unlink(const char*isem){intptr_t 반환값=사용자호출(11,(uintptr_t)isem,0,0,0,0,0);if(반환값<0){żball=-반환값;return -1;}return 반환값;}
char *realpath(const char*isem,char*miżura_data){if(!miżura_data){miżura_data=malloc(strlen(isem)+1);if(!miżura_data)return 0;}return strcpy(miżura_data,isem);}
char *getcwd(char*data_pożizzjoni,size_t element_COUNT){if(element_COUNT<2){żball=34;return 0;}data_pożizzjoni[0]='/';data_pożizzjoni[1]=0;return data_pożizzjoni;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_entrata){time_t 임시값=0;if(Terminal_entrata)*Terminal_entrata=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_entrata){(void)Terminal_entrata;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int fajl_handle,const char*metodu_MODE){(void)metodu_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].żball=0;흐름목록[순번].fajl_handle=fajl_handle;return &흐름목록[순번];}żball=24;return 0;}
int fflush(FILE*fajl_entrata){return fajl_entrata&&fajl_entrata->żball?-1:0;}
int fclose(FILE*fajl_entrata){int 반환값=close(fajl_entrata->fajl_handle);if(fajl_entrata->żball)반환값=-1;fajl_entrata->사용량=0;return 반환값;}
size_t fwrite(const void*data_pożizzjoni,size_t string_data,size_t element_COUNT,FILE*fajl_entrata){if(!string_data)return 0;if(element_COUNT>SIZE_MAX/string_data){fajl_entrata->żball=1;return 0;}long 반환값=write(fajl_entrata->fajl_handle,data_pożizzjoni,string_data*element_COUNT);if(반환값<0){fajl_entrata->żball=1;return 0;}return (size_t)반환값/string_data;}
int fputc(int kodiċi_tal_karattru,FILE*fajl_entrata){unsigned char SECOND_VALUE=kodiċi_tal_karattru;return fwrite(&SECOND_VALUE,1,1,fajl_entrata)==1?SECOND_VALUE:EOF;}
int fputs(const char*string_data,FILE*fajl_entrata){return fwrite(string_data,1,strlen(string_data),fajl_entrata)==strlen(string_data)?0:EOF;}
static void 넣기(char*miżura_data,size_t 용량한도,size_t*현재위치,char kodiċi_tal_karattru){if(*현재위치+1<용량한도)miżura_data[*현재위치]=kodiċi_tal_karattru;(*현재위치)++;}
int vsnprintf(char*miżura_data,size_t 용량한도,const char*format,va_list 가변인수){
    size_t 현재위치=0;while(*format){if(*format!='%'){넣기(miżura_data,용량한도,&현재위치,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,정밀도=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;정밀도=0;if(*format=='*'){정밀도=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')정밀도=정밀도*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TYPE_kategorija=*format?*format++:0,bafer_Ħażna[80];const char*string_data=bafer_Ħażna;size_t element_COUNT=0;
        if(TYPE_kategorija=='s'){string_data=va_arg(가변인수,const char*);if(!string_data)string_data="(null)";element_COUNT=strlen(string_data);if(정밀도>=0&&element_COUNT>(size_t)정밀도)element_COUNT=정밀도;}
        else if(TYPE_kategorija=='c'){bafer_Ħażna[0]=va_arg(가변인수,int);element_COUNT=1;}
        else if(TYPE_kategorija=='%'){bafer_Ħażna[0]='%';element_COUNT=1;}
        else if(TYPE_kategorija=='d'||TYPE_kategorija=='i'||TYPE_kategorija=='u'||TYPE_kategorija=='x'||TYPE_kategorija=='X'||TYPE_kategorija=='o'||TYPE_kategorija=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_kategorija=='d'||TYPE_kategorija=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_kategorija=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Sfond_VALUE=TYPE_kategorija=='x'||TYPE_kategorija=='X'||TYPE_kategorija=='p'?16:TYPE_kategorija=='o'?8:10;char ċifra_COUNT[64];unsigned 사용량=0;
            do{ċifra_COUNT[사용량++]="0123456789abcdef"[VALUE%Sfond_VALUE];VALUE/=Sfond_VALUE;}while(VALUE);
            if(음수표시)bafer_Ħażna[element_COUNT++]='-';if(TYPE_kategorija=='p'||(대체값&&Sfond_VALUE==16)){bafer_Ħażna[element_COUNT++]='0';bafer_Ħażna[element_COUNT++]='x';}
            for(int imla_VALUE=(int)사용량;정밀도>imla_VALUE&&element_COUNT<sizeof(bafer_Ħażna)-사용량;imla_VALUE++)bafer_Ħażna[element_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(element_COUNT+사용량)&&element_COUNT<sizeof(bafer_Ħażna)-사용량)bafer_Ħażna[element_COUNT++]='0';
            while(사용량)bafer_Ħażna[element_COUNT++]=ċifra_COUNT[--사용량];
        }else{bafer_Ħażna[0]='?';element_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)element_COUNT){넣기(miżura_data,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<element_COUNT;순번++)넣기(miżura_data,용량한도,&현재위치,string_data[순번]);while(왼쪽&&너비>(int)element_COUNT){넣기(miżura_data,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)miżura_data[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*miżura_data,size_t 용량한도,const char*fajl_entrata,...){va_list 첫째값;va_start(첫째값,fajl_entrata);int 반환값=vsnprintf(miżura_data,용량한도,fajl_entrata,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*miżura_data,const char*fajl_entrata,...){va_list 첫째값;va_start(첫째값,fajl_entrata);int 반환값=vsnprintf(miżura_data,SIZE_MAX,fajl_entrata,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*fajl_entrata,va_list 첫째값){char SECOND_VALUE[2048];int element_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),fajl_entrata,첫째값);if(element_COUNT>2047)element_COUNT=2047;return fwrite(SECOND_VALUE,1,element_COUNT,Stream_VALUE)==(size_t)element_COUNT?element_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*fajl_entrata,...){va_list 첫째값;va_start(첫째값,fajl_entrata);int 반환값=vfprintf(Stream_VALUE,fajl_entrata,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fajl_entrata,...){va_list 첫째값;va_start(첫째값,fajl_entrata);int 반환값=vfprintf(stdout,fajl_entrata,첫째값);va_end(첫째값);return 반환값;}
