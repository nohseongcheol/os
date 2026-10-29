#include "../denominación/nombresEnlazarMáquina.h"
#include "informaciónPantalla.h"
/* propio 네 ventana 합성과 UTF-8 terminal. 바뀐 영역의 valorCompletado 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t palabraMáquina;
extern palabraMáquina píxelPlaca(palabraMáquina,palabraMáquina,palabraMáquina),búferImagenPlaca(void);
extern void *memset(void *,int,size_t);
extern const unsigned char fuenteTipográficaTerminal[];
#define columnasMáximo 237
#define númeroElementosLíneaHistorial 160
typedef struct {
    uint32_t celdasCarácter[númeroElementosLíneaHistorial][columnasMáximo]; uint8_t listaFormas[númeroElementosLíneaHistorial][columnasMáximo];
    unsigned valorAnchura,valorAltura,columnas,númeroElementosFila,redimensionadoEra;
    unsigned esEnVida,coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,posiciónFila,posiciónColumna,entradaElementoExtremoSuperior,desplazarVista,colorPrimerPlano,colorFondo,escapar,valorParámetro[4],índiceParámetro,filaGuardado,númeroColumnaGuardado;
    unsigned resultadoSinSigno,valorLargoSinSigno,valorFormatoPequeño,alternativo,visiblePuntoInserción;
} Terminal;
static Terminal listaVentanas[4];
static int foco=-1,salida,valorOrden[4],númeroElementosEntradaElemento,valorArrastrar=-1,coordenadaHorizontalArrastrar,coordenadaVerticalArrastrar;
static unsigned esPendiente,botones,vistaEscritorio,entradaHangul;
static const uint32_t coloresPíxel[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int visiblePantalla(int),punteroPantalla(int,unsigned,int,int);
extern void pantallaRedibujar(int);
static Terminal *entradaElementoTerminal;
static unsigned carácterAncho(unsigned códigoCarácter){return códigoCarácter>=256?2:1;}
static void regiónRectangular(unsigned coordenadaCoordenadaHorizontal,unsigned coordenadaCoordenadaVertical,unsigned valorAnchuraSolicitado,unsigned valorAlturaSolicitado,unsigned colorPíxel){
    rellenarRectánguloPlaca(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,valorAnchuraSolicitado,valorAlturaSolicitado,colorPíxel);
}
void glifoTerminal(unsigned coordenadaCoordenadaHorizontal,unsigned coordenadaCoordenadaVertical,unsigned códigoCarácter,unsigned colorPrimerPlano,unsigned colorFondo){
    unsigned valorAnchura=carácterAncho(códigoCarácter)*8;if(códigoCarácter==0xffffffffu)return;
    int ladoIzquierdo=coordenadaCoordenadaHorizontal,ladoSuperior=coordenadaCoordenadaVertical,extensiónRangoAnchura=valorAnchura,longitud=16;
    if(!límitesDibujoPlaca(&ladoIzquierdo,&ladoSuperior,&extensiónRangoAnchura,&longitud))return;
    if(códigoCarácter==' '){rellenarRectánguloPlaca(ladoIzquierdo,ladoSuperior,extensiónRangoAnchura,longitud,colorFondo);return;}
    unsigned índiceBuscar=códigoCarácter<65536?códigoCarácter:códigoCarácter>=0x1f600&&códigoCarácter<0x1f650?65536+códigoCarácter-0x1f600:0xfffd;
    const unsigned char *valorFuenteTipográfica=fuenteTipográficaTerminal+índiceBuscar*32;
    for(int línea=ladoSuperior;línea<ladoSuperior+longitud;línea++){unsigned listaBits=valorFuenteTipográfica[(línea-coordenadaCoordenadaVertical)*2]*256+valorFuenteTipográfica[(línea-coordenadaCoordenadaVertical)*2+1];for(int entradaElementoRanura=ladoIzquierdo;entradaElementoRanura<ladoIzquierdo+extensiónRangoAnchura;entradaElementoRanura++)píxelPlaca(entradaElementoRanura,línea,(listaBits&(0x8000>>(entradaElementoRanura-coordenadaCoordenadaHorizontal)))?colorPrimerPlano:colorFondo);}
}
static void tablaNombre(unsigned coordenadaCoordenadaHorizontal,unsigned coordenadaCoordenadaVertical,const char *datosCadena,unsigned colorPrimerPlano,unsigned colorFondo){while(*datosCadena){unsigned códigoCarácter=(unsigned char)*datosCadena++, númeroElementosRestante=0;if(códigoCarácter>=0xc0){númeroElementosRestante=códigoCarácter<0xe0?1:códigoCarácter<0xf0?2:3;códigoCarácter&=(1u<<(6-númeroElementosRestante))-1;while(númeroElementosRestante--&&*datosCadena)códigoCarácter=(códigoCarácter<<6)|((unsigned char)*datosCadena++&63);}glifoTerminal(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,códigoCarácter,colorPrimerPlano,colorFondo);coordenadaCoordenadaHorizontal+=carácterAncho(códigoCarácter)*8;}}
static unsigned entradaElementoPrimero(void){return entradaElementoTerminal->entradaElementoExtremoSuperior;}
static int esMostrado(void){return entradaElementoTerminal->esEnVida&&foco>=0&&entradaElementoTerminal==&listaVentanas[foco]&&!visiblePantalla(foco);}
static void pantallaPintar(unsigned posiciónFila,unsigned posiciónColumna){
    if(!esMostrado()||posiciónFila<entradaElementoPrimero()-entradaElementoTerminal->desplazarVista||posiciónFila>=entradaElementoPrimero()-entradaElementoTerminal->desplazarVista+entradaElementoTerminal->númeroElementosFila||posiciónColumna>=entradaElementoTerminal->columnas)return;
    unsigned códigoCarácter=entradaElementoTerminal->celdasCarácter[posiciónFila%númeroElementosLíneaHistorial][posiciónColumna],datosCadena=entradaElementoTerminal->listaFormas[posiciónFila%númeroElementosLíneaHistorial][posiciónColumna];
    if(carácterAncho(códigoCarácter)==2&&posiciónColumna+1>=entradaElementoTerminal->columnas)códigoCarácter=' ';
    glifoTerminal(entradaElementoTerminal->coordenadaCoordenadaHorizontal+12+posiciónColumna*8,entradaElementoTerminal->coordenadaCoordenadaVertical+36+(posiciónFila-entradaElementoPrimero()+entradaElementoTerminal->desplazarVista)*16,códigoCarácter?códigoCarácter:' ',coloresPíxel[datosCadena&15],coloresPíxel[datosCadena>>4]);
}
static void valorPuntoInserción(int mostrarVentana){if(!esMostrado()||entradaElementoTerminal->desplazarVista||entradaElementoTerminal->posiciónColumna>=entradaElementoTerminal->columnas||entradaElementoTerminal->posiciónFila<entradaElementoTerminal->entradaElementoExtremoSuperior||entradaElementoTerminal->posiciónFila>=entradaElementoTerminal->entradaElementoExtremoSuperior+entradaElementoTerminal->númeroElementosFila)return;
    if(!mostrarVentana||!entradaElementoTerminal->visiblePuntoInserción)pantallaPintar(entradaElementoTerminal->posiciónFila,entradaElementoTerminal->posiciónColumna);else regiónRectangular(entradaElementoTerminal->coordenadaCoordenadaHorizontal+12+entradaElementoTerminal->posiciónColumna*8,entradaElementoTerminal->coordenadaCoordenadaVertical+36+(entradaElementoTerminal->posiciónFila-entradaElementoTerminal->entradaElementoExtremoSuperior)*16+14,8,2,coloresPíxel[entradaElementoTerminal->colorPrimerPlano]);}
static void valorContenidoValor(void){
    regiónRectangular(entradaElementoTerminal->coordenadaCoordenadaHorizontal+12,entradaElementoTerminal->coordenadaCoordenadaVertical+36,entradaElementoTerminal->columnas*8,entradaElementoTerminal->númeroElementosFila*16,coloresPíxel[0]);
    int posiciónHorizontal=entradaElementoTerminal->coordenadaCoordenadaHorizontal+12,posiciónVertical=entradaElementoTerminal->coordenadaCoordenadaVertical+36,extensiónRangoAnchura=entradaElementoTerminal->columnas*8,longitud=entradaElementoTerminal->númeroElementosFila*16;
    if(límitesDibujoPlaca(&posiciónHorizontal,&posiciónVertical,&extensiónRangoAnchura,&longitud)){
    unsigned líneaPrimero=(posiciónVertical-entradaElementoTerminal->coordenadaCoordenadaVertical-36)/16,líneaÚltimo=(posiciónVertical+longitud-entradaElementoTerminal->coordenadaCoordenadaVertical-36+15)/16;
    unsigned ranuraPrimero=(posiciónHorizontal-entradaElementoTerminal->coordenadaCoordenadaHorizontal-12)/8,ranuraÚltimo=(posiciónHorizontal+extensiónRangoAnchura-entradaElementoTerminal->coordenadaCoordenadaHorizontal-12+7)/8;
    if(ranuraPrimero)ranuraPrimero--; /* 잘림 valorFrontera 왼쪽에서 시작한 두 entradaElementoRanura 글자도 그린다. */
    for(unsigned valorDevuelto=líneaPrimero;valorDevuelto<líneaÚltimo;valorDevuelto++)for(unsigned códigoCarácter=ranuraPrimero;códigoCarácter<ranuraÚltimo;códigoCarácter++){
        unsigned posiciónFila=entradaElementoPrimero()-entradaElementoTerminal->desplazarVista+valorDevuelto,valorCarácter=entradaElementoTerminal->celdasCarácter[posiciónFila%númeroElementosLíneaHistorial][códigoCarácter],datosCadena=entradaElementoTerminal->listaFormas[posiciónFila%númeroElementosLíneaHistorial][códigoCarácter];
        if(carácterAncho(valorCarácter)==2&&códigoCarácter+1>=entradaElementoTerminal->columnas)valorCarácter=' ';
        if((valorCarácter==0||valorCarácter==' ')&&(datosCadena>>4)==0)continue;
        glifoTerminal(entradaElementoTerminal->coordenadaCoordenadaHorizontal+12+códigoCarácter*8,entradaElementoTerminal->coordenadaCoordenadaVertical+36+valorDevuelto*16,valorCarácter?valorCarácter:' ',coloresPíxel[datosCadena&15],coloresPíxel[datosCadena>>4]);
    }}
    tablaNombre(entradaElementoTerminal->coordenadaCoordenadaHorizontal+12,entradaElementoTerminal->coordenadaCoordenadaVertical+entradaElementoTerminal->valorAltura-18,entradaElementoTerminal->desplazarVista?"PgDn: recent output":entradaElementoTerminal->valorAnchura>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);valorPuntoInserción(1);
}
static void marcoEjecución(int valorIdentificador){
    entradaElementoTerminal=&listaVentanas[valorIdentificador];
    int posiciónHorizontal=entradaElementoTerminal->coordenadaCoordenadaHorizontal,posiciónVertical=entradaElementoTerminal->coordenadaCoordenadaVertical,extensiónRangoAnchura=entradaElementoTerminal->valorAnchura,longitud=entradaElementoTerminal->valorAltura;
    if(!límitesDibujoPlaca(&posiciónHorizontal,&posiciónVertical,&extensiónRangoAnchura,&longitud))return;
    regiónRectangular(entradaElementoTerminal->coordenadaCoordenadaHorizontal,entradaElementoTerminal->coordenadaCoordenadaVertical,entradaElementoTerminal->valorAnchura,entradaElementoTerminal->valorAltura,0x403127);
    unsigned colorPíxel=valorIdentificador==foco?0x905020:0x604438;regiónRectangular(entradaElementoTerminal->coordenadaCoordenadaHorizontal,entradaElementoTerminal->coordenadaCoordenadaVertical,entradaElementoTerminal->valorAnchura,30,colorPíxel);
    tablaNombre(entradaElementoTerminal->coordenadaCoordenadaHorizontal+12,entradaElementoTerminal->coordenadaCoordenadaVertical+7,"JKOROS Terminal",0xffffff,colorPíxel);
    char valorNumérico[2]={(char)('1'+valorIdentificador),0};tablaNombre(entradaElementoTerminal->coordenadaCoordenadaHorizontal+148,entradaElementoTerminal->coordenadaCoordenadaVertical+7,valorNumérico,0xffffff,colorPíxel);
    tablaNombre(entradaElementoTerminal->coordenadaCoordenadaHorizontal+240,entradaElementoTerminal->coordenadaCoordenadaVertical+7,entradaElementoTerminal->valorAnchura>=500?(entradaHangul?"[ES] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(entradaHangul?"[ES]":"[EN]"),0xffffff,colorPíxel);
    regiónRectangular(entradaElementoTerminal->coordenadaCoordenadaHorizontal+entradaElementoTerminal->valorAnchura-32,entradaElementoTerminal->coordenadaCoordenadaVertical+4,26,22,0x5555b8);tablaNombre(entradaElementoTerminal->coordenadaCoordenadaHorizontal+entradaElementoTerminal->valorAnchura-24,entradaElementoTerminal->coordenadaCoordenadaVertical+7,"X",0xffffff,0x5555b8);
    valorContenidoValor();
}
static void dibujarEscena(void){
    if(!vistaEscritorio)return;regiónRectangular(0,0,anchuraPantallaPlaca(),alturaPantallaPlaca(),0x302018);regiónRectangular(0,0,anchuraPantallaPlaca(),32,0x403127);
    regiónRectangular(6,4,136,24,0x905020);tablaNombre(14,8,"+ New terminal",0xffffff,0x905020);
    for(int índiceOrdinal=0;índiceOrdinal<4;índiceOrdinal++)if(listaVentanas[índiceOrdinal].esEnVida){unsigned códigoCarácter=foco==índiceOrdinal?0x905020:0x604438;regiónRectangular(154+índiceOrdinal*112,4,106,24,códigoCarácter);tablaNombre(160+índiceOrdinal*112,8,"Terminal",0xffffff,códigoCarácter);char datosCadena[2]={(char)('1'+índiceOrdinal),0};tablaNombre(232+índiceOrdinal*112,8,datosCadena,0xffffff,códigoCarácter);}
    if(!númeroElementosEntradaElemento)tablaNombre(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int índiceOrdinal=0;índiceOrdinal<númeroElementosEntradaElemento;índiceOrdinal++)marcoEjecución(valorOrden[índiceOrdinal]);pantallaRedibujar(foco);entradaElementoTerminal=&listaVentanas[salida];
}
static void regiónPintar(int posiciónHorizontal,int posiciónVertical,int extensiónRangoAnchura,int longitud){
    if(!vistaEscritorio||!límitesDibujoPlaca(&posiciónHorizontal,&posiciónVertical,&extensiónRangoAnchura,&longitud))return;
    for(int línea=posiciónVertical;línea<posiciónVertical+longitud;línea+=32){
        int alturaBanda=posiciónVertical+longitud-línea;if(alturaBanda>32)alturaBanda=32;
        if(dibujoIniciarPlaca(posiciónHorizontal,línea,extensiónRangoAnchura,alturaBanda)){dibujarEscena();dibujoTerminarPlaca();}
    }
}
static void redibujar(void){regiónPintar(0,0,anchuraPantallaPlaca(),alturaPantallaPlaca());}
/* 서로 겹치지 않는 새 ventana 영역과 elementoListaElementoPrevio 자리의 네 띠를 복구한다. */
static void límitesVentanaPintar(int posiciónHorizontal,int posiciónVertical,int extensiónRangoAnchura,int longitud,Terminal *ventana){
    int ladoIzquierdo=posiciónHorizontal>(int)ventana->coordenadaCoordenadaHorizontal?posiciónHorizontal:(int)ventana->coordenadaCoordenadaHorizontal;
    int ladoSuperior=posiciónVertical>(int)ventana->coordenadaCoordenadaVertical?posiciónVertical:(int)ventana->coordenadaCoordenadaVertical;
    int derecho=posiciónHorizontal+extensiónRangoAnchura<(int)(ventana->coordenadaCoordenadaHorizontal+ventana->valorAnchura)?posiciónHorizontal+extensiónRangoAnchura:(int)(ventana->coordenadaCoordenadaHorizontal+ventana->valorAnchura);
    int ladoInferior=posiciónVertical+longitud<(int)(ventana->coordenadaCoordenadaVertical+ventana->valorAltura)?posiciónVertical+longitud:(int)(ventana->coordenadaCoordenadaVertical+ventana->valorAltura);
    regiónPintar(ventana->coordenadaCoordenadaHorizontal,ventana->coordenadaCoordenadaVertical,ventana->valorAnchura,ventana->valorAltura);
    if(ladoIzquierdo>=derecho||ladoSuperior>=ladoInferior){regiónPintar(posiciónHorizontal,posiciónVertical,extensiónRangoAnchura,longitud);return;}
    regiónPintar(posiciónHorizontal,posiciónVertical,extensiónRangoAnchura,ladoSuperior-posiciónVertical);
    regiónPintar(posiciónHorizontal,ladoInferior,extensiónRangoAnchura,posiciónVertical+longitud-ladoInferior);
    regiónPintar(posiciónHorizontal,ladoSuperior,ladoIzquierdo-posiciónHorizontal,ladoInferior-ladoSuperior);
    regiónPintar(derecho,ladoSuperior,posiciónHorizontal+extensiónRangoAnchura-derecho,ladoInferior-ladoSuperior);
}
static void focoSeñal(void){esPendiente=(esPendiente&~15u)|(unsigned)(foco+1)|0x10000;}
void modoEntradaTerminal(unsigned coreano){
    entradaHangul=coreano!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(foco>=0){
        Terminal *entradaElementoVentana=&listaVentanas[foco];
        tablaNombre(entradaElementoVentana->coordenadaCoordenadaHorizontal+240,entradaElementoVentana->coordenadaCoordenadaVertical+7,entradaElementoVentana->valorAnchura>=500?(entradaHangul?"[ES] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(entradaHangul?"[ES]":"[EN]"),0xffffff,0x905020);
    }
}
static void ladoDelanteroHaciaTraer(int valorIdentificador){if(valorIdentificador<0||valorIdentificador>=4||!listaVentanas[valorIdentificador].esEnVida)return;int posiciónActual=0;while(posiciónActual<númeroElementosEntradaElemento&&valorOrden[posiciónActual]!=valorIdentificador)posiciónActual++;for(;posiciónActual+1<númeroElementosEntradaElemento;posiciónActual++)valorOrden[posiciónActual]=valorOrden[posiciónActual+1];valorOrden[númeroElementosEntradaElemento-1]=valorIdentificador;foco=valorIdentificador;focoSeñal();redibujar();}
static void vacío(unsigned posiciónFila){for(unsigned códigoCarácter=0;códigoCarácter<columnasMáximo;códigoCarácter++){entradaElementoTerminal->celdasCarácter[posiciónFila%númeroElementosLíneaHistorial][códigoCarácter]=0;entradaElementoTerminal->listaFormas[posiciónFila%númeroElementosLíneaHistorial][códigoCarácter]=entradaElementoTerminal->colorPrimerPlano|(entradaElementoTerminal->colorFondo<<4);}}
static void borrarContenidoContenido(void){entradaElementoTerminal->posiciónFila=entradaElementoTerminal->posiciónColumna=entradaElementoTerminal->entradaElementoExtremoSuperior=entradaElementoTerminal->desplazarVista=0;for(unsigned valorDevuelto=0;valorDevuelto<númeroElementosLíneaHistorial;valorDevuelto++)vacío(valorDevuelto);if(esMostrado())valorContenidoValor();}
static int crearEntradaElemento(void){
    if(!búferImagenPlaca())return -19;int valorIdentificador=0;while(valorIdentificador<4&&listaVentanas[valorIdentificador].esEnVida)valorIdentificador++;if(valorIdentificador==4)return -28;
    vistaEscritorio=1;entradaElementoTerminal=&listaVentanas[valorIdentificador];memset(entradaElementoTerminal,0,sizeof(*entradaElementoTerminal));entradaElementoTerminal->esEnVida=1;entradaElementoTerminal->valorAnchura=568;entradaElementoTerminal->valorAltura=360;entradaElementoTerminal->columnas=68;entradaElementoTerminal->númeroElementosFila=19;entradaElementoTerminal->coordenadaCoordenadaHorizontal=12+valorIdentificador*16;entradaElementoTerminal->coordenadaCoordenadaVertical=48+valorIdentificador*18;entradaElementoTerminal->colorPrimerPlano=7;entradaElementoTerminal->visiblePuntoInserción=1;
    for(unsigned valorDevuelto=0;valorDevuelto<númeroElementosLíneaHistorial;valorDevuelto++)vacío(valorDevuelto);valorOrden[númeroElementosEntradaElemento++]=valorIdentificador;foco=valorIdentificador;esPendiente|=1u<<(4+valorIdentificador);focoSeñal();redibujar();return valorIdentificador+1;
}
static void cerrarVentana(int valorIdentificador){
    if(valorIdentificador<0||valorIdentificador>=4||!listaVentanas[valorIdentificador].esEnVida)return;listaVentanas[valorIdentificador].esEnVida=0;esPendiente|=1u<<(8+valorIdentificador);
    int posiciónActual=0;while(posiciónActual<númeroElementosEntradaElemento&&valorOrden[posiciónActual]!=valorIdentificador)posiciónActual++;for(;posiciónActual+1<númeroElementosEntradaElemento;posiciónActual++)valorOrden[posiciónActual]=valorOrden[posiciónActual+1];númeroElementosEntradaElemento--;
    if(foco==valorIdentificador)foco=númeroElementosEntradaElemento?valorOrden[númeroElementosEntradaElemento-1]:-1;focoSeñal();redibujar();
}
static void nuevaLínea(void){entradaElementoTerminal->posiciónColumna=0;entradaElementoTerminal->posiciónFila++;if(entradaElementoTerminal->posiciónFila>=entradaElementoTerminal->entradaElementoExtremoSuperior+entradaElementoTerminal->númeroElementosFila){entradaElementoTerminal->entradaElementoExtremoSuperior++;vacío(entradaElementoTerminal->posiciónFila);if(esMostrado())valorContenidoValor();}}
static void puntoCódigo(unsigned códigoCarácter){
    if(códigoCarácter==13){entradaElementoTerminal->posiciónColumna=0;return;}if(códigoCarácter==10){nuevaLínea();return;}if(códigoCarácter==8){if(entradaElementoTerminal->posiciónColumna)entradaElementoTerminal->posiciónColumna--;return;}
    if(códigoCarácter==9){unsigned númeroElementosElementoLista=8-entradaElementoTerminal->posiciónColumna%8;while(númeroElementosElementoLista--)puntoCódigo(' ');return;}if(códigoCarácter<32||códigoCarácter==127)return;
    unsigned valorAnchuraSolicitado=carácterAncho(códigoCarácter);if(entradaElementoTerminal->posiciónColumna+valorAnchuraSolicitado>entradaElementoTerminal->columnas)nuevaLínea();
    if(entradaElementoTerminal->celdasCarácter[entradaElementoTerminal->posiciónFila%númeroElementosLíneaHistorial][entradaElementoTerminal->posiciónColumna]==0xffffffffu&&entradaElementoTerminal->posiciónColumna){entradaElementoTerminal->celdasCarácter[entradaElementoTerminal->posiciónFila%númeroElementosLíneaHistorial][entradaElementoTerminal->posiciónColumna-1]=' ';pantallaPintar(entradaElementoTerminal->posiciónFila,entradaElementoTerminal->posiciónColumna-1);}
    if(carácterAncho(entradaElementoTerminal->celdasCarácter[entradaElementoTerminal->posiciónFila%númeroElementosLíneaHistorial][entradaElementoTerminal->posiciónColumna])==2&&entradaElementoTerminal->posiciónColumna+1<entradaElementoTerminal->columnas){entradaElementoTerminal->celdasCarácter[entradaElementoTerminal->posiciónFila%númeroElementosLíneaHistorial][entradaElementoTerminal->posiciónColumna+1]=' ';pantallaPintar(entradaElementoTerminal->posiciónFila,entradaElementoTerminal->posiciónColumna+1);}
    entradaElementoTerminal->celdasCarácter[entradaElementoTerminal->posiciónFila%númeroElementosLíneaHistorial][entradaElementoTerminal->posiciónColumna]=códigoCarácter;entradaElementoTerminal->listaFormas[entradaElementoTerminal->posiciónFila%númeroElementosLíneaHistorial][entradaElementoTerminal->posiciónColumna]=entradaElementoTerminal->colorPrimerPlano|(entradaElementoTerminal->colorFondo<<4);
    if(valorAnchuraSolicitado==2)entradaElementoTerminal->celdasCarácter[entradaElementoTerminal->posiciónFila%númeroElementosLíneaHistorial][entradaElementoTerminal->posiciónColumna+1]=0xffffffffu;
    pantallaPintar(entradaElementoTerminal->posiciónFila,entradaElementoTerminal->posiciónColumna);entradaElementoTerminal->posiciónColumna+=valorAnchuraSolicitado;
}
static void secuenciaControlManejador(unsigned códigoCarácter){
    unsigned númeroElementosElementoLista=entradaElementoTerminal->valorParámetro[0]?entradaElementoTerminal->valorParámetro[0]:1;
    if(códigoCarácter=='m')for(unsigned índiceOrdinal=0;índiceOrdinal<=entradaElementoTerminal->índiceParámetro;índiceOrdinal++){unsigned posiciónDatos=entradaElementoTerminal->valorParámetro[índiceOrdinal];if(!posiciónDatos){entradaElementoTerminal->colorPrimerPlano=7;entradaElementoTerminal->colorFondo=0;}if(posiciónDatos==1&&entradaElementoTerminal->colorPrimerPlano<8)entradaElementoTerminal->colorPrimerPlano+=8;if(posiciónDatos==7){unsigned retenerValor=entradaElementoTerminal->colorPrimerPlano;entradaElementoTerminal->colorPrimerPlano=entradaElementoTerminal->colorFondo;entradaElementoTerminal->colorFondo=retenerValor;}if(posiciónDatos>=30&&posiciónDatos<=37)entradaElementoTerminal->colorPrimerPlano=posiciónDatos-30;if(posiciónDatos>=90&&posiciónDatos<=97)entradaElementoTerminal->colorPrimerPlano=posiciónDatos-90+8;if(posiciónDatos>=40&&posiciónDatos<=47)entradaElementoTerminal->colorFondo=posiciónDatos-40;if(posiciónDatos>=100&&posiciónDatos<=107)entradaElementoTerminal->colorFondo=posiciónDatos-100+8;if(posiciónDatos==39)entradaElementoTerminal->colorPrimerPlano=7;if(posiciónDatos==49)entradaElementoTerminal->colorFondo=0;}
    if(códigoCarácter=='J'&&(entradaElementoTerminal->valorParámetro[0]==2||entradaElementoTerminal->valorParámetro[0]==3))borrarContenidoContenido();
    if(códigoCarácter=='K'){unsigned posiciónPartida=entradaElementoTerminal->valorParámetro[0]==2?0:entradaElementoTerminal->posiciónColumna,posiciónLlegada=entradaElementoTerminal->valorParámetro[0]==1?entradaElementoTerminal->posiciónColumna+1:entradaElementoTerminal->columnas;if(entradaElementoTerminal->valorParámetro[0]==1)posiciónPartida=0;for(unsigned índiceOrdinal=posiciónPartida;índiceOrdinal<posiciónLlegada&&índiceOrdinal<entradaElementoTerminal->columnas;índiceOrdinal++){
        unsigned valorFila=entradaElementoTerminal->posiciónFila%númeroElementosLíneaHistorial,valorCarácter=entradaElementoTerminal->celdasCarácter[valorFila][índiceOrdinal],valorForma=entradaElementoTerminal->colorPrimerPlano|(entradaElementoTerminal->colorFondo<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 valorFuenteTipográfica 화소를 되풀이해 칠하지 않는다. */
        int esModificado=(valorCarácter!=0&&valorCarácter!=' ')||entradaElementoTerminal->listaFormas[valorFila][índiceOrdinal]!=valorForma;
        entradaElementoTerminal->celdasCarácter[valorFila][índiceOrdinal]=' ';entradaElementoTerminal->listaFormas[valorFila][índiceOrdinal]=valorForma;
        if(esModificado)pantallaPintar(entradaElementoTerminal->posiciónFila,índiceOrdinal);
    }}
    if(códigoCarácter=='D')entradaElementoTerminal->posiciónColumna=númeroElementosElementoLista>entradaElementoTerminal->posiciónColumna?0:entradaElementoTerminal->posiciónColumna-númeroElementosElementoLista;if(códigoCarácter=='C')entradaElementoTerminal->posiciónColumna=entradaElementoTerminal->posiciónColumna+númeroElementosElementoLista>=entradaElementoTerminal->columnas?entradaElementoTerminal->columnas-1:entradaElementoTerminal->posiciónColumna+númeroElementosElementoLista;
    if(códigoCarácter=='G')entradaElementoTerminal->posiciónColumna=númeroElementosElementoLista>entradaElementoTerminal->columnas?entradaElementoTerminal->columnas-1:númeroElementosElementoLista-1;if(códigoCarácter=='A')entradaElementoTerminal->posiciónFila=númeroElementosElementoLista>entradaElementoTerminal->posiciónFila-entradaElementoTerminal->entradaElementoExtremoSuperior?entradaElementoTerminal->entradaElementoExtremoSuperior:entradaElementoTerminal->posiciónFila-númeroElementosElementoLista;
    if(códigoCarácter=='B')entradaElementoTerminal->posiciónFila=entradaElementoTerminal->posiciónFila+númeroElementosElementoLista>=entradaElementoTerminal->entradaElementoExtremoSuperior+entradaElementoTerminal->númeroElementosFila?entradaElementoTerminal->entradaElementoExtremoSuperior+entradaElementoTerminal->númeroElementosFila-1:entradaElementoTerminal->posiciónFila+númeroElementosElementoLista;
    if(códigoCarácter=='H'||códigoCarácter=='f'){entradaElementoTerminal->posiciónFila=entradaElementoTerminal->entradaElementoExtremoSuperior+(númeroElementosElementoLista>entradaElementoTerminal->númeroElementosFila?entradaElementoTerminal->númeroElementosFila:númeroElementosElementoLista)-1;unsigned coordenadaCoordenadaHorizontal=entradaElementoTerminal->valorParámetro[1]?entradaElementoTerminal->valorParámetro[1]:1;entradaElementoTerminal->posiciónColumna=(coordenadaCoordenadaHorizontal>entradaElementoTerminal->columnas?entradaElementoTerminal->columnas:coordenadaCoordenadaHorizontal)-1;}
    if(códigoCarácter=='s'){entradaElementoTerminal->filaGuardado=entradaElementoTerminal->posiciónFila;entradaElementoTerminal->númeroColumnaGuardado=entradaElementoTerminal->posiciónColumna;}if(códigoCarácter=='u'){entradaElementoTerminal->posiciónFila=entradaElementoTerminal->filaGuardado;entradaElementoTerminal->posiciónColumna=entradaElementoTerminal->númeroColumnaGuardado<entradaElementoTerminal->columnas?entradaElementoTerminal->númeroColumnaGuardado:entradaElementoTerminal->columnas-1;}
    if((códigoCarácter=='h'||códigoCarácter=='l')&&entradaElementoTerminal->valorParámetro[0]==25)entradaElementoTerminal->visiblePuntoInserción=códigoCarácter=='h';
}
void byteTerminal(unsigned valorSegundo){
    entradaElementoTerminal=&listaVentanas[salida];if(!entradaElementoTerminal->esEnVida)return;valorPuntoInserción(0);if(entradaElementoTerminal->desplazarVista){entradaElementoTerminal->desplazarVista=0;if(esMostrado())valorContenidoValor();}
    if(entradaElementoTerminal->escapar==1){entradaElementoTerminal->escapar=valorSegundo=='['?2:0;entradaElementoTerminal->índiceParámetro=0;for(unsigned índiceOrdinal=0;índiceOrdinal<4;índiceOrdinal++)entradaElementoTerminal->valorParámetro[índiceOrdinal]=0;}
    else if(entradaElementoTerminal->escapar==2){if(valorSegundo=='?'){}else if(valorSegundo>='0'&&valorSegundo<='9'){if(entradaElementoTerminal->valorParámetro[entradaElementoTerminal->índiceParámetro]<10000)entradaElementoTerminal->valorParámetro[entradaElementoTerminal->índiceParámetro]=entradaElementoTerminal->valorParámetro[entradaElementoTerminal->índiceParámetro]*10+valorSegundo-'0';}else if(valorSegundo==';'&&entradaElementoTerminal->índiceParámetro<3)entradaElementoTerminal->índiceParámetro++;else{secuenciaControlManejador(valorSegundo);entradaElementoTerminal->escapar=0;}}
    else if(valorSegundo==27){entradaElementoTerminal->valorLargoSinSigno=0;entradaElementoTerminal->escapar=1;}else{
        if(entradaElementoTerminal->valorLargoSinSigno&&(valorSegundo&0xc0)!=0x80){entradaElementoTerminal->valorLargoSinSigno=0;puntoCódigo(0xfffd);}
        if(entradaElementoTerminal->valorLargoSinSigno){entradaElementoTerminal->resultadoSinSigno=entradaElementoTerminal->resultadoSinSigno*64+(valorSegundo&63);if(--entradaElementoTerminal->valorLargoSinSigno==0)puntoCódigo(entradaElementoTerminal->resultadoSinSigno<entradaElementoTerminal->valorFormatoPequeño||entradaElementoTerminal->resultadoSinSigno>0x10ffff||(entradaElementoTerminal->resultadoSinSigno>=0xd800&&entradaElementoTerminal->resultadoSinSigno<=0xdfff)?0xfffd:entradaElementoTerminal->resultadoSinSigno);}
        else if(valorSegundo<128)puntoCódigo(valorSegundo);else if(valorSegundo>=0xc2&&valorSegundo<=0xf4){entradaElementoTerminal->valorLargoSinSigno=valorSegundo<0xe0?1:valorSegundo<0xf0?2:3;entradaElementoTerminal->resultadoSinSigno=valorSegundo&((1u<<(6-entradaElementoTerminal->valorLargoSinSigno))-1);entradaElementoTerminal->valorFormatoPequeño=entradaElementoTerminal->valorLargoSinSigno==1?128:entradaElementoTerminal->valorLargoSinSigno==2?2048:65536;}else puntoCódigo(0xfffd);
    }valorPuntoInserción(1);
}
int pendienteTerminal(void){return esPendiente!=0;}
/* valorEsquina número: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int arrastrarRedimensionar=-1,esquinaAgarrado,coordenadaHorizontalAgarrado,coordenadaVerticalAgarrado,posiciónHorizontalInicialValor,posiciónVerticalInicialValor,valorAnchuraInicialValor,valorAlturaInicialValor;
static int ventanaApuntado(int posiciónHorizontal,int posiciónVertical) {
    for(int valorSecuencia=númeroElementosEntradaElemento-1;valorSecuencia>=0;valorSecuencia--){
        int valorIdentificador=valorOrden[valorSecuencia];Terminal *ventana=&listaVentanas[valorIdentificador];
        if(posiciónHorizontal>=(int)ventana->coordenadaCoordenadaHorizontal&&posiciónVertical>=(int)ventana->coordenadaCoordenadaVertical&&
           posiciónHorizontal<(int)(ventana->coordenadaCoordenadaHorizontal+ventana->valorAnchura)&&posiciónVertical<(int)(ventana->coordenadaCoordenadaVertical+ventana->valorAltura))return valorIdentificador;
    }return -1;
}
static int encontrarEsquina(int valorIdentificador,int posiciónHorizontal,int posiciónVertical) {
    if(valorIdentificador<0)return 0;Terminal *ventana=&listaVentanas[valorIdentificador];
    int ladoIzquierdo=posiciónHorizontal<(int)ventana->coordenadaCoordenadaHorizontal+8,derecho=posiciónHorizontal>=(int)(ventana->coordenadaCoordenadaHorizontal+ventana->valorAnchura)-8;
    int ladoSuperior=posiciónVertical<(int)ventana->coordenadaCoordenadaVertical+8,ladoInferior=posiciónVertical>=(int)(ventana->coordenadaCoordenadaVertical+ventana->valorAltura)-8;
    return (ladoIzquierdo||derecho)&&(ladoSuperior||ladoInferior)?1+derecho+ladoInferior*2:0;
}
static int valorSeparador(int valor,int valorMínimo,int valorMáximo){return valor<valorMínimo?valorMínimo:valor>valorMáximo?valorMáximo:valor;}
static void redimensionarMover(int posiciónHorizontal,int posiciónVertical) {
    Terminal *ventana=&listaVentanas[arrastrarRedimensionar];int ladoIzquierdo=posiciónHorizontalInicialValor,ladoSuperior=posiciónVerticalInicialValor,derecho=posiciónHorizontalInicialValor+valorAnchuraInicialValor,ladoInferior=posiciónVerticalInicialValor+valorAlturaInicialValor;
    if(esquinaAgarrado==1||esquinaAgarrado==3)ladoIzquierdo=valorSeparador(posiciónHorizontalInicialValor+posiciónHorizontal-coordenadaHorizontalAgarrado,0,derecho-360);
    else derecho=valorSeparador(posiciónHorizontalInicialValor+valorAnchuraInicialValor+posiciónHorizontal-coordenadaHorizontalAgarrado,ladoIzquierdo+360,anchuraPantallaPlaca());
    if(esquinaAgarrado<=2)ladoSuperior=valorSeparador(posiciónVerticalInicialValor+posiciónVertical-coordenadaVerticalAgarrado,34,ladoInferior-216);
    else ladoInferior=valorSeparador(posiciónVerticalInicialValor+valorAlturaInicialValor+posiciónVertical-coordenadaVerticalAgarrado,ladoSuperior+216,alturaPantallaPlaca());
    unsigned columnas=(derecho-ladoIzquierdo-24)/8,númeroElementosFila=(ladoInferior-ladoSuperior-56)/16;
    if(ventana->columnas!=columnas||ventana->númeroElementosFila!=númeroElementosFila){
        ventana->redimensionadoEra=1;ventana->columnas=columnas;ventana->númeroElementosFila=númeroElementosFila;
        if(ventana->posiciónColumna>=columnas)ventana->posiciónColumna=columnas-1;
        if(ventana->posiciónFila>=ventana->entradaElementoExtremoSuperior+númeroElementosFila)ventana->entradaElementoExtremoSuperior=ventana->posiciónFila-númeroElementosFila+1;
        unsigned límiteCapacidad=ventana->entradaElementoExtremoSuperior;if(límiteCapacidad>númeroElementosLíneaHistorial-númeroElementosFila)límiteCapacidad=númeroElementosLíneaHistorial-númeroElementosFila;
        if(ventana->desplazarVista>límiteCapacidad)ventana->desplazarVista=límiteCapacidad;
    }
    int posiciónHorizontalAntiguo=ventana->coordenadaCoordenadaHorizontal,posiciónVerticalAntiguo=ventana->coordenadaCoordenadaVertical,anchuraAntiguo=ventana->valorAnchura,longitudAntiguo=ventana->valorAltura;
    if(posiciónHorizontalAntiguo==ladoIzquierdo&&posiciónVerticalAntiguo==ladoSuperior&&anchuraAntiguo==derecho-ladoIzquierdo&&longitudAntiguo==ladoInferior-ladoSuperior)return;
    ventana->coordenadaCoordenadaHorizontal=ladoIzquierdo;ventana->coordenadaCoordenadaVertical=ladoSuperior;ventana->valorAnchura=derecho-ladoIzquierdo;ventana->valorAltura=ladoInferior-ladoSuperior;
    límitesVentanaPintar(posiciónHorizontalAntiguo,posiciónVerticalAntiguo,anchuraAntiguo,longitudAntiguo,ventana);
}
void punteroTerminal(unsigned elementoListaSiguiente,int coordenadaCoordenadaHorizontal,int coordenadaCoordenadaVertical){
    unsigned esPulsado=elementoListaSiguiente&~botones;botones=elementoListaSiguiente;
    if(!vistaEscritorio){valorArrastrar=-1;arrastrarRedimensionar=-1;punteroPlaca(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,1);return;}
    if(!(elementoListaSiguiente&1)){valorArrastrar=-1;arrastrarRedimensionar=-1;}
    if(arrastrarRedimensionar>=0&&!listaVentanas[arrastrarRedimensionar].esEnVida)arrastrarRedimensionar=-1;
    if(valorArrastrar>=0&&!listaVentanas[valorArrastrar].esEnVida)valorArrastrar=-1;
    if(arrastrarRedimensionar>=0){
        redimensionarMover(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical);punteroPlaca(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,esquinaAgarrado==1||esquinaAgarrado==4?2:3);return;
    }
    punteroPlaca(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,1);
    if(valorArrastrar>=0){
        Terminal *ventana=&listaVentanas[valorArrastrar];
        int posiciónHorizontalAntiguo=ventana->coordenadaCoordenadaHorizontal,posiciónVerticalAntiguo=ventana->coordenadaCoordenadaVertical;
        ventana->coordenadaCoordenadaHorizontal=valorSeparador(coordenadaCoordenadaHorizontal-coordenadaHorizontalArrastrar,0,anchuraPantallaPlaca()-ventana->valorAnchura);
        ventana->coordenadaCoordenadaVertical=valorSeparador(coordenadaCoordenadaVertical-coordenadaVerticalArrastrar,34,alturaPantallaPlaca()-ventana->valorAltura);
        if(posiciónHorizontalAntiguo!=(int)ventana->coordenadaCoordenadaHorizontal||posiciónVerticalAntiguo!=(int)ventana->coordenadaCoordenadaVertical)límitesVentanaPintar(posiciónHorizontalAntiguo,posiciónVerticalAntiguo,ventana->valorAnchura,ventana->valorAltura,ventana);
        return;
    }
    extern int superponerPantalla(int,int,int);
    if(superponerPantalla(foco,coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical)){punteroPantalla(foco,esPulsado,coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical);return;}
    int valorIdentificador=ventanaApuntado(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical),valorEsquina=encontrarEsquina(valorIdentificador,coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical);
    if(valorEsquina)punteroPlaca(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,valorEsquina==1||valorEsquina==4?2:3);
    if(esPulsado&1){
        if(valorEsquina){
            Terminal *ventana=&listaVentanas[valorIdentificador];arrastrarRedimensionar=valorIdentificador;esquinaAgarrado=valorEsquina;coordenadaHorizontalAgarrado=coordenadaCoordenadaHorizontal;coordenadaVerticalAgarrado=coordenadaCoordenadaVertical;
            posiciónHorizontalInicialValor=ventana->coordenadaCoordenadaHorizontal;posiciónVerticalInicialValor=ventana->coordenadaCoordenadaVertical;valorAnchuraInicialValor=ventana->valorAnchura;valorAlturaInicialValor=ventana->valorAltura;
            if(valorIdentificador!=foco)ladoDelanteroHaciaTraer(valorIdentificador);return;
        }
        if(coordenadaCoordenadaVertical<32&&coordenadaCoordenadaHorizontal>=6&&coordenadaCoordenadaHorizontal<142){crearEntradaElemento();return;}
        if(coordenadaCoordenadaVertical<32&&coordenadaCoordenadaHorizontal>=154&&coordenadaCoordenadaHorizontal<602){ladoDelanteroHaciaTraer((coordenadaCoordenadaHorizontal-154)/112);return;}
        if(valorIdentificador>=0){
            Terminal *ventana=&listaVentanas[valorIdentificador];
            if(coordenadaCoordenadaVertical<(int)ventana->coordenadaCoordenadaVertical+30&&coordenadaCoordenadaHorizontal>=(int)(ventana->coordenadaCoordenadaHorizontal+ventana->valorAnchura)-32){cerrarVentana(valorIdentificador);return;}
            if(valorIdentificador!=foco)ladoDelanteroHaciaTraer(valorIdentificador);
            if(coordenadaCoordenadaVertical<(int)ventana->coordenadaCoordenadaVertical+30){valorArrastrar=valorIdentificador;coordenadaHorizontalArrastrar=coordenadaCoordenadaHorizontal-ventana->coordenadaCoordenadaHorizontal;coordenadaVerticalArrastrar=coordenadaCoordenadaVertical-ventana->coordenadaCoordenadaVertical;}return;
        }
    }
    if(foco>=0&&(esPulsado&(8|16))){entradaElementoTerminal=&listaVentanas[foco];if(esPulsado&8){unsigned límiteCapacidad=entradaElementoTerminal->entradaElementoExtremoSuperior;if(límiteCapacidad>númeroElementosLíneaHistorial-entradaElementoTerminal->númeroElementosFila)límiteCapacidad=númeroElementosLíneaHistorial-entradaElementoTerminal->númeroElementosFila;entradaElementoTerminal->desplazarVista=entradaElementoTerminal->desplazarVista+9>límiteCapacidad?límiteCapacidad:entradaElementoTerminal->desplazarVista+9;}else entradaElementoTerminal->desplazarVista=entradaElementoTerminal->desplazarVista<9?0:entradaElementoTerminal->desplazarVista-9;redibujar();}
}
void atajoTecladoTerminal(unsigned valorPulsado){if(valorPulsado==1)crearEntradaElemento();if(valorPulsado==2&&númeroElementosEntradaElemento)ladoDelanteroHaciaTraer(valorOrden[0]);if(valorPulsado==3)cerrarVentana(foco);}
palabraMáquina terminalPlaca(palabraMáquina acción){
    if(acción==300){if(!listaVentanas[salida].esEnVida)return crearEntradaElemento();vistaEscritorio=1;redibujar();return 0;}
    if(acción==0){cerrarVentana(foco);return 0;}if(acción==1)return (uint32_t)crearEntradaElemento();if(acción==2)return foco>=0;
    if(acción==9){vistaEscritorio=0;return 0;}if(acción==7)return númeroElementosEntradaElemento;if(acción==10)return foco+1;if(acción==11)return salida;
    if(acción==13){Terminal *ventana=&listaVentanas[salida];return ventana->esEnVida?(ventana->númeroElementosFila<<16)|ventana->columnas:(19<<16)|68;}
    if(acción==14){unsigned valor=listaVentanas[salida].redimensionadoEra;listaVentanas[salida].redimensionadoEra=0;return valor;}
    if(acción==12){unsigned valor=esPendiente;esPendiente=0;return valor;}
    if(acción>=20&&acción<24)return listaVentanas[acción-20].esEnVida;
    if(acción>=100&&acción<104){salida=acción-100;entradaElementoTerminal=&listaVentanas[salida];return 0;}
    if(acción>=200&&acción<204){ladoDelanteroHaciaTraer(acción-200);return 0;}
    if(acción==3){redibujar();return 0;}entradaElementoTerminal=&listaVentanas[salida];if(!entradaElementoTerminal->esEnVida)return 0;
    if(acción==4)borrarContenidoContenido();if(acción==5||acción==6){unsigned elementoListaElementoPrevio=botones;punteroTerminal(acción==5?8:16,0,0);botones=elementoListaElementoPrevio;}return 1;
}
