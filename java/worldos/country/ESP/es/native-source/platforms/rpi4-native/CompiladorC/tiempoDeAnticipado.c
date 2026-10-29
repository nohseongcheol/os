#include "../denominación/nombresEnlazarMáquina.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "invocar.h"
#include "Paquete.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char Datos[16384];static unsigned longitud,posiciónActual;static int esInválido;
static unsigned listaEtiquetasMarcador[512],valorPrimero[512],valorSegundo[512],reservaConstante,claseActual;
static char texto[65536];static unsigned tamañoTexto;
typedef struct {unsigned bitsConfiguración,nombre,datosDescriptor,secuenciaInstrucciónMáquina,tamaño,variablesLocal,almacenamientoPila;} entradaElementoMétodo;
static entradaElementoMétodo métodosDeclarado[64];static unsigned númeroElementosMétodoDeclarado;
static unsigned nombreCampo[64],descriptorCampo[64],constanteCampo[64],númeroElementosCampoDeclarado;
static unsigned valorTomar(unsigned númeroElementosElementoLista){if(posiciónActual>longitud||númeroElementosElementoLista>longitud-posiciónActual){esInválido=1;return 0;}unsigned posiciónDatos=posiciónActual;posiciónActual+=númeroElementosElementoLista;return posiciónDatos;}
static unsigned datosByte(void){unsigned posiciónDatos=valorTomar(1);return esInválido?0:Datos[posiciónDatos];}
static unsigned valorMitad(void){unsigned coordenadaCoordenadaHorizontal=datosByte();return coordenadaCoordenadaHorizontal<<8|datosByte();}
static uint32_t esLleno(void){uint32_t coordenadaCoordenadaHorizontal=valorMitad();return coordenadaCoordenadaHorizontal<<16|valorMitad();}
static int valorUnicode(unsigned índiceOrdinal,const char*datosCadena){return índiceOrdinal>0&&índiceOrdinal<reservaConstante&&listaEtiquetasMarcador[índiceOrdinal]==1&&strlen(datosCadena)==valorSegundo[índiceOrdinal]&&!memcmp(Datos+valorPrimero[índiceOrdinal],datosCadena,valorSegundo[índiceOrdinal]);}
static int textoIgual(unsigned coordenadaCoordenadaHorizontal,unsigned coordenadaCoordenadaVertical){return coordenadaCoordenadaHorizontal>0&&coordenadaCoordenadaHorizontal<reservaConstante&&coordenadaCoordenadaVertical>0&&coordenadaCoordenadaVertical<reservaConstante&&listaEtiquetasMarcador[coordenadaCoordenadaHorizontal]==1&&listaEtiquetasMarcador[coordenadaCoordenadaVertical]==1&&valorSegundo[coordenadaCoordenadaHorizontal]==valorSegundo[coordenadaCoordenadaVertical]&&!memcmp(Datos+valorPrimero[coordenadaCoordenadaHorizontal],Datos+valorPrimero[coordenadaCoordenadaVertical],valorSegundo[coordenadaCoordenadaHorizontal]);}
static void emitirValor(const char*entradaElementoArchivo,...){if(esInválido)return;va_list arregloArgumento;va_start(arregloArgumento,entradaElementoArchivo);int númeroElementosElementoLista=vsnprintf(texto+tamañoTexto,sizeof(texto)-tamañoTexto,entradaElementoArchivo,arregloArgumento);va_end(arregloArgumento);if(númeroElementosElementoLista<0||(unsigned)númeroElementosElementoLista>=sizeof(texto)-tamañoTexto){esInválido=1;return;}tamañoTexto+=númeroElementosElementoLista;}
static int entradaElementoDescriptor(unsigned valorIdentificador,int*resultado){
    if(valorIdentificador<1||valorIdentificador>=reservaConstante||listaEtiquetasMarcador[valorIdentificador]!=1)return -1;unsigned posiciónDatos=valorPrimero[valorIdentificador],desfaseFin=posiciónDatos+valorSegundo[valorIdentificador];if(posiciónDatos>=desfaseFin||Datos[posiciónDatos++]!='(')return -1;int númeroElementosEntradaElemento=0;
    while(posiciónDatos<desfaseFin&&Datos[posiciónDatos]!=')'){
        unsigned códigoCarácter=Datos[posiciónDatos++];while(códigoCarácter=='['&&posiciónDatos<desfaseFin)códigoCarácter=Datos[posiciónDatos++];
        if(códigoCarácter=='L'){while(posiciónDatos<desfaseFin&&Datos[posiciónDatos]!=';')posiciónDatos++;if(posiciónDatos==desfaseFin)return -1;posiciónDatos++;}
        else if(códigoCarácter!='I'&&códigoCarácter!='Z'&&códigoCarácter!='B'&&códigoCarácter!='C'&&códigoCarácter!='S')return -1;
        if(++númeroElementosEntradaElemento>16)return -1;
    }
    if(posiciónDatos+1>=desfaseFin||Datos[posiciónDatos++]!=')')return -1;*resultado=Datos[posiciónDatos]=='V'?0:1;
    if(Datos[posiciónDatos]=='J'||Datos[posiciónDatos]=='D'||Datos[posiciónDatos]=='F')return -1;return númeroElementosEntradaElemento;
}
static void atributos(void){unsigned númeroElementosElementoLista=valorMitad();for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista&&!esInválido;índiceOrdinal++){valorMitad();unsigned tamaño=esLleno();valorTomar(tamaño);}}
static int analizarEntrada(void){
    if(esLleno()!=0xcafebabe)return -1;unsigned versiónMenor=valorMitad(),númeroVersión=valorMitad();if(versiónMenor||númeroVersión<45||númeroVersión>52)return -1;
    reservaConstante=valorMitad();if(reservaConstante<1||reservaConstante>512)return -1;
    for(unsigned índiceOrdinal=1;índiceOrdinal<reservaConstante&&!esInválido;índiceOrdinal++){
        listaEtiquetasMarcador[índiceOrdinal]=datosByte();switch(listaEtiquetasMarcador[índiceOrdinal]){
        case 1:valorSegundo[índiceOrdinal]=valorMitad();valorPrimero[índiceOrdinal]=valorTomar(valorSegundo[índiceOrdinal]);break;case 3:case 4:valorPrimero[índiceOrdinal]=esLleno();break;
        case 5:case 6:valorTomar(8);if(++índiceOrdinal>=reservaConstante)return -1;break;
        case 7:case 8:case 16:valorPrimero[índiceOrdinal]=valorMitad();break;
        case 9:case 10:case 11:case 12:case 18:valorPrimero[índiceOrdinal]=valorMitad();valorSegundo[índiceOrdinal]=valorMitad();break;
        case 15:valorPrimero[índiceOrdinal]=datosByte();valorSegundo[índiceOrdinal]=valorMitad();break;default:return -1;
        }
    }
    valorMitad();claseActual=valorMitad();valorMitad();if(claseActual<1||claseActual>=reservaConstante||listaEtiquetasMarcador[claseActual]!=7||valorPrimero[claseActual]<1||valorPrimero[claseActual]>=reservaConstante||listaEtiquetasMarcador[valorPrimero[claseActual]]!=1)return -1;unsigned interfaces=valorMitad();valorTomar(interfaces*2);
    númeroElementosCampoDeclarado=valorMitad();if(númeroElementosCampoDeclarado>64)return -1;
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosCampoDeclarado&&!esInválido;índiceOrdinal++){
        unsigned bitsConfiguración=valorMitad();nombreCampo[índiceOrdinal]=valorMitad();descriptorCampo[índiceOrdinal]=valorMitad();
        if(!(bitsConfiguración&8))return -1;
        unsigned númeroElementosEntradaElemento=valorMitad();for(unsigned ordinalInterior=0;ordinalInterior<númeroElementosEntradaElemento&&!esInválido;ordinalInterior++){
            unsigned nombre=valorMitad(),tamaño=esLleno();
            if(valorUnicode(nombre,"ConstantValue")){if(tamaño!=2)return -1;constanteCampo[índiceOrdinal]=valorMitad();}
            else valorTomar(tamaño);
        }
    }
    númeroElementosMétodoDeclarado=valorMitad();if(númeroElementosMétodoDeclarado>64)return -1;
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosMétodoDeclarado&&!esInválido;índiceOrdinal++){
        entradaElementoMétodo*tamañoGrupo=métodosDeclarado+índiceOrdinal;tamañoGrupo->bitsConfiguración=valorMitad();tamañoGrupo->nombre=valorMitad();tamañoGrupo->datosDescriptor=valorMitad();unsigned númeroElementosEntradaElemento=valorMitad();
        for(unsigned ordinalInterior=0;ordinalInterior<númeroElementosEntradaElemento&&!esInválido;ordinalInterior++){
            unsigned nombre=valorMitad(),tamaño=esLleno(),ponerEnMarcha=posiciónActual;
            if(tamaño>longitud-posiciónActual)return -1;
            if(valorUnicode(nombre,"Code")){
                tamañoGrupo->almacenamientoPila=valorMitad();tamañoGrupo->variablesLocal=valorMitad();tamañoGrupo->tamaño=esLleno();tamañoGrupo->secuenciaInstrucciónMáquina=valorTomar(tamañoGrupo->tamaño);
                if(tamañoGrupo->almacenamientoPila>128||tamañoGrupo->variablesLocal>128||tamañoGrupo->tamaño>8192||valorMitad())return -1;atributos();
            }else valorTomar(tamaño);
            if(posiciónActual!=ponerEnMarcha+tamaño)return -1;
        }
        if(!valorUnicode(tamañoGrupo->nombre,"<init>")&&(!(tamañoGrupo->bitsConfiguración&8)||(tamañoGrupo->bitsConfiguración&(0x100|0x20))||!tamañoGrupo->tamaño))return -1;
    }
    atributos();return esInválido||posiciónActual!=longitud?-1:0;
}
static void valorConstante(unsigned valorIdentificador){
    if(!valorIdentificador||valorIdentificador>=reservaConstante){esInválido=1;return;}
    if(listaEtiquetasMarcador[valorIdentificador]==3)emitirValor("P(%uU);",valorPrimero[valorIdentificador]);
    else if(listaEtiquetasMarcador[valorIdentificador]==8)emitirValor("P((W)k%u);",valorIdentificador);else esInválido=1;
}
static void invocar(unsigned valorIdentificador,int llamadaVirtual){
    if(valorIdentificador<1||valorIdentificador>=reservaConstante||(listaEtiquetasMarcador[valorIdentificador]!=10&&listaEtiquetasMarcador[valorIdentificador]!=11)||valorPrimero[valorIdentificador]<1||valorPrimero[valorIdentificador]>=reservaConstante||listaEtiquetasMarcador[valorPrimero[valorIdentificador]]!=7||valorSegundo[valorIdentificador]<1||valorSegundo[valorIdentificador]>=reservaConstante||listaEtiquetasMarcador[valorSegundo[valorIdentificador]]!=12){esInválido=1;return;}
    unsigned objetoPropietario=valorPrimero[valorPrimero[valorIdentificador]],nombre=valorPrimero[valorSegundo[valorIdentificador]],datosDescriptor=valorSegundo[valorSegundo[valorIdentificador]];int resultado=0,númeroElementosElementoLista=entradaElementoDescriptor(datosDescriptor,&resultado);if(númeroElementosElementoLista<0){esInválido=1;return;}
    for(int índiceOrdinal=númeroElementosElementoLista;índiceOrdinal>0;índiceOrdinal--)emitirValor("x[%d]=Q();",índiceOrdinal-1);if(llamadaVirtual)emitirValor("Q();");
    if(!llamadaVirtual&&textoIgual(objetoPropietario,valorPrimero[claseActual])){
        unsigned tamañoGrupo=0;for(;tamañoGrupo<númeroElementosMétodoDeclarado;tamañoGrupo++)if(textoIgual(nombre,métodosDeclarado[tamañoGrupo].nombre)&&textoIgual(datosDescriptor,métodosDeclarado[tamañoGrupo].datosDescriptor))break;
        if(tamañoGrupo==númeroElementosMétodoDeclarado||!(métodosDeclarado[tamañoGrupo].bitsConfiguración&8)){esInválido=1;return;}
        if(resultado)emitirValor("P(");emitirValor("m%u(",tamañoGrupo);for(int índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)emitirValor(índiceOrdinal?",x[%d]":"x[%d]",índiceOrdinal);emitirValor(resultado?"));":" );");return;
    }
    if((llamadaVirtual&&valorUnicode(objetoPropietario,"java/io/PrintStream")&& (valorUnicode(nombre,"print")||valorUnicode(nombre,"println")))||(!llamadaVirtual&&valorUnicode(objetoPropietario,"español/propio/Salida"))){
        if(valorUnicode(datosDescriptor,"(I)V")&&(valorUnicode(nombre,"print")||valorUnicode(nombre,"println")||valorUnicode(nombre,"escribirNúmero"))){emitirValor("jprint(x[0],1,%d);",valorUnicode(nombre,"print")?0:1);return;}
        if(valorUnicode(datosDescriptor,"(Ljava/lang/String;)V")&&(valorUnicode(nombre,"print")||valorUnicode(nombre,"println")||valorUnicode(nombre,"escribir")||valorUnicode(nombre,"escribirLínea"))){emitirValor("jprint(x[0],0,%d);",valorUnicode(nombre,"print")||valorUnicode(nombre,"escribir")?0:1);return;}
        if(valorUnicode(datosDescriptor,"()V")&&valorUnicode(nombre,"println")){emitirValor("jprint((W)\"\",0,1);");return;}
    }
    if(!llamadaVirtual&&valorUnicode(objetoPropietario,"español/propio/Archivo")){
        if(valorUnicode(nombre,"escribir")&&valorUnicode(datosDescriptor,"(Ljava/lang/String;Ljava/lang/String;)V")){emitirValor("jfwrite(x[0],x[1]);");return;}
        if(valorUnicode(nombre,"leer")&&valorUnicode(datosDescriptor,"(Ljava/lang/String;)Ljava/lang/String;")){emitirValor("P(jfread(x[0]));");return;}
    }
    esInválido=1;
}
static void compilarMétodo(unsigned índiceBuscar){
    entradaElementoMétodo*tamañoGrupo=métodosDeclarado+índiceBuscar;if(valorUnicode(tamañoGrupo->nombre,"<init>"))return;int resultado,númeroElementosElementoLista=entradaElementoDescriptor(tamañoGrupo->datosDescriptor,&resultado);if(númeroElementosElementoLista<0){esInválido=1;return;}
    emitirValor("static W m%u(",índiceBuscar);for(int índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)emitirValor(índiceOrdinal?",W a%d":"W a%d",índiceOrdinal);if(!númeroElementosElementoLista)emitirValor("void");
    if((unsigned)númeroElementosElementoLista>tamañoGrupo->variablesLocal){esInválido=1;return;}
    emitirValor("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",tamañoGrupo->variablesLocal?tamañoGrupo->variablesLocal:1);for(int índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)emitirValor("v[%d]=a%d;",índiceOrdinal,índiceOrdinal);
    unsigned guardado=longitud;longitud=tamañoGrupo->secuenciaInstrucciónMáquina+tamañoGrupo->tamaño;posiciónActual=tamañoGrupo->secuenciaInstrucciónMáquina;
    while(posiciónActual<longitud&&!esInválido){unsigned posiciónComando=posiciónActual-tamañoGrupo->secuenciaInstrucciónMáquina,valorOperación=datosByte();emitirValor("L%u:;",posiciónComando);
        if(valorOperación==0){}
        else if(valorOperación==1)emitirValor("P(0);");
        else if(valorOperación>=2&&valorOperación<=8)emitirValor("P(%uU);",valorOperación-3);
        else if(valorOperación==16){int valor=(int8_t)datosByte();emitirValor("P(%uU);",(unsigned)valor);}
        else if(valorOperación==17){int valor=(int16_t)valorMitad();emitirValor("P(%uU);",(unsigned)valor);}
        else if(valorOperación==18||valorOperación==19)valorConstante(valorOperación==18?datosByte():valorMitad());
        else if(valorOperación==21||valorOperación==25){unsigned índiceOrdinal=datosByte();if(índiceOrdinal>=tamañoGrupo->variablesLocal)esInválido=1;emitirValor("P(v[%u]);",índiceOrdinal);}
        else if((valorOperación>=26&&valorOperación<=29)||(valorOperación>=42&&valorOperación<=45)){unsigned índiceOrdinal=valorOperación>=42?valorOperación-42:valorOperación-26;if(índiceOrdinal>=tamañoGrupo->variablesLocal)esInválido=1;emitirValor("P(v[%u]);",índiceOrdinal);}
        else if(valorOperación==54||valorOperación==58){unsigned índiceOrdinal=datosByte();if(índiceOrdinal>=tamañoGrupo->variablesLocal)esInválido=1;emitirValor("v[%u]=Q();",índiceOrdinal);}
        else if((valorOperación>=59&&valorOperación<=62)||(valorOperación>=75&&valorOperación<=78)){unsigned índiceOrdinal=valorOperación>=75?valorOperación-75:valorOperación-59;if(índiceOrdinal>=tamañoGrupo->variablesLocal)esInválido=1;emitirValor("v[%u]=Q();",índiceOrdinal);}
        else if(valorOperación==46||valorOperación==50||valorOperación==51||valorOperación==52||valorOperación==53)emitirValor("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(valorOperación==79||valorOperación==83||valorOperación==84||valorOperación==85||valorOperación==86)emitirValor("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",valorOperación==84?"(unsigned)(signed char)q":valorOperación==85?"(unsigned short)q":valorOperación==86?"(unsigned)(short)q":"q");
        else if(valorOperación==87)emitirValor("Q();");
        else if(valorOperación==89)emitirValor("q=Q();P(q);P(q);");
        else if(valorOperación==90)emitirValor("q=Q();r=Q();P(q);P(r);P(q);");
        else if(valorOperación==95)emitirValor("q=Q();r=Q();P(q);P(r);");
        else if(valorOperación==96||valorOperación==100||valorOperación==104||valorOperación==120||valorOperación==124||valorOperación==126||valorOperación==128||valorOperación==130){const char*valorCodificaciónEstado=valorOperación==96?"+":valorOperación==100?"-":valorOperación==104?"*":valorOperación==120?"<<":valorOperación==124?">>":valorOperación==126?"&":valorOperación==128?"|":"^";emitirValor("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",valorCodificaciónEstado,valorOperación==120||valorOperación==124?"%32":"");}
        else if(valorOperación==108||valorOperación==112)emitirValor("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",valorOperación==112);
        else if(valorOperación==116)emitirValor("P(0U-(unsigned)Q());");
        else if(valorOperación==122)emitirValor("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(valorOperación==132){unsigned índiceOrdinal=datosByte();int valorDiferencia=(int8_t)datosByte();if(índiceOrdinal>=tamañoGrupo->variablesLocal)esInválido=1;emitirValor("v[%u]=(unsigned)v[%u]+%uU;",índiceOrdinal,índiceOrdinal,(unsigned)valorDiferencia);}
        else if(valorOperación>=145&&valorOperación<=147)emitirValor("P((unsigned)(%s)Q());",valorOperación==145?"signed char":valorOperación==146?"unsigned short":"short");
        else if(valorOperación>=153&&valorOperación<=166){int valorObjetivo=(int)posiciónComando+(int16_t)valorMitad();const char*valorComparación[]={"==","!=","<",">=",">","<="};if(valorObjetivo<0||valorObjetivo>=(int)tamañoGrupo->tamaño){esInválido=1;break;}if(valorOperación<159)emitirValor("if((int)Q()%s0)goto L%d;",valorComparación[valorOperación-153],valorObjetivo);else if(valorOperación<165)emitirValor("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",valorComparación[valorOperación-159],valorObjetivo);else emitirValor("q=Q();r=Q();if(r%sq)goto L%d;",valorOperación==165?"==":"!=",valorObjetivo);}
        else if(valorOperación==167){int valorObjetivo=(int)posiciónComando+(int16_t)valorMitad();if(valorObjetivo<0||valorObjetivo>=(int)tamañoGrupo->tamaño)esInválido=1;emitirValor("goto L%d;",valorObjetivo);}
        else if(valorOperación==172||valorOperación==176)emitirValor("return Q();");else if(valorOperación==177)emitirValor("return 0;");
        else if(valorOperación==178||valorOperación==179){unsigned valorIdentificador=valorMitad();if(valorIdentificador<1||valorIdentificador>=reservaConstante||listaEtiquetasMarcador[valorIdentificador]!=9||valorPrimero[valorIdentificador]>=reservaConstante||valorSegundo[valorIdentificador]>=reservaConstante||listaEtiquetasMarcador[valorPrimero[valorIdentificador]]!=7||listaEtiquetasMarcador[valorSegundo[valorIdentificador]]!=12){esInválido=1;break;}unsigned objetoPropietario=valorPrimero[valorPrimero[valorIdentificador]],nombre=valorPrimero[valorSegundo[valorIdentificador]],datosDescriptor=valorSegundo[valorSegundo[valorIdentificador]];
            if(valorOperación==178&&valorUnicode(objetoPropietario,"java/lang/System")&&valorUnicode(nombre,"out")&&valorUnicode(datosDescriptor,"Ljava/io/PrintStream;"))emitirValor("P(1);");
            else {unsigned entradaElementoArchivo=0;while(entradaElementoArchivo<númeroElementosCampoDeclarado&&(!textoIgual(nombre,nombreCampo[entradaElementoArchivo])||!textoIgual(datosDescriptor,descriptorCampo[entradaElementoArchivo])))entradaElementoArchivo++;if(!textoIgual(objetoPropietario,valorPrimero[claseActual])||entradaElementoArchivo==númeroElementosCampoDeclarado){esInválido=1;break;}emitirValor(valorOperación==178?"P(fields[%u]);":"fields[%u]=Q();",entradaElementoArchivo);}}
        else if(valorOperación==182||valorOperación==184)invocar(valorMitad(),valorOperación==182);
        else if(valorOperación==188){unsigned categoríaTipo=datosByte();if(categoríaTipo!=4&&categoríaTipo!=5&&categoríaTipo!=8&&categoríaTipo!=9&&categoríaTipo!=10)esInválido=1;emitirValor("P(jarray((int)Q()));");}
        else if(valorOperación==190)emitirValor("P(jlength(Q()));");
        else if(valorOperación==198||valorOperación==199){int valorObjetivo=(int)posiciónComando+(int16_t)valorMitad();if(valorObjetivo<0||valorObjetivo>=(int)tamañoGrupo->tamaño)esInválido=1;emitirValor("if(Q()%s0)goto L%d;",valorOperación==198?"==":"!=",valorObjetivo);}
        else esInválido=1;
        if(esInválido)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",índiceBuscar,valorOperación,posiciónComando);
        emitirValor("\n");
    }
    longitud=guardado;emitirValor("jfail();return 0;}\n");
}
static unsigned unidadCadena(unsigned *posiciónDatos,unsigned desfaseFin){
    if(*posiciónDatos>=desfaseFin){esInválido=1;return 0;}unsigned códigoCarácter=Datos[(*posiciónDatos)++];
    if(códigoCarácter<128)return códigoCarácter;
    unsigned númeroElementosElementoLista=códigoCarácter>=0xc0&&códigoCarácter<=0xdf?1:códigoCarácter>=0xe0&&códigoCarácter<=0xef?2:3;
    if(númeroElementosElementoLista==3||númeroElementosElementoLista>desfaseFin-*posiciónDatos){esInválido=1;return 0;}unsigned valor=códigoCarácter&((1u<<(6-númeroElementosElementoLista))-1);
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++){unsigned elementoListaSiguiente=Datos[(*posiciónDatos)++];if((elementoListaSiguiente&0xc0)!=0x80)esInválido=1;valor=valor<<6|(elementoListaSiguiente&63);}
    if((númeroElementosElementoLista==1&&valor<128&&valor!=0)||(númeroElementosElementoLista==2&&valor<2048))esInválido=1;return valor;
}
static void constanteCadena(unsigned valorIdentificador){
    unsigned valorSinSigno=valorPrimero[valorIdentificador];if(valorSinSigno<1||valorSinSigno>=reservaConstante||listaEtiquetasMarcador[valorSinSigno]!=1){esInválido=1;return;}emitirValor("static const unsigned char k%u[]={",valorIdentificador);
    unsigned posiciónDatos=valorPrimero[valorSinSigno],desfaseFin=posiciónDatos+valorSegundo[valorSinSigno];
    while(posiciónDatos<desfaseFin&&!esInválido){unsigned códigoCarácter=unidadCadena(&posiciónDatos,desfaseFin);
        if(códigoCarácter>=0xd800&&códigoCarácter<=0xdbff){unsigned parteBajo=unidadCadena(&posiciónDatos,desfaseFin);if(parteBajo<0xdc00||parteBajo>0xdfff){esInválido=1;break;}códigoCarácter=0x10000+((códigoCarácter-0xd800)<<10)+parteBajo-0xdc00;}
        else if(códigoCarácter>=0xdc00&&códigoCarácter<=0xdfff){esInválido=1;break;}
        if(!códigoCarácter){printf("jaot: embedded NUL string needs JVM mode\n");esInválido=1;break;}
        if(códigoCarácter<128)emitirValor("%u,",códigoCarácter);
        else{unsigned númeroElementosElementoLista=códigoCarácter<2048?2:códigoCarácter<65536?3:4;emitirValor("%u,",(númeroElementosElementoLista==2?0xc0:númeroElementosElementoLista==3?0xe0:0xf0)|(códigoCarácter>>(6*(númeroElementosElementoLista-1))));for(unsigned índiceOrdinal=númeroElementosElementoLista-1;índiceOrdinal;índiceOrdinal--)emitirValor("%u,",0x80|((códigoCarácter>>(6*(índiceOrdinal-1)))&63));}
    }emitirValor("0};\n");
}
const char *fuenteCompilaciónJavaAnticipada(const char*nombre){
    size_t númeroElementosElementoLista=strlen(nombre);
    if(númeroElementosElementoLista>4&&!strcmp(nombre+númeroElementosElementoLista-4,".jar")){
        if(abrirJAR(nombre)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char ruta[256];const char*métodoEntradaElemento=principalJAR();númeroElementosElementoLista=strlen(métodoEntradaElemento);if(númeroElementosElementoLista+6>=sizeof(ruta))return 0;
        for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)ruta[índiceOrdinal]=métodoEntradaElemento[índiceOrdinal]=='.'?'/':métodoEntradaElemento[índiceOrdinal];strcpy(ruta+númeroElementosElementoLista,".class");int númeroElementosEntradaElemento=leerJAR(ruta,Datos,sizeof(Datos));if(númeroElementosEntradaElemento<0)return 0;longitud=númeroElementosEntradaElemento;
    }else{intptr_t manejadorArchivo=invocarUsuario(3,(uintptr_t)nombre,0,0,0,0,0);if(manejadorArchivo<0)return 0;intptr_t númeroElementosEntradaElemento=invocarUsuario(9,manejadorArchivo,0,0,0,0,0);if(númeroElementosEntradaElemento<0||númeroElementosEntradaElemento>sizeof(Datos)){invocarUsuario(4,manejadorArchivo,0,0,0,0,0);return 0;}intptr_t númeroElementosRecibido=invocarUsuario(2,manejadorArchivo,(uintptr_t)Datos,númeroElementosEntradaElemento,0,0,0);invocarUsuario(4,manejadorArchivo,0,0,0,0,0);if(númeroElementosRecibido!=númeroElementosEntradaElemento)return 0;longitud=númeroElementosEntradaElemento;}
    if(analizarEntrada()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    emitirValor("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned índiceOrdinal=1;índiceOrdinal<reservaConstante&&!esInválido;índiceOrdinal++)if(listaEtiquetasMarcador[índiceOrdinal]==8)constanteCadena(índiceOrdinal);
    if(esInválido)return 0;
    int puntoEntradaElemento=-1,valorInicialValor=-1;
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosMétodoDeclarado;índiceOrdinal++)if(!valorUnicode(métodosDeclarado[índiceOrdinal].nombre,"<init>")){
        int resultado,númeroElementosEntradaElemento=entradaElementoDescriptor(métodosDeclarado[índiceOrdinal].datosDescriptor,&resultado);if(númeroElementosEntradaElemento<0)return 0;emitirValor("static W m%u(",índiceOrdinal);for(int ordinalInterior=0;ordinalInterior<númeroElementosEntradaElemento;ordinalInterior++)emitirValor(ordinalInterior?",W":"W");if(!númeroElementosEntradaElemento)emitirValor("void");emitirValor(");\n");
        if(valorUnicode(métodosDeclarado[índiceOrdinal].nombre,"main")&&valorUnicode(métodosDeclarado[índiceOrdinal].datosDescriptor,"([Ljava/lang/String;)V")&&(métodosDeclarado[índiceOrdinal].bitsConfiguración&9)==9)puntoEntradaElemento=índiceOrdinal;
        if(valorUnicode(métodosDeclarado[índiceOrdinal].nombre,"<clinit>"))valorInicialValor=índiceOrdinal;
    }
    if(puntoEntradaElemento<0)return 0;for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosMétodoDeclarado&&!esInválido;índiceOrdinal++)compilarMétodo(índiceOrdinal);
    emitirValor("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned índiceOrdinal=0;índiceOrdinal<númeroElementosCampoDeclarado;índiceOrdinal++)if(constanteCampo[índiceOrdinal]){
        unsigned códigoCarácter=constanteCampo[índiceOrdinal];if(códigoCarácter>=reservaConstante)return 0;
        if(listaEtiquetasMarcador[códigoCarácter]==3)emitirValor("fields[%u]=%uU;",índiceOrdinal,valorPrimero[códigoCarácter]);else if(listaEtiquetasMarcador[códigoCarácter]==8)emitirValor("fields[%u]=(W)k%u;",índiceOrdinal,códigoCarácter);else return 0;
    }
    if(valorInicialValor>=0)emitirValor("m%d();",valorInicialValor);emitirValor("m%d((W)a);return 0;}\n",puntoEntradaElemento);
    return esInválido?0:texto;
}
