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
static int FEIL;
int *__errno_location(void){return &FEIL;}
void exit(int status_VALUE){사용자호출(6,status_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *sjekk_uttrykk,const char *Fil,unsigned linje,const char *metode_oppføring_namn){fprintf(stderr,"cc assertion: %s %s:%u %s\n",sjekk_uttrykk,Fil,linje,metode_oppføring_namn);exit(1);}
size_t strlen(const char*streng_data){const char*data_plassere=streng_data;while(*data_plassere)data_plassere++;return data_plassere-streng_data;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t vare_COUNT){while(vare_COUNT--){unsigned char x_koordinat=*첫째값++,Y_koordinat=*SECOND_VALUE++;if(x_koordinat!=Y_koordinat)return x_koordinat-Y_koordinat;if(!x_koordinat)return 0;}return 0;}
char *strcpy(char*mål_data,const char*streng_data){char*반환값=mål_data;while((*mål_data++=*streng_data++)){}return 반환값;}
char *strchr(const char*streng_data,int teiknkode){do{if(*streng_data==(char)teiknkode)return (char*)streng_data;}while(*streng_data++);return 0;}
char *strrchr(const char*streng_data,int teiknkode){const char*반환값=0;do{if(*streng_data==(char)teiknkode)반환값=streng_data;}while(*streng_data++);return (char*)반환값;}
char *strstr(const char*streng_data,const char*Terminal_oppføring){size_t vare_COUNT=strlen(Terminal_oppføring);for(;*streng_data;streng_data++)if(!strncmp(streng_data,Terminal_oppføring,vare_COUNT))return (char*)streng_data;return vare_COUNT?0:(char*)streng_data;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t vare_COUNT){const unsigned char*x_koordinat=첫째값,*Y_koordinat=SECOND_VALUE;while(vare_COUNT--){if(*x_koordinat!=*Y_koordinat)return *x_koordinat-*Y_koordinat;x_koordinat++;Y_koordinat++;}return 0;}
void *memmove(void*mål_data,const void*streng_data,size_t vare_COUNT){unsigned char*x_koordinat=mål_data;const unsigned char*Y_koordinat=streng_data;if(x_koordinat<Y_koordinat){for(size_t 순번=0;순번<vare_COUNT;순번++)x_koordinat[순번]=Y_koordinat[순번];}else while(vare_COUNT){vare_COUNT--;x_koordinat[vare_COUNT]=Y_koordinat[vare_COUNT];}return mål_data;}
static unsigned char tildeling_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct data_Blokker {size_t Storleik;struct data_Blokker*Neste_vare;int 남은공간;int 채울크기;uint64_t justering_leksjon;} data_Blokker;
static data_Blokker *첫항목;
void free(void*data_plassere){if(!data_plassere)return;data_Blokker*SECOND_VALUE=(data_Blokker*)data_plassere-1;SECOND_VALUE->남은공간=1;for(data_Blokker*Neste_OFFSET=첫항목;Neste_OFFSET&&Neste_OFFSET->Neste_vare;){if(Neste_OFFSET->남은공간&&Neste_OFFSET->Neste_vare->남은공간){Neste_OFFSET->Storleik+=sizeof(data_Blokker)+Neste_OFFSET->Neste_vare->Storleik;Neste_OFFSET->Neste_vare=Neste_OFFSET->Neste_vare->Neste_vare;}else Neste_OFFSET=Neste_OFFSET->Neste_vare;}}
void *realloc(void*data_plassere,size_t vare_COUNT){
    if(!vare_COUNT){free(data_plassere);return 0;}if(vare_COUNT>sizeof(tildeling_Arena)-sizeof(data_Blokker))return 0;vare_COUNT=(vare_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(data_Blokker*)tildeling_Arena;첫항목->Storleik=sizeof(tildeling_Arena)-sizeof(data_Blokker);첫항목->남은공간=1;첫항목->Neste_vare=0;}
    data_Blokker*이전=data_plassere?(data_Blokker*)data_plassere-1:0;if(이전&&이전->Storleik>=vare_COUNT)return data_plassere;
    for(data_Blokker*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Neste_vare)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Storleik>=vare_COUNT){
        if(SECOND_VALUE->Storleik>=vare_COUNT+sizeof(data_Blokker)+16){data_Blokker*나머지부분=(data_Blokker*)((unsigned char*)(SECOND_VALUE+1)+vare_COUNT);나머지부분->Storleik=SECOND_VALUE->Storleik-vare_COUNT-sizeof(data_Blokker);나머지부분->Neste_vare=SECOND_VALUE->Neste_vare;나머지부분->남은공간=1;SECOND_VALUE->Neste_vare=나머지부분;SECOND_VALUE->Storleik=vare_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,data_plassere,이전->Storleik);free(data_plassere);}return 반환값;
    }FEIL=12;return 0;
}
void *malloc(size_t vare_COUNT){return realloc(0,vare_COUNT);}
void *calloc(size_t vare_COUNT,size_t streng_data){if(streng_data&&vare_COUNT>SIZE_MAX/streng_data)return 0;void*data_plassere=malloc(vare_COUNT*streng_data);if(data_plassere)memset(data_plassere,0,vare_COUNT*streng_data);return data_plassere;}
unsigned long long strtoull(const char*streng_data,char**avslutte_OFFSET,int bakgrunn_VALUE){
    const char*START_OFFSET=streng_data;while(*streng_data==' '||(*streng_data>=9&&*streng_data<=13))streng_data++;int 음수여부=0;if(*streng_data=='-'||*streng_data=='+')음수여부=*streng_data++=='-';
    if((!bakgrunn_VALUE||bakgrunn_VALUE==16)&&streng_data[0]=='0'&&(streng_data[1]=='x'||streng_data[1]=='X')){bakgrunn_VALUE=16;streng_data+=2;}if(!bakgrunn_VALUE)bakgrunn_VALUE=*streng_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned teiknkode=*streng_data,mål_data=teiknkode>='0'&&teiknkode<='9'?teiknkode-'0':teiknkode>='a'&&teiknkode<='z'?teiknkode-'a'+10:teiknkode>='A'&&teiknkode<='Z'?teiknkode-'A'+10:99;if(mål_data>=(unsigned)bakgrunn_VALUE)break;하나라도=1;streng_data++;if(임시값>(~0ull-mål_data)/(unsigned)bakgrunn_VALUE){임시값=~0ull;FEIL=34;}else 임시값=임시값*bakgrunn_VALUE+mål_data;}
    if(avslutte_OFFSET)*avslutte_OFFSET=(char*)(하나라도?streng_data:START_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*streng_data,char**보조항목,int SECOND_VALUE){return strtoull(streng_data,보조항목,SECOND_VALUE);}
long strtol(const char*streng_data,char**보조항목,int SECOND_VALUE){return (long)strtoull(streng_data,보조항목,SECOND_VALUE);}
int atoi(const char*streng_data){return (int)strtol(streng_data,0,10);}
long double ldexpl(long double x_koordinat,int vare_COUNT){while(vare_COUNT>0){x_koordinat*=2;vare_COUNT--;}while(vare_COUNT<0){x_koordinat/=2;vare_COUNT++;}return x_koordinat;}
long double strtold(const char*streng_data,char**avslutte_OFFSET){
    const char*START_OFFSET=streng_data;while(*streng_data==' '||(*streng_data>=9&&*streng_data<=13))streng_data++;int 음수여부=0;if(*streng_data=='-'||*streng_data=='+')음수여부=*streng_data++=='-';
    int bakgrunn_VALUE=10;if(streng_data[0]=='0'&&(streng_data[1]=='x'||streng_data[1]=='X')){bakgrunn_VALUE=16;streng_data+=2;}long double 임시값=0,skalere=1;int 소수부=0,하나라도=0;
    for(;;){int teiknkode=*streng_data,mål_data=teiknkode>='0'&&teiknkode<='9'?teiknkode-'0':teiknkode>='a'&&teiknkode<='f'?teiknkode-'a'+10:teiknkode>='A'&&teiknkode<='F'?teiknkode-'A'+10:99;
        if(teiknkode=='.'&&!소수부){소수부=1;streng_data++;continue;}if(mål_data>=bakgrunn_VALUE)break;하나라도=1;streng_data++;임시값=임시값*bakgrunn_VALUE+mål_data;if(소수부)skalere*=bakgrunn_VALUE;
    }임시값/=skalere;
    if((bakgrunn_VALUE==10&&(*streng_data=='e'||*streng_data=='E'))||(bakgrunn_VALUE==16&&(*streng_data=='p'||*streng_data=='P'))){const char*vise_VALUE_487749b8=streng_data++;int 빼기=0;if(*streng_data=='-'||*streng_data=='+')빼기=*streng_data++=='-';int vare_COUNT=0,oppføring_COUNT=0;while(*streng_data>='0'&&*streng_data<='9'){oppføring_COUNT++;if(vare_COUNT<20000)vare_COUNT=vare_COUNT*10+*streng_data-'0';streng_data++;}if(!oppføring_COUNT)streng_data=vise_VALUE_487749b8;else{long double faktor=bakgrunn_VALUE==16?2:10;while(vare_COUNT-->0&&vare_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(avslutte_OFFSET)*avslutte_OFFSET=(char*)(하나라도?streng_data:START_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*streng_data,char**보조항목){return (double)strtold(streng_data,보조항목);}float strtof(const char*streng_data,char**보조항목){return (float)strtold(streng_data,보조항목);}
void qsort(void*bakgrunn_VALUE,size_t vare_COUNT,size_t Storleik,int(*Samanlikn)(const void*,const void*)){
    unsigned char*data_plassere=bakgrunn_VALUE;for(size_t 순번=1;순번<vare_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Samanlikn(data_plassere+(안쪽순번-1)*Storleik,data_plassere+안쪽순번*Storleik)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Storleik;셋째순번++){unsigned char teiknkode=data_plassere[(안쪽순번-1)*Storleik+셋째순번];data_plassere[(안쪽순번-1)*Storleik+셋째순번]=data_plassere[안쪽순번*Storleik+셋째순번];data_plassere[안쪽순번*Storleik+셋째순번]=teiknkode;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Posisjon;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *vare_COUNT){*vare_COUNT=출력크기;return 출력결과;}
int open(const char*Namn,int 설정비트,...){
    if(!strcmp(Namn,"/@cc-output")){if(출력열림){FEIL=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Namn,번역기자원들[순번].Namn)){
        if(설정비트&3){FEIL=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Posisjon=0;return 128+안쪽순번;}FEIL=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Namn,설정비트,0,0,0,0);if(반환값<0){FEIL=-반환값;return -1;}return 반환값;
}
int close(int fil_handtak){if(fil_handtak==100){출력열림=0;return 0;}if(fil_handtak>=128&&fil_handtak<152){열림[fil_handtak-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fil_handtak,0,0,0,0,0);if(반환값<0){FEIL=-반환값;return -1;}return 0;}
long read(int fil_handtak,void*data,size_t vare_COUNT){
    if(fil_handtak>=128&&fil_handtak<152&&열림[fil_handtak-128].사용량){int 순번=fil_handtak-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Storleik-열림[순번].Posisjon;if(vare_COUNT>왼쪽)vare_COUNT=왼쪽;memcpy(data,반환값->data+열림[순번].Posisjon,vare_COUNT);열림[순번].Posisjon+=vare_COUNT;return vare_COUNT;}
    intptr_t 반환값=사용자호출(2,fil_handtak,(uintptr_t)data,vare_COUNT,0,0,0);if(반환값<0){FEIL=-반환값;return -1;}return 반환값;
}
long write(int fil_handtak,const void*data,size_t vare_COUNT){
    if(fil_handtak==100){if(vare_COUNT>sizeof(출력결과)-출력위치){FEIL=28;return -1;}memcpy(출력결과+출력위치,data,vare_COUNT);출력위치+=vare_COUNT;if(출력크기<출력위치)출력크기=출력위치;return vare_COUNT;}
    intptr_t 반환값=사용자호출(1,fil_handtak,(uintptr_t)data,vare_COUNT,0,0,0);if(반환값<0){FEIL=-반환값;return -1;}return 반환값;
}
long lseek(int fil_handtak,long OFFSET_VALUE,int søk_nullpunkt){
    if(fil_handtak==100){long data_plassere=OFFSET_VALUE+(søk_nullpunkt==0?0:søk_nullpunkt==1?출력위치:출력크기);if(data_plassere<0||(size_t)data_plassere>sizeof(출력결과)){FEIL=22;return -1;}출력위치=data_plassere;return data_plassere;}
    if(fil_handtak>=128&&fil_handtak<152&&열림[fil_handtak-128].사용량){int 순번=fil_handtak-128;long data_plassere=OFFSET_VALUE+(søk_nullpunkt==0?0:søk_nullpunkt==1?열림[순번].Posisjon:번역기자원들[열림[순번].LOOKUP_INDEX].Storleik);if(data_plassere<0||(size_t)data_plassere>번역기자원들[열림[순번].LOOKUP_INDEX].Storleik){FEIL=22;return -1;}열림[순번].Posisjon=data_plassere;return data_plassere;}
    intptr_t 반환값=사용자호출(5,fil_handtak,OFFSET_VALUE,søk_nullpunkt,0,0,0);if(반환값<0){FEIL=-반환값;return -1;}return 반환값;
}
int unlink(const char*Namn){intptr_t 반환값=사용자호출(11,(uintptr_t)Namn,0,0,0,0,0);if(반환값<0){FEIL=-반환값;return -1;}return 반환값;}
char *realpath(const char*Namn,char*forretningsmål_data){if(!forretningsmål_data){forretningsmål_data=malloc(strlen(Namn)+1);if(!forretningsmål_data)return 0;}return strcpy(forretningsmål_data,Namn);}
char *getcwd(char*data_plassere,size_t vare_COUNT){if(vare_COUNT<2){FEIL=34;return 0;}data_plassere[0]='/';data_plassere[1]=0;return data_plassere;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_oppføring){time_t 임시값=0;if(Terminal_oppføring)*Terminal_oppføring=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_oppføring){(void)Terminal_oppføring;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int fil_handtak,const char*metode_MODE){(void)metode_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].FEIL=0;흐름목록[순번].fil_handtak=fil_handtak;return &흐름목록[순번];}FEIL=24;return 0;}
int fflush(FILE*fil_oppføring){return fil_oppføring&&fil_oppføring->FEIL?-1:0;}
int fclose(FILE*fil_oppføring){int 반환값=close(fil_oppføring->fil_handtak);if(fil_oppføring->FEIL)반환값=-1;fil_oppføring->사용량=0;return 반환값;}
size_t fwrite(const void*data_plassere,size_t streng_data,size_t vare_COUNT,FILE*fil_oppføring){if(!streng_data)return 0;if(vare_COUNT>SIZE_MAX/streng_data){fil_oppføring->FEIL=1;return 0;}long 반환값=write(fil_oppføring->fil_handtak,data_plassere,streng_data*vare_COUNT);if(반환값<0){fil_oppføring->FEIL=1;return 0;}return (size_t)반환값/streng_data;}
int fputc(int teiknkode,FILE*fil_oppføring){unsigned char SECOND_VALUE=teiknkode;return fwrite(&SECOND_VALUE,1,1,fil_oppføring)==1?SECOND_VALUE:EOF;}
int fputs(const char*streng_data,FILE*fil_oppføring){return fwrite(streng_data,1,strlen(streng_data),fil_oppføring)==strlen(streng_data)?0:EOF;}
static void 넣기(char*forretningsmål_data,size_t 용량한도,size_t*betalt_plassere,char teiknkode){if(*betalt_plassere+1<용량한도)forretningsmål_data[*betalt_plassere]=teiknkode;(*betalt_plassere)++;}
int vsnprintf(char*forretningsmål_data,size_t 용량한도,const char*format,va_list 가변인수){
    size_t betalt_plassere=0;while(*format){if(*format!='%'){넣기(forretningsmål_data,용량한도,&betalt_plassere,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,정밀도=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;정밀도=0;if(*format=='*'){정밀도=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')정밀도=정밀도*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TYPE_kategori=*format?*format++:0,buffer_Lagring[80];const char*streng_data=buffer_Lagring;size_t vare_COUNT=0;
        if(TYPE_kategori=='s'){streng_data=va_arg(가변인수,const char*);if(!streng_data)streng_data="(null)";vare_COUNT=strlen(streng_data);if(정밀도>=0&&vare_COUNT>(size_t)정밀도)vare_COUNT=정밀도;}
        else if(TYPE_kategori=='c'){buffer_Lagring[0]=va_arg(가변인수,int);vare_COUNT=1;}
        else if(TYPE_kategori=='%'){buffer_Lagring[0]='%';vare_COUNT=1;}
        else if(TYPE_kategori=='d'||TYPE_kategori=='i'||TYPE_kategori=='u'||TYPE_kategori=='x'||TYPE_kategori=='X'||TYPE_kategori=='o'||TYPE_kategori=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_kategori=='d'||TYPE_kategori=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_kategori=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned bakgrunn_VALUE=TYPE_kategori=='x'||TYPE_kategori=='X'||TYPE_kategori=='p'?16:TYPE_kategori=='o'?8:10;char siffer_COUNT[64];unsigned 사용량=0;
            do{siffer_COUNT[사용량++]="0123456789abcdef"[VALUE%bakgrunn_VALUE];VALUE/=bakgrunn_VALUE;}while(VALUE);
            if(음수표시)buffer_Lagring[vare_COUNT++]='-';if(TYPE_kategori=='p'||(대체값&&bakgrunn_VALUE==16)){buffer_Lagring[vare_COUNT++]='0';buffer_Lagring[vare_COUNT++]='x';}
            for(int fylle_VALUE=(int)사용량;정밀도>fylle_VALUE&&vare_COUNT<sizeof(buffer_Lagring)-사용량;fylle_VALUE++)buffer_Lagring[vare_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(vare_COUNT+사용량)&&vare_COUNT<sizeof(buffer_Lagring)-사용량)buffer_Lagring[vare_COUNT++]='0';
            while(사용량)buffer_Lagring[vare_COUNT++]=siffer_COUNT[--사용량];
        }else{buffer_Lagring[0]='?';vare_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)vare_COUNT){넣기(forretningsmål_data,용량한도,&betalt_plassere,' ');너비--;}
        for(size_t 순번=0;순번<vare_COUNT;순번++)넣기(forretningsmål_data,용량한도,&betalt_plassere,streng_data[순번]);while(왼쪽&&너비>(int)vare_COUNT){넣기(forretningsmål_data,용량한도,&betalt_plassere,' ');너비--;}
    }if(용량한도)forretningsmål_data[betalt_plassere<용량한도?betalt_plassere:용량한도-1]=0;return betalt_plassere;
}
int snprintf(char*forretningsmål_data,size_t 용량한도,const char*fil_oppføring,...){va_list 첫째값;va_start(첫째값,fil_oppføring);int 반환값=vsnprintf(forretningsmål_data,용량한도,fil_oppføring,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*forretningsmål_data,const char*fil_oppføring,...){va_list 첫째값;va_start(첫째값,fil_oppføring);int 반환값=vsnprintf(forretningsmål_data,SIZE_MAX,fil_oppføring,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*fil_oppføring,va_list 첫째값){char SECOND_VALUE[2048];int vare_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),fil_oppføring,첫째값);if(vare_COUNT>2047)vare_COUNT=2047;return fwrite(SECOND_VALUE,1,vare_COUNT,Stream_VALUE)==(size_t)vare_COUNT?vare_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*fil_oppføring,...){va_list 첫째값;va_start(첫째값,fil_oppføring);int 반환값=vfprintf(Stream_VALUE,fil_oppføring,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fil_oppføring,...){va_list 첫째값;va_start(첫째값,fil_oppføring);int 반환값=vfprintf(stdout,fil_oppføring,첫째값);va_end(첫째값);return 반환값;}
