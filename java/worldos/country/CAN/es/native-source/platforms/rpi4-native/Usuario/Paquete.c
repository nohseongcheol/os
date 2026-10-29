#include "../denominación/nombresEnlazarMáquina.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "invocar.h"
#include "Paquete.h"
#include "uzlib.h"
static unsigned char archivoComprimido[16384], desempaquetado[16385];
static unsigned tamaño, central, listaEntradas;
static char claseEntradaElemento[256];
static unsigned leerBytesDos(unsigned posiciónActual) { return archivoComprimido[posiciónActual] | archivoComprimido[posiciónActual+1] << 8; }
static uint32_t leerBytesCuatro(unsigned posiciónActual) { return leerBytesDos(posiciónActual) | (uint32_t)leerBytesDos(posiciónActual+2) << 16; }
static int recortar(unsigned posiciónActual, unsigned númeroElementosElementoLista, unsigned límiteCapacidad) { return posiciónActual <= límiteCapacidad && númeroElementosElementoLista <= límiteCapacidad-posiciónActual; }
static size_t longitud(const char *datosCadena) { size_t númeroElementosElementoLista=0; while(datosCadena[númeroElementosElementoLista]) númeroElementosElementoLista++; return númeroElementosElementoLista; }
static int textoIgual(const unsigned char *valorPrimero, const unsigned char *valorSegundo, unsigned númeroElementosElementoLista) { for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)if(valorPrimero[índiceOrdinal]!=valorSegundo[índiceOrdinal])return 0;return 1; }
static int finArchivo(void *sinUsar) { (void)sinUsar; return -1; }
static int datosAtributo(const char *línea,unsigned capacidadUsado,int *existePuntoEntradaElemento) {
    if(capacidadUsado>=12 && textoIgual((const unsigned char*)línea,(const unsigned char*)"Class-Path: ",12))return -95;
    if(capacidadUsado>=12 && textoIgual((const unsigned char*)línea,(const unsigned char*)"Main-Class: ",12)) {
        unsigned valor=capacidadUsado-12;if(*existePuntoEntradaElemento||!valor||valor>=sizeof(claseEntradaElemento))return -8;
        for(unsigned índiceOrdinal=0;índiceOrdinal<valor;índiceOrdinal++){unsigned char códigoCarácter=línea[12+índiceOrdinal];if(códigoCarácter<=32||códigoCarácter=='/'||códigoCarácter=='\\')return -8;claseEntradaElemento[índiceOrdinal]=códigoCarácter;}
        claseEntradaElemento[valor]=0;*existePuntoEntradaElemento=1;
    }
    return 0;
}
static int miembro(unsigned posiciónActual, unsigned char *datosResultado, unsigned máximoCapacidad) {
    unsigned entradaElementoMétodo=leerBytesDos(posiciónActual+10), bitsConfiguración=leerBytesDos(posiciónActual+8), comprimido=leerBytesCuatro(posiciónActual+20), liberarTamaño=leerBytesCuatro(posiciónActual+24), local=leerBytesCuatro(posiciónActual+42);
    unsigned nombre=leerBytesDos(posiciónActual+28);
    if(liberarTamaño>máximoCapacidad || liberarTamaño>16384 || (entradaElementoMétodo!=0 && entradaElementoMétodo!=8) || (bitsConfiguración&~0x80e))return -8;
    if(!recortar(local,30,central) || leerBytesCuatro(local)!=0x04034b50 || leerBytesDos(local+8)!=entradaElementoMétodo || leerBytesDos(local+6)!=bitsConfiguración || leerBytesDos(local+26)!=nombre)return -8;
    unsigned iniciarDesfase=local+30, regiónAdicional=leerBytesDos(local+28);
    if(!recortar(iniciarDesfase,nombre,central) || !textoIgual(archivoComprimido+iniciarDesfase,archivoComprimido+posiciónActual+46,nombre))return -8;
    iniciarDesfase+=nombre;if(!recortar(iniciarDesfase,regiónAdicional,central))return -8;iniciarDesfase+=regiónAdicional;
    if(!recortar(iniciarDesfase,comprimido,central))return -8;
    if(!(bitsConfiguración&8) && (leerBytesCuatro(local+14)!=leerBytesCuatro(posiciónActual+16) || leerBytesCuatro(local+18)!=comprimido || leerBytesCuatro(local+22)!=liberarTamaño))return -8;
    if(entradaElementoMétodo==0) { if(comprimido!=liberarTamaño)return -8; for(unsigned índiceOrdinal=0;índiceOrdinal<liberarTamaño;índiceOrdinal++)datosResultado[índiceOrdinal]=archivoComprimido[iniciarDesfase+índiceOrdinal]; }
    else {
        uzlib_uncomp_t datosDestino={0};uzlib_uncompress_init(&datosDestino,0,0);
        datosDestino.source=archivoComprimido+iniciarDesfase;datosDestino.source_limit=datosDestino.source+comprimido;datosDestino.source_read_cb=finArchivo;
        /* One extra output byte lets inflate consume/check the end marker. */
        datosDestino.dest_start=datosDestino.dest=desempaquetado;datosDestino.dest_limit=desempaquetado+liberarTamaño+1;
        int valorDevuelto=uzlib_uncompress(&datosDestino);
        if(valorDevuelto!=UZLIB_DONE || datosDestino.eof || datosDestino.dest!=desempaquetado+liberarTamaño || datosDestino.source!=datosDestino.source_limit)return -8;
        for(unsigned índiceOrdinal=0;índiceOrdinal<liberarTamaño;índiceOrdinal++)datosResultado[índiceOrdinal]=desempaquetado[índiceOrdinal];
    }
    if((uzlib_crc32(datosResultado,liberarTamaño,0xffffffffu)^0xffffffffu)!=leerBytesCuatro(posiciónActual+16))return -8;
    return liberarTamaño;
}
int leerJAR(const char *nombre, unsigned char *datosResultado, unsigned capacidadBúfer) {
    if(!listaEntradas)return -2;unsigned númeroElementosElementoLista=longitud(nombre),posiciónActual=central;
    for(unsigned índiceOrdinal=0;índiceOrdinal<listaEntradas;índiceOrdinal++) {
        unsigned longitudNombre=leerBytesDos(posiciónActual+28);
        if(longitudNombre==númeroElementosElementoLista && textoIgual(archivoComprimido+posiciónActual+46,(const unsigned char*)nombre,númeroElementosElementoLista))return miembro(posiciónActual,datosResultado,capacidadBúfer);
        posiciónActual+=46+longitudNombre+leerBytesDos(posiciónActual+30)+leerBytesDos(posiciónActual+32);
    }
    return -2;
}
const char *principalJAR(void) { return claseEntradaElemento; }
int abrirJAR(const char *nombreEntradaElementoArchivo) {
    listaEntradas=0;claseEntradaElemento[0]=0;
    intptr_t manejadorArchivo=invocarUsuario(3,(uintptr_t)nombreEntradaElementoArchivo,0,0,0,0,0);if(manejadorArchivo<0)return manejadorArchivo;
    intptr_t númeroElementosElementoLista=invocarUsuario(9,manejadorArchivo,0,0,0,0,0);
    if(númeroElementosElementoLista<22 || númeroElementosElementoLista>(intptr_t)sizeof(archivoComprimido)) { invocarUsuario(4,manejadorArchivo,0,0,0,0,0);return -8; }
    intptr_t númeroElementosRecibido=invocarUsuario(2,manejadorArchivo,(uintptr_t)archivoComprimido,númeroElementosElementoLista,0,0,0);invocarUsuario(4,manejadorArchivo,0,0,0,0,0);
    if(númeroElementosRecibido!=númeroElementosElementoLista)return -5;tamaño=númeroElementosElementoLista;
    unsigned desfaseFin=tamaño-22;
    for(;;) { if(leerBytesCuatro(desfaseFin)==0x06054b50 && desfaseFin+22+leerBytesDos(desfaseFin+20)==tamaño)break; if(!desfaseFin)return -8;desfaseFin--; }
    unsigned númeroElementosEntradaElemento=leerBytesDos(desfaseFin+10);central=leerBytesCuatro(desfaseFin+16);
    if(leerBytesDos(desfaseFin+4)||leerBytesDos(desfaseFin+6)||leerBytesDos(desfaseFin+8)!=númeroElementosEntradaElemento||!númeroElementosEntradaElemento||númeroElementosEntradaElemento>256||!recortar(central,leerBytesCuatro(desfaseFin+12),desfaseFin)||central+leerBytesCuatro(desfaseFin+12)!=desfaseFin)return -8;
    unsigned posiciónActual=central;
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosEntradaElemento;índiceOrdinal++) {
        if(!recortar(posiciónActual,46,desfaseFin)||leerBytesCuatro(posiciónActual)!=0x02014b50||leerBytesDos(posiciónActual+34))return -8;
        unsigned longitudNombre=leerBytesDos(posiciónActual+28),elementoListaSiguiente=46+longitudNombre+leerBytesDos(posiciónActual+30)+leerBytesDos(posiciónActual+32);
        if(!longitudNombre||longitudNombre>511||!recortar(posiciónActual,elementoListaSiguiente,desfaseFin)||leerBytesCuatro(posiciónActual+24)>16384)return -8;
        for(unsigned ordinalInterior=0;ordinalInterior<longitudNombre;ordinalInterior++)if(!archivoComprimido[posiciónActual+46+ordinalInterior])return -8;
        unsigned entradaElementoOtro=central;
        for(unsigned ordinalInterior=0;ordinalInterior<índiceOrdinal;ordinalInterior++){unsigned datosLongitud=leerBytesDos(entradaElementoOtro+28);if(datosLongitud==longitudNombre&&textoIgual(archivoComprimido+entradaElementoOtro+46,archivoComprimido+posiciónActual+46,datosLongitud))return -8;entradaElementoOtro+=46+datosLongitud+leerBytesDos(entradaElementoOtro+30)+leerBytesDos(entradaElementoOtro+32);}
        posiciónActual+=elementoListaSiguiente;
    }
    if(posiciónActual!=desfaseFin)return -8;listaEntradas=númeroElementosEntradaElemento;
    unsigned char manifiestoPaquete[4096];int tamañoGrupo=leerJAR("META-INF/MANIFEST.MF",manifiestoPaquete,sizeof(manifiestoPaquete)-1);if(tamañoGrupo<0){listaEntradas=0;return -8;}
    manifiestoPaquete[tamañoGrupo]=0;
    char lógico[512];unsigned capacidadUsado=0,valorÍndice=0;int existePuntoEntradaElemento=0;
    while(valorÍndice<(unsigned)tamañoGrupo) {
        unsigned ponerEnMarcha=valorÍndice;while(valorÍndice<(unsigned)tamañoGrupo && manifiestoPaquete[valorÍndice]!='\n')valorÍndice++;
        unsigned datosLongitud=valorÍndice-ponerEnMarcha;if(valorÍndice<(unsigned)tamañoGrupo)valorÍndice++;if(datosLongitud && manifiestoPaquete[ponerEnMarcha+datosLongitud-1]=='\r')datosLongitud--;
        if(capacidadUsado && datosLongitud && manifiestoPaquete[ponerEnMarcha]==' ') {ponerEnMarcha++;datosLongitud--;}
        else {
            int resultado=datosAtributo(lógico,capacidadUsado,&existePuntoEntradaElemento);if(resultado)return resultado;
            capacidadUsado=0;if(!datosLongitud)break;
        }
        if(datosLongitud>sizeof(lógico)-capacidadUsado)return -8;
        for(unsigned índiceOrdinal=0;índiceOrdinal<datosLongitud;índiceOrdinal++)lógico[capacidadUsado++]=manifiestoPaquete[ponerEnMarcha+índiceOrdinal];
    }
    /* The last attribute may be followed by only one newline. */
    int resultado=datosAtributo(lógico,capacidadUsado,&existePuntoEntradaElemento);if(resultado)return resultado;
    return existePuntoEntradaElemento?0:-8;
}
