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
static int eroare;
int *__errno_location(void){return &eroare;}
void exit(int Stare_VALUE){사용자호출(6,Stare_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *verifica_expresie,const char *Fișier,unsigned Linie,const char *metodă_intrare_nume){fprintf(stderr,"cc assertion: %s %s:%u %s\n",verifica_expresie,Fișier,Linie,metodă_intrare_nume);exit(1);}
size_t strlen(const char*șir_date){const char*date_poziție=șir_date;while(*date_poziție)date_poziție++;return date_poziție-șir_date;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t element_COUNT){while(element_COUNT--){unsigned char coordonata_X=*첫째값++,세로좌표=*SECOND_VALUE++;if(coordonata_X!=세로좌표)return coordonata_X-세로좌표;if(!coordonata_X)return 0;}return 0;}
char *strcpy(char*destinație_date,const char*șir_date){char*반환값=destinație_date;while((*destinație_date++=*șir_date++)){}return 반환값;}
char *strchr(const char*șir_date,int cod_caracter){do{if(*șir_date==(char)cod_caracter)return (char*)șir_date;}while(*șir_date++);return 0;}
char *strrchr(const char*șir_date,int cod_caracter){const char*반환값=0;do{if(*șir_date==(char)cod_caracter)반환값=șir_date;}while(*șir_date++);return (char*)반환값;}
char *strstr(const char*șir_date,const char*Terminal_intrare){size_t element_COUNT=strlen(Terminal_intrare);for(;*șir_date;șir_date++)if(!strncmp(șir_date,Terminal_intrare,element_COUNT))return (char*)șir_date;return element_COUNT?0:(char*)șir_date;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t element_COUNT){const unsigned char*coordonata_X=첫째값,*세로좌표=SECOND_VALUE;while(element_COUNT--){if(*coordonata_X!=*세로좌표)return *coordonata_X-*세로좌표;coordonata_X++;세로좌표++;}return 0;}
void *memmove(void*destinație_date,const void*șir_date,size_t element_COUNT){unsigned char*coordonata_X=destinație_date;const unsigned char*세로좌표=șir_date;if(coordonata_X<세로좌표){for(size_t 순번=0;순번<element_COUNT;순번++)coordonata_X[순번]=세로좌표[순번];}else while(element_COUNT){element_COUNT--;coordonata_X[element_COUNT]=세로좌표[element_COUNT];}return destinație_date;}
static unsigned char alocare_Arenă[6*1024*1024] __attribute__((aligned(16)));
typedef struct bloc_de_date {size_t Mărime;struct bloc_de_date*Următorul_element;int 남은공간;int completare;uint64_t aliniere_lecție;} bloc_de_date;
static bloc_de_date *첫항목;
void free(void*date_poziție){if(!date_poziție)return;bloc_de_date*SECOND_VALUE=(bloc_de_date*)date_poziție-1;SECOND_VALUE->남은공간=1;for(bloc_de_date*Următorul_OFFSET=첫항목;Următorul_OFFSET&&Următorul_OFFSET->Următorul_element;){if(Următorul_OFFSET->남은공간&&Următorul_OFFSET->Următorul_element->남은공간){Următorul_OFFSET->Mărime+=sizeof(bloc_de_date)+Următorul_OFFSET->Următorul_element->Mărime;Următorul_OFFSET->Următorul_element=Următorul_OFFSET->Următorul_element->Următorul_element;}else Următorul_OFFSET=Următorul_OFFSET->Următorul_element;}}
void *realloc(void*date_poziție,size_t element_COUNT){
    if(!element_COUNT){free(date_poziție);return 0;}if(element_COUNT>sizeof(alocare_Arenă)-sizeof(bloc_de_date))return 0;element_COUNT=(element_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(bloc_de_date*)alocare_Arenă;첫항목->Mărime=sizeof(alocare_Arenă)-sizeof(bloc_de_date);첫항목->남은공간=1;첫항목->Următorul_element=0;}
    bloc_de_date*Anteriorul_element=date_poziție?(bloc_de_date*)date_poziție-1:0;if(Anteriorul_element&&Anteriorul_element->Mărime>=element_COUNT)return date_poziție;
    for(bloc_de_date*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Următorul_element)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Mărime>=element_COUNT){
        if(SECOND_VALUE->Mărime>=element_COUNT+sizeof(bloc_de_date)+16){bloc_de_date*나머지부분=(bloc_de_date*)((unsigned char*)(SECOND_VALUE+1)+element_COUNT);나머지부분->Mărime=SECOND_VALUE->Mărime-element_COUNT-sizeof(bloc_de_date);나머지부분->Următorul_element=SECOND_VALUE->Următorul_element;나머지부분->남은공간=1;SECOND_VALUE->Următorul_element=나머지부분;SECOND_VALUE->Mărime=element_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(Anteriorul_element){memcpy(반환값,date_poziție,Anteriorul_element->Mărime);free(date_poziție);}return 반환값;
    }eroare=12;return 0;
}
void *malloc(size_t element_COUNT){return realloc(0,element_COUNT);}
void *calloc(size_t element_COUNT,size_t șir_date){if(șir_date&&element_COUNT>SIZE_MAX/șir_date)return 0;void*date_poziție=malloc(element_COUNT*șir_date);if(date_poziție)memset(date_poziție,0,element_COUNT*șir_date);return date_poziție;}
unsigned long long strtoull(const char*șir_date,char**termina_un_apel_OFFSET,int tapet_VALUE){
    const char*buta_OFFSET=șir_date;while(*șir_date==' '||(*șir_date>=9&&*șir_date<=13))șir_date++;int 음수여부=0;if(*șir_date=='-'||*șir_date=='+')음수여부=*șir_date++=='-';
    if((!tapet_VALUE||tapet_VALUE==16)&&șir_date[0]=='0'&&(șir_date[1]=='x'||șir_date[1]=='X')){tapet_VALUE=16;șir_date+=2;}if(!tapet_VALUE)tapet_VALUE=*șir_date=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned cod_caracter=*șir_date,destinație_date=cod_caracter>='0'&&cod_caracter<='9'?cod_caracter-'0':cod_caracter>='a'&&cod_caracter<='z'?cod_caracter-'a'+10:cod_caracter>='A'&&cod_caracter<='Z'?cod_caracter-'A'+10:99;if(destinație_date>=(unsigned)tapet_VALUE)break;하나라도=1;șir_date++;if(임시값>(~0ull-destinație_date)/(unsigned)tapet_VALUE){임시값=~0ull;eroare=34;}else 임시값=임시값*tapet_VALUE+destinație_date;}
    if(termina_un_apel_OFFSET)*termina_un_apel_OFFSET=(char*)(하나라도?șir_date:buta_OFFSET);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*șir_date,char**보조항목,int SECOND_VALUE){return strtoull(șir_date,보조항목,SECOND_VALUE);}
long strtol(const char*șir_date,char**보조항목,int SECOND_VALUE){return (long)strtoull(șir_date,보조항목,SECOND_VALUE);}
int atoi(const char*șir_date){return (int)strtol(șir_date,0,10);}
long double ldexpl(long double coordonata_X,int element_COUNT){while(element_COUNT>0){coordonata_X*=2;element_COUNT--;}while(element_COUNT<0){coordonata_X/=2;element_COUNT++;}return coordonata_X;}
long double strtold(const char*șir_date,char**termina_un_apel_OFFSET){
    const char*buta_OFFSET=șir_date;while(*șir_date==' '||(*șir_date>=9&&*șir_date<=13))șir_date++;int 음수여부=0;if(*șir_date=='-'||*șir_date=='+')음수여부=*șir_date++=='-';
    int tapet_VALUE=10;if(șir_date[0]=='0'&&(șir_date[1]=='x'||șir_date[1]=='X')){tapet_VALUE=16;șir_date+=2;}long double 임시값=0,scala=1;int 소수부=0,하나라도=0;
    for(;;){int cod_caracter=*șir_date,destinație_date=cod_caracter>='0'&&cod_caracter<='9'?cod_caracter-'0':cod_caracter>='a'&&cod_caracter<='f'?cod_caracter-'a'+10:cod_caracter>='A'&&cod_caracter<='F'?cod_caracter-'A'+10:99;
        if(cod_caracter=='.'&&!소수부){소수부=1;șir_date++;continue;}if(destinație_date>=tapet_VALUE)break;하나라도=1;șir_date++;임시값=임시값*tapet_VALUE+destinație_date;if(소수부)scala*=tapet_VALUE;
    }임시값/=scala;
    if((tapet_VALUE==10&&(*șir_date=='e'||*șir_date=='E'))||(tapet_VALUE==16&&(*șir_date=='p'||*șir_date=='P'))){const char*afișa_VALUE=șir_date++;int 빼기=0;if(*șir_date=='-'||*șir_date=='+')빼기=*șir_date++=='-';int element_COUNT=0,intrare_COUNT=0;while(*șir_date>='0'&&*șir_date<='9'){intrare_COUNT++;if(element_COUNT<20000)element_COUNT=element_COUNT*10+*șir_date-'0';șir_date++;}if(!intrare_COUNT)șir_date=afișa_VALUE;else{long double factor=tapet_VALUE==16?2:10;while(element_COUNT-->0&&element_COUNT<200000)임시값=빼기?임시값/factor:임시값*factor;}}
    if(termina_un_apel_OFFSET)*termina_un_apel_OFFSET=(char*)(하나라도?șir_date:buta_OFFSET);return 음수여부?-임시값:임시값;
}
double strtod(const char*șir_date,char**보조항목){return (double)strtold(șir_date,보조항목);}float strtof(const char*șir_date,char**보조항목){return (float)strtold(șir_date,보조항목);}
void qsort(void*tapet_VALUE,size_t element_COUNT,size_t Mărime,int(*compara)(const void*,const void*)){
    unsigned char*date_poziție=tapet_VALUE;for(size_t 순번=1;순번<element_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&compara(date_poziție+(안쪽순번-1)*Mărime,date_poziție+안쪽순번*Mărime)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Mărime;셋째순번++){unsigned char cod_caracter=date_poziție[(안쪽순번-1)*Mărime+셋째순번];date_poziție[(안쪽순번-1)*Mărime+셋째순번]=date_poziție[안쪽순번*Mărime+셋째순번];date_poziție[안쪽순번*Mărime+셋째순번]=cod_caracter;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Poziție;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *element_COUNT){*element_COUNT=출력크기;return 출력결과;}
int open(const char*Nume,int configurație_Serviciu_de_transfer_inteligent_în_fundal,...){
    if(!strcmp(Nume,"/@cc-output")){if(출력열림){eroare=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(compilator_Resurse)/sizeof(compilator_Resurse[0]);순번++)if(!strcmp(Nume,compilator_Resurse[순번].Nume)){
        if(configurație_Serviciu_de_transfer_inteligent_în_fundal&3){eroare=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Poziție=0;return 128+안쪽순번;}eroare=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nume,configurație_Serviciu_de_transfer_inteligent_în_fundal,0,0,0,0);if(반환값<0){eroare=-반환값;return -1;}return 반환값;
}
int close(int Fișier_handle){if(Fișier_handle==100){출력열림=0;return 0;}if(Fișier_handle>=128&&Fișier_handle<152){열림[Fișier_handle-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Fișier_handle,0,0,0,0,0);if(반환값<0){eroare=-반환값;return -1;}return 0;}
long read(int Fișier_handle,void*date,size_t element_COUNT){
    if(Fișier_handle>=128&&Fișier_handle<152&&열림[Fișier_handle-128].사용량){int 순번=Fișier_handle-128;const compilator_resursă*반환값=&compilator_Resurse[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Mărime-열림[순번].Poziție;if(element_COUNT>왼쪽)element_COUNT=왼쪽;memcpy(date,반환값->date+열림[순번].Poziție,element_COUNT);열림[순번].Poziție+=element_COUNT;return element_COUNT;}
    intptr_t 반환값=사용자호출(2,Fișier_handle,(uintptr_t)date,element_COUNT,0,0,0);if(반환값<0){eroare=-반환값;return -1;}return 반환값;
}
long write(int Fișier_handle,const void*date,size_t element_COUNT){
    if(Fișier_handle==100){if(element_COUNT>sizeof(출력결과)-출력위치){eroare=28;return -1;}memcpy(출력결과+출력위치,date,element_COUNT);출력위치+=element_COUNT;if(출력크기<출력위치)출력크기=출력위치;return element_COUNT;}
    intptr_t 반환값=사용자호출(1,Fișier_handle,(uintptr_t)date,element_COUNT,0,0,0);if(반환값<0){eroare=-반환값;return -1;}return 반환값;
}
long lseek(int Fișier_handle,long OFFSET_VALUE,int 기준점){
    if(Fișier_handle==100){long date_poziție=OFFSET_VALUE+(기준점==0?0:기준점==1?출력위치:출력크기);if(date_poziție<0||(size_t)date_poziție>sizeof(출력결과)){eroare=22;return -1;}출력위치=date_poziție;return date_poziție;}
    if(Fișier_handle>=128&&Fișier_handle<152&&열림[Fișier_handle-128].사용량){int 순번=Fișier_handle-128;long date_poziție=OFFSET_VALUE+(기준점==0?0:기준점==1?열림[순번].Poziție:compilator_Resurse[열림[순번].LOOKUP_INDEX].Mărime);if(date_poziție<0||(size_t)date_poziție>compilator_Resurse[열림[순번].LOOKUP_INDEX].Mărime){eroare=22;return -1;}열림[순번].Poziție=date_poziție;return date_poziție;}
    intptr_t 반환값=사용자호출(5,Fișier_handle,OFFSET_VALUE,기준점,0,0,0);if(반환값<0){eroare=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nume){intptr_t 반환값=사용자호출(11,(uintptr_t)Nume,0,0,0,0,0);if(반환값<0){eroare=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nume,char*KR_date){if(!KR_date){KR_date=malloc(strlen(Nume)+1);if(!KR_date)return 0;}return strcpy(KR_date,Nume);}
char *getcwd(char*date_poziție,size_t element_COUNT){if(element_COUNT<2){eroare=34;return 0;}date_poziție[0]='/';date_poziție[1]=0;return date_poziție;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_intrare){time_t 임시값=0;if(Terminal_intrare)*Terminal_intrare=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_intrare){(void)Terminal_intrare;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Fluxuri[18]={{1,0,1},{2,0,1}};FILE*stdout=&Fluxuri[0],*stderr=&Fluxuri[1];
FILE*fdopen(int Fișier_handle,const char*metodă_mod){(void)metodă_mod;for(unsigned 순번=2;순번<18;순번++)if(!Fluxuri[순번].사용량){Fluxuri[순번].사용량=1;Fluxuri[순번].eroare=0;Fluxuri[순번].Fișier_handle=Fișier_handle;return &Fluxuri[순번];}eroare=24;return 0;}
int fflush(FILE*Fișier_intrare){return Fișier_intrare&&Fișier_intrare->eroare?-1:0;}
int fclose(FILE*Fișier_intrare){int 반환값=close(Fișier_intrare->Fișier_handle);if(Fișier_intrare->eroare)반환값=-1;Fișier_intrare->사용량=0;return 반환값;}
size_t fwrite(const void*date_poziție,size_t șir_date,size_t element_COUNT,FILE*Fișier_intrare){if(!șir_date)return 0;if(element_COUNT>SIZE_MAX/șir_date){Fișier_intrare->eroare=1;return 0;}long 반환값=write(Fișier_intrare->Fișier_handle,date_poziție,șir_date*element_COUNT);if(반환값<0){Fișier_intrare->eroare=1;return 0;}return (size_t)반환값/șir_date;}
int fputc(int cod_caracter,FILE*Fișier_intrare){unsigned char SECOND_VALUE=cod_caracter;return fwrite(&SECOND_VALUE,1,1,Fișier_intrare)==1?SECOND_VALUE:EOF;}
int fputs(const char*șir_date,FILE*Fișier_intrare){return fwrite(șir_date,1,strlen(șir_date),Fișier_intrare)==strlen(șir_date)?0:EOF;}
static void 넣기(char*KR_date,size_t 용량한도,size_t*curent_poziție,char cod_caracter){if(*curent_poziție+1<용량한도)KR_date[*curent_poziție]=cod_caracter;(*curent_poziție)++;}
int vsnprintf(char*KR_date,size_t 용량한도,const char*format,va_list 가변인수){
    size_t curent_poziție=0;while(*format){if(*format!='%'){넣기(KR_date,용량한도,&curent_poziție,*format++);continue;}format++;
        int 왼쪽=0,zero_VALUE=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')zero_VALUE=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,precizie_VALUE=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;precizie_VALUE=0;if(*format=='*'){precizie_VALUE=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')precizie_VALUE=precizie_VALUE*10+*format++-'0';}
        int caracter_larg=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')caracter_larg=1;format++;}
        char Tip_zonă=*format?*format++:0,zonă_de_stocare_tampon[80];const char*șir_date=zonă_de_stocare_tampon;size_t element_COUNT=0;
        if(Tip_zonă=='s'){șir_date=va_arg(가변인수,const char*);if(!șir_date)șir_date="(null)";element_COUNT=strlen(șir_date);if(precizie_VALUE>=0&&element_COUNT>(size_t)precizie_VALUE)element_COUNT=precizie_VALUE;}
        else if(Tip_zonă=='c'){zonă_de_stocare_tampon[0]=va_arg(가변인수,int);element_COUNT=1;}
        else if(Tip_zonă=='%'){zonă_de_stocare_tampon[0]='%';element_COUNT=1;}
        else if(Tip_zonă=='d'||Tip_zonă=='i'||Tip_zonă=='u'||Tip_zonă=='x'||Tip_zonă=='X'||Tip_zonă=='o'||Tip_zonă=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(Tip_zonă=='d'||Tip_zonă=='i'){long long 임시값=caracter_larg?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=Tip_zonă=='p'?(uintptr_t)va_arg(가변인수,void*):caracter_larg?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned tapet_VALUE=Tip_zonă=='x'||Tip_zonă=='X'||Tip_zonă=='p'?16:Tip_zonă=='o'?8:10;char cifră_COUNT[64];unsigned 사용량=0;
            do{cifră_COUNT[사용량++]="0123456789abcdef"[VALUE%tapet_VALUE];VALUE/=tapet_VALUE;}while(VALUE);
            if(음수표시)zonă_de_stocare_tampon[element_COUNT++]='-';if(Tip_zonă=='p'||(대체값&&tapet_VALUE==16)){zonă_de_stocare_tampon[element_COUNT++]='0';zonă_de_stocare_tampon[element_COUNT++]='x';}
            for(int umple_VALUE=(int)사용량;precizie_VALUE>umple_VALUE&&element_COUNT<sizeof(zonă_de_stocare_tampon)-사용량;umple_VALUE++)zonă_de_stocare_tampon[element_COUNT++]='0';
            if(zero_VALUE&&!왼쪽&&precizie_VALUE<0)while(너비>(int)(element_COUNT+사용량)&&element_COUNT<sizeof(zonă_de_stocare_tampon)-사용량)zonă_de_stocare_tampon[element_COUNT++]='0';
            while(사용량)zonă_de_stocare_tampon[element_COUNT++]=cifră_COUNT[--사용량];
        }else{zonă_de_stocare_tampon[0]='?';element_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)element_COUNT){넣기(KR_date,용량한도,&curent_poziție,' ');너비--;}
        for(size_t 순번=0;순번<element_COUNT;순번++)넣기(KR_date,용량한도,&curent_poziție,șir_date[순번]);while(왼쪽&&너비>(int)element_COUNT){넣기(KR_date,용량한도,&curent_poziție,' ');너비--;}
    }if(용량한도)KR_date[curent_poziție<용량한도?curent_poziție:용량한도-1]=0;return curent_poziție;
}
int snprintf(char*KR_date,size_t 용량한도,const char*Fișier_intrare,...){va_list 첫째값;va_start(첫째값,Fișier_intrare);int 반환값=vsnprintf(KR_date,용량한도,Fișier_intrare,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_date,const char*Fișier_intrare,...){va_list 첫째값;va_start(첫째값,Fișier_intrare);int 반환값=vsnprintf(KR_date,SIZE_MAX,Fișier_intrare,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*flux_VALUE,const char*Fișier_intrare,va_list 첫째값){char SECOND_VALUE[2048];int element_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Fișier_intrare,첫째값);if(element_COUNT>2047)element_COUNT=2047;return fwrite(SECOND_VALUE,1,element_COUNT,flux_VALUE)==(size_t)element_COUNT?element_COUNT:-1;}
int fprintf(FILE*flux_VALUE,const char*Fișier_intrare,...){va_list 첫째값;va_start(첫째값,Fișier_intrare);int 반환값=vfprintf(flux_VALUE,Fișier_intrare,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Fișier_intrare,...){va_list 첫째값;va_start(첫째값,Fișier_intrare);int 반환값=vfprintf(stdout,Fișier_intrare,첫째값);va_end(첫째값);return 반환값;}
