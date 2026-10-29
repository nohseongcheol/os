#include "../denominación/nombresEnlazarMáquina.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "PilaRed.h"
extern int32_t conectorRedRedBucleJava(int32_t,int32_t,int32_t), asociarRedBucleJava(int32_t,int32_t,int32_t);
extern int32_t enviarRedBucleJava(int32_t,int32_t,int32_t,int32_t), operaciónRecepciónRedBucleJava(int32_t,int32_t);
extern int32_t puertoRedBucleJava(int32_t), direcciónRedBucleJava(int32_t), parRedRedBucleJava(int32_t), cerrarRedBucleJava(int32_t);
extern int32_t ponerRedJava(int32_t,int32_t),obtenerRedJava(int32_t);
extern int32_t crearFlujoBucleJava(void),asociarFlujoBucleJava(int32_t,int32_t,int32_t),escucharFlujoBucleJava(int32_t,int32_t);
extern int32_t conectarFlujoBucleJava(int32_t,int32_t,int32_t),aceptarFlujoBucleJava(int32_t),leerFlujoBucleJava(int32_t,int32_t),escribirFlujoBucleJava(int32_t,int32_t);
extern int32_t puertoFlujoBucleJava(int32_t),parRedFlujoBucleJava(int32_t),cerrarFlujoBucleJava(int32_t);
static int externo[24];
static int direcciónCualquiera[24], escuchadorDoble[24], parRedExternoUDP[8], direcciónAsociado[8];
static int númeroExterno(int manejadorArchivo) { return manejadorArchivo>=32 && manejadorArchivo<56 ? externo[manejadorArchivo-32]-1 : -1; }
static int textoPegar(int manejadorArchivo,int categoríaTipo) {
    if(manejadorArchivo<32||manejadorArchivo>=56)return -9;int elementoListaElementoPrevio=númeroExterno(manejadorArchivo);if(elementoListaElementoPrevio>=0)return elementoListaElementoPrevio;
    int númeroElementosElementoLista=crearExtremoConectorRed(categoríaTipo);if(númeroElementosElementoLista>=0)externo[manejadorArchivo-32]=númeroElementosElementoLista+1;return númeroElementosElementoLista;
}
int32_t conectorRedRedJava(int32_t valorPrimero,int32_t valorSegundo,int32_t códigoCarácter){return conectorRedRedBucleJava(valorPrimero,valorSegundo,códigoCarácter);}
int32_t asociarRedJava(int32_t manejadorArchivo,int32_t DirecciónInternet,int32_t númeroPuerto){
    if(DirecciónInternet==0x7f000001)return asociarRedBucleJava(manejadorArchivo,DirecciónInternet,númeroPuerto);
    if(DirecciónInternet!=0&&DirecciónInternet!=leerEstadoRed(0,0))return -99;
    int valorDevuelto=asociarRedBucleJava(manejadorArchivo,0,númeroPuerto);if(valorDevuelto<0)return valorDevuelto;
    int númeroElementosElementoLista=textoPegar(manejadorArchivo,2);if(númeroElementosElementoLista<0)return númeroElementosElementoLista;valorDevuelto=asociarRedCorta(númeroElementosElementoLista,leerEstadoRed(0,0),puertoRedBucleJava(manejadorArchivo));if(!valorDevuelto)direcciónAsociado[manejadorArchivo-32]=DirecciónInternet;return valorDevuelto;
}
int32_t enviarRedJava(int32_t manejadorArchivo,int32_t DirecciónInternet,int32_t númeroPuerto,int32_t tamaño){
    if(DirecciónInternet==0x7f000001)return enviarRedBucleJava(manejadorArchivo,DirecciónInternet,númeroPuerto,tamaño);
    if(tamaño<0||tamaño>512)return -90;if(númeroPuerto<1||númeroPuerto>65535)return -22;
    if(puertoRedBucleJava(manejadorArchivo)<0)return -9;
    if(direcciónRedBucleJava(manejadorArchivo)==0x7f000001)return -101;
    int númeroElementosElementoLista=númeroExterno(manejadorArchivo);if(númeroElementosElementoLista<0){int valorDevuelto=0;if(puertoRedBucleJava(manejadorArchivo)==0)valorDevuelto=asociarRedBucleJava(manejadorArchivo,0,0);if(valorDevuelto<0)return valorDevuelto;númeroElementosElementoLista=textoPegar(manejadorArchivo,2);if(númeroElementosElementoLista<0)return númeroElementosElementoLista;valorDevuelto=asociarRedCorta(númeroElementosElementoLista,leerEstadoRed(0,0),puertoRedBucleJava(manejadorArchivo));if(valorDevuelto<0)return valorDevuelto;}
    unsigned char Datos[512];for(int índiceOrdinal=0;índiceOrdinal<tamaño;índiceOrdinal++)Datos[índiceOrdinal]=obtenerRedJava(índiceOrdinal);return enviarDatagrama(númeroElementosElementoLista,Datos,tamaño,DirecciónInternet,númeroPuerto);
}
int32_t operaciónRecepciónRedJava(int32_t manejadorArchivo,int32_t tamaño){
    int númeroElementosElementoLista=númeroExterno(manejadorArchivo);if(númeroElementosElementoLista<0)return operaciónRecepciónRedBucleJava(manejadorArchivo,tamaño);if(tamaño<0||tamaño>512)return -22;
    int local=operaciónRecepciónRedBucleJava(manejadorArchivo,tamaño);if(local!=-11){parRedExternoUDP[manejadorArchivo-32]=0;return local;}
    unsigned char Datos[512];int valorDevuelto=recibirDatagrama(númeroElementosElementoLista,Datos,tamaño);if(valorDevuelto>=0)parRedExternoUDP[manejadorArchivo-32]=1;for(int índiceOrdinal=0;índiceOrdinal<valorDevuelto;índiceOrdinal++)ponerRedJava(índiceOrdinal,Datos[índiceOrdinal]);return valorDevuelto;
}
int32_t puertoRedJava(int32_t manejadorArchivo){int númeroElementosElementoLista=númeroExterno(manejadorArchivo);return númeroElementosElementoLista<0?puertoRedBucleJava(manejadorArchivo):(int32_t)númeroPuertoRed(númeroElementosElementoLista);}
int32_t direcciónRedJava(int32_t manejadorArchivo){return númeroExterno(manejadorArchivo)<0?direcciónRedBucleJava(manejadorArchivo):direcciónAsociado[manejadorArchivo-32];}
int32_t parRedRedJava(int32_t manejadorArchivo){int númeroElementosElementoLista=númeroExterno(manejadorArchivo);return númeroElementosElementoLista<0||!parRedExternoUDP[manejadorArchivo-32]?parRedRedBucleJava(manejadorArchivo):(int32_t)númeroPuertoParRed(númeroElementosElementoLista);}
int32_t remotoRedJava(int32_t manejadorArchivo){int númeroElementosElementoLista=númeroExterno(manejadorArchivo);return númeroElementosElementoLista<0||!parRedExternoUDP[manejadorArchivo-32]?0x7f000001:(int32_t)direcciónParRedRedCorta(númeroElementosElementoLista);}
int32_t cerrarRedJava(int32_t manejadorArchivo){int númeroElementosElementoLista=númeroExterno(manejadorArchivo);if(númeroElementosElementoLista>=0){cerrarRed(númeroElementosElementoLista);externo[manejadorArchivo-32]=0;}if(manejadorArchivo>=32&&manejadorArchivo<40)parRedExternoUDP[manejadorArchivo-32]=direcciónAsociado[manejadorArchivo-32]=0;return cerrarRedBucleJava(manejadorArchivo);}
int32_t crearFlujoJava(void){return crearFlujoBucleJava();}
int32_t asociarFlujoJava(int32_t manejadorArchivo,int32_t DirecciónInternet,int32_t númeroPuerto){
    if(DirecciónInternet==0||DirecciónInternet==0x7f000001){int valorDevuelto=asociarFlujoBucleJava(manejadorArchivo,DirecciónInternet,númeroPuerto);if(!valorDevuelto)direcciónCualquiera[manejadorArchivo-32]=DirecciónInternet==0;return valorDevuelto;}
    if(DirecciónInternet!=leerEstadoRed(0,0))return -99;int valorDevuelto=asociarFlujoBucleJava(manejadorArchivo,0,númeroPuerto);if(valorDevuelto<0)return valorDevuelto;
    int númeroElementosElementoLista=textoPegar(manejadorArchivo,1);return númeroElementosElementoLista<0?númeroElementosElementoLista:asociarRedCorta(númeroElementosElementoLista,DirecciónInternet,puertoFlujoBucleJava(manejadorArchivo));
}
int32_t escucharFlujoJava(int32_t manejadorArchivo,int32_t esperaConexiones){
    int númeroElementosElementoLista=númeroExterno(manejadorArchivo);if(númeroElementosElementoLista<0){int valorDevuelto=escucharFlujoBucleJava(manejadorArchivo,esperaConexiones);if(valorDevuelto<0||!direcciónCualquiera[manejadorArchivo-32])return valorDevuelto;
        númeroElementosElementoLista=textoPegar(manejadorArchivo,1);if(númeroElementosElementoLista<0)return númeroElementosElementoLista;valorDevuelto=asociarRedCorta(númeroElementosElementoLista,leerEstadoRed(0,0),puertoFlujoBucleJava(manejadorArchivo));if(valorDevuelto<0)return valorDevuelto;escuchadorDoble[manejadorArchivo-32]=1;
    }return esperaConexiones<1?-22:escucharRedCorta(númeroElementosElementoLista);
}
int32_t conectarFlujoJava(int32_t manejadorArchivo,int32_t DirecciónInternet,int32_t númeroPuerto){
    if(DirecciónInternet==0x7f000001 && númeroExterno(manejadorArchivo)<0)return conectarFlujoBucleJava(manejadorArchivo,DirecciónInternet,númeroPuerto);
    if(puertoFlujoBucleJava(manejadorArchivo)<0)return -9;int númeroElementosElementoLista=textoPegar(manejadorArchivo,1);return númeroElementosElementoLista<0?númeroElementosElementoLista:conectarRedCorta(númeroElementosElementoLista,DirecciónInternet,númeroPuerto);
}
int32_t aceptarFlujoJava(int32_t manejadorArchivo){
    int númeroElementosElementoLista=númeroExterno(manejadorArchivo);if(númeroElementosElementoLista<0)return aceptarFlujoBucleJava(manejadorArchivo);
    if(escuchadorDoble[manejadorArchivo-32]){int local=aceptarFlujoBucleJava(manejadorArchivo);if(local!=-11)return local;}
    int valorParRed=aceptarRedCorta(númeroElementosElementoLista);if(valorParRed<0)return valorParRed;
    int valorObjetivo=crearFlujoBucleJava();if(valorObjetivo<0){cerrarRed(valorParRed);return valorObjetivo;}externo[valorObjetivo-32]=valorParRed+1;return valorObjetivo;
}
int32_t leerFlujoJava(int32_t manejadorArchivo,int32_t tamaño){
    int númeroElementosElementoLista=númeroExterno(manejadorArchivo);if(númeroElementosElementoLista<0)return leerFlujoBucleJava(manejadorArchivo,tamaño);if(tamaño<0||tamaño>512)return -22;
    unsigned char Datos[512];int valorDevuelto=leerRedCorta(númeroElementosElementoLista,Datos,tamaño);for(int índiceOrdinal=0;índiceOrdinal<valorDevuelto;índiceOrdinal++)ponerRedJava(índiceOrdinal,Datos[índiceOrdinal]);return valorDevuelto;
}
int32_t escribirFlujoJava(int32_t manejadorArchivo,int32_t tamaño){
    int númeroElementosElementoLista=númeroExterno(manejadorArchivo);if(númeroElementosElementoLista<0)return escribirFlujoBucleJava(manejadorArchivo,tamaño);if(tamaño<0||tamaño>512)return -22;
    unsigned char Datos[512];for(int índiceOrdinal=0;índiceOrdinal<tamaño;índiceOrdinal++)Datos[índiceOrdinal]=obtenerRedJava(índiceOrdinal);return escribirRedCorta(númeroElementosElementoLista,Datos,tamaño);
}
int32_t puertoFlujoJava(int32_t manejadorArchivo){int númeroElementosElementoLista=númeroExterno(manejadorArchivo);return númeroElementosElementoLista<0?puertoFlujoBucleJava(manejadorArchivo):(int32_t)númeroPuertoRed(númeroElementosElementoLista);}
int32_t parRedFlujoJava(int32_t manejadorArchivo){int númeroElementosElementoLista=númeroExterno(manejadorArchivo);return númeroElementosElementoLista<0?parRedFlujoBucleJava(manejadorArchivo):(int32_t)númeroPuertoParRed(númeroElementosElementoLista);}
int32_t direcciónFlujoJava(int32_t manejadorArchivo){return númeroExterno(manejadorArchivo)<0?0x7f000001:escuchadorDoble[manejadorArchivo-32]?0:leerEstadoRed(0,0);}
int32_t cerrarFlujoJava(int32_t manejadorArchivo){int númeroElementosElementoLista=númeroExterno(manejadorArchivo);if(númeroElementosElementoLista>=0){cerrarRed(númeroElementosElementoLista);externo[manejadorArchivo-32]=0;}if(manejadorArchivo>=40&&manejadorArchivo<56)direcciónCualquiera[manejadorArchivo-32]=escuchadorDoble[manejadorArchivo-32]=0;return cerrarFlujoBucleJava(manejadorArchivo);}
