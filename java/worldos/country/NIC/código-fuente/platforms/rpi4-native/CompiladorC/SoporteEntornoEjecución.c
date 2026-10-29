#include "../denominación/nombresEnlazarMáquina.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "invocar.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int error;
int *__errno_location(void){return &error;}
void exit(int valorEstadoValor){invocarUsuario(6,valorEstadoValor,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *comprobarExpresión,const char *Archivo,unsigned línea,const char *nombreEntradaElementoMétodo){fprintf(stderr,"cc assertion: %s %s:%u %s\n",comprobarExpresión,Archivo,línea,nombreEntradaElementoMétodo);exit(1);}
size_t strlen(const char*datosCadena){const char*posiciónDatos=datosCadena;while(*posiciónDatos)posiciónDatos++;return posiciónDatos-datosCadena;}
int strcmp(const char*valorPrimero,const char*valorSegundo){while(*valorPrimero&&*valorPrimero==*valorSegundo){valorPrimero++;valorSegundo++;}return (unsigned char)*valorPrimero-(unsigned char)*valorSegundo;}
int strncmp(const char*valorPrimero,const char*valorSegundo,size_t númeroElementosElementoLista){while(númeroElementosElementoLista--){unsigned char coordenadaCoordenadaHorizontal=*valorPrimero++,coordenadaCoordenadaVertical=*valorSegundo++;if(coordenadaCoordenadaHorizontal!=coordenadaCoordenadaVertical)return coordenadaCoordenadaHorizontal-coordenadaCoordenadaVertical;if(!coordenadaCoordenadaHorizontal)return 0;}return 0;}
char *strcpy(char*datosDestino,const char*datosCadena){char*valorDevuelto=datosDestino;while((*datosDestino++=*datosCadena++)){}return valorDevuelto;}
char *strchr(const char*datosCadena,int códigoCarácter){do{if(*datosCadena==(char)códigoCarácter)return (char*)datosCadena;}while(*datosCadena++);return 0;}
char *strrchr(const char*datosCadena,int códigoCarácter){const char*valorDevuelto=0;do{if(*datosCadena==(char)códigoCarácter)valorDevuelto=datosCadena;}while(*datosCadena++);return (char*)valorDevuelto;}
char *strstr(const char*datosCadena,const char*entradaElementoTerminal){size_t númeroElementosElementoLista=strlen(entradaElementoTerminal);for(;*datosCadena;datosCadena++)if(!strncmp(datosCadena,entradaElementoTerminal,númeroElementosElementoLista))return (char*)datosCadena;return númeroElementosElementoLista?0:(char*)datosCadena;}
int memcmp(const void*valorPrimero,const void*valorSegundo,size_t númeroElementosElementoLista){const unsigned char*coordenadaCoordenadaHorizontal=valorPrimero,*coordenadaCoordenadaVertical=valorSegundo;while(númeroElementosElementoLista--){if(*coordenadaCoordenadaHorizontal!=*coordenadaCoordenadaVertical)return *coordenadaCoordenadaHorizontal-*coordenadaCoordenadaVertical;coordenadaCoordenadaHorizontal++;coordenadaCoordenadaVertical++;}return 0;}
void *memmove(void*datosDestino,const void*datosCadena,size_t númeroElementosElementoLista){unsigned char*coordenadaCoordenadaHorizontal=datosDestino;const unsigned char*coordenadaCoordenadaVertical=datosCadena;if(coordenadaCoordenadaHorizontal<coordenadaCoordenadaVertical){for(size_t índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)coordenadaCoordenadaHorizontal[índiceOrdinal]=coordenadaCoordenadaVertical[índiceOrdinal];}else while(númeroElementosElementoLista){númeroElementosElementoLista--;coordenadaCoordenadaHorizontal[númeroElementosElementoLista]=coordenadaCoordenadaVertical[númeroElementosElementoLista];}return datosDestino;}
static unsigned char áreaMemoriaAsignaciónMemoria[6*1024*1024] __attribute__((aligned(16)));
typedef struct bloqueDatos {size_t tamaño;struct bloqueDatos*elementoListaSiguiente;int capacidadRestante;int relleno;uint64_t unidadAlineación;} bloqueDatos;
static bloqueDatos *entradaElementoPrimero;
void free(void*posiciónDatos){if(!posiciónDatos)return;bloqueDatos*valorSegundo=(bloqueDatos*)posiciónDatos-1;valorSegundo->capacidadRestante=1;for(bloqueDatos*desfaseSiguiente=entradaElementoPrimero;desfaseSiguiente&&desfaseSiguiente->elementoListaSiguiente;){if(desfaseSiguiente->capacidadRestante&&desfaseSiguiente->elementoListaSiguiente->capacidadRestante){desfaseSiguiente->tamaño+=sizeof(bloqueDatos)+desfaseSiguiente->elementoListaSiguiente->tamaño;desfaseSiguiente->elementoListaSiguiente=desfaseSiguiente->elementoListaSiguiente->elementoListaSiguiente;}else desfaseSiguiente=desfaseSiguiente->elementoListaSiguiente;}}
void *realloc(void*posiciónDatos,size_t númeroElementosElementoLista){
    if(!númeroElementosElementoLista){free(posiciónDatos);return 0;}if(númeroElementosElementoLista>sizeof(áreaMemoriaAsignaciónMemoria)-sizeof(bloqueDatos))return 0;númeroElementosElementoLista=(númeroElementosElementoLista+15)&~(size_t)15;
    if(!entradaElementoPrimero){entradaElementoPrimero=(bloqueDatos*)áreaMemoriaAsignaciónMemoria;entradaElementoPrimero->tamaño=sizeof(áreaMemoriaAsignaciónMemoria)-sizeof(bloqueDatos);entradaElementoPrimero->capacidadRestante=1;entradaElementoPrimero->elementoListaSiguiente=0;}
    bloqueDatos*elementoListaElementoPrevio=posiciónDatos?(bloqueDatos*)posiciónDatos-1:0;if(elementoListaElementoPrevio&&elementoListaElementoPrevio->tamaño>=númeroElementosElementoLista)return posiciónDatos;
    for(bloqueDatos*valorSegundo=entradaElementoPrimero;valorSegundo;valorSegundo=valorSegundo->elementoListaSiguiente)if(valorSegundo->capacidadRestante&&valorSegundo->tamaño>=númeroElementosElementoLista){
        if(valorSegundo->tamaño>=númeroElementosElementoLista+sizeof(bloqueDatos)+16){bloqueDatos*parteRestante=(bloqueDatos*)((unsigned char*)(valorSegundo+1)+númeroElementosElementoLista);parteRestante->tamaño=valorSegundo->tamaño-númeroElementosElementoLista-sizeof(bloqueDatos);parteRestante->elementoListaSiguiente=valorSegundo->elementoListaSiguiente;parteRestante->capacidadRestante=1;valorSegundo->elementoListaSiguiente=parteRestante;valorSegundo->tamaño=númeroElementosElementoLista;}
        valorSegundo->capacidadRestante=0;void*valorDevuelto=valorSegundo+1;if(elementoListaElementoPrevio){memcpy(valorDevuelto,posiciónDatos,elementoListaElementoPrevio->tamaño);free(posiciónDatos);}return valorDevuelto;
    }error=12;return 0;
}
void *malloc(size_t númeroElementosElementoLista){return realloc(0,númeroElementosElementoLista);}
void *calloc(size_t númeroElementosElementoLista,size_t datosCadena){if(datosCadena&&númeroElementosElementoLista>SIZE_MAX/datosCadena)return 0;void*posiciónDatos=malloc(númeroElementosElementoLista*datosCadena);if(posiciónDatos)memset(posiciónDatos,0,númeroElementosElementoLista*datosCadena);return posiciónDatos;}
unsigned long long strtoull(const char*datosCadena,char**desfaseFin,int valorFondo){
    const char*iniciarDesfase=datosCadena;while(*datosCadena==' '||(*datosCadena>=9&&*datosCadena<=13))datosCadena++;int esNegativo=0;if(*datosCadena=='-'||*datosCadena=='+')esNegativo=*datosCadena++=='-';
    if((!valorFondo||valorFondo==16)&&datosCadena[0]=='0'&&(datosCadena[1]=='x'||datosCadena[1]=='X')){valorFondo=16;datosCadena+=2;}if(!valorFondo)valorFondo=*datosCadena=='0'?8:10;
    unsigned long long datosTemporal=0;int valorCualquiera=0;for(;;){unsigned códigoCarácter=*datosCadena,datosDestino=códigoCarácter>='0'&&códigoCarácter<='9'?códigoCarácter-'0':códigoCarácter>='a'&&códigoCarácter<='z'?códigoCarácter-'a'+10:códigoCarácter>='A'&&códigoCarácter<='Z'?códigoCarácter-'A'+10:99;if(datosDestino>=(unsigned)valorFondo)break;valorCualquiera=1;datosCadena++;if(datosTemporal>(~0ull-datosDestino)/(unsigned)valorFondo){datosTemporal=~0ull;error=34;}else datosTemporal=datosTemporal*valorFondo+datosDestino;}
    if(desfaseFin)*desfaseFin=(char*)(valorCualquiera?datosCadena:iniciarDesfase);return esNegativo?0-datosTemporal:datosTemporal;
}
unsigned long strtoul(const char*datosCadena,char**entradaElementoAuxiliar,int valorSegundo){return strtoull(datosCadena,entradaElementoAuxiliar,valorSegundo);}
long strtol(const char*datosCadena,char**entradaElementoAuxiliar,int valorSegundo){return (long)strtoull(datosCadena,entradaElementoAuxiliar,valorSegundo);}
int atoi(const char*datosCadena){return (int)strtol(datosCadena,0,10);}
long double ldexpl(long double coordenadaCoordenadaHorizontal,int númeroElementosElementoLista){while(númeroElementosElementoLista>0){coordenadaCoordenadaHorizontal*=2;númeroElementosElementoLista--;}while(númeroElementosElementoLista<0){coordenadaCoordenadaHorizontal/=2;númeroElementosElementoLista++;}return coordenadaCoordenadaHorizontal;}
long double strtold(const char*datosCadena,char**desfaseFin){
    const char*iniciarDesfase=datosCadena;while(*datosCadena==' '||(*datosCadena>=9&&*datosCadena<=13))datosCadena++;int esNegativo=0;if(*datosCadena=='-'||*datosCadena=='+')esNegativo=*datosCadena++=='-';
    int valorFondo=10;if(datosCadena[0]=='0'&&(datosCadena[1]=='x'||datosCadena[1]=='X')){valorFondo=16;datosCadena+=2;}long double datosTemporal=0,escala=1;int fraccionario=0,valorCualquiera=0;
    for(;;){int códigoCarácter=*datosCadena,datosDestino=códigoCarácter>='0'&&códigoCarácter<='9'?códigoCarácter-'0':códigoCarácter>='a'&&códigoCarácter<='f'?códigoCarácter-'a'+10:códigoCarácter>='A'&&códigoCarácter<='F'?códigoCarácter-'A'+10:99;
        if(códigoCarácter=='.'&&!fraccionario){fraccionario=1;datosCadena++;continue;}if(datosDestino>=valorFondo)break;valorCualquiera=1;datosCadena++;datosTemporal=datosTemporal*valorFondo+datosDestino;if(fraccionario)escala*=valorFondo;
    }datosTemporal/=escala;
    if((valorFondo==10&&(*datosCadena=='e'||*datosCadena=='E'))||(valorFondo==16&&(*datosCadena=='p'||*datosCadena=='P'))){const char*mostrarValor=datosCadena++;int restarValores=0;if(*datosCadena=='-'||*datosCadena=='+')restarValores=*datosCadena++=='-';int númeroElementosElementoLista=0,númeroElementosEntradaElemento=0;while(*datosCadena>='0'&&*datosCadena<='9'){númeroElementosEntradaElemento++;if(númeroElementosElementoLista<20000)númeroElementosElementoLista=númeroElementosElementoLista*10+*datosCadena-'0';datosCadena++;}if(!númeroElementosEntradaElemento)datosCadena=mostrarValor;else{long double factor=valorFondo==16?2:10;while(númeroElementosElementoLista-->0&&númeroElementosElementoLista<200000)datosTemporal=restarValores?datosTemporal/factor:datosTemporal*factor;}}
    if(desfaseFin)*desfaseFin=(char*)(valorCualquiera?datosCadena:iniciarDesfase);return esNegativo?-datosTemporal:datosTemporal;
}
double strtod(const char*datosCadena,char**entradaElementoAuxiliar){return (double)strtold(datosCadena,entradaElementoAuxiliar);}float strtof(const char*datosCadena,char**entradaElementoAuxiliar){return (float)strtold(datosCadena,entradaElementoAuxiliar);}
void qsort(void*valorFondo,size_t númeroElementosElementoLista,size_t tamaño,int(*comparar)(const void*,const void*)){
    unsigned char*posiciónDatos=valorFondo;for(size_t índiceOrdinal=1;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)for(size_t ordinalInterior=índiceOrdinal;ordinalInterior&&comparar(posiciónDatos+(ordinalInterior-1)*tamaño,posiciónDatos+ordinalInterior*tamaño)>0;ordinalInterior--)for(size_t índiceTercero=0;índiceTercero<tamaño;índiceTercero++){unsigned char códigoCarácter=posiciónDatos[(ordinalInterior-1)*tamaño+índiceTercero];posiciónDatos[(ordinalInterior-1)*tamaño+índiceTercero]=posiciónDatos[ordinalInterior*tamaño+índiceTercero];posiciónDatos[ordinalInterior*tamaño+índiceTercero]=códigoCarácter;}
}
static struct {int capacidadUsado,índiceBuscar;size_t posición;} abierto[24];
static unsigned char salida[32768];static size_t tamañoSalida,posiciónSalida;static int abrirSalida;
const unsigned char *salidaC(size_t *númeroElementosElementoLista){*númeroElementosElementoLista=tamañoSalida;return salida;}
int open(const char*nombre,int bitsConfiguración,...){
    if(!strcmp(nombre,"/@cc-output")){if(abrirSalida){error=16;return -1;}abrirSalida=1;tamañoSalida=posiciónSalida=0;return 100;}
    for(unsigned índiceOrdinal=0;índiceOrdinal<sizeof(recursosCompilador)/sizeof(recursosCompilador[0]);índiceOrdinal++)if(!strcmp(nombre,recursosCompilador[índiceOrdinal].nombre)){
        if(bitsConfiguración&3){error=30;return -1;}for(int ordinalInterior=0;ordinalInterior<24;ordinalInterior++)if(!abierto[ordinalInterior].capacidadUsado){abierto[ordinalInterior].capacidadUsado=1;abierto[ordinalInterior].índiceBuscar=índiceOrdinal;abierto[ordinalInterior].posición=0;return 128+ordinalInterior;}error=24;return -1;
    }
    intptr_t valorDevuelto=invocarUsuario(3,(uintptr_t)nombre,bitsConfiguración,0,0,0,0);if(valorDevuelto<0){error=-valorDevuelto;return -1;}return valorDevuelto;
}
int close(int manejadorArchivo){if(manejadorArchivo==100){abrirSalida=0;return 0;}if(manejadorArchivo>=128&&manejadorArchivo<152){abierto[manejadorArchivo-128].capacidadUsado=0;return 0;}intptr_t valorDevuelto=invocarUsuario(4,manejadorArchivo,0,0,0,0,0);if(valorDevuelto<0){error=-valorDevuelto;return -1;}return 0;}
long read(int manejadorArchivo,void*Datos,size_t númeroElementosElementoLista){
    if(manejadorArchivo>=128&&manejadorArchivo<152&&abierto[manejadorArchivo-128].capacidadUsado){int índiceOrdinal=manejadorArchivo-128;const recursoCompilador*valorDevuelto=&recursosCompilador[abierto[índiceOrdinal].índiceBuscar];size_t ladoIzquierdo=valorDevuelto->tamaño-abierto[índiceOrdinal].posición;if(númeroElementosElementoLista>ladoIzquierdo)númeroElementosElementoLista=ladoIzquierdo;memcpy(Datos,valorDevuelto->Datos+abierto[índiceOrdinal].posición,númeroElementosElementoLista);abierto[índiceOrdinal].posición+=númeroElementosElementoLista;return númeroElementosElementoLista;}
    intptr_t valorDevuelto=invocarUsuario(2,manejadorArchivo,(uintptr_t)Datos,númeroElementosElementoLista,0,0,0);if(valorDevuelto<0){error=-valorDevuelto;return -1;}return valorDevuelto;
}
long write(int manejadorArchivo,const void*Datos,size_t númeroElementosElementoLista){
    if(manejadorArchivo==100){if(númeroElementosElementoLista>sizeof(salida)-posiciónSalida){error=28;return -1;}memcpy(salida+posiciónSalida,Datos,númeroElementosElementoLista);posiciónSalida+=númeroElementosElementoLista;if(tamañoSalida<posiciónSalida)tamañoSalida=posiciónSalida;return númeroElementosElementoLista;}
    intptr_t valorDevuelto=invocarUsuario(1,manejadorArchivo,(uintptr_t)Datos,númeroElementosElementoLista,0,0,0);if(valorDevuelto<0){error=-valorDevuelto;return -1;}return valorDevuelto;
}
long lseek(int manejadorArchivo,long valorDesfase,int posicionarOrigen){
    if(manejadorArchivo==100){long posiciónDatos=valorDesfase+(posicionarOrigen==0?0:posicionarOrigen==1?posiciónSalida:tamañoSalida);if(posiciónDatos<0||(size_t)posiciónDatos>sizeof(salida)){error=22;return -1;}posiciónSalida=posiciónDatos;return posiciónDatos;}
    if(manejadorArchivo>=128&&manejadorArchivo<152&&abierto[manejadorArchivo-128].capacidadUsado){int índiceOrdinal=manejadorArchivo-128;long posiciónDatos=valorDesfase+(posicionarOrigen==0?0:posicionarOrigen==1?abierto[índiceOrdinal].posición:recursosCompilador[abierto[índiceOrdinal].índiceBuscar].tamaño);if(posiciónDatos<0||(size_t)posiciónDatos>recursosCompilador[abierto[índiceOrdinal].índiceBuscar].tamaño){error=22;return -1;}abierto[índiceOrdinal].posición=posiciónDatos;return posiciónDatos;}
    intptr_t valorDevuelto=invocarUsuario(5,manejadorArchivo,valorDesfase,posicionarOrigen,0,0,0);if(valorDevuelto<0){error=-valorDevuelto;return -1;}return valorDevuelto;
}
int unlink(const char*nombre){intptr_t valorDevuelto=invocarUsuario(11,(uintptr_t)nombre,0,0,0,0,0);if(valorDevuelto<0){error=-valorDevuelto;return -1;}return valorDevuelto;}
char *realpath(const char*nombre,char*datosResultado){if(!datosResultado){datosResultado=malloc(strlen(nombre)+1);if(!datosResultado)return 0;}return strcpy(datosResultado,nombre);}
char *getcwd(char*posiciónDatos,size_t númeroElementosElementoLista){if(númeroElementosElementoLista<2){error=34;return 0;}posiciónDatos[0]='/';posiciónDatos[1]=0;return posiciónDatos;}
char *strerror(int entradaElementoAuxiliar){(void)entradaElementoAuxiliar;return "native compiler I/O error";}
time_t time(time_t*entradaElementoTerminal){time_t datosTemporal=0;if(entradaElementoTerminal)*entradaElementoTerminal=datosTemporal;return datosTemporal;}
struct tm *localtime(const time_t*entradaElementoTerminal){(void)entradaElementoTerminal;static struct tm datosTemporal={.tm_year=126,.tm_mon=0,.tm_mday=1};return &datosTemporal;}
static FILE flujos[18]={{1,0,1},{2,0,1}};FILE*stdout=&flujos[0],*stderr=&flujos[1];
FILE*fdopen(int manejadorArchivo,const char*modoMétodo){(void)modoMétodo;for(unsigned índiceOrdinal=2;índiceOrdinal<18;índiceOrdinal++)if(!flujos[índiceOrdinal].capacidadUsado){flujos[índiceOrdinal].capacidadUsado=1;flujos[índiceOrdinal].error=0;flujos[índiceOrdinal].manejadorArchivo=manejadorArchivo;return &flujos[índiceOrdinal];}error=24;return 0;}
int fflush(FILE*entradaElementoArchivo){return entradaElementoArchivo&&entradaElementoArchivo->error?-1:0;}
int fclose(FILE*entradaElementoArchivo){int valorDevuelto=close(entradaElementoArchivo->manejadorArchivo);if(entradaElementoArchivo->error)valorDevuelto=-1;entradaElementoArchivo->capacidadUsado=0;return valorDevuelto;}
size_t fwrite(const void*posiciónDatos,size_t datosCadena,size_t númeroElementosElementoLista,FILE*entradaElementoArchivo){if(!datosCadena)return 0;if(númeroElementosElementoLista>SIZE_MAX/datosCadena){entradaElementoArchivo->error=1;return 0;}long valorDevuelto=write(entradaElementoArchivo->manejadorArchivo,posiciónDatos,datosCadena*númeroElementosElementoLista);if(valorDevuelto<0){entradaElementoArchivo->error=1;return 0;}return (size_t)valorDevuelto/datosCadena;}
int fputc(int códigoCarácter,FILE*entradaElementoArchivo){unsigned char valorSegundo=códigoCarácter;return fwrite(&valorSegundo,1,1,entradaElementoArchivo)==1?valorSegundo:EOF;}
int fputs(const char*datosCadena,FILE*entradaElementoArchivo){return fwrite(datosCadena,1,strlen(datosCadena),entradaElementoArchivo)==strlen(datosCadena)?0:EOF;}
static void ponerValor(char*datosResultado,size_t máximoCapacidad,size_t*posiciónActual,char códigoCarácter){if(*posiciónActual+1<máximoCapacidad)datosResultado[*posiciónActual]=códigoCarácter;(*posiciónActual)++;}
int vsnprintf(char*datosResultado,size_t máximoCapacidad,const char*formato,va_list argumentosArgumentosVariables){
    size_t posiciónActual=0;while(*formato){if(*formato!='%'){ponerValor(datosResultado,máximoCapacidad,&posiciónActual,*formato++);continue;}formato++;
        int ladoIzquierdo=0,valorCero=0,valorAlternativa=0;while(*formato=='-'||*formato=='0'||*formato=='#'||*formato=='+'||*formato==' '){if(*formato=='-')ladoIzquierdo=1;if(*formato=='0')valorCero=1;if(*formato=='#')valorAlternativa=1;formato++;}
        int valorAnchura=0,valorPrecisión=-1;if(*formato=='*'){valorAnchura=va_arg(argumentosArgumentosVariables,int);formato++;}else while(*formato>='0'&&*formato<='9')valorAnchura=valorAnchura*10+*formato++-'0';
        if(*formato=='.'){formato++;valorPrecisión=0;if(*formato=='*'){valorPrecisión=va_arg(argumentosArgumentosVariables,int);formato++;}else while(*formato>='0'&&*formato<='9')valorPrecisión=valorPrecisión*10+*formato++-'0';}
        int carácterAncho=0;while(*formato=='l'||*formato=='z'||*formato=='t'||*formato=='j'||*formato=='h'){if(*formato!='h')carácterAncho=1;formato++;}
        char categoríaTipo=*formato?*formato++:0,almacenamientoBúfer[80];const char*datosCadena=almacenamientoBúfer;size_t númeroElementosElementoLista=0;
        if(categoríaTipo=='s'){datosCadena=va_arg(argumentosArgumentosVariables,const char*);if(!datosCadena)datosCadena="(null)";númeroElementosElementoLista=strlen(datosCadena);if(valorPrecisión>=0&&númeroElementosElementoLista>(size_t)valorPrecisión)númeroElementosElementoLista=valorPrecisión;}
        else if(categoríaTipo=='c'){almacenamientoBúfer[0]=va_arg(argumentosArgumentosVariables,int);númeroElementosElementoLista=1;}
        else if(categoríaTipo=='%'){almacenamientoBúfer[0]='%';númeroElementosElementoLista=1;}
        else if(categoríaTipo=='d'||categoríaTipo=='i'||categoríaTipo=='u'||categoríaTipo=='x'||categoríaTipo=='X'||categoríaTipo=='o'||categoríaTipo=='p'){
            unsigned long long valor;int negativo=0;
            if(categoríaTipo=='d'||categoríaTipo=='i'){long long datosTemporal=carácterAncho?va_arg(argumentosArgumentosVariables,long long):va_arg(argumentosArgumentosVariables,int);negativo=datosTemporal<0;valor=negativo?0-(unsigned long long)datosTemporal:datosTemporal;}
            else valor=categoríaTipo=='p'?(uintptr_t)va_arg(argumentosArgumentosVariables,void*):carácterAncho?va_arg(argumentosArgumentosVariables,unsigned long long):va_arg(argumentosArgumentosVariables,unsigned);
            unsigned valorFondo=categoríaTipo=='x'||categoríaTipo=='X'||categoríaTipo=='p'?16:categoríaTipo=='o'?8:10;char númeroElementosDígito[64];unsigned capacidadUsado=0;
            do{númeroElementosDígito[capacidadUsado++]="0123456789abcdef"[valor%valorFondo];valor/=valorFondo;}while(valor);
            if(negativo)almacenamientoBúfer[númeroElementosElementoLista++]='-';if(categoríaTipo=='p'||(valorAlternativa&&valorFondo==16)){almacenamientoBúfer[númeroElementosElementoLista++]='0';almacenamientoBúfer[númeroElementosElementoLista++]='x';}
            for(int rellenarValor=(int)capacidadUsado;valorPrecisión>rellenarValor&&númeroElementosElementoLista<sizeof(almacenamientoBúfer)-capacidadUsado;rellenarValor++)almacenamientoBúfer[númeroElementosElementoLista++]='0';
            if(valorCero&&!ladoIzquierdo&&valorPrecisión<0)while(valorAnchura>(int)(númeroElementosElementoLista+capacidadUsado)&&númeroElementosElementoLista<sizeof(almacenamientoBúfer)-capacidadUsado)almacenamientoBúfer[númeroElementosElementoLista++]='0';
            while(capacidadUsado)almacenamientoBúfer[númeroElementosElementoLista++]=númeroElementosDígito[--capacidadUsado];
        }else{almacenamientoBúfer[0]='?';númeroElementosElementoLista=1;}
        if(valorAnchura>4096)valorAnchura=4096;while(!ladoIzquierdo&&valorAnchura>(int)númeroElementosElementoLista){ponerValor(datosResultado,máximoCapacidad,&posiciónActual,' ');valorAnchura--;}
        for(size_t índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)ponerValor(datosResultado,máximoCapacidad,&posiciónActual,datosCadena[índiceOrdinal]);while(ladoIzquierdo&&valorAnchura>(int)númeroElementosElementoLista){ponerValor(datosResultado,máximoCapacidad,&posiciónActual,' ');valorAnchura--;}
    }if(máximoCapacidad)datosResultado[posiciónActual<máximoCapacidad?posiciónActual:máximoCapacidad-1]=0;return posiciónActual;
}
int snprintf(char*datosResultado,size_t máximoCapacidad,const char*entradaElementoArchivo,...){va_list valorPrimero;va_start(valorPrimero,entradaElementoArchivo);int valorDevuelto=vsnprintf(datosResultado,máximoCapacidad,entradaElementoArchivo,valorPrimero);va_end(valorPrimero);return valorDevuelto;}
int sprintf(char*datosResultado,const char*entradaElementoArchivo,...){va_list valorPrimero;va_start(valorPrimero,entradaElementoArchivo);int valorDevuelto=vsnprintf(datosResultado,SIZE_MAX,entradaElementoArchivo,valorPrimero);va_end(valorPrimero);return valorDevuelto;}
int vfprintf(FILE*valorFlujo,const char*entradaElementoArchivo,va_list valorPrimero){char valorSegundo[2048];int númeroElementosElementoLista=vsnprintf(valorSegundo,sizeof(valorSegundo),entradaElementoArchivo,valorPrimero);if(númeroElementosElementoLista>2047)númeroElementosElementoLista=2047;return fwrite(valorSegundo,1,númeroElementosElementoLista,valorFlujo)==(size_t)númeroElementosElementoLista?númeroElementosElementoLista:-1;}
int fprintf(FILE*valorFlujo,const char*entradaElementoArchivo,...){va_list valorPrimero;va_start(valorPrimero,entradaElementoArchivo);int valorDevuelto=vfprintf(valorFlujo,entradaElementoArchivo,valorPrimero);va_end(valorPrimero);return valorDevuelto;}
int printf(const char*entradaElementoArchivo,...){va_list valorPrimero;va_start(valorPrimero,entradaElementoArchivo);int valorDevuelto=vfprintf(stdout,entradaElementoArchivo,valorPrimero);va_end(valorPrimero);return valorDevuelto;}
