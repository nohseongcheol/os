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
static int Feeler;
int *__errno_location(void){return &Feeler;}
void exit(int Status_VALUE){사용자호출(6,Status_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *Scheck_Ausdrock,const char *Fichier,unsigned Zeil,const char *Method_Agab_Numm){fprintf(stderr,"cc assertion: %s %s:%u %s\n",Scheck_Ausdrock,Fichier,Zeil,Method_Agab_Numm);exit(1);}
size_t strlen(const char*Zeechefolleg_Daten){const char*Daten_positionéieren=Zeechefolleg_Daten;while(*Daten_positionéieren)Daten_positionéieren++;return Daten_positionéieren-Zeechefolleg_Daten;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t Element_COUNT){while(Element_COUNT--){unsigned char X_Koordinat=*첫째값++,세로좌표=*SECOND_VALUE++;if(X_Koordinat!=세로좌표)return X_Koordinat-세로좌표;if(!X_Koordinat)return 0;}return 0;}
char *strcpy(char*Zil_Daten,const char*Zeechefolleg_Daten){char*반환값=Zil_Daten;while((*Zil_Daten++=*Zeechefolleg_Daten++)){}return 반환값;}
char *strchr(const char*Zeechefolleg_Daten,int Zeechecode){do{if(*Zeechefolleg_Daten==(char)Zeechecode)return (char*)Zeechefolleg_Daten;}while(*Zeechefolleg_Daten++);return 0;}
char *strrchr(const char*Zeechefolleg_Daten,int Zeechecode){const char*반환값=0;do{if(*Zeechefolleg_Daten==(char)Zeechecode)반환값=Zeechefolleg_Daten;}while(*Zeechefolleg_Daten++);return (char*)반환값;}
char *strstr(const char*Zeechefolleg_Daten,const char*Terminal_Agab){size_t Element_COUNT=strlen(Terminal_Agab);for(;*Zeechefolleg_Daten;Zeechefolleg_Daten++)if(!strncmp(Zeechefolleg_Daten,Terminal_Agab,Element_COUNT))return (char*)Zeechefolleg_Daten;return Element_COUNT?0:(char*)Zeechefolleg_Daten;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t Element_COUNT){const unsigned char*X_Koordinat=첫째값,*세로좌표=SECOND_VALUE;while(Element_COUNT--){if(*X_Koordinat!=*세로좌표)return *X_Koordinat-*세로좌표;X_Koordinat++;세로좌표++;}return 0;}
void *memmove(void*Zil_Daten,const void*Zeechefolleg_Daten,size_t Element_COUNT){unsigned char*X_Koordinat=Zil_Daten;const unsigned char*세로좌표=Zeechefolleg_Daten;if(X_Koordinat<세로좌표){for(size_t 순번=0;순번<Element_COUNT;순번++)X_Koordinat[순번]=세로좌표[순번];}else while(Element_COUNT){Element_COUNT--;X_Koordinat[Element_COUNT]=세로좌표[Element_COUNT];}return Zil_Daten;}
static unsigned char 할당마당[6*1024*1024] __attribute__((aligned(16)));
typedef struct Daten_blockéieren {size_t d_Gréisst_veränneren;struct Daten_blockéieren*Weider_Element;int 남은공간;int 채울크기;uint64_t Ausriichtung_Lektioun;} Daten_blockéieren;
static Daten_blockéieren *첫항목;
void free(void*Daten_positionéieren){if(!Daten_positionéieren)return;Daten_blockéieren*SECOND_VALUE=(Daten_blockéieren*)Daten_positionéieren-1;SECOND_VALUE->남은공간=1;for(Daten_blockéieren*Weider_OFFSET=첫항목;Weider_OFFSET&&Weider_OFFSET->Weider_Element;){if(Weider_OFFSET->남은공간&&Weider_OFFSET->Weider_Element->남은공간){Weider_OFFSET->d_Gréisst_veränneren+=sizeof(Daten_blockéieren)+Weider_OFFSET->Weider_Element->d_Gréisst_veränneren;Weider_OFFSET->Weider_Element=Weider_OFFSET->Weider_Element->Weider_Element;}else Weider_OFFSET=Weider_OFFSET->Weider_Element;}}
void *realloc(void*Daten_positionéieren,size_t Element_COUNT){
    if(!Element_COUNT){free(Daten_positionéieren);return 0;}if(Element_COUNT>sizeof(할당마당)-sizeof(Daten_blockéieren))return 0;Element_COUNT=(Element_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(Daten_blockéieren*)할당마당;첫항목->d_Gréisst_veränneren=sizeof(할당마당)-sizeof(Daten_blockéieren);첫항목->남은공간=1;첫항목->Weider_Element=0;}
    Daten_blockéieren*이전=Daten_positionéieren?(Daten_blockéieren*)Daten_positionéieren-1:0;if(이전&&이전->d_Gréisst_veränneren>=Element_COUNT)return Daten_positionéieren;
    for(Daten_blockéieren*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Weider_Element)if(SECOND_VALUE->남은공간&&SECOND_VALUE->d_Gréisst_veränneren>=Element_COUNT){
        if(SECOND_VALUE->d_Gréisst_veränneren>=Element_COUNT+sizeof(Daten_blockéieren)+16){Daten_blockéieren*나머지부분=(Daten_blockéieren*)((unsigned char*)(SECOND_VALUE+1)+Element_COUNT);나머지부분->d_Gréisst_veränneren=SECOND_VALUE->d_Gréisst_veränneren-Element_COUNT-sizeof(Daten_blockéieren);나머지부분->Weider_Element=SECOND_VALUE->Weider_Element;나머지부분->남은공간=1;SECOND_VALUE->Weider_Element=나머지부분;SECOND_VALUE->d_Gréisst_veränneren=Element_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,Daten_positionéieren,이전->d_Gréisst_veränneren);free(Daten_positionéieren);}return 반환값;
    }Feeler=12;return 0;
}
void *malloc(size_t Element_COUNT){return realloc(0,Element_COUNT);}
void *calloc(size_t Element_COUNT,size_t Zeechefolleg_Daten){if(Zeechefolleg_Daten&&Element_COUNT>SIZE_MAX/Zeechefolleg_Daten)return 0;void*Daten_positionéieren=malloc(Element_COUNT*Zeechefolleg_Daten);if(Daten_positionéieren)memset(Daten_positionéieren,0,Element_COUNT*Zeechefolleg_Daten);return Daten_positionéieren;}
unsigned long long strtoull(const char*Zeechefolleg_Daten,char**bëennegen_OFFSET,int Hannergrond_VALUE){
    const char*Start_OFFSET=Zeechefolleg_Daten;while(*Zeechefolleg_Daten==' '||(*Zeechefolleg_Daten>=9&&*Zeechefolleg_Daten<=13))Zeechefolleg_Daten++;int 음수여부=0;if(*Zeechefolleg_Daten=='-'||*Zeechefolleg_Daten=='+')음수여부=*Zeechefolleg_Daten++=='-';
    if((!Hannergrond_VALUE||Hannergrond_VALUE==16)&&Zeechefolleg_Daten[0]=='0'&&(Zeechefolleg_Daten[1]=='x'||Zeechefolleg_Daten[1]=='X')){Hannergrond_VALUE=16;Zeechefolleg_Daten+=2;}if(!Hannergrond_VALUE)Hannergrond_VALUE=*Zeechefolleg_Daten=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned Zeechecode=*Zeechefolleg_Daten,Zil_Daten=Zeechecode>='0'&&Zeechecode<='9'?Zeechecode-'0':Zeechecode>='a'&&Zeechecode<='z'?Zeechecode-'a'+10:Zeechecode>='A'&&Zeechecode<='Z'?Zeechecode-'A'+10:99;if(Zil_Daten>=(unsigned)Hannergrond_VALUE)break;하나라도=1;Zeechefolleg_Daten++;if(임시값>(~0ull-Zil_Daten)/(unsigned)Hannergrond_VALUE){임시값=~0ull;Feeler=34;}else 임시값=임시값*Hannergrond_VALUE+Zil_Daten;}
    if(bëennegen_OFFSET)*bëennegen_OFFSET=(char*)(하나라도?Zeechefolleg_Daten:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*Zeechefolleg_Daten,char**보조항목,int SECOND_VALUE){return strtoull(Zeechefolleg_Daten,보조항목,SECOND_VALUE);}
long strtol(const char*Zeechefolleg_Daten,char**보조항목,int SECOND_VALUE){return (long)strtoull(Zeechefolleg_Daten,보조항목,SECOND_VALUE);}
int atoi(const char*Zeechefolleg_Daten){return (int)strtol(Zeechefolleg_Daten,0,10);}
long double ldexpl(long double X_Koordinat,int Element_COUNT){while(Element_COUNT>0){X_Koordinat*=2;Element_COUNT--;}while(Element_COUNT<0){X_Koordinat/=2;Element_COUNT++;}return X_Koordinat;}
long double strtold(const char*Zeechefolleg_Daten,char**bëennegen_OFFSET){
    const char*Start_OFFSET=Zeechefolleg_Daten;while(*Zeechefolleg_Daten==' '||(*Zeechefolleg_Daten>=9&&*Zeechefolleg_Daten<=13))Zeechefolleg_Daten++;int 음수여부=0;if(*Zeechefolleg_Daten=='-'||*Zeechefolleg_Daten=='+')음수여부=*Zeechefolleg_Daten++=='-';
    int Hannergrond_VALUE=10;if(Zeechefolleg_Daten[0]=='0'&&(Zeechefolleg_Daten[1]=='x'||Zeechefolleg_Daten[1]=='X')){Hannergrond_VALUE=16;Zeechefolleg_Daten+=2;}long double 임시값=0,skaléieren=1;int 소수부=0,하나라도=0;
    for(;;){int Zeechecode=*Zeechefolleg_Daten,Zil_Daten=Zeechecode>='0'&&Zeechecode<='9'?Zeechecode-'0':Zeechecode>='a'&&Zeechecode<='f'?Zeechecode-'a'+10:Zeechecode>='A'&&Zeechecode<='F'?Zeechecode-'A'+10:99;
        if(Zeechecode=='.'&&!소수부){소수부=1;Zeechefolleg_Daten++;continue;}if(Zil_Daten>=Hannergrond_VALUE)break;하나라도=1;Zeechefolleg_Daten++;임시값=임시값*Hannergrond_VALUE+Zil_Daten;if(소수부)skaléieren*=Hannergrond_VALUE;
    }임시값/=skaléieren;
    if((Hannergrond_VALUE==10&&(*Zeechefolleg_Daten=='e'||*Zeechefolleg_Daten=='E'))||(Hannergrond_VALUE==16&&(*Zeechefolleg_Daten=='p'||*Zeechefolleg_Daten=='P'))){const char*Show_VALUE=Zeechefolleg_Daten++;int 빼기=0;if(*Zeechefolleg_Daten=='-'||*Zeechefolleg_Daten=='+')빼기=*Zeechefolleg_Daten++=='-';int Element_COUNT=0,Agab_COUNT=0;while(*Zeechefolleg_Daten>='0'&&*Zeechefolleg_Daten<='9'){Agab_COUNT++;if(Element_COUNT<20000)Element_COUNT=Element_COUNT*10+*Zeechefolleg_Daten-'0';Zeechefolleg_Daten++;}if(!Agab_COUNT)Zeechefolleg_Daten=Show_VALUE;else{long double Facteur=Hannergrond_VALUE==16?2:10;while(Element_COUNT-->0&&Element_COUNT<200000)임시값=빼기?임시값/Facteur:임시값*Facteur;}}
    if(bëennegen_OFFSET)*bëennegen_OFFSET=(char*)(하나라도?Zeechefolleg_Daten:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*Zeechefolleg_Daten,char**보조항목){return (double)strtold(Zeechefolleg_Daten,보조항목);}float strtof(const char*Zeechefolleg_Daten,char**보조항목){return (float)strtold(Zeechefolleg_Daten,보조항목);}
void qsort(void*Hannergrond_VALUE,size_t Element_COUNT,size_t d_Gréisst_veränneren,int(*Vergläichen)(const void*,const void*)){
    unsigned char*Daten_positionéieren=Hannergrond_VALUE;for(size_t 순번=1;순번<Element_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Vergläichen(Daten_positionéieren+(안쪽순번-1)*d_Gréisst_veränneren,Daten_positionéieren+안쪽순번*d_Gréisst_veränneren)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<d_Gréisst_veränneren;셋째순번++){unsigned char Zeechecode=Daten_positionéieren[(안쪽순번-1)*d_Gréisst_veränneren+셋째순번];Daten_positionéieren[(안쪽순번-1)*d_Gréisst_veränneren+셋째순번]=Daten_positionéieren[안쪽순번*d_Gréisst_veränneren+셋째순번];Daten_positionéieren[안쪽순번*d_Gréisst_veränneren+셋째순번]=Zeechecode;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t positionéieren;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *Element_COUNT){*Element_COUNT=출력크기;return 출력결과;}
int open(const char*Numm,int 설정비트,...){
    if(!strcmp(Numm,"/@cc-output")){if(출력열림){Feeler=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Numm,번역기자원들[순번].Numm)){
        if(설정비트&3){Feeler=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].positionéieren=0;return 128+안쪽순번;}Feeler=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Numm,설정비트,0,0,0,0);if(반환값<0){Feeler=-반환값;return -1;}return 반환값;
}
int close(int Fichier_Handle){if(Fichier_Handle==100){출력열림=0;return 0;}if(Fichier_Handle>=128&&Fichier_Handle<152){열림[Fichier_Handle-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Fichier_Handle,0,0,0,0,0);if(반환값<0){Feeler=-반환값;return -1;}return 0;}
long read(int Fichier_Handle,void*Daten,size_t Element_COUNT){
    if(Fichier_Handle>=128&&Fichier_Handle<152&&열림[Fichier_Handle-128].사용량){int 순번=Fichier_Handle-128;const 번역기자원*반환값=&번역기자원들[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->d_Gréisst_veränneren-열림[순번].positionéieren;if(Element_COUNT>왼쪽)Element_COUNT=왼쪽;memcpy(Daten,반환값->Daten+열림[순번].positionéieren,Element_COUNT);열림[순번].positionéieren+=Element_COUNT;return Element_COUNT;}
    intptr_t 반환값=사용자호출(2,Fichier_Handle,(uintptr_t)Daten,Element_COUNT,0,0,0);if(반환값<0){Feeler=-반환값;return -1;}return 반환값;
}
long write(int Fichier_Handle,const void*Daten,size_t Element_COUNT){
    if(Fichier_Handle==100){if(Element_COUNT>sizeof(출력결과)-출력위치){Feeler=28;return -1;}memcpy(출력결과+출력위치,Daten,Element_COUNT);출력위치+=Element_COUNT;if(출력크기<출력위치)출력크기=출력위치;return Element_COUNT;}
    intptr_t 반환값=사용자호출(1,Fichier_Handle,(uintptr_t)Daten,Element_COUNT,0,0,0);if(반환값<0){Feeler=-반환값;return -1;}return 반환값;
}
long lseek(int Fichier_Handle,long OFFSET_VALUE,int 기준점){
    if(Fichier_Handle==100){long Daten_positionéieren=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(Daten_positionéieren<0||(size_t)Daten_positionéieren>sizeof(출력결과)){Feeler=22;return -1;}출력위치=Daten_positionéieren;return Daten_positionéieren;}
    if(Fichier_Handle>=128&&Fichier_Handle<152&&열림[Fichier_Handle-128].사용량){int 순번=Fichier_Handle-128;long Daten_positionéieren=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].positionéieren:번역기자원들[열림[순번].LOOKUP_INDEX].d_Gréisst_veränneren);if(Daten_positionéieren<0||(size_t)Daten_positionéieren>번역기자원들[열림[순번].LOOKUP_INDEX].d_Gréisst_veränneren){Feeler=22;return -1;}열림[순번].positionéieren=Daten_positionéieren;return Daten_positionéieren;}
    intptr_t 반환값=사용자호출(5,Fichier_Handle,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){Feeler=-반환값;return -1;}return 반환값;
}
int unlink(const char*Numm){intptr_t 반환값=사용자호출(11,(uintptr_t)Numm,0,0,0,0,0);if(반환값<0){Feeler=-반환값;return -1;}return 반환값;}
char *realpath(const char*Numm,char*Mooss_Daten){if(!Mooss_Daten){Mooss_Daten=malloc(strlen(Numm)+1);if(!Mooss_Daten)return 0;}return strcpy(Mooss_Daten,Numm);}
char *getcwd(char*Daten_positionéieren,size_t Element_COUNT){if(Element_COUNT<2){Feeler=34;return 0;}Daten_positionéieren[0]='/';Daten_positionéieren[1]=0;return Daten_positionéieren;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_Agab){time_t 임시값=0;if(Terminal_Agab)*Terminal_Agab=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_Agab){(void)Terminal_Agab;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE 흐름목록[18]={{1,0,1},{2,0,1}};FILE*stdout=&흐름목록[0],*stderr=&흐름목록[1];
FILE*fdopen(int Fichier_Handle,const char*Method_MODE){(void)Method_MODE;for(unsigned 순번=2;순번<18;순번++)if(!흐름목록[순번].사용량){흐름목록[순번].사용량=1;흐름목록[순번].Feeler=0;흐름목록[순번].Fichier_Handle=Fichier_Handle;return &흐름목록[순번];}Feeler=24;return 0;}
int fflush(FILE*Fichier_Agab){return Fichier_Agab&&Fichier_Agab->Feeler?-1:0;}
int fclose(FILE*Fichier_Agab){int 반환값=close(Fichier_Agab->Fichier_Handle);if(Fichier_Agab->Feeler)반환값=-1;Fichier_Agab->사용량=0;return 반환값;}
size_t fwrite(const void*Daten_positionéieren,size_t Zeechefolleg_Daten,size_t Element_COUNT,FILE*Fichier_Agab){if(!Zeechefolleg_Daten)return 0;if(Element_COUNT>SIZE_MAX/Zeechefolleg_Daten){Fichier_Agab->Feeler=1;return 0;}long 반환값=write(Fichier_Agab->Fichier_Handle,Daten_positionéieren,Zeechefolleg_Daten*Element_COUNT);if(반환값<0){Fichier_Agab->Feeler=1;return 0;}return (size_t)반환값/Zeechefolleg_Daten;}
int fputc(int Zeechecode,FILE*Fichier_Agab){unsigned char SECOND_VALUE=Zeechecode;return fwrite(&SECOND_VALUE,1,1,Fichier_Agab)==1?SECOND_VALUE:EOF;}
int fputs(const char*Zeechefolleg_Daten,FILE*Fichier_Agab){return fwrite(Zeechefolleg_Daten,1,strlen(Zeechefolleg_Daten),Fichier_Agab)==strlen(Zeechefolleg_Daten)?0:EOF;}
static void 넣기(char*Mooss_Daten,size_t 용량한도,size_t*현재위치,char Zeechecode){if(*현재위치+1<용량한도)Mooss_Daten[*현재위치]=Zeechecode;(*현재위치)++;}
int vsnprintf(char*Mooss_Daten,size_t 용량한도,const char*Format,va_list 가변인수){
    size_t 현재위치=0;while(*Format){if(*Format!='%'){넣기(Mooss_Daten,용량한도,&현재위치,*Format++);continue;}Format++;
        int 왼쪽=0,영값=0,대체값=0;while(*Format=='-'||*Format=='0'||*Format=='#'||*Format=='+'||*Format==' '){if(*Format=='-')왼쪽=1;if(*Format=='0')영값=1;if(*Format=='#')대체값=1;Format++;}
        int 너비=0,정밀도=-1;if(*Format=='*'){너비=va_arg(가변인수,int);Format++;}else while(*Format>='0'&&*Format<='9')너비=너비*10+*Format++-'0';
        if(*Format=='.'){Format++;정밀도=0;if(*Format=='*'){정밀도=va_arg(가변인수,int);Format++;}else while(*Format>='0'&&*Format<='9')정밀도=정밀도*10+*Format++-'0';}
        int 넓은글자=0;while(*Format=='l'||*Format=='z'||*Format=='t'||*Format=='j'||*Format=='h'){if(*Format!='h')넓은글자=1;Format++;}
        char TYPE_Kategorie=*Format?*Format++:0,Puffer_Späicher[80];const char*Zeechefolleg_Daten=Puffer_Späicher;size_t Element_COUNT=0;
        if(TYPE_Kategorie=='s'){Zeechefolleg_Daten=va_arg(가변인수,const char*);if(!Zeechefolleg_Daten)Zeechefolleg_Daten="(null)";Element_COUNT=strlen(Zeechefolleg_Daten);if(정밀도>=0&&Element_COUNT>(size_t)정밀도)Element_COUNT=정밀도;}
        else if(TYPE_Kategorie=='c'){Puffer_Späicher[0]=va_arg(가변인수,int);Element_COUNT=1;}
        else if(TYPE_Kategorie=='%'){Puffer_Späicher[0]='%';Element_COUNT=1;}
        else if(TYPE_Kategorie=='d'||TYPE_Kategorie=='i'||TYPE_Kategorie=='u'||TYPE_Kategorie=='x'||TYPE_Kategorie=='X'||TYPE_Kategorie=='o'||TYPE_Kategorie=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_Kategorie=='d'||TYPE_Kategorie=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_Kategorie=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Hannergrond_VALUE=TYPE_Kategorie=='x'||TYPE_Kategorie=='X'||TYPE_Kategorie=='p'?16:TYPE_Kategorie=='o'?8:10;char Ziffer_COUNT[64];unsigned 사용량=0;
            do{Ziffer_COUNT[사용량++]="0123456789abcdef"[VALUE%Hannergrond_VALUE];VALUE/=Hannergrond_VALUE;}while(VALUE);
            if(음수표시)Puffer_Späicher[Element_COUNT++]='-';if(TYPE_Kategorie=='p'||(대체값&&Hannergrond_VALUE==16)){Puffer_Späicher[Element_COUNT++]='0';Puffer_Späicher[Element_COUNT++]='x';}
            for(int fëllen_VALUE=(int)사용량;정밀도>fëllen_VALUE&&Element_COUNT<sizeof(Puffer_Späicher)-사용량;fëllen_VALUE++)Puffer_Späicher[Element_COUNT++]='0';
            if(영값&&!왼쪽&&정밀도<0)while(너비>(int)(Element_COUNT+사용량)&&Element_COUNT<sizeof(Puffer_Späicher)-사용량)Puffer_Späicher[Element_COUNT++]='0';
            while(사용량)Puffer_Späicher[Element_COUNT++]=Ziffer_COUNT[--사용량];
        }else{Puffer_Späicher[0]='?';Element_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)Element_COUNT){넣기(Mooss_Daten,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<Element_COUNT;순번++)넣기(Mooss_Daten,용량한도,&현재위치,Zeechefolleg_Daten[순번]);while(왼쪽&&너비>(int)Element_COUNT){넣기(Mooss_Daten,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)Mooss_Daten[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*Mooss_Daten,size_t 용량한도,const char*Fichier_Agab,...){va_list 첫째값;va_start(첫째값,Fichier_Agab);int 반환값=vsnprintf(Mooss_Daten,용량한도,Fichier_Agab,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*Mooss_Daten,const char*Fichier_Agab,...){va_list 첫째값;va_start(첫째값,Fichier_Agab);int 반환값=vsnprintf(Mooss_Daten,SIZE_MAX,Fichier_Agab,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*Fichier_Agab,va_list 첫째값){char SECOND_VALUE[2048];int Element_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Fichier_Agab,첫째값);if(Element_COUNT>2047)Element_COUNT=2047;return fwrite(SECOND_VALUE,1,Element_COUNT,Stream_VALUE)==(size_t)Element_COUNT?Element_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*Fichier_Agab,...){va_list 첫째값;va_start(첫째값,Fichier_Agab);int 반환값=vfprintf(Stream_VALUE,Fichier_Agab,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Fichier_Agab,...){va_list 첫째값;va_start(첫째값,Fichier_Agab);int 반환값=vfprintf(stdout,Fichier_Agab,첫째값);va_end(첫째값);return 반환값;}
