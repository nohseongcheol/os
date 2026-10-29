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
static int s_ha_produït_un_error;
int *__errno_location(void){return &s_ha_produït_un_error;}
void exit(int Estat_VALOR){사용자호출(6,Estat_VALOR,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *xec_expressió,const char *Fitxer,unsigned línia,const char *함수이름){fprintf(stderr,"cc assertion: %s %s:%u %s\n",xec_expressió,Fitxer,línia,함수이름);exit(1);}
size_t strlen(const char*cadena_dades){const char*dades_càrrec=cadena_dades;while(*dades_càrrec)dades_càrrec++;return dades_càrrec-cadena_dades;}
int strcmp(const char*첫째값,const char*SEGON_VALOR){while(*첫째값&&*첫째값==*SEGON_VALOR){첫째값++;SEGON_VALOR++;}return (unsigned char)*첫째값-(unsigned char)*SEGON_VALOR;}
int strncmp(const char*첫째값,const char*SEGON_VALOR,size_t element_COMPT){while(element_COMPT--){unsigned char X_coordenada=*첫째값++,Y_coordenada=*SEGON_VALOR++;if(X_coordenada!=Y_coordenada)return X_coordenada-Y_coordenada;if(!X_coordenada)return 0;}return 0;}
char *strcpy(char*destinació_dades,const char*cadena_dades){char*반환값=destinació_dades;while((*destinació_dades++=*cadena_dades++)){}return 반환값;}
char *strchr(const char*cadena_dades,int codi_de_caràcter){do{if(*cadena_dades==(char)codi_de_caràcter)return (char*)cadena_dades;}while(*cadena_dades++);return 0;}
char *strrchr(const char*cadena_dades,int codi_de_caràcter){const char*반환값=0;do{if(*cadena_dades==(char)codi_de_caràcter)반환값=cadena_dades;}while(*cadena_dades++);return (char*)반환값;}
char *strstr(const char*cadena_dades,const char*Terminal_introducció){size_t element_COMPT=strlen(Terminal_introducció);for(;*cadena_dades;cadena_dades++)if(!strncmp(cadena_dades,Terminal_introducció,element_COMPT))return (char*)cadena_dades;return element_COMPT?0:(char*)cadena_dades;}
int memcmp(const void*첫째값,const void*SEGON_VALOR,size_t element_COMPT){const unsigned char*X_coordenada=첫째값,*Y_coordenada=SEGON_VALOR;while(element_COMPT--){if(*X_coordenada!=*Y_coordenada)return *X_coordenada-*Y_coordenada;X_coordenada++;Y_coordenada++;}return 0;}
void *memmove(void*destinació_dades,const void*cadena_dades,size_t element_COMPT){unsigned char*X_coordenada=destinació_dades;const unsigned char*Y_coordenada=cadena_dades;if(X_coordenada<Y_coordenada){for(size_t 순번=0;순번<element_COMPT;순번++)X_coordenada[순번]=Y_coordenada[순번];}else while(element_COMPT){element_COMPT--;X_coordenada[element_COMPT]=Y_coordenada[element_COMPT];}return destinació_dades;}
static unsigned char assignació_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct dades_bloquejar {size_t Mida;struct dades_bloquejar*Següent_element;int 남은공간;int 채울크기;uint64_t alineació_lliçó;} dades_bloquejar;
static dades_bloquejar *첫항목;
void free(void*dades_càrrec){if(!dades_càrrec)return;dades_bloquejar*SEGON_VALOR=(dades_bloquejar*)dades_càrrec-1;SEGON_VALOR->남은공간=1;for(dades_bloquejar*Següent_DESPLAÇAMENT=첫항목;Següent_DESPLAÇAMENT&&Següent_DESPLAÇAMENT->Següent_element;){if(Següent_DESPLAÇAMENT->남은공간&&Següent_DESPLAÇAMENT->Següent_element->남은공간){Següent_DESPLAÇAMENT->Mida+=sizeof(dades_bloquejar)+Següent_DESPLAÇAMENT->Següent_element->Mida;Següent_DESPLAÇAMENT->Següent_element=Següent_DESPLAÇAMENT->Següent_element->Següent_element;}else Següent_DESPLAÇAMENT=Següent_DESPLAÇAMENT->Següent_element;}}
void *realloc(void*dades_càrrec,size_t element_COMPT){
    if(!element_COMPT){free(dades_càrrec);return 0;}if(element_COMPT>sizeof(assignació_Arena)-sizeof(dades_bloquejar))return 0;element_COMPT=(element_COMPT+15)&~(size_t)15;
    if(!첫항목){첫항목=(dades_bloquejar*)assignació_Arena;첫항목->Mida=sizeof(assignació_Arena)-sizeof(dades_bloquejar);첫항목->남은공간=1;첫항목->Següent_element=0;}
    dades_bloquejar*이전=dades_càrrec?(dades_bloquejar*)dades_càrrec-1:0;if(이전&&이전->Mida>=element_COMPT)return dades_càrrec;
    for(dades_bloquejar*SEGON_VALOR=첫항목;SEGON_VALOR;SEGON_VALOR=SEGON_VALOR->Següent_element)if(SEGON_VALOR->남은공간&&SEGON_VALOR->Mida>=element_COMPT){
        if(SEGON_VALOR->Mida>=element_COMPT+sizeof(dades_bloquejar)+16){dades_bloquejar*나머지부분=(dades_bloquejar*)((unsigned char*)(SEGON_VALOR+1)+element_COMPT);나머지부분->Mida=SEGON_VALOR->Mida-element_COMPT-sizeof(dades_bloquejar);나머지부분->Següent_element=SEGON_VALOR->Següent_element;나머지부분->남은공간=1;SEGON_VALOR->Següent_element=나머지부분;SEGON_VALOR->Mida=element_COMPT;}
        SEGON_VALOR->남은공간=0;void*반환값=SEGON_VALOR+1;if(이전){memcpy(반환값,dades_càrrec,이전->Mida);free(dades_càrrec);}return 반환값;
    }s_ha_produït_un_error=12;return 0;
}
void *malloc(size_t element_COMPT){return realloc(0,element_COMPT);}
void *calloc(size_t element_COMPT,size_t cadena_dades){if(cadena_dades&&element_COMPT>SIZE_MAX/cadena_dades)return 0;void*dades_càrrec=malloc(element_COMPT*cadena_dades);if(dades_càrrec)memset(dades_càrrec,0,element_COMPT*cadena_dades);return dades_càrrec;}
unsigned long long strtoull(const char*cadena_dades,char**finalitzar_DESPLAÇAMENT,int Fons_VALOR){
    const char*Inici_DESPLAÇAMENT=cadena_dades;while(*cadena_dades==' '||(*cadena_dades>=9&&*cadena_dades<=13))cadena_dades++;int 음수여부=0;if(*cadena_dades=='-'||*cadena_dades=='+')음수여부=*cadena_dades++=='-';
    if((!Fons_VALOR||Fons_VALOR==16)&&cadena_dades[0]=='0'&&(cadena_dades[1]=='x'||cadena_dades[1]=='X')){Fons_VALOR=16;cadena_dades+=2;}if(!Fons_VALOR)Fons_VALOR=*cadena_dades=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned codi_de_caràcter=*cadena_dades,destinació_dades=codi_de_caràcter>='0'&&codi_de_caràcter<='9'?codi_de_caràcter-'0':codi_de_caràcter>='a'&&codi_de_caràcter<='z'?codi_de_caràcter-'a'+10:codi_de_caràcter>='A'&&codi_de_caràcter<='Z'?codi_de_caràcter-'A'+10:99;if(destinació_dades>=(unsigned)Fons_VALOR)break;하나라도=1;cadena_dades++;if(임시값>(~0ull-destinació_dades)/(unsigned)Fons_VALOR){임시값=~0ull;s_ha_produït_un_error=34;}else 임시값=임시값*Fons_VALOR+destinació_dades;}
    if(finalitzar_DESPLAÇAMENT)*finalitzar_DESPLAÇAMENT=(char*)(하나라도?cadena_dades:Inici_DESPLAÇAMENT);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*cadena_dades,char**보조항목,int SEGON_VALOR){return strtoull(cadena_dades,보조항목,SEGON_VALOR);}
long strtol(const char*cadena_dades,char**보조항목,int SEGON_VALOR){return (long)strtoull(cadena_dades,보조항목,SEGON_VALOR);}
int atoi(const char*cadena_dades){return (int)strtol(cadena_dades,0,10);}
long double ldexpl(long double X_coordenada,int element_COMPT){while(element_COMPT>0){X_coordenada*=2;element_COMPT--;}while(element_COMPT<0){X_coordenada/=2;element_COMPT++;}return X_coordenada;}
long double strtold(const char*cadena_dades,char**finalitzar_DESPLAÇAMENT){
    const char*Inici_DESPLAÇAMENT=cadena_dades;while(*cadena_dades==' '||(*cadena_dades>=9&&*cadena_dades<=13))cadena_dades++;int 음수여부=0;if(*cadena_dades=='-'||*cadena_dades=='+')음수여부=*cadena_dades++=='-';
    int Fons_VALOR=10;if(cadena_dades[0]=='0'&&(cadena_dades[1]=='x'||cadena_dades[1]=='X')){Fons_VALOR=16;cadena_dades+=2;}long double 임시값=0,ajustar_l_escala=1;int 소수부=0,하나라도=0;
    for(;;){int codi_de_caràcter=*cadena_dades,destinació_dades=codi_de_caràcter>='0'&&codi_de_caràcter<='9'?codi_de_caràcter-'0':codi_de_caràcter>='a'&&codi_de_caràcter<='f'?codi_de_caràcter-'a'+10:codi_de_caràcter>='A'&&codi_de_caràcter<='F'?codi_de_caràcter-'A'+10:99;
        if(codi_de_caràcter=='.'&&!소수부){소수부=1;cadena_dades++;continue;}if(destinació_dades>=Fons_VALOR)break;하나라도=1;cadena_dades++;임시값=임시값*Fons_VALOR+destinació_dades;if(소수부)ajustar_l_escala*=Fons_VALOR;
    }임시값/=ajustar_l_escala;
    if((Fons_VALOR==10&&(*cadena_dades=='e'||*cadena_dades=='E'))||(Fons_VALOR==16&&(*cadena_dades=='p'||*cadena_dades=='P'))){const char*mostrar_VALOR=cadena_dades++;int 빼기=0;if(*cadena_dades=='-'||*cadena_dades=='+')빼기=*cadena_dades++=='-';int element_COMPT=0,introducció_COMPT=0;while(*cadena_dades>='0'&&*cadena_dades<='9'){introducció_COMPT++;if(element_COMPT<20000)element_COMPT=element_COMPT*10+*cadena_dades-'0';cadena_dades++;}if(!introducció_COMPT)cadena_dades=mostrar_VALOR;else{long double factor=Fons_VALOR==16?2:10;while(element_COMPT-->0&&element_COMPT<200000)임시값=빼기?임시값/factor:임시값*factor;}}
    if(finalitzar_DESPLAÇAMENT)*finalitzar_DESPLAÇAMENT=(char*)(하나라도?cadena_dades:Inici_DESPLAÇAMENT);return 음수여부?-임시값:임시값;
}
double strtod(const char*cadena_dades,char**보조항목){return (double)strtold(cadena_dades,보조항목);}float strtof(const char*cadena_dades,char**보조항목){return (float)strtold(cadena_dades,보조항목);}
void qsort(void*Fons_VALOR,size_t element_COMPT,size_t Mida,int(*comparar)(const void*,const void*)){
    unsigned char*dades_càrrec=Fons_VALOR;for(size_t 순번=1;순번<element_COMPT;순번++)for(size_t 안쪽순번=순번;안쪽순번&&comparar(dades_càrrec+(안쪽순번-1)*Mida,dades_càrrec+안쪽순번*Mida)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Mida;셋째순번++){unsigned char codi_de_caràcter=dades_càrrec[(안쪽순번-1)*Mida+셋째순번];dades_càrrec[(안쪽순번-1)*Mida+셋째순번]=dades_càrrec[안쪽순번*Mida+셋째순번];dades_càrrec[안쪽순번*Mida+셋째순번]=codi_de_caràcter;}
}
static struct {int 사용량,Cerca_INDEX;size_t Posició;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *element_COMPT){*element_COMPT=출력크기;return 출력결과;}
int open(const char*Nom,int configuració_Servei_de_transferència_intel_ligent_en_segon_terme,...){
    if(!strcmp(Nom,"/@cc-output")){if(출력열림){s_ha_produït_un_error=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Nom,번역기자원들[순번].Nom)){
        if(configuració_Servei_de_transferència_intel_ligent_en_segon_terme&3){s_ha_produït_un_error=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].Cerca_INDEX=순번;열림[안쪽순번].Posició=0;return 128+안쪽순번;}s_ha_produït_un_error=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nom,configuració_Servei_de_transferència_intel_ligent_en_segon_terme,0,0,0,0);if(반환값<0){s_ha_produït_un_error=-반환값;return -1;}return 반환값;
}
int close(int arxiu_control_7f4cdfd5){if(arxiu_control_7f4cdfd5==100){출력열림=0;return 0;}if(arxiu_control_7f4cdfd5>=128&&arxiu_control_7f4cdfd5<152){열림[arxiu_control_7f4cdfd5-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,arxiu_control_7f4cdfd5,0,0,0,0,0);if(반환값<0){s_ha_produït_un_error=-반환값;return -1;}return 0;}
long read(int arxiu_control_7f4cdfd5,void*dades,size_t element_COMPT){
    if(arxiu_control_7f4cdfd5>=128&&arxiu_control_7f4cdfd5<152&&열림[arxiu_control_7f4cdfd5-128].사용량){int 순번=arxiu_control_7f4cdfd5-128;const 번역기자원*반환값=&번역기자원들[열림[순번].Cerca_INDEX];size_t 왼쪽=반환값->Mida-열림[순번].Posició;if(element_COMPT>왼쪽)element_COMPT=왼쪽;memcpy(dades,반환값->dades+열림[순번].Posició,element_COMPT);열림[순번].Posició+=element_COMPT;return element_COMPT;}
    intptr_t 반환값=사용자호출(2,arxiu_control_7f4cdfd5,(uintptr_t)dades,element_COMPT,0,0,0);if(반환값<0){s_ha_produït_un_error=-반환값;return -1;}return 반환값;
}
long write(int arxiu_control_7f4cdfd5,const void*dades,size_t element_COMPT){
    if(arxiu_control_7f4cdfd5==100){if(element_COMPT>sizeof(출력결과)-출력위치){s_ha_produït_un_error=28;return -1;}memcpy(출력결과+출력위치,dades,element_COMPT);출력위치+=element_COMPT;if(출력크기<출력위치)출력크기=출력위치;return element_COMPT;}
    intptr_t 반환값=사용자호출(1,arxiu_control_7f4cdfd5,(uintptr_t)dades,element_COMPT,0,0,0);if(반환값<0){s_ha_produït_un_error=-반환값;return -1;}return 반환값;
}
long lseek(int arxiu_control_7f4cdfd5,long DESPLAÇAMENT_VALOR,int 기준점){
    if(arxiu_control_7f4cdfd5==100){long dades_càrrec=DESPLAÇAMENT_VALOR+(기준점==0?0:기준점==1?출력위치:출력크기);if(dades_càrrec<0||(size_t)dades_càrrec>sizeof(출력결과)){s_ha_produït_un_error=22;return -1;}출력위치=dades_càrrec;return dades_càrrec;}
    if(arxiu_control_7f4cdfd5>=128&&arxiu_control_7f4cdfd5<152&&열림[arxiu_control_7f4cdfd5-128].사용량){int 순번=arxiu_control_7f4cdfd5-128;long dades_càrrec=DESPLAÇAMENT_VALOR+(기준점==0?0:기준점==1?열림[순번].Posició:번역기자원들[열림[순번].Cerca_INDEX].Mida);if(dades_càrrec<0||(size_t)dades_càrrec>번역기자원들[열림[순번].Cerca_INDEX].Mida){s_ha_produït_un_error=22;return -1;}열림[순번].Posició=dades_càrrec;return dades_càrrec;}
    intptr_t 반환값=사용자호출(5,arxiu_control_7f4cdfd5,DESPLAÇAMENT_VALOR,기준점,0,0,0);if(반환값<0){s_ha_produït_un_error=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nom){intptr_t 반환값=사용자호출(11,(uintptr_t)Nom,0,0,0,0,0);if(반환값<0){s_ha_produït_un_error=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nom,char*mesura_dades){if(!mesura_dades){mesura_dades=malloc(strlen(Nom)+1);if(!mesura_dades)return 0;}return strcpy(mesura_dades,Nom);}
char *getcwd(char*dades_càrrec,size_t element_COMPT){if(element_COMPT<2){s_ha_produït_un_error=34;return 0;}dades_càrrec[0]='/';dades_càrrec[1]=0;return dades_càrrec;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_introducció){time_t 임시값=0;if(Terminal_introducció)*Terminal_introducció=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_introducció){(void)Terminal_introducció;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Seqüències[18]={{1,0,1},{2,0,1}};FILE*stdout=&Seqüències[0],*stderr=&Seqüències[1];
FILE*fdopen(int arxiu_control_7f4cdfd5,const char*방식){(void)방식;for(unsigned 순번=2;순번<18;순번++)if(!Seqüències[순번].사용량){Seqüències[순번].사용량=1;Seqüències[순번].s_ha_produït_un_error=0;Seqüències[순번].arxiu_control_7f4cdfd5=arxiu_control_7f4cdfd5;return &Seqüències[순번];}s_ha_produït_un_error=24;return 0;}
int fflush(FILE*arxiu_introducció){return arxiu_introducció&&arxiu_introducció->s_ha_produït_un_error?-1:0;}
int fclose(FILE*arxiu_introducció){int 반환값=close(arxiu_introducció->arxiu_control_7f4cdfd5);if(arxiu_introducció->s_ha_produït_un_error)반환값=-1;arxiu_introducció->사용량=0;return 반환값;}
size_t fwrite(const void*dades_càrrec,size_t cadena_dades,size_t element_COMPT,FILE*arxiu_introducció){if(!cadena_dades)return 0;if(element_COMPT>SIZE_MAX/cadena_dades){arxiu_introducció->s_ha_produït_un_error=1;return 0;}long 반환값=write(arxiu_introducció->arxiu_control_7f4cdfd5,dades_càrrec,cadena_dades*element_COMPT);if(반환값<0){arxiu_introducció->s_ha_produït_un_error=1;return 0;}return (size_t)반환값/cadena_dades;}
int fputc(int codi_de_caràcter,FILE*arxiu_introducció){unsigned char SEGON_VALOR=codi_de_caràcter;return fwrite(&SEGON_VALOR,1,1,arxiu_introducció)==1?SEGON_VALOR:EOF;}
int fputs(const char*cadena_dades,FILE*arxiu_introducció){return fwrite(cadena_dades,1,strlen(cadena_dades),arxiu_introducció)==strlen(cadena_dades)?0:EOF;}
static void 넣기(char*mesura_dades,size_t 용량한도,size_t*현재위치,char codi_de_caràcter){if(*현재위치+1<용량한도)mesura_dades[*현재위치]=codi_de_caràcter;(*현재위치)++;}
int vsnprintf(char*mesura_dades,size_t 용량한도,const char*format,va_list 가변인수){
    size_t 현재위치=0;while(*format){if(*format!='%'){넣기(mesura_dades,용량한도,&현재위치,*format++);continue;}format++;
        int 왼쪽=0,영값=0,대체값=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')왼쪽=1;if(*format=='0')영값=1;if(*format=='#')대체값=1;format++;}
        int 너비=0,precisió_VALOR=-1;if(*format=='*'){너비=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')너비=너비*10+*format++-'0';
        if(*format=='.'){format++;precisió_VALOR=0;if(*format=='*'){precisió_VALOR=va_arg(가변인수,int);format++;}else while(*format>='0'&&*format<='9')precisió_VALOR=precisió_VALOR*10+*format++-'0';}
        int 넓은글자=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')넓은글자=1;format++;}
        char TIPUS_Categoria=*format?*format++:0,memòria_intermèdia_Emmagatzematge[80];const char*cadena_dades=memòria_intermèdia_Emmagatzematge;size_t element_COMPT=0;
        if(TIPUS_Categoria=='s'){cadena_dades=va_arg(가변인수,const char*);if(!cadena_dades)cadena_dades="(null)";element_COMPT=strlen(cadena_dades);if(precisió_VALOR>=0&&element_COMPT>(size_t)precisió_VALOR)element_COMPT=precisió_VALOR;}
        else if(TIPUS_Categoria=='c'){memòria_intermèdia_Emmagatzematge[0]=va_arg(가변인수,int);element_COMPT=1;}
        else if(TIPUS_Categoria=='%'){memòria_intermèdia_Emmagatzematge[0]='%';element_COMPT=1;}
        else if(TIPUS_Categoria=='d'||TIPUS_Categoria=='i'||TIPUS_Categoria=='u'||TIPUS_Categoria=='x'||TIPUS_Categoria=='X'||TIPUS_Categoria=='o'||TIPUS_Categoria=='p'){
            unsigned long long VALOR;int 음수표시=0;
            if(TIPUS_Categoria=='d'||TIPUS_Categoria=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALOR=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALOR=TIPUS_Categoria=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Fons_VALOR=TIPUS_Categoria=='x'||TIPUS_Categoria=='X'||TIPUS_Categoria=='p'?16:TIPUS_Categoria=='o'?8:10;char dígit_COMPT[64];unsigned 사용량=0;
            do{dígit_COMPT[사용량++]="0123456789abcdef"[VALOR%Fons_VALOR];VALOR/=Fons_VALOR;}while(VALOR);
            if(음수표시)memòria_intermèdia_Emmagatzematge[element_COMPT++]='-';if(TIPUS_Categoria=='p'||(대체값&&Fons_VALOR==16)){memòria_intermèdia_Emmagatzematge[element_COMPT++]='0';memòria_intermèdia_Emmagatzematge[element_COMPT++]='x';}
            for(int emplenar_VALOR=(int)사용량;precisió_VALOR>emplenar_VALOR&&element_COMPT<sizeof(memòria_intermèdia_Emmagatzematge)-사용량;emplenar_VALOR++)memòria_intermèdia_Emmagatzematge[element_COMPT++]='0';
            if(영값&&!왼쪽&&precisió_VALOR<0)while(너비>(int)(element_COMPT+사용량)&&element_COMPT<sizeof(memòria_intermèdia_Emmagatzematge)-사용량)memòria_intermèdia_Emmagatzematge[element_COMPT++]='0';
            while(사용량)memòria_intermèdia_Emmagatzematge[element_COMPT++]=dígit_COMPT[--사용량];
        }else{memòria_intermèdia_Emmagatzematge[0]='?';element_COMPT=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)element_COMPT){넣기(mesura_dades,용량한도,&현재위치,' ');너비--;}
        for(size_t 순번=0;순번<element_COMPT;순번++)넣기(mesura_dades,용량한도,&현재위치,cadena_dades[순번]);while(왼쪽&&너비>(int)element_COMPT){넣기(mesura_dades,용량한도,&현재위치,' ');너비--;}
    }if(용량한도)mesura_dades[현재위치<용량한도?현재위치:용량한도-1]=0;return 현재위치;
}
int snprintf(char*mesura_dades,size_t 용량한도,const char*arxiu_introducció,...){va_list 첫째값;va_start(첫째값,arxiu_introducció);int 반환값=vsnprintf(mesura_dades,용량한도,arxiu_introducció,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*mesura_dades,const char*arxiu_introducció,...){va_list 첫째값;va_start(첫째값,arxiu_introducció);int 반환값=vsnprintf(mesura_dades,SIZE_MAX,arxiu_introducció,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*flux_VALOR,const char*arxiu_introducció,va_list 첫째값){char SEGON_VALOR[2048];int element_COMPT=vsnprintf(SEGON_VALOR,sizeof(SEGON_VALOR),arxiu_introducció,첫째값);if(element_COMPT>2047)element_COMPT=2047;return fwrite(SEGON_VALOR,1,element_COMPT,flux_VALOR)==(size_t)element_COMPT?element_COMPT:-1;}
int fprintf(FILE*flux_VALOR,const char*arxiu_introducció,...){va_list 첫째값;va_start(첫째값,arxiu_introducció);int 반환값=vfprintf(flux_VALOR,arxiu_introducció,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*arxiu_introducció,...){va_list 첫째값;va_start(첫째값,arxiu_introducció);int 반환값=vfprintf(stdout,arxiu_introducció,첫째값);va_end(첫째값);return 반환값;}
