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
static int ERRO;
int *__errno_location(void){return &ERRO;}
void exit(int Estado_VALOR){사용자호출(6,Estado_VALOR,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *cheque_expresión,const char *Ficheiro,unsigned Liña,const char *함수이름){fprintf(stderr,"cc assertion: %s %s:%u %s\n",cheque_expresión,Ficheiro,Liña,함수이름);exit(1);}
size_t strlen(const char*cadea_datos){const char*datos_cargo=cadea_datos;while(*datos_cargo)datos_cargo++;return datos_cargo-cadea_datos;}
int strcmp(const char*첫째값,const char*SEGUNDO_VALOR){while(*첫째값&&*첫째값==*SEGUNDO_VALOR){첫째값++;SEGUNDO_VALOR++;}return (unsigned char)*첫째값-(unsigned char)*SEGUNDO_VALOR;}
int strncmp(const char*첫째값,const char*SEGUNDO_VALOR,size_t elemento_CONTAR){while(elemento_CONTAR--){unsigned char X_coordenada=*첫째값++,Y_coordenada=*SEGUNDO_VALOR++;if(X_coordenada!=Y_coordenada)return X_coordenada-Y_coordenada;if(!X_coordenada)return 0;}return 0;}
char *strcpy(char*destino_datos,const char*cadea_datos){char*반환값=destino_datos;while((*destino_datos++=*cadea_datos++)){}return 반환값;}
char *strchr(const char*cadea_datos,int código_de_carácter){do{if(*cadea_datos==(char)código_de_carácter)return (char*)cadea_datos;}while(*cadea_datos++);return 0;}
char *strrchr(const char*cadea_datos,int código_de_carácter){const char*반환값=0;do{if(*cadea_datos==(char)código_de_carácter)반환값=cadea_datos;}while(*cadea_datos++);return (char*)반환값;}
char *strstr(const char*cadea_datos,const char*Terminal_introdución){size_t elemento_CONTAR=strlen(Terminal_introdución);for(;*cadea_datos;cadea_datos++)if(!strncmp(cadea_datos,Terminal_introdución,elemento_CONTAR))return (char*)cadea_datos;return elemento_CONTAR?0:(char*)cadea_datos;}
int memcmp(const void*첫째값,const void*SEGUNDO_VALOR,size_t elemento_CONTAR){const unsigned char*X_coordenada=첫째값,*Y_coordenada=SEGUNDO_VALOR;while(elemento_CONTAR--){if(*X_coordenada!=*Y_coordenada)return *X_coordenada-*Y_coordenada;X_coordenada++;Y_coordenada++;}return 0;}
void *memmove(void*destino_datos,const void*cadea_datos,size_t elemento_CONTAR){unsigned char*X_coordenada=destino_datos;const unsigned char*Y_coordenada=cadea_datos;if(X_coordenada<Y_coordenada){for(size_t 순번=0;순번<elemento_CONTAR;순번++)X_coordenada[순번]=Y_coordenada[순번];}else while(elemento_CONTAR){elemento_CONTAR--;X_coordenada[elemento_CONTAR]=Y_coordenada[elemento_CONTAR];}return destino_datos;}
static unsigned char atribución_Arena[6*1024*1024] __attribute__((aligned(16)));
typedef struct datos_bloquear {size_t Tamaño;struct datos_bloquear*Seguinte_elemento;int 남은공간;int 채울크기;uint64_t aliñamento_lección;} datos_bloquear;
static datos_bloquear *첫항목;
void free(void*datos_cargo){if(!datos_cargo)return;datos_bloquear*SEGUNDO_VALOR=(datos_bloquear*)datos_cargo-1;SEGUNDO_VALOR->남은공간=1;for(datos_bloquear*Seguinte_DESPRAZAMENTO=첫항목;Seguinte_DESPRAZAMENTO&&Seguinte_DESPRAZAMENTO->Seguinte_elemento;){if(Seguinte_DESPRAZAMENTO->남은공간&&Seguinte_DESPRAZAMENTO->Seguinte_elemento->남은공간){Seguinte_DESPRAZAMENTO->Tamaño+=sizeof(datos_bloquear)+Seguinte_DESPRAZAMENTO->Seguinte_elemento->Tamaño;Seguinte_DESPRAZAMENTO->Seguinte_elemento=Seguinte_DESPRAZAMENTO->Seguinte_elemento->Seguinte_elemento;}else Seguinte_DESPRAZAMENTO=Seguinte_DESPRAZAMENTO->Seguinte_elemento;}}
void *realloc(void*datos_cargo,size_t elemento_CONTAR){
    if(!elemento_CONTAR){free(datos_cargo);return 0;}if(elemento_CONTAR>sizeof(atribución_Arena)-sizeof(datos_bloquear))return 0;elemento_CONTAR=(elemento_CONTAR+15)&~(size_t)15;
    if(!첫항목){첫항목=(datos_bloquear*)atribución_Arena;첫항목->Tamaño=sizeof(atribución_Arena)-sizeof(datos_bloquear);첫항목->남은공간=1;첫항목->Seguinte_elemento=0;}
    datos_bloquear*이전=datos_cargo?(datos_bloquear*)datos_cargo-1:0;if(이전&&이전->Tamaño>=elemento_CONTAR)return datos_cargo;
    for(datos_bloquear*SEGUNDO_VALOR=첫항목;SEGUNDO_VALOR;SEGUNDO_VALOR=SEGUNDO_VALOR->Seguinte_elemento)if(SEGUNDO_VALOR->남은공간&&SEGUNDO_VALOR->Tamaño>=elemento_CONTAR){
        if(SEGUNDO_VALOR->Tamaño>=elemento_CONTAR+sizeof(datos_bloquear)+16){datos_bloquear*나머지부분=(datos_bloquear*)((unsigned char*)(SEGUNDO_VALOR+1)+elemento_CONTAR);나머지부분->Tamaño=SEGUNDO_VALOR->Tamaño-elemento_CONTAR-sizeof(datos_bloquear);나머지부분->Seguinte_elemento=SEGUNDO_VALOR->Seguinte_elemento;나머지부분->남은공간=1;SEGUNDO_VALOR->Seguinte_elemento=나머지부분;SEGUNDO_VALOR->Tamaño=elemento_CONTAR;}
        SEGUNDO_VALOR->남은공간=0;void*반환값=SEGUNDO_VALOR+1;if(이전){memcpy(반환값,datos_cargo,이전->Tamaño);free(datos_cargo);}return 반환값;
    }ERRO=12;return 0;
}
void *malloc(size_t elemento_CONTAR){return realloc(0,elemento_CONTAR);}
void *calloc(size_t elemento_CONTAR,size_t cadea_datos){if(cadea_datos&&elemento_CONTAR>SIZE_MAX/cadea_datos)return 0;void*datos_cargo=malloc(elemento_CONTAR*cadea_datos);if(datos_cargo)memset(datos_cargo,0,elemento_CONTAR*cadea_datos);return datos_cargo;}
unsigned long long strtoull(const char*cadea_datos,char**finalizar_DESPRAZAMENTO,int Fondo_VALOR){
    const char*START_DESPRAZAMENTO=cadea_datos;while(*cadea_datos==' '||(*cadea_datos>=9&&*cadea_datos<=13))cadea_datos++;int 음수여부=0;if(*cadea_datos=='-'||*cadea_datos=='+')음수여부=*cadea_datos++=='-';
    if((!Fondo_VALOR||Fondo_VALOR==16)&&cadea_datos[0]=='0'&&(cadea_datos[1]=='x'||cadea_datos[1]=='X')){Fondo_VALOR=16;cadea_datos+=2;}if(!Fondo_VALOR)Fondo_VALOR=*cadea_datos=='0'?8:10;
    unsigned long long 임시값=0;int 하나라도=0;for(;;){unsigned código_de_carácter=*cadea_datos,destino_datos=código_de_carácter>='0'&&código_de_carácter<='9'?código_de_carácter-'0':código_de_carácter>='a'&&código_de_carácter<='z'?código_de_carácter-'a'+10:código_de_carácter>='A'&&código_de_carácter<='Z'?código_de_carácter-'A'+10:99;if(destino_datos>=(unsigned)Fondo_VALOR)break;하나라도=1;cadea_datos++;if(임시값>(~0ull-destino_datos)/(unsigned)Fondo_VALOR){임시값=~0ull;ERRO=34;}else 임시값=임시값*Fondo_VALOR+destino_datos;}
    if(finalizar_DESPRAZAMENTO)*finalizar_DESPRAZAMENTO=(char*)(하나라도?cadea_datos:START_DESPRAZAMENTO);return 음수여부?0-임시값:임시값;
}
unsigned long strtoul(const char*cadea_datos,char**보조항목,int SEGUNDO_VALOR){return strtoull(cadea_datos,보조항목,SEGUNDO_VALOR);}
long strtol(const char*cadea_datos,char**보조항목,int SEGUNDO_VALOR){return (long)strtoull(cadea_datos,보조항목,SEGUNDO_VALOR);}
int atoi(const char*cadea_datos){return (int)strtol(cadea_datos,0,10);}
long double ldexpl(long double X_coordenada,int elemento_CONTAR){while(elemento_CONTAR>0){X_coordenada*=2;elemento_CONTAR--;}while(elemento_CONTAR<0){X_coordenada/=2;elemento_CONTAR++;}return X_coordenada;}
long double strtold(const char*cadea_datos,char**finalizar_DESPRAZAMENTO){
    const char*START_DESPRAZAMENTO=cadea_datos;while(*cadea_datos==' '||(*cadea_datos>=9&&*cadea_datos<=13))cadea_datos++;int 음수여부=0;if(*cadea_datos=='-'||*cadea_datos=='+')음수여부=*cadea_datos++=='-';
    int Fondo_VALOR=10;if(cadea_datos[0]=='0'&&(cadea_datos[1]=='x'||cadea_datos[1]=='X')){Fondo_VALOR=16;cadea_datos+=2;}long double 임시값=0,redimensionar=1;int 소수부=0,하나라도=0;
    for(;;){int código_de_carácter=*cadea_datos,destino_datos=código_de_carácter>='0'&&código_de_carácter<='9'?código_de_carácter-'0':código_de_carácter>='a'&&código_de_carácter<='f'?código_de_carácter-'a'+10:código_de_carácter>='A'&&código_de_carácter<='F'?código_de_carácter-'A'+10:99;
        if(código_de_carácter=='.'&&!소수부){소수부=1;cadea_datos++;continue;}if(destino_datos>=Fondo_VALOR)break;하나라도=1;cadea_datos++;임시값=임시값*Fondo_VALOR+destino_datos;if(소수부)redimensionar*=Fondo_VALOR;
    }임시값/=redimensionar;
    if((Fondo_VALOR==10&&(*cadea_datos=='e'||*cadea_datos=='E'))||(Fondo_VALOR==16&&(*cadea_datos=='p'||*cadea_datos=='P'))){const char*mostrar_VALOR=cadea_datos++;int 빼기=0;if(*cadea_datos=='-'||*cadea_datos=='+')빼기=*cadea_datos++=='-';int elemento_CONTAR=0,introdución_CONTAR=0;while(*cadea_datos>='0'&&*cadea_datos<='9'){introdución_CONTAR++;if(elemento_CONTAR<20000)elemento_CONTAR=elemento_CONTAR*10+*cadea_datos-'0';cadea_datos++;}if(!introdución_CONTAR)cadea_datos=mostrar_VALOR;else{long double factor=Fondo_VALOR==16?2:10;while(elemento_CONTAR-->0&&elemento_CONTAR<200000)임시값=빼기?임시값/factor:임시값*factor;}}
    if(finalizar_DESPRAZAMENTO)*finalizar_DESPRAZAMENTO=(char*)(하나라도?cadea_datos:START_DESPRAZAMENTO);return 음수여부?-임시값:임시값;
}
double strtod(const char*cadea_datos,char**보조항목){return (double)strtold(cadea_datos,보조항목);}float strtof(const char*cadea_datos,char**보조항목){return (float)strtold(cadea_datos,보조항목);}
void qsort(void*Fondo_VALOR,size_t elemento_CONTAR,size_t Tamaño,int(*Comparar)(const void*,const void*)){
    unsigned char*datos_cargo=Fondo_VALOR;for(size_t 순번=1;순번<elemento_CONTAR;순번++)for(size_t 안쪽순번=순번;안쪽순번&&Comparar(datos_cargo+(안쪽순번-1)*Tamaño,datos_cargo+안쪽순번*Tamaño)>0;안쪽순번--)for(size_t 셋째순번=0;셋째순번<Tamaño;셋째순번++){unsigned char código_de_carácter=datos_cargo[(안쪽순번-1)*Tamaño+셋째순번];datos_cargo[(안쪽순번-1)*Tamaño+셋째순번]=datos_cargo[안쪽순번*Tamaño+셋째순번];datos_cargo[안쪽순번*Tamaño+셋째순번]=código_de_carácter;}
}
static struct {int 사용량,Busca_ÍNDICE;size_t Posición;} 열림[24];
static unsigned char 출력결과[32768];static size_t 출력크기,출력위치;static int 출력열림;
const unsigned char *시언어출력(size_t *elemento_CONTAR){*elemento_CONTAR=출력크기;return 출력결과;}
int open(const char*Nome,int configuración_Servizo_de_transferencia_intelixente_en_segundo_plano,...){
    if(!strcmp(Nome,"/@cc-output")){if(출력열림){ERRO=16;return -1;}출력열림=1;출력크기=출력위치=0;return 100;}
    for(unsigned 순번=0;순번<sizeof(번역기자원들)/sizeof(번역기자원들[0]);순번++)if(!strcmp(Nome,번역기자원들[순번].Nome)){
        if(configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&3){ERRO=30;return -1;}for(int 안쪽순번=0;안쪽순번<24;안쪽순번++)if(!열림[안쪽순번].사용량){열림[안쪽순번].사용량=1;열림[안쪽순번].Busca_ÍNDICE=순번;열림[안쪽순번].Posición=0;return 128+안쪽순번;}ERRO=24;return -1;
    }
    intptr_t 반환값=사용자호출(3,(uintptr_t)Nome,configuración_Servizo_de_transferencia_intelixente_en_segundo_plano,0,0,0,0);if(반환값<0){ERRO=-반환값;return -1;}return 반환값;
}
int close(int Ficheiro_agarradoira){if(Ficheiro_agarradoira==100){출력열림=0;return 0;}if(Ficheiro_agarradoira>=128&&Ficheiro_agarradoira<152){열림[Ficheiro_agarradoira-128].사용량=0;return 0;}intptr_t 반환값=사용자호출(4,Ficheiro_agarradoira,0,0,0,0,0);if(반환값<0){ERRO=-반환값;return -1;}return 0;}
long read(int Ficheiro_agarradoira,void*datos,size_t elemento_CONTAR){
    if(Ficheiro_agarradoira>=128&&Ficheiro_agarradoira<152&&열림[Ficheiro_agarradoira-128].사용량){int 순번=Ficheiro_agarradoira-128;const 번역기자원*반환값=&번역기자원들[열림[순번].Busca_ÍNDICE];size_t 왼쪽=반환값->Tamaño-열림[순번].Posición;if(elemento_CONTAR>왼쪽)elemento_CONTAR=왼쪽;memcpy(datos,반환값->datos+열림[순번].Posición,elemento_CONTAR);열림[순번].Posición+=elemento_CONTAR;return elemento_CONTAR;}
    intptr_t 반환값=사용자호출(2,Ficheiro_agarradoira,(uintptr_t)datos,elemento_CONTAR,0,0,0);if(반환값<0){ERRO=-반환값;return -1;}return 반환값;
}
long write(int Ficheiro_agarradoira,const void*datos,size_t elemento_CONTAR){
    if(Ficheiro_agarradoira==100){if(elemento_CONTAR>sizeof(출력결과)-출력위치){ERRO=28;return -1;}memcpy(출력결과+출력위치,datos,elemento_CONTAR);출력위치+=elemento_CONTAR;if(출력크기<출력위치)출력크기=출력위치;return elemento_CONTAR;}
    intptr_t 반환값=사용자호출(1,Ficheiro_agarradoira,(uintptr_t)datos,elemento_CONTAR,0,0,0);if(반환값<0){ERRO=-반환값;return -1;}return 반환값;
}
long lseek(int Ficheiro_agarradoira,long DESPRAZAMENTO_VALOR,int 기준점){
    if(Ficheiro_agarradoira==100){long datos_cargo=DESPRAZAMENTO_VALOR+(기준점==0?0:기준점==1?출력위치:출력크기);if(datos_cargo<0||(size_t)datos_cargo>sizeof(출력결과)){ERRO=22;return -1;}출력위치=datos_cargo;return datos_cargo;}
    if(Ficheiro_agarradoira>=128&&Ficheiro_agarradoira<152&&열림[Ficheiro_agarradoira-128].사용량){int 순번=Ficheiro_agarradoira-128;long datos_cargo=DESPRAZAMENTO_VALOR+(기준점==0?0:기준점==1?열림[순번].Posición:번역기자원들[열림[순번].Busca_ÍNDICE].Tamaño);if(datos_cargo<0||(size_t)datos_cargo>번역기자원들[열림[순번].Busca_ÍNDICE].Tamaño){ERRO=22;return -1;}열림[순번].Posición=datos_cargo;return datos_cargo;}
    intptr_t 반환값=사용자호출(5,Ficheiro_agarradoira,DESPRAZAMENTO_VALOR,기준점,0,0,0);if(반환값<0){ERRO=-반환값;return -1;}return 반환값;
}
int unlink(const char*Nome){intptr_t 반환값=사용자호출(11,(uintptr_t)Nome,0,0,0,0,0);if(반환값<0){ERRO=-반환값;return -1;}return 반환값;}
char *realpath(const char*Nome,char*medida_datos){if(!medida_datos){medida_datos=malloc(strlen(Nome)+1);if(!medida_datos)return 0;}return strcpy(medida_datos,Nome);}
char *getcwd(char*datos_cargo,size_t elemento_CONTAR){if(elemento_CONTAR<2){ERRO=34;return 0;}datos_cargo[0]='/';datos_cargo[1]=0;return datos_cargo;}
char *strerror(int 보조항목){(void)보조항목;return "native compiler I/O error";}
time_t time(time_t*Terminal_introdución){time_t 임시값=0;if(Terminal_introdución)*Terminal_introdución=임시값;return 임시값;}
struct tm *localtime(const time_t*Terminal_introdución){(void)Terminal_introdución;static struct tm 임시값={.tm_year=126,.tm_mon=0,.tm_mday=1};return &임시값;}
static FILE Secuencias[18]={{1,0,1},{2,0,1}};FILE*stdout=&Secuencias[0],*stderr=&Secuencias[1];
FILE*fdopen(int Ficheiro_agarradoira,const char*방식){(void)방식;for(unsigned 순번=2;순번<18;순번++)if(!Secuencias[순번].사용량){Secuencias[순번].사용량=1;Secuencias[순번].ERRO=0;Secuencias[순번].Ficheiro_agarradoira=Ficheiro_agarradoira;return &Secuencias[순번];}ERRO=24;return 0;}
int fflush(FILE*Ficheiro_introdución){return Ficheiro_introdución&&Ficheiro_introdución->ERRO?-1:0;}
int fclose(FILE*Ficheiro_introdución){int 반환값=close(Ficheiro_introdución->Ficheiro_agarradoira);if(Ficheiro_introdución->ERRO)반환값=-1;Ficheiro_introdución->사용량=0;return 반환값;}
size_t fwrite(const void*datos_cargo,size_t cadea_datos,size_t elemento_CONTAR,FILE*Ficheiro_introdución){if(!cadea_datos)return 0;if(elemento_CONTAR>SIZE_MAX/cadea_datos){Ficheiro_introdución->ERRO=1;return 0;}long 반환값=write(Ficheiro_introdución->Ficheiro_agarradoira,datos_cargo,cadea_datos*elemento_CONTAR);if(반환값<0){Ficheiro_introdución->ERRO=1;return 0;}return (size_t)반환값/cadea_datos;}
int fputc(int código_de_carácter,FILE*Ficheiro_introdución){unsigned char SEGUNDO_VALOR=código_de_carácter;return fwrite(&SEGUNDO_VALOR,1,1,Ficheiro_introdución)==1?SEGUNDO_VALOR:EOF;}
int fputs(const char*cadea_datos,FILE*Ficheiro_introdución){return fwrite(cadea_datos,1,strlen(cadea_datos),Ficheiro_introdución)==strlen(cadea_datos)?0:EOF;}
static void 넣기(char*medida_datos,size_t 용량한도,size_t*ao_corrente_cargo,char código_de_carácter){if(*ao_corrente_cargo+1<용량한도)medida_datos[*ao_corrente_cargo]=código_de_carácter;(*ao_corrente_cargo)++;}
int vsnprintf(char*medida_datos,size_t 용량한도,const char*formato,va_list 가변인수){
    size_t ao_corrente_cargo=0;while(*formato){if(*formato!='%'){넣기(medida_datos,용량한도,&ao_corrente_cargo,*formato++);continue;}formato++;
        int 왼쪽=0,영값=0,대체값=0;while(*formato=='-'||*formato=='0'||*formato=='#'||*formato=='+'||*formato==' '){if(*formato=='-')왼쪽=1;if(*formato=='0')영값=1;if(*formato=='#')대체값=1;formato++;}
        int 너비=0,precisión_VALOR=-1;if(*formato=='*'){너비=va_arg(가변인수,int);formato++;}else while(*formato>='0'&&*formato<='9')너비=너비*10+*formato++-'0';
        if(*formato=='.'){formato++;precisión_VALOR=0;if(*formato=='*'){precisión_VALOR=va_arg(가변인수,int);formato++;}else while(*formato>='0'&&*formato<='9')precisión_VALOR=precisión_VALOR*10+*formato++-'0';}
        int 넓은글자=0;while(*formato=='l'||*formato=='z'||*formato=='t'||*formato=='j'||*formato=='h'){if(*formato!='h')넓은글자=1;formato++;}
        char TIPO_Categoría=*formato?*formato++:0,búfer_Almacenamento[80];const char*cadea_datos=búfer_Almacenamento;size_t elemento_CONTAR=0;
        if(TIPO_Categoría=='s'){cadea_datos=va_arg(가변인수,const char*);if(!cadea_datos)cadea_datos="(null)";elemento_CONTAR=strlen(cadea_datos);if(precisión_VALOR>=0&&elemento_CONTAR>(size_t)precisión_VALOR)elemento_CONTAR=precisión_VALOR;}
        else if(TIPO_Categoría=='c'){búfer_Almacenamento[0]=va_arg(가변인수,int);elemento_CONTAR=1;}
        else if(TIPO_Categoría=='%'){búfer_Almacenamento[0]='%';elemento_CONTAR=1;}
        else if(TIPO_Categoría=='d'||TIPO_Categoría=='i'||TIPO_Categoría=='u'||TIPO_Categoría=='x'||TIPO_Categoría=='X'||TIPO_Categoría=='o'||TIPO_Categoría=='p'){
            unsigned long long VALOR;int 음수표시=0;
            if(TIPO_Categoría=='d'||TIPO_Categoría=='i'){long long 임시값=넓은글자?va_arg(가변인수,long long):va_arg(가변인수,int);음수표시=임시값<0;VALOR=음수표시?0-(unsigned long long)임시값:임시값;}
            else VALOR=TIPO_Categoría=='p'?(uintptr_t)va_arg(가변인수,void*):넓은글자?va_arg(가변인수,unsigned long long):va_arg(가변인수,unsigned);
            unsigned Fondo_VALOR=TIPO_Categoría=='x'||TIPO_Categoría=='X'||TIPO_Categoría=='p'?16:TIPO_Categoría=='o'?8:10;char díxito_CONTAR[64];unsigned 사용량=0;
            do{díxito_CONTAR[사용량++]="0123456789abcdef"[VALOR%Fondo_VALOR];VALOR/=Fondo_VALOR;}while(VALOR);
            if(음수표시)búfer_Almacenamento[elemento_CONTAR++]='-';if(TIPO_Categoría=='p'||(대체값&&Fondo_VALOR==16)){búfer_Almacenamento[elemento_CONTAR++]='0';búfer_Almacenamento[elemento_CONTAR++]='x';}
            for(int encher_VALOR=(int)사용량;precisión_VALOR>encher_VALOR&&elemento_CONTAR<sizeof(búfer_Almacenamento)-사용량;encher_VALOR++)búfer_Almacenamento[elemento_CONTAR++]='0';
            if(영값&&!왼쪽&&precisión_VALOR<0)while(너비>(int)(elemento_CONTAR+사용량)&&elemento_CONTAR<sizeof(búfer_Almacenamento)-사용량)búfer_Almacenamento[elemento_CONTAR++]='0';
            while(사용량)búfer_Almacenamento[elemento_CONTAR++]=díxito_CONTAR[--사용량];
        }else{búfer_Almacenamento[0]='?';elemento_CONTAR=1;}
        if(너비>4096)너비=4096;while(!왼쪽&&너비>(int)elemento_CONTAR){넣기(medida_datos,용량한도,&ao_corrente_cargo,' ');너비--;}
        for(size_t 순번=0;순번<elemento_CONTAR;순번++)넣기(medida_datos,용량한도,&ao_corrente_cargo,cadea_datos[순번]);while(왼쪽&&너비>(int)elemento_CONTAR){넣기(medida_datos,용량한도,&ao_corrente_cargo,' ');너비--;}
    }if(용량한도)medida_datos[ao_corrente_cargo<용량한도?ao_corrente_cargo:용량한도-1]=0;return ao_corrente_cargo;
}
int snprintf(char*medida_datos,size_t 용량한도,const char*Ficheiro_introdución,...){va_list 첫째값;va_start(첫째값,Ficheiro_introdución);int 반환값=vsnprintf(medida_datos,용량한도,Ficheiro_introdución,첫째값);va_end(첫째값);return 반환값;}
int sprintf(char*medida_datos,const char*Ficheiro_introdución,...){va_list 첫째값;va_start(첫째값,Ficheiro_introdución);int 반환값=vsnprintf(medida_datos,SIZE_MAX,Ficheiro_introdución,첫째값);va_end(첫째값);return 반환값;}
int vfprintf(FILE*fluxo_VALOR,const char*Ficheiro_introdución,va_list 첫째값){char SEGUNDO_VALOR[2048];int elemento_CONTAR=vsnprintf(SEGUNDO_VALOR,sizeof(SEGUNDO_VALOR),Ficheiro_introdución,첫째값);if(elemento_CONTAR>2047)elemento_CONTAR=2047;return fwrite(SEGUNDO_VALOR,1,elemento_CONTAR,fluxo_VALOR)==(size_t)elemento_CONTAR?elemento_CONTAR:-1;}
int fprintf(FILE*fluxo_VALOR,const char*Ficheiro_introdución,...){va_list 첫째값;va_start(첫째값,Ficheiro_introdución);int 반환값=vfprintf(fluxo_VALOR,Ficheiro_introdución,첫째값);va_end(첫째값);return 반환값;}
int printf(const char*Ficheiro_introdución,...){va_list 첫째값;va_start(첫째값,Ficheiro_introdución);int 반환값=vfprintf(stdout,Ficheiro_introdución,첫째값);va_end(첫째값);return 반환값;}
