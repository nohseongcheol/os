/* datosEfectivo Pantalla 메모리와 기존 C invocar 규약만 연결한다. 합성 구현은 fuente/ComponedorBúferImagen.java. */
#include "../denominación/nombresEnlazarMáquina.h"
#include "informaciónPantalla.h"
static volatile uint32_t *listaPíxeles;
static unsigned númeroElementosPalabraFilaPantalla, anchuraPantalla, alturaPantalla;
extern void prepararDibujoJava(int,int),finDibujoJava(void),rectánguloDibujoJava(int,int,int,int,int),punteroDibujoJava(int,int,int);
extern int anchuraDibujoJava(void),alturaDibujoJava(void),bajoNúmeroElementosDibujoJava(void),altoNúmeroElementosDibujoJava(void);
extern int recortarDibujoJava(int,int,int,int),valorRecortarDibujoJava(int),inicioPosiciónDibujoJava(int,int,int,int),píxelDibujoJava(int,int,int);
uintptr_t leerBúferImagenPlaca(uintptr_t posiciónHorizontal,uintptr_t posiciónVertical){
    return listaPíxeles&&posiciónHorizontal<anchuraPantalla&&posiciónVertical<alturaPantalla?listaPíxeles[posiciónVertical*númeroElementosPalabraFilaPantalla+posiciónHorizontal]:0;
}
void escribirBúferImagenPlaca(uintptr_t posiciónHorizontal,uintptr_t posiciónVertical,uintptr_t valorColor){
    if(listaPíxeles&&posiciónHorizontal<anchuraPantalla&&posiciónVertical<alturaPantalla)listaPíxeles[posiciónVertical*númeroElementosPalabraFilaPantalla+posiciónHorizontal]=(uint32_t)valorColor;
}
void dibujoPrepararPlaca(volatile uint32_t *Datos,unsigned extensiónRangoAnchura,unsigned longitud,unsigned valorEspaciadoLínea){
    listaPíxeles=Datos;anchuraPantalla=extensiónRangoAnchura;alturaPantalla=longitud;númeroElementosPalabraFilaPantalla=valorEspaciadoLínea/4;prepararDibujoJava((int)extensiónRangoAnchura,(int)longitud);
}
uintptr_t anchuraPantallaPlaca(void){return (unsigned)anchuraDibujoJava();}
uintptr_t alturaPantallaPlaca(void){return (unsigned)alturaDibujoJava();}
uint64_t númeroElementosDibujoPlaca(void){return ((uint64_t)(uint32_t)altoNúmeroElementosDibujoJava()<<32)|(uint32_t)bajoNúmeroElementosDibujoJava();}
uint32_t pantallaLeerPlaca(unsigned posiciónHorizontal,unsigned posiciónVertical){return (uint32_t)leerBúferImagenPlaca(posiciónHorizontal,posiciónVertical);}
int límitesDibujoPlaca(int *posiciónHorizontal,int *posiciónVertical,int *extensiónRangoAnchura,int *longitud){
    if(!recortarDibujoJava(*posiciónHorizontal,*posiciónVertical,*extensiónRangoAnchura,*longitud))return 0;
    *posiciónHorizontal=valorRecortarDibujoJava(0);*posiciónVertical=valorRecortarDibujoJava(1);*extensiónRangoAnchura=valorRecortarDibujoJava(2);*longitud=valorRecortarDibujoJava(3);return 1;
}
int dibujoIniciarPlaca(int posiciónHorizontal,int posiciónVertical,int extensiónRangoAnchura,int longitud){return inicioPosiciónDibujoJava(posiciónHorizontal,posiciónVertical,extensiónRangoAnchura,longitud);}
void dibujoTerminarPlaca(void){finDibujoJava();}
uintptr_t píxelPlaca(uintptr_t posiciónHorizontal,uintptr_t posiciónVertical,uintptr_t valorColor){return (unsigned)píxelDibujoJava((int)posiciónHorizontal,(int)posiciónVertical,(int)valorColor);}
void rellenarRectánguloPlaca(int posiciónHorizontal,int posiciónVertical,int extensiónRangoAnchura,int longitud,uint32_t valorColor){rectánguloDibujoJava(posiciónHorizontal,posiciónVertical,extensiónRangoAnchura,longitud,(int)valorColor);}
void punteroPlaca(int posiciónHorizontal,int posiciónVertical,unsigned valorForma){punteroDibujoJava(posiciónHorizontal,posiciónVertical,(int)valorForma);}
