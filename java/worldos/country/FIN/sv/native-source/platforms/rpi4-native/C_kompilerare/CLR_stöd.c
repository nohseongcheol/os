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
static int fel;
int *__errno_location(void){return &fel;}
void exit(int status_värde){사용자호출(6,status_värde,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *check_uttryck,const char *filnamn,unsigned inmatningsrad,const char *metod_post_namn){fprintf(stderr,"cc assertion: %s %s:%u %s\n",check_uttryck,filnamn,inmatningsrad,metod_post_namn);exit(1);}
size_t strlen(const char*sträng_data){const char*data_placera=sträng_data;while(*data_placera)data_placera++;return data_placera-sträng_data;}
int strcmp(const char*첫째값,const char*SEKUND_värde){while(*첫째값&&*첫째값==*SEKUND_värde){첫째값++;SEKUND_värde++;}return (unsigned char)*첫째값-(unsigned char)*SEKUND_värde;}
int strncmp(const char*첫째값,const char*SEKUND_värde,size_t objekt_ANTAL){while(objekt_ANTAL--){unsigned char x_koordinat=*첫째값++,Y_koordinat=*SEKUND_värde++;if(x_koordinat!=Y_koordinat)return x_koordinat-Y_koordinat;if(!x_koordinat)return 0;}return 0;}
char *strcpy(char*mål_data,const char*sträng_data){char*반환값=mål_data;while((*mål_data++=*sträng_data++)){}return 반환값;}
char *strchr(const char*sträng_data,int kodpunkt){do{if(*sträng_data==(char)kodpunkt)return (char*)sträng_data;}while(*sträng_data++);return 0;}
char *strrchr(const char*sträng_data,int kodpunkt){const char*반환값=0;do{if(*sträng_data==(char)kodpunkt)반환값=sträng_data;}while(*sträng_data++);return (char*)반환값;}
char *strstr(const char*sträng_data,const char*Terminal_post){size_t objekt_ANTAL=strlen(Terminal_post);for(;*sträng_data;sträng_data++)if(!strncmp(sträng_data,Terminal_post,objekt_ANTAL))return (char*)sträng_data;return objekt_ANTAL?0:(char*)sträng_data;}
int memcmp(const void*첫째값,const void*SEKUND_värde,size_t objekt_ANTAL){const unsigned char*x_koordinat=첫째값,*Y_koordinat=SEKUND_värde;while(objekt_ANTAL--){if(*x_koordinat!=*Y_koordinat)return *x_koordinat-*Y_koordinat;x_koordinat++;Y_koordinat++;}return 0;}
void *memmove(void*mål_data,const void*sträng_data,size_t objekt_ANTAL){unsigned char*x_koordinat=mål_data;const unsigned char*Y_koordinat=sträng_data;if(x_koordinat<Y_koordinat){for(size_t 순번=0;순번<objekt_ANTAL;순번++)x_koordinat[순번]=Y_koordinat[순번];}else while(objekt_ANTAL){objekt_ANTAL--;x_koordinat[objekt_ANTAL]=Y_koordinat[objekt_ANTAL];}return mål_data;}
static unsigned char allokering_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct datablock {size_t Storlek;struct datablock*Nästa_objekt;int 남은공간;int Utfyllnad;uint64_t justering_enhet;} datablock;
static datablock *첫항목;
void free(void*data_placera){if(!data_placera)return;datablock*SEKUND_värde=(datablock*)data_placera-1;SEKUND_värde->남은공간=1;for(datablock*Nästa_FÖRSKJUTNING=첫항목;Nästa_FÖRSKJUTNING&&Nästa_FÖRSKJUTNING->Nästa_objekt;){if(Nästa_FÖRSKJUTNING->남은공간&&Nästa_FÖRSKJUTNING->Nästa_objekt->남은공간){Nästa_FÖRSKJUTNING->Storlek+=sizeof(datablock)+Nästa_FÖRSKJUTNING->Nästa_objekt->Storlek;Nästa_FÖRSKJUTNING->Nästa_objekt=Nästa_FÖRSKJUTNING->Nästa_objekt->Nästa_objekt;}else Nästa_FÖRSKJUTNING=Nästa_FÖRSKJUTNING->Nästa_objekt;}}
void *realloc(void*data_placera,size_t objekt_ANTAL){
    if(!objekt_ANTAL){free(data_placera);return 0;}if(objekt_ANTAL>sizeof(allokering_Arena)-sizeof(datablock))return 0;objekt_ANTAL=(objekt_ANTAL+15)&~(size_t)15;
    if(!첫항목){첫항목=(datablock*)allokering_Arena;첫항목->Storlek=sizeof(allokering_Arena)-sizeof(datablock);첫항목->남은공간=1;첫항목->Nästa_objekt=0;}
    datablock*Föregående_objekt=data_placera?(datablock*)data_placera-1:0;if(Föregående_objekt&&Föregående_objekt->Storlek>=objekt_ANTAL)return data_placera;
    for(datablock*SEKUND_värde=첫항목;SEKUND_värde;SEKUND_värde=SEKUND_värde->Nästa_objekt)if(SEKUND_värde->남은공간&&SEKUND_värde->Storlek>=objekt_ANTAL){
        if(SEKUND_värde->Storlek>=objekt_ANTAL+sizeof(datablock)+16){datablock*나머지부분=(datablock*)((unsigned char*)(SEKUND_värde+1)+objekt_ANTAL);나머지부분->Storlek=SEKUND_värde->Storlek-objekt_ANTAL-sizeof(datablock);나머지부분->Nästa_objekt=SEKUND_värde->Nästa_objekt;나머지부분->남은공간=1;SEKUND_värde->Nästa_objekt=나머지부분;SEKUND_värde->Storlek=objekt_ANTAL;}
        SEKUND_värde->남은공간=0;void*반환값=SEKUND_värde+1;if(Föregående_objekt){memcpy(반환값,data_placera,Föregående_objekt->Storlek);free(data_placera);}return 반환값;
    }fel=12;return 0;
}
void *malloc(size_t objekt_ANTAL){return realloc(0,objekt_ANTAL);}
void *calloc(size_t objekt_ANTAL,size_t sträng_data){if(sträng_data&&objekt_ANTAL>SIZE_MAX/sträng_data)return 0;void*data_placera=malloc(objekt_ANTAL*sträng_data);if(data_placera)memset(data_placera,0,objekt_ANTAL*sträng_data);return data_placera;}
unsigned long long strtoull(const char*sträng_data,char**avsluta_FÖRSKJUTNING,int Bakgrund_värde){
    const char*START_FÖRSKJUTNING=sträng_data;while(*sträng_data==' '||(*sträng_data>=9&&*sträng_data<=13))sträng_data++;int 음수여부=0;if(*sträng_data=='-'||*sträng_data=='+')음수여부=*sträng_data++=='-';
    if((!Bakgrund_värde||Bakgrund_värde==16)&&sträng_data[0]=='0'&&(sträng_data[1]=='x'||sträng_data[1]=='X')){Bakgrund_värde=16;sträng_data+=2;}if(!Bakgrund_värde)Bakgrund_värde=*sträng_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned kodpunkt=*sträng_data,mål_data=kodpunkt>='0'&&kodpunkt<='9'?kodpunkt-'0':kodpunkt>='a'&&kodpunkt<='z'?kodpunkt-'a'+10:kodpunkt>='A'&&kodpunkt<='Z'?kodpunkt-'A'+10:99;if(mål_data>=(unsigned)Bakgrund_värde)break;하나라도=1;sträng_data++;if(임시값>(~0ull-mål_data)/(unsigned)Bakgrund_värde){임시값=~0ull;fel=34;}else 임시값=임시값*Bakgrund_värde+mål_data;}
    if(avsluta_FÖRSKJUTNING)*avsluta_FÖRSKJUTNING=(char*)(하나라도?sträng_data:START_FÖRSKJUTNING);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*sträng_data,char**보조항목,int SEKUND_värde){return strtoull(sträng_data,보조항목,SEKUND_värde);}
long strtol(const char*sträng_data,char**보조항목,int SEKUND_värde){return (long)strtoull(sträng_data,보조항목,SEKUND_värde);}
int atoi(const char*sträng_data){return (int)strtol(sträng_data,0,10);}
long double ldexpl(long double x_koordinat,int objekt_ANTAL){while(objekt_ANTAL>0){x_koordinat*=2;objekt_ANTAL--;}while(objekt_ANTAL<0){x_koordinat/=2;objekt_ANTAL++;}return x_koordinat;}
long double strtold(const char*sträng_data,char**avsluta_FÖRSKJUTNING){
    const char*START_FÖRSKJUTNING=sträng_data;while(*sträng_data==' '||(*sträng_data>=9&&*sträng_data<=13))sträng_data++;int 음수여부=0;if(*sträng_data=='-'||*sträng_data=='+')음수여부=*sträng_data++=='-';
    int Bakgrund_värde=10;if(sträng_data[0]=='0'&&(sträng_data[1]=='x'||sträng_data[1]=='X')){Bakgrund_värde=16;sträng_data+=2;}long double 임시값=0,skala=1;int 소수부=0,하나라도=0;
    for(;;){int kodpunkt=*sträng_data,mål_data=kodpunkt>='0'&&kodpunkt<='9'?kodpunkt-'0':kodpunkt>='a'&&kodpunkt<='f'?kodpunkt-'a'+10:kodpunkt>='A'&&kodpunkt<='F'?kodpunkt-'A'+10:99;
        if(kodpunkt=='.'&&!소수부){소수부=1;sträng_data++;continue;}if(mål_data>=Bakgrund_värde)break;하나라도=1;sträng_data++;임시값=임시값*Bakgrund_värde+mål_data;if(소수부)skala*=Bakgrund_värde;
    }임시값/=skala;
    if((Bakgrund_värde==10&&(*sträng_data=='e'||*sträng_data=='E'))||(Bakgrund_värde==16&&(*sträng_data=='p'||*sträng_data=='P'))){const char*visa_värde=sträng_data++;int 빼기=0;if(*sträng_data=='-'||*sträng_data=='+')빼기=*sträng_data++=='-';int objekt_ANTAL=0,post_ANTAL=0;while(*sträng_data>='0'&&*sträng_data<='9'){post_ANTAL++;if(objekt_ANTAL<20000)objekt_ANTAL=objekt_ANTAL*10+*sträng_data-'0';sträng_data++;}if(!post_ANTAL)sträng_data=visa_värde;else{long double faktor=Bakgrund_värde==16?2:10;while(objekt_ANTAL-->0&&objekt_ANTAL<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(avsluta_FÖRSKJUTNING)*avsluta_FÖRSKJUTNING=(char*)(하나라도?sträng_data:START_FÖRSKJUTNING);return 음수여부?-임시값:임시값;
}
double strtod(const char*sträng_data,char**보조항목){return (double)strtold(sträng_data,보조항목);}float strtof(const char*sträng_data,char**보조항목){return (float)strtold(sträng_data,보조항목);}
void qsort(void*Bakgrund_värde,size_t objekt_ANTAL,size_t Storlek,int(*Jämför)(const void*,const void*)){
    unsigned char*data_placera=Bakgrund_värde;for(size_t 순번=1;순번<objekt_ANTAL;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Jämför(data_placera+(안쪽순번-1)*Storlek,data_placera+안쪽순번*Storlek)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Storlek;셋째순번++){unsigned char kodpunkt=data_placera[(안쪽순번-1)*Storlek+셋째순번];data_placera[(안쪽순번-1)*Storlek+셋째순번]=data_placera[안쪽순번*Storlek+셋째순번];data_placera[안쪽순번*Storlek+셋째순번]=kodpunkt;}
}
static struct {int 사용량,LETAUPP_INDEX;size_t position;} 열림[24];
static unsigned char utleverans[32768];static size_t utleverans_storlek,utleverans_placera;static int utleverans_skapa;
const unsigned char *C_utleverans(size_t *objekt_ANTAL){*objekt_ANTAL=utleverans_storlek;return utleverans;}
int open(const char*Namn,int konfiguration_BITS,...){
    if(!strcmp(Namn,"/@cc-output")){if(utleverans_skapa){fel=16;return -1;}utleverans_skapa=1;utleverans_storlek=utleverans_placera=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompilerare_Resurser)/sizeof(kompilerare_Resurser[0]);순번++)if(!strcmp(Namn,kompilerare_Resurser[순번].Namn)){
        if(konfiguration_BITS&3){fel=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].LETAUPP_INDEX=순번;열림[안쪽순번].position=0;return 128+안쪽순번;}fel=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Namn,konfiguration_BITS,0,0,0,0);if(반환값<0){fel=-반환값;return -1;}return 반환값;
}
int close(int filreferens){if(filreferens==100){utleverans_skapa=0;return 0;}if(filreferens>=128&&filreferens<152){열림[filreferens-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,filreferens,0,0,0,0,0);if(반환값<0){fel=-반환값;return -1;}return 0;}
long read(int filreferens,void*data,size_t objekt_ANTAL){
    if(filreferens>=128&&filreferens<152&&열림[filreferens-128].사용량){int 순번=filreferens-128;const kompilerare_resurs*반환값=&kompilerare_Resurser[열림[순번].LETAUPP_INDEX];size_t 왼쪽=반환값->Storlek-열림[순번].position;if(objekt_ANTAL>왼쪽)objekt_ANTAL=왼쪽;memcpy(data,반환값->data+열림[순번].position,objekt_ANTAL);열림[순번].position+=objekt_ANTAL;return objekt_ANTAL;}
    intptr_t 반환값=사용자호출(2,filreferens,(uintptr_t)data,objekt_ANTAL,0,0,0);if(반환값<0){fel=-반환값;return -1;}return 반환값;
}
long write(int filreferens,const void*data,size_t objekt_ANTAL){
    if(filreferens==100){if(objekt_ANTAL>sizeof(utleverans)-utleverans_placera){fel=28;return -1;}memcpy(utleverans+utleverans_placera,data,objekt_ANTAL);utleverans_placera+=objekt_ANTAL;if(utleverans_storlek<utleverans_placera)utleverans_storlek=utleverans_placera;return objekt_ANTAL;}
    intptr_t 반환값=사용자호출(1,filreferens,(uintptr_t)data,objekt_ANTAL,0,0,0);if(반환값<0){fel=-반환값;return -1;}return 반환값;
}
long lseek(int filreferens,long FÖRSKJUTNING_värde,int söka_origo){
    if(filreferens==100){long data_placera=FÖRSKJUTNING_värde+(söka_origo==0?0:söka_origo==1?utleverans_placera:utleverans_storlek);if(data_placera<0||(size_t)data_placera>sizeof(utleverans)){fel=22;return -1;}utleverans_placera=data_placera;return data_placera;}
    if(filreferens>=128&&filreferens<152&&열림[filreferens-128].사용량){int 순번=filreferens-128;long data_placera=FÖRSKJUTNING_värde+(söka_origo==0?0:söka_origo==1?열림[순번].position:kompilerare_Resurser[열림[순번].LETAUPP_INDEX].Storlek);if(data_placera<0||(size_t)data_placera>kompilerare_Resurser[열림[순번].LETAUPP_INDEX].Storlek){fel=22;return -1;}열림[순번].position=data_placera;return data_placera;}
    intptr_t 반환값=사용자호출(5,filreferens,FÖRSKJUTNING_värde,söka_origo,0,0,0);if(반환값<0){fel=-반환값;return -1;}return 반환값;
}
int unlink(const char*Namn){intptr_t 반환값=사용자호출(11,(uintptr_t)Namn,0,0,0,0,0);if(반환값<0){fel=-반환값;return -1;}return 반환값;}
char *realpath(const char*Namn,char*KR_data){if(!KR_data){KR_data=malloc(strlen(Namn)+1);if(!KR_data)return 0;}return strcpy(KR_data,Namn);}
char *getcwd(char*data_placera,size_t objekt_ANTAL){if(objekt_ANTAL<2){fel=34;return 0;}data_placera[0]='/';data_placera[1]=0;return data_placera;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_post){time_t 임시값=0;if(Terminal_post)*Terminal_post=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_post){(void)Terminal_post;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Flöden[18]={{1,0,1},{2,0,1}};FILE*stdout=&Flöden[0],*stderr=&Flöden[1];
FILE*fdopen(int filreferens,const char*metod_läge){(void)metod_läge;for(unsigned 순번=2;순번<18;순번++)if(!Flöden[순번].사용량){Flöden[순번].사용량=1;Flöden[순번].fel=0;Flöden[순번].filreferens=filreferens;return &Flöden[순번];}fel=24;return 0;}
int fflush(FILE*fil_post){return fil_post&&fil_post->fel?-1:0;}
int fclose(FILE*fil_post){int 반환값=close(fil_post->filreferens);if(fil_post->fel)반환값=-1;fil_post->사용량=0;return 반환값;}
size_t fwrite(const void*data_placera,size_t sträng_data,size_t objekt_ANTAL,FILE*fil_post){if(!sträng_data)return 0;if(objekt_ANTAL>SIZE_MAX/sträng_data){fil_post->fel=1;return 0;}long 반환값=write(fil_post->filreferens,data_placera,sträng_data*objekt_ANTAL);if(반환값<0){fil_post->fel=1;return 0;}return (size_t)반환값/sträng_data;}
int fputc(int kodpunkt,FILE*fil_post){unsigned char SEKUND_värde=kodpunkt;return fwrite(&SEKUND_värde,1,1,fil_post)==1?SEKUND_värde:EOF;}
int fputs(const char*sträng_data,FILE*fil_post){return fwrite(sträng_data,1,strlen(sträng_data),fil_post)==strlen(sträng_data)?0:EOF;}
static void 넣기(char*KR_data,size_t 용량한도,size_t*aktuellt_placera,char kodpunkt){if(*aktuellt_placera+1<용량한도)KR_data[*aktuellt_placera]=kodpunkt;(*aktuellt_placera)++;}
int vsnprintf(char*KR_data,size_t 용량한도,const char*format,va_list 가변인수){
    size_t aktuellt_placera=0;while(*format){if(*format!='%'){넣기(KR_data,용량한도,&aktuellt_placera,*format++);continue;}format++;
        int 왼쪽=0,nollvärde=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')nollvärde=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,precision_värde=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;precision_värde=0;if(*format=='*'){precision_värde=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')precision_värde=precision_värde*10+*format++-'0';}
        int brett_tecken=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')brett_tecken=1;format++;}
        char Typ_område=*format?*format++:0,buffertminne[80];const char*sträng_data=buffertminne;size_t objekt_ANTAL=0;
        if(Typ_område=='s'){sträng_data=va_arg(가변인수,const char*);if(!sträng_data)sträng_data="(null)";objekt_ANTAL=strlen(sträng_data);if(precision_värde>=0&&objekt_ANTAL>(size_t)precision_värde)objekt_ANTAL=precision_värde;}
        else if(Typ_område=='c'){buffertminne[0]=va_arg(가변인수,int);objekt_ANTAL=1;}
        else if(Typ_område=='%'){buffertminne[0]='%';objekt_ANTAL=1;}
        else if(Typ_område=='d'||Typ_område=='i'||Typ_område=='u'||Typ_område=='x'||Typ_område=='X'||Typ_område=='o'||Typ_område=='p'){
            unsigned long long värde;int 음수표시=0;
            if(Typ_område=='d'||Typ_område=='i'){long long 임시값=brett_tecken?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;värde=음수표시?0-(unsigned long long)임시값:임시값;}
            else värde=Typ_område=='p'?(uintptr_t)va_arg(가변인수,void*):brett_tecken?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Bakgrund_värde=Typ_område=='x'||Typ_område=='X'||Typ_område=='p'?16:Typ_område=='o'?8:10;char siffra_ANTAL[64];unsigned 사용량=0;
            do{siffra_ANTAL[사용량++]="0123456789abcdef"[värde%Bakgrund_värde];värde/=Bakgrund_värde;}while(värde);
            if(음수표시)buffertminne[objekt_ANTAL++]='-';if(Typ_område=='p'||(대체값&&Bakgrund_värde==16)){buffertminne[objekt_ANTAL++]='0';buffertminne[objekt_ANTAL++]='x';}
            for(int Fyll_värde=(int)사용량;precision_värde>Fyll_värde&&objekt_ANTAL<sizeof(buffertminne)-사용량;Fyll_värde++)buffertminne[objekt_ANTAL++]='0';
            if(nollvärde&&!왼쪽&&precision_värde<0)while(너비>(int)(objekt_ANTAL+사용량)&&objekt_ANTAL<sizeof(buffertminne)-사용량)buffertminne[objekt_ANTAL++]='0';
            while(사용량)buffertminne[objekt_ANTAL++]=siffra_ANTAL[--사용량];
        }else{buffertminne[0]='?';objekt_ANTAL=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)objekt_ANTAL){넣기(KR_data,용량한도,&aktuellt_placera,' ');너비--;}
        for(size_t 순번=0;순번<objekt_ANTAL;순번++)넣기(KR_data,용량한도,&aktuellt_placera,sträng_data[순번]);while(왼쪽&&너비>(int)objekt_ANTAL){넣기(KR_data,용량한도,&aktuellt_placera,' ');너비--;}
    }if(용량한도)KR_data[aktuellt_placera<용량한도?aktuellt_placera:용량한도-1]=0;return aktuellt_placera;
}
int snprintf(char*KR_data,size_t 용량한도,const char*fil_post,...){va_list 첫째값;va_start(첫째값,fil_post);int 반환값=vsnprintf(KR_data,용량한도,fil_post,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_data,const char*fil_post,...){va_list 첫째값;va_start(첫째값,fil_post);int 반환값=vsnprintf(KR_data,SIZE_MAX,fil_post,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*flöde_värde,const char*fil_post,va_list 첫째값){char SEKUND_värde[2048];int objekt_ANTAL=vsnprintf(SEKUND_värde,sizeof(SEKUND_värde),fil_post,첫째값);if(objekt_ANTAL>2047)objekt_ANTAL=2047;return fwrite(SEKUND_värde,1,objekt_ANTAL,flöde_värde)==(size_t)objekt_ANTAL?objekt_ANTAL:-1;}
int fprintf(FILE*flöde_värde,const char*fil_post,...){va_list 첫째값;va_start(첫째값,fil_post);int 반환값=vfprintf(flöde_värde,fil_post,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*fil_post,...){va_list 첫째값;va_start(첫째값,fil_post);int 반환값=vfprintf(stdout,fil_post,첫째값);va_end(첫째값);return 반환값;}
