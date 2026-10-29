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
static int VIRHE;
int *__errno_location(void){return &VIRHE;}
void exit(int Tila_ARVO){사용자호출(6,Tila_ARVO,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *sekki_lauseke,const char *tiedoston_nimi,unsigned syöterivi,const char *menetelmä_merkintä_nimi){fprintf(stderr,"cc assertion: %s %s:%u %s\n",sekki_lauseke,tiedoston_nimi,syöterivi,menetelmä_merkintä_nimi);exit(1);}
size_t strlen(const char*merkkijono_data){const char*data_toimi=merkkijono_data;while(*data_toimi)data_toimi++;return data_toimi-merkkijono_data;}
int strcmp(const char*첫째값,const char*SEKUNNIT_ARVO){while(*첫째값&&*첫째값==*SEKUNNIT_ARVO){첫째값++;SEKUNNIT_ARVO++;}return (unsigned char)*첫째값-(unsigned char)*SEKUNNIT_ARVO;}
int strncmp(const char*첫째값,const char*SEKUNNIT_ARVO,size_t kohde_LASKE){while(kohde_LASKE--){unsigned char x_koordinaatti=*첫째값++,Y_koordinaatti=*SEKUNNIT_ARVO++;if(x_koordinaatti!=Y_koordinaatti)return x_koordinaatti-Y_koordinaatti;if(!x_koordinaatti)return 0;}return 0;}
char *strcpy(char*kohde_data,const char*merkkijono_data){char*반환값=kohde_data;while((*kohde_data++=*merkkijono_data++)){}return 반환값;}
char *strchr(const char*merkkijono_data,int merkkikoodi){do{if(*merkkijono_data==(char)merkkikoodi)return (char*)merkkijono_data;}while(*merkkijono_data++);return 0;}
char *strrchr(const char*merkkijono_data,int merkkikoodi){const char*반환값=0;do{if(*merkkijono_data==(char)merkkikoodi)반환값=merkkijono_data;}while(*merkkijono_data++);return (char*)반환값;}
char *strstr(const char*merkkijono_data,const char*Pääte_merkintä){size_t kohde_LASKE=strlen(Pääte_merkintä);for(;*merkkijono_data;merkkijono_data++)if(!strncmp(merkkijono_data,Pääte_merkintä,kohde_LASKE))return (char*)merkkijono_data;return kohde_LASKE?0:(char*)merkkijono_data;}
int memcmp(const void*첫째값,const void*SEKUNNIT_ARVO,size_t kohde_LASKE){const unsigned char*x_koordinaatti=첫째값,*Y_koordinaatti=SEKUNNIT_ARVO;while(kohde_LASKE--){if(*x_koordinaatti!=*Y_koordinaatti)return *x_koordinaatti-*Y_koordinaatti;x_koordinaatti++;Y_koordinaatti++;}return 0;}
void *memmove(void*kohde_data,const void*merkkijono_data,size_t kohde_LASKE){unsigned char*x_koordinaatti=kohde_data;const unsigned char*Y_koordinaatti=merkkijono_data;if(x_koordinaatti<Y_koordinaatti){for(size_t 순번=0;순번<kohde_LASKE;순번++)x_koordinaatti[순번]=Y_koordinaatti[순번];}else while(kohde_LASKE){kohde_LASKE--;x_koordinaatti[kohde_LASKE]=Y_koordinaatti[kohde_LASKE];}return kohde_data;}
static unsigned char varaus_Areena[6*1024*1024] __attribute__((aligned(16)));
typedef struct tietolohko {size_t Koko;struct tietolohko*Seuraava_kohde;int 남은공간;int täyttö;uint64_t tasaus_osio;} tietolohko;
static tietolohko *첫항목;
void free(void*data_toimi){if(!data_toimi)return;tietolohko*SEKUNNIT_ARVO=(tietolohko*)data_toimi-1;SEKUNNIT_ARVO->남은공간=1;for(tietolohko*Seuraava_SIIRTYMÄ=첫항목;Seuraava_SIIRTYMÄ&&Seuraava_SIIRTYMÄ->Seuraava_kohde;){if(Seuraava_SIIRTYMÄ->남은공간&&Seuraava_SIIRTYMÄ->Seuraava_kohde->남은공간){Seuraava_SIIRTYMÄ->Koko+=sizeof(tietolohko)+Seuraava_SIIRTYMÄ->Seuraava_kohde->Koko;Seuraava_SIIRTYMÄ->Seuraava_kohde=Seuraava_SIIRTYMÄ->Seuraava_kohde->Seuraava_kohde;}else Seuraava_SIIRTYMÄ=Seuraava_SIIRTYMÄ->Seuraava_kohde;}}
void *realloc(void*data_toimi,size_t kohde_LASKE){
    if(!kohde_LASKE){free(data_toimi);return 0;}if(kohde_LASKE>sizeof(varaus_Areena)-sizeof(tietolohko))return 0;kohde_LASKE=(kohde_LASKE+15)&~(size_t)15;
    if(!첫항목){첫항목=(tietolohko*)varaus_Areena;첫항목->Koko=sizeof(varaus_Areena)-sizeof(tietolohko);첫항목->남은공간=1;첫항목->Seuraava_kohde=0;}
    tietolohko*Edellinen_kohde=data_toimi?(tietolohko*)data_toimi-1:0;if(Edellinen_kohde&&Edellinen_kohde->Koko>=kohde_LASKE)return data_toimi;
    for(tietolohko*SEKUNNIT_ARVO=첫항목;SEKUNNIT_ARVO;SEKUNNIT_ARVO=SEKUNNIT_ARVO->Seuraava_kohde)if(SEKUNNIT_ARVO->남은공간&&SEKUNNIT_ARVO->Koko>=kohde_LASKE){
        if(SEKUNNIT_ARVO->Koko>=kohde_LASKE+sizeof(tietolohko)+16){tietolohko*나머지부분=(tietolohko*)((unsigned char*)(SEKUNNIT_ARVO+1)+kohde_LASKE);나머지부분->Koko=SEKUNNIT_ARVO->Koko-kohde_LASKE-sizeof(tietolohko);나머지부분->Seuraava_kohde=SEKUNNIT_ARVO->Seuraava_kohde;나머지부분->남은공간=1;SEKUNNIT_ARVO->Seuraava_kohde=나머지부분;SEKUNNIT_ARVO->Koko=kohde_LASKE;}
        SEKUNNIT_ARVO->남은공간=0;void*반환값=SEKUNNIT_ARVO+1;if(Edellinen_kohde){memcpy(반환값,data_toimi,Edellinen_kohde->Koko);free(data_toimi);}return 반환값;
    }VIRHE=12;return 0;
}
void *malloc(size_t kohde_LASKE){return realloc(0,kohde_LASKE);}
void *calloc(size_t kohde_LASKE,size_t merkkijono_data){if(merkkijono_data&&kohde_LASKE>SIZE_MAX/merkkijono_data)return 0;void*data_toimi=malloc(kohde_LASKE*merkkijono_data);if(data_toimi)memset(data_toimi,0,kohde_LASKE*merkkijono_data);return data_toimi;}
unsigned long long strtoull(const char*merkkijono_data,char**lopettaa_puhelu_SIIRTYMÄ,int Tausta_ARVO){
    const char*alku_SIIRTYMÄ=merkkijono_data;while(*merkkijono_data==' '||(*merkkijono_data>=9&&*merkkijono_data<=13))merkkijono_data++;int 음수여부=0;if(*merkkijono_data=='-'||*merkkijono_data=='+')음수여부=*merkkijono_data++=='-';
    if((!Tausta_ARVO||Tausta_ARVO==16)&&merkkijono_data[0]=='0'&&(merkkijono_data[1]=='x'||merkkijono_data[1]=='X')){Tausta_ARVO=16;merkkijono_data+=2;}if(!Tausta_ARVO)Tausta_ARVO=*merkkijono_data=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned merkkikoodi=*merkkijono_data,kohde_data=merkkikoodi>='0'&&merkkikoodi<='9'?merkkikoodi-'0':merkkikoodi>='a'&&merkkikoodi<='z'?merkkikoodi-'a'+10:merkkikoodi>='A'&&merkkikoodi<='Z'?merkkikoodi-'A'+10:99;if(kohde_data>=(unsigned)Tausta_ARVO)break;하나라도=1;merkkijono_data++;if(임시값>(~0ull-kohde_data)/(unsigned)Tausta_ARVO){임시값=~0ull;VIRHE=34;}else 임시값=임시값*Tausta_ARVO+kohde_data;}
    if(lopettaa_puhelu_SIIRTYMÄ)*lopettaa_puhelu_SIIRTYMÄ=(char*)(하나라도?merkkijono_data:alku_SIIRTYMÄ);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*merkkijono_data,char**보조항목,int SEKUNNIT_ARVO){return strtoull(merkkijono_data,보조항목,SEKUNNIT_ARVO);}
long strtol(const char*merkkijono_data,char**보조항목,int SEKUNNIT_ARVO){return (long)strtoull(merkkijono_data,보조항목,SEKUNNIT_ARVO);}
int atoi(const char*merkkijono_data){return (int)strtol(merkkijono_data,0,10);}
long double ldexpl(long double x_koordinaatti,int kohde_LASKE){while(kohde_LASKE>0){x_koordinaatti*=2;kohde_LASKE--;}while(kohde_LASKE<0){x_koordinaatti/=2;kohde_LASKE++;}return x_koordinaatti;}
long double strtold(const char*merkkijono_data,char**lopettaa_puhelu_SIIRTYMÄ){
    const char*alku_SIIRTYMÄ=merkkijono_data;while(*merkkijono_data==' '||(*merkkijono_data>=9&&*merkkijono_data<=13))merkkijono_data++;int 음수여부=0;if(*merkkijono_data=='-'||*merkkijono_data=='+')음수여부=*merkkijono_data++=='-';
    int Tausta_ARVO=10;if(merkkijono_data[0]=='0'&&(merkkijono_data[1]=='x'||merkkijono_data[1]=='X')){Tausta_ARVO=16;merkkijono_data+=2;}long double 임시값=0,skaalata=1;int 소수부=0,하나라도=0;
    for(;;){int merkkikoodi=*merkkijono_data,kohde_data=merkkikoodi>='0'&&merkkikoodi<='9'?merkkikoodi-'0':merkkikoodi>='a'&&merkkikoodi<='f'?merkkikoodi-'a'+10:merkkikoodi>='A'&&merkkikoodi<='F'?merkkikoodi-'A'+10:99;
        if(merkkikoodi=='.'&&!소수부){소수부=1;merkkijono_data++;continue;}if(kohde_data>=Tausta_ARVO)break;하나라도=1;merkkijono_data++;임시값=임시값*Tausta_ARVO+kohde_data;if(소수부)skaalata*=Tausta_ARVO;
    }임시값/=skaalata;
    if((Tausta_ARVO==10&&(*merkkijono_data=='e'||*merkkijono_data=='E'))||(Tausta_ARVO==16&&(*merkkijono_data=='p'||*merkkijono_data=='P'))){const char*näyttää_ARVO=merkkijono_data++;int 빼기=0;if(*merkkijono_data=='-'||*merkkijono_data=='+')빼기=*merkkijono_data++=='-';int kohde_LASKE=0,merkintä_LASKE=0;while(*merkkijono_data>='0'&&*merkkijono_data<='9'){merkintä_LASKE++;if(kohde_LASKE<20000)kohde_LASKE=kohde_LASKE*10+*merkkijono_data-'0';merkkijono_data++;}if(!merkintä_LASKE)merkkijono_data=näyttää_ARVO;else{long double tekijä=Tausta_ARVO==16?2:10;while(kohde_LASKE-->0&&kohde_LASKE<200000)임시값=빼기?임시값/tekijä:임시값*tekijä;}}
    if(lopettaa_puhelu_SIIRTYMÄ)*lopettaa_puhelu_SIIRTYMÄ=(char*)(하나라도?merkkijono_data:alku_SIIRTYMÄ);return 음수여부?-임시값:임시값;
}
double strtod(const char*merkkijono_data,char**보조항목){return (double)strtold(merkkijono_data,보조항목);}float strtof(const char*merkkijono_data,char**보조항목){return (float)strtold(merkkijono_data,보조항목);}
void qsort(void*Tausta_ARVO,size_t kohde_LASKE,size_t Koko,int(*Vertaa)(const void*,const void*)){
    unsigned char*data_toimi=Tausta_ARVO;for(size_t 순번=1;순번<kohde_LASKE;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Vertaa(data_toimi+(안쪽순번-1)*Koko,data_toimi+안쪽순번*Koko)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Koko;셋째순번++){unsigned char merkkikoodi=data_toimi[(안쪽순번-1)*Koko+셋째순번];data_toimi[(안쪽순번-1)*Koko+셋째순번]=data_toimi[안쪽순번*Koko+셋째순번];data_toimi[안쪽순번*Koko+셋째순번]=merkkikoodi;}
}
static struct {int 사용량,HAKU_INDEKSI;size_t paikka;} 열림[24];
static unsigned char tulos[32768];static size_t tulos_muuttaa_kokoa,tulos_toimi;static int tulos_avata;
const unsigned char *C_tulos(size_t *kohde_LASKE){*kohde_LASKE=tulos_muuttaa_kokoa;return tulos;}
int open(const char*Nimi,int määritys_Background_Intelligent_Transfer_Service,...){
    if(!strcmp(Nimi,"/@cc-output")){if(tulos_avata){VIRHE=16;return -1;}tulos_avata=1;tulos_muuttaa_kokoa=tulos_toimi=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(kääntäjä_Resurssit)/sizeof(kääntäjä_Resurssit[0]);순번++)if(!strcmp(Nimi,kääntäjä_Resurssit[순번].Nimi)){
        if(määritys_Background_Intelligent_Transfer_Service&3){VIRHE=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].HAKU_INDEKSI=순번;열림[안쪽순번].paikka=0;return 128+안쪽순번;}VIRHE=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nimi,määritys_Background_Intelligent_Transfer_Service,0,0,0,0);if(반환값<0){VIRHE=-반환값;return -1;}return 반환값;
}
int close(int Tiedosto_kahva){if(Tiedosto_kahva==100){tulos_avata=0;return 0;}if(Tiedosto_kahva>=128&&Tiedosto_kahva<152){열림[Tiedosto_kahva-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Tiedosto_kahva,0,0,0,0,0);if(반환값<0){VIRHE=-반환값;return -1;}return 0;}
long read(int Tiedosto_kahva,void*data,size_t kohde_LASKE){
    if(Tiedosto_kahva>=128&&Tiedosto_kahva<152&&열림[Tiedosto_kahva-128].사용량){int 순번=Tiedosto_kahva-128;const kääntäjä_resurssi*반환값=&kääntäjä_Resurssit[열림[순번].HAKU_INDEKSI];size_t 왼쪽=반환값->Koko-열림[순번].paikka;if(kohde_LASKE>왼쪽)kohde_LASKE=왼쪽;memcpy(data,반환값->data+열림[순번].paikka,kohde_LASKE);열림[순번].paikka+=kohde_LASKE;return kohde_LASKE;}
    intptr_t 반환값=사용자호출(2,Tiedosto_kahva,(uintptr_t)data,kohde_LASKE,0,0,0);if(반환값<0){VIRHE=-반환값;return -1;}return 반환값;
}
long write(int Tiedosto_kahva,const void*data,size_t kohde_LASKE){
    if(Tiedosto_kahva==100){if(kohde_LASKE>sizeof(tulos)-tulos_toimi){VIRHE=28;return -1;}memcpy(tulos+tulos_toimi,data,kohde_LASKE);tulos_toimi+=kohde_LASKE;if(tulos_muuttaa_kokoa<tulos_toimi)tulos_muuttaa_kokoa=tulos_toimi;return kohde_LASKE;}
    intptr_t 반환값=사용자호출(1,Tiedosto_kahva,(uintptr_t)data,kohde_LASKE,0,0,0);if(반환값<0){VIRHE=-반환값;return -1;}return 반환값;
}
long lseek(int Tiedosto_kahva,long SIIRTYMÄ_ARVO,int hae_origo){
    if(Tiedosto_kahva==100){long data_toimi=SIIRTYMÄ_ARVO+(hae_origo==0?0:hae_origo==1?tulos_toimi:tulos_muuttaa_kokoa);if(data_toimi<0||(size_t)data_toimi>sizeof(tulos)){VIRHE=22;return -1;}tulos_toimi=data_toimi;return data_toimi;}
    if(Tiedosto_kahva>=128&&Tiedosto_kahva<152&&열림[Tiedosto_kahva-128].사용량){int 순번=Tiedosto_kahva-128;long data_toimi=SIIRTYMÄ_ARVO+(hae_origo==0?0:hae_origo==1?열림[순번].paikka:kääntäjä_Resurssit[열림[순번].HAKU_INDEKSI].Koko);if(data_toimi<0||(size_t)data_toimi>kääntäjä_Resurssit[열림[순번].HAKU_INDEKSI].Koko){VIRHE=22;return -1;}열림[순번].paikka=data_toimi;return data_toimi;}
    intptr_t 반환값=사용자호출(5,Tiedosto_kahva,SIIRTYMÄ_ARVO,hae_origo,0,0,0);if(반환값<0){VIRHE=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nimi){intptr_t 반환값=사용자호출(11,(uintptr_t)Nimi,0,0,0,0,0);if(반환값<0){VIRHE=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nimi,char*KR_data){if(!KR_data){KR_data=malloc(strlen(Nimi)+1);if(!KR_data)return 0;}return strcpy(KR_data,Nimi);}
char *getcwd(char*data_toimi,size_t kohde_LASKE){if(kohde_LASKE<2){VIRHE=34;return 0;}data_toimi[0]='/';data_toimi[1]=0;return data_toimi;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Pääte_merkintä){time_t 임시값=0;if(Pääte_merkintä)*Pääte_merkintä=임시값;return 임시값;}
struct tm *localtime(const time_t*Pääte_merkintä){(void)Pääte_merkintä;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Viestivirrat[18]={{1,0,1},{2,0,1}};FILE*stdout=&Viestivirrat[0],*stderr=&Viestivirrat[1];
FILE*fdopen(int Tiedosto_kahva,const char*menetelmä_tila){(void)menetelmä_tila;for(unsigned 순번=2;순번<18;순번++)if(!Viestivirrat[순번].사용량){Viestivirrat[순번].사용량=1;Viestivirrat[순번].VIRHE=0;Viestivirrat[순번].Tiedosto_kahva=Tiedosto_kahva;return &Viestivirrat[순번];}VIRHE=24;return 0;}
int fflush(FILE*Tiedosto_merkintä){return Tiedosto_merkintä&&Tiedosto_merkintä->VIRHE?-1:0;}
int fclose(FILE*Tiedosto_merkintä){int 반환값=close(Tiedosto_merkintä->Tiedosto_kahva);if(Tiedosto_merkintä->VIRHE)반환값=-1;Tiedosto_merkintä->사용량=0;return 반환값;}
size_t fwrite(const void*data_toimi,size_t merkkijono_data,size_t kohde_LASKE,FILE*Tiedosto_merkintä){if(!merkkijono_data)return 0;if(kohde_LASKE>SIZE_MAX/merkkijono_data){Tiedosto_merkintä->VIRHE=1;return 0;}long 반환값=write(Tiedosto_merkintä->Tiedosto_kahva,data_toimi,merkkijono_data*kohde_LASKE);if(반환값<0){Tiedosto_merkintä->VIRHE=1;return 0;}return (size_t)반환값/merkkijono_data;}
int fputc(int merkkikoodi,FILE*Tiedosto_merkintä){unsigned char SEKUNNIT_ARVO=merkkikoodi;return fwrite(&SEKUNNIT_ARVO,1,1,Tiedosto_merkintä)==1?SEKUNNIT_ARVO:EOF;}
int fputs(const char*merkkijono_data,FILE*Tiedosto_merkintä){return fwrite(merkkijono_data,1,strlen(merkkijono_data),Tiedosto_merkintä)==strlen(merkkijono_data)?0:EOF;}
static void 넣기(char*KR_data,size_t 용량한도,size_t*nykyinen_toimi,char merkkikoodi){if(*nykyinen_toimi+1<용량한도)KR_data[*nykyinen_toimi]=merkkikoodi;(*nykyinen_toimi)++;}
int vsnprintf(char*KR_data,size_t 용량한도,const char*muoto,va_list 가변인수){
    size_t nykyinen_toimi=0;while(*muoto){if(*muoto!='%'){넣기(KR_data,용량한도,&nykyinen_toimi,*muoto++);continue;}muoto++;
        int 왼쪽=0,nolla_ARVO=0,대체값=0;while(*muoto=='-'||*muoto=='0'||*muoto=='#'||*muoto=='+'||*muoto==' '){if(*muoto=='-')왼쪽=1;if(*muoto=='0')nolla_ARVO=1;if(*muoto=='#')대체값=1;muoto++;}
        int 너비=0,tarkkuus_ARVO_2bff91c1=-1;if(*muoto=='*'){너비=va_arg(가변인수,int);muoto++;}else while(*muoto>='0'&&*muoto<='9')너비=너비*10+*muoto++-'0';
        if(*muoto=='.'){muoto++;tarkkuus_ARVO_2bff91c1=0;if(*muoto=='*'){tarkkuus_ARVO_2bff91c1=va_arg(가변인수,int);muoto++;}else while(*muoto>='0'&&*muoto<='9')tarkkuus_ARVO_2bff91c1=tarkkuus_ARVO_2bff91c1*10+*muoto++-'0';}
        int leveä_merkki=0;while(*muoto=='l'||*muoto=='z'||*muoto=='t'||*muoto=='j'||*muoto=='h'){if(*muoto!='h')leveä_merkki=1;muoto++;}
        char TYYPPI_alue=*muoto?*muoto++:0,puskurimuisti[80];const char*merkkijono_data=puskurimuisti;size_t kohde_LASKE=0;
        if(TYYPPI_alue=='s'){merkkijono_data=va_arg(가변인수,const char*);if(!merkkijono_data)merkkijono_data="(null)";kohde_LASKE=strlen(merkkijono_data);if(tarkkuus_ARVO_2bff91c1>=0&&kohde_LASKE>(size_t)tarkkuus_ARVO_2bff91c1)kohde_LASKE=tarkkuus_ARVO_2bff91c1;}
        else if(TYYPPI_alue=='c'){puskurimuisti[0]=va_arg(가변인수,int);kohde_LASKE=1;}
        else if(TYYPPI_alue=='%'){puskurimuisti[0]='%';kohde_LASKE=1;}
        else if(TYYPPI_alue=='d'||TYYPPI_alue=='i'||TYYPPI_alue=='u'||TYYPPI_alue=='x'||TYYPPI_alue=='X'||TYYPPI_alue=='o'||TYYPPI_alue=='p'){
            unsigned long long ARVO;int 음수표시=0;
            if(TYYPPI_alue=='d'||TYYPPI_alue=='i'){long long 임시값=leveä_merkki?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;ARVO=음수표시?0-(unsigned long long)임시값:임시값;}
            else ARVO=TYYPPI_alue=='p'?(uintptr_t)va_arg(가변인수,void*):leveä_merkki?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Tausta_ARVO=TYYPPI_alue=='x'||TYYPPI_alue=='X'||TYYPPI_alue=='p'?16:TYYPPI_alue=='o'?8:10;char numero_LASKE[64];unsigned 사용량=0;
            do{numero_LASKE[사용량++]="0123456789abcdef"[ARVO%Tausta_ARVO];ARVO/=Tausta_ARVO;}while(ARVO);
            if(음수표시)puskurimuisti[kohde_LASKE++]='-';if(TYYPPI_alue=='p'||(대체값&&Tausta_ARVO==16)){puskurimuisti[kohde_LASKE++]='0';puskurimuisti[kohde_LASKE++]='x';}
            for(int täyttö_ARVO=(int)사용량;tarkkuus_ARVO_2bff91c1>täyttö_ARVO&&kohde_LASKE<sizeof(puskurimuisti)-사용량;täyttö_ARVO++)puskurimuisti[kohde_LASKE++]='0';
            if(nolla_ARVO&&!왼쪽&&tarkkuus_ARVO_2bff91c1<0)while(너비>(int)(kohde_LASKE+사용량)&&kohde_LASKE<sizeof(puskurimuisti)-사용량)puskurimuisti[kohde_LASKE++]='0';
            while(사용량)puskurimuisti[kohde_LASKE++]=numero_LASKE[--사용량];
        }else{puskurimuisti[0]='?';kohde_LASKE=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)kohde_LASKE){넣기(KR_data,용량한도,&nykyinen_toimi,' ');너비--;}
        for(size_t 순번=0;순번<kohde_LASKE;순번++)넣기(KR_data,용량한도,&nykyinen_toimi,merkkijono_data[순번]);while(왼쪽&&너비>(int)kohde_LASKE){넣기(KR_data,용량한도,&nykyinen_toimi,' ');너비--;}
    }if(용량한도)KR_data[nykyinen_toimi<용량한도?nykyinen_toimi:용량한도-1]=0;return nykyinen_toimi;
}
int snprintf(char*KR_data,size_t 용량한도,const char*Tiedosto_merkintä,...){va_list 첫째값;va_start(첫째값,Tiedosto_merkintä);int 반환값=vsnprintf(KR_data,용량한도,Tiedosto_merkintä,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*KR_data,const char*Tiedosto_merkintä,...){va_list 첫째값;va_start(첫째값,Tiedosto_merkintä);int 반환값=vsnprintf(KR_data,SIZE_MAX,Tiedosto_merkintä,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*virta_ARVO,const char*Tiedosto_merkintä,va_list 첫째값){char SEKUNNIT_ARVO[2048];int kohde_LASKE=vsnprintf(SEKUNNIT_ARVO,sizeof(SEKUNNIT_ARVO),Tiedosto_merkintä,첫째값);if(kohde_LASKE>2047)kohde_LASKE=2047;return fwrite(SEKUNNIT_ARVO,1,kohde_LASKE,virta_ARVO)==(size_t)kohde_LASKE?kohde_LASKE:-1;}
int fprintf(FILE*virta_ARVO,const char*Tiedosto_merkintä,...){va_list 첫째값;va_start(첫째값,Tiedosto_merkintä);int 반환값=vfprintf(virta_ARVO,Tiedosto_merkintä,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Tiedosto_merkintä,...){va_list 첫째값;va_start(첫째값,Tiedosto_merkintä);int 반환값=vfprintf(stdout,Tiedosto_merkintä,첫째값);va_end(첫째값);return 반환값;}
