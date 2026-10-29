#include "../denominación/nombresEnlazarMáquina.h"
#include "invocar.h"
extern int main(int,char **);
static char arregloArgumento[8][256];
int iniciarUsuario(int sinUsar){
    (void)sinUsar;char *listaArgumento[9];int númeroElementosArgumentos=invocarUsuario(15,UINTPTR_MAX,0,0,0,0,0);
    if(númeroElementosArgumentos<0||númeroElementosArgumentos>8)return 126;
    for(int índiceOrdinal=0;índiceOrdinal<númeroElementosArgumentos;índiceOrdinal++){if(invocarUsuario(15,índiceOrdinal,(uintptr_t)arregloArgumento[índiceOrdinal],256,0,0,0)<0)return 126;listaArgumento[índiceOrdinal]=arregloArgumento[índiceOrdinal];}listaArgumento[númeroElementosArgumentos]=0;
    return main(númeroElementosArgumentos,listaArgumento);
}
void *memset(void*posiciónDatos,int códigoCarácter,size_t númeroElementosElementoLista){unsigned char*datosDestino=posiciónDatos;while(númeroElementosElementoLista--)*datosDestino++=códigoCarácter;return posiciónDatos;}
void *memcpy(void*datosDestino,const void*datosCadena,size_t númeroElementosElementoLista){unsigned char*valorPrimero=datosDestino;const unsigned char*valorSegundo=datosCadena;while(númeroElementosElementoLista--)*valorPrimero++=*valorSegundo++;return datosDestino;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned coordenadaCoordenadaHorizontal,unsigned coordenadaCoordenadaVertical,unsigned valorAnchura,unsigned valorAltura,unsigned colorPíxel){return rectánguloPantalla(coordenadaCoordenadaHorizontal,coordenadaCoordenadaVertical,valorAnchura,valorAltura,colorPíxel);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return invocarUsuario(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return esperarTeclaPantallaPara();}
int dibujarRectángulo(unsigned posiciónHorizontal,unsigned posiciónVertical,unsigned valorAnchura,unsigned valorAltura,unsigned colorPíxel){return pk_rectangle(posiciónHorizontal,posiciónVertical,valorAnchura,valorAltura,colorPíxel);}
unsigned milisegundos(void){return pk_ticks_ms();}
int esperarDibujoPara(void){return pk_graphics_wait();}
int anchuraPantalla(void){return leerAnchuraPantalla();}
int alturaPantalla(void){return leerAlturaPantalla();}
