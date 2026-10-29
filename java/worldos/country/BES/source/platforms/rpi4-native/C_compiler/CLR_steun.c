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
static int fout;
int *__errno_location(void){return &fout;}
void exit(int Status_WAARDE){사용자호출(6,Status_WAARDE,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *cheque_expressie,const char *bestand,unsigned invoerregel,const char *methode_invoer_naam){fprintf(stderr,"cc assertion: %s %s:%u %s\n",cheque_expressie,bestand,invoerregel,methode_invoer_naam);exit(1);}
size_t strlen(const char*tekenreeks_gegevens){const char*gegevens_functie=tekenreeks_gegevens;while(*gegevens_functie)gegevens_functie++;return gegevens_functie-tekenreeks_gegevens;}
int strcmp(const char*첫째값,const char*SECONDE_WAARDE){while(*첫째값&&*첫째값==*SECONDE_WAARDE){첫째값++;SECONDE_WAARDE++;}return (unsigned char)*첫째값-(unsigned char)*SECONDE_WAARDE;}
int strncmp(const char*첫째값,const char*SECONDE_WAARDE,size_t item_AANTAL){while(item_AANTAL--){unsigned char x_coördinaat=*첫째값++,Y_coördinaat=*SECONDE_WAARDE++;if(x_coördinaat!=Y_coördinaat)return x_coördinaat-Y_coördinaat;if(!x_coördinaat)return 0;}return 0;}
char *strcpy(char*doel_gegevens,const char*tekenreeks_gegevens){char*반환값=doel_gegevens;while((*doel_gegevens++=*tekenreeks_gegevens++)){}return 반환값;}
char *strchr(const char*tekenreeks_gegevens,int codepoint){do{if(*tekenreeks_gegevens==(char)codepoint)return (char*)tekenreeks_gegevens;}while(*tekenreeks_gegevens++);return 0;}
char *strrchr(const char*tekenreeks_gegevens,int codepoint){const char*반환값=0;do{if(*tekenreeks_gegevens==(char)codepoint)반환값=tekenreeks_gegevens;}while(*tekenreeks_gegevens++);return (char*)반환값;}
char *strstr(const char*tekenreeks_gegevens,const char*Terminal_invoer){size_t item_AANTAL=strlen(Terminal_invoer);for(;*tekenreeks_gegevens;tekenreeks_gegevens++)if(!strncmp(tekenreeks_gegevens,Terminal_invoer,item_AANTAL))return (char*)tekenreeks_gegevens;return item_AANTAL?0:(char*)tekenreeks_gegevens;}
int memcmp(const void*첫째값,const void*SECONDE_WAARDE,size_t item_AANTAL){const unsigned char*x_coördinaat=첫째값,*Y_coördinaat=SECONDE_WAARDE;while(item_AANTAL--){if(*x_coördinaat!=*Y_coördinaat)return *x_coördinaat-*Y_coördinaat;x_coördinaat++;Y_coördinaat++;}return 0;}
void *memmove(void*doel_gegevens,const void*tekenreeks_gegevens,size_t item_AANTAL){unsigned char*x_coördinaat=doel_gegevens;const unsigned char*Y_coördinaat=tekenreeks_gegevens;if(x_coördinaat<Y_coördinaat){for(size_t 순번=0;순번<item_AANTAL;순번++)x_coördinaat[순번]=Y_coördinaat[순번];}else while(item_AANTAL){item_AANTAL--;x_coördinaat[item_AANTAL]=Y_coördinaat[item_AANTAL];}return doel_gegevens;}
static unsigned char toewijzing_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct gegevensblok {size_t Grootte;struct gegevensblok*Volgende_item;int 남은공간;int opvulling;uint64_t uitlijning_les;} gegevensblok;
static gegevensblok *첫항목;
void free(void*gegevens_functie){if(!gegevens_functie)return;gegevensblok*SECONDE_WAARDE=(gegevensblok*)gegevens_functie-1;SECONDE_WAARDE->남은공간=1;for(gegevensblok*Volgende_VERSCHUIVING=첫항목;Volgende_VERSCHUIVING&&Volgende_VERSCHUIVING->Volgende_item;){if(Volgende_VERSCHUIVING->남은공간&&Volgende_VERSCHUIVING->Volgende_item->남은공간){Volgende_VERSCHUIVING->Grootte+=sizeof(gegevensblok)+Volgende_VERSCHUIVING->Volgende_item->Grootte;Volgende_VERSCHUIVING->Volgende_item=Volgende_VERSCHUIVING->Volgende_item->Volgende_item;}else Volgende_VERSCHUIVING=Volgende_VERSCHUIVING->Volgende_item;}}
void *realloc(void*gegevens_functie,size_t item_AANTAL){
    if(!item_AANTAL){free(gegevens_functie);return 0;}if(item_AANTAL>sizeof(toewijzing_Arena)-sizeof(gegevensblok))return 0;item_AANTAL=(item_AANTAL+15)&~(size_t)15;
    if(!첫항목){첫항목=(gegevensblok*)toewijzing_Arena;첫항목->Grootte=sizeof(toewijzing_Arena)-sizeof(gegevensblok);첫항목->남은공간=1;첫항목->Volgende_item=0;}
    gegevensblok*Vorige_item=gegevens_functie?(gegevensblok*)gegevens_functie-1:0;if(Vorige_item&&Vorige_item->Grootte>=item_AANTAL)return gegevens_functie;
    for(gegevensblok*SECONDE_WAARDE=첫항목;SECONDE_WAARDE;SECONDE_WAARDE=SECONDE_WAARDE->Volgende_item)if(SECONDE_WAARDE->남은공간&&SECONDE_WAARDE->Grootte>=item_AANTAL){
        if(SECONDE_WAARDE->Grootte>=item_AANTAL+sizeof(gegevensblok)+16){gegevensblok*나머지부분=(gegevensblok*)((unsigned char*)(SECONDE_WAARDE+1)+item_AANTAL);나머지부분->Grootte=SECONDE_WAARDE->Grootte-item_AANTAL-sizeof(gegevensblok);나머지부분->Volgende_item=SECONDE_WAARDE->Volgende_item;나머지부분->남은공간=1;SECONDE_WAARDE->Volgende_item=나머지부분;SECONDE_WAARDE->Grootte=item_AANTAL;}
        SECONDE_WAARDE->남은공간=0;void*반환값=SECONDE_WAARDE+1;if(Vorige_item){memcpy(반환값,gegevens_functie,Vorige_item->Grootte);free(gegevens_functie);}return 반환값;
    }fout=12;return 0;
}
void *malloc(size_t item_AANTAL){return realloc(0,item_AANTAL);}
void *calloc(size_t item_AANTAL,size_t tekenreeks_gegevens){if(tekenreeks_gegevens&&item_AANTAL>SIZE_MAX/tekenreeks_gegevens)return 0;void*gegevens_functie=malloc(item_AANTAL*tekenreeks_gegevens);if(gegevens_functie)memset(gegevens_functie,0,item_AANTAL*tekenreeks_gegevens);return gegevens_functie;}
unsigned long long strtoull(const char*tekenreeks_gegevens,char**beëindigen_VERSCHUIVING,int Achtergrond_WAARDE){
    const char*START_VERSCHUIVING=tekenreeks_gegevens;while(*tekenreeks_gegevens==' '||(*tekenreeks_gegevens>=9&&*tekenreeks_gegevens<=13))tekenreeks_gegevens++;int 음수여부=0;if(*tekenreeks_gegevens=='-'||*tekenreeks_gegevens=='+')음수여부=*tekenreeks_gegevens++=='-';
    if((!Achtergrond_WAARDE||Achtergrond_WAARDE==16)&&tekenreeks_gegevens[0]=='0'&&(tekenreeks_gegevens[1]=='x'||tekenreeks_gegevens[1]=='X')){Achtergrond_WAARDE=16;tekenreeks_gegevens+=2;}if(!Achtergrond_WAARDE)Achtergrond_WAARDE=*tekenreeks_gegevens=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned codepoint=*tekenreeks_gegevens,doel_gegevens=codepoint>='0'&&codepoint<='9'?codepoint-'0':codepoint>='a'&&codepoint<='z'?codepoint-'a'+10:codepoint>='A'&&codepoint<='Z'?codepoint-'A'+10:99;if(doel_gegevens>=(unsigned)Achtergrond_WAARDE)break;하나라도=1;tekenreeks_gegevens++;if(임시값>(~0ull-doel_gegevens)/(unsigned)Achtergrond_WAARDE){임시값=~0ull;fout=34;}else 임시값=임시값*Achtergrond_WAARDE+doel_gegevens;}
    if(beëindigen_VERSCHUIVING)*beëindigen_VERSCHUIVING=(char*)(하나라도?tekenreeks_gegevens:START_VERSCHUIVING);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*tekenreeks_gegevens,char**보조항목,int SECONDE_WAARDE){return strtoull(tekenreeks_gegevens,보조항목,SECONDE_WAARDE);}
long strtol(const char*tekenreeks_gegevens,char**보조항목,int SECONDE_WAARDE){return (long)strtoull(tekenreeks_gegevens,보조항목,SECONDE_WAARDE);}
int atoi(const char*tekenreeks_gegevens){return (int)strtol(tekenreeks_gegevens,0,10);}
long double ldexpl(long double x_coördinaat,int item_AANTAL){while(item_AANTAL>0){x_coördinaat*=2;item_AANTAL--;}while(item_AANTAL<0){x_coördinaat/=2;item_AANTAL++;}return x_coördinaat;}
long double strtold(const char*tekenreeks_gegevens,char**beëindigen_VERSCHUIVING){
    const char*START_VERSCHUIVING=tekenreeks_gegevens;while(*tekenreeks_gegevens==' '||(*tekenreeks_gegevens>=9&&*tekenreeks_gegevens<=13))tekenreeks_gegevens++;int 음수여부=0;if(*tekenreeks_gegevens=='-'||*tekenreeks_gegevens=='+')음수여부=*tekenreeks_gegevens++=='-';
    int Achtergrond_WAARDE=10;if(tekenreeks_gegevens[0]=='0'&&(tekenreeks_gegevens[1]=='x'||tekenreeks_gegevens[1]=='X')){Achtergrond_WAARDE=16;tekenreeks_gegevens+=2;}long double 임시값=0,schaal=1;int 소수부=0,하나라도=0;
    for(;;){int codepoint=*tekenreeks_gegevens,doel_gegevens=codepoint>='0'&&codepoint<='9'?codepoint-'0':codepoint>='a'&&codepoint<='f'?codepoint-'a'+10:codepoint>='A'&&codepoint<='F'?codepoint-'A'+10:99;
        if(codepoint=='.'&&!소수부){소수부=1;tekenreeks_gegevens++;continue;}if(doel_gegevens>=Achtergrond_WAARDE)break;하나라도=1;tekenreeks_gegevens++;임시값=임시값*Achtergrond_WAARDE+doel_gegevens;if(소수부)schaal*=Achtergrond_WAARDE;
    }임시값/=schaal;
    if((Achtergrond_WAARDE==10&&(*tekenreeks_gegevens=='e'||*tekenreeks_gegevens=='E'))||(Achtergrond_WAARDE==16&&(*tekenreeks_gegevens=='p'||*tekenreeks_gegevens=='P'))){const char*weergeven_WAARDE=tekenreeks_gegevens++;int 빼기=0;if(*tekenreeks_gegevens=='-'||*tekenreeks_gegevens=='+')빼기=*tekenreeks_gegevens++=='-';int item_AANTAL=0,invoer_AANTAL_8f7753a1=0;while(*tekenreeks_gegevens>='0'&&*tekenreeks_gegevens<='9'){invoer_AANTAL_8f7753a1++;if(item_AANTAL<20000)item_AANTAL=item_AANTAL*10+*tekenreeks_gegevens-'0';tekenreeks_gegevens++;}if(!invoer_AANTAL_8f7753a1)tekenreeks_gegevens=weergeven_WAARDE;else{long double factor=Achtergrond_WAARDE==16?2:10;while(item_AANTAL-->0&&item_AANTAL<200000)임시값=빼기?임시값/factor:임시값*factor;}}
    if(beëindigen_VERSCHUIVING)*beëindigen_VERSCHUIVING=(char*)(하나라도?tekenreeks_gegevens:START_VERSCHUIVING);return 음수여부?-임시값:임시값;
}
double strtod(const char*tekenreeks_gegevens,char**보조항목){return (double)strtold(tekenreeks_gegevens,보조항목);}float strtof(const char*tekenreeks_gegevens,char**보조항목){return (float)strtold(tekenreeks_gegevens,보조항목);}
void qsort(void*Achtergrond_WAARDE,size_t item_AANTAL,size_t Grootte,int(*Vergelijken)(const void*,const void*)){
    unsigned char*gegevens_functie=Achtergrond_WAARDE;for(size_t 순번=1;순번<item_AANTAL;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Vergelijken(gegevens_functie+(안쪽순번-1)*Grootte,gegevens_functie+안쪽순번*Grootte)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Grootte;셋째순번++){unsigned char codepoint=gegevens_functie[(안쪽순번-1)*Grootte+셋째순번];gegevens_functie[(안쪽순번-1)*Grootte+셋째순번]=gegevens_functie[안쪽순번*Grootte+셋째순번];gegevens_functie[안쪽순번*Grootte+셋째순번]=codepoint;}
}
static struct {int 사용량,ZOEKEN_INDEX;size_t positie;} 열림[24];
static unsigned char uitvoer[32768];static size_t uitvoer_formaat_wijzigen,uitvoer_functie;static int uitvoer_open;
const unsigned char *C_uitvoer(size_t *item_AANTAL){*item_AANTAL=uitvoer_formaat_wijzigen;return uitvoer;}
int open(const char*Naam,int configuratie_BITS,...){
    if(!strcmp(Naam,"/@cc-output")){if(uitvoer_open){fout=16;return -1;}uitvoer_open=1;uitvoer_formaat_wijzigen=uitvoer_functie=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(compiler_Bronnen)/sizeof(compiler_Bronnen[0]);순번++)if(!strcmp(Naam,compiler_Bronnen[순번].Naam)){
        if(configuratie_BITS&3){fout=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].ZOEKEN_INDEX=순번;열림[안쪽순번].positie=0;return 128+안쪽순번;}fout=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Naam,configuratie_BITS,0,0,0,0);if(반환값<0){fout=-반환값;return -1;}return 반환값;
}
int close(int bestandsingang){if(bestandsingang==100){uitvoer_open=0;return 0;}if(bestandsingang>=128&&bestandsingang<152){열림[bestandsingang-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,bestandsingang,0,0,0,0,0);if(반환값<0){fout=-반환값;return -1;}return 0;}
long read(int bestandsingang,void*gegevens,size_t item_AANTAL){
    if(bestandsingang>=128&&bestandsingang<152&&열림[bestandsingang-128].사용량){int 순번=bestandsingang-128;const compiler_bron*반환값=&compiler_Bronnen[열림[순번].ZOEKEN_INDEX];size_t 왼쪽=반환값->Grootte-열림[순번].positie;if(item_AANTAL>왼쪽)item_AANTAL=왼쪽;memcpy(gegevens,반환값->gegevens+열림[순번].positie,item_AANTAL);열림[순번].positie+=item_AANTAL;return item_AANTAL;}
    intptr_t 반환값=사용자호출(2,bestandsingang,(uintptr_t)gegevens,item_AANTAL,0,0,0);if(반환값<0){fout=-반환값;return -1;}return 반환값;
}
long write(int bestandsingang,const void*gegevens,size_t item_AANTAL){
    if(bestandsingang==100){if(item_AANTAL>sizeof(uitvoer)-uitvoer_functie){fout=28;return -1;}memcpy(uitvoer+uitvoer_functie,gegevens,item_AANTAL);uitvoer_functie+=item_AANTAL;if(uitvoer_formaat_wijzigen<uitvoer_functie)uitvoer_formaat_wijzigen=uitvoer_functie;return item_AANTAL;}
    intptr_t 반환값=사용자호출(1,bestandsingang,(uintptr_t)gegevens,item_AANTAL,0,0,0);if(반환값<0){fout=-반환값;return -1;}return 반환값;
}
long lseek(int bestandsingang,long VERSCHUIVING_WAARDE,int zoeken_oorsprong){
    if(bestandsingang==100){long gegevens_functie=VERSCHUIVING_WAARDE+(zoeken_oorsprong==0?0:zoeken_oorsprong==1?uitvoer_functie:uitvoer_formaat_wijzigen);if(gegevens_functie<0||(size_t)gegevens_functie>sizeof(uitvoer)){fout=22;return -1;}uitvoer_functie=gegevens_functie;return gegevens_functie;}
    if(bestandsingang>=128&&bestandsingang<152&&열림[bestandsingang-128].사용량){int 순번=bestandsingang-128;long gegevens_functie=VERSCHUIVING_WAARDE+(zoeken_oorsprong==0?0:zoeken_oorsprong==1?열림[순번].positie:compiler_Bronnen[열림[순번].ZOEKEN_INDEX].Grootte);if(gegevens_functie<0||(size_t)gegevens_functie>compiler_Bronnen[열림[순번].ZOEKEN_INDEX].Grootte){fout=22;return -1;}열림[순번].positie=gegevens_functie;return gegevens_functie;}
    intptr_t 반환값=사용자호출(5,bestandsingang,VERSCHUIVING_WAARDE,zoeken_oorsprong,0,0,0);if(반환값<0){fout=-반환값;return -1;}return 반환값;
}
int unlink(const char*Naam){intptr_t 반환값=사용자호출(11,(uintptr_t)Naam,0,0,0,0,0);if(반환값<0){fout=-반환값;return -1;}return 반환값;}
char *realpath(const char*Naam,char*HR_gegevens){if(!HR_gegevens){HR_gegevens=malloc(strlen(Naam)+1);if(!HR_gegevens)return 0;}return strcpy(HR_gegevens,Naam);}
char *getcwd(char*gegevens_functie,size_t item_AANTAL){if(item_AANTAL<2){fout=34;return 0;}gegevens_functie[0]='/';gegevens_functie[1]=0;return gegevens_functie;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_invoer){time_t 임시값=0;if(Terminal_invoer)*Terminal_invoer=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_invoer){(void)Terminal_invoer;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Streams[18]={{1,0,1},{2,0,1}};FILE*stdout=&Streams[0],*stderr=&Streams[1];
FILE*fdopen(int bestandsingang,const char*methode_MODUS){(void)methode_MODUS;for(unsigned 순번=2;순번<18;순번++)if(!Streams[순번].사용량){Streams[순번].사용량=1;Streams[순번].fout=0;Streams[순번].bestandsingang=bestandsingang;return &Streams[순번];}fout=24;return 0;}
int fflush(FILE*Bestand_invoer){return Bestand_invoer&&Bestand_invoer->fout?-1:0;}
int fclose(FILE*Bestand_invoer){int 반환값=close(Bestand_invoer->bestandsingang);if(Bestand_invoer->fout)반환값=-1;Bestand_invoer->사용량=0;return 반환값;}
size_t fwrite(const void*gegevens_functie,size_t tekenreeks_gegevens,size_t item_AANTAL,FILE*Bestand_invoer){if(!tekenreeks_gegevens)return 0;if(item_AANTAL>SIZE_MAX/tekenreeks_gegevens){Bestand_invoer->fout=1;return 0;}long 반환값=write(Bestand_invoer->bestandsingang,gegevens_functie,tekenreeks_gegevens*item_AANTAL);if(반환값<0){Bestand_invoer->fout=1;return 0;}return (size_t)반환값/tekenreeks_gegevens;}
int fputc(int codepoint,FILE*Bestand_invoer){unsigned char SECONDE_WAARDE=codepoint;return fwrite(&SECONDE_WAARDE,1,1,Bestand_invoer)==1?SECONDE_WAARDE:EOF;}
int fputs(const char*tekenreeks_gegevens,FILE*Bestand_invoer){return fwrite(tekenreeks_gegevens,1,strlen(tekenreeks_gegevens),Bestand_invoer)==strlen(tekenreeks_gegevens)?0:EOF;}
static void 넣기(char*HR_gegevens,size_t 용량한도,size_t*actueel_functie,char codepoint){if(*actueel_functie+1<용량한도)HR_gegevens[*actueel_functie]=codepoint;(*actueel_functie)++;}
int vsnprintf(char*HR_gegevens,size_t 용량한도,const char*opmaak,va_list 가변인수){
    size_t actueel_functie=0;while(*opmaak){if(*opmaak!='%'){넣기(HR_gegevens,용량한도,&actueel_functie,*opmaak++);continue;}opmaak++;
        int 왼쪽=0,nulwaarde=0,대체값=0;while(*opmaak=='-'||*opmaak=='0'||*opmaak=='#'||*opmaak=='+'||*opmaak==' '){if(*opmaak=='-')왼쪽=1;if(*opmaak=='0')nulwaarde=1;if(*opmaak=='#')대체값=1;opmaak++;}
        int 너비=0,precisie_WAARDE=-1;if(*opmaak=='*'){너비=va_arg(가변인수,int);opmaak++;}else while(*opmaak>='0'&&*opmaak<='9')너비=너비*10+*opmaak++-'0';
        if(*opmaak=='.'){opmaak++;precisie_WAARDE=0;if(*opmaak=='*'){precisie_WAARDE=va_arg(가변인수,int);opmaak++;}else while(*opmaak>='0'&&*opmaak<='9')precisie_WAARDE=precisie_WAARDE*10+*opmaak++-'0';}
        int breed_teken=0;while(*opmaak=='l'||*opmaak=='z'||*opmaak=='t'||*opmaak=='j'||*opmaak=='h'){if(*opmaak!='h')breed_teken=1;opmaak++;}
        char TYPE_gebied=*opmaak?*opmaak++:0,bufferopslag[80];const char*tekenreeks_gegevens=bufferopslag;size_t item_AANTAL=0;
        if(TYPE_gebied=='s'){tekenreeks_gegevens=va_arg(가변인수,const char*);if(!tekenreeks_gegevens)tekenreeks_gegevens="(null)";item_AANTAL=strlen(tekenreeks_gegevens);if(precisie_WAARDE>=0&&item_AANTAL>(size_t)precisie_WAARDE)item_AANTAL=precisie_WAARDE;}
        else if(TYPE_gebied=='c'){bufferopslag[0]=va_arg(가변인수,int);item_AANTAL=1;}
        else if(TYPE_gebied=='%'){bufferopslag[0]='%';item_AANTAL=1;}
        else if(TYPE_gebied=='d'||TYPE_gebied=='i'||TYPE_gebied=='u'||TYPE_gebied=='x'||TYPE_gebied=='X'||TYPE_gebied=='o'||TYPE_gebied=='p'){
            unsigned long long WAARDE;int 음수표시=0;
            if(TYPE_gebied=='d'||TYPE_gebied=='i'){long long 임시값=breed_teken?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;WAARDE=음수표시?0-(unsigned long long)임시값:임시값;}
            else WAARDE=TYPE_gebied=='p'?(uintptr_t)va_arg(가변인수,void*):breed_teken?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Achtergrond_WAARDE=TYPE_gebied=='x'||TYPE_gebied=='X'||TYPE_gebied=='p'?16:TYPE_gebied=='o'?8:10;char cijfer_AANTAL[64];unsigned 사용량=0;
            do{cijfer_AANTAL[사용량++]="0123456789abcdef"[WAARDE%Achtergrond_WAARDE];WAARDE/=Achtergrond_WAARDE;}while(WAARDE);
            if(음수표시)bufferopslag[item_AANTAL++]='-';if(TYPE_gebied=='p'||(대체값&&Achtergrond_WAARDE==16)){bufferopslag[item_AANTAL++]='0';bufferopslag[item_AANTAL++]='x';}
            for(int vullen_WAARDE=(int)사용량;precisie_WAARDE>vullen_WAARDE&&item_AANTAL<sizeof(bufferopslag)-사용량;vullen_WAARDE++)bufferopslag[item_AANTAL++]='0';
            if(nulwaarde&&!왼쪽&&precisie_WAARDE<0)while(너비>(int)(item_AANTAL+사용량)&&item_AANTAL<sizeof(bufferopslag)-사용량)bufferopslag[item_AANTAL++]='0';
            while(사용량)bufferopslag[item_AANTAL++]=cijfer_AANTAL[--사용량];
        }else{bufferopslag[0]='?';item_AANTAL=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)item_AANTAL){넣기(HR_gegevens,용량한도,&actueel_functie,' ');너비--;}
        for(size_t 순번=0;순번<item_AANTAL;순번++)넣기(HR_gegevens,용량한도,&actueel_functie,tekenreeks_gegevens[순번]);while(왼쪽&&너비>(int)item_AANTAL){넣기(HR_gegevens,용량한도,&actueel_functie,' ');너비--;}
    }if(용량한도)HR_gegevens[actueel_functie<용량한도?actueel_functie:용량한도-1]=0;return actueel_functie;
}
int snprintf(char*HR_gegevens,size_t 용량한도,const char*Bestand_invoer,...){va_list 첫째값;va_start(첫째값,Bestand_invoer);int 반환값=vsnprintf(HR_gegevens,용량한도,Bestand_invoer,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*HR_gegevens,const char*Bestand_invoer,...){va_list 첫째값;va_start(첫째값,Bestand_invoer);int 반환값=vsnprintf(HR_gegevens,SIZE_MAX,Bestand_invoer,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*Stream_WAARDE,const char*Bestand_invoer,va_list 첫째값){char SECONDE_WAARDE[2048];int item_AANTAL=vsnprintf(SECONDE_WAARDE,sizeof(SECONDE_WAARDE),Bestand_invoer,첫째값);if(item_AANTAL>2047)item_AANTAL=2047;return fwrite(SECONDE_WAARDE,1,item_AANTAL,Stream_WAARDE)==(size_t)item_AANTAL?item_AANTAL:-1;}
int fprintf(FILE*Stream_WAARDE,const char*Bestand_invoer,...){va_list 첫째값;va_start(첫째값,Bestand_invoer);int 반환값=vfprintf(Stream_WAARDE,Bestand_invoer,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Bestand_invoer,...){va_list 첫째값;va_start(첫째값,Bestand_invoer);int 반환값=vfprintf(stdout,Bestand_invoer,첫째값);va_end(첫째값);return 반환값;}
