/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 conectar, 제한된 valorEntrada longitud, 비동기 enviarValor, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 Pantalla Datos 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "valorRemoto.h"
#include "soporteCriptografía.h"
#include "perfil.h"
#include "../PilaRed/PilaRed.h"
#include "../máquina/informaciónPantalla.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(contraseñaPantalla)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t milisegundosTranscurridosPlaca(void);
extern uintptr_t terminalPlaca(uintptr_t);
void trazoTeclaRemoto(unsigned,int);
void inicializarTrazoTeclaRemoto(void);
void teclaRemotoConfirmar(void);
static int extremoEscuchaEnCurso=-1,valorParRed=-1,valorEtapa,futuroCerrar;
static uintptr_t tiempoConexión,otraVezRecibirActivado;
static unsigned char valorEntrada[8192],Salida[4096],valorDesafío[16];
static unsigned númeroElementosEntrada,númeroElementosSalida,númeroElementosEnviado;
static unsigned valorAnchura,valorAltura,tamañoPíxel=4,valorOrdenBytesGrande,máximoRojo=255,máximoVerde=255,máximoAzul=255,desplazarRojo=16,desplazarVerde=8,desplazarAzul;
static uint32_t resumenElementoPrevio[60*68];
static unsigned short baldosaCambiado[60*68];
static unsigned númeroElementosBaldosa,posiciónBaldosa,coordenadaHorizontalSolicitado,coordenadaVerticalSolicitado,extensiónRangoSolicitado,alturaSolicitado;
static unsigned leer16Bits(const unsigned char *posiciónDatos){return(unsigned)posiciónDatos[0]*256+posiciónDatos[1];}
static uint32_t leer32Bits(const unsigned char *posiciónDatos){return(uint32_t)posiciónDatos[0]<<24|(uint32_t)posiciónDatos[1]<<16|(uint32_t)posiciónDatos[2]<<8|posiciónDatos[3];}
static void escribir16Bits(unsigned char *posiciónDatos,unsigned valor){posiciónDatos[0]=valor>>8;posiciónDatos[1]=valor;}
static void escribir32Bits(unsigned char *posiciónDatos,uint32_t valor){posiciónDatos[0]=valor>>24;posiciónDatos[1]=valor>>16;posiciónDatos[2]=valor>>8;posiciónDatos[3]=valor;}
static void cerrar(void){if(valorParRed>=0)cerrarRed(valorParRed);valorParRed=-1;valorEtapa=0;númeroElementosEntrada=númeroElementosSalida=númeroElementosEnviado=0;númeroElementosBaldosa=posiciónBaldosa=0;futuroCerrar=0;inicializarTrazoTeclaRemoto();otraVezRecibirActivado=milisegundosTranscurridosPlaca()+500;}
static void emitirValor(const void *Datos,unsigned númeroValor){memcpy(Salida,Datos,númeroValor);númeroElementosSalida=númeroValor;númeroElementosEnviado=0;}
static void consumirValor(unsigned númeroValor){númeroElementosEntrada-=númeroValor;memmove(valorEntrada,valorEntrada+númeroValor,númeroElementosEntrada);}
int presentarRemotoControl(unsigned acción){
    if(acción==0){cerrar();if(extremoEscuchaEnCurso>=0)cerrarRed(extremoEscuchaEnCurso);extremoEscuchaEnCurso=-1;return 0;}
    if(acción!=1)return extremoEscuchaEnCurso>=0;
    if(extremoEscuchaEnCurso>=0)return 0;
    int valorPuerto=crearExtremoConectorRed(1);if(valorPuerto<0)return valorPuerto;direcciónConectorRedReutilizar(valorPuerto);
    int resultado=asociarRedCorta(valorPuerto,0,5900);if(!resultado)resultado=escucharRedCorta(valorPuerto);
    if(resultado<0){cerrarRed(valorPuerto);return resultado;}extremoEscuchaEnCurso=valorPuerto;return 0;
}
static uint32_t resumenBaldosa(unsigned posiciónHorizontal,unsigned posiciónVertical){
    uint32_t valor=2166136261u;
    for(unsigned coordenadaCoordenadaVertical=posiciónVertical;coordenadaCoordenadaVertical<posiciónVertical+16&&coordenadaCoordenadaVertical<valorAltura;coordenadaCoordenadaVertical++)for(unsigned coordenadaCoordenadaHorizontal=posiciónHorizontal;coordenadaCoordenadaHorizontal<posiciónHorizontal+32&&coordenadaCoordenadaHorizontal<valorAnchura;coordenadaCoordenadaHorizontal++)valor=(valor^pantallaLeerPlaca(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical))*16777619u;
    return valor;
}
static void peticiónPantalla(const unsigned char *posiciónDatos){
    coordenadaHorizontalSolicitado=leer16Bits(posiciónDatos+2);coordenadaVerticalSolicitado=leer16Bits(posiciónDatos+4);extensiónRangoSolicitado=leer16Bits(posiciónDatos+6);alturaSolicitado=leer16Bits(posiciónDatos+8);
    if(coordenadaHorizontalSolicitado>=valorAnchura||coordenadaVerticalSolicitado>=valorAltura)extensiónRangoSolicitado=alturaSolicitado=0;
    if(extensiónRangoSolicitado>valorAnchura-coordenadaHorizontalSolicitado&&coordenadaHorizontalSolicitado<valorAnchura)extensiónRangoSolicitado=valorAnchura-coordenadaHorizontalSolicitado;
    if(alturaSolicitado>valorAltura-coordenadaVerticalSolicitado&&coordenadaVerticalSolicitado<valorAltura)alturaSolicitado=valorAltura-coordenadaVerticalSolicitado;
    númeroElementosBaldosa=posiciónBaldosa=0;
    if(extensiónRangoSolicitado&&alturaSolicitado)for(unsigned coordenadaCoordenadaVertical=coordenadaVerticalSolicitado/16;coordenadaCoordenadaVertical<=(coordenadaVerticalSolicitado+alturaSolicitado-1)/16;coordenadaCoordenadaVertical++)for(unsigned coordenadaCoordenadaHorizontal=coordenadaHorizontalSolicitado/32;coordenadaCoordenadaHorizontal<=(coordenadaHorizontalSolicitado+extensiónRangoSolicitado-1)/32;coordenadaCoordenadaHorizontal++){
        unsigned índicePosición=coordenadaCoordenadaVertical*60+coordenadaCoordenadaHorizontal;uint32_t valorResumen=resumenBaldosa(coordenadaCoordenadaHorizontal*32,coordenadaCoordenadaVertical*16);
        if(!posiciónDatos[1]||resumenElementoPrevio[índicePosición]!=valorResumen)baldosaCambiado[númeroElementosBaldosa++]=índicePosición;
    }
    Salida[0]=Salida[1]=0;escribir16Bits(Salida+2,númeroElementosBaldosa);númeroElementosSalida=4;númeroElementosEnviado=0;
}
static void enviarBaldosa(void){
    unsigned índicePosición=baldosaCambiado[posiciónBaldosa++],posiciónHorizontal=(índicePosición%60)*32,posiciónVertical=(índicePosición/60)*16;
    unsigned coordenadaHorizontalFin=posiciónHorizontal+32,coordenadaVerticalFin=posiciónVertical+16;if(coordenadaHorizontalFin>valorAnchura)coordenadaHorizontalFin=valorAnchura;if(coordenadaVerticalFin>valorAltura)coordenadaVerticalFin=valorAltura;
    /* valorSubparte 타일 petición 뒤에도 valorRestoDivisión 화소를 보낸 것으로 처리하지 않는다. */
    int valoresTodos=posiciónHorizontal>=coordenadaHorizontalSolicitado&&posiciónVertical>=coordenadaVerticalSolicitado&&coordenadaHorizontalFin<=coordenadaHorizontalSolicitado+extensiónRangoSolicitado&&coordenadaVerticalFin<=coordenadaVerticalSolicitado+alturaSolicitado;
    if(valoresTodos)resumenElementoPrevio[índicePosición]=resumenBaldosa(posiciónHorizontal,posiciónVertical);
    if(posiciónHorizontal<coordenadaHorizontalSolicitado)posiciónHorizontal=coordenadaHorizontalSolicitado;if(posiciónVertical<coordenadaVerticalSolicitado)posiciónVertical=coordenadaVerticalSolicitado;
    if(coordenadaHorizontalFin>coordenadaHorizontalSolicitado+extensiónRangoSolicitado)coordenadaHorizontalFin=coordenadaHorizontalSolicitado+extensiónRangoSolicitado;if(coordenadaVerticalFin>coordenadaVerticalSolicitado+alturaSolicitado)coordenadaVerticalFin=coordenadaVerticalSolicitado+alturaSolicitado;
    escribir16Bits(Salida,posiciónHorizontal);escribir16Bits(Salida+2,posiciónVertical);escribir16Bits(Salida+4,coordenadaHorizontalFin-posiciónHorizontal);escribir16Bits(Salida+6,coordenadaVerticalFin-posiciónVertical);escribir32Bits(Salida+8,0);
    númeroElementosSalida=12;númeroElementosEnviado=0;
    for(unsigned coordenadaCoordenadaVertical=posiciónVertical;coordenadaCoordenadaVertical<coordenadaVerticalFin;coordenadaCoordenadaVertical++)for(unsigned coordenadaCoordenadaHorizontal=posiciónHorizontal;coordenadaCoordenadaHorizontal<coordenadaHorizontalFin;coordenadaCoordenadaHorizontal++){
        uint32_t valorColor=pantallaLeerPlaca(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical),valor=(((valorColor>>16)&255)*máximoRojo/255)<<desplazarRojo|
            (((valorColor>>8)&255)*máximoVerde/255)<<desplazarVerde|((valorColor&255)*máximoAzul/255)<<desplazarAzul;
        for(unsigned índiceOrdinal=0;índiceOrdinal<tamañoPíxel;índiceOrdinal++)Salida[númeroElementosSalida++]=valor>>(8*(valorOrdenBytesGrande?tamañoPíxel-1-índiceOrdinal:índiceOrdinal));
    }
}
void inspeccionarPresentarRemoto(void){
    if(extremoEscuchaEnCurso<0)return;
    if(valorParRed<0){if(milisegundosTranscurridosPlaca()<otraVezRecibirActivado)return;valorParRed=aceptarRedCorta(extremoEscuchaEnCurso);if(valorParRed<0)return;
        tiempoConexión=milisegundosTranscurridosPlaca();valorEtapa=1;emitirValor("RFB 003.008\n",12);memset(resumenElementoPrevio,0,sizeof(resumenElementoPrevio));
        tamañoPíxel=4;valorOrdenBytesGrande=0;máximoRojo=máximoVerde=máximoAzul=255;desplazarRojo=16;desplazarVerde=8;desplazarAzul=0;}
    if(valorEtapa<5&&milisegundosTranscurridosPlaca()-tiempoConexión>15000){cerrar();return;}
    if(númeroElementosSalida){int númeroValor=escribirRedCorta(valorParRed,Salida+númeroElementosEnviado,númeroElementosSalida-númeroElementosEnviado);if(númeroValor>0){númeroElementosEnviado+=númeroValor;if(númeroElementosEnviado==númeroElementosSalida)númeroElementosSalida=númeroElementosEnviado=0;}else if(númeroValor!=-11){cerrar();return;}}
    if(!númeroElementosSalida&&futuroCerrar){cerrar();return;}
    if(!númeroElementosSalida&&posiciónBaldosa<númeroElementosBaldosa)enviarBaldosa();
    if(númeroElementosEntrada==sizeof(valorEntrada)){cerrar();return;}
    int númeroElementosRecibido=leerRedCorta(valorParRed,valorEntrada+númeroElementosEntrada,sizeof(valorEntrada)-númeroElementosEntrada);
    if(númeroElementosRecibido==0||(númeroElementosRecibido<0&&númeroElementosRecibido!=-11)){cerrar();return;}if(númeroElementosRecibido>0)númeroElementosEntrada+=númeroElementosRecibido;
    if(númeroElementosSalida||posiciónBaldosa<númeroElementosBaldosa)return;
    if(valorEtapa==1&&númeroElementosEntrada>=12){if(memcmp(valorEntrada,"RFB 003.008\n",12)){cerrar();return;}consumirValor(12);const unsigned char métodoAutenticación[]={1,2};emitirValor(métodoAutenticación,2);valorEtapa=2;return;}
    if(valorEtapa==2&&númeroElementosEntrada){if(valorEntrada[0]!=2||aleatorioRemoto(valorDesafío,16)){cerrar();return;}consumirValor(1);emitirValor(valorDesafío,16);valorEtapa=3;return;}
    if(valorEtapa==3&&númeroElementosEntrada>=16){unsigned char materialTecla[8],respuestaEsperadaCorrecto[16];br_des_ct_cbcenc_keys valorContraseña;
        for(unsigned índiceOrdinal=0;índiceOrdinal<8;índiceOrdinal++){unsigned valor=contraseñaPantalla[índiceOrdinal],esInvertido=0;for(unsigned ordinalInterior=0;ordinalInterior<8;ordinalInterior++){esInvertido=(esInvertido<<1)|(valor&1);valor>>=1;}materialTecla[índiceOrdinal]=esInvertido;}
        br_des_ct_cbcenc_init(&valorContraseña,materialTecla,8);memcpy(respuestaEsperadaCorrecto,valorDesafío,16);
        for(unsigned índiceOrdinal=0;índiceOrdinal<16;índiceOrdinal+=8){unsigned char valorVector[8]={0};br_des_ct_cbcenc_run(&valorContraseña,valorVector,respuestaEsperadaCorrecto+índiceOrdinal,8);memset(valorVector,0,8);}
        unsigned valorDiferencia=0;for(unsigned índiceOrdinal=0;índiceOrdinal<16;índiceOrdinal++)valorDiferencia|=respuestaEsperadaCorrecto[índiceOrdinal]^valorEntrada[índiceOrdinal];consumirValor(16);memset(&valorContraseña,0,sizeof(valorContraseña));memset(materialTecla,0,8);memset(respuestaEsperadaCorrecto,0,16);memset(valorDesafío,0,16);
        escribir32Bits(Salida,valorDiferencia?1:0);númeroElementosSalida=4;númeroElementosEnviado=0;
        if(valorDiferencia){escribir32Bits(Salida+4,19);memcpy(Salida+8,"Authentication fail",19);númeroElementosSalida=27;futuroCerrar=1;}else valorEtapa=4;return;}
    if(valorEtapa==4&&númeroElementosEntrada){consumirValor(1);valorAnchura=anchuraPantallaPlaca();valorAltura=alturaPantallaPlaca();if(!valorAnchura||!valorAltura||valorAnchura>1920||valorAltura>1080){cerrar();return;}
        if(!terminalPlaca(7)){const unsigned char evento[]={30,2,1,0,0,0,0};entradaRemotoAlimentar(evento,7);}
        memset(Salida,0,40);escribir16Bits(Salida,valorAnchura);escribir16Bits(Salida+2,valorAltura);Salida[4]=32;Salida[5]=24;Salida[7]=1;
        escribir16Bits(Salida+8,255);escribir16Bits(Salida+10,255);escribir16Bits(Salida+12,255);Salida[14]=16;Salida[15]=8;
        const char *nombre="jkoros native";escribir32Bits(Salida+20,strlen(nombre));memcpy(Salida+24,nombre,strlen(nombre));númeroElementosSalida=24+strlen(nombre);númeroElementosEnviado=0;valorEtapa=5;return;}
    if(valorEtapa!=5||!númeroElementosEntrada)return;
    unsigned categoríaTipo=valorEntrada[0],valorNecesario=categoríaTipo==0?20:categoríaTipo==2?4:categoríaTipo==3?10:categoríaTipo==4?8:categoríaTipo==5?6:categoríaTipo==6?8:0;
    if(!valorNecesario){cerrar();return;}if(númeroElementosEntrada<valorNecesario)return;
    if(categoríaTipo==2){unsigned númeroValor=leer16Bits(valorEntrada+2);if(númeroValor>128){cerrar();return;}valorNecesario+=númeroValor*4;}
    if(categoríaTipo==6){unsigned númeroValor=leer32Bits(valorEntrada+4);if(númeroValor>4096){cerrar();return;}valorNecesario+=númeroValor;}
    if(númeroElementosEntrada<valorNecesario)return;
    if(categoríaTipo==0){unsigned valorBit=valorEntrada[4],máximoCanalRojo=leer16Bits(valorEntrada+8),valorSegundos=leer16Bits(valorEntrada+10),máximoCanalAzul=leer16Bits(valorEntrada+12),desplazarCanalRojo=valorEntrada[14],desplazarCanalVerde=valorEntrada[15],desplazarCanalAzul=valorEntrada[16];
        if((valorBit!=16&&valorBit!=32)||!valorEntrada[7]||valorEntrada[6]>1||!máximoCanalRojo||!valorSegundos||!máximoCanalAzul||máximoCanalRojo>255||valorSegundos>255||máximoCanalAzul>255||desplazarCanalRojo>24||desplazarCanalVerde>24||desplazarCanalAzul>24||
           ((uint64_t)máximoCanalRojo<<desplazarCanalRojo)>((1ull<<valorBit)-1)||((uint64_t)valorSegundos<<desplazarCanalVerde)>((1ull<<valorBit)-1)||((uint64_t)máximoCanalAzul<<desplazarCanalAzul)>((1ull<<valorBit)-1)){cerrar();return;}
        tamañoPíxel=valorBit/8;valorOrdenBytesGrande=valorEntrada[6];máximoRojo=máximoCanalRojo;máximoVerde=valorSegundos;máximoAzul=máximoCanalAzul;desplazarRojo=desplazarCanalRojo;desplazarVerde=desplazarCanalVerde;desplazarAzul=desplazarCanalAzul;memset(resumenElementoPrevio,0,sizeof(resumenElementoPrevio));
    }else if(categoríaTipo==3)peticiónPantalla(valorEntrada);
    else if(categoríaTipo==4)trazoTeclaRemoto(leer32Bits(valorEntrada+4),valorEntrada[1]!=0);
    else if(categoríaTipo==5){unsigned coordenadaCoordenadaHorizontal=leer16Bits(valorEntrada+2),coordenadaCoordenadaVertical=leer16Bits(valorEntrada+4);if(coordenadaCoordenadaHorizontal>=valorAnchura)coordenadaCoordenadaHorizontal=valorAnchura-1;if(coordenadaCoordenadaVertical>=valorAltura)coordenadaCoordenadaVertical=valorAltura-1;
        if(valorEntrada[1])teclaRemotoConfirmar();
        unsigned char evento[]={30,1,valorEntrada[1],coordenadaCoordenadaHorizontal&255,coordenadaCoordenadaHorizontal>>8,coordenadaCoordenadaVertical&255,coordenadaCoordenadaVertical>>8};entradaRemotoAlimentar(evento,sizeof(evento));}
    consumirValor(valorNecesario);
}
