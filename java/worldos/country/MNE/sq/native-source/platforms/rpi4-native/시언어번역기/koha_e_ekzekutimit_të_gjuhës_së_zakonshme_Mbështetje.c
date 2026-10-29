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
static int GABIM;
int *__errno_location(void){return &GABIM;}
void exit(int status_VALUE){사용자호출(6,status_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *çek_shprehje,const char *Kartelë,unsigned linjë,const char *metoda_futje_emër){fprintf(stderr,"cc assertion: %s %s:%u %s\n",çek_shprehje,Kartelë,linjë,metoda_futje_emër);exit(1);}
size_t strlen(const char*varg_të_dhëna){const char*të_dhëna_pozicioni=varg_të_dhëna;while(*të_dhëna_pozicioni)të_dhëna_pozicioni++;return të_dhëna_pozicioni-varg_të_dhëna;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t njësi_COUNT){while(njësi_COUNT--){unsigned char koordinata_x=*첫째값++,Y_koordinatë=*SECOND_VALUE++;if(koordinata_x!=Y_koordinatë)return koordinata_x-Y_koordinatë;if(!koordinata_x)return 0;}return 0;}
char *strcpy(char*vendmbërritje_të_dhëna,const char*varg_të_dhëna){char*반환값=vendmbërritje_të_dhëna;while((*vendmbërritje_të_dhëna++=*varg_të_dhëna++)){}return 반환값;}
char *strchr(const char*varg_të_dhëna,int kodi_i_karakterit){do{if(*varg_të_dhëna==(char)kodi_i_karakterit)return (char*)varg_të_dhëna;}while(*varg_të_dhëna++);return 0;}
char *strrchr(const char*varg_të_dhëna,int kodi_i_karakterit){const char*반환값=0;do{if(*varg_të_dhëna==(char)kodi_i_karakterit)반환값=varg_të_dhëna;}while(*varg_të_dhëna++);return (char*)반환값;}
char *strstr(const char*varg_të_dhëna,const char*Terminali_futje){size_t njësi_COUNT=strlen(Terminali_futje);for(;*varg_të_dhëna;varg_të_dhëna++)if(!strncmp(varg_të_dhëna,Terminali_futje,njësi_COUNT))return (char*)varg_të_dhëna;return njësi_COUNT?0:(char*)varg_të_dhëna;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t njësi_COUNT){const unsigned char*koordinata_x=첫째값,*Y_koordinatë=SECOND_VALUE;while(njësi_COUNT--){if(*koordinata_x!=*Y_koordinatë)return *koordinata_x-*Y_koordinatë;koordinata_x++;Y_koordinatë++;}return 0;}
void *memmove(void*vendmbërritje_të_dhëna,const void*varg_të_dhëna,size_t njësi_COUNT){unsigned char*koordinata_x=vendmbërritje_të_dhëna;const unsigned char*Y_koordinatë=varg_të_dhëna;if(koordinata_x<Y_koordinatë){for(size_t 순번=0;순번<njësi_COUNT;순번++)koordinata_x[순번]=Y_koordinatë[순번];}else while(njësi_COUNT){njësi_COUNT--;koordinata_x[njësi_COUNT]=Y_koordinatë[njësi_COUNT];}return vendmbërritje_të_dhëna;}
static unsigned char rezervim_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct të_dhëna_bllokoj {size_t Madhësi;struct të_dhëna_bllokoj*Tjetër_njësi;int 남은공간;int 채울크기;uint64_t drejtvendosje_mësim;} të_dhëna_bllokoj;
static të_dhëna_bllokoj *첫항목;
void free(void*të_dhëna_pozicioni){if(!të_dhëna_pozicioni)return;të_dhëna_bllokoj*SECOND_VALUE=(të_dhëna_bllokoj*)të_dhëna_pozicioni-1;SECOND_VALUE->남은공간=1;for(të_dhëna_bllokoj*Tjetër_OFFSET=첫항목;Tjetër_OFFSET&&Tjetër_OFFSET->Tjetër_njësi;){if(Tjetër_OFFSET->남은공간&&Tjetër_OFFSET->Tjetër_njësi->남은공간){Tjetër_OFFSET->Madhësi+=sizeof(të_dhëna_bllokoj)+Tjetër_OFFSET->Tjetër_njësi->Madhësi;Tjetër_OFFSET->Tjetër_njësi=Tjetër_OFFSET->Tjetër_njësi->Tjetër_njësi;}else Tjetër_OFFSET=Tjetër_OFFSET->Tjetër_njësi;}}
void *realloc(void*të_dhëna_pozicioni,size_t njësi_COUNT){
    if(!njësi_COUNT){free(të_dhëna_pozicioni);return 0;}if(njësi_COUNT>sizeof(rezervim_Arena)-sizeof(të_dhëna_bllokoj))return 0;njësi_COUNT=(njësi_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(të_dhëna_bllokoj*)rezervim_Arena;첫항목->Madhësi=sizeof(rezervim_Arena)-sizeof(të_dhëna_bllokoj);첫항목->남은공간=1;첫항목->Tjetër_njësi=0;}
    të_dhëna_bllokoj*이전=të_dhëna_pozicioni?(të_dhëna_bllokoj*)të_dhëna_pozicioni-1:0;if(이전&&이전->Madhësi>=njësi_COUNT)return të_dhëna_pozicioni;
    for(të_dhëna_bllokoj*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Tjetër_njësi)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Madhësi>=njësi_COUNT){
        if(SECOND_VALUE->Madhësi>=njësi_COUNT+sizeof(të_dhëna_bllokoj)+16){të_dhëna_bllokoj*나머지부분=(të_dhëna_bllokoj*)((unsigned char*)(SECOND_VALUE+1)+njësi_COUNT);나머지부분->Madhësi=SECOND_VALUE->Madhësi-njësi_COUNT-sizeof(të_dhëna_bllokoj);나머지부분->Tjetër_njësi=SECOND_VALUE->Tjetër_njësi;나머지부분->남은공간=1;SECOND_VALUE->Tjetër_njësi=나머지부분;SECOND_VALUE->Madhësi=njësi_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,të_dhëna_pozicioni,이전->Madhësi);free(të_dhëna_pozicioni);}return 반환값;
    }GABIM=12;return 0;
}
void *malloc(size_t njësi_COUNT){return realloc(0,njësi_COUNT);}
void *calloc(size_t njësi_COUNT,size_t varg_të_dhëna){if(varg_të_dhëna&&njësi_COUNT>SIZE_MAX/varg_të_dhëna)return 0;void*të_dhëna_pozicioni=malloc(njësi_COUNT*varg_të_dhëna);if(të_dhëna_pozicioni)memset(të_dhëna_pozicioni,0,njësi_COUNT*varg_të_dhëna);return të_dhëna_pozicioni;}
unsigned long long strtoull(const char*varg_të_dhëna,char**mbaroj_OFFSET,int Sfond_VALUE){
    const char*nis_OFFSET=varg_të_dhëna;while(*varg_të_dhëna==' '||(*varg_të_dhëna>=9&&*varg_të_dhëna<=13))varg_të_dhëna++;int 음수여부=0;if(*varg_të_dhëna=='-'||*varg_të_dhëna=='+')음수여부=*varg_të_dhëna++=='-';
    if((!Sfond_VALUE||Sfond_VALUE==16)&&varg_të_dhëna[0]=='0'&&(varg_të_dhëna[1]=='x'||varg_të_dhëna[1]=='X')){Sfond_VALUE=16;varg_të_dhëna+=2;}if(!Sfond_VALUE)Sfond_VALUE=*varg_të_dhëna=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kodi_i_karakterit=*varg_të_dhëna,vendmbërritje_të_dhëna=kodi_i_karakterit>='0'&&kodi_i_karakterit<='9'?kodi_i_karakterit-'0':kodi_i_karakterit>='a'&&kodi_i_karakterit<='z'?kodi_i_karakterit-'a'+10:kodi_i_karakterit>='A'&&kodi_i_karakterit<='Z'?kodi_i_karakterit-'A'+10:99;if(vendmbërritje_të_dhëna>=(unsigned)Sfond_VALUE)break;하나라도=1;varg_të_dhëna++;if(임시값>(~0ull-vendmbërritje_të_dhëna)/(unsigned)Sfond_VALUE){임시값=~0ull;GABIM=34;}else 임시값=임시값*Sfond_VALUE+vendmbërritje_të_dhëna;}
    if(mbaroj_OFFSET)*mbaroj_OFFSET=(char*)(하나라도?varg_të_dhëna:nis_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*varg_të_dhëna,char**보조항목,int SECOND_VALUE){return strtoull(varg_të_dhëna,보조항목,SECOND_VALUE);}
long strtol(const char*varg_të_dhëna,char**보조항목,int SECOND_VALUE){return (long)strtoull(varg_të_dhëna,보조항목,SECOND_VALUE);}
int atoi(const char*varg_të_dhëna){return (int)strtol(varg_të_dhëna,0,10);}
long double ldexpl(long double koordinata_x,int njësi_COUNT){while(njësi_COUNT>0){koordinata_x*=2;njësi_COUNT--;}while(njësi_COUNT<0){koordinata_x/=2;njësi_COUNT++;}return koordinata_x;}
long double strtold(const char*varg_të_dhëna,char**mbaroj_OFFSET){
    const char*nis_OFFSET=varg_të_dhëna;while(*varg_të_dhëna==' '||(*varg_të_dhëna>=9&&*varg_të_dhëna<=13))varg_të_dhëna++;int 음수여부=0;if(*varg_të_dhëna=='-'||*varg_të_dhëna=='+')음수여부=*varg_të_dhëna++=='-';
    int Sfond_VALUE=10;if(varg_të_dhëna[0]=='0'&&(varg_të_dhëna[1]=='x'||varg_të_dhëna[1]=='X')){Sfond_VALUE=16;varg_të_dhëna+=2;}long double 임시값=0,shkallë=1;int 소수부=0,하나라도=0;
    for(;;){int kodi_i_karakterit=*varg_të_dhëna,vendmbërritje_të_dhëna=kodi_i_karakterit>='0'&&kodi_i_karakterit<='9'?kodi_i_karakterit-'0':kodi_i_karakterit>='a'&&kodi_i_karakterit<='f'?kodi_i_karakterit-'a'+10:kodi_i_karakterit>='A'&&kodi_i_karakterit<='F'?kodi_i_karakterit-'A'+10:99;
        if(kodi_i_karakterit=='.'&&!소수부){소수부=1;varg_të_dhëna++;continue;}if(vendmbërritje_të_dhëna>=Sfond_VALUE)break;하나라도=1;varg_të_dhëna++;임시값=임시값*Sfond_VALUE+vendmbërritje_të_dhëna;if(소수부)shkallë*=Sfond_VALUE;
    }임시값/=shkallë;
    if((Sfond_VALUE==10&&(*varg_të_dhëna=='e'||*varg_të_dhëna=='E'))||(Sfond_VALUE==16&&(*varg_të_dhëna=='p'||*varg_të_dhëna=='P'))){const char*shfaq_VALUE=varg_të_dhëna++;int 빼기=0;if(*varg_të_dhëna=='-'||*varg_të_dhëna=='+')빼기=*varg_të_dhëna++=='-';int njësi_COUNT=0,futje_COUNT=0;while(*varg_të_dhëna>='0'&&*varg_të_dhëna<='9'){futje_COUNT++;if(njësi_COUNT<20000)njësi_COUNT=njësi_COUNT*10+*varg_të_dhëna-'0';varg_të_dhëna++;}if(!futje_COUNT)varg_të_dhëna=shfaq_VALUE;else{long double faktor=Sfond_VALUE==16?2:10;while(njësi_COUNT-->0&&njësi_COUNT<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(mbaroj_OFFSET)*mbaroj_OFFSET=(char*)(하나라도?varg_të_dhëna:nis_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*varg_të_dhëna,char**보조항목){return (double)strtold(varg_të_dhëna,보조항목);}float strtof(const char*varg_të_dhëna,char**보조항목){return (float)strtold(varg_të_dhëna,보조항목);}
void qsort(void*Sfond_VALUE,size_t njësi_COUNT,size_t Madhësi,int(*Krahaso)(const void*,const void*)){
    unsigned char*të_dhëna_pozicioni=Sfond_VALUE;for(size_t 순번=1;순번<njësi_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Krahaso(të_dhëna_pozicioni+(안쪽순번-1)*Madhësi,të_dhëna_pozicioni+안쪽순번*Madhësi)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Madhësi;셋째순번++){unsigned char kodi_i_karakterit=të_dhëna_pozicioni[(안쪽순번-1)*Madhësi+셋째순번];të_dhëna_pozicioni[(안쪽순번-1)*Madhësi+셋째순번]=të_dhëna_pozicioni[안쪽순번*Madhësi+셋째순번];të_dhëna_pozicioni[안쪽순번*Madhësi+셋째순번]=kodi_i_karakterit;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Pozicioni;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *njësi_COUNT){*njësi_COUNT=출력크기;return 출력결과;}
int open(const char*Emër,int konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond,...){
    if(!strcmp(Emër,"/@cc-output")){if(출력열림){GABIM=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Emër,번역기자원들[순번].Emër)){
        if(konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&3){GABIM=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Pozicioni=0;return 128+안쪽순번;}GABIM=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Emër,konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond,0,0,0,0);if(반환값<0){GABIM=-반환값;return -1;}return 반환값;
}
int close(int skedar_dorezë){if(skedar_dorezë==100){출력열림=0;return 0;}if(skedar_dorezë>=128&&skedar_dorezë<152){열림[skedar_dorezë-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,skedar_dorezë,0,0,0,0,0);if(반환값<0){GABIM=-반환값;return -1;}return 0;}
long read(int skedar_dorezë,void*të_dhëna,size_t njësi_COUNT){
    if(skedar_dorezë>=128&&skedar_dorezë<152&&열림[skedar_dorezë-128].사용량){int 순번=skedar_dorezë-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Madhësi-열림[순번].Pozicioni;if(njësi_COUNT>왼쪽)njësi_COUNT=왼쪽;memcpy(të_dhëna,반환값->të_dhëna+열림[순번].Pozicioni,njësi_COUNT);열림[순번].Pozicioni+=njësi_COUNT;return njësi_COUNT;}
    intptr_t 반환값=사용자호출(2,skedar_dorezë,(uintptr_t)të_dhëna,njësi_COUNT,0,0,0);if(반환값<0){GABIM=-반환값;return -1;}return 반환값;
}
long write(int skedar_dorezë,const void*të_dhëna,size_t njësi_COUNT){
    if(skedar_dorezë==100){if(njësi_COUNT>sizeof(출력결과)-출력위치){GABIM=28;return -1;}memcpy(출력결과+출력위치,të_dhëna,njësi_COUNT);출력위치+=njësi_COUNT;if(출력크기<출력위치)출력크기=출력위치;return njësi_COUNT;}
    intptr_t 반환값=사용자호출(1,skedar_dorezë,(uintptr_t)të_dhëna,njësi_COUNT,0,0,0);if(반환값<0){GABIM=-반환값;return -1;}return 반환값;
}
long lseek(int skedar_dorezë,long OFFSET_VALUE,int 기준점){
    if(skedar_dorezë==100){long të_dhëna_pozicioni=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(të_dhëna_pozicioni<0||(size_t)të_dhëna_pozicioni>sizeof(출력결과)){GABIM=22;return -1;}출력위치=të_dhëna_pozicioni;return të_dhëna_pozicioni;}
    if(skedar_dorezë>=128&&skedar_dorezë<152&&열림[skedar_dorezë-128].사용량){int 순번=skedar_dorezë-128;long të_dhëna_pozicioni=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].Pozicioni:번역기자원들[열림[순번].LOOKUP_INDEX].Madhësi);if(të_dhëna_pozicioni<0||(size_t)të_dhëna_pozicioni>번역기자원들[열림[순번].LOOKUP_INDEX].Madhësi){GABIM=22;return -1;}열림[순번].Pozicioni=të_dhëna_pozicioni;return të_dhëna_pozicioni;}
    intptr_t 반환값=사용자호출(5,skedar_dorezë,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){GABIM=-반환값;return -1;}return 반환값;
}
int unlink(const char*Emër){intptr_t 반환값=사용자호출(11,(uintptr_t)Emër,0,0,0,0,0);if(반환값<0){GABIM=-반환값;return -1;}return 반환값;}
char *realpath(const char*Emër,char*llogaritje_të_dhëna){if(!llogaritje_të_dhëna){llogaritje_të_dhëna=malloc(strlen(Emër)+1);if(!llogaritje_të_dhëna)return 0;}return strcpy(llogaritje_të_dhëna,Emër);}
char *getcwd(char*të_dhëna_pozicioni,size_t njësi_COUNT){if(njësi_COUNT<2){GABIM=34;return 0;}të_dhëna_pozicioni[0]='/';të_dhëna_pozicioni[1]=0;return të_dhëna_pozicioni;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminali_futje){time_t 임시값=0;if(Terminali_futje)*Terminali_futje=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminali_futje){(void)Terminali_futje;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int skedar_dorezë,const char*metoda_MODE){(void)metoda_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].GABIM=0;흐름목록[순번].skedar_dorezë=skedar_dorezë;return &흐름목록[순번];}GABIM=24;return 0;}
int fflush(FILE*skedar_futje){return skedar_futje&&skedar_futje->GABIM?-1:0;}
int fclose(FILE*skedar_futje){int 반환값=close(skedar_futje->skedar_dorezë);if(skedar_futje->GABIM)반환값=-1;skedar_futje->사용량=0;return 반환값;}
size_t fwrite(const void*të_dhëna_pozicioni,size_t varg_të_dhëna,size_t njësi_COUNT,FILE*skedar_futje){if(!varg_të_dhëna)return 0;if(njësi_COUNT>SIZE_MAX/varg_të_dhëna){skedar_futje->GABIM=1;return 0;}long 반환값=write(skedar_futje->skedar_dorezë,të_dhëna_pozicioni,varg_të_dhëna*njësi_COUNT);if(반환값<0){skedar_futje->GABIM=1;return 0;}return (size_t)반환값/varg_të_dhëna;}
int fputc(int kodi_i_karakterit,FILE*skedar_futje){unsigned char SECOND_VALUE=kodi_i_karakterit;return fwrite(&SECOND_VALUE,1,1,skedar_futje)==1?SECOND_VALUE:EOF;}
int fputs(const char*varg_të_dhëna,FILE*skedar_futje){return fwrite(varg_të_dhëna,1,strlen(varg_të_dhëna),skedar_futje)==strlen(varg_të_dhëna)?0:EOF;}
static void 넣기(char*llogaritje_të_dhëna,size_t 용량한도,size_t*현재위치,char kodi_i_karakterit){if(*현재위치+1<용량한도)llogaritje_të_dhëna[*현재위치]=kodi_i_karakterit;(*현재위치)++;}
int vsnprintf(char*llogaritje_të_dhëna,size_t 용량한도,const char*format,va_list 가변인수){
    size_t 현재위치=0;while(*format){if(*format!='%'){넣기(llogaritje_të_dhëna,용량한도,&현재위치,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,정밀도=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;정밀도=0;if(*format=='*'){정밀도=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')정밀도=정밀도*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TYPE_kategori=*format?*format++:0,ndërmemorie_hapësira_ruajtëse[80];const char*varg_të_dhëna=ndërmemorie_hapësira_ruajtëse;size_t njësi_COUNT=0;
        if(TYPE_kategori=='s'){varg_të_dhëna=va_arg(가변인수,const char*);if(!varg_të_dhëna)varg_të_dhëna="(null)";njësi_COUNT=strlen(varg_të_dhëna);if(정밀도>=0&&njësi_COUNT>(size_t)정밀도)njësi_COUNT=정밀도;}
        else if(TYPE_kategori=='c'){ndërmemorie_hapësira_ruajtëse[0]=va_arg(가변인수,int);njësi_COUNT=1;}
        else if(TYPE_kategori=='%'){ndërmemorie_hapësira_ruajtëse[0]='%';njësi_COUNT=1;}
        else if(TYPE_kategori=='d'||TYPE_kategori=='i'||TYPE_kategori=='u'||TYPE_kategori=='x'||TYPE_kategori=='X'||TYPE_kategori=='o'||TYPE_kategori=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_kategori=='d'||TYPE_kategori=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_kategori=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Sfond_VALUE=TYPE_kategori=='x'||TYPE_kategori=='X'||TYPE_kategori=='p'?16:TYPE_kategori=='o'?8:10;char shifër_COUNT[64];unsigned 사용량=0;
            do{shifër_COUNT[사용량++]="0123456789abcdef"[VALUE%Sfond_VALUE];VALUE/=Sfond_VALUE;}while(VALUE);
            if(음수표시)ndërmemorie_hapësira_ruajtëse[njësi_COUNT++]='-';if(TYPE_kategori=='p'||(대체값&&Sfond_VALUE==16)){ndërmemorie_hapësira_ruajtëse[njësi_COUNT++]='0';ndërmemorie_hapësira_ruajtëse[njësi_COUNT++]='x';}
            for(int mbushje_VALUE=(int)사용량;정밀도>mbushje_VALUE&&njësi_COUNT<sizeof(ndërmemorie_hapësira_ruajtëse)-사용량;mbushje_VALUE++)ndërmemorie_hapësira_ruajtëse[njësi_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(njësi_COUNT+사용량)&&njësi_COUNT<sizeof(ndërmemorie_hapësira_ruajtëse)-사용량)ndërmemorie_hapësira_ruajtëse[njësi_COUNT++]='0';
            while(사용량)ndërmemorie_hapësira_ruajtëse[njësi_COUNT++]=shifër_COUNT[--사용량];
        }else{ndërmemorie_hapësira_ruajtëse[0]='?';njësi_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)njësi_COUNT){넣기(llogaritje_të_dhëna,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<njësi_COUNT;순번++)넣기(llogaritje_të_dhëna,용량한도,&현재위치,varg_të_dhëna[순번]);while(왼쪽&&너비>(int)njësi_COUNT){넣기(llogaritje_të_dhëna,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)llogaritje_të_dhëna[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*llogaritje_të_dhëna,size_t 용량한도,const char*skedar_futje,...){va_list 첫째값;va_start(첫째값,skedar_futje);int 반환값=vsnprintf(llogaritje_të_dhëna,용량한도,skedar_futje,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*llogaritje_të_dhëna,const char*skedar_futje,...){va_list 첫째값;va_start(첫째값,skedar_futje);int 반환값=vsnprintf(llogaritje_të_dhëna,SIZE_MAX,skedar_futje,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*skedar_futje,va_list 첫째값){char SECOND_VALUE[2048];int njësi_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),skedar_futje,첫째값);if(njësi_COUNT>2047)njësi_COUNT=2047;return fwrite(SECOND_VALUE,1,njësi_COUNT,Stream_VALUE)==(size_t)njësi_COUNT?njësi_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*skedar_futje,...){va_list 첫째값;va_start(첫째값,skedar_futje);int 반환값=vfprintf(Stream_VALUE,skedar_futje,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*skedar_futje,...){va_list 첫째값;va_start(첫째값,skedar_futje);int 반환값=vfprintf(stdout,skedar_futje,첫째값);va_end(첫째값);return 반환값;}
