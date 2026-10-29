/* valorNúcleo 전용 할당기와 valorContraseña 난수 공급. Usuario ELF의 libc와 별개이다. */
#include "soporteCriptografía.h"
#include "../denominación/nombresEnlazarMáquina.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t milisegundosTranscurridosPlaca(void);
typedef struct bloqueMemoria { size_t longitud; struct bloqueMemoria *elementoListaSiguiente; int valorUsar; } bloqueMemoria;
static unsigned char áreaMemoriaMemoria[2*1024*1024] __attribute__((aligned(16)));
static bloqueMemoria *valorFragmentoPrimero;
void *asignarMemoriaRemoto(size_t longitud) {
    if (!longitud || longitud>sizeof(áreaMemoriaMemoria)-64) return 0;
    longitud=(longitud+15)&~(size_t)15;
    if(!valorFragmentoPrimero){valorFragmentoPrimero=(void*)áreaMemoriaMemoria;valorFragmentoPrimero->longitud=sizeof(áreaMemoriaMemoria)-32;}
    for(bloqueMemoria *valorFragmento=valorFragmentoPrimero;valorFragmento;valorFragmento=valorFragmento->elementoListaSiguiente)if(!valorFragmento->valorUsar&&valorFragmento->longitud>=longitud){
        if(valorFragmento->longitud>=longitud+64){bloqueMemoria *fragmentoNuevo=(void*)((char*)valorFragmento+32+longitud);
            fragmentoNuevo->longitud=valorFragmento->longitud-longitud-32;fragmentoNuevo->elementoListaSiguiente=valorFragmento->elementoListaSiguiente;fragmentoNuevo->valorUsar=0;valorFragmento->elementoListaSiguiente=fragmentoNuevo;valorFragmento->longitud=longitud;}
        valorFragmento->valorUsar=1;return(char*)valorFragmento+32;
    }return 0;
}
void liberarRemoto(void *dirección) {
    if(!dirección)return;bloqueMemoria *valorFragmento=(void*)((char*)dirección-32);
    volatile unsigned char *valorBorrado=dirección;for(size_t índiceOrdinal=0;índiceOrdinal<valorFragmento->longitud;índiceOrdinal++)valorBorrado[índiceOrdinal]=0;
    valorFragmento->valorUsar=0;
    for(valorFragmento=valorFragmentoPrimero;valorFragmento&&valorFragmento->elementoListaSiguiente;){if(!valorFragmento->valorUsar&&!valorFragmento->elementoListaSiguiente->valorUsar){valorFragmento->longitud+=32+valorFragmento->elementoListaSiguiente->longitud;valorFragmento->elementoListaSiguiente=valorFragmento->elementoListaSiguiente->elementoListaSiguiente;}else valorFragmento=valorFragmento->elementoListaSiguiente;}
}
void *reasignarRemoto(void *dirección,size_t longitud){
    if(!dirección)return asignarMemoriaRemoto(longitud);if(!longitud){liberarRemoto(dirección);return 0;}
    bloqueMemoria *valorFragmento=(void*)((char*)dirección-32);void *direcciónNuevo=asignarMemoriaRemoto(longitud);
    if(direcciónNuevo){memcpy(direcciónNuevo,dirección,longitud<valorFragmento->longitud?longitud:valorFragmento->longitud);liberarRemoto(dirección);}return direcciónNuevo;
}
int strcmp(const char *operandoPrimero,const char *operandoSegundo){while(*operandoPrimero&&*operandoPrimero==*operandoSegundo){operandoPrimero++;operandoSegundo++;}return(unsigned char)*operandoPrimero-(unsigned char)*operandoSegundo;}
char *strchr(const char *textoPalabra,int valorCarácter){for(;;textoPalabra++){if(*textoPalabra==(char)valorCarácter)return(char*)textoPalabra;if(!*textoPalabra)return 0;}}
char *strstr(const char *textoPalabra,const char *valorEncontrado){size_t longitud=strlen(valorEncontrado);for(;*textoPalabra;textoPalabra++)if(!strncmp(textoPalabra,valorEncontrado,longitud))return(char*)textoPalabra;return longitud?0:(char*)textoPalabra;}
char *strncpy(char *valorDestino,const char *original,size_t longitud){size_t índiceOrdinal=0;for(;índiceOrdinal<longitud&&original[índiceOrdinal];índiceOrdinal++)valorDestino[índiceOrdinal]=original[índiceOrdinal];for(;índiceOrdinal<longitud;índiceOrdinal++)valorDestino[índiceOrdinal]=0;return valorDestino;}
char *strncat(char *valorDestino,const char *original,size_t longitud){char *terminación=valorDestino+strlen(valorDestino);while(longitud--&&*original)*terminación++=*original++;*terminación=0;return valorDestino;}
int strncasecmp(const char *operandoPrimero,const char *operandoSegundo,size_t longitud){while(longitud--){unsigned carácterPrimero=*operandoPrimero++,carácterSegundo=*operandoSegundo++;if(carácterPrimero>='A'&&carácterPrimero<='Z')carácterPrimero+=32;if(carácterSegundo>='A'&&carácterSegundo<='Z')carácterSegundo+=32;if(carácterPrimero!=carácterSegundo)return(int)carácterPrimero-(int)carácterSegundo;if(!carácterPrimero)break;}return 0;}
int strcasecmp(const char *operandoPrimero,const char *operandoSegundo){return strncasecmp(operandoPrimero,operandoSegundo,(size_t)-1);}
char *strtok_r(char *textoPalabra,const char *valorDelimitador,char **elementoListaSiguiente){if(!textoPalabra)textoPalabra=*elementoListaSiguiente;while(*textoPalabra&&strchr(valorDelimitador,*textoPalabra))textoPalabra++;if(!*textoPalabra){*elementoListaSiguiente=textoPalabra;return 0;}char *elementoListaInicialValor=textoPalabra;while(*textoPalabra&&!strchr(valorDelimitador,*textoPalabra))textoPalabra++;if(*textoPalabra)*textoPalabra++=0;*elementoListaSiguiente=textoPalabra;return elementoListaInicialValor;}
unsigned long strtoul(const char *textoPalabra, char **terminación, int valorBase) {
    const char *fuente=textoPalabra;unsigned long valor=0;int valorNegativo=0,valorDesbordamiento=0;
    while(*textoPalabra==' '||(*textoPalabra>=9&&*textoPalabra<=13))textoPalabra++;
    if(*textoPalabra=='-'||*textoPalabra=='+')valorNegativo=*textoPalabra++=='-';
    if((valorBase==0||valorBase==16)&&textoPalabra[0]=='0'&&(textoPalabra[1]=='x'||textoPalabra[1]=='X')&&
       ((textoPalabra[2]>='0'&&textoPalabra[2]<='9')||(textoPalabra[2]>='a'&&textoPalabra[2]<='f')||(textoPalabra[2]>='A'&&textoPalabra[2]<='F'))) {valorBase=16;textoPalabra+=2;}
    if(!valorBase)valorBase=*textoPalabra=='0'?8:10;
    if(valorBase<2||valorBase>36){if(terminación)*terminación=(char*)fuente;return 0;}
    const char *elementoListaInicialValor=textoPalabra;
    for(;;textoPalabra++) {
        unsigned valorCarácter=(unsigned char)*textoPalabra;
        unsigned númeroValor=valorCarácter>='0'&&valorCarácter<='9'?valorCarácter-'0':valorCarácter>='a'&&valorCarácter<='z'?valorCarácter-'a'+10:valorCarácter>='A'&&valorCarácter<='Z'?valorCarácter-'A'+10:36;
        if(númeroValor>=(unsigned)valorBase)break;
        if(valor>(~0ul-númeroValor)/(unsigned)valorBase)valorDesbordamiento=1;
        if(!valorDesbordamiento)valor=valor*(unsigned)valorBase+númeroValor;
    }
    if(terminación)*terminación=(char*)(textoPalabra==elementoListaInicialValor?fuente:textoPalabra);
    return valorDesbordamiento?~0ul:valorNegativo?0ul-valor:valor;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char semillaDoblePrueba[32];
static int estadoValorSemilla;
void resumenRemoto(const void *Datos, size_t longitud, unsigned char resultado[32]) {
    br_sha256_context valorContexto;
    br_sha256_init(&valorContexto); br_sha256_update(&valorContexto, Datos, longitud); br_sha256_out(&valorContexto, resultado);
    memset(&valorContexto, 0, sizeof(valorContexto));
}
#define registrosAleatorio(posición) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(posición)))
int aleatorioRemoto(unsigned char *valorDestino,unsigned longitud){
    if(!estadoValorSemilla){volatile unsigned char *Datos=(void*)0x01ff0000ul;const char *valorMarcador="JKRENRG1";unsigned valorDiferencia=0;
        for(unsigned índiceOrdinal=0;índiceOrdinal<8;índiceOrdinal++)valorDiferencia|=Datos[índiceOrdinal]^(unsigned char)valorMarcador[índiceOrdinal];
        if(!valorDiferencia){for(unsigned índiceOrdinal=0;índiceOrdinal<32;índiceOrdinal++)semillaDoblePrueba[índiceOrdinal]=Datos[8+índiceOrdinal];for(unsigned índiceOrdinal=0;índiceOrdinal<40;índiceOrdinal++)Datos[índiceOrdinal]=0;estadoValorSemilla=2;}
        else {estadoValorSemilla=1;registrosAleatorio(0)=(registrosAleatorio(0)&~0x1fffu)|1;}
    }
    if(estadoValorSemilla==2){while(longitud){unsigned char elementoListaSiguiente[32],valorEntrada[33];memcpy(valorEntrada,semillaDoblePrueba,32);valorEntrada[32]=0;resumenRemoto(valorEntrada,33,elementoListaSiguiente);
        valorEntrada[32]=1;resumenRemoto(valorEntrada,33,semillaDoblePrueba);memset(valorEntrada,0,33);
        unsigned númeroValor=longitud<32?longitud:32;memcpy(valorDestino,elementoListaSiguiente,númeroValor);memset(elementoListaSiguiente,0,32);valorDestino+=númeroValor;longitud-=númeroValor;}return 0;}
    uintptr_t valorLímite=milisegundosTranscurridosPlaca()+1000;
    while(longitud){if((registrosAleatorio(0x18)&0x80000020u)||milisegundosTranscurridosPlaca()>valorLímite)return -1;
        if(!(registrosAleatorio(0x24)&255))continue;uint32_t valor=registrosAleatorio(0x20);
        for(unsigned índiceOrdinal=0;índiceOrdinal<4&&longitud;índiceOrdinal++,longitud--){*valorDestino++=valor&255;valor>>=8;}}
    return 0;
}
