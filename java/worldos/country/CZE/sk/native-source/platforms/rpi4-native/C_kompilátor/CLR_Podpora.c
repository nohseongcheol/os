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
static int chyba;
int *__errno_location(void){return &chyba;}
void exit(int Stav_VALUE){사용자호출(6,Stav_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *skontrolovať_výraz,const char *Súbor,unsigned riadok,const char *metóda_položka_názov){fprintf(stderr,"cc assertion: %s %s:%u %s\n",skontrolovať_výraz,Súbor,riadok,metóda_položka_názov);exit(1);}
size_t strlen(const char*reťazec_údaje){const char*údaje_pozícia=reťazec_údaje;while(*údaje_pozícia)údaje_pozícia++;return údaje_pozícia-reťazec_údaje;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t položka_COUNT){while(položka_COUNT--){unsigned char X_súradnica=*첫째값++,Y_súradnica=*SECOND_VALUE++;if(X_súradnica!=Y_súradnica)return X_súradnica-Y_súradnica;if(!X_súradnica)return 0;}return 0;}
char *strcpy(char*cieľ_údaje,const char*reťazec_údaje){char*반환값=cieľ_údaje;while((*cieľ_údaje++=*reťazec_údaje++)){}return 반환값;}
char *strchr(const char*reťazec_údaje,int bod_kódu){do{if(*reťazec_údaje==(char)bod_kódu)return (char*)reťazec_údaje;}while(*reťazec_údaje++);return 0;}
char *strrchr(const char*reťazec_údaje,int bod_kódu){const char*반환값=0;do{if(*reťazec_údaje==(char)bod_kódu)반환값=reťazec_údaje;}while(*reťazec_údaje++);return (char*)반환값;}
char *strstr(const char*reťazec_údaje,const char*Terminál_položka){size_t položka_COUNT=strlen(Terminál_položka);for(;*reťazec_údaje;reťazec_údaje++)if(!strncmp(reťazec_údaje,Terminál_položka,položka_COUNT))return (char*)reťazec_údaje;return položka_COUNT?0:(char*)reťazec_údaje;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t položka_COUNT){const unsigned char*X_súradnica=첫째값,*Y_súradnica=SECOND_VALUE;while(položka_COUNT--){if(*X_súradnica!=*Y_súradnica)return *X_súradnica-*Y_súradnica;X_súradnica++;Y_súradnica++;}return 0;}
void *memmove(void*cieľ_údaje,const void*reťazec_údaje,size_t položka_COUNT){unsigned char*X_súradnica=cieľ_údaje;const unsigned char*Y_súradnica=reťazec_údaje;if(X_súradnica<Y_súradnica){for(size_t 순번=0;순번<položka_COUNT;순번++)X_súradnica[순번]=Y_súradnica[순번];}else while(položka_COUNT){položka_COUNT--;X_súradnica[položka_COUNT]=Y_súradnica[položka_COUNT];}return cieľ_údaje;}
static unsigned char vyhradenie_Aréna[6*1024*1024] __attribute__((aligned(16)));
typedef struct blok_údajov {size_t Veľkosť;struct blok_údajov*Ďalej_položka;int 남은공간;int pridanie_výplne;uint64_t zarovnanie_lekcia;} blok_údajov;
static blok_údajov *첫항목;
void free(void*údaje_pozícia){if(!údaje_pozícia)return;blok_údajov*SECOND_VALUE=(blok_údajov*)údaje_pozícia-1;SECOND_VALUE->남은공간=1;for(blok_údajov*Ďalej_Posun=첫항목;Ďalej_Posun&&Ďalej_Posun->Ďalej_položka;){if(Ďalej_Posun->남은공간&&Ďalej_Posun->Ďalej_položka->남은공간){Ďalej_Posun->Veľkosť+=sizeof(blok_údajov)+Ďalej_Posun->Ďalej_položka->Veľkosť;Ďalej_Posun->Ďalej_položka=Ďalej_Posun->Ďalej_položka->Ďalej_položka;}else Ďalej_Posun=Ďalej_Posun->Ďalej_položka;}}
void *realloc(void*údaje_pozícia,size_t položka_COUNT){
    if(!položka_COUNT){free(údaje_pozícia);return 0;}if(položka_COUNT>sizeof(vyhradenie_Aréna)-sizeof(blok_údajov))return 0;položka_COUNT=(položka_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(blok_údajov*)vyhradenie_Aréna;첫항목->Veľkosť=sizeof(vyhradenie_Aréna)-sizeof(blok_údajov);첫항목->남은공간=1;첫항목->Ďalej_položka=0;}
    blok_údajov*이전=údaje_pozícia?(blok_údajov*)údaje_pozícia-1:0;if(이전&&이전->Veľkosť>=položka_COUNT)return údaje_pozícia;
    for(blok_údajov*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Ďalej_položka)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Veľkosť>=položka_COUNT){
        if(SECOND_VALUE->Veľkosť>=položka_COUNT+sizeof(blok_údajov)+16){blok_údajov*나머지부분=(blok_údajov*)((unsigned char*)(SECOND_VALUE+1)+položka_COUNT);나머지부분->Veľkosť=SECOND_VALUE->Veľkosť-položka_COUNT-sizeof(blok_údajov);나머지부분->Ďalej_položka=SECOND_VALUE->Ďalej_položka;나머지부분->남은공간=1;SECOND_VALUE->Ďalej_položka=나머지부분;SECOND_VALUE->Veľkosť=položka_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,údaje_pozícia,이전->Veľkosť);free(údaje_pozícia);}return 반환값;
    }chyba=12;return 0;
}
void *malloc(size_t položka_COUNT){return realloc(0,položka_COUNT);}
void *calloc(size_t položka_COUNT,size_t reťazec_údaje){if(reťazec_údaje&&položka_COUNT>SIZE_MAX/reťazec_údaje)return 0;void*údaje_pozícia=malloc(položka_COUNT*reťazec_údaje);if(údaje_pozícia)memset(údaje_pozícia,0,položka_COUNT*reťazec_údaje);return údaje_pozícia;}
unsigned long long strtoull(const char*reťazec_údaje,char**ukončiť_hovor_Posun,int tapeta_VALUE){
    const char*START_Posun=reťazec_údaje;while(*reťazec_údaje==' '||(*reťazec_údaje>=9&&*reťazec_údaje<=13))reťazec_údaje++;int 음수여부=0;if(*reťazec_údaje=='-'||*reťazec_údaje=='+')음수여부=*reťazec_údaje++=='-';
    if((!tapeta_VALUE||tapeta_VALUE==16)&&reťazec_údaje[0]=='0'&&(reťazec_údaje[1]=='x'||reťazec_údaje[1]=='X')){tapeta_VALUE=16;reťazec_údaje+=2;}if(!tapeta_VALUE)tapeta_VALUE=*reťazec_údaje=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned bod_kódu=*reťazec_údaje,cieľ_údaje=bod_kódu>='0'&&bod_kódu<='9'?bod_kódu-'0':bod_kódu>='a'&&bod_kódu<='z'?bod_kódu-'a'+10:bod_kódu>='A'&&bod_kódu<='Z'?bod_kódu-'A'+10:99;if(cieľ_údaje>=(unsigned)tapeta_VALUE)break;하나라도=1;reťazec_údaje++;if(임시값>(~0ull-cieľ_údaje)/(unsigned)tapeta_VALUE){임시값=~0ull;chyba=34;}else 임시값=임시값*tapeta_VALUE+cieľ_údaje;}
    if(ukončiť_hovor_Posun)*ukončiť_hovor_Posun=(char*)(하나라도?reťazec_údaje:START_Posun);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*reťazec_údaje,char**보조항목,int SECOND_VALUE){return strtoull(reťazec_údaje,보조항목,SECOND_VALUE);}
long strtol(const char*reťazec_údaje,char**보조항목,int SECOND_VALUE){return (long)strtoull(reťazec_údaje,보조항목,SECOND_VALUE);}
int atoi(const char*reťazec_údaje){return (int)strtol(reťazec_údaje,0,10);}
long double ldexpl(long double X_súradnica,int položka_COUNT){while(položka_COUNT>0){X_súradnica*=2;položka_COUNT--;}while(položka_COUNT<0){X_súradnica/=2;položka_COUNT++;}return X_súradnica;}
long double strtold(const char*reťazec_údaje,char**ukončiť_hovor_Posun){
    const char*START_Posun=reťazec_údaje;while(*reťazec_údaje==' '||(*reťazec_údaje>=9&&*reťazec_údaje<=13))reťazec_údaje++;int 음수여부=0;if(*reťazec_údaje=='-'||*reťazec_údaje=='+')음수여부=*reťazec_údaje++=='-';
    int tapeta_VALUE=10;if(reťazec_údaje[0]=='0'&&(reťazec_údaje[1]=='x'||reťazec_údaje[1]=='X')){tapeta_VALUE=16;reťazec_údaje+=2;}long double 임시값=0,škálovať=1;int 소수부=0,하나라도=0;
    for(;;){int bod_kódu=*reťazec_údaje,cieľ_údaje=bod_kódu>='0'&&bod_kódu<='9'?bod_kódu-'0':bod_kódu>='a'&&bod_kódu<='f'?bod_kódu-'a'+10:bod_kódu>='A'&&bod_kódu<='F'?bod_kódu-'A'+10:99;
        if(bod_kódu=='.'&&!소수부){소수부=1;reťazec_údaje++;continue;}if(cieľ_údaje>=tapeta_VALUE)break;하나라도=1;reťazec_údaje++;임시값=임시값*tapeta_VALUE+cieľ_údaje;if(소수부)škálovať*=tapeta_VALUE;
    }임시값/=škálovať;
    if((tapeta_VALUE==10&&(*reťazec_údaje=='e'||*reťazec_údaje=='E'))||(tapeta_VALUE==16&&(*reťazec_údaje=='p'||*reťazec_údaje=='P'))){const char*zobraziť_VALUE_487749b8=reťazec_údaje++;int 빼기=0;if(*reťazec_údaje=='-'||*reťazec_údaje=='+')빼기=*reťazec_údaje++=='-';int položka_COUNT=0,položka_COUNT_8f7753a1=0;while(*reťazec_údaje>='0'&&*reťazec_údaje<='9'){položka_COUNT_8f7753a1++;if(položka_COUNT<20000)položka_COUNT=položka_COUNT*10+*reťazec_údaje-'0';reťazec_údaje++;}if(!položka_COUNT_8f7753a1)reťazec_údaje=zobraziť_VALUE_487749b8;else{long double činiteľ=tapeta_VALUE==16?2:10;while(položka_COUNT-->0&&položka_COUNT<200000)임시값=빼기?임시값/činiteľ:임시값*činiteľ;}}
    if(ukončiť_hovor_Posun)*ukončiť_hovor_Posun=(char*)(하나라도?reťazec_údaje:START_Posun);return 음수여부?-임시값:임시값;
}
double strtod(const char*reťazec_údaje,char**보조항목){return (double)strtold(reťazec_údaje,보조항목);}float strtof(const char*reťazec_údaje,char**보조항목){return (float)strtold(reťazec_údaje,보조항목);}
void qsort(void*tapeta_VALUE,size_t položka_COUNT,size_t Veľkosť,int(*Compare)(const void*,const void*)){
    unsigned char*údaje_pozícia=tapeta_VALUE;for(size_t 순번=1;순번<položka_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Compare(údaje_pozícia+(안쪽순번-1)*Veľkosť,údaje_pozícia+안쪽순번*Veľkosť)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Veľkosť;셋째순번++){unsigned char bod_kódu=údaje_pozícia[(안쪽순번-1)*Veľkosť+셋째순번];údaje_pozícia[(안쪽순번-1)*Veľkosť+셋째순번]=údaje_pozícia[안쪽순번*Veľkosť+셋째순번];údaje_pozícia[안쪽순번*Veľkosť+셋째순번]=bod_kódu;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Pozícia;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *položka_COUNT){*položka_COUNT=출력크기;return 출력결과;}
int open(const char*Názov,int konfigurácia_Background_Intelligent_Transfer_Service,...){
    if(!strcmp(Názov,"/@cc-output")){if(출력열림){chyba=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompilátor_Zdroje)/sizeof(kompilátor_Zdroje[0]);순번++)if(!strcmp(Názov,kompilátor_Zdroje[순번].Názov)){
        if(konfigurácia_Background_Intelligent_Transfer_Service&3){chyba=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Pozícia=0;return 128+안쪽순번;}chyba=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Názov,konfigurácia_Background_Intelligent_Transfer_Service,0,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;
}
int close(int Súbor_rukoväť){if(Súbor_rukoväť==100){출력열림=0;return 0;}if(Súbor_rukoväť>=128&&Súbor_rukoväť<152){열림[Súbor_rukoväť-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Súbor_rukoväť,0,0,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 0;}
long read(int Súbor_rukoväť,void*údaje,size_t položka_COUNT){
    if(Súbor_rukoväť>=128&&Súbor_rukoväť<152&&열림[Súbor_rukoväť-128].사용량){int 순번=Súbor_rukoväť-128;const kompilátor_zdroj*반환값=&kompilátor_Zdroje[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Veľkosť-열림[순번].Pozícia;if(položka_COUNT>왼쪽)položka_COUNT=왼쪽;memcpy(údaje,반환값->údaje+열림[순번].Pozícia,položka_COUNT);열림[순번].Pozícia+=položka_COUNT;return položka_COUNT;}
    intptr_t 반환값=사용자호출(2,Súbor_rukoväť,(uintptr_t)údaje,položka_COUNT,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;
}
long write(int Súbor_rukoväť,const void*údaje,size_t položka_COUNT){
    if(Súbor_rukoväť==100){if(položka_COUNT>sizeof(출력결과)-출력위치){chyba=28;return -1;}memcpy(출력결과+출력위치,údaje,položka_COUNT);출력위치+=položka_COUNT;if(출력크기<출력위치)출력크기=출력위치;return položka_COUNT;}
    intptr_t 반환값=사용자호출(1,Súbor_rukoväť,(uintptr_t)údaje,položka_COUNT,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;
}
long lseek(int Súbor_rukoväť,long Posun_VALUE,int 기준점){
    if(Súbor_rukoväť==100){long údaje_pozícia=Posun_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(údaje_pozícia<0||(size_t)údaje_pozícia>sizeof(출력결과)){chyba=22;return -1;}출력위치=údaje_pozícia;return údaje_pozícia;}
    if(Súbor_rukoväť>=128&&Súbor_rukoväť<152&&열림[Súbor_rukoväť-128].사용량){int 순번=Súbor_rukoväť-128;long údaje_pozícia=Posun_VALUE+(기준점==0?0:기준점==1?열림[순번].Pozícia:kompilátor_Zdroje[열림[순번].LOOKUP_INDEX].Veľkosť);if(údaje_pozícia<0||(size_t)údaje_pozícia>kompilátor_Zdroje[열림[순번].LOOKUP_INDEX].Veľkosť){chyba=22;return -1;}열림[순번].Pozícia=údaje_pozícia;return údaje_pozícia;}
    intptr_t 반환값=사용자호출(5,Súbor_rukoväť,Posun_VALUE,기준점,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;
}
int unlink(const char*Názov){intptr_t 반환값=사용자호출(11,(uintptr_t)Názov,0,0,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;}
char *realpath(const char*Názov,char*KR_údaje){if(!KR_údaje){KR_údaje=malloc(strlen(Názov)+1);if(!KR_údaje)return 0;}return strcpy(KR_údaje,Názov);}
char *getcwd(char*údaje_pozícia,size_t položka_COUNT){if(položka_COUNT<2){chyba=34;return 0;}údaje_pozícia[0]='/';údaje_pozícia[1]=0;return údaje_pozícia;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminál_položka){time_t 임시값=0;if(Terminál_položka)*Terminál_položka=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminál_položka){(void)Terminál_položka;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Prehľady[18]={{1,0,1},{2,0,1}};FILE*stdout=&Prehľady[0],*stderr=&Prehľady[1];
FILE*fdopen(int Súbor_rukoväť,const char*metóda_MODE){(void)metóda_MODE;for(unsigned 순번=2;순번<18;순번++)if(!Prehľady[순번].사용량){Prehľady[순번].사용량=1;Prehľady[순번].chyba=0;Prehľady[순번].Súbor_rukoväť=Súbor_rukoväť;return &Prehľady[순번];}chyba=24;return 0;}
int fflush(FILE*Súbor_položka){return Súbor_položka&&Súbor_položka->chyba?-1:0;}
int fclose(FILE*Súbor_položka){int 반환값=close(Súbor_položka->Súbor_rukoväť);if(Súbor_položka->chyba)반환값=-1;Súbor_položka->사용량=0;return 반환값;}
size_t fwrite(const void*údaje_pozícia,size_t reťazec_údaje,size_t položka_COUNT,FILE*Súbor_položka){if(!reťazec_údaje)return 0;if(položka_COUNT>SIZE_MAX/reťazec_údaje){Súbor_položka->chyba=1;return 0;}long 반환값=write(Súbor_položka->Súbor_rukoväť,údaje_pozícia,reťazec_údaje*položka_COUNT);if(반환값<0){Súbor_položka->chyba=1;return 0;}return (size_t)반환값/reťazec_údaje;}
int fputc(int bod_kódu,FILE*Súbor_položka){unsigned char SECOND_VALUE=bod_kódu;return fwrite(&SECOND_VALUE,1,1,Súbor_položka)==1?SECOND_VALUE:EOF;}
int fputs(const char*reťazec_údaje,FILE*Súbor_položka){return fwrite(reťazec_údaje,1,strlen(reťazec_údaje),Súbor_položka)==strlen(reťazec_údaje)?0:EOF;}
static void 넣기(char*KR_údaje,size_t 용량한도,size_t*v_termíne_splatnosti_pozícia,char bod_kódu){if(*v_termíne_splatnosti_pozícia+1<용량한도)KR_údaje[*v_termíne_splatnosti_pozícia]=bod_kódu;(*v_termíne_splatnosti_pozícia)++;}
int vsnprintf(char*KR_údaje,size_t 용량한도,const char*formát,va_list 가변인수){
    size_t v_termíne_splatnosti_pozícia=0;while(*formát){if(*formát!='%'){넣기(KR_údaje,용량한도,&v_termíne_splatnosti_pozícia,*formát++);continue;}formát++;
        int 왼쪽=0,영값=0,대체값=0;while(*formát=='-'||*formát=='0'||*formát=='#'||*formát=='+'||*formát==' '){if(*formát=='-')왼쪽=1;if(*formát=='0')영값=1;if(*formát=='#')대체값=1;formát++;}
        int 너비=0,presnosť_VALUE=-1;if(*formát=='*'){너비=va_arg(가변인수,int);formát++;}else while(*formát>='0'&&*formát<='9')너비=너비*10+*formát++-'0';
        if(*formát=='.'){formát++;presnosť_VALUE=0;if(*formát=='*'){presnosť_VALUE=va_arg(가변인수,int);formát++;}else while(*formát>='0'&&*formát<='9')presnosť_VALUE=presnosť_VALUE*10+*formát++-'0';}
        int 넓은글자=0;while(*formát=='l'||*formát=='z'||*formát=='t'||*formát=='j'||*formát=='h'){if(*formát!='h')넓은글자=1;formát++;}
        char Typ_oblasť=*formát?*formát++:0,ukladací_priestor_medzipamäte[80];const char*reťazec_údaje=ukladací_priestor_medzipamäte;size_t položka_COUNT=0;
        if(Typ_oblasť=='s'){reťazec_údaje=va_arg(가변인수,const char*);if(!reťazec_údaje)reťazec_údaje="(null)";položka_COUNT=strlen(reťazec_údaje);if(presnosť_VALUE>=0&&položka_COUNT>(size_t)presnosť_VALUE)položka_COUNT=presnosť_VALUE;}
        else if(Typ_oblasť=='c'){ukladací_priestor_medzipamäte[0]=va_arg(가변인수,int);položka_COUNT=1;}
        else if(Typ_oblasť=='%'){ukladací_priestor_medzipamäte[0]='%';položka_COUNT=1;}
        else if(Typ_oblasť=='d'||Typ_oblasť=='i'||Typ_oblasť=='u'||Typ_oblasť=='x'||Typ_oblasť=='X'||Typ_oblasť=='o'||Typ_oblasť=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(Typ_oblasť=='d'||Typ_oblasť=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=Typ_oblasť=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned tapeta_VALUE=Typ_oblasť=='x'||Typ_oblasť=='X'||Typ_oblasť=='p'?16:Typ_oblasť=='o'?8:10;char číslica_COUNT[64];unsigned 사용량=0;
            do{číslica_COUNT[사용량++]="0123456789abcdef"[VALUE%tapeta_VALUE];VALUE/=tapeta_VALUE;}while(VALUE);
            if(음수표시)ukladací_priestor_medzipamäte[položka_COUNT++]='-';if(Typ_oblasť=='p'||(대체값&&tapeta_VALUE==16)){ukladací_priestor_medzipamäte[položka_COUNT++]='0';ukladací_priestor_medzipamäte[položka_COUNT++]='x';}
            for(int výplň_VALUE=(int)사용량;presnosť_VALUE>výplň_VALUE&&položka_COUNT<sizeof(ukladací_priestor_medzipamäte)-사용량;výplň_VALUE++)ukladací_priestor_medzipamäte[položka_COUNT++]='0';
            if(영값&&!왼쪽&&presnosť_VALUE<0)while(너비>(int)(položka_COUNT+사용량)&&položka_COUNT<sizeof(ukladací_priestor_medzipamäte)-사용량)ukladací_priestor_medzipamäte[položka_COUNT++]='0';
            while(사용량)ukladací_priestor_medzipamäte[položka_COUNT++]=číslica_COUNT[--사용량];
        }else{ukladací_priestor_medzipamäte[0]='?';položka_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)položka_COUNT){넣기(KR_údaje,용량한도,&v_termíne_splatnosti_pozícia,' ');너비--;}
        for(size_t 순번=0;순번<položka_COUNT;순번++)넣기(KR_údaje,용량한도,&v_termíne_splatnosti_pozícia,reťazec_údaje[순번]);while(왼쪽&&너비>(int)položka_COUNT){넣기(KR_údaje,용량한도,&v_termíne_splatnosti_pozícia,' ');너비--;}
    }if(용량한도)KR_údaje[v_termíne_splatnosti_pozícia<용량한도?v_termíne_splatnosti_pozícia:용량한도-1]=0;return v_termíne_splatnosti_pozícia;
}
int snprintf(char*KR_údaje,size_t 용량한도,const char*Súbor_položka,...){va_list 첫째값;va_start(첫째값,Súbor_položka);int 반환값=vsnprintf(KR_údaje,용량한도,Súbor_položka,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_údaje,const char*Súbor_položka,...){va_list 첫째값;va_start(첫째값,Súbor_položka);int 반환값=vsnprintf(KR_údaje,SIZE_MAX,Súbor_položka,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*Súbor_položka,va_list 첫째값){char SECOND_VALUE[2048];int položka_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Súbor_položka,첫째값);if(položka_COUNT>2047)položka_COUNT=2047;return fwrite(SECOND_VALUE,1,položka_COUNT,Stream_VALUE)==(size_t)položka_COUNT?položka_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*Súbor_položka,...){va_list 첫째값;va_start(첫째값,Súbor_položka);int 반환값=vfprintf(Stream_VALUE,Súbor_položka,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Súbor_položka,...){va_list 첫째값;va_start(첫째값,Súbor_položka);int 반환값=vfprintf(stdout,Súbor_položka,첫째값);va_end(첫째값);return 반환값;}
