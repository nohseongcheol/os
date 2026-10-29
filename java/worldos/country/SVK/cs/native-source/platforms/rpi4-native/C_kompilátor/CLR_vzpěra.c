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
void exit(int Stav_HODNOTA){사용자호출(6,Stav_HODNOTA,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *šek_výraz,const char *název_souboru,unsigned vstupní_řádek,const char *metoda_položka_název){fprintf(stderr,"cc assertion: %s %s:%u %s\n",šek_výraz,název_souboru,vstupní_řádek,metoda_položka_název);exit(1);}
size_t strlen(const char*řetězec_data){const char*data_pozice=řetězec_data;while(*data_pozice)data_pozice++;return data_pozice-řetězec_data;}
int strcmp(const char*첫째값,const char*SEKUNDA_HODNOTA){while(*첫째값&&*첫째값==*SEKUNDA_HODNOTA){첫째값++;SEKUNDA_HODNOTA++;}return (unsigned char)*첫째값-(unsigned char)*SEKUNDA_HODNOTA;}
int strncmp(const char*첫째값,const char*SEKUNDA_HODNOTA,size_t zboží_POČET){while(zboží_POČET--){unsigned char souřadnice_x=*첫째값++,Y_souřadnice=*SEKUNDA_HODNOTA++;if(souřadnice_x!=Y_souřadnice)return souřadnice_x-Y_souřadnice;if(!souřadnice_x)return 0;}return 0;}
char *strcpy(char*cíl_data,const char*řetězec_data){char*반환값=cíl_data;while((*cíl_data++=*řetězec_data++)){}return 반환값;}
char *strchr(const char*řetězec_data,int bod_kódu){do{if(*řetězec_data==(char)bod_kódu)return (char*)řetězec_data;}while(*řetězec_data++);return 0;}
char *strrchr(const char*řetězec_data,int bod_kódu){const char*반환값=0;do{if(*řetězec_data==(char)bod_kódu)반환값=řetězec_data;}while(*řetězec_data++);return (char*)반환값;}
char *strstr(const char*řetězec_data,const char*Terminál_položka){size_t zboží_POČET=strlen(Terminál_položka);for(;*řetězec_data;řetězec_data++)if(!strncmp(řetězec_data,Terminál_položka,zboží_POČET))return (char*)řetězec_data;return zboží_POČET?0:(char*)řetězec_data;}
int memcmp(const void*첫째값,const void*SEKUNDA_HODNOTA,size_t zboží_POČET){const unsigned char*souřadnice_x=첫째값,*Y_souřadnice=SEKUNDA_HODNOTA;while(zboží_POČET--){if(*souřadnice_x!=*Y_souřadnice)return *souřadnice_x-*Y_souřadnice;souřadnice_x++;Y_souřadnice++;}return 0;}
void *memmove(void*cíl_data,const void*řetězec_data,size_t zboží_POČET){unsigned char*souřadnice_x=cíl_data;const unsigned char*Y_souřadnice=řetězec_data;if(souřadnice_x<Y_souřadnice){for(size_t 순번=0;순번<zboží_POČET;순번++)souřadnice_x[순번]=Y_souřadnice[순번];}else while(zboží_POČET){zboží_POČET--;souřadnice_x[zboží_POČET]=Y_souřadnice[zboží_POČET];}return cíl_data;}
static unsigned char přidělení_Aréna[6*1024*1024] __attribute__((aligned(16)));
typedef struct datový_blok {size_t Velikost;struct datový_blok*Další_zboží;int 남은공간;int odsazení;uint64_t zarovnání_lekce;} datový_blok;
static datový_blok *첫항목;
void free(void*data_pozice){if(!data_pozice)return;datový_blok*SEKUNDA_HODNOTA=(datový_blok*)data_pozice-1;SEKUNDA_HODNOTA->남은공간=1;for(datový_blok*Další_POSUN=첫항목;Další_POSUN&&Další_POSUN->Další_zboží;){if(Další_POSUN->남은공간&&Další_POSUN->Další_zboží->남은공간){Další_POSUN->Velikost+=sizeof(datový_blok)+Další_POSUN->Další_zboží->Velikost;Další_POSUN->Další_zboží=Další_POSUN->Další_zboží->Další_zboží;}else Další_POSUN=Další_POSUN->Další_zboží;}}
void *realloc(void*data_pozice,size_t zboží_POČET){
    if(!zboží_POČET){free(data_pozice);return 0;}if(zboží_POČET>sizeof(přidělení_Aréna)-sizeof(datový_blok))return 0;zboží_POČET=(zboží_POČET+15)&~(size_t)15;
    if(!첫항목){첫항목=(datový_blok*)přidělení_Aréna;첫항목->Velikost=sizeof(přidělení_Aréna)-sizeof(datový_blok);첫항목->남은공간=1;첫항목->Další_zboží=0;}
    datový_blok*Předchozí_zboží=data_pozice?(datový_blok*)data_pozice-1:0;if(Předchozí_zboží&&Předchozí_zboží->Velikost>=zboží_POČET)return data_pozice;
    for(datový_blok*SEKUNDA_HODNOTA=첫항목;SEKUNDA_HODNOTA;SEKUNDA_HODNOTA=SEKUNDA_HODNOTA->Další_zboží)if(SEKUNDA_HODNOTA->남은공간&&SEKUNDA_HODNOTA->Velikost>=zboží_POČET){
        if(SEKUNDA_HODNOTA->Velikost>=zboží_POČET+sizeof(datový_blok)+16){datový_blok*나머지부분=(datový_blok*)((unsigned char*)(SEKUNDA_HODNOTA+1)+zboží_POČET);나머지부분->Velikost=SEKUNDA_HODNOTA->Velikost-zboží_POČET-sizeof(datový_blok);나머지부분->Další_zboží=SEKUNDA_HODNOTA->Další_zboží;나머지부분->남은공간=1;SEKUNDA_HODNOTA->Další_zboží=나머지부분;SEKUNDA_HODNOTA->Velikost=zboží_POČET;}
        SEKUNDA_HODNOTA->남은공간=0;void*반환값=SEKUNDA_HODNOTA+1;if(Předchozí_zboží){memcpy(반환값,data_pozice,Předchozí_zboží->Velikost);free(data_pozice);}return 반환값;
    }chyba=12;return 0;
}
void *malloc(size_t zboží_POČET){return realloc(0,zboží_POČET);}
void *calloc(size_t zboží_POČET,size_t řetězec_data){if(řetězec_data&&zboží_POČET>SIZE_MAX/řetězec_data)return 0;void*data_pozice=malloc(zboží_POČET*řetězec_data);if(data_pozice)memset(data_pozice,0,zboží_POČET*řetězec_data);return data_pozice;}
unsigned long long strtoull(const char*řetězec_data,char**konec_POSUN,int Pozadí_HODNOTA){
    const char*START_POSUN=řetězec_data;while(*řetězec_data==' '||(*řetězec_data>=9&&*řetězec_data<=13))řetězec_data++;int 음수여부=0;if(*řetězec_data=='-'||*řetězec_data=='+')음수여부=*řetězec_data++=='-';
    if((!Pozadí_HODNOTA||Pozadí_HODNOTA==16)&&řetězec_data[0]=='0'&&(řetězec_data[1]=='x'||řetězec_data[1]=='X')){Pozadí_HODNOTA=16;řetězec_data+=2;}if(!Pozadí_HODNOTA)Pozadí_HODNOTA=*řetězec_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned bod_kódu=*řetězec_data,cíl_data=bod_kódu>='0'&&bod_kódu<='9'?bod_kódu-'0':bod_kódu>='a'&&bod_kódu<='z'?bod_kódu-'a'+10:bod_kódu>='A'&&bod_kódu<='Z'?bod_kódu-'A'+10:99;if(cíl_data>=(unsigned)Pozadí_HODNOTA)break;하나라도=1;řetězec_data++;if(임시값>(~0ull-cíl_data)/(unsigned)Pozadí_HODNOTA){임시값=~0ull;chyba=34;}else 임시값=임시값*Pozadí_HODNOTA+cíl_data;}
    if(konec_POSUN)*konec_POSUN=(char*)(하나라도?řetězec_data:START_POSUN);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*řetězec_data,char**보조항목,int SEKUNDA_HODNOTA){return strtoull(řetězec_data,보조항목,SEKUNDA_HODNOTA);}
long strtol(const char*řetězec_data,char**보조항목,int SEKUNDA_HODNOTA){return (long)strtoull(řetězec_data,보조항목,SEKUNDA_HODNOTA);}
int atoi(const char*řetězec_data){return (int)strtol(řetězec_data,0,10);}
long double ldexpl(long double souřadnice_x,int zboží_POČET){while(zboží_POČET>0){souřadnice_x*=2;zboží_POČET--;}while(zboží_POČET<0){souřadnice_x/=2;zboží_POČET++;}return souřadnice_x;}
long double strtold(const char*řetězec_data,char**konec_POSUN){
    const char*START_POSUN=řetězec_data;while(*řetězec_data==' '||(*řetězec_data>=9&&*řetězec_data<=13))řetězec_data++;int 음수여부=0;if(*řetězec_data=='-'||*řetězec_data=='+')음수여부=*řetězec_data++=='-';
    int Pozadí_HODNOTA=10;if(řetězec_data[0]=='0'&&(řetězec_data[1]=='x'||řetězec_data[1]=='X')){Pozadí_HODNOTA=16;řetězec_data+=2;}long double 임시값=0,měřítko=1;int 소수부=0,하나라도=0;
    for(;;){int bod_kódu=*řetězec_data,cíl_data=bod_kódu>='0'&&bod_kódu<='9'?bod_kódu-'0':bod_kódu>='a'&&bod_kódu<='f'?bod_kódu-'a'+10:bod_kódu>='A'&&bod_kódu<='F'?bod_kódu-'A'+10:99;
        if(bod_kódu=='.'&&!소수부){소수부=1;řetězec_data++;continue;}if(cíl_data>=Pozadí_HODNOTA)break;하나라도=1;řetězec_data++;임시값=임시값*Pozadí_HODNOTA+cíl_data;if(소수부)měřítko*=Pozadí_HODNOTA;
    }임시값/=měřítko;
    if((Pozadí_HODNOTA==10&&(*řetězec_data=='e'||*řetězec_data=='E'))||(Pozadí_HODNOTA==16&&(*řetězec_data=='p'||*řetězec_data=='P'))){const char*zobrazit_HODNOTA=řetězec_data++;int 빼기=0;if(*řetězec_data=='-'||*řetězec_data=='+')빼기=*řetězec_data++=='-';int zboží_POČET=0,položka_POČET=0;while(*řetězec_data>='0'&&*řetězec_data<='9'){položka_POČET++;if(zboží_POČET<20000)zboží_POČET=zboží_POČET*10+*řetězec_data-'0';řetězec_data++;}if(!položka_POČET)řetězec_data=zobrazit_HODNOTA;else{long double činitel=Pozadí_HODNOTA==16?2:10;while(zboží_POČET-->0&&zboží_POČET<200000)임시값=빼기?임시값/činitel:임시값*činitel;}}
    if(konec_POSUN)*konec_POSUN=(char*)(하나라도?řetězec_data:START_POSUN);return 음수여부?-임시값:임시값;
}
double strtod(const char*řetězec_data,char**보조항목){return (double)strtold(řetězec_data,보조항목);}float strtof(const char*řetězec_data,char**보조항목){return (float)strtold(řetězec_data,보조항목);}
void qsort(void*Pozadí_HODNOTA,size_t zboží_POČET,size_t Velikost,int(*Porovnat)(const void*,const void*)){
    unsigned char*data_pozice=Pozadí_HODNOTA;for(size_t 순번=1;순번<zboží_POČET;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Porovnat(data_pozice+(안쪽순번-1)*Velikost,data_pozice+안쪽순번*Velikost)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Velikost;셋째순번++){unsigned char bod_kódu=data_pozice[(안쪽순번-1)*Velikost+셋째순번];data_pozice[(안쪽순번-1)*Velikost+셋째순번]=data_pozice[안쪽순번*Velikost+셋째순번];data_pozice[안쪽순번*Velikost+셋째순번]=bod_kódu;}
}
static struct {int 사용량,VYHLEDAT_INDEX;size_t pozice;} 열림[24];
static unsigned char výstup[32768];static size_t výstup_změnit_velikost,výstup_pozice;static int výstup_otevřít;
const unsigned char *C_výstup(size_t *zboží_POČET){*zboží_POČET=výstup_změnit_velikost;return výstup;}
int open(const char*Název,int konfigurace_BITS,...){
    if(!strcmp(Název,"/@cc-output")){if(výstup_otevřít){chyba=16;return -1;}výstup_otevřít=1;výstup_změnit_velikost=výstup_pozice=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompilátor_Prostředky)/sizeof(kompilátor_Prostředky[0]);순번++)if(!strcmp(Název,kompilátor_Prostředky[순번].Název)){
        if(konfigurace_BITS&3){chyba=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].VYHLEDAT_INDEX=순번;열림[안쪽순번].pozice=0;return 128+안쪽순번;}chyba=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Název,konfigurace_BITS,0,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;
}
int close(int popisovač_souboru){if(popisovač_souboru==100){výstup_otevřít=0;return 0;}if(popisovač_souboru>=128&&popisovač_souboru<152){열림[popisovač_souboru-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,popisovač_souboru,0,0,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 0;}
long read(int popisovač_souboru,void*data,size_t zboží_POČET){
    if(popisovač_souboru>=128&&popisovač_souboru<152&&열림[popisovač_souboru-128].사용량){int 순번=popisovač_souboru-128;const kompilátor_zdroj*반환값=&kompilátor_Prostředky[열림[순번].VYHLEDAT_INDEX];size_t 왼쪽=반환값->Velikost-열림[순번].pozice;if(zboží_POČET>왼쪽)zboží_POČET=왼쪽;memcpy(data,반환값->data+열림[순번].pozice,zboží_POČET);열림[순번].pozice+=zboží_POČET;return zboží_POČET;}
    intptr_t 반환값=사용자호출(2,popisovač_souboru,(uintptr_t)data,zboží_POČET,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;
}
long write(int popisovač_souboru,const void*data,size_t zboží_POČET){
    if(popisovač_souboru==100){if(zboží_POČET>sizeof(výstup)-výstup_pozice){chyba=28;return -1;}memcpy(výstup+výstup_pozice,data,zboží_POČET);výstup_pozice+=zboží_POČET;if(výstup_změnit_velikost<výstup_pozice)výstup_změnit_velikost=výstup_pozice;return zboží_POČET;}
    intptr_t 반환값=사용자호출(1,popisovač_souboru,(uintptr_t)data,zboží_POČET,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;
}
long lseek(int popisovač_souboru,long POSUN_HODNOTA,int hledat_origin){
    if(popisovač_souboru==100){long data_pozice=POSUN_HODNOTA+(hledat_origin==0?0:hledat_origin==1?výstup_pozice:výstup_změnit_velikost);if(data_pozice<0||(size_t)data_pozice>sizeof(výstup)){chyba=22;return -1;}výstup_pozice=data_pozice;return data_pozice;}
    if(popisovač_souboru>=128&&popisovač_souboru<152&&열림[popisovač_souboru-128].사용량){int 순번=popisovač_souboru-128;long data_pozice=POSUN_HODNOTA+(hledat_origin==0?0:hledat_origin==1?열림[순번].pozice:kompilátor_Prostředky[열림[순번].VYHLEDAT_INDEX].Velikost);if(data_pozice<0||(size_t)data_pozice>kompilátor_Prostředky[열림[순번].VYHLEDAT_INDEX].Velikost){chyba=22;return -1;}열림[순번].pozice=data_pozice;return data_pozice;}
    intptr_t 반환값=사용자호출(5,popisovač_souboru,POSUN_HODNOTA,hledat_origin,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;
}
int unlink(const char*Název){intptr_t 반환값=사용자호출(11,(uintptr_t)Název,0,0,0,0,0);if(반환값<0){chyba=-반환값;return -1;}return 반환값;}
char *realpath(const char*Název,char*KV_data){if(!KV_data){KV_data=malloc(strlen(Název)+1);if(!KV_data)return 0;}return strcpy(KV_data,Název);}
char *getcwd(char*data_pozice,size_t zboží_POČET){if(zboží_POČET<2){chyba=34;return 0;}data_pozice[0]='/';data_pozice[1]=0;return data_pozice;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminál_položka){time_t 임시값=0;if(Terminál_položka)*Terminál_položka=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminál_položka){(void)Terminál_položka;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Toky[18]={{1,0,1},{2,0,1}};FILE*stdout=&Toky[0],*stderr=&Toky[1];
FILE*fdopen(int popisovač_souboru,const char*metoda_MODE){(void)metoda_MODE;for(unsigned 순번=2;순번<18;순번++)if(!Toky[순번].사용량){Toky[순번].사용량=1;Toky[순번].chyba=0;Toky[순번].popisovač_souboru=popisovač_souboru;return &Toky[순번];}chyba=24;return 0;}
int fflush(FILE*Soubor_položka){return Soubor_položka&&Soubor_položka->chyba?-1:0;}
int fclose(FILE*Soubor_položka){int 반환값=close(Soubor_položka->popisovač_souboru);if(Soubor_položka->chyba)반환값=-1;Soubor_položka->사용량=0;return 반환값;}
size_t fwrite(const void*data_pozice,size_t řetězec_data,size_t zboží_POČET,FILE*Soubor_položka){if(!řetězec_data)return 0;if(zboží_POČET>SIZE_MAX/řetězec_data){Soubor_položka->chyba=1;return 0;}long 반환값=write(Soubor_položka->popisovač_souboru,data_pozice,řetězec_data*zboží_POČET);if(반환값<0){Soubor_položka->chyba=1;return 0;}return (size_t)반환값/řetězec_data;}
int fputc(int bod_kódu,FILE*Soubor_položka){unsigned char SEKUNDA_HODNOTA=bod_kódu;return fwrite(&SEKUNDA_HODNOTA,1,1,Soubor_položka)==1?SEKUNDA_HODNOTA:EOF;}
int fputs(const char*řetězec_data,FILE*Soubor_položka){return fwrite(řetězec_data,1,strlen(řetězec_data),Soubor_položka)==strlen(řetězec_data)?0:EOF;}
static void 넣기(char*KV_data,size_t 용량한도,size_t*dobrá_pozice,char bod_kódu){if(*dobrá_pozice+1<용량한도)KV_data[*dobrá_pozice]=bod_kódu;(*dobrá_pozice)++;}
int vsnprintf(char*KV_data,size_t 용량한도,const char*formát,va_list 가변인수){
    size_t dobrá_pozice=0;while(*formát){if(*formát!='%'){넣기(KV_data,용량한도,&dobrá_pozice,*formát++);continue;}formát++;
        int 왼쪽=0,nulová_hodnota=0,대체값=0;while(*formát=='-'||*formát=='0'||*formát=='#'||*formát=='+'||*formát==' '){if(*formát=='-')왼쪽=1;if(*formát=='0')nulová_hodnota=1;if(*formát=='#')대체값=1;formát++;}
        int 너비=0,přesnost_HODNOTA=-1;if(*formát=='*'){너비=va_arg(가변인수,int);formát++;}else while(*formát>='0'&&*formát<='9')너비=너비*10+*formát++-'0';
        if(*formát=='.'){formát++;přesnost_HODNOTA=0;if(*formát=='*'){přesnost_HODNOTA=va_arg(가변인수,int);formát++;}else while(*formát>='0'&&*formát<='9')přesnost_HODNOTA=přesnost_HODNOTA*10+*formát++-'0';}
        int široký_znak=0;while(*formát=='l'||*formát=='z'||*formát=='t'||*formát=='j'||*formát=='h'){if(*formát!='h')široký_znak=1;formát++;}
        char TYP_oblast=*formát?*formát++:0,zásobník_Storage[80];const char*řetězec_data=zásobník_Storage;size_t zboží_POČET=0;
        if(TYP_oblast=='s'){řetězec_data=va_arg(가변인수,const char*);if(!řetězec_data)řetězec_data="(null)";zboží_POČET=strlen(řetězec_data);if(přesnost_HODNOTA>=0&&zboží_POČET>(size_t)přesnost_HODNOTA)zboží_POČET=přesnost_HODNOTA;}
        else if(TYP_oblast=='c'){zásobník_Storage[0]=va_arg(가변인수,int);zboží_POČET=1;}
        else if(TYP_oblast=='%'){zásobník_Storage[0]='%';zboží_POČET=1;}
        else if(TYP_oblast=='d'||TYP_oblast=='i'||TYP_oblast=='u'||TYP_oblast=='x'||TYP_oblast=='X'||TYP_oblast=='o'||TYP_oblast=='p'){
            unsigned long long HODNOTA;int 음수표시=0;
            if(TYP_oblast=='d'||TYP_oblast=='i'){long long 임시값=široký_znak?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;HODNOTA=음수표시?0-(unsigned long long)임시값:임시값;}
            else HODNOTA=TYP_oblast=='p'?(uintptr_t)va_arg(가변인수,void*):široký_znak?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Pozadí_HODNOTA=TYP_oblast=='x'||TYP_oblast=='X'||TYP_oblast=='p'?16:TYP_oblast=='o'?8:10;char číslice_POČET[64];unsigned 사용량=0;
            do{číslice_POČET[사용량++]="0123456789abcdef"[HODNOTA%Pozadí_HODNOTA];HODNOTA/=Pozadí_HODNOTA;}while(HODNOTA);
            if(음수표시)zásobník_Storage[zboží_POČET++]='-';if(TYP_oblast=='p'||(대체값&&Pozadí_HODNOTA==16)){zásobník_Storage[zboží_POČET++]='0';zásobník_Storage[zboží_POČET++]='x';}
            for(int výplň_HODNOTA=(int)사용량;přesnost_HODNOTA>výplň_HODNOTA&&zboží_POČET<sizeof(zásobník_Storage)-사용량;výplň_HODNOTA++)zásobník_Storage[zboží_POČET++]='0';
            if(nulová_hodnota&&!왼쪽&&přesnost_HODNOTA<0)while(너비>(int)(zboží_POČET+사용량)&&zboží_POČET<sizeof(zásobník_Storage)-사용량)zásobník_Storage[zboží_POČET++]='0';
            while(사용량)zásobník_Storage[zboží_POČET++]=číslice_POČET[--사용량];
        }else{zásobník_Storage[0]='?';zboží_POČET=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)zboží_POČET){넣기(KV_data,용량한도,&dobrá_pozice,' ');너비--;}
        for(size_t 순번=0;순번<zboží_POČET;순번++)넣기(KV_data,용량한도,&dobrá_pozice,řetězec_data[순번]);while(왼쪽&&너비>(int)zboží_POČET){넣기(KV_data,용량한도,&dobrá_pozice,' ');너비--;}
    }if(용량한도)KV_data[dobrá_pozice<용량한도?dobrá_pozice:용량한도-1]=0;return dobrá_pozice;
}
int snprintf(char*KV_data,size_t 용량한도,const char*Soubor_položka,...){va_list 첫째값;va_start(첫째값,Soubor_položka);int 반환값=vsnprintf(KV_data,용량한도,Soubor_položka,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KV_data,const char*Soubor_položka,...){va_list 첫째값;va_start(첫째값,Soubor_položka);int 반환값=vsnprintf(KV_data,SIZE_MAX,Soubor_položka,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*tok_HODNOTA,const char*Soubor_položka,va_list 첫째값){char SEKUNDA_HODNOTA[2048];int zboží_POČET=vsnprintf(SEKUNDA_HODNOTA,sizeof(SEKUNDA_HODNOTA),Soubor_položka,첫째값);if(zboží_POČET>2047)zboží_POČET=2047;return fwrite(SEKUNDA_HODNOTA,1,zboží_POČET,tok_HODNOTA)==(size_t)zboží_POČET?zboží_POČET:-1;}
int fprintf(FILE*tok_HODNOTA,const char*Soubor_položka,...){va_list 첫째값;va_start(첫째값,Soubor_položka);int 반환값=vfprintf(tok_HODNOTA,Soubor_položka,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Soubor_položka,...){va_list 첫째값;va_start(첫째값,Soubor_položka);int 반환값=vfprintf(stdout,Soubor_položka,첫째값);va_end(첫째값);return 반환값;}
