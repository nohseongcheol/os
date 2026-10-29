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
static int Fout;
int *__errno_location(void){return &Fout;}
void exit(int stand_VALUE){사용자호출(6,stand_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *tjek_uitdrukking,const char *Lêer,unsigned lyn,const char *metode_inskrywing_naam){fprintf(stderr,"cc assertion: %s %s:%u %s\n",tjek_uitdrukking,Lêer,lyn,metode_inskrywing_naam);exit(1);}
size_t strlen(const char*string_data){const char*data_plaas=string_data;while(*data_plaas)data_plaas++;return data_plaas-string_data;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t item_COUNT){while(item_COUNT--){unsigned char x_koördinaat=*첫째값++,Y_koördinaat=*SECOND_VALUE++;if(x_koördinaat!=Y_koördinaat)return x_koördinaat-Y_koördinaat;if(!x_koördinaat)return 0;}return 0;}
char *strcpy(char*bestemming_data,const char*string_data){char*반환값=bestemming_data;while((*bestemming_data++=*string_data++)){}return 반환값;}
char *strchr(const char*string_data,int karakterkode){do{if(*string_data==(char)karakterkode)return (char*)string_data;}while(*string_data++);return 0;}
char *strrchr(const char*string_data,int karakterkode){const char*반환값=0;do{if(*string_data==(char)karakterkode)반환값=string_data;}while(*string_data++);return (char*)반환값;}
char *strstr(const char*string_data,const char*Terminaal_inskrywing){size_t item_COUNT=strlen(Terminaal_inskrywing);for(;*string_data;string_data++)if(!strncmp(string_data,Terminaal_inskrywing,item_COUNT))return (char*)string_data;return item_COUNT?0:(char*)string_data;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t item_COUNT){const unsigned char*x_koördinaat=첫째값,*Y_koördinaat=SECOND_VALUE;while(item_COUNT--){if(*x_koördinaat!=*Y_koördinaat)return *x_koördinaat-*Y_koördinaat;x_koördinaat++;Y_koördinaat++;}return 0;}
void *memmove(void*bestemming_data,const void*string_data,size_t item_COUNT){unsigned char*x_koördinaat=bestemming_data;const unsigned char*Y_koördinaat=string_data;if(x_koördinaat<Y_koördinaat){for(size_t 순번=0;순번<item_COUNT;순번++)x_koördinaat[순번]=Y_koördinaat[순번];}else while(item_COUNT){item_COUNT--;x_koördinaat[item_COUNT]=Y_koördinaat[item_COUNT];}return bestemming_data;}
static unsigned char toewysing_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct data_blokkeer {size_t Grootte;struct data_blokkeer*Volgende_item;int 남은공간;int 채울크기;uint64_t belyning_les;} data_blokkeer;
static data_blokkeer *첫항목;
void free(void*data_plaas){if(!data_plaas)return;data_blokkeer*SECOND_VALUE=(data_blokkeer*)data_plaas-1;SECOND_VALUE->남은공간=1;for(data_blokkeer*Volgende_OFFSET=첫항목;Volgende_OFFSET&&Volgende_OFFSET->Volgende_item;){if(Volgende_OFFSET->남은공간&&Volgende_OFFSET->Volgende_item->남은공간){Volgende_OFFSET->Grootte+=sizeof(data_blokkeer)+Volgende_OFFSET->Volgende_item->Grootte;Volgende_OFFSET->Volgende_item=Volgende_OFFSET->Volgende_item->Volgende_item;}else Volgende_OFFSET=Volgende_OFFSET->Volgende_item;}}
void *realloc(void*data_plaas,size_t item_COUNT){
    if(!item_COUNT){free(data_plaas);return 0;}if(item_COUNT>sizeof(toewysing_Arena)-sizeof(data_blokkeer))return 0;item_COUNT=(item_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(data_blokkeer*)toewysing_Arena;첫항목->Grootte=sizeof(toewysing_Arena)-sizeof(data_blokkeer);첫항목->남은공간=1;첫항목->Volgende_item=0;}
    data_blokkeer*이전=data_plaas?(data_blokkeer*)data_plaas-1:0;if(이전&&이전->Grootte>=item_COUNT)return data_plaas;
    for(data_blokkeer*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Volgende_item)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Grootte>=item_COUNT){
        if(SECOND_VALUE->Grootte>=item_COUNT+sizeof(data_blokkeer)+16){data_blokkeer*나머지부분=(data_blokkeer*)((unsigned char*)(SECOND_VALUE+1)+item_COUNT);나머지부분->Grootte=SECOND_VALUE->Grootte-item_COUNT-sizeof(data_blokkeer);나머지부분->Volgende_item=SECOND_VALUE->Volgende_item;나머지부분->남은공간=1;SECOND_VALUE->Volgende_item=나머지부분;SECOND_VALUE->Grootte=item_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,data_plaas,이전->Grootte);free(data_plaas);}return 반환값;
    }Fout=12;return 0;
}
void *malloc(size_t item_COUNT){return realloc(0,item_COUNT);}
void *calloc(size_t item_COUNT,size_t string_data){if(string_data&&item_COUNT>SIZE_MAX/string_data)return 0;void*data_plaas=malloc(item_COUNT*string_data);if(data_plaas)memset(data_plaas,0,item_COUNT*string_data);return data_plaas;}
unsigned long long strtoull(const char*string_data,char**beëindig_OFFSET,int muur_VALUE){
    const char*BEGIN_OFFSET=string_data;while(*string_data==' '||(*string_data>=9&&*string_data<=13))string_data++;int 음수여부=0;if(*string_data=='-'||*string_data=='+')음수여부=*string_data++=='-';
    if((!muur_VALUE||muur_VALUE==16)&&string_data[0]=='0'&&(string_data[1]=='x'||string_data[1]=='X')){muur_VALUE=16;string_data+=2;}if(!muur_VALUE)muur_VALUE=*string_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned karakterkode=*string_data,bestemming_data=karakterkode>='0'&&karakterkode<='9'?karakterkode-'0':karakterkode>='a'&&karakterkode<='z'?karakterkode-'a'+10:karakterkode>='A'&&karakterkode<='Z'?karakterkode-'A'+10:99;if(bestemming_data>=(unsigned)muur_VALUE)break;하나라도=1;string_data++;if(임시값>(~0ull-bestemming_data)/(unsigned)muur_VALUE){임시값=~0ull;Fout=34;}else 임시값=임시값*muur_VALUE+bestemming_data;}
    if(beëindig_OFFSET)*beëindig_OFFSET=(char*)(하나라도?string_data:BEGIN_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*string_data,char**보조항목,int SECOND_VALUE){return strtoull(string_data,보조항목,SECOND_VALUE);}
long strtol(const char*string_data,char**보조항목,int SECOND_VALUE){return (long)strtoull(string_data,보조항목,SECOND_VALUE);}
int atoi(const char*string_data){return (int)strtol(string_data,0,10);}
long double ldexpl(long double x_koördinaat,int item_COUNT){while(item_COUNT>0){x_koördinaat*=2;item_COUNT--;}while(item_COUNT<0){x_koördinaat/=2;item_COUNT++;}return x_koördinaat;}
long double strtold(const char*string_data,char**beëindig_OFFSET){
    const char*BEGIN_OFFSET=string_data;while(*string_data==' '||(*string_data>=9&&*string_data<=13))string_data++;int 음수여부=0;if(*string_data=='-'||*string_data=='+')음수여부=*string_data++=='-';
    int muur_VALUE=10;if(string_data[0]=='0'&&(string_data[1]=='x'||string_data[1]=='X')){muur_VALUE=16;string_data+=2;}long double 임시값=0,skaleer=1;int 소수부=0,하나라도=0;
    for(;;){int karakterkode=*string_data,bestemming_data=karakterkode>='0'&&karakterkode<='9'?karakterkode-'0':karakterkode>='a'&&karakterkode<='f'?karakterkode-'a'+10:karakterkode>='A'&&karakterkode<='F'?karakterkode-'A'+10:99;
        if(karakterkode=='.'&&!소수부){소수부=1;string_data++;continue;}if(bestemming_data>=muur_VALUE)break;하나라도=1;string_data++;임시값=임시값*muur_VALUE+bestemming_data;if(소수부)skaleer*=muur_VALUE;
    }임시값/=skaleer;
    if((muur_VALUE==10&&(*string_data=='e'||*string_data=='E'))||(muur_VALUE==16&&(*string_data=='p'||*string_data=='P'))){const char*wys_VALUE=string_data++;int 빼기=0;if(*string_data=='-'||*string_data=='+')빼기=*string_data++=='-';int item_COUNT=0,inskrywing_COUNT=0;while(*string_data>='0'&&*string_data<='9'){inskrywing_COUNT++;if(item_COUNT<20000)item_COUNT=item_COUNT*10+*string_data-'0';string_data++;}if(!inskrywing_COUNT)string_data=wys_VALUE;else{long double faktor=muur_VALUE==16?2:10;while(item_COUNT-->0&&item_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(beëindig_OFFSET)*beëindig_OFFSET=(char*)(하나라도?string_data:BEGIN_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*string_data,char**보조항목){return (double)strtold(string_data,보조항목);}float strtof(const char*string_data,char**보조항목){return (float)strtold(string_data,보조항목);}
void qsort(void*muur_VALUE,size_t item_COUNT,size_t Grootte,int(*Vergelyk)(const void*,const void*)){
    unsigned char*data_plaas=muur_VALUE;for(size_t 순번=1;순번<item_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Vergelyk(data_plaas+(안쪽순번-1)*Grootte,data_plaas+안쪽순번*Grootte)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Grootte;셋째순번++){unsigned char karakterkode=data_plaas[(안쪽순번-1)*Grootte+셋째순번];data_plaas[(안쪽순번-1)*Grootte+셋째순번]=data_plaas[안쪽순번*Grootte+셋째순번];data_plaas[안쪽순번*Grootte+셋째순번]=karakterkode;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Posisie;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *item_COUNT){*item_COUNT=출력크기;return 출력결과;}
int open(const char*Naam,int konfigurasie_Agtergrond_intelligente_oordragdiens,...){
    if(!strcmp(Naam,"/@cc-output")){if(출력열림){Fout=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Naam,번역기자원들[순번].Naam)){
        if(konfigurasie_Agtergrond_intelligente_oordragdiens&3){Fout=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Posisie=0;return 128+안쪽순번;}Fout=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Naam,konfigurasie_Agtergrond_intelligente_oordragdiens,0,0,0,0);if(반환값<0){Fout=-반환값;return -1;}return 반환값;
}
int close(int lêer_handvatsel){if(lêer_handvatsel==100){출력열림=0;return 0;}if(lêer_handvatsel>=128&&lêer_handvatsel<152){열림[lêer_handvatsel-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,lêer_handvatsel,0,0,0,0,0);if(반환값<0){Fout=-반환값;return -1;}return 0;}
long read(int lêer_handvatsel,void*data,size_t item_COUNT){
    if(lêer_handvatsel>=128&&lêer_handvatsel<152&&열림[lêer_handvatsel-128].사용량){int 순번=lêer_handvatsel-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Grootte-열림[순번].Posisie;if(item_COUNT>왼쪽)item_COUNT=왼쪽;memcpy(data,반환값->data+열림[순번].Posisie,item_COUNT);열림[순번].Posisie+=item_COUNT;return item_COUNT;}
    intptr_t 반환값=사용자호출(2,lêer_handvatsel,(uintptr_t)data,item_COUNT,0,0,0);if(반환값<0){Fout=-반환값;return -1;}return 반환값;
}
long write(int lêer_handvatsel,const void*data,size_t item_COUNT){
    if(lêer_handvatsel==100){if(item_COUNT>sizeof(출력결과)-출력위치){Fout=28;return -1;}memcpy(출력결과+출력위치,data,item_COUNT);출력위치+=item_COUNT;if(출력크기<출력위치)출력크기=출력위치;return item_COUNT;}
    intptr_t 반환값=사용자호출(1,lêer_handvatsel,(uintptr_t)data,item_COUNT,0,0,0);if(반환값<0){Fout=-반환값;return -1;}return 반환값;
}
long lseek(int lêer_handvatsel,long OFFSET_VALUE,int 기준점){
    if(lêer_handvatsel==100){long data_plaas=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(data_plaas<0||(size_t)data_plaas>sizeof(출력결과)){Fout=22;return -1;}출력위치=data_plaas;return data_plaas;}
    if(lêer_handvatsel>=128&&lêer_handvatsel<152&&열림[lêer_handvatsel-128].사용량){int 순번=lêer_handvatsel-128;long data_plaas=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].Posisie:번역기자원들[열림[순번].LOOKUP_INDEX].Grootte);if(data_plaas<0||(size_t)data_plaas>번역기자원들[열림[순번].LOOKUP_INDEX].Grootte){Fout=22;return -1;}열림[순번].Posisie=data_plaas;return data_plaas;}
    intptr_t 반환값=사용자호출(5,lêer_handvatsel,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){Fout=-반환값;return -1;}return 반환값;
}
int unlink(const char*Naam){intptr_t 반환값=사용자호출(11,(uintptr_t)Naam,0,0,0,0,0);if(반환값<0){Fout=-반환값;return -1;}return 반환값;}
char *realpath(const char*Naam,char*maatreël_data){if(!maatreël_data){maatreël_data=malloc(strlen(Naam)+1);if(!maatreël_data)return 0;}return strcpy(maatreël_data,Naam);}
char *getcwd(char*data_plaas,size_t item_COUNT){if(item_COUNT<2){Fout=34;return 0;}data_plaas[0]='/';data_plaas[1]=0;return data_plaas;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminaal_inskrywing){time_t 임시값=0;if(Terminaal_inskrywing)*Terminaal_inskrywing=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminaal_inskrywing){(void)Terminaal_inskrywing;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int lêer_handvatsel,const char*metode_MODE){(void)metode_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Fout=0;흐름목록[순번].lêer_handvatsel=lêer_handvatsel;return &흐름목록[순번];}Fout=24;return 0;}
int fflush(FILE*lêer_inskrywing){return lêer_inskrywing&&lêer_inskrywing->Fout?-1:0;}
int fclose(FILE*lêer_inskrywing){int 반환값=close(lêer_inskrywing->lêer_handvatsel);if(lêer_inskrywing->Fout)반환값=-1;lêer_inskrywing->사용량=0;return 반환값;}
size_t fwrite(const void*data_plaas,size_t string_data,size_t item_COUNT,FILE*lêer_inskrywing){if(!string_data)return 0;if(item_COUNT>SIZE_MAX/string_data){lêer_inskrywing->Fout=1;return 0;}long 반환값=write(lêer_inskrywing->lêer_handvatsel,data_plaas,string_data*item_COUNT);if(반환값<0){lêer_inskrywing->Fout=1;return 0;}return (size_t)반환값/string_data;}
int fputc(int karakterkode,FILE*lêer_inskrywing){unsigned char SECOND_VALUE=karakterkode;return fwrite(&SECOND_VALUE,1,1,lêer_inskrywing)==1?SECOND_VALUE:EOF;}
int fputs(const char*string_data,FILE*lêer_inskrywing){return fwrite(string_data,1,strlen(string_data),lêer_inskrywing)==strlen(string_data)?0:EOF;}
static void 넣기(char*maatreël_data,size_t 용량한도,size_t*현재위치,char karakterkode){if(*현재위치+1<용량한도)maatreël_data[*현재위치]=karakterkode;(*현재위치)++;}
int vsnprintf(char*maatreël_data,size_t 용량한도,const char*formaat,va_list 가변인수){
    size_t 현재위치=0;while(*formaat){if(*formaat!='%'){넣기(maatreël_data,용량한도,&현재위치,*formaat++);continue;}formaat++;
        int 왼쪽=0,영값=0,대체값=0;while(*formaat=='-'||*formaat=='0'||*formaat=='#'||*formaat=='+'||*formaat==' '){if(*formaat=='-')왼쪽=1;if(*formaat=='0')영값=1;if(*formaat=='#')대체값=1;formaat++;}
        int 너비=0,정밀도=-1;if(*formaat=='*'){너비=va_arg(가변인수,int);formaat++;}else while(*formaat>='0'&&*formaat<='9')너비=너비*10+*formaat++-'0';
        if(*formaat=='.'){formaat++;정밀도=0;if(*formaat=='*'){정밀도=va_arg(가변인수,int);formaat++;}else while(*formaat>='0'&&*formaat<='9')정밀도=정밀도*10+*formaat++-'0';}
        int 넓은글자=0;while(*formaat=='l'||*formaat=='z'||*formaat=='t'||*formaat=='j'||*formaat=='h'){if(*formaat!='h')넓은글자=1;formaat++;}
        char TYPE_kategorie=*formaat?*formaat++:0,buffer_Berging[80];const char*string_data=buffer_Berging;size_t item_COUNT=0;
        if(TYPE_kategorie=='s'){string_data=va_arg(가변인수,const char*);if(!string_data)string_data="(null)";item_COUNT=strlen(string_data);if(정밀도>=0&&item_COUNT>(size_t)정밀도)item_COUNT=정밀도;}
        else if(TYPE_kategorie=='c'){buffer_Berging[0]=va_arg(가변인수,int);item_COUNT=1;}
        else if(TYPE_kategorie=='%'){buffer_Berging[0]='%';item_COUNT=1;}
        else if(TYPE_kategorie=='d'||TYPE_kategorie=='i'||TYPE_kategorie=='u'||TYPE_kategorie=='x'||TYPE_kategorie=='X'||TYPE_kategorie=='o'||TYPE_kategorie=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_kategorie=='d'||TYPE_kategorie=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_kategorie=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned muur_VALUE=TYPE_kategorie=='x'||TYPE_kategorie=='X'||TYPE_kategorie=='p'?16:TYPE_kategorie=='o'?8:10;char syfer_COUNT[64];unsigned 사용량=0;
            do{syfer_COUNT[사용량++]="0123456789abcdef"[VALUE%muur_VALUE];VALUE/=muur_VALUE;}while(VALUE);
            if(음수표시)buffer_Berging[item_COUNT++]='-';if(TYPE_kategorie=='p'||(대체값&&muur_VALUE==16)){buffer_Berging[item_COUNT++]='0';buffer_Berging[item_COUNT++]='x';}
            for(int vul_VALUE=(int)사용량;정밀도>vul_VALUE&&item_COUNT<sizeof(buffer_Berging)-사용량;vul_VALUE++)buffer_Berging[item_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(item_COUNT+사용량)&&item_COUNT<sizeof(buffer_Berging)-사용량)buffer_Berging[item_COUNT++]='0';
            while(사용량)buffer_Berging[item_COUNT++]=syfer_COUNT[--사용량];
        }else{buffer_Berging[0]='?';item_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)item_COUNT){넣기(maatreël_data,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<item_COUNT;순번++)넣기(maatreël_data,용량한도,&현재위치,string_data[순번]);while(왼쪽&&너비>(int)item_COUNT){넣기(maatreël_data,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)maatreël_data[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*maatreël_data,size_t 용량한도,const char*lêer_inskrywing,...){va_list 첫째값;va_start(첫째값,lêer_inskrywing);int 반환값=vsnprintf(maatreël_data,용량한도,lêer_inskrywing,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*maatreël_data,const char*lêer_inskrywing,...){va_list 첫째값;va_start(첫째값,lêer_inskrywing);int 반환값=vsnprintf(maatreël_data,SIZE_MAX,lêer_inskrywing,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*lêer_inskrywing,va_list 첫째값){char SECOND_VALUE[2048];int item_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),lêer_inskrywing,첫째값);if(item_COUNT>2047)item_COUNT=2047;return fwrite(SECOND_VALUE,1,item_COUNT,Stream_VALUE)==(size_t)item_COUNT?item_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*lêer_inskrywing,...){va_list 첫째값;va_start(첫째값,lêer_inskrywing);int 반환값=vfprintf(Stream_VALUE,lêer_inskrywing,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*lêer_inskrywing,...){va_list 첫째값;va_start(첫째값,lêer_inskrywing);int 반환값=vfprintf(stdout,lêer_inskrywing,첫째값);va_end(첫째값);return 반환값;}
