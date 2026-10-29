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
static int error;
int *__errno_location(void){return &error;}
void exit(int katayuan_VALUE){사용자호출(6,katayuan_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *tseke_expression,const char *file,unsigned linya,const char *pamamaraan_pagpasok_pangalan){fprintf(stderr,"cc assertion: %s %s:%u %s\n",tseke_expression,file,linya,pamamaraan_pagpasok_pangalan);exit(1);}
size_t strlen(const char*string_data){const char*data_posisyon=string_data;while(*data_posisyon)data_posisyon++;return data_posisyon-string_data;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t item_COUNT){while(item_COUNT--){unsigned char x_coordinate=*첫째값++,Y_button_coordinate=*SECOND_VALUE++;if(x_coordinate!=Y_button_coordinate)return x_coordinate-Y_button_coordinate;if(!x_coordinate)return 0;}return 0;}
char *strcpy(char*patutunguhan_data,const char*string_data){char*반환값=patutunguhan_data;while((*patutunguhan_data++=*string_data++)){}return 반환값;}
char *strchr(const char*string_data,int character_code){do{if(*string_data==(char)character_code)return (char*)string_data;}while(*string_data++);return 0;}
char *strrchr(const char*string_data,int character_code){const char*반환값=0;do{if(*string_data==(char)character_code)반환값=string_data;}while(*string_data++);return (char*)반환값;}
char *strstr(const char*string_data,const char*Terminal_pagpasok){size_t item_COUNT=strlen(Terminal_pagpasok);for(;*string_data;string_data++)if(!strncmp(string_data,Terminal_pagpasok,item_COUNT))return (char*)string_data;return item_COUNT?0:(char*)string_data;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t item_COUNT){const unsigned char*x_coordinate=첫째값,*Y_button_coordinate=SECOND_VALUE;while(item_COUNT--){if(*x_coordinate!=*Y_button_coordinate)return *x_coordinate-*Y_button_coordinate;x_coordinate++;Y_button_coordinate++;}return 0;}
void *memmove(void*patutunguhan_data,const void*string_data,size_t item_COUNT){unsigned char*x_coordinate=patutunguhan_data;const unsigned char*Y_button_coordinate=string_data;if(x_coordinate<Y_button_coordinate){for(size_t 순번=0;순번<item_COUNT;순번++)x_coordinate[순번]=Y_button_coordinate[순번];}else while(item_COUNT){item_COUNT--;x_coordinate[item_COUNT]=Y_button_coordinate[item_COUNT];}return patutunguhan_data;}
static unsigned char paglaan_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct data_i_block {size_t sukat_82232621;struct data_i_block*Susunod_item;int 남은공간;int 채울크기;uint64_t paghahanay_aralin;} data_i_block;
static data_i_block *첫항목;
void free(void*data_posisyon){if(!data_posisyon)return;data_i_block*SECOND_VALUE=(data_i_block*)data_posisyon-1;SECOND_VALUE->남은공간=1;for(data_i_block*Susunod_OFFSET=첫항목;Susunod_OFFSET&&Susunod_OFFSET->Susunod_item;){if(Susunod_OFFSET->남은공간&&Susunod_OFFSET->Susunod_item->남은공간){Susunod_OFFSET->sukat_82232621+=sizeof(data_i_block)+Susunod_OFFSET->Susunod_item->sukat_82232621;Susunod_OFFSET->Susunod_item=Susunod_OFFSET->Susunod_item->Susunod_item;}else Susunod_OFFSET=Susunod_OFFSET->Susunod_item;}}
void *realloc(void*data_posisyon,size_t item_COUNT){
    if(!item_COUNT){free(data_posisyon);return 0;}if(item_COUNT>sizeof(paglaan_Arena)-sizeof(data_i_block))return 0;item_COUNT=(item_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(data_i_block*)paglaan_Arena;첫항목->sukat_82232621=sizeof(paglaan_Arena)-sizeof(data_i_block);첫항목->남은공간=1;첫항목->Susunod_item=0;}
    data_i_block*이전=data_posisyon?(data_i_block*)data_posisyon-1:0;if(이전&&이전->sukat_82232621>=item_COUNT)return data_posisyon;
    for(data_i_block*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Susunod_item)if(SECOND_VALUE->남은공간&&SECOND_VALUE->sukat_82232621>=item_COUNT){
        if(SECOND_VALUE->sukat_82232621>=item_COUNT+sizeof(data_i_block)+16){data_i_block*나머지부분=(data_i_block*)((unsigned char*)(SECOND_VALUE+1)+item_COUNT);나머지부분->sukat_82232621=SECOND_VALUE->sukat_82232621-item_COUNT-sizeof(data_i_block);나머지부분->Susunod_item=SECOND_VALUE->Susunod_item;나머지부분->남은공간=1;SECOND_VALUE->Susunod_item=나머지부분;SECOND_VALUE->sukat_82232621=item_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,data_posisyon,이전->sukat_82232621);free(data_posisyon);}return 반환값;
    }error=12;return 0;
}
void *malloc(size_t item_COUNT){return realloc(0,item_COUNT);}
void *calloc(size_t item_COUNT,size_t string_data){if(string_data&&item_COUNT>SIZE_MAX/string_data)return 0;void*data_posisyon=malloc(item_COUNT*string_data);if(data_posisyon)memset(data_posisyon,0,item_COUNT*string_data);return data_posisyon;}
unsigned long long strtoull(const char*string_data,char**tapusin_OFFSET,int wallpaper_VALUE){
    const char*Start_OFFSET=string_data;while(*string_data==' '||(*string_data>=9&&*string_data<=13))string_data++;int 음수여부=0;if(*string_data=='-'||*string_data=='+')음수여부=*string_data++=='-';
    if((!wallpaper_VALUE||wallpaper_VALUE==16)&&string_data[0]=='0'&&(string_data[1]=='x'||string_data[1]=='X')){wallpaper_VALUE=16;string_data+=2;}if(!wallpaper_VALUE)wallpaper_VALUE=*string_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned character_code=*string_data,patutunguhan_data=character_code>='0'&&character_code<='9'?character_code-'0':character_code>='a'&&character_code<='z'?character_code-'a'+10:character_code>='A'&&character_code<='Z'?character_code-'A'+10:99;if(patutunguhan_data>=(unsigned)wallpaper_VALUE)break;하나라도=1;string_data++;if(임시값>(~0ull-patutunguhan_data)/(unsigned)wallpaper_VALUE){임시값=~0ull;error=34;}else 임시값=임시값*wallpaper_VALUE+patutunguhan_data;}
    if(tapusin_OFFSET)*tapusin_OFFSET=(char*)(하나라도?string_data:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*string_data,char**보조항목,int SECOND_VALUE){return strtoull(string_data,보조항목,SECOND_VALUE);}
long strtol(const char*string_data,char**보조항목,int SECOND_VALUE){return (long)strtoull(string_data,보조항목,SECOND_VALUE);}
int atoi(const char*string_data){return (int)strtol(string_data,0,10);}
long double ldexpl(long double x_coordinate,int item_COUNT){while(item_COUNT>0){x_coordinate*=2;item_COUNT--;}while(item_COUNT<0){x_coordinate/=2;item_COUNT++;}return x_coordinate;}
long double strtold(const char*string_data,char**tapusin_OFFSET){
    const char*Start_OFFSET=string_data;while(*string_data==' '||(*string_data>=9&&*string_data<=13))string_data++;int 음수여부=0;if(*string_data=='-'||*string_data=='+')음수여부=*string_data++=='-';
    int wallpaper_VALUE=10;if(string_data[0]=='0'&&(string_data[1]=='x'||string_data[1]=='X')){wallpaper_VALUE=16;string_data+=2;}long double 임시값=0,mag_eskala=1;int 소수부=0,하나라도=0;
    for(;;){int character_code=*string_data,patutunguhan_data=character_code>='0'&&character_code<='9'?character_code-'0':character_code>='a'&&character_code<='f'?character_code-'a'+10:character_code>='A'&&character_code<='F'?character_code-'A'+10:99;
        if(character_code=='.'&&!소수부){소수부=1;string_data++;continue;}if(patutunguhan_data>=wallpaper_VALUE)break;하나라도=1;string_data++;임시값=임시값*wallpaper_VALUE+patutunguhan_data;if(소수부)mag_eskala*=wallpaper_VALUE;
    }임시값/=mag_eskala;
    if((wallpaper_VALUE==10&&(*string_data=='e'||*string_data=='E'))||(wallpaper_VALUE==16&&(*string_data=='p'||*string_data=='P'))){const char*ipakita_VALUE=string_data++;int 빼기=0;if(*string_data=='-'||*string_data=='+')빼기=*string_data++=='-';int item_COUNT=0,pagpasok_COUNT=0;while(*string_data>='0'&&*string_data<='9'){pagpasok_COUNT++;if(item_COUNT<20000)item_COUNT=item_COUNT*10+*string_data-'0';string_data++;}if(!pagpasok_COUNT)string_data=ipakita_VALUE;else{long double factor=wallpaper_VALUE==16?2:10;while(item_COUNT-->0&&item_COUNT<200000)임시값=빼기?임시값/factor:임시값*factor;}}
    if(tapusin_OFFSET)*tapusin_OFFSET=(char*)(하나라도?string_data:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*string_data,char**보조항목){return (double)strtold(string_data,보조항목);}float strtof(const char*string_data,char**보조항목){return (float)strtold(string_data,보조항목);}
void qsort(void*wallpaper_VALUE,size_t item_COUNT,size_t sukat_82232621,int(*Ihambing)(const void*,const void*)){
    unsigned char*data_posisyon=wallpaper_VALUE;for(size_t 순번=1;순번<item_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Ihambing(data_posisyon+(안쪽순번-1)*sukat_82232621,data_posisyon+안쪽순번*sukat_82232621)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<sukat_82232621;셋째순번++){unsigned char character_code=data_posisyon[(안쪽순번-1)*sukat_82232621+셋째순번];data_posisyon[(안쪽순번-1)*sukat_82232621+셋째순번]=data_posisyon[안쪽순번*sukat_82232621+셋째순번];data_posisyon[안쪽순번*sukat_82232621+셋째순번]=character_code;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t posisyon;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *item_COUNT){*item_COUNT=출력크기;return 출력결과;}
int open(const char*pangalan,int kompigurasyon_Background_Intelligent_Transfer_Service,...){
    if(!strcmp(pangalan,"/@cc-output")){if(출력열림){error=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(pangalan,번역기자원들[순번].pangalan)){
        if(kompigurasyon_Background_Intelligent_Transfer_Service&3){error=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].posisyon=0;return 128+안쪽순번;}error=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)pangalan,kompigurasyon_Background_Intelligent_Transfer_Service,0,0,0,0);if(반환값<0){error=-반환값;return -1;}return 반환값;
}
int close(int file_hawakán){if(file_hawakán==100){출력열림=0;return 0;}if(file_hawakán>=128&&file_hawakán<152){열림[file_hawakán-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,file_hawakán,0,0,0,0,0);if(반환값<0){error=-반환값;return -1;}return 0;}
long read(int file_hawakán,void*data,size_t item_COUNT){
    if(file_hawakán>=128&&file_hawakán<152&&열림[file_hawakán-128].사용량){int 순번=file_hawakán-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->sukat_82232621-열림[순번].posisyon;if(item_COUNT>왼쪽)item_COUNT=왼쪽;memcpy(data,반환값->data+열림[순번].posisyon,item_COUNT);열림[순번].posisyon+=item_COUNT;return item_COUNT;}
    intptr_t 반환값=사용자호출(2,file_hawakán,(uintptr_t)data,item_COUNT,0,0,0);if(반환값<0){error=-반환값;return -1;}return 반환값;
}
long write(int file_hawakán,const void*data,size_t item_COUNT){
    if(file_hawakán==100){if(item_COUNT>sizeof(출력결과)-출력위치){error=28;return -1;}memcpy(출력결과+출력위치,data,item_COUNT);출력위치+=item_COUNT;if(출력크기<출력위치)출력크기=출력위치;return item_COUNT;}
    intptr_t 반환값=사용자호출(1,file_hawakán,(uintptr_t)data,item_COUNT,0,0,0);if(반환값<0){error=-반환값;return -1;}return 반환값;
}
long lseek(int file_hawakán,long OFFSET_VALUE,int 기준점){
    if(file_hawakán==100){long data_posisyon=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(data_posisyon<0||(size_t)data_posisyon>sizeof(출력결과)){error=22;return -1;}출력위치=data_posisyon;return data_posisyon;}
    if(file_hawakán>=128&&file_hawakán<152&&열림[file_hawakán-128].사용량){int 순번=file_hawakán-128;long data_posisyon=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].posisyon:번역기자원들[열림[순번].LOOKUP_INDEX].sukat_82232621);if(data_posisyon<0||(size_t)data_posisyon>번역기자원들[열림[순번].LOOKUP_INDEX].sukat_82232621){error=22;return -1;}열림[순번].posisyon=data_posisyon;return data_posisyon;}
    intptr_t 반환값=사용자호출(5,file_hawakán,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){error=-반환값;return -1;}return 반환값;
}
int unlink(const char*pangalan){intptr_t 반환값=사용자호출(11,(uintptr_t)pangalan,0,0,0,0,0);if(반환값<0){error=-반환값;return -1;}return 반환값;}
char *realpath(const char*pangalan,char*sukat_data){if(!sukat_data){sukat_data=malloc(strlen(pangalan)+1);if(!sukat_data)return 0;}return strcpy(sukat_data,pangalan);}
char *getcwd(char*data_posisyon,size_t item_COUNT){if(item_COUNT<2){error=34;return 0;}data_posisyon[0]='/';data_posisyon[1]=0;return data_posisyon;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_pagpasok){time_t 임시값=0;if(Terminal_pagpasok)*Terminal_pagpasok=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_pagpasok){(void)Terminal_pagpasok;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int file_hawakán,const char*pamamaraan_MODE){(void)pamamaraan_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].error=0;흐름목록[순번].file_hawakán=file_hawakán;return &흐름목록[순번];}error=24;return 0;}
int fflush(FILE*file_pagpasok){return file_pagpasok&&file_pagpasok->error?-1:0;}
int fclose(FILE*file_pagpasok){int 반환값=close(file_pagpasok->file_hawakán);if(file_pagpasok->error)반환값=-1;file_pagpasok->사용량=0;return 반환값;}
size_t fwrite(const void*data_posisyon,size_t string_data,size_t item_COUNT,FILE*file_pagpasok){if(!string_data)return 0;if(item_COUNT>SIZE_MAX/string_data){file_pagpasok->error=1;return 0;}long 반환값=write(file_pagpasok->file_hawakán,data_posisyon,string_data*item_COUNT);if(반환값<0){file_pagpasok->error=1;return 0;}return (size_t)반환값/string_data;}
int fputc(int character_code,FILE*file_pagpasok){unsigned char SECOND_VALUE=character_code;return fwrite(&SECOND_VALUE,1,1,file_pagpasok)==1?SECOND_VALUE:EOF;}
int fputs(const char*string_data,FILE*file_pagpasok){return fwrite(string_data,1,strlen(string_data),file_pagpasok)==strlen(string_data)?0:EOF;}
static void 넣기(char*sukat_data,size_t 용량한도,size_t*현재위치,char character_code){if(*현재위치+1<용량한도)sukat_data[*현재위치]=character_code;(*현재위치)++;}
int vsnprintf(char*sukat_data,size_t 용량한도,const char*format,va_list 가변인수){
    size_t 현재위치=0;while(*format){if(*format!='%'){넣기(sukat_data,용량한도,&현재위치,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,정밀도=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;정밀도=0;if(*format=='*'){정밀도=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')정밀도=정밀도*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TYPE_kategorya=*format?*format++:0,buffer_Storage[80];const char*string_data=buffer_Storage;size_t item_COUNT=0;
        if(TYPE_kategorya=='s'){string_data=va_arg(가변인수,const char*);if(!string_data)string_data="(null)";item_COUNT=strlen(string_data);if(정밀도>=0&&item_COUNT>(size_t)정밀도)item_COUNT=정밀도;}
        else if(TYPE_kategorya=='c'){buffer_Storage[0]=va_arg(가변인수,int);item_COUNT=1;}
        else if(TYPE_kategorya=='%'){buffer_Storage[0]='%';item_COUNT=1;}
        else if(TYPE_kategorya=='d'||TYPE_kategorya=='i'||TYPE_kategorya=='u'||TYPE_kategorya=='x'||TYPE_kategorya=='X'||TYPE_kategorya=='o'||TYPE_kategorya=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_kategorya=='d'||TYPE_kategorya=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_kategorya=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned wallpaper_VALUE=TYPE_kategorya=='x'||TYPE_kategorya=='X'||TYPE_kategorya=='p'?16:TYPE_kategorya=='o'?8:10;char digit_COUNT[64];unsigned 사용량=0;
            do{digit_COUNT[사용량++]="0123456789abcdef"[VALUE%wallpaper_VALUE];VALUE/=wallpaper_VALUE;}while(VALUE);
            if(음수표시)buffer_Storage[item_COUNT++]='-';if(TYPE_kategorya=='p'||(대체값&&wallpaper_VALUE==16)){buffer_Storage[item_COUNT++]='0';buffer_Storage[item_COUNT++]='x';}
            for(int fill_VALUE=(int)사용량;정밀도>fill_VALUE&&item_COUNT<sizeof(buffer_Storage)-사용량;fill_VALUE++)buffer_Storage[item_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(item_COUNT+사용량)&&item_COUNT<sizeof(buffer_Storage)-사용량)buffer_Storage[item_COUNT++]='0';
            while(사용량)buffer_Storage[item_COUNT++]=digit_COUNT[--사용량];
        }else{buffer_Storage[0]='?';item_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)item_COUNT){넣기(sukat_data,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<item_COUNT;순번++)넣기(sukat_data,용량한도,&현재위치,string_data[순번]);while(왼쪽&&너비>(int)item_COUNT){넣기(sukat_data,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)sukat_data[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*sukat_data,size_t 용량한도,const char*file_pagpasok,...){va_list 첫째값;va_start(첫째값,file_pagpasok);int 반환값=vsnprintf(sukat_data,용량한도,file_pagpasok,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*sukat_data,const char*file_pagpasok,...){va_list 첫째값;va_start(첫째값,file_pagpasok);int 반환값=vsnprintf(sukat_data,SIZE_MAX,file_pagpasok,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*file_pagpasok,va_list 첫째값){char SECOND_VALUE[2048];int item_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),file_pagpasok,첫째값);if(item_COUNT>2047)item_COUNT=2047;return fwrite(SECOND_VALUE,1,item_COUNT,Stream_VALUE)==(size_t)item_COUNT?item_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*file_pagpasok,...){va_list 첫째값;va_start(첫째값,file_pagpasok);int 반환값=vfprintf(Stream_VALUE,file_pagpasok,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*file_pagpasok,...){va_list 첫째값;va_start(첫째값,file_pagpasok);int 반환값=vfprintf(stdout,file_pagpasok,첫째값);va_end(첫째값);return 반환값;}
