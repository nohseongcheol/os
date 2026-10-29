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
static int feil;
int *__errno_location(void){return &feil;}
void exit(int status_VERDI){사용자호출(6,status_VERDI,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *sjekk_uttrykk,const char *Fil,unsigned Linje,const char *metode_oppføring_navn){fprintf(stderr,"cc assertion: %s %s:%u %s\n",sjekk_uttrykk,Fil,Linje,metode_oppføring_navn);exit(1);}
size_t strlen(const char*streng_data){const char*data_plassere=streng_data;while(*data_plassere)data_plassere++;return data_plassere-streng_data;}
int strcmp(const char*첫째값,const char*SEKUND_VERDI){while(*첫째값&&*첫째값==*SEKUND_VERDI){첫째값++;SEKUND_VERDI++;}return (unsigned char)*첫째값-(unsigned char)*SEKUND_VERDI;}
int strncmp(const char*첫째값,const char*SEKUND_VERDI,size_t vare_ANTALL){while(vare_ANTALL--){unsigned char x_koordinat=*첫째값++,Y_koordinat=*SEKUND_VERDI++;if(x_koordinat!=Y_koordinat)return x_koordinat-Y_koordinat;if(!x_koordinat)return 0;}return 0;}
char *strcpy(char*mål_data,const char*streng_data){char*반환값=mål_data;while((*mål_data++=*streng_data++)){}return 반환값;}
char *strchr(const char*streng_data,int tegnkode){do{if(*streng_data==(char)tegnkode)return (char*)streng_data;}while(*streng_data++);return 0;}
char *strrchr(const char*streng_data,int tegnkode){const char*반환값=0;do{if(*streng_data==(char)tegnkode)반환값=streng_data;}while(*streng_data++);return (char*)반환값;}
char *strstr(const char*streng_data,const char*Terminal_oppføring){size_t vare_ANTALL=strlen(Terminal_oppføring);for(;*streng_data;streng_data++)if(!strncmp(streng_data,Terminal_oppføring,vare_ANTALL))return (char*)streng_data;return vare_ANTALL?0:(char*)streng_data;}
int memcmp(const void*첫째값,const void*SEKUND_VERDI,size_t vare_ANTALL){const unsigned char*x_koordinat=첫째값,*Y_koordinat=SEKUND_VERDI;while(vare_ANTALL--){if(*x_koordinat!=*Y_koordinat)return *x_koordinat-*Y_koordinat;x_koordinat++;Y_koordinat++;}return 0;}
void *memmove(void*mål_data,const void*streng_data,size_t vare_ANTALL){unsigned char*x_koordinat=mål_data;const unsigned char*Y_koordinat=streng_data;if(x_koordinat<Y_koordinat){for(size_t 순번=0;순번<vare_ANTALL;순번++)x_koordinat[순번]=Y_koordinat[순번];}else while(vare_ANTALL){vare_ANTALL--;x_koordinat[vare_ANTALL]=Y_koordinat[vare_ANTALL];}return mål_data;}
static unsigned char fordeling_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct data_blokk {size_t Størrelse;struct data_blokk*Neste_vare;int 남은공간;int utfylling;uint64_t justering_enhet;} data_blokk;
static data_blokk *첫항목;
void free(void*data_plassere){if(!data_plassere)return;data_blokk*SEKUND_VERDI=(data_blokk*)data_plassere-1;SEKUND_VERDI->남은공간=1;for(data_blokk*Neste_FORSKYVNING=첫항목;Neste_FORSKYVNING&&Neste_FORSKYVNING->Neste_vare;){if(Neste_FORSKYVNING->남은공간&&Neste_FORSKYVNING->Neste_vare->남은공간){Neste_FORSKYVNING->Størrelse+=sizeof(data_blokk)+Neste_FORSKYVNING->Neste_vare->Størrelse;Neste_FORSKYVNING->Neste_vare=Neste_FORSKYVNING->Neste_vare->Neste_vare;}else Neste_FORSKYVNING=Neste_FORSKYVNING->Neste_vare;}}
void *realloc(void*data_plassere,size_t vare_ANTALL){
    if(!vare_ANTALL){free(data_plassere);return 0;}if(vare_ANTALL>sizeof(fordeling_Arena)-sizeof(data_blokk))return 0;vare_ANTALL=(vare_ANTALL+15)&~(size_t)15;
    if(!첫항목){첫항목=(data_blokk*)fordeling_Arena;첫항목->Størrelse=sizeof(fordeling_Arena)-sizeof(data_blokk);첫항목->남은공간=1;첫항목->Neste_vare=0;}
    data_blokk*Forrige_vare=data_plassere?(data_blokk*)data_plassere-1:0;if(Forrige_vare&&Forrige_vare->Størrelse>=vare_ANTALL)return data_plassere;
    for(data_blokk*SEKUND_VERDI=첫항목;SEKUND_VERDI;SEKUND_VERDI=SEKUND_VERDI->Neste_vare)if(SEKUND_VERDI->남은공간&&SEKUND_VERDI->Størrelse>=vare_ANTALL){
        if(SEKUND_VERDI->Størrelse>=vare_ANTALL+sizeof(data_blokk)+16){data_blokk*나머지부분=(data_blokk*)((unsigned char*)(SEKUND_VERDI+1)+vare_ANTALL);나머지부분->Størrelse=SEKUND_VERDI->Størrelse-vare_ANTALL-sizeof(data_blokk);나머지부분->Neste_vare=SEKUND_VERDI->Neste_vare;나머지부분->남은공간=1;SEKUND_VERDI->Neste_vare=나머지부분;SEKUND_VERDI->Størrelse=vare_ANTALL;}
        SEKUND_VERDI->남은공간=0;void*반환값=SEKUND_VERDI+1;if(Forrige_vare){memcpy(반환값,data_plassere,Forrige_vare->Størrelse);free(data_plassere);}return 반환값;
    }feil=12;return 0;
}
void *malloc(size_t vare_ANTALL){return realloc(0,vare_ANTALL);}
void *calloc(size_t vare_ANTALL,size_t streng_data){if(streng_data&&vare_ANTALL>SIZE_MAX/streng_data)return 0;void*data_plassere=malloc(vare_ANTALL*streng_data);if(data_plassere)memset(data_plassere,0,vare_ANTALL*streng_data);return data_plassere;}
unsigned long long strtoull(const char*streng_data,char**avslutte_en_samtale_FORSKYVNING,int bakgrunn_VERDI){
    const char*START_FORSKYVNING=streng_data;while(*streng_data==' '||(*streng_data>=9&&*streng_data<=13))streng_data++;int 음수여부=0;if(*streng_data=='-'||*streng_data=='+')음수여부=*streng_data++=='-';
    if((!bakgrunn_VERDI||bakgrunn_VERDI==16)&&streng_data[0]=='0'&&(streng_data[1]=='x'||streng_data[1]=='X')){bakgrunn_VERDI=16;streng_data+=2;}if(!bakgrunn_VERDI)bakgrunn_VERDI=*streng_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned tegnkode=*streng_data,mål_data=tegnkode>='0'&&tegnkode<='9'?tegnkode-'0':tegnkode>='a'&&tegnkode<='z'?tegnkode-'a'+10:tegnkode>='A'&&tegnkode<='Z'?tegnkode-'A'+10:99;if(mål_data>=(unsigned)bakgrunn_VERDI)break;하나라도=1;streng_data++;if(임시값>(~0ull-mål_data)/(unsigned)bakgrunn_VERDI){임시값=~0ull;feil=34;}else 임시값=임시값*bakgrunn_VERDI+mål_data;}
    if(avslutte_en_samtale_FORSKYVNING)*avslutte_en_samtale_FORSKYVNING=(char*)(하나라도?streng_data:START_FORSKYVNING);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*streng_data,char**보조항목,int SEKUND_VERDI){return strtoull(streng_data,보조항목,SEKUND_VERDI);}
long strtol(const char*streng_data,char**보조항목,int SEKUND_VERDI){return (long)strtoull(streng_data,보조항목,SEKUND_VERDI);}
int atoi(const char*streng_data){return (int)strtol(streng_data,0,10);}
long double ldexpl(long double x_koordinat,int vare_ANTALL){while(vare_ANTALL>0){x_koordinat*=2;vare_ANTALL--;}while(vare_ANTALL<0){x_koordinat/=2;vare_ANTALL++;}return x_koordinat;}
long double strtold(const char*streng_data,char**avslutte_en_samtale_FORSKYVNING){
    const char*START_FORSKYVNING=streng_data;while(*streng_data==' '||(*streng_data>=9&&*streng_data<=13))streng_data++;int 음수여부=0;if(*streng_data=='-'||*streng_data=='+')음수여부=*streng_data++=='-';
    int bakgrunn_VERDI=10;if(streng_data[0]=='0'&&(streng_data[1]=='x'||streng_data[1]=='X')){bakgrunn_VERDI=16;streng_data+=2;}long double 임시값=0,skalere=1;int 소수부=0,하나라도=0;
    for(;;){int tegnkode=*streng_data,mål_data=tegnkode>='0'&&tegnkode<='9'?tegnkode-'0':tegnkode>='a'&&tegnkode<='f'?tegnkode-'a'+10:tegnkode>='A'&&tegnkode<='F'?tegnkode-'A'+10:99;
        if(tegnkode=='.'&&!소수부){소수부=1;streng_data++;continue;}if(mål_data>=bakgrunn_VERDI)break;하나라도=1;streng_data++;임시값=임시값*bakgrunn_VERDI+mål_data;if(소수부)skalere*=bakgrunn_VERDI;
    }임시값/=skalere;
    if((bakgrunn_VERDI==10&&(*streng_data=='e'||*streng_data=='E'))||(bakgrunn_VERDI==16&&(*streng_data=='p'||*streng_data=='P'))){const char*vise_VERDI_487749b8=streng_data++;int 빼기=0;if(*streng_data=='-'||*streng_data=='+')빼기=*streng_data++=='-';int vare_ANTALL=0,oppføring_ANTALL=0;while(*streng_data>='0'&&*streng_data<='9'){oppføring_ANTALL++;if(vare_ANTALL<20000)vare_ANTALL=vare_ANTALL*10+*streng_data-'0';streng_data++;}if(!oppføring_ANTALL)streng_data=vise_VERDI_487749b8;else{long double faktor=bakgrunn_VERDI==16?2:10;while(vare_ANTALL-->0&&vare_ANTALL<200000)임시값=빼기?임시값/faktor:임시값*faktor;}}
    if(avslutte_en_samtale_FORSKYVNING)*avslutte_en_samtale_FORSKYVNING=(char*)(하나라도?streng_data:START_FORSKYVNING);return 음수여부?-임시값:임시값;
}
double strtod(const char*streng_data,char**보조항목){return (double)strtold(streng_data,보조항목);}float strtof(const char*streng_data,char**보조항목){return (float)strtold(streng_data,보조항목);}
void qsort(void*bakgrunn_VERDI,size_t vare_ANTALL,size_t Størrelse,int(*Sammenlign)(const void*,const void*)){
    unsigned char*data_plassere=bakgrunn_VERDI;for(size_t 순번=1;순번<vare_ANTALL;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Sammenlign(data_plassere+(안쪽순번-1)*Størrelse,data_plassere+안쪽순번*Størrelse)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Størrelse;셋째순번++){unsigned char tegnkode=data_plassere[(안쪽순번-1)*Størrelse+셋째순번];data_plassere[(안쪽순번-1)*Størrelse+셋째순번]=data_plassere[안쪽순번*Størrelse+셋째순번];data_plassere[안쪽순번*Størrelse+셋째순번]=tegnkode;}
}
static struct {int 사용량,Oppslag_INDEKS;size_t Posisjon;} 열림[24];
static unsigned char produksjon[32768];static size_t produksjon_skalere,produksjon_plassere;static int produksjon_åpen;
const unsigned char *C_produksjon(size_t *vare_ANTALL){*vare_ANTALL=produksjon_skalere;return produksjon;}
int open(const char*Navn,int konfigurasjon_BITS,...){
    if(!strcmp(Navn,"/@cc-output")){if(produksjon_åpen){feil=16;return -1;}produksjon_åpen=1;produksjon_skalere=produksjon_plassere=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kompilator_Ressurser)/sizeof(kompilator_Ressurser[0]);순번++)if(!strcmp(Navn,kompilator_Ressurser[순번].Navn)){
        if(konfigurasjon_BITS&3){feil=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].Oppslag_INDEKS=순번;열림[안쪽순번].Posisjon=0;return 128+안쪽순번;}feil=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Navn,konfigurasjon_BITS,0,0,0,0);if(반환값<0){feil=-반환값;return -1;}return 반환값;
}
int close(int Fil_håndtak){if(Fil_håndtak==100){produksjon_åpen=0;return 0;}if(Fil_håndtak>=128&&Fil_håndtak<152){열림[Fil_håndtak-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Fil_håndtak,0,0,0,0,0);if(반환값<0){feil=-반환값;return -1;}return 0;}
long read(int Fil_håndtak,void*data,size_t vare_ANTALL){
    if(Fil_håndtak>=128&&Fil_håndtak<152&&열림[Fil_håndtak-128].사용량){int 순번=Fil_håndtak-128;const kompilator_ressurs*반환값=&kompilator_Ressurser[열림[순번].Oppslag_INDEKS];size_t 왼쪽=반환값->Størrelse-열림[순번].Posisjon;if(vare_ANTALL>왼쪽)vare_ANTALL=왼쪽;memcpy(data,반환값->data+열림[순번].Posisjon,vare_ANTALL);열림[순번].Posisjon+=vare_ANTALL;return vare_ANTALL;}
    intptr_t 반환값=사용자호출(2,Fil_håndtak,(uintptr_t)data,vare_ANTALL,0,0,0);if(반환값<0){feil=-반환값;return -1;}return 반환값;
}
long write(int Fil_håndtak,const void*data,size_t vare_ANTALL){
    if(Fil_håndtak==100){if(vare_ANTALL>sizeof(produksjon)-produksjon_plassere){feil=28;return -1;}memcpy(produksjon+produksjon_plassere,data,vare_ANTALL);produksjon_plassere+=vare_ANTALL;if(produksjon_skalere<produksjon_plassere)produksjon_skalere=produksjon_plassere;return vare_ANTALL;}
    intptr_t 반환값=사용자호출(1,Fil_håndtak,(uintptr_t)data,vare_ANTALL,0,0,0);if(반환값<0){feil=-반환값;return -1;}return 반환값;
}
long lseek(int Fil_håndtak,long FORSKYVNING_VERDI,int søk_origo){
    if(Fil_håndtak==100){long data_plassere=FORSKYVNING_VERDI+(søk_origo==0?0:søk_origo==1?produksjon_plassere:produksjon_skalere);if(data_plassere<0||(size_t)data_plassere>sizeof(produksjon)){feil=22;return -1;}produksjon_plassere=data_plassere;return data_plassere;}
    if(Fil_håndtak>=128&&Fil_håndtak<152&&열림[Fil_håndtak-128].사용량){int 순번=Fil_håndtak-128;long data_plassere=FORSKYVNING_VERDI+(søk_origo==0?0:søk_origo==1?열림[순번].Posisjon:kompilator_Ressurser[열림[순번].Oppslag_INDEKS].Størrelse);if(data_plassere<0||(size_t)data_plassere>kompilator_Ressurser[열림[순번].Oppslag_INDEKS].Størrelse){feil=22;return -1;}열림[순번].Posisjon=data_plassere;return data_plassere;}
    intptr_t 반환값=사용자호출(5,Fil_håndtak,FORSKYVNING_VERDI,søk_origo,0,0,0);if(반환값<0){feil=-반환값;return -1;}return 반환값;
}
int unlink(const char*Navn){intptr_t 반환값=사용자호출(11,(uintptr_t)Navn,0,0,0,0,0);if(반환값<0){feil=-반환값;return -1;}return 반환값;}
char *realpath(const char*Navn,char*KR_data){if(!KR_data){KR_data=malloc(strlen(Navn)+1);if(!KR_data)return 0;}return strcpy(KR_data,Navn);}
char *getcwd(char*data_plassere,size_t vare_ANTALL){if(vare_ANTALL<2){feil=34;return 0;}data_plassere[0]='/';data_plassere[1]=0;return data_plassere;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_oppføring){time_t 임시값=0;if(Terminal_oppføring)*Terminal_oppføring=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_oppføring){(void)Terminal_oppføring;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Strømmer[18]={{1,0,1},{2,0,1}};FILE*stdout=&Strømmer[0],*stderr=&Strømmer[1];
FILE*fdopen(int Fil_håndtak,const char*metode_MODUS){(void)metode_MODUS;for(unsigned 순번=2;순번<18;순번++)if(!Strømmer[순번].사용량){Strømmer[순번].사용량=1;Strømmer[순번].feil=0;Strømmer[순번].Fil_håndtak=Fil_håndtak;return &Strømmer[순번];}feil=24;return 0;}
int fflush(FILE*Fil_oppføring){return Fil_oppføring&&Fil_oppføring->feil?-1:0;}
int fclose(FILE*Fil_oppføring){int 반환값=close(Fil_oppføring->Fil_håndtak);if(Fil_oppføring->feil)반환값=-1;Fil_oppføring->사용량=0;return 반환값;}
size_t fwrite(const void*data_plassere,size_t streng_data,size_t vare_ANTALL,FILE*Fil_oppføring){if(!streng_data)return 0;if(vare_ANTALL>SIZE_MAX/streng_data){Fil_oppføring->feil=1;return 0;}long 반환값=write(Fil_oppføring->Fil_håndtak,data_plassere,streng_data*vare_ANTALL);if(반환값<0){Fil_oppføring->feil=1;return 0;}return (size_t)반환값/streng_data;}
int fputc(int tegnkode,FILE*Fil_oppføring){unsigned char SEKUND_VERDI=tegnkode;return fwrite(&SEKUND_VERDI,1,1,Fil_oppføring)==1?SEKUND_VERDI:EOF;}
int fputs(const char*streng_data,FILE*Fil_oppføring){return fwrite(streng_data,1,strlen(streng_data),Fil_oppføring)==strlen(streng_data)?0:EOF;}
static void 넣기(char*KR_data,size_t 용량한도,size_t*betalt_plassere,char tegnkode){if(*betalt_plassere+1<용량한도)KR_data[*betalt_plassere]=tegnkode;(*betalt_plassere)++;}
int vsnprintf(char*KR_data,size_t 용량한도,const char*format,va_list 가변인수){
    size_t betalt_plassere=0;while(*format){if(*format!='%'){넣기(KR_data,용량한도,&betalt_plassere,*format++);continue;}format++;
        int 왼쪽=0,null_VERDI=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')null_VERDI=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,presisjon_VERDI=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;presisjon_VERDI=0;if(*format=='*'){presisjon_VERDI=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')presisjon_VERDI=presisjon_VERDI*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char Type_område=*format?*format++:0,bufre_lager[80];const char*streng_data=bufre_lager;size_t vare_ANTALL=0;
        if(Type_område=='s'){streng_data=va_arg(가변인수,const char*);if(!streng_data)streng_data="(null)";vare_ANTALL=strlen(streng_data);if(presisjon_VERDI>=0&&vare_ANTALL>(size_t)presisjon_VERDI)vare_ANTALL=presisjon_VERDI;}
        else if(Type_område=='c'){bufre_lager[0]=va_arg(가변인수,int);vare_ANTALL=1;}
        else if(Type_område=='%'){bufre_lager[0]='%';vare_ANTALL=1;}
        else if(Type_område=='d'||Type_område=='i'||Type_område=='u'||Type_område=='x'||Type_område=='X'||Type_område=='o'||Type_område=='p'){
            unsigned long long VERDI;int 음수표시=0;
            if(Type_område=='d'||Type_område=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VERDI=음수표시?0-(unsigned long long)임시값:임시값;}
            else VERDI=Type_område=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned bakgrunn_VERDI=Type_område=='x'||Type_område=='X'||Type_område=='p'?16:Type_område=='o'?8:10;char siffer_ANTALL[64];unsigned 사용량=0;
            do{siffer_ANTALL[사용량++]="0123456789abcdef"[VERDI%bakgrunn_VERDI];VERDI/=bakgrunn_VERDI;}while(VERDI);
            if(음수표시)bufre_lager[vare_ANTALL++]='-';if(Type_område=='p'||(대체값&&bakgrunn_VERDI==16)){bufre_lager[vare_ANTALL++]='0';bufre_lager[vare_ANTALL++]='x';}
            for(int fyll_VERDI=(int)사용량;presisjon_VERDI>fyll_VERDI&&vare_ANTALL<sizeof(bufre_lager)-사용량;fyll_VERDI++)bufre_lager[vare_ANTALL++]='0';
            if(null_VERDI&&!왼쪽&&presisjon_VERDI<0)while(너비>(int)(vare_ANTALL+사용량)&&vare_ANTALL<sizeof(bufre_lager)-사용량)bufre_lager[vare_ANTALL++]='0';
            while(사용량)bufre_lager[vare_ANTALL++]=siffer_ANTALL[--사용량];
        }else{bufre_lager[0]='?';vare_ANTALL=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)vare_ANTALL){넣기(KR_data,용량한도,&betalt_plassere,' ');너비--;}
        for(size_t 순번=0;순번<vare_ANTALL;순번++)넣기(KR_data,용량한도,&betalt_plassere,streng_data[순번]);while(왼쪽&&너비>(int)vare_ANTALL){넣기(KR_data,용량한도,&betalt_plassere,' ');너비--;}
    }if(용량한도)KR_data[betalt_plassere<용량한도?betalt_plassere:용량한도-1]=0;return betalt_plassere;
}
int snprintf(char*KR_data,size_t 용량한도,const char*Fil_oppføring,...){va_list 첫째값;va_start(첫째값,Fil_oppføring);int 반환값=vsnprintf(KR_data,용량한도,Fil_oppføring,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_data,const char*Fil_oppføring,...){va_list 첫째값;va_start(첫째값,Fil_oppføring);int 반환값=vsnprintf(KR_data,SIZE_MAX,Fil_oppføring,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*strøm_VERDI,const char*Fil_oppføring,va_list 첫째값){char SEKUND_VERDI[2048];int vare_ANTALL=vsnprintf(SEKUND_VERDI,sizeof(SEKUND_VERDI),Fil_oppføring,첫째값);if(vare_ANTALL>2047)vare_ANTALL=2047;return fwrite(SEKUND_VERDI,1,vare_ANTALL,strøm_VERDI)==(size_t)vare_ANTALL?vare_ANTALL:-1;}
int fprintf(FILE*strøm_VERDI,const char*Fil_oppføring,...){va_list 첫째값;va_start(첫째값,Fil_oppføring);int 반환값=vfprintf(strøm_VERDI,Fil_oppføring,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Fil_oppføring,...){va_list 첫째값;va_start(첫째값,Fil_oppføring);int 반환값=vfprintf(stdout,Fil_oppføring,첫째값);va_end(첫째값);return 반환값;}
