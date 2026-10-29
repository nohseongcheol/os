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
static int errorea;
int *__errno_location(void){return &errorea;}
void exit(int Egoera_balio){사용자호출(6,Egoera_balio,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *txeke_adierazpen,const char *Fitxategia,unsigned Marra,const char *함수이름){fprintf(stderr,"cc assertion: %s %s:%u %s\n",txeke_adierazpen,Fitxategia,Marra,함수이름);exit(1);}
size_t strlen(const char*kate_datuak){const char*datuak_kargu=kate_datuak;while(*datuak_kargu)datuak_kargu++;return datuak_kargu-kate_datuak;}
int strcmp(const char*첫째값,const char*SEGUNDOA_balio){while(*첫째값&&*첫째값==*SEGUNDOA_balio){첫째값++;SEGUNDOA_balio++;}return (unsigned char)*첫째값-(unsigned char)*SEGUNDOA_balio;}
int strncmp(const char*첫째값,const char*SEGUNDOA_balio,size_t elementu_ZENBATU){while(elementu_ZENBATU--){unsigned char X_koordenatu=*첫째값++,Y_koordenatu=*SEGUNDOA_balio++;if(X_koordenatu!=Y_koordenatu)return X_koordenatu-Y_koordenatu;if(!X_koordenatu)return 0;}return 0;}
char *strcpy(char*helburu_datuak,const char*kate_datuak){char*반환값=helburu_datuak;while((*helburu_datuak++=*kate_datuak++)){}return 반환값;}
char *strchr(const char*kate_datuak,int karaktere_kode){do{if(*kate_datuak==(char)karaktere_kode)return (char*)kate_datuak;}while(*kate_datuak++);return 0;}
char *strrchr(const char*kate_datuak,int karaktere_kode){const char*반환값=0;do{if(*kate_datuak==(char)karaktere_kode)반환값=kate_datuak;}while(*kate_datuak++);return (char*)반환값;}
char *strstr(const char*kate_datuak,const char*Terminal_sarrera){size_t elementu_ZENBATU=strlen(Terminal_sarrera);for(;*kate_datuak;kate_datuak++)if(!strncmp(kate_datuak,Terminal_sarrera,elementu_ZENBATU))return (char*)kate_datuak;return elementu_ZENBATU?0:(char*)kate_datuak;}
int memcmp(const void*첫째값,const void*SEGUNDOA_balio,size_t elementu_ZENBATU){const unsigned char*X_koordenatu=첫째값,*Y_koordenatu=SEGUNDOA_balio;while(elementu_ZENBATU--){if(*X_koordenatu!=*Y_koordenatu)return *X_koordenatu-*Y_koordenatu;X_koordenatu++;Y_koordenatu++;}return 0;}
void *memmove(void*helburu_datuak,const void*kate_datuak,size_t elementu_ZENBATU){unsigned char*X_koordenatu=helburu_datuak;const unsigned char*Y_koordenatu=kate_datuak;if(X_koordenatu<Y_koordenatu){for(size_t 순번=0;순번<elementu_ZENBATU;순번++)X_koordenatu[순번]=Y_koordenatu[순번];}else while(elementu_ZENBATU){elementu_ZENBATU--;X_koordenatu[elementu_ZENBATU]=Y_koordenatu[elementu_ZENBATU];}return helburu_datuak;}
static unsigned char biltegi_esleipen_Borroka_lekua[6*1024*1024] __attribute__((aligned(16)));
typedef struct datuak_blokeatu {size_t Tamaina;struct datuak_blokeatu*Hurrengoa_elementu;int 남은공간;int 채울크기;uint64_t lerrokatze_unitate;} datuak_blokeatu;
static datuak_blokeatu *첫항목;
void free(void*datuak_kargu){if(!datuak_kargu)return;datuak_blokeatu*SEGUNDOA_balio=(datuak_blokeatu*)datuak_kargu-1;SEGUNDOA_balio->남은공간=1;for(datuak_blokeatu*Hurrengoa_Geruzak=첫항목;Hurrengoa_Geruzak&&Hurrengoa_Geruzak->Hurrengoa_elementu;){if(Hurrengoa_Geruzak->남은공간&&Hurrengoa_Geruzak->Hurrengoa_elementu->남은공간){Hurrengoa_Geruzak->Tamaina+=sizeof(datuak_blokeatu)+Hurrengoa_Geruzak->Hurrengoa_elementu->Tamaina;Hurrengoa_Geruzak->Hurrengoa_elementu=Hurrengoa_Geruzak->Hurrengoa_elementu->Hurrengoa_elementu;}else Hurrengoa_Geruzak=Hurrengoa_Geruzak->Hurrengoa_elementu;}}
void *realloc(void*datuak_kargu,size_t elementu_ZENBATU){
    if(!elementu_ZENBATU){free(datuak_kargu);return 0;}if(elementu_ZENBATU>sizeof(biltegi_esleipen_Borroka_lekua)-sizeof(datuak_blokeatu))return 0;elementu_ZENBATU=(elementu_ZENBATU+15)&~(size_t)15;
    if(!첫항목){첫항목=(datuak_blokeatu*)biltegi_esleipen_Borroka_lekua;첫항목->Tamaina=sizeof(biltegi_esleipen_Borroka_lekua)-sizeof(datuak_blokeatu);첫항목->남은공간=1;첫항목->Hurrengoa_elementu=0;}
    datuak_blokeatu*이전=datuak_kargu?(datuak_blokeatu*)datuak_kargu-1:0;if(이전&&이전->Tamaina>=elementu_ZENBATU)return datuak_kargu;
    for(datuak_blokeatu*SEGUNDOA_balio=첫항목;SEGUNDOA_balio;SEGUNDOA_balio=SEGUNDOA_balio->Hurrengoa_elementu)if(SEGUNDOA_balio->남은공간&&SEGUNDOA_balio->Tamaina>=elementu_ZENBATU){
        if(SEGUNDOA_balio->Tamaina>=elementu_ZENBATU+sizeof(datuak_blokeatu)+16){datuak_blokeatu*나머지부분=(datuak_blokeatu*)((unsigned char*)(SEGUNDOA_balio+1)+elementu_ZENBATU);나머지부분->Tamaina=SEGUNDOA_balio->Tamaina-elementu_ZENBATU-sizeof(datuak_blokeatu);나머지부분->Hurrengoa_elementu=SEGUNDOA_balio->Hurrengoa_elementu;나머지부분->남은공간=1;SEGUNDOA_balio->Hurrengoa_elementu=나머지부분;SEGUNDOA_balio->Tamaina=elementu_ZENBATU;}
        SEGUNDOA_balio->남은공간=0;void*반환값=SEGUNDOA_balio+1;if(이전){memcpy(반환값,datuak_kargu,이전->Tamaina);free(datuak_kargu);}return 반환값;
    }errorea=12;return 0;
}
void *malloc(size_t elementu_ZENBATU){return realloc(0,elementu_ZENBATU);}
void *calloc(size_t elementu_ZENBATU,size_t kate_datuak){if(kate_datuak&&elementu_ZENBATU>SIZE_MAX/kate_datuak)return 0;void*datuak_kargu=malloc(elementu_ZENBATU*kate_datuak);if(datuak_kargu)memset(datuak_kargu,0,elementu_ZENBATU*kate_datuak);return datuak_kargu;}
unsigned long long strtoull(const char*kate_datuak,char**amaitu_Geruzak,int horma_paper_balio){
    const char*HASI_Geruzak=kate_datuak;while(*kate_datuak==' '||(*kate_datuak>=9&&*kate_datuak<=13))kate_datuak++;int 음수여부=0;if(*kate_datuak=='-'||*kate_datuak=='+')음수여부=*kate_datuak++=='-';
    if((!horma_paper_balio||horma_paper_balio==16)&&kate_datuak[0]=='0'&&(kate_datuak[1]=='x'||kate_datuak[1]=='X')){horma_paper_balio=16;kate_datuak+=2;}if(!horma_paper_balio)horma_paper_balio=*kate_datuak=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned karaktere_kode=*kate_datuak,helburu_datuak=karaktere_kode>='0'&&karaktere_kode<='9'?karaktere_kode-'0':karaktere_kode>='a'&&karaktere_kode<='z'?karaktere_kode-'a'+10:karaktere_kode>='A'&&karaktere_kode<='Z'?karaktere_kode-'A'+10:99;if(helburu_datuak>=(unsigned)horma_paper_balio)break;하나라도=1;kate_datuak++;if(임시값>(~0ull-helburu_datuak)/(unsigned)horma_paper_balio){임시값=~0ull;errorea=34;}else 임시값=임시값*horma_paper_balio+helburu_datuak;}
    if(amaitu_Geruzak)*amaitu_Geruzak=(char*)(하나라도?kate_datuak:HASI_Geruzak);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*kate_datuak,char**보조항목,int SEGUNDOA_balio){return strtoull(kate_datuak,보조항목,SEGUNDOA_balio);}
long strtol(const char*kate_datuak,char**보조항목,int SEGUNDOA_balio){return (long)strtoull(kate_datuak,보조항목,SEGUNDOA_balio);}
int atoi(const char*kate_datuak){return (int)strtol(kate_datuak,0,10);}
long double ldexpl(long double X_koordenatu,int elementu_ZENBATU){while(elementu_ZENBATU>0){X_koordenatu*=2;elementu_ZENBATU--;}while(elementu_ZENBATU<0){X_koordenatu/=2;elementu_ZENBATU++;}return X_koordenatu;}
long double strtold(const char*kate_datuak,char**amaitu_Geruzak){
    const char*HASI_Geruzak=kate_datuak;while(*kate_datuak==' '||(*kate_datuak>=9&&*kate_datuak<=13))kate_datuak++;int 음수여부=0;if(*kate_datuak=='-'||*kate_datuak=='+')음수여부=*kate_datuak++=='-';
    int horma_paper_balio=10;if(kate_datuak[0]=='0'&&(kate_datuak[1]=='x'||kate_datuak[1]=='X')){horma_paper_balio=16;kate_datuak+=2;}long double 임시값=0,eskalan_jarri=1;int 소수부=0,하나라도=0;
    for(;;){int karaktere_kode=*kate_datuak,helburu_datuak=karaktere_kode>='0'&&karaktere_kode<='9'?karaktere_kode-'0':karaktere_kode>='a'&&karaktere_kode<='f'?karaktere_kode-'a'+10:karaktere_kode>='A'&&karaktere_kode<='F'?karaktere_kode-'A'+10:99;
        if(karaktere_kode=='.'&&!소수부){소수부=1;kate_datuak++;continue;}if(helburu_datuak>=horma_paper_balio)break;하나라도=1;kate_datuak++;임시값=임시값*horma_paper_balio+helburu_datuak;if(소수부)eskalan_jarri*=horma_paper_balio;
    }임시값/=eskalan_jarri;
    if((horma_paper_balio==10&&(*kate_datuak=='e'||*kate_datuak=='E'))||(horma_paper_balio==16&&(*kate_datuak=='p'||*kate_datuak=='P'))){const char*erakutsi_balio=kate_datuak++;int 빼기=0;if(*kate_datuak=='-'||*kate_datuak=='+')빼기=*kate_datuak++=='-';int elementu_ZENBATU=0,sarrera_ZENBATU=0;while(*kate_datuak>='0'&&*kate_datuak<='9'){sarrera_ZENBATU++;if(elementu_ZENBATU<20000)elementu_ZENBATU=elementu_ZENBATU*10+*kate_datuak-'0';kate_datuak++;}if(!sarrera_ZENBATU)kate_datuak=erakutsi_balio;else{long double biderkagai=horma_paper_balio==16?2:10;while(elementu_ZENBATU-->0&&elementu_ZENBATU<200000)임시값=빼기?임시값/biderkagai:임시값*biderkagai;}}
    if(amaitu_Geruzak)*amaitu_Geruzak=(char*)(하나라도?kate_datuak:HASI_Geruzak);return 음수여부?-임시값:임시값;
}
double strtod(const char*kate_datuak,char**보조항목){return (double)strtold(kate_datuak,보조항목);}float strtof(const char*kate_datuak,char**보조항목){return (float)strtold(kate_datuak,보조항목);}
void qsort(void*horma_paper_balio,size_t elementu_ZENBATU,size_t Tamaina,int(*Alderatu)(const void*,const void*)){
    unsigned char*datuak_kargu=horma_paper_balio;for(size_t 순번=1;순번<elementu_ZENBATU;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Alderatu(datuak_kargu+(안쪽순번-1)*Tamaina,datuak_kargu+안쪽순번*Tamaina)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Tamaina;셋째순번++){unsigned char karaktere_kode=datuak_kargu[(안쪽순번-1)*Tamaina+셋째순번];datuak_kargu[(안쪽순번-1)*Tamaina+셋째순번]=datuak_kargu[안쪽순번*Tamaina+셋째순번];datuak_kargu[안쪽순번*Tamaina+셋째순번]=karaktere_kode;}
}
static struct {int 사용량,BEGIRATU_INDIZE;size_t Posizioa;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *elementu_ZENBATU){*elementu_ZENBATU=출력크기;return 출력결과;}
int open(const char*Izena,int konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna,...){
    if(!strcmp(Izena,"/@cc-output")){if(출력열림){errorea=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Izena,번역기자원들[순번].Izena)){
        if(konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&3){errorea=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].BEGIRATU_INDIZE=순번;열림[안쪽순번].Posizioa=0;return 128+안쪽순번;}errorea=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Izena,konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna,0,0,0,0);if(반환값<0){errorea=-반환값;return -1;}return 반환값;
}
int close(int fitxategi_helduleku){if(fitxategi_helduleku==100){출력열림=0;return 0;}if(fitxategi_helduleku>=128&&fitxategi_helduleku<152){열림[fitxategi_helduleku-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,fitxategi_helduleku,0,0,0,0,0);if(반환값<0){errorea=-반환값;return -1;}return 0;}
long read(int fitxategi_helduleku,void*datuak,size_t elementu_ZENBATU){
    if(fitxategi_helduleku>=128&&fitxategi_helduleku<152&&열림[fitxategi_helduleku-128].사용량){int 순번=fitxategi_helduleku-128;const 번역기자원*반환값=&번역기자원들[열림[순번].BEGIRATU_INDIZE];size_t 왼쪽=반환값->Tamaina-열림[순번].Posizioa;if(elementu_ZENBATU>왼쪽)elementu_ZENBATU=왼쪽;memcpy(datuak,반환값->datuak+열림[순번].Posizioa,elementu_ZENBATU);열림[순번].Posizioa+=elementu_ZENBATU;return elementu_ZENBATU;}
    intptr_t 반환값=사용자호출(2,fitxategi_helduleku,(uintptr_t)datuak,elementu_ZENBATU,0,0,0);if(반환값<0){errorea=-반환값;return -1;}return 반환값;
}
long write(int fitxategi_helduleku,const void*datuak,size_t elementu_ZENBATU){
    if(fitxategi_helduleku==100){if(elementu_ZENBATU>sizeof(출력결과)-출력위치){errorea=28;return -1;}memcpy(출력결과+출력위치,datuak,elementu_ZENBATU);출력위치+=elementu_ZENBATU;if(출력크기<출력위치)출력크기=출력위치;return elementu_ZENBATU;}
    intptr_t 반환값=사용자호출(1,fitxategi_helduleku,(uintptr_t)datuak,elementu_ZENBATU,0,0,0);if(반환값<0){errorea=-반환값;return -1;}return 반환값;
}
long lseek(int fitxategi_helduleku,long Geruzak_balio,int 기준점){
    if(fitxategi_helduleku==100){long datuak_kargu=Geruzak_balio+(기준점==0?0:기준점==1?출력위치:출력크기);if(datuak_kargu<0||(size_t)datuak_kargu>sizeof(출력결과)){errorea=22;return -1;}출력위치=datuak_kargu;return datuak_kargu;}
    if(fitxategi_helduleku>=128&&fitxategi_helduleku<152&&열림[fitxategi_helduleku-128].사용량){int 순번=fitxategi_helduleku-128;long datuak_kargu=Geruzak_balio+(기준점==0?0:기준점==1?열림[순번].Posizioa:번역기자원들[열림[순번].BEGIRATU_INDIZE].Tamaina);if(datuak_kargu<0||(size_t)datuak_kargu>번역기자원들[열림[순번].BEGIRATU_INDIZE].Tamaina){errorea=22;return -1;}열림[순번].Posizioa=datuak_kargu;return datuak_kargu;}
    intptr_t 반환값=사용자호출(5,fitxategi_helduleku,Geruzak_balio,기준점,0,0,0);if(반환값<0){errorea=-반환값;return -1;}return 반환값;
}
int unlink(const char*Izena){intptr_t 반환값=사용자호출(11,(uintptr_t)Izena,0,0,0,0,0);if(반환값<0){errorea=-반환값;return -1;}return 반환값;}
char *realpath(const char*Izena,char*neurria_datuak){if(!neurria_datuak){neurria_datuak=malloc(strlen(Izena)+1);if(!neurria_datuak)return 0;}return strcpy(neurria_datuak,Izena);}
char *getcwd(char*datuak_kargu,size_t elementu_ZENBATU){if(elementu_ZENBATU<2){errorea=34;return 0;}datuak_kargu[0]='/';datuak_kargu[1]=0;return datuak_kargu;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_sarrera){time_t 임시값=0;if(Terminal_sarrera)*Terminal_sarrera=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_sarrera){(void)Terminal_sarrera;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Korronteak[18]={{1,0,1},{2,0,1}};FILE*stdout=&Korronteak[0],*stderr=&Korronteak[1];
FILE*fdopen(int fitxategi_helduleku,const char*방식){(void)방식;for(unsigned 순번=2;순번<18;순번++)if(!Korronteak[순번].사용량){Korronteak[순번].사용량=1;Korronteak[순번].errorea=0;Korronteak[순번].fitxategi_helduleku=fitxategi_helduleku;return &Korronteak[순번];}errorea=24;return 0;}
int fflush(FILE*fitxategi_sarrera){return fitxategi_sarrera&&fitxategi_sarrera->errorea?-1:0;}
int fclose(FILE*fitxategi_sarrera){int 반환값=close(fitxategi_sarrera->fitxategi_helduleku);if(fitxategi_sarrera->errorea)반환값=-1;fitxategi_sarrera->사용량=0;return 반환값;}
size_t fwrite(const void*datuak_kargu,size_t kate_datuak,size_t elementu_ZENBATU,FILE*fitxategi_sarrera){if(!kate_datuak)return 0;if(elementu_ZENBATU>SIZE_MAX/kate_datuak){fitxategi_sarrera->errorea=1;return 0;}long 반환값=write(fitxategi_sarrera->fitxategi_helduleku,datuak_kargu,kate_datuak*elementu_ZENBATU);if(반환값<0){fitxategi_sarrera->errorea=1;return 0;}return (size_t)반환값/kate_datuak;}
int fputc(int karaktere_kode,FILE*fitxategi_sarrera){unsigned char SEGUNDOA_balio=karaktere_kode;return fwrite(&SEGUNDOA_balio,1,1,fitxategi_sarrera)==1?SEGUNDOA_balio:EOF;}
int fputs(const char*kate_datuak,FILE*fitxategi_sarrera){return fwrite(kate_datuak,1,strlen(kate_datuak),fitxategi_sarrera)==strlen(kate_datuak)?0:EOF;}
static void 넣기(char*neurria_datuak,size_t 용량한도,size_t*현재위치,char karaktere_kode){if(*현재위치+1<용량한도)neurria_datuak[*현재위치]=karaktere_kode;(*현재위치)++;}
int vsnprintf(char*neurria_datuak,size_t 용량한도,const char*formatu,va_list 가변인수){
    size_t 현재위치=0;while(*formatu){if(*formatu!='%'){넣기(neurria_datuak,용량한도,&현재위치,*formatu++);continue;}formatu++;
        int 왼쪽=0,영값=0,대체값=0;while(*formatu=='-'||*formatu=='0'||*formatu=='#'||*formatu=='+'||*formatu==' '){if(*formatu=='-')왼쪽=1;if(*formatu=='0')영값=1;if(*formatu=='#')대체값=1;formatu++;}
        int 너비=0,zehaztasun_balio=-1;if(*formatu=='*'){너비=va_arg(가변인수,int);formatu++;}else while(*formatu>='0'&&*formatu<='9')너비=너비*10+*formatu++-'0';
        if(*formatu=='.'){formatu++;zehaztasun_balio=0;if(*formatu=='*'){zehaztasun_balio=va_arg(가변인수,int);formatu++;}else while(*formatu>='0'&&*formatu<='9')zehaztasun_balio=zehaztasun_balio*10+*formatu++-'0';}
        int 넓은글자=0;while(*formatu=='l'||*formatu=='z'||*formatu=='t'||*formatu=='j'||*formatu=='h'){if(*formatu!='h')넓은글자=1;formatu++;}
        char MOTA_Kategoria=*formatu?*formatu++:0,buffer_biltegi[80];const char*kate_datuak=buffer_biltegi;size_t elementu_ZENBATU=0;
        if(MOTA_Kategoria=='s'){kate_datuak=va_arg(가변인수,const char*);if(!kate_datuak)kate_datuak="(null)";elementu_ZENBATU=strlen(kate_datuak);if(zehaztasun_balio>=0&&elementu_ZENBATU>(size_t)zehaztasun_balio)elementu_ZENBATU=zehaztasun_balio;}
        else if(MOTA_Kategoria=='c'){buffer_biltegi[0]=va_arg(가변인수,int);elementu_ZENBATU=1;}
        else if(MOTA_Kategoria=='%'){buffer_biltegi[0]='%';elementu_ZENBATU=1;}
        else if(MOTA_Kategoria=='d'||MOTA_Kategoria=='i'||MOTA_Kategoria=='u'||MOTA_Kategoria=='x'||MOTA_Kategoria=='X'||MOTA_Kategoria=='o'||MOTA_Kategoria=='p'){
            unsigned long long balio;int 음수표시=0;
            if(MOTA_Kategoria=='d'||MOTA_Kategoria=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;balio=음수표시?0-(unsigned long long)임시값:임시값;}
            else balio=MOTA_Kategoria=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned horma_paper_balio=MOTA_Kategoria=='x'||MOTA_Kategoria=='X'||MOTA_Kategoria=='p'?16:MOTA_Kategoria=='o'?8:10;char digitu_ZENBATU[64];unsigned 사용량=0;
            do{digitu_ZENBATU[사용량++]="0123456789abcdef"[balio%horma_paper_balio];balio/=horma_paper_balio;}while(balio);
            if(음수표시)buffer_biltegi[elementu_ZENBATU++]='-';if(MOTA_Kategoria=='p'||(대체값&&horma_paper_balio==16)){buffer_biltegi[elementu_ZENBATU++]='0';buffer_biltegi[elementu_ZENBATU++]='x';}
            for(int bete_balio=(int)사용량;zehaztasun_balio>bete_balio&&elementu_ZENBATU<sizeof(buffer_biltegi)-사용량;bete_balio++)buffer_biltegi[elementu_ZENBATU++]='0';
            if(영값&&!왼쪽&&zehaztasun_balio<0)while(너비>(int)(elementu_ZENBATU+사용량)&&elementu_ZENBATU<sizeof(buffer_biltegi)-사용량)buffer_biltegi[elementu_ZENBATU++]='0';
            while(사용량)buffer_biltegi[elementu_ZENBATU++]=digitu_ZENBATU[--사용량];
        }else{buffer_biltegi[0]='?';elementu_ZENBATU=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)elementu_ZENBATU){넣기(neurria_datuak,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<elementu_ZENBATU;순번++)넣기(neurria_datuak,용량한도,&현재위치,kate_datuak[순번]);while(왼쪽&&너비>(int)elementu_ZENBATU){넣기(neurria_datuak,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)neurria_datuak[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*neurria_datuak,size_t 용량한도,const char*fitxategi_sarrera,...){va_list 첫째값;va_start(첫째값,fitxategi_sarrera);int 반환값=vsnprintf(neurria_datuak,용량한도,fitxategi_sarrera,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*neurria_datuak,const char*fitxategi_sarrera,...){va_list 첫째값;va_start(첫째값,fitxategi_sarrera);int 반환값=vsnprintf(neurria_datuak,SIZE_MAX,fitxategi_sarrera,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_balio,const char*fitxategi_sarrera,va_list 첫째값){char SEGUNDOA_balio[2048];int elementu_ZENBATU=vsnprintf(SEGUNDOA_balio,sizeof(SEGUNDOA_balio),fitxategi_sarrera,첫째값);if(elementu_ZENBATU>2047)elementu_ZENBATU=2047;return fwrite(SEGUNDOA_balio,1,elementu_ZENBATU,Stream_balio)==(size_t)elementu_ZENBATU?elementu_ZENBATU:-1;}
int fprintf(FILE*Stream_balio,const char*fitxategi_sarrera,...){va_list 첫째값;va_start(첫째값,fitxategi_sarrera);int 반환값=vfprintf(Stream_balio,fitxategi_sarrera,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fitxategi_sarrera,...){va_list 첫째값;va_start(첫째값,fitxategi_sarrera);int 반환값=vfprintf(stdout,fitxategi_sarrera,첫째값);va_end(첫째값);return 반환값;}
