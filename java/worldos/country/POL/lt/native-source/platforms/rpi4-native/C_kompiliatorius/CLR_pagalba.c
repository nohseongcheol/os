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
static int KLAIDA;
int *__errno_location(void){return &KLAIDA;}
void exit(int Būsena_VALUE){사용자호출(6,Būsena_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *čekis_reiškinys,const char *Failas,unsigned Eilutė,const char *metodas_įrašas_pavadinimas){fprintf(stderr,"cc assertion: %s %s:%u %s\n",čekis_reiškinys,Failas,Eilutė,metodas_įrašas_pavadinimas);exit(1);}
size_t strlen(const char*eilutė_duomenys){const char*duomenys_padėtis=eilutė_duomenys;while(*duomenys_padėtis)duomenys_padėtis++;return duomenys_padėtis-eilutė_duomenys;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t prekė_COUNT){while(prekė_COUNT--){unsigned char x_koordinatė=*첫째값++,세로좌표=*SECOND_VALUE++;if(x_koordinatė!=세로좌표)return x_koordinatė-세로좌표;if(!x_koordinatė)return 0;}return 0;}
char *strcpy(char*vieta_duomenys,const char*eilutė_duomenys){char*반환값=vieta_duomenys;while((*vieta_duomenys++=*eilutė_duomenys++)){}return 반환값;}
char *strchr(const char*eilutė_duomenys,int simbolio_kodas){do{if(*eilutė_duomenys==(char)simbolio_kodas)return (char*)eilutė_duomenys;}while(*eilutė_duomenys++);return 0;}
char *strrchr(const char*eilutė_duomenys,int simbolio_kodas){const char*반환값=0;do{if(*eilutė_duomenys==(char)simbolio_kodas)반환값=eilutė_duomenys;}while(*eilutė_duomenys++);return (char*)반환값;}
char *strstr(const char*eilutė_duomenys,const char*Terminalas_įrašas){size_t prekė_COUNT=strlen(Terminalas_įrašas);for(;*eilutė_duomenys;eilutė_duomenys++)if(!strncmp(eilutė_duomenys,Terminalas_įrašas,prekė_COUNT))return (char*)eilutė_duomenys;return prekė_COUNT?0:(char*)eilutė_duomenys;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t prekė_COUNT){const unsigned char*x_koordinatė=첫째값,*세로좌표=SECOND_VALUE;while(prekė_COUNT--){if(*x_koordinatė!=*세로좌표)return *x_koordinatė-*세로좌표;x_koordinatė++;세로좌표++;}return 0;}
void *memmove(void*vieta_duomenys,const void*eilutė_duomenys,size_t prekė_COUNT){unsigned char*x_koordinatė=vieta_duomenys;const unsigned char*세로좌표=eilutė_duomenys;if(x_koordinatė<세로좌표){for(size_t 순번=0;순번<prekė_COUNT;순번++)x_koordinatė[순번]=세로좌표[순번];}else while(prekė_COUNT){prekė_COUNT--;x_koordinatė[prekė_COUNT]=세로좌표[prekė_COUNT];}return vieta_duomenys;}
static unsigned char priskyrimas_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct duomenų_blokas {size_t Dydis;struct duomenų_blokas*toliau_prekė;int 남은공간;int užpildymas;uint64_t lygiuotė_pamoka;} duomenų_blokas;
static duomenų_blokas *첫항목;
void free(void*duomenys_padėtis){if(!duomenys_padėtis)return;duomenų_blokas*SECOND_VALUE=(duomenų_blokas*)duomenys_padėtis-1;SECOND_VALUE->남은공간=1;for(duomenų_blokas*toliau_OFFSET=첫항목;toliau_OFFSET&&toliau_OFFSET->toliau_prekė;){if(toliau_OFFSET->남은공간&&toliau_OFFSET->toliau_prekė->남은공간){toliau_OFFSET->Dydis+=sizeof(duomenų_blokas)+toliau_OFFSET->toliau_prekė->Dydis;toliau_OFFSET->toliau_prekė=toliau_OFFSET->toliau_prekė->toliau_prekė;}else toliau_OFFSET=toliau_OFFSET->toliau_prekė;}}
void *realloc(void*duomenys_padėtis,size_t prekė_COUNT){
    if(!prekė_COUNT){free(duomenys_padėtis);return 0;}if(prekė_COUNT>sizeof(priskyrimas_Arena)-sizeof(duomenų_blokas))return 0;prekė_COUNT=(prekė_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(duomenų_blokas*)priskyrimas_Arena;첫항목->Dydis=sizeof(priskyrimas_Arena)-sizeof(duomenų_blokas);첫항목->남은공간=1;첫항목->toliau_prekė=0;}
    duomenų_blokas*이전=duomenys_padėtis?(duomenų_blokas*)duomenys_padėtis-1:0;if(이전&&이전->Dydis>=prekė_COUNT)return duomenys_padėtis;
    for(duomenų_blokas*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->toliau_prekė)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Dydis>=prekė_COUNT){
        if(SECOND_VALUE->Dydis>=prekė_COUNT+sizeof(duomenų_blokas)+16){duomenų_blokas*나머지부분=(duomenų_blokas*)((unsigned char*)(SECOND_VALUE+1)+prekė_COUNT);나머지부분->Dydis=SECOND_VALUE->Dydis-prekė_COUNT-sizeof(duomenų_blokas);나머지부분->toliau_prekė=SECOND_VALUE->toliau_prekė;나머지부분->남은공간=1;SECOND_VALUE->toliau_prekė=나머지부분;SECOND_VALUE->Dydis=prekė_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,duomenys_padėtis,이전->Dydis);free(duomenys_padėtis);}return 반환값;
    }KLAIDA=12;return 0;
}
void *malloc(size_t prekė_COUNT){return realloc(0,prekė_COUNT);}
void *calloc(size_t prekė_COUNT,size_t eilutė_duomenys){if(eilutė_duomenys&&prekė_COUNT>SIZE_MAX/eilutė_duomenys)return 0;void*duomenys_padėtis=malloc(prekė_COUNT*eilutė_duomenys);if(duomenys_padėtis)memset(duomenys_padėtis,0,prekė_COUNT*eilutė_duomenys);return duomenys_padėtis;}
unsigned long long strtoull(const char*eilutė_duomenys,char**baigti_pokalbį_OFFSET,int Fonas_VALUE){
    const char*Start_OFFSET=eilutė_duomenys;while(*eilutė_duomenys==' '||(*eilutė_duomenys>=9&&*eilutė_duomenys<=13))eilutė_duomenys++;int 음수여부=0;if(*eilutė_duomenys=='-'||*eilutė_duomenys=='+')음수여부=*eilutė_duomenys++=='-';
    if((!Fonas_VALUE||Fonas_VALUE==16)&&eilutė_duomenys[0]=='0'&&(eilutė_duomenys[1]=='x'||eilutė_duomenys[1]=='X')){Fonas_VALUE=16;eilutė_duomenys+=2;}if(!Fonas_VALUE)Fonas_VALUE=*eilutė_duomenys=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned simbolio_kodas=*eilutė_duomenys,vieta_duomenys=simbolio_kodas>='0'&&simbolio_kodas<='9'?simbolio_kodas-'0':simbolio_kodas>='a'&&simbolio_kodas<='z'?simbolio_kodas-'a'+10:simbolio_kodas>='A'&&simbolio_kodas<='Z'?simbolio_kodas-'A'+10:99;if(vieta_duomenys>=(unsigned)Fonas_VALUE)break;하나라도=1;eilutė_duomenys++;if(임시값>(~0ull-vieta_duomenys)/(unsigned)Fonas_VALUE){임시값=~0ull;KLAIDA=34;}else 임시값=임시값*Fonas_VALUE+vieta_duomenys;}
    if(baigti_pokalbį_OFFSET)*baigti_pokalbį_OFFSET=(char*)(하나라도?eilutė_duomenys:Start_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*eilutė_duomenys,char**보조항목,int SECOND_VALUE){return strtoull(eilutė_duomenys,보조항목,SECOND_VALUE);}
long strtol(const char*eilutė_duomenys,char**보조항목,int SECOND_VALUE){return (long)strtoull(eilutė_duomenys,보조항목,SECOND_VALUE);}
int atoi(const char*eilutė_duomenys){return (int)strtol(eilutė_duomenys,0,10);}
long double ldexpl(long double x_koordinatė,int prekė_COUNT){while(prekė_COUNT>0){x_koordinatė*=2;prekė_COUNT--;}while(prekė_COUNT<0){x_koordinatė/=2;prekė_COUNT++;}return x_koordinatė;}
long double strtold(const char*eilutė_duomenys,char**baigti_pokalbį_OFFSET){
    const char*Start_OFFSET=eilutė_duomenys;while(*eilutė_duomenys==' '||(*eilutė_duomenys>=9&&*eilutė_duomenys<=13))eilutė_duomenys++;int 음수여부=0;if(*eilutė_duomenys=='-'||*eilutė_duomenys=='+')음수여부=*eilutė_duomenys++=='-';
    int Fonas_VALUE=10;if(eilutė_duomenys[0]=='0'&&(eilutė_duomenys[1]=='x'||eilutė_duomenys[1]=='X')){Fonas_VALUE=16;eilutė_duomenys+=2;}long double 임시값=0,keisti_kiekį=1;int 소수부=0,하나라도=0;
    for(;;){int simbolio_kodas=*eilutė_duomenys,vieta_duomenys=simbolio_kodas>='0'&&simbolio_kodas<='9'?simbolio_kodas-'0':simbolio_kodas>='a'&&simbolio_kodas<='f'?simbolio_kodas-'a'+10:simbolio_kodas>='A'&&simbolio_kodas<='F'?simbolio_kodas-'A'+10:99;
        if(simbolio_kodas=='.'&&!소수부){소수부=1;eilutė_duomenys++;continue;}if(vieta_duomenys>=Fonas_VALUE)break;하나라도=1;eilutė_duomenys++;임시값=임시값*Fonas_VALUE+vieta_duomenys;if(소수부)keisti_kiekį*=Fonas_VALUE;
    }임시값/=keisti_kiekį;
    if((Fonas_VALUE==10&&(*eilutė_duomenys=='e'||*eilutė_duomenys=='E'))||(Fonas_VALUE==16&&(*eilutė_duomenys=='p'||*eilutė_duomenys=='P'))){const char*laida_VALUE=eilutė_duomenys++;int 빼기=0;if(*eilutė_duomenys=='-'||*eilutė_duomenys=='+')빼기=*eilutė_duomenys++=='-';int prekė_COUNT=0,įrašas_COUNT=0;while(*eilutė_duomenys>='0'&&*eilutė_duomenys<='9'){įrašas_COUNT++;if(prekė_COUNT<20000)prekė_COUNT=prekė_COUNT*10+*eilutė_duomenys-'0';eilutė_duomenys++;}if(!įrašas_COUNT)eilutė_duomenys=laida_VALUE;else{long double daugiklis=Fonas_VALUE==16?2:10;while(prekė_COUNT-->0&&prekė_COUNT<200000)임시값=빼기?임시값/daugiklis:임시값*daugiklis;}}
    if(baigti_pokalbį_OFFSET)*baigti_pokalbį_OFFSET=(char*)(하나라도?eilutė_duomenys:Start_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*eilutė_duomenys,char**보조항목){return (double)strtold(eilutė_duomenys,보조항목);}float strtof(const char*eilutė_duomenys,char**보조항목){return (float)strtold(eilutė_duomenys,보조항목);}
void qsort(void*Fonas_VALUE,size_t prekė_COUNT,size_t Dydis,int(*Palyginti)(const void*,const void*)){
    unsigned char*duomenys_padėtis=Fonas_VALUE;for(size_t 순번=1;순번<prekė_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Palyginti(duomenys_padėtis+(안쪽순번-1)*Dydis,duomenys_padėtis+안쪽순번*Dydis)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Dydis;셋째순번++){unsigned char simbolio_kodas=duomenys_padėtis[(안쪽순번-1)*Dydis+셋째순번];duomenys_padėtis[(안쪽순번-1)*Dydis+셋째순번]=duomenys_padėtis[안쪽순번*Dydis+셋째순번];duomenys_padėtis[안쪽순번*Dydis+셋째순번]=simbolio_kodas;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Pozicija;} 열림[24];
static unsigned char išeiga[32768];static size_t išeiga_dydis,išeiga_padėtis;static int išeiga_kurti;
const unsigned char *C_išeiga(size_t *prekė_COUNT){*prekė_COUNT=išeiga_dydis;return išeiga;}
int open(const char*Pavadinimas_2,int konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba,...){
    if(!strcmp(Pavadinimas_2,"/@cc-output")){if(išeiga_kurti){KLAIDA=16;return -1;}išeiga_kurti=1;išeiga_dydis=išeiga_padėtis=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompiliatorius_Ištekliai)/sizeof(kompiliatorius_Ištekliai[0]);순번++)if(!strcmp(Pavadinimas_2,kompiliatorius_Ištekliai[순번].Pavadinimas_2)){
        if(konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba&3){KLAIDA=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Pozicija=0;return 128+안쪽순번;}KLAIDA=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Pavadinimas_2,konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba,0,0,0,0);if(반환값<0){KLAIDA=-반환값;return -1;}return 반환값;
}
int close(int Failas_rodyklė){if(Failas_rodyklė==100){išeiga_kurti=0;return 0;}if(Failas_rodyklė>=128&&Failas_rodyklė<152){열림[Failas_rodyklė-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Failas_rodyklė,0,0,0,0,0);if(반환값<0){KLAIDA=-반환값;return -1;}return 0;}
long read(int Failas_rodyklė,void*duomenys,size_t prekė_COUNT){
    if(Failas_rodyklė>=128&&Failas_rodyklė<152&&열림[Failas_rodyklė-128].사용량){int 순번=Failas_rodyklė-128;const kompiliatorius_ištekliai*반환값=&kompiliatorius_Ištekliai[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Dydis-열림[순번].Pozicija;if(prekė_COUNT>왼쪽)prekė_COUNT=왼쪽;memcpy(duomenys,반환값->duomenys+열림[순번].Pozicija,prekė_COUNT);열림[순번].Pozicija+=prekė_COUNT;return prekė_COUNT;}
    intptr_t 반환값=사용자호출(2,Failas_rodyklė,(uintptr_t)duomenys,prekė_COUNT,0,0,0);if(반환값<0){KLAIDA=-반환값;return -1;}return 반환값;
}
long write(int Failas_rodyklė,const void*duomenys,size_t prekė_COUNT){
    if(Failas_rodyklė==100){if(prekė_COUNT>sizeof(išeiga)-išeiga_padėtis){KLAIDA=28;return -1;}memcpy(išeiga+išeiga_padėtis,duomenys,prekė_COUNT);išeiga_padėtis+=prekė_COUNT;if(išeiga_dydis<išeiga_padėtis)išeiga_dydis=išeiga_padėtis;return prekė_COUNT;}
    intptr_t 반환값=사용자호출(1,Failas_rodyklė,(uintptr_t)duomenys,prekė_COUNT,0,0,0);if(반환값<0){KLAIDA=-반환값;return -1;}return 반환값;
}
long lseek(int Failas_rodyklė,long OFFSET_VALUE,int 기준점){
    if(Failas_rodyklė==100){long duomenys_padėtis=OFFSET_VALUE+(기준점==0?0:기준점==1?išeiga_padėtis:išeiga_dydis);if(duomenys_padėtis<0||(size_t)duomenys_padėtis>sizeof(išeiga)){KLAIDA=22;return -1;}išeiga_padėtis=duomenys_padėtis;return duomenys_padėtis;}
    if(Failas_rodyklė>=128&&Failas_rodyklė<152&&열림[Failas_rodyklė-128].사용량){int 순번=Failas_rodyklė-128;long duomenys_padėtis=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].Pozicija:kompiliatorius_Ištekliai[열림[순번].LOOKUP_INDEX].Dydis);if(duomenys_padėtis<0||(size_t)duomenys_padėtis>kompiliatorius_Ištekliai[열림[순번].LOOKUP_INDEX].Dydis){KLAIDA=22;return -1;}열림[순번].Pozicija=duomenys_padėtis;return duomenys_padėtis;}
    intptr_t 반환값=사용자호출(5,Failas_rodyklė,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){KLAIDA=-반환값;return -1;}return 반환값;
}
int unlink(const char*Pavadinimas_2){intptr_t 반환값=사용자호출(11,(uintptr_t)Pavadinimas_2,0,0,0,0,0);if(반환값<0){KLAIDA=-반환값;return -1;}return 반환값;}
char *realpath(const char*Pavadinimas_2,char*KR_duomenys){if(!KR_duomenys){KR_duomenys=malloc(strlen(Pavadinimas_2)+1);if(!KR_duomenys)return 0;}return strcpy(KR_duomenys,Pavadinimas_2);}
char *getcwd(char*duomenys_padėtis,size_t prekė_COUNT){if(prekė_COUNT<2){KLAIDA=34;return 0;}duomenys_padėtis[0]='/';duomenys_padėtis[1]=0;return duomenys_padėtis;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminalas_įrašas){time_t 임시값=0;if(Terminalas_įrašas)*Terminalas_įrašas=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminalas_įrašas){(void)Terminalas_įrašas;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE srautai[18]={{1,0,1},{2,0,1}};FILE*stdout=&srautai[0],*stderr=&srautai[1];
FILE*fdopen(int Failas_rodyklė,const char*metodas_MODE){(void)metodas_MODE;for(unsigned 순번=2;순번<18;순번++)if(!srautai[순번].사용량){srautai[순번].사용량=1;srautai[순번].KLAIDA=0;srautai[순번].Failas_rodyklė=Failas_rodyklė;return &srautai[순번];}KLAIDA=24;return 0;}
int fflush(FILE*Failas_įrašas){return Failas_įrašas&&Failas_įrašas->KLAIDA?-1:0;}
int fclose(FILE*Failas_įrašas){int 반환값=close(Failas_įrašas->Failas_rodyklė);if(Failas_įrašas->KLAIDA)반환값=-1;Failas_įrašas->사용량=0;return 반환값;}
size_t fwrite(const void*duomenys_padėtis,size_t eilutė_duomenys,size_t prekė_COUNT,FILE*Failas_įrašas){if(!eilutė_duomenys)return 0;if(prekė_COUNT>SIZE_MAX/eilutė_duomenys){Failas_įrašas->KLAIDA=1;return 0;}long 반환값=write(Failas_įrašas->Failas_rodyklė,duomenys_padėtis,eilutė_duomenys*prekė_COUNT);if(반환값<0){Failas_įrašas->KLAIDA=1;return 0;}return (size_t)반환값/eilutė_duomenys;}
int fputc(int simbolio_kodas,FILE*Failas_įrašas){unsigned char SECOND_VALUE=simbolio_kodas;return fwrite(&SECOND_VALUE,1,1,Failas_įrašas)==1?SECOND_VALUE:EOF;}
int fputs(const char*eilutė_duomenys,FILE*Failas_įrašas){return fwrite(eilutė_duomenys,1,strlen(eilutė_duomenys),Failas_įrašas)==strlen(eilutė_duomenys)?0:EOF;}
static void 넣기(char*KR_duomenys,size_t 용량한도,size_t*dabartinis_padėtis,char simbolio_kodas){if(*dabartinis_padėtis+1<용량한도)KR_duomenys[*dabartinis_padėtis]=simbolio_kodas;(*dabartinis_padėtis)++;}
int vsnprintf(char*KR_duomenys,size_t 용량한도,const char*formatas,va_list 가변인수){
    size_t dabartinis_padėtis=0;while(*formatas){if(*formatas!='%'){넣기(KR_duomenys,용량한도,&dabartinis_padėtis,*formatas++);continue;}formatas++;
        int 왼쪽=0,nulis_VALUE=0,대체값=0;while(*formatas=='-'||*formatas=='0'||*formatas=='#'||*formatas=='+'||*formatas==' '){if(*formatas=='-')왼쪽=1;if(*formatas=='0')nulis_VALUE=1;if(*formatas=='#')대체값=1;formatas++;}
        int 너비=0,tikslumas_VALUE=-1;if(*formatas=='*'){너비=va_arg(가변인수,int);formatas++;}else while(*formatas>='0'&&*formatas<='9')너비=너비*10+*formatas++-'0';
        if(*formatas=='.'){formatas++;tikslumas_VALUE=0;if(*formatas=='*'){tikslumas_VALUE=va_arg(가변인수,int);formatas++;}else while(*formatas>='0'&&*formatas<='9')tikslumas_VALUE=tikslumas_VALUE*10+*formatas++-'0';}
        int platusis_simbolis=0;while(*formatas=='l'||*formatas=='z'||*formatas=='t'||*formatas=='j'||*formatas=='h'){if(*formatas!='h')platusis_simbolis=1;formatas++;}
        char TYPE_sritis=*formatas?*formatas++:0,buferio_saugykla[80];const char*eilutė_duomenys=buferio_saugykla;size_t prekė_COUNT=0;
        if(TYPE_sritis=='s'){eilutė_duomenys=va_arg(가변인수,const char*);if(!eilutė_duomenys)eilutė_duomenys="(null)";prekė_COUNT=strlen(eilutė_duomenys);if(tikslumas_VALUE>=0&&prekė_COUNT>(size_t)tikslumas_VALUE)prekė_COUNT=tikslumas_VALUE;}
        else if(TYPE_sritis=='c'){buferio_saugykla[0]=va_arg(가변인수,int);prekė_COUNT=1;}
        else if(TYPE_sritis=='%'){buferio_saugykla[0]='%';prekė_COUNT=1;}
        else if(TYPE_sritis=='d'||TYPE_sritis=='i'||TYPE_sritis=='u'||TYPE_sritis=='x'||TYPE_sritis=='X'||TYPE_sritis=='o'||TYPE_sritis=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_sritis=='d'||TYPE_sritis=='i'){long long 임시값=platusis_simbolis?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_sritis=='p'?(uintptr_t)va_arg(가변인수,void*):platusis_simbolis?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Fonas_VALUE=TYPE_sritis=='x'||TYPE_sritis=='X'||TYPE_sritis=='p'?16:TYPE_sritis=='o'?8:10;char skaitmuo_COUNT[64];unsigned 사용량=0;
            do{skaitmuo_COUNT[사용량++]="0123456789abcdef"[VALUE%Fonas_VALUE];VALUE/=Fonas_VALUE;}while(VALUE);
            if(음수표시)buferio_saugykla[prekė_COUNT++]='-';if(TYPE_sritis=='p'||(대체값&&Fonas_VALUE==16)){buferio_saugykla[prekė_COUNT++]='0';buferio_saugykla[prekė_COUNT++]='x';}
            for(int užpildas_VALUE=(int)사용량;tikslumas_VALUE>užpildas_VALUE&&prekė_COUNT<sizeof(buferio_saugykla)-사용량;užpildas_VALUE++)buferio_saugykla[prekė_COUNT++]='0';
            if(nulis_VALUE&&!왼쪽&&tikslumas_VALUE<0)while(너비>(int)(prekė_COUNT+사용량)&&prekė_COUNT<sizeof(buferio_saugykla)-사용량)buferio_saugykla[prekė_COUNT++]='0';
            while(사용량)buferio_saugykla[prekė_COUNT++]=skaitmuo_COUNT[--사용량];
        }else{buferio_saugykla[0]='?';prekė_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)prekė_COUNT){넣기(KR_duomenys,용량한도,&dabartinis_padėtis,' ');너비--;}
        for(size_t 순번=0;순번<prekė_COUNT;순번++)넣기(KR_duomenys,용량한도,&dabartinis_padėtis,eilutė_duomenys[순번]);while(왼쪽&&너비>(int)prekė_COUNT){넣기(KR_duomenys,용량한도,&dabartinis_padėtis,' ');너비--;}
    }if(용량한도)KR_duomenys[dabartinis_padėtis<용량한도?dabartinis_padėtis:용량한도-1]=0;return dabartinis_padėtis;
}
int snprintf(char*KR_duomenys,size_t 용량한도,const char*Failas_įrašas,...){va_list 첫째값;va_start(첫째값,Failas_įrašas);int 반환값=vsnprintf(KR_duomenys,용량한도,Failas_įrašas,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_duomenys,const char*Failas_įrašas,...){va_list 첫째값;va_start(첫째값,Failas_įrašas);int 반환값=vsnprintf(KR_duomenys,SIZE_MAX,Failas_įrašas,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*Failas_įrašas,va_list 첫째값){char SECOND_VALUE[2048];int prekė_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Failas_įrašas,첫째값);if(prekė_COUNT>2047)prekė_COUNT=2047;return fwrite(SECOND_VALUE,1,prekė_COUNT,Stream_VALUE)==(size_t)prekė_COUNT?prekė_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*Failas_įrašas,...){va_list 첫째값;va_start(첫째값,Failas_įrašas);int 반환값=vfprintf(Stream_VALUE,Failas_įrašas,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Failas_įrašas,...){va_list 첫째값;va_start(첫째값,Failas_įrašas);int 반환값=vfprintf(stdout,Failas_įrašas,첫째값);va_end(첫째값);return 반환값;}
