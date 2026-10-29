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
static int Kļūda;
int *__errno_location(void){return &Kļūda;}
void exit(int Statuss_VALUE){사용자호출(6,Statuss_VALUE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *čeks_izteiksme,const char *Fails,unsigned Līniju,const char *metode_ievade_nosaukums){fprintf(stderr,"cc assertion: %s %s:%u %s\n",čeks_izteiksme,Fails,Līniju,metode_ievade_nosaukums);exit(1);}
size_t strlen(const char*virkne_dati){const char*dati_amats=virkne_dati;while(*dati_amats)dati_amats++;return dati_amats-virkne_dati;}
int strcmp(const char*첫째값,const char*SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return (unsigned char)*첫째값-(unsigned char)*SECOND_VALUE;}
int strncmp(const char*첫째값,const char*SECOND_VALUE,size_t krājums_COUNT){while(krājums_COUNT--){unsigned char x_koordināta=*첫째값++,세로좌표=*SECOND_VALUE++;if(x_koordināta!=세로좌표)return x_koordināta-세로좌표;if(!x_koordināta)return 0;}return 0;}
char *strcpy(char*mērķis_dati,const char*virkne_dati){char*반환값=mērķis_dati;while((*mērķis_dati++=*virkne_dati++)){}return 반환값;}
char *strchr(const char*virkne_dati,int koda_punkts){do{if(*virkne_dati==(char)koda_punkts)return (char*)virkne_dati;}while(*virkne_dati++);return 0;}
char *strrchr(const char*virkne_dati,int koda_punkts){const char*반환값=0;do{if(*virkne_dati==(char)koda_punkts)반환값=virkne_dati;}while(*virkne_dati++);return (char*)반환값;}
char *strstr(const char*virkne_dati,const char*Terminālis_ievade){size_t krājums_COUNT=strlen(Terminālis_ievade);for(;*virkne_dati;virkne_dati++)if(!strncmp(virkne_dati,Terminālis_ievade,krājums_COUNT))return (char*)virkne_dati;return krājums_COUNT?0:(char*)virkne_dati;}
int memcmp(const void*첫째값,const void*SECOND_VALUE,size_t krājums_COUNT){const unsigned char*x_koordināta=첫째값,*세로좌표=SECOND_VALUE;while(krājums_COUNT--){if(*x_koordināta!=*세로좌표)return *x_koordināta-*세로좌표;x_koordināta++;세로좌표++;}return 0;}
void *memmove(void*mērķis_dati,const void*virkne_dati,size_t krājums_COUNT){unsigned char*x_koordināta=mērķis_dati;const unsigned char*세로좌표=virkne_dati;if(x_koordināta<세로좌표){for(size_t 순번=0;순번<krājums_COUNT;순번++)x_koordināta[순번]=세로좌표[순번];}else while(krājums_COUNT){krājums_COUNT--;x_koordināta[krājums_COUNT]=세로좌표[krājums_COUNT];}return mērķis_dati;}
static unsigned char iedalīšana_Arēna[6*1024*1024] __attribute__((aligned(16)));
typedef struct datu_bloks {size_t Izmērs;struct datu_bloks*Tālāk_krājums;int 남은공간;int 채울크기;uint64_t līdzinājums_vienība;} datu_bloks;
static datu_bloks *첫항목;
void free(void*dati_amats){if(!dati_amats)return;datu_bloks*SECOND_VALUE=(datu_bloks*)dati_amats-1;SECOND_VALUE->남은공간=1;for(datu_bloks*Tālāk_Nobīde=첫항목;Tālāk_Nobīde&&Tālāk_Nobīde->Tālāk_krājums;){if(Tālāk_Nobīde->남은공간&&Tālāk_Nobīde->Tālāk_krājums->남은공간){Tālāk_Nobīde->Izmērs+=sizeof(datu_bloks)+Tālāk_Nobīde->Tālāk_krājums->Izmērs;Tālāk_Nobīde->Tālāk_krājums=Tālāk_Nobīde->Tālāk_krājums->Tālāk_krājums;}else Tālāk_Nobīde=Tālāk_Nobīde->Tālāk_krājums;}}
void *realloc(void*dati_amats,size_t krājums_COUNT){
    if(!krājums_COUNT){free(dati_amats);return 0;}if(krājums_COUNT>sizeof(iedalīšana_Arēna)-sizeof(datu_bloks))return 0;krājums_COUNT=(krājums_COUNT+15)&~(size_t)15;
    if(!첫항목){첫항목=(datu_bloks*)iedalīšana_Arēna;첫항목->Izmērs=sizeof(iedalīšana_Arēna)-sizeof(datu_bloks);첫항목->남은공간=1;첫항목->Tālāk_krājums=0;}
    datu_bloks*이전=dati_amats?(datu_bloks*)dati_amats-1:0;if(이전&&이전->Izmērs>=krājums_COUNT)return dati_amats;
    for(datu_bloks*SECOND_VALUE=첫항목;SECOND_VALUE;SECOND_VALUE=SECOND_VALUE->Tālāk_krājums)if(SECOND_VALUE->남은공간&&SECOND_VALUE->Izmērs>=krājums_COUNT){
        if(SECOND_VALUE->Izmērs>=krājums_COUNT+sizeof(datu_bloks)+16){datu_bloks*나머지부분=(datu_bloks*)((unsigned char*)(SECOND_VALUE+1)+krājums_COUNT);나머지부분->Izmērs=SECOND_VALUE->Izmērs-krājums_COUNT-sizeof(datu_bloks);나머지부분->Tālāk_krājums=SECOND_VALUE->Tālāk_krājums;나머지부분->남은공간=1;SECOND_VALUE->Tālāk_krājums=나머지부분;SECOND_VALUE->Izmērs=krājums_COUNT;}
        SECOND_VALUE->남은공간=0;void*반환값=SECOND_VALUE+1;if(이전){memcpy(반환값,dati_amats,이전->Izmērs);free(dati_amats);}return 반환값;
    }Kļūda=12;return 0;
}
void *malloc(size_t krājums_COUNT){return realloc(0,krājums_COUNT);}
void *calloc(size_t krājums_COUNT,size_t virkne_dati){if(virkne_dati&&krājums_COUNT>SIZE_MAX/virkne_dati)return 0;void*dati_amats=malloc(krājums_COUNT*virkne_dati);if(dati_amats)memset(dati_amats,0,krājums_COUNT*virkne_dati);return dati_amats;}
unsigned long long strtoull(const char*virkne_dati,char**beigt_zvanu_Nobīde,int Fons_VALUE){
    const char*Sākt_Nobīde=virkne_dati;while(*virkne_dati==' '||(*virkne_dati>=9&&*virkne_dati<=13))virkne_dati++;int 음수여부=0;if(*virkne_dati=='-'||*virkne_dati=='+')음수여부=*virkne_dati++=='-';
    if((!Fons_VALUE||Fons_VALUE==16)&&virkne_dati[0]=='0'&&(virkne_dati[1]=='x'||virkne_dati[1]=='X')){Fons_VALUE=16;virkne_dati+=2;}if(!Fons_VALUE)Fons_VALUE=*virkne_dati=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned koda_punkts=*virkne_dati,mērķis_dati=koda_punkts>='0'&&koda_punkts<='9'?koda_punkts-'0':koda_punkts>='a'&&koda_punkts<='z'?koda_punkts-'a'+10:koda_punkts>='A'&&koda_punkts<='Z'?koda_punkts-'A'+10:99;if(mērķis_dati>=(unsigned)Fons_VALUE)break;하나라도=1;virkne_dati++;if(임시값>(~0ull-mērķis_dati)/(unsigned)Fons_VALUE){임시값=~0ull;Kļūda=34;}else 임시값=임시값*Fons_VALUE+mērķis_dati;}
    if(beigt_zvanu_Nobīde)*beigt_zvanu_Nobīde=(char*)(하나라도?virkne_dati:Sākt_Nobīde);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*virkne_dati,char**보조항목,int SECOND_VALUE){return strtoull(virkne_dati,보조항목,SECOND_VALUE);}
long strtol(const char*virkne_dati,char**보조항목,int SECOND_VALUE){return (long)strtoull(virkne_dati,보조항목,SECOND_VALUE);}
int atoi(const char*virkne_dati){return (int)strtol(virkne_dati,0,10);}
long double ldexpl(long double x_koordināta,int krājums_COUNT){while(krājums_COUNT>0){x_koordināta*=2;krājums_COUNT--;}while(krājums_COUNT<0){x_koordināta/=2;krājums_COUNT++;}return x_koordināta;}
long double strtold(const char*virkne_dati,char**beigt_zvanu_Nobīde){
    const char*Sākt_Nobīde=virkne_dati;while(*virkne_dati==' '||(*virkne_dati>=9&&*virkne_dati<=13))virkne_dati++;int 음수여부=0;if(*virkne_dati=='-'||*virkne_dati=='+')음수여부=*virkne_dati++=='-';
    int Fons_VALUE=10;if(virkne_dati[0]=='0'&&(virkne_dati[1]=='x'||virkne_dati[1]=='X')){Fons_VALUE=16;virkne_dati+=2;}long double 임시값=0,mērogot=1;int 소수부=0,하나라도=0;
    for(;;){int koda_punkts=*virkne_dati,mērķis_dati=koda_punkts>='0'&&koda_punkts<='9'?koda_punkts-'0':koda_punkts>='a'&&koda_punkts<='f'?koda_punkts-'a'+10:koda_punkts>='A'&&koda_punkts<='F'?koda_punkts-'A'+10:99;
        if(koda_punkts=='.'&&!소수부){소수부=1;virkne_dati++;continue;}if(mērķis_dati>=Fons_VALUE)break;하나라도=1;virkne_dati++;임시값=임시값*Fons_VALUE+mērķis_dati;if(소수부)mērogot*=Fons_VALUE;
    }임시값/=mērogot;
    if((Fons_VALUE==10&&(*virkne_dati=='e'||*virkne_dati=='E'))||(Fons_VALUE==16&&(*virkne_dati=='p'||*virkne_dati=='P'))){const char*rādīt_VALUE=virkne_dati++;int 빼기=0;if(*virkne_dati=='-'||*virkne_dati=='+')빼기=*virkne_dati++=='-';int krājums_COUNT=0,ievade_COUNT=0;while(*virkne_dati>='0'&&*virkne_dati<='9'){ievade_COUNT++;if(krājums_COUNT<20000)krājums_COUNT=krājums_COUNT*10+*virkne_dati-'0';virkne_dati++;}if(!ievade_COUNT)virkne_dati=rādīt_VALUE;else{long double koeficients=Fons_VALUE==16?2:10;while(krājums_COUNT-->0&&krājums_COUNT<200000)임시값=빼기?임시값/koeficients:임시값*koeficients;}}
    if(beigt_zvanu_Nobīde)*beigt_zvanu_Nobīde=(char*)(하나라도?virkne_dati:Sākt_Nobīde);return 음수여부?-임시값:임시값;
}
double strtod(const char*virkne_dati,char**보조항목){return (double)strtold(virkne_dati,보조항목);}float strtof(const char*virkne_dati,char**보조항목){return (float)strtold(virkne_dati,보조항목);}
void qsort(void*Fons_VALUE,size_t krājums_COUNT,size_t Izmērs,int(*Salīdzināt)(const void*,const void*)){
    unsigned char*dati_amats=Fons_VALUE;for(size_t 순번=1;순번<krājums_COUNT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Salīdzināt(dati_amats+(안쪽순번-1)*Izmērs,dati_amats+안쪽순번*Izmērs)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Izmērs;셋째순번++){unsigned char koda_punkts=dati_amats[(안쪽순번-1)*Izmērs+셋째순번];dati_amats[(안쪽순번-1)*Izmērs+셋째순번]=dati_amats[안쪽순번*Izmērs+셋째순번];dati_amats[안쪽순번*Izmērs+셋째순번]=koda_punkts;}
}
static struct {int 사용량,LOOKUP_INDEX;size_t Novietojums;} 열림[24];
static unsigned char ražojums[32768];static size_t ražojums_mainīt_izmērus,ražojums_amats;static int ražojums_atvērt;
const unsigned char *C_ražojums(size_t *krājums_COUNT){*krājums_COUNT=ražojums_mainīt_izmērus;return ražojums;}
int open(const char*Nosaukums,int konfigurācija_Background_Intelligent_Transfer_Service,...){
    if(!strcmp(Nosaukums,"/@cc-output")){if(ražojums_atvērt){Kļūda=16;return -1;}ražojums_atvērt=1;ražojums_mainīt_izmērus=ražojums_amats=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompilators_Resursi)/sizeof(kompilators_Resursi[0]);순번++)if(!strcmp(Nosaukums,kompilators_Resursi[순번].Nosaukums)){
        if(konfigurācija_Background_Intelligent_Transfer_Service&3){Kļūda=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LOOKUP_INDEX=순번;열림[안쪽순번].Novietojums=0;return 128+안쪽순번;}Kļūda=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nosaukums,konfigurācija_Background_Intelligent_Transfer_Service,0,0,0,0);if(반환값<0){Kļūda=-반환값;return -1;}return 반환값;
}
int close(int Fails_turis){if(Fails_turis==100){ražojums_atvērt=0;return 0;}if(Fails_turis>=128&&Fails_turis<152){열림[Fails_turis-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Fails_turis,0,0,0,0,0);if(반환값<0){Kļūda=-반환값;return -1;}return 0;}
long read(int Fails_turis,void*dati,size_t krājums_COUNT){
    if(Fails_turis>=128&&Fails_turis<152&&열림[Fails_turis-128].사용량){int 순번=Fails_turis-128;const kompilators_resurss*반환값=&kompilators_Resursi[열림[순번].LOOKUP_INDEX];size_t 왼쪽=반환값->Izmērs-열림[순번].Novietojums;if(krājums_COUNT>왼쪽)krājums_COUNT=왼쪽;memcpy(dati,반환값->dati+열림[순번].Novietojums,krājums_COUNT);열림[순번].Novietojums+=krājums_COUNT;return krājums_COUNT;}
    intptr_t 반환값=사용자호출(2,Fails_turis,(uintptr_t)dati,krājums_COUNT,0,0,0);if(반환값<0){Kļūda=-반환값;return -1;}return 반환값;
}
long write(int Fails_turis,const void*dati,size_t krājums_COUNT){
    if(Fails_turis==100){if(krājums_COUNT>sizeof(ražojums)-ražojums_amats){Kļūda=28;return -1;}memcpy(ražojums+ražojums_amats,dati,krājums_COUNT);ražojums_amats+=krājums_COUNT;if(ražojums_mainīt_izmērus<ražojums_amats)ražojums_mainīt_izmērus=ražojums_amats;return krājums_COUNT;}
    intptr_t 반환값=사용자호출(1,Fails_turis,(uintptr_t)dati,krājums_COUNT,0,0,0);if(반환값<0){Kļūda=-반환값;return -1;}return 반환값;
}
long lseek(int Fails_turis,long Nobīde_VALUE,int 기준점){
    if(Fails_turis==100){long dati_amats=Nobīde_VALUE+(기준점==0?0:기준점==1?ražojums_amats:ražojums_mainīt_izmērus);if(dati_amats<0||(size_t)dati_amats>sizeof(ražojums)){Kļūda=22;return -1;}ražojums_amats=dati_amats;return dati_amats;}
    if(Fails_turis>=128&&Fails_turis<152&&열림[Fails_turis-128].사용량){int 순번=Fails_turis-128;long dati_amats=Nobīde_VALUE+(기준점==0?0:기준점==1?열림[순번].Novietojums:kompilators_Resursi[열림[순번].LOOKUP_INDEX].Izmērs);if(dati_amats<0||(size_t)dati_amats>kompilators_Resursi[열림[순번].LOOKUP_INDEX].Izmērs){Kļūda=22;return -1;}열림[순번].Novietojums=dati_amats;return dati_amats;}
    intptr_t 반환값=사용자호출(5,Fails_turis,Nobīde_VALUE,기준점,0,0,0);if(반환값<0){Kļūda=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nosaukums){intptr_t 반환값=사용자호출(11,(uintptr_t)Nosaukums,0,0,0,0,0);if(반환값<0){Kļūda=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nosaukums,char*mērs_dati){if(!mērs_dati){mērs_dati=malloc(strlen(Nosaukums)+1);if(!mērs_dati)return 0;}return strcpy(mērs_dati,Nosaukums);}
char *getcwd(char*dati_amats,size_t krājums_COUNT){if(krājums_COUNT<2){Kļūda=34;return 0;}dati_amats[0]='/';dati_amats[1]=0;return dati_amats;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminālis_ievade){time_t 임시값=0;if(Terminālis_ievade)*Terminālis_ievade=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminālis_ievade){(void)Terminālis_ievade;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Straumes[18]={{1,0,1},{2,0,1}};FILE*stdout=&Straumes[0],*stderr=&Straumes[1];
FILE*fdopen(int Fails_turis,const char*metode_MODE){(void)metode_MODE;for(unsigned 순번=2;순번<18;순번++)if(!Straumes[순번].사용량){Straumes[순번].사용량=1;Straumes[순번].Kļūda=0;Straumes[순번].Fails_turis=Fails_turis;return &Straumes[순번];}Kļūda=24;return 0;}
int fflush(FILE*Fails_ievade){return Fails_ievade&&Fails_ievade->Kļūda?-1:0;}
int fclose(FILE*Fails_ievade){int 반환값=close(Fails_ievade->Fails_turis);if(Fails_ievade->Kļūda)반환값=-1;Fails_ievade->사용량=0;return 반환값;}
size_t fwrite(const void*dati_amats,size_t virkne_dati,size_t krājums_COUNT,FILE*Fails_ievade){if(!virkne_dati)return 0;if(krājums_COUNT>SIZE_MAX/virkne_dati){Fails_ievade->Kļūda=1;return 0;}long 반환값=write(Fails_ievade->Fails_turis,dati_amats,virkne_dati*krājums_COUNT);if(반환값<0){Fails_ievade->Kļūda=1;return 0;}return (size_t)반환값/virkne_dati;}
int fputc(int koda_punkts,FILE*Fails_ievade){unsigned char SECOND_VALUE=koda_punkts;return fwrite(&SECOND_VALUE,1,1,Fails_ievade)==1?SECOND_VALUE:EOF;}
int fputs(const char*virkne_dati,FILE*Fails_ievade){return fwrite(virkne_dati,1,strlen(virkne_dati),Fails_ievade)==strlen(virkne_dati)?0:EOF;}
static void 넣기(char*mērs_dati,size_t 용량한도,size_t*pašreizējais_amats,char koda_punkts){if(*pašreizējais_amats+1<용량한도)mērs_dati[*pašreizējais_amats]=koda_punkts;(*pašreizējais_amats)++;}
int vsnprintf(char*mērs_dati,size_t 용량한도,const char*formāts,va_list 가변인수){
    size_t pašreizējais_amats=0;while(*formāts){if(*formāts!='%'){넣기(mērs_dati,용량한도,&pašreizējais_amats,*formāts++);continue;}formāts++;
        int 왼쪽=0,nulle_VALUE=0,대체값=0;while(*formāts=='-'||*formāts=='0'||*formāts=='#'||*formāts=='+'||*formāts==' '){if(*formāts=='-')왼쪽=1;if(*formāts=='0')nulle_VALUE=1;if(*formāts=='#')대체값=1;formāts++;}
        int 너비=0,precizitāte_VALUE=-1;if(*formāts=='*'){너비=va_arg(가변인수,int);formāts++;}else while(*formāts>='0'&&*formāts<='9')너비=너비*10+*formāts++-'0';
        if(*formāts=='.'){formāts++;precizitāte_VALUE=0;if(*formāts=='*'){precizitāte_VALUE=va_arg(가변인수,int);formāts++;}else while(*formāts>='0'&&*formāts<='9')precizitāte_VALUE=precizitāte_VALUE*10+*formāts++-'0';}
        int paplašināta_rakstzīme=0;while(*formāts=='l'||*formāts=='z'||*formāts=='t'||*formāts=='j'||*formāts=='h'){if(*formāts!='h')paplašināta_rakstzīme=1;formāts++;}
        char TYPE_joma=*formāts?*formāts++:0,bufera_krātuve[80];const char*virkne_dati=bufera_krātuve;size_t krājums_COUNT=0;
        if(TYPE_joma=='s'){virkne_dati=va_arg(가변인수,const char*);if(!virkne_dati)virkne_dati="(null)";krājums_COUNT=strlen(virkne_dati);if(precizitāte_VALUE>=0&&krājums_COUNT>(size_t)precizitāte_VALUE)krājums_COUNT=precizitāte_VALUE;}
        else if(TYPE_joma=='c'){bufera_krātuve[0]=va_arg(가변인수,int);krājums_COUNT=1;}
        else if(TYPE_joma=='%'){bufera_krātuve[0]='%';krājums_COUNT=1;}
        else if(TYPE_joma=='d'||TYPE_joma=='i'||TYPE_joma=='u'||TYPE_joma=='x'||TYPE_joma=='X'||TYPE_joma=='o'||TYPE_joma=='p'){
            unsigned long long VALUE;int 음수표시=0;
            if(TYPE_joma=='d'||TYPE_joma=='i'){long long 임시값=paplašināta_rakstzīme?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALUE=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALUE=TYPE_joma=='p'?(uintptr_t)va_arg(가변인수,void*):paplašināta_rakstzīme?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Fons_VALUE=TYPE_joma=='x'||TYPE_joma=='X'||TYPE_joma=='p'?16:TYPE_joma=='o'?8:10;char cipars_COUNT[64];unsigned 사용량=0;
            do{cipars_COUNT[사용량++]="0123456789abcdef"[VALUE%Fons_VALUE];VALUE/=Fons_VALUE;}while(VALUE);
            if(음수표시)bufera_krātuve[krājums_COUNT++]='-';if(TYPE_joma=='p'||(대체값&&Fons_VALUE==16)){bufera_krātuve[krājums_COUNT++]='0';bufera_krātuve[krājums_COUNT++]='x';}
            for(int aizpildīt_VALUE=(int)사용량;precizitāte_VALUE>aizpildīt_VALUE&&krājums_COUNT<sizeof(bufera_krātuve)-사용량;aizpildīt_VALUE++)bufera_krātuve[krājums_COUNT++]='0';
            if(nulle_VALUE&&!왼쪽&&precizitāte_VALUE<0)while(너비>(int)(krājums_COUNT+사용량)&&krājums_COUNT<sizeof(bufera_krātuve)-사용량)bufera_krātuve[krājums_COUNT++]='0';
            while(사용량)bufera_krātuve[krājums_COUNT++]=cipars_COUNT[--사용량];
        }else{bufera_krātuve[0]='?';krājums_COUNT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)krājums_COUNT){넣기(mērs_dati,용량한도,&pašreizējais_amats,' ');너비--;}
        for(size_t 순번=0;순번<krājums_COUNT;순번++)넣기(mērs_dati,용량한도,&pašreizējais_amats,virkne_dati[순번]);while(왼쪽&&너비>(int)krājums_COUNT){넣기(mērs_dati,용량한도,&pašreizējais_amats,' ');너비--;}
    }if(용량한도)mērs_dati[pašreizējais_amats<용량한도?pašreizējais_amats:용량한도-1]=0;return pašreizējais_amats;
}
int snprintf(char*mērs_dati,size_t 용량한도,const char*Fails_ievade,...){va_list 첫째값;va_start(첫째값,Fails_ievade);int 반환값=vsnprintf(mērs_dati,용량한도,Fails_ievade,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*mērs_dati,const char*Fails_ievade,...){va_list 첫째값;va_start(첫째값,Fails_ievade);int 반환값=vsnprintf(mērs_dati,SIZE_MAX,Fails_ievade,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_VALUE,const char*Fails_ievade,va_list 첫째값){char SECOND_VALUE[2048];int krājums_COUNT=vsnprintf(SECOND_VALUE,sizeof(SECOND_VALUE),Fails_ievade,첫째값);if(krājums_COUNT>2047)krājums_COUNT=2047;return fwrite(SECOND_VALUE,1,krājums_COUNT,Stream_VALUE)==(size_t)krājums_COUNT?krājums_COUNT:-1;}
int fprintf(FILE*Stream_VALUE,const char*Fails_ievade,...){va_list 첫째값;va_start(첫째값,Fails_ievade);int 반환값=vfprintf(Stream_VALUE,Fails_ievade,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Fails_ievade,...){va_list 첫째값;va_start(첫째값,Fails_ievade);int 반환값=vfprintf(stdout,Fails_ievade,첫째값);va_end(첫째값);return 반환값;}
