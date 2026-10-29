#include "valorRemoto.h"
#include <string.h>
#include "tablaTecladoEstablecerDos.h"
static unsigned valorControl,teclaDesplazar,textoHangul;
typedef struct {unsigned elementoListaPrimero,medio,terminación;} estadoValorComposición;
static estadoValorComposición Combinación,registroEntradaDiario[16];
static unsigned númeroElementosDiario;
void teclaRemotoConfirmar(void){memset(&Combinación,0,sizeof(Combinación));númeroElementosDiario=0;}
void inicializarTrazoTeclaRemoto(void){valorControl=teclaDesplazar=textoHangul=0;teclaRemotoConfirmar();}
static void ponerTexto(unsigned valor){
    unsigned char texto[4];unsigned númeroValor;
    if(valor<128){texto[0]=valor;númeroValor=1;}else if(valor<2048){texto[0]=0xc0|(valor>>6);texto[1]=0x80|(valor&63);númeroValor=2;}
    else if(valor<65536){texto[0]=0xe0|(valor>>12);texto[1]=0x80|((valor>>6)&63);texto[2]=0x80|(valor&63);númeroValor=3;}
    else{texto[0]=0xf0|(valor>>18);texto[1]=0x80|((valor>>12)&63);texto[2]=0x80|((valor>>6)&63);texto[3]=0x80|(valor&63);númeroValor=4;}
    entradaRemotoAlimentar(texto,númeroValor);
}
static int encontrarEntradaElemento(const unsigned *listaEntradaElemento,unsigned númeroValor,unsigned valor){for(unsigned índiceOrdinal=0;índiceOrdinal<númeroValor;índiceOrdinal++)if(listaEntradaElemento[índiceOrdinal]==valor)return índiceOrdinal;return -1;}
static unsigned encontrarDuplicado(const unsigned Tabla[][3],unsigned númeroValor,unsigned operandoPrimero,unsigned operandoSegundo){for(unsigned índiceOrdinal=0;índiceOrdinal<númeroValor;índiceOrdinal++)if(Tabla[índiceOrdinal][0]==operandoPrimero&&Tabla[índiceOrdinal][1]==operandoSegundo)return Tabla[índiceOrdinal][2];return 0;}
static unsigned textoCompuesto(void){
    if(Combinación.elementoListaPrimero&&Combinación.medio)return 0xac00+(encontrarEntradaElemento(tablaLetraHangulInicialValor,19,Combinación.elementoListaPrimero)*21+encontrarEntradaElemento(tablaLetraHangulVocalMedial,21,Combinación.medio))*28+(Combinación.terminación?encontrarEntradaElemento(tablaLetraHangulFinal,28,Combinación.terminación):0);
    return Combinación.elementoListaPrimero?Combinación.elementoListaPrimero:Combinación.medio;
}
static int hangulAlimentar(unsigned trazoTecla){
    unsigned valorLetraHangul=0;for(unsigned índiceOrdinal=0;índiceOrdinal<sizeof(disposiciónTecla)/sizeof(disposiciónTecla[0]);índiceOrdinal++)if(disposiciónTecla[índiceOrdinal][0]==trazoTecla)valorLetraHangul=disposiciónTecla[índiceOrdinal][1];
    if(!valorLetraHangul&&trazoTecla>='A'&&trazoTecla<='Z')return hangulAlimentar(trazoTecla+32);if(!valorLetraHangul)return 0;
    unsigned elementoListaElementoPrevio=textoCompuesto(),valorConfirmar=0;estadoValorComposición valorAntes=Combinación;
    if(númeroElementosDiario<16)registroEntradaDiario[númeroElementosDiario++]=valorAntes;
    if(encontrarEntradaElemento(tablaLetraHangulInicialValor,19,valorLetraHangul)>=0){
        if(Combinación.elementoListaPrimero&&Combinación.medio&&!Combinación.terminación&&encontrarEntradaElemento(tablaLetraHangulFinal,28,valorLetraHangul)>=0)Combinación.terminación=valorLetraHangul;
        else{unsigned valorSuperponer=encontrarDuplicado(letraHangulFinalPalabraCompuesta,11,Combinación.terminación,valorLetraHangul);if(Combinación.terminación&&valorSuperponer)Combinación.terminación=valorSuperponer;
            else{valorConfirmar=elementoListaElementoPrevio;teclaRemotoConfirmar();Combinación.elementoListaPrimero=valorLetraHangul;númeroElementosDiario=1;memset(registroEntradaDiario,0,sizeof(estadoValorComposición));}}
    }else if(Combinación.terminación){
        unsigned ladoIzquierdo=0,derecho=Combinación.terminación;for(unsigned índiceOrdinal=0;índiceOrdinal<11;índiceOrdinal++)if(letraHangulFinalPalabraCompuesta[índiceOrdinal][2]==Combinación.terminación){ladoIzquierdo=letraHangulFinalPalabraCompuesta[índiceOrdinal][0];derecho=letraHangulFinalPalabraCompuesta[índiceOrdinal][1];break;}
        Combinación.terminación=ladoIzquierdo;valorConfirmar=textoCompuesto();teclaRemotoConfirmar();Combinación.elementoListaPrimero=derecho;Combinación.medio=valorLetraHangul;númeroElementosDiario=2;
        memset(registroEntradaDiario,0,2*sizeof(estadoValorComposición));registroEntradaDiario[1].elementoListaPrimero=derecho;
    }else if(Combinación.medio){unsigned valorSuperponer=encontrarDuplicado(letraHangulVocalMedialPalabraCompuesta,7,Combinación.medio,valorLetraHangul);
        if(valorSuperponer)Combinación.medio=valorSuperponer;else{valorConfirmar=elementoListaElementoPrevio;teclaRemotoConfirmar();Combinación.medio=valorLetraHangul;númeroElementosDiario=1;memset(registroEntradaDiario,0,sizeof(estadoValorComposición));}
    }else Combinación.medio=valorLetraHangul;
    if(elementoListaElementoPrevio)ponerTexto(127);if(valorConfirmar)ponerTexto(valorConfirmar);unsigned valorAhora=textoCompuesto();if(valorAhora)ponerTexto(valorAhora);return 1;
}
void trazoTeclaRemoto(unsigned símbolo,int valorPulsar){
    if(símbolo==0xffe3||símbolo==0xffe4){valorControl=valorPulsar;return;}
    if(símbolo==0xffe1||símbolo==0xffe2){teclaDesplazar=valorPulsar;return;}
    if(!valorPulsar)return;
    if(símbolo==0xffc6||símbolo==0xff31||(símbolo==32&&teclaDesplazar&&!valorControl)){
        teclaRemotoConfirmar();textoHangul=!textoHangul;unsigned char evento[]={30,3,textoHangul,0,0,0,0};entradaRemotoAlimentar(evento,7);return;
    }
    if(símbolo==0xff08&&textoHangul&&!valorControl&&númeroElementosDiario){Combinación=registroEntradaDiario[--númeroElementosDiario];ponerTexto(127);unsigned texto=textoCompuesto();if(texto)ponerTexto(texto);return;}
    if(textoHangul&&!valorControl&&símbolo<128&&hangulAlimentar(símbolo))return;
    teclaRemotoConfirmar();
    if((valorControl&&teclaDesplazar&&(símbolo=='t'||símbolo=='T'))||símbolo==0xffc3||símbolo==0xffc9){unsigned char evento[]={30,2,símbolo==0xffc3?2:símbolo==0xffc9?3:1,0,0,0,0};entradaRemotoAlimentar(evento,7);return;}
    const char *valorEspecial=símbolo==0xff08?"\177":símbolo==0xff09?"\t":símbolo==0xff0d?"\r":símbolo==0xff1b?"\033":
        símbolo==0xffff?"\033[3~":símbolo==0xff50?"\033[H":símbolo==0xff57?"\033[F":símbolo==0xff51?"\033[D":
        símbolo==0xff52?"\033[A":símbolo==0xff53?"\033[C":símbolo==0xff54?"\033[B":símbolo==0xff55?"\033[5~":símbolo==0xff56?"\033[6~":0;
    if(valorEspecial){entradaRemotoAlimentar((const unsigned char*)valorEspecial,strlen(valorEspecial));return;}
    unsigned valor=(símbolo&0xff000000)==0x01000000?símbolo&0xffffff:símbolo;
    if(valor>0x10ffff||(valor>=0xd800&&valor<=0xdfff)||(símbolo>=0xff00&&símbolo<0x1000000))return;
    if(valorControl){if(valor>='a'&&valor<='z')valor-=96;else if(valor>='A'&&valor<='Z')valor-=64;}
    ponerTexto(valor);
}
