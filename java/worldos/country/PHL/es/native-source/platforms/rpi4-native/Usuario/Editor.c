/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "invocar.h"
#include "ABIArchivo.h"
#define capacidadEditor 16384
static unsigned char texto[capacidadEditor],datosDeshacer[capacidadEditor],datosCopiado[capacidadEditor],datosResultado[1024];
static int longitud,valorÍndice,entradaElementoExtremoSuperior,ladoIzquierdo,cambiadoEra,insertar,longitudDeshacer,ladoSuperior,cambiosDeshacer,deshacerPoseer,copiarLongitud,capacidadUsado,columnas=68,númeroElementosFila=19;
static char nombreEntradaElementoArchivo[64],comando[128],encontrarEntradaElemento[128];
static const char *textoNotificación="NORMAL  i:insert  :w:save  :q:quit";
static unsigned teclaPendiente;
static int categoríaAyuda,imagenEstadoValor,colaEstadoValor;
static void vaciarBúfer(void){if(capacidadUsado){invocarUsuario(1,1,(uintptr_t)datosResultado,capacidadUsado,0,0,0);capacidadUsado=0;}}
static void datosByte(unsigned códigoCarácter){if(imagenEstadoValor){if((códigoCarácter&192)!=128){colaEstadoValor+=códigoCarácter>=196?2:1;}if(colaEstadoValor>=columnas)return;}if(capacidadUsado==(int)sizeof(datosResultado))vaciarBúfer();datosResultado[capacidadUsado++]=códigoCarácter;}
static void emitirTexto(const char *datosCadena){while(*datosCadena)datosByte((unsigned char)*datosCadena++);}
static void valorNumérico(unsigned númeroElementosElementoLista){char valorSegundo[12];int índiceOrdinal=0;do{valorSegundo[índiceOrdinal++]='0'+númeroElementosElementoLista%10;númeroElementosElementoLista/=10;}while(númeroElementosElementoLista);while(índiceOrdinal)datosByte(valorSegundo[--índiceOrdinal]);}
static void valorMover(int posiciónFila,int posiciónColumna){emitirTexto("\033[");valorNumérico(posiciónFila);datosByte(';');valorNumérico(posiciónColumna);datosByte('H');}
static int elementoPrevio(int posiciónDatos){if(posiciónDatos){posiciónDatos--;while(posiciónDatos>0&&(texto[posiciónDatos]&192)==128)posiciónDatos--;}return posiciónDatos;}
static int elementoListaSiguiente(int posiciónDatos){if(posiciónDatos<longitud){posiciónDatos++;while(posiciónDatos<longitud&&(texto[posiciónDatos]&192)==128)posiciónDatos++;}return posiciónDatos;}
static int ponerEnMarcha(int posiciónDatos){while(posiciónDatos>0&&texto[posiciónDatos-1]!='\n')posiciónDatos--;return posiciónDatos;}
static int desfaseFin(int posiciónDatos){while(posiciónDatos<longitud&&texto[posiciónDatos]!='\n')posiciónDatos++;return posiciónDatos;}
static int valorAnchura(unsigned códigoCarácter){return códigoCarácter>=196?2:1;}
static int columna(int posiciónDatos){int códigoCarácter=0;for(int índiceOrdinal=ponerEnMarcha(posiciónDatos);índiceOrdinal<posiciónDatos;índiceOrdinal=elementoListaSiguiente(índiceOrdinal))códigoCarácter+=texto[índiceOrdinal]=='\t'?4-códigoCarácter%4:valorAnchura(texto[índiceOrdinal]);return códigoCarácter;}
static void puntoControl(void){for(int índiceOrdinal=0;índiceOrdinal<longitud;índiceOrdinal++)datosDeshacer[índiceOrdinal]=texto[índiceOrdinal];longitudDeshacer=longitud;ladoSuperior=valorÍndice;cambiosDeshacer=cambiadoEra;deshacerPoseer=1;}
static void borrarContenidoBytes(int posiciónPartida,int posiciónLlegada){puntoControl();for(int índiceOrdinal=posiciónLlegada;índiceOrdinal<longitud;índiceOrdinal++)texto[posiciónPartida+índiceOrdinal-posiciónLlegada]=texto[índiceOrdinal];longitud-=posiciónLlegada-posiciónPartida;valorÍndice=posiciónPartida;cambiadoEra=1;}
static int añadirFinalValor(const unsigned char *datosCadena,int númeroElementosElementoLista){if(númeroElementosElementoLista>capacidadEditor-longitud){textoNotificación="File full (16384 bytes)";return 0;}puntoControl();for(int índiceOrdinal=longitud-1;índiceOrdinal>=valorÍndice;índiceOrdinal--)texto[índiceOrdinal+númeroElementosElementoLista]=texto[índiceOrdinal];for(int índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++)texto[valorÍndice+índiceOrdinal]=datosCadena[índiceOrdinal];longitud+=númeroElementosElementoLista;valorÍndice+=númeroElementosElementoLista;cambiadoEra=1;return 1;}
static void vertical(int valorDiferencia){int posiciónColumna=columna(valorÍndice),posiciónDatos=ponerEnMarcha(valorÍndice);if(valorDiferencia<0){if(!posiciónDatos)return;posiciónDatos=ponerEnMarcha(posiciónDatos-1);}else{posiciónDatos=desfaseFin(posiciónDatos);if(posiciónDatos==longitud)return;posiciónDatos++;}int códigoCarácter=0;while(posiciónDatos<longitud&&texto[posiciónDatos]!='\n'&&códigoCarácter<posiciónColumna){códigoCarácter+=texto[posiciónDatos]=='\t'?4-códigoCarácter%4:valorAnchura(texto[posiciónDatos]);posiciónDatos=elementoListaSiguiente(posiciónDatos);}valorÍndice=posiciónDatos;}
static void dibujarPantalla(void){
    if(valorÍndice>longitud)valorÍndice=longitud;if(entradaElementoExtremoSuperior>valorÍndice)entradaElementoExtremoSuperior=ponerEnMarcha(valorÍndice);entradaElementoExtremoSuperior=ponerEnMarcha(entradaElementoExtremoSuperior);
    int posiciónFila=0;for(int índiceOrdinal=entradaElementoExtremoSuperior;índiceOrdinal<valorÍndice;índiceOrdinal++)if(texto[índiceOrdinal]=='\n')posiciónFila++;
    while(posiciónFila>=númeroElementosFila-1){entradaElementoExtremoSuperior=desfaseFin(entradaElementoExtremoSuperior);if(entradaElementoExtremoSuperior<longitud)entradaElementoExtremoSuperior++;posiciónFila--;}
    int posiciónColumna=columna(valorÍndice);if(posiciónColumna<ladoIzquierdo)ladoIzquierdo=posiciónColumna;if(posiciónColumna-ladoIzquierdo>=columnas-1)ladoIzquierdo=posiciónColumna-columnas+2;
    emitirTexto("\033[?25l");int posiciónDatos=entradaElementoExtremoSuperior;
    for(int valorDevuelto=0;valorDevuelto<númeroElementosFila-1;valorDevuelto++){
        valorMover(valorDevuelto+1,1);emitirTexto("\033[0m\033[2K");int códigoCarácter=0,esDibujado=0;
        if(posiciónDatos>=longitud&&valorDevuelto>posiciónFila){emitirTexto("\033[90m~\033[0m");continue;}
        while(posiciónDatos<longitud&&texto[posiciónDatos]!='\n'){
            int desfaseSiguiente=elementoListaSiguiente(posiciónDatos),valorAnchuraSolicitado=texto[posiciónDatos]=='\t'?4-códigoCarácter%4:valorAnchura(texto[posiciónDatos]);
            if(códigoCarácter>=ladoIzquierdo&&códigoCarácter-ladoIzquierdo+valorAnchuraSolicitado<columnas){
                if(texto[posiciónDatos]=='\t'){for(int ordinalInterior=0;ordinalInterior<valorAnchuraSolicitado;ordinalInterior++)datosByte(' ');}else if(texto[posiciónDatos]<32||texto[posiciónDatos]==127){datosByte('?');}else for(int ordinalInterior=posiciónDatos;ordinalInterior<desfaseSiguiente;ordinalInterior++)datosByte(texto[ordinalInterior]);esDibujado+=valorAnchuraSolicitado;
            }códigoCarácter+=valorAnchuraSolicitado;posiciónDatos=desfaseSiguiente;
        }
        (void)esDibujado;if(posiciónDatos<longitud)posiciónDatos++;
    }
    valorMover(númeroElementosFila,1);emitirTexto("\033[7m\033[2K");imagenEstadoValor=1;colaEstadoValor=0;emitirTexto(insertar?"INSERT ":"NORMAL ");
    int bytesNombre=0;while(nombreEntradaElementoArchivo[bytesNombre]&&bytesNombre<30)datosByte(nombreEntradaElementoArchivo[bytesNombre++]);emitirTexto(cambiadoEra?" [+] ":" ");
    emitirTexto("L");int línea=1;for(int índiceOrdinal=0;índiceOrdinal<valorÍndice;índiceOrdinal++)if(texto[índiceOrdinal]=='\n')línea++;valorNumérico(línea);emitirTexto(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(textoNotificación){int númeroElementosElementoLista=0;emitirTexto(" | ");while(textoNotificación[númeroElementosElementoLista]&&númeroElementosElementoLista<20)datosByte(textoNotificación[númeroElementosElementoLista++]);}
    imagenEstadoValor=0;emitirTexto("\033[0m");valorMover(posiciónFila+1,posiciónColumna-ladoIzquierdo+1);emitirTexto("\033[?25h");vaciarBúfer();
}
static int valorPulsado(void){
    if(teclaPendiente){int índiceTercero=teclaPendiente;teclaPendiente=0;return índiceTercero;}
    for(;;){
        int índiceTercero=invocarUsuario(16,1,0,0,0,0,0);
        unsigned tamaño=invocarUsuario(16,3,0,0,0,0,0);
        if(columnas!=(int)(tamaño&65535)||númeroElementosFila!=(int)(tamaño>>16)){
            columnas=tamaño&65535;númeroElementosFila=tamaño>>16;dibujarPantalla();
            if(categoríaAyuda){valorMover(númeroElementosFila,1);emitirTexto("\033[0m\033[2K");datosByte(categoríaAyuda);emitirTexto(comando);vaciarBúfer();}
        }
        if(índiceTercero>=0)return índiceTercero;
    }
}
static int escapado(void){
    unsigned posiciónActual=invocarUsuario(7,0,0,0,0,0,0);int índiceTercero=-1;
    while((unsigned)invocarUsuario(7,0,0,0,0,0,0)-posiciónActual<100){índiceTercero=invocarUsuario(16,1,0,0,0,0,0);if(índiceTercero>=0)break;}
    if(índiceTercero<0)return 27;if(índiceTercero!='['&&índiceTercero!='O'){teclaPendiente=índiceTercero;return 27;}
    int númeroElementosElementoLista=0;for(int índiceOrdinal=0;índiceOrdinal<12;índiceOrdinal++){índiceTercero=valorPulsado();if(índiceTercero>='0'&&índiceTercero<='9'){númeroElementosElementoLista=númeroElementosElementoLista*10+índiceTercero-'0';continue;}if(índiceTercero=='A')return 1001;if(índiceTercero=='B')return 1002;if(índiceTercero=='C')return 1003;if(índiceTercero=='D')return 1004;if(índiceTercero=='H')return 1005;if(índiceTercero=='F')return 1006;if(índiceTercero=='~')return númeroElementosElementoLista==3?1007:númeroElementosElementoLista==5?1008:númeroElementosElementoLista==6?1009:númeroElementosElementoLista==1?1005:númeroElementosElementoLista==4?1006:27;return 27;}return 27;
}
static int valorAlmacenar(void){
    int manejadorArchivo=abrirArchivo(nombreEntradaElementoArchivo,EscribirLeer|AusenteSiCrear|ContenidoTruncar,0600);if(manejadorArchivo<0){textoNotificación="Cannot open for save";return 0;}
    intptr_t númeroElementosElementoLista=escribirDatosArchivo(manejadorArchivo,texto,longitud);cerrarArchivo(manejadorArchivo);if(númeroElementosElementoLista!=longitud){textoNotificación="Write failed";return 0;}cambiadoEra=0;textoNotificación="Saved (RAM)";return 1;
}
static int igual(const char *valorPrimero,const char *valorSegundo){while(*valorPrimero&&*valorPrimero==*valorSegundo){valorPrimero++;valorSegundo++;}return *valorPrimero==*valorSegundo;}
static void encontrarSiguiente(void){int númeroElementosElementoLista=0;while(encontrarEntradaElemento[númeroElementosElementoLista])númeroElementosElementoLista++;if(!númeroElementosElementoLista){textoNotificación="No search pattern";return;}for(int índiceOrdinal=1;índiceOrdinal<=longitud;índiceOrdinal++){int posiciónDatos=(valorÍndice+índiceOrdinal)%(longitud?longitud:1),ordinalInterior=0;while(ordinalInterior<númeroElementosElementoLista&&posiciónDatos+ordinalInterior<longitud&&texto[posiciónDatos+ordinalInterior]==(unsigned char)encontrarEntradaElemento[ordinalInterior])ordinalInterior++;if(ordinalInterior==númeroElementosElementoLista){valorÍndice=posiciónDatos;textoNotificación="Match";return;}}textoNotificación="Pattern not found";}
static int indicadorEntrada(int valorCategoría){
    int númeroElementosElementoLista=0;comando[0]=0;
    for(;;){valorMover(númeroElementosFila,1);emitirTexto("\033[0m\033[2K");datosByte(valorCategoría);emitirTexto(comando);vaciarBúfer();categoríaAyuda=valorCategoría;int índiceTercero=valorPulsado();categoríaAyuda=0;
        if(índiceTercero==27||índiceTercero==3)return 0;if(índiceTercero==13||índiceTercero==10)break;
        if(índiceTercero==127||índiceTercero==8){if(númeroElementosElementoLista){númeroElementosElementoLista--;while(númeroElementosElementoLista>0&&((unsigned char)comando[númeroElementosElementoLista]&192)==128)númeroElementosElementoLista--;comando[númeroElementosElementoLista]=0;}continue;}
        if(índiceTercero>=32&&índiceTercero<256&&númeroElementosElementoLista<120){comando[númeroElementosElementoLista++]=índiceTercero;comando[númeroElementosElementoLista]=0;}
    }
    if(valorCategoría=='/'){for(int índiceOrdinal=0;índiceOrdinal<=númeroElementosElementoLista;índiceOrdinal++)encontrarEntradaElemento[índiceOrdinal]=comando[índiceOrdinal];encontrarSiguiente();return 0;}
    if(igual(comando,"q!"))return 1;
    if(igual(comando,"q")){if(!cambiadoEra)return 1;textoNotificación="Unsaved: :w or :q!";return 0;}
    if(igual(comando,"wq")||igual(comando,"x"))return valorAlmacenar();
    if(igual(comando,"w")){valorAlmacenar();return 0;}
    if(comando[0]=='w'&&comando[1]==' '){int índiceOrdinal=2;while(comando[índiceOrdinal]==' ')índiceOrdinal++;int tamaño=númeroElementosElementoLista-índiceOrdinal;if(tamaño<1||tamaño>63){textoNotificación="Invalid file name";return 0;}for(int ordinalInterior=0;ordinalInterior<tamaño;ordinalInterior++)nombreEntradaElementoArchivo[ordinalInterior]=comando[índiceOrdinal+ordinalInterior];nombreEntradaElementoArchivo[tamaño]=0;valorAlmacenar();return 0;}
    int línea=0;for(int índiceOrdinal=0;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++){if(comando[índiceOrdinal]<'0'||comando[índiceOrdinal]>'9'){línea=0;break;}línea=línea*10+comando[índiceOrdinal]-'0';if(línea>16384){línea=0;break;}}
    if(línea){valorÍndice=0;while(--línea&&valorÍndice<longitud){valorÍndice=desfaseFin(valorÍndice);if(valorÍndice<longitud)valorÍndice++;}return 0;}
    textoNotificación="Unknown vi command";return 0;
}
int iniciarProgramaUsuario(int valorIgnorado){
    (void)valorIgnorado;if(númeroElementosArgumentoUsuario()!=1||argumentoUsuario(0,nombreEntradaElementoArchivo,sizeof(nombreEntradaElementoArchivo))<0){emitirTexto("Usage: vi FILE\n");vaciarBúfer();return 2;}
    int manejadorArchivo=abrirArchivo(nombreEntradaElementoArchivo,leerValorSolamente,0);
    if(manejadorArchivo>=0){int númeroElementosElementoLista=tamañoArchivo(manejadorArchivo);if(númeroElementosElementoLista<0||númeroElementosElementoLista>capacidadEditor){cerrarArchivo(manejadorArchivo);return 1;}longitud=leerDatosArchivo(manejadorArchivo,texto,númeroElementosElementoLista);cerrarArchivo(manejadorArchivo);if(longitud!=númeroElementosElementoLista)return 1;for(int índiceOrdinal=0;índiceOrdinal<longitud;índiceOrdinal++)if(!texto[índiceOrdinal]){emitirTexto("vi: NUL byte in text file\n");vaciarBúfer();return 1;}}
    else if(númeroError!=2){emitirTexto("vi: cannot read file\n");vaciarBúfer();return 1;}
    int colorAtenuar=invocarUsuario(16,0,0,0,0,0,0);if(colorAtenuar<0){emitirTexto("vi: use a standalone interactive command\n");vaciarBúfer();return 1;}columnas=colorAtenuar&65535;númeroElementosFila=(unsigned)colorAtenuar>>16;
    emitirTexto("\033[2J\033[H");vaciarBúfer();
    int partePrevio=0,programaTerminarSesión=0;
    while(!programaTerminarSesión){dibujarPantalla();int índiceTercero=valorPulsado();if(índiceTercero==27)índiceTercero=escapado();textoNotificación=0;
        if(índiceTercero==1001){vertical(-1);continue;}if(índiceTercero==1002){vertical(1);continue;}if(índiceTercero==1003){valorÍndice=elementoListaSiguiente(valorÍndice);continue;}if(índiceTercero==1004){valorÍndice=elementoPrevio(valorÍndice);continue;}
        if(índiceTercero==1005){valorÍndice=ponerEnMarcha(valorÍndice);continue;}if(índiceTercero==1006){valorÍndice=desfaseFin(valorÍndice);continue;}
        if(índiceTercero==1008||índiceTercero==1009){for(int índiceOrdinal=0;índiceOrdinal<númeroElementosFila-2;índiceOrdinal++)vertical(índiceTercero==1008?-1:1);continue;}
        if(insertar){
            if(índiceTercero==27||índiceTercero==3){insertar=0;continue;}
            if(índiceTercero==127||índiceTercero==8){if(valorÍndice)borrarContenidoBytes(elementoPrevio(valorÍndice),valorÍndice);continue;}
            if(índiceTercero==1007){if(valorÍndice<longitud)borrarContenidoBytes(valorÍndice,elementoListaSiguiente(valorÍndice));continue;}
            if(índiceTercero==13)índiceTercero=10;if(índiceTercero==10||índiceTercero==9||(índiceTercero>=32&&índiceTercero<256)){
                unsigned char valorSegundo[4];valorSegundo[0]=índiceTercero;int númeroElementosElementoLista=índiceTercero<128?1:índiceTercero>=0xc2&&índiceTercero<0xe0?2:índiceTercero<0xf0?3:índiceTercero<=0xf4?4:0;
                if(!númeroElementosElementoLista){textoNotificación="Invalid UTF-8";continue;}int válido=1;for(int índiceOrdinal=1;índiceOrdinal<númeroElementosElementoLista;índiceOrdinal++){int códigoCarácter=valorPulsado();if(códigoCarácter<128||códigoCarácter>191){teclaPendiente=códigoCarácter;válido=0;break;}valorSegundo[índiceOrdinal]=códigoCarácter;}
                if(válido)añadirFinalValor(valorSegundo,númeroElementosElementoLista);
            }continue;
        }
        if(partePrevio){int posiciónDatos=partePrevio;partePrevio=0;if(posiciónDatos=='g'&&índiceTercero=='g'){valorÍndice=0;continue;}if(posiciónDatos=='Z'&&índiceTercero=='Z'){programaTerminarSesión=valorAlmacenar();continue;}if((posiciónDatos=='d'&&índiceTercero=='d')||(posiciónDatos=='y'&&índiceTercero=='y')){int valorPrimero=ponerEnMarcha(valorÍndice),valorSegundo=desfaseFin(valorÍndice);if(valorSegundo<longitud)valorSegundo++;copiarLongitud=valorSegundo-valorPrimero;for(int índiceOrdinal=0;índiceOrdinal<copiarLongitud;índiceOrdinal++)datosCopiado[índiceOrdinal]=texto[valorPrimero+índiceOrdinal];if(posiciónDatos=='d')borrarContenidoBytes(valorPrimero,valorSegundo);continue;}}
        if(índiceTercero=='i'){insertar=1;continue;}if(índiceTercero=='a'){if(valorÍndice<desfaseFin(valorÍndice))valorÍndice=elementoListaSiguiente(valorÍndice);insertar=1;continue;}
        if(índiceTercero=='I'){valorÍndice=ponerEnMarcha(valorÍndice);insertar=1;continue;}if(índiceTercero=='A'){valorÍndice=desfaseFin(valorÍndice);insertar=1;continue;}
        if(índiceTercero=='o'||índiceTercero=='O'){unsigned char finLínea='\n';valorÍndice=índiceTercero=='o'?desfaseFin(valorÍndice):ponerEnMarcha(valorÍndice);if(añadirFinalValor(&finLínea,1)){if(índiceTercero=='O')valorÍndice--;insertar=1;}continue;}
        if(índiceTercero=='h'){valorÍndice=elementoPrevio(valorÍndice);continue;}if(índiceTercero=='l'){valorÍndice=elementoListaSiguiente(valorÍndice);continue;}if(índiceTercero=='j'){vertical(1);continue;}if(índiceTercero=='k'){vertical(-1);continue;}
        if(índiceTercero=='0'){valorÍndice=ponerEnMarcha(valorÍndice);continue;}if(índiceTercero=='$'){valorÍndice=desfaseFin(valorÍndice);continue;}if(índiceTercero=='G'){valorÍndice=ponerEnMarcha(longitud);continue;}
        if(índiceTercero=='g'||índiceTercero=='d'||índiceTercero=='y'||índiceTercero=='Z'){partePrevio=índiceTercero;continue;}
        if(índiceTercero=='x'||índiceTercero==1007){if(valorÍndice<longitud)borrarContenidoBytes(valorÍndice,elementoListaSiguiente(valorÍndice));continue;}
        if(índiceTercero=='p'&&copiarLongitud){valorÍndice=desfaseFin(valorÍndice);if(valorÍndice<longitud)valorÍndice++;añadirFinalValor(datosCopiado,copiarLongitud);continue;}
        if(índiceTercero=='u'&&deshacerPoseer){for(int índiceOrdinal=0;índiceOrdinal<capacidadEditor;índiceOrdinal++){unsigned char valorSegundo=texto[índiceOrdinal];texto[índiceOrdinal]=datosDeshacer[índiceOrdinal];datosDeshacer[índiceOrdinal]=valorSegundo;}int númeroElementosElementoLista=longitud;longitud=longitudDeshacer;longitudDeshacer=númeroElementosElementoLista;númeroElementosElementoLista=valorÍndice;valorÍndice=ladoSuperior;ladoSuperior=númeroElementosElementoLista;númeroElementosElementoLista=cambiadoEra;cambiadoEra=cambiosDeshacer;cambiosDeshacer=númeroElementosElementoLista;continue;}
        if(índiceTercero==':'||índiceTercero=='/'){programaTerminarSesión=indicadorEntrada(índiceTercero);continue;}if(índiceTercero=='n'){encontrarSiguiente();continue;}
    }
    emitirTexto("\033[0m\033[?25h\033[2J\033[H");vaciarBúfer();invocarUsuario(16,2,0,0,0,0,0);return 0;
}
