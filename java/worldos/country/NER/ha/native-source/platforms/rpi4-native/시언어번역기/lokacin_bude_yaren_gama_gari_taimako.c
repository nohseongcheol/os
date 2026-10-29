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
static int Kuskure;
int *__errno_location(void){return &Kuskure;}
void exit(int Matsayi_Daraja){사용자호출(6,Matsayi_Daraja,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *Bincika_Aiyana_alƙaluma,const char *Fayil,unsigned Layi,const char *tsari_Mashigar_bayanai_Suna){fprintf(stderr,"cc assertion: %s %s:%u %s\n",Bincika_Aiyana_alƙaluma,Fayil,Layi,tsari_Mashigar_bayanai_Suna);exit(1);}
size_t strlen(const char*Zare_Tarin_bayani){const char*자료위치=Zare_Tarin_bayani;while(*자료위치)자료위치++;return 자료위치-Zare_Tarin_bayani;}
int strcmp(const char*첫째값,const char*둘째값){while(*첫째값&&*첫째값==*둘째값){첫째값++;둘째값++;}return (unsigned char)*첫째값-(unsigned char)*둘째값;}
int strncmp(const char*첫째값,const char*둘째값,size_t 개수){while(개수--){unsigned char gamayyar_x=*첫째값++,Maɓallin_Y_Mai_tsarawa=*둘째값++;if(gamayyar_x!=Maɓallin_Y_Mai_tsarawa)return gamayyar_x-Maɓallin_Y_Mai_tsarawa;if(!gamayyar_x)return 0;}return 0;}
char *strcpy(char*Zangon_ƙarshe_Tarin_bayani,const char*Zare_Tarin_bayani){char*반환값=Zangon_ƙarshe_Tarin_bayani;while((*Zangon_ƙarshe_Tarin_bayani++=*Zare_Tarin_bayani++)){}return 반환값;}
char *strchr(const char*Zare_Tarin_bayani,int Lambar_sirrin_harafi){do{if(*Zare_Tarin_bayani==(char)Lambar_sirrin_harafi)return (char*)Zare_Tarin_bayani;}while(*Zare_Tarin_bayani++);return 0;}
char *strrchr(const char*Zare_Tarin_bayani,int Lambar_sirrin_harafi){const char*반환값=0;do{if(*Zare_Tarin_bayani==(char)Lambar_sirrin_harafi)반환값=Zare_Tarin_bayani;}while(*Zare_Tarin_bayani++);return (char*)반환값;}
char *strstr(const char*Zare_Tarin_bayani,const char*터미널항목){size_t 개수=strlen(터미널항목);for(;*Zare_Tarin_bayani;Zare_Tarin_bayani++)if(!strncmp(Zare_Tarin_bayani,터미널항목,개수))return (char*)Zare_Tarin_bayani;return 개수?0:(char*)Zare_Tarin_bayani;}
int memcmp(const void*첫째값,const void*둘째값,size_t 개수){const unsigned char*gamayyar_x=첫째값,*Maɓallin_Y_Mai_tsarawa=둘째값;while(개수--){if(*gamayyar_x!=*Maɓallin_Y_Mai_tsarawa)return *gamayyar_x-*Maɓallin_Y_Mai_tsarawa;gamayyar_x++;Maɓallin_Y_Mai_tsarawa++;}return 0;}
void *memmove(void*Zangon_ƙarshe_Tarin_bayani,const void*Zare_Tarin_bayani,size_t 개수){unsigned char*gamayyar_x=Zangon_ƙarshe_Tarin_bayani;const unsigned char*Maɓallin_Y_Mai_tsarawa=Zare_Tarin_bayani;if(gamayyar_x<Maɓallin_Y_Mai_tsarawa){for(size_t 순번=0;순번<개수;순번++)gamayyar_x[순번]=Maɓallin_Y_Mai_tsarawa[순번];}else while(개수){개수--;gamayyar_x[개수]=Maɓallin_Y_Mai_tsarawa[개수];}return Zangon_ƙarshe_Tarin_bayani;}
static unsigned char rarrabawa_Fage[6*1024*1024] __attribute__((aligned(16)));
typedef struct Tarin_bayani_bulo {size_t Girma;struct Tarin_bayani_bulo*다음;int 남은공간;int 채울크기;uint64_t saitin_bai_daya_darasi;} Tarin_bayani_bulo;
static Tarin_bayani_bulo *첫항목;
void free(void*자료위치){if(!자료위치)return;Tarin_bayani_bulo*둘째값=(Tarin_bayani_bulo*)자료위치-1;둘째값->남은공간=1;for(Tarin_bayani_bulo*다음위치=첫항목;다음위치&&다음위치->다음;){if(다음위치->남은공간&&다음위치->다음->남은공간){다음위치->Girma+=sizeof(Tarin_bayani_bulo)+다음위치->다음->Girma;다음위치->다음=다음위치->다음->다음;}else 다음위치=다음위치->다음;}}
void *realloc(void*자료위치,size_t 개수){
    if(!개수){free(자료위치);return 0;}if(개수>sizeof(rarrabawa_Fage)-sizeof(Tarin_bayani_bulo))return 0;개수=(개수+15)&~(size_t)15;
    if(!첫항목){첫항목=(Tarin_bayani_bulo*)rarrabawa_Fage;첫항목->Girma=sizeof(rarrabawa_Fage)-sizeof(Tarin_bayani_bulo);첫항목->남은공간=1;첫항목->다음=0;}
    Tarin_bayani_bulo*이전=자료위치?(Tarin_bayani_bulo*)자료위치-1:0;if(이전&&이전->Girma>=개수)return 자료위치;
    for(Tarin_bayani_bulo*둘째값=첫항목;둘째값;둘째값=둘째값->다음)if(둘째값->남은공간&&둘째값->Girma>=개수){
        if(둘째값->Girma>=개수+sizeof(Tarin_bayani_bulo)+16){Tarin_bayani_bulo*나머지부분=(Tarin_bayani_bulo*)((unsigned char*)(둘째값+1)+개수);나머지부분->Girma=둘째값->Girma-개수-sizeof(Tarin_bayani_bulo);나머지부분->다음=둘째값->다음;나머지부분->남은공간=1;둘째값->다음=나머지부분;둘째값->Girma=개수;}
        둘째값->남은공간=0;void*반환값=둘째값+1;if(이전){memcpy(반환값,자료위치,이전->Girma);free(자료위치);}return 반환값;
    }Kuskure=12;return 0;
}
void *malloc(size_t 개수){return realloc(0,개수);}
void *calloc(size_t 개수,size_t Zare_Tarin_bayani){if(Zare_Tarin_bayani&&개수>SIZE_MAX/Zare_Tarin_bayani)return 0;void*자료위치=malloc(개수*Zare_Tarin_bayani);if(자료위치)memset(자료위치,0,개수*Zare_Tarin_bayani);return 자료위치;}
unsigned long long strtoull(const char*Zare_Tarin_bayani,char**Ƙarshe_Sassautawa,int Bi_bango_Daraja){
    const char*Fara_Sassautawa=Zare_Tarin_bayani;while(*Zare_Tarin_bayani==' '||(*Zare_Tarin_bayani>=9&&*Zare_Tarin_bayani<=13))Zare_Tarin_bayani++;int 음수여부=0;if(*Zare_Tarin_bayani=='-'||*Zare_Tarin_bayani=='+')음수여부=*Zare_Tarin_bayani++=='-';
    if((!Bi_bango_Daraja||Bi_bango_Daraja==16)&&Zare_Tarin_bayani[0]=='0'&&(Zare_Tarin_bayani[1]=='x'||Zare_Tarin_bayani[1]=='X')){Bi_bango_Daraja=16;Zare_Tarin_bayani+=2;}if(!Bi_bango_Daraja)Bi_bango_Daraja=*Zare_Tarin_bayani=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned Lambar_sirrin_harafi=*Zare_Tarin_bayani,Zangon_ƙarshe_Tarin_bayani=Lambar_sirrin_harafi>='0'&&Lambar_sirrin_harafi<='9'?Lambar_sirrin_harafi-'0':Lambar_sirrin_harafi>='a'&&Lambar_sirrin_harafi<='z'?Lambar_sirrin_harafi-'a'+10:Lambar_sirrin_harafi>='A'&&Lambar_sirrin_harafi<='Z'?Lambar_sirrin_harafi-'A'+10:99;if(Zangon_ƙarshe_Tarin_bayani>=(unsigned)Bi_bango_Daraja)break;하나라도=1;Zare_Tarin_bayani++;if(임시값>(~0ull-Zangon_ƙarshe_Tarin_bayani)/(unsigned)Bi_bango_Daraja){임시값=~0ull;Kuskure=34;}else 임시값=임시값*Bi_bango_Daraja+Zangon_ƙarshe_Tarin_bayani;}
    if(Ƙarshe_Sassautawa)*Ƙarshe_Sassautawa=(char*)(하나라도?Zare_Tarin_bayani:Fara_Sassautawa);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*Zare_Tarin_bayani,char**보조항목,int 둘째값){return strtoull(Zare_Tarin_bayani,보조항목,둘째값);}
long strtol(const char*Zare_Tarin_bayani,char**보조항목,int 둘째값){return (long)strtoull(Zare_Tarin_bayani,보조항목,둘째값);}
int atoi(const char*Zare_Tarin_bayani){return (int)strtol(Zare_Tarin_bayani,0,10);}
long double ldexpl(long double gamayyar_x,int 개수){while(개수>0){gamayyar_x*=2;개수--;}while(개수<0){gamayyar_x/=2;개수++;}return gamayyar_x;}
long double strtold(const char*Zare_Tarin_bayani,char**Ƙarshe_Sassautawa){
    const char*Fara_Sassautawa=Zare_Tarin_bayani;while(*Zare_Tarin_bayani==' '||(*Zare_Tarin_bayani>=9&&*Zare_Tarin_bayani<=13))Zare_Tarin_bayani++;int 음수여부=0;if(*Zare_Tarin_bayani=='-'||*Zare_Tarin_bayani=='+')음수여부=*Zare_Tarin_bayani++=='-';
    int Bi_bango_Daraja=10;if(Zare_Tarin_bayani[0]=='0'&&(Zare_Tarin_bayani[1]=='x'||Zare_Tarin_bayani[1]=='X')){Bi_bango_Daraja=16;Zare_Tarin_bayani+=2;}long double 임시값=0,Sikeli=1;int 소수부=0,하나라도=0;
    for(;;){int Lambar_sirrin_harafi=*Zare_Tarin_bayani,Zangon_ƙarshe_Tarin_bayani=Lambar_sirrin_harafi>='0'&&Lambar_sirrin_harafi<='9'?Lambar_sirrin_harafi-'0':Lambar_sirrin_harafi>='a'&&Lambar_sirrin_harafi<='f'?Lambar_sirrin_harafi-'a'+10:Lambar_sirrin_harafi>='A'&&Lambar_sirrin_harafi<='F'?Lambar_sirrin_harafi-'A'+10:99;
        if(Lambar_sirrin_harafi=='.'&&!소수부){소수부=1;Zare_Tarin_bayani++;continue;}if(Zangon_ƙarshe_Tarin_bayani>=Bi_bango_Daraja)break;하나라도=1;Zare_Tarin_bayani++;임시값=임시값*Bi_bango_Daraja+Zangon_ƙarshe_Tarin_bayani;if(소수부)Sikeli*=Bi_bango_Daraja;
    }임시값/=Sikeli;
    if((Bi_bango_Daraja==10&&(*Zare_Tarin_bayani=='e'||*Zare_Tarin_bayani=='E'))||(Bi_bango_Daraja==16&&(*Zare_Tarin_bayani=='p'||*Zare_Tarin_bayani=='P'))){const char*Nuna_Daraja=Zare_Tarin_bayani++;int 빼기=0;if(*Zare_Tarin_bayani=='-'||*Zare_Tarin_bayani=='+')빼기=*Zare_Tarin_bayani++=='-';int 개수=0,항목수=0;while(*Zare_Tarin_bayani>='0'&&*Zare_Tarin_bayani<='9'){항목수++;if(개수<20000)개수=개수*10+*Zare_Tarin_bayani-'0';Zare_Tarin_bayani++;}if(!항목수)Zare_Tarin_bayani=Nuna_Daraja;else{long double 배율=Bi_bango_Daraja==16?2:10;while(개수-->0&&개수<200000)임시값=빼기?임시값/배율:임시값*배율;}}
    if(Ƙarshe_Sassautawa)*Ƙarshe_Sassautawa=(char*)(하나라도?Zare_Tarin_bayani:Fara_Sassautawa);return 음수여부?-임시값:임시값;
}
double strtod(const char*Zare_Tarin_bayani,char**보조항목){return (double)strtold(Zare_Tarin_bayani,보조항목);}float strtof(const char*Zare_Tarin_bayani,char**보조항목){return (float)strtold(Zare_Tarin_bayani,보조항목);}
void qsort(void*Bi_bango_Daraja,size_t 개수,size_t Girma,int(*Kwatanta)(const void*,const void*)){
    unsigned char*자료위치=Bi_bango_Daraja;for(size_t 순번=1;순번<개수;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Kwatanta(자료위치+(안쪽순번-1)*Girma,자료위치+안쪽순번*Girma)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Girma;셋째순번++){unsigned char Lambar_sirrin_harafi=자료위치[(안쪽순번-1)*Girma+셋째순번];자료위치[(안쪽순번-1)*Girma+셋째순번]=자료위치[안쪽순번*Girma+셋째순번];자료위치[안쪽순번*Girma+셋째순번]=Lambar_sirrin_harafi;}
}
static struct {int 사용량,색인;size_t 위치;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *개수){*개수=출력크기;return 출력결과;}
int open(const char*Suna,int saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango,...){
    if(!strcmp(Suna,"/@cc-output")){if(출력열림){Kuskure=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Suna,번역기자원들[순번].Suna)){
        if(saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&3){Kuskure=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].색인=순번;열림[안쪽순번].위치=0;return 128+안쪽순번;}Kuskure=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Suna,saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango,0,0,0,0);if(반환값<0){Kuskure=-반환값;return -1;}return 반환값;
}
int close(int Fayil_Mariki){if(Fayil_Mariki==100){출력열림=0;return 0;}if(Fayil_Mariki>=128&&Fayil_Mariki<152){열림[Fayil_Mariki-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Fayil_Mariki,0,0,0,0,0);if(반환값<0){Kuskure=-반환값;return -1;}return 0;}
long read(int Fayil_Mariki,void*Tarin_bayani,size_t 개수){
    if(Fayil_Mariki>=128&&Fayil_Mariki<152&&열림[Fayil_Mariki-128].사용량){int 순번=Fayil_Mariki-128;const 번역기자원*반환값=&번역기자원들[열림[순번].색인];size_t 왼쪽=반환값->Girma-열림[순번].위치;if(개수>왼쪽)개수=왼쪽;memcpy(Tarin_bayani,반환값->Tarin_bayani+열림[순번].위치,개수);열림[순번].위치+=개수;return 개수;}
    intptr_t 반환값=사용자호출(2,Fayil_Mariki,(uintptr_t)Tarin_bayani,개수,0,0,0);if(반환값<0){Kuskure=-반환값;return -1;}return 반환값;
}
long write(int Fayil_Mariki,const void*Tarin_bayani,size_t 개수){
    if(Fayil_Mariki==100){if(개수>sizeof(출력결과)-출력위치){Kuskure=28;return -1;}memcpy(출력결과+출력위치,Tarin_bayani,개수);출력위치+=개수;if(출력크기<출력위치)출력크기=출력위치;return 개수;}
    intptr_t 반환값=사용자호출(1,Fayil_Mariki,(uintptr_t)Tarin_bayani,개수,0,0,0);if(반환값<0){Kuskure=-반환값;return -1;}return 반환값;
}
long lseek(int Fayil_Mariki,long Sassautawa_Daraja,int 기준점){
    if(Fayil_Mariki==100){long 자료위치=Sassautawa_Daraja+(기준점==0?0:기준점==1?출력위치:출력크기);if(자료위치<0||(size_t)자료위치>sizeof(출력결과)){Kuskure=22;return -1;}출력위치=자료위치;return 자료위치;}
    if(Fayil_Mariki>=128&&Fayil_Mariki<152&&열림[Fayil_Mariki-128].사용량){int 순번=Fayil_Mariki-128;long 자료위치=Sassautawa_Daraja+(기준점==0?0:기준점==1?열림[순번].위치:번역기자원들[열림[순번].색인].Girma);if(자료위치<0||(size_t)자료위치>번역기자원들[열림[순번].색인].Girma){Kuskure=22;return -1;}열림[순번].위치=자료위치;return 자료위치;}
    intptr_t 반환값=사용자호출(5,Fayil_Mariki,Sassautawa_Daraja,기준점,0,0,0);if(반환값<0){Kuskure=-반환값;return -1;}return 반환값;
}
int unlink(const char*Suna){intptr_t 반환값=사용자호출(11,(uintptr_t)Suna,0,0,0,0,0);if(반환값<0){Kuskure=-반환값;return -1;}return 반환값;}
char *realpath(const char*Suna,char*결과자료){if(!결과자료){결과자료=malloc(strlen(Suna)+1);if(!결과자료)return 0;}return strcpy(결과자료,Suna);}
char *getcwd(char*자료위치,size_t 개수){if(개수<2){Kuskure=34;return 0;}자료위치[0]='/';자료위치[1]=0;return 자료위치;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*터미널항목){time_t 임시값=0;if(터미널항목)*터미널항목=임시값;return 임시값;}
struct tm *localtime(const time_t*터미널항목){(void)터미널항목;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int Fayil_Mariki,const char*tsari_yanayin_aiki){(void)tsari_yanayin_aiki;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Kuskure=0;흐름목록[순번].Fayil_Mariki=Fayil_Mariki;return &흐름목록[순번];}Kuskure=24;return 0;}
int fflush(FILE*Fayil_Mashigar_bayanai){return Fayil_Mashigar_bayanai&&Fayil_Mashigar_bayanai->Kuskure?-1:0;}
int fclose(FILE*Fayil_Mashigar_bayanai){int 반환값=close(Fayil_Mashigar_bayanai->Fayil_Mariki);if(Fayil_Mashigar_bayanai->Kuskure)반환값=-1;Fayil_Mashigar_bayanai->사용량=0;return 반환값;}
size_t fwrite(const void*자료위치,size_t Zare_Tarin_bayani,size_t 개수,FILE*Fayil_Mashigar_bayanai){if(!Zare_Tarin_bayani)return 0;if(개수>SIZE_MAX/Zare_Tarin_bayani){Fayil_Mashigar_bayanai->Kuskure=1;return 0;}long 반환값=write(Fayil_Mashigar_bayanai->Fayil_Mariki,자료위치,Zare_Tarin_bayani*개수);if(반환값<0){Fayil_Mashigar_bayanai->Kuskure=1;return 0;}return (size_t)반환값/Zare_Tarin_bayani;}
int fputc(int Lambar_sirrin_harafi,FILE*Fayil_Mashigar_bayanai){unsigned char 둘째값=Lambar_sirrin_harafi;return fwrite(&둘째값,1,1,Fayil_Mashigar_bayanai)==1?둘째값:EOF;}
int fputs(const char*Zare_Tarin_bayani,FILE*Fayil_Mashigar_bayanai){return fwrite(Zare_Tarin_bayani,1,strlen(Zare_Tarin_bayani),Fayil_Mashigar_bayanai)==strlen(Zare_Tarin_bayani)?0:EOF;}
static void 넣기(char*결과자료,size_t 용량한도,size_t*현재위치,char Lambar_sirrin_harafi){if(*현재위치+1<용량한도)결과자료[*현재위치]=Lambar_sirrin_harafi;(*현재위치)++;}
int vsnprintf(char*결과자료,size_t 용량한도,const char*zubi,va_list 가변인수){
    size_t 현재위치=0;while(*zubi){if(*zubi!='%'){넣기(결과자료,용량한도,&현재위치,*zubi++);continue;}zubi++;
        int 왼쪽=0,영값=0,대체값=0;while(*zubi=='-'||*zubi=='0'||*zubi=='#'||*zubi=='+'||*zubi==' '){if(*zubi=='-')왼쪽=1;if(*zubi=='0')영값=1;if(*zubi=='#')대체값=1;zubi++;}
        int 너비=0,정밀도=-1;if(*zubi=='*'){너비=va_arg(가변인수,int);zubi++;}else while(*zubi>='0'&&*zubi<='9')너비=너비*10+*zubi++-'0';
        if(*zubi=='.'){zubi++;정밀도=0;if(*zubi=='*'){정밀도=va_arg(가변인수,int);zubi++;}else while(*zubi>='0'&&*zubi<='9')정밀도=정밀도*10+*zubi++-'0';}
        int 넓은글자=0;while(*zubi=='l'||*zubi=='z'||*zubi=='t'||*zubi=='j'||*zubi=='h'){if(*zubi!='h')넓은글자=1;zubi++;}
        char rubuta_ɓangare=*zubi?*zubi++:0,Tunani_na_wucin_gadi_Wurin_adana[80];const char*Zare_Tarin_bayani=Tunani_na_wucin_gadi_Wurin_adana;size_t 개수=0;
        if(rubuta_ɓangare=='s'){Zare_Tarin_bayani=va_arg(가변인수,const char*);if(!Zare_Tarin_bayani)Zare_Tarin_bayani="(null)";개수=strlen(Zare_Tarin_bayani);if(정밀도>=0&&개수>(size_t)정밀도)개수=정밀도;}
        else if(rubuta_ɓangare=='c'){Tunani_na_wucin_gadi_Wurin_adana[0]=va_arg(가변인수,int);개수=1;}
        else if(rubuta_ɓangare=='%'){Tunani_na_wucin_gadi_Wurin_adana[0]='%';개수=1;}
        else if(rubuta_ɓangare=='d'||rubuta_ɓangare=='i'||rubuta_ɓangare=='u'||rubuta_ɓangare=='x'||rubuta_ɓangare=='X'||rubuta_ɓangare=='o'||rubuta_ɓangare=='p'){
            unsigned long long Daraja;int 음수표시=0;
            if(rubuta_ɓangare=='d'||rubuta_ɓangare=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;Daraja=음수표시?0-(unsigned long long)임시값:임시값;}
            else Daraja=rubuta_ɓangare=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Bi_bango_Daraja=rubuta_ɓangare=='x'||rubuta_ɓangare=='X'||rubuta_ɓangare=='p'?16:rubuta_ɓangare=='o'?8:10;char 숫자수[64];unsigned 사용량=0;
            do{숫자수[사용량++]="0123456789abcdef"[Daraja%Bi_bango_Daraja];Daraja/=Bi_bango_Daraja;}while(Daraja);
            if(음수표시)Tunani_na_wucin_gadi_Wurin_adana[개수++]='-';if(rubuta_ɓangare=='p'||(대체값&&Bi_bango_Daraja==16)){Tunani_na_wucin_gadi_Wurin_adana[개수++]='0';Tunani_na_wucin_gadi_Wurin_adana[개수++]='x';}
            for(int ciko_Daraja=(int)사용량;정밀도>ciko_Daraja&&개수<sizeof(Tunani_na_wucin_gadi_Wurin_adana)-사용량;ciko_Daraja++)Tunani_na_wucin_gadi_Wurin_adana[개수++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(개수+사용량)&&개수<sizeof(Tunani_na_wucin_gadi_Wurin_adana)-사용량)Tunani_na_wucin_gadi_Wurin_adana[개수++]='0';
            while(사용량)Tunani_na_wucin_gadi_Wurin_adana[개수++]=숫자수[--사용량];
        }else{Tunani_na_wucin_gadi_Wurin_adana[0]='?';개수=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<개수;순번++)넣기(결과자료,용량한도,&현재위치,Zare_Tarin_bayani[순번]);while(왼쪽&&너비>(int)개수){넣기(결과자료,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)결과자료[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*결과자료,size_t 용량한도,const char*Fayil_Mashigar_bayanai,...){va_list 첫째값;va_start(첫째값,Fayil_Mashigar_bayanai);int 반환값=vsnprintf(결과자료,용량한도,Fayil_Mashigar_bayanai,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*결과자료,const char*Fayil_Mashigar_bayanai,...){va_list 첫째값;va_start(첫째값,Fayil_Mashigar_bayanai);int 반환값=vsnprintf(결과자료,SIZE_MAX,Fayil_Mashigar_bayanai,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*watsuwa_Daraja,const char*Fayil_Mashigar_bayanai,va_list 첫째값){char 둘째값[2048];int 개수=vsnprintf(둘째값,sizeof(둘째값),Fayil_Mashigar_bayanai,첫째값);if(개수>2047)개수=2047;return fwrite(둘째값,1,개수,watsuwa_Daraja)==(size_t)개수?개수:-1;}
int fprintf(FILE*watsuwa_Daraja,const char*Fayil_Mashigar_bayanai,...){va_list 첫째값;va_start(첫째값,Fayil_Mashigar_bayanai);int 반환값=vfprintf(watsuwa_Daraja,Fayil_Mashigar_bayanai,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Fayil_Mashigar_bayanai,...){va_list 첫째값;va_start(첫째값,Fayil_Mashigar_bayanai);int 반환값=vfprintf(stdout,Fayil_Mashigar_bayanai,첫째값);va_end(첫째값);return 반환값;}
