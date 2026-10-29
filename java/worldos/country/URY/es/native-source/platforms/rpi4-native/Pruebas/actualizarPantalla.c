#include "../denominación/nombresEnlazarMáquina.h"
#include "../máquina/informaciónPantalla.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void paradaFatalNúcleo(const char *descripción){fputs(descripción,stderr);abort();}
extern uintptr_t terminalPlaca(uintptr_t),píxelPlaca(uintptr_t,uintptr_t,uintptr_t);
extern void punteroTerminal(unsigned,int,int),byteTerminal(unsigned);
extern int invocarPantalla(int,unsigned,int,int,int,int,int);
static uint32_t Pantalla[1080][1936],imagenComparación[1080][1936];
uintptr_t búferImagenPlaca(void){return 1;}
static void compararEntero(void){
    punteroPlaca(0,0,0);memcpy(imagenComparación,Pantalla,sizeof(Pantalla));
    uint64_t elementoListaElementoPrevio=númeroElementosDibujoPlaca();terminalPlaca(3);
    assert(memcmp(imagenComparación,Pantalla,sizeof(Pantalla))==0);
    assert(númeroElementosDibujoPlaca()==elementoListaElementoPrevio); /* 같은 화면을 valorReintentar 그려도 mostrarValor 메모리에 쓰지 않는다. */
}
static void escribirTexto(const char *texto){while(*texto)byteTerminal((unsigned char)*texto++);}
int main(void){
    dibujoPrepararPlaca(&Pantalla[0][0],1920,1080,sizeof(Pantalla[0]));
    terminalPlaca(300);escribirTexto("elementoListaPrimero 창의 한글 Datos\n");
    for(int número=1;número<4;número++){terminalPlaca(1);terminalPlaca(100+número);escribirTexto("겹친 창의 한글 Datos\n\033[41m색칠한 saltarEspaciosBlancos     \033[0m\n");}
    compararEntero();
    int posiciónHorizontal=60,posiciónVertical=102,extensiónRangoAnchura=568,valorAltura=360;
    uint64_t diarioMover=0;double tiempoMovimiento=0;
    for(int valorSecuencia=0;valorSecuencia<80;valorSecuencia++){
        punteroTerminal(1,posiciónHorizontal+100,posiciónVertical+15);
        int posiciónHorizontalNuevo=80+(valorSecuencia*37)%850,posiciónVerticalNuevo=50+(valorSecuencia*13)%450;
        píxelPlaca(1900,1050,0x123456); /* actualizar valorRegión 밖의 Usuario Dibujo */
        uint64_t elementoListaElementoPrevio=númeroElementosDibujoPlaca();clock_t ponerEnMarcha=clock();
        punteroTerminal(1,posiciónHorizontalNuevo+100,posiciónVerticalNuevo+15);
        tiempoMovimiento+=(double)(clock()-ponerEnMarcha)/CLOCKS_PER_SEC;
        diarioMover+=númeroElementosDibujoPlaca()-elementoListaElementoPrevio;
        assert(númeroElementosDibujoPlaca()-elementoListaElementoPrevio<=2u*extensiónRangoAnchura*valorAltura);
        assert(Pantalla[1050][1900]==0x123456);
        píxelPlaca(1900,1050,0x302018);
        punteroTerminal(0,posiciónHorizontalNuevo+100,posiciónVerticalNuevo+15);posiciónHorizontal=posiciónHorizontalNuevo;posiciónVertical=posiciónVerticalNuevo;
        compararEntero();
    }
    for(int valorSecuencia=0;valorSecuencia<40;valorSecuencia++){
        int anchuraNuevo=360+(valorSecuencia*29)%700,alturaNuevo=216+(valorSecuencia*17)%350;
        if(anchuraNuevo>1920-posiciónHorizontal)anchuraNuevo=1920-posiciónHorizontal;if(alturaNuevo>1080-posiciónVertical)alturaNuevo=1080-posiciónVertical;
        punteroTerminal(1,posiciónHorizontal+extensiónRangoAnchura-4,posiciónVertical+valorAltura-4);
        punteroTerminal(1,posiciónHorizontal+anchuraNuevo-4,posiciónVertical+alturaNuevo-4);
        uint64_t elementoListaElementoPrevio=númeroElementosDibujoPlaca();
        punteroTerminal(1,posiciónHorizontal+anchuraNuevo-4,posiciónVertical+alturaNuevo-4);
        assert(númeroElementosDibujoPlaca()==elementoListaElementoPrevio); /* 같은 좌표의 중복 evento */
        punteroTerminal(0,posiciónHorizontal+anchuraNuevo-4,posiciónVertical+alturaNuevo-4);extensiónRangoAnchura=anchuraNuevo;valorAltura=alturaNuevo;
        compararEntero();
    }
    /* valorRecortado 범위와 datosEfectivo línea 간격을 지킨다. */
    for(int línea=0;línea<1080;línea++)for(int entradaElementoRanura=1920;entradaElementoRanura<1936;entradaElementoRanura++)assert(Pantalla[línea][entradaElementoRanura]==0);
    assert(!dibujoIniciarPlaca(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",tiempoMovimiento*1000/80,(unsigned long long)(diarioMover/80));
    return 0;
}
