// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Inserción, borrado, flechas, historial y completado con Tab respetan los límites de bytes UTF-8. */
public final class EditorLínea {
    static boolean líneaComando;
    static int[] registroEntradaDiario = new int[16 * 1024], longitudDiario = new int[16], valorAlmacenar = new int[4096], candidato = new int[64];
    static int númeroElementosDiario, finRegistroEntradaDiario, buscarCoincidenciaValor, longitudAlmacenado, tamaño, valorCursor, númeroElementosCandidato, longitudCandidato, iniciarVentana;
    static boolean mostrarPosiciónHorizontal;
    static String listaComandos = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd intérpreteComandosAsegurar PresentarRemoto run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] candidatoComando = new int[128];
    static void añadirCandidatoComando(String listaEntradaElemento, int iniciarPosición, int posiciónFin, int longitudEntrada) {
        int númeroElementosByte=0;
        for(int índicePosición=iniciarPosición;índicePosición<posiciónFin;índicePosición++) {
            int códigoCarácter=listaEntradaElemento.charAt(índicePosición);
            if(códigoCarácter>=0xd800 && códigoCarácter<=0xdbff && índicePosición+1<posiciónFin)códigoCarácter=0x10000+((códigoCarácter-0xd800)<<10)+listaEntradaElemento.charAt(++índicePosición)-0xdc00;
            int númeroValor=códigoCarácter<128?1:códigoCarácter<2048?2:códigoCarácter<65536?3:4;
            if(númeroElementosByte+númeroValor>62)return;
            for(int valorSecuencia=númeroValor-1;valorSecuencia>=0;valorSecuencia--)candidatoComando[númeroElementosByte++]=númeroValor==1?códigoCarácter:valorSecuencia==númeroValor-1?(númeroValor==2?0xc0:númeroValor==3?0xe0:0xf0)|(códigoCarácter>>(6*valorSecuencia)):0x80|((códigoCarácter>>(6*valorSecuencia))&63);
        }
        if(númeroElementosByte<longitudEntrada)return;
        for(int índicePosición=0;índicePosición<longitudEntrada;índicePosición++)if(candidatoComando[índicePosición]!=IntérpreteComandos.línea[índicePosición])return;
        númeroElementosCandidato++;longitudCandidato=númeroElementosByte+1;
        for(int índicePosición=0;índicePosición<númeroElementosByte;índicePosición++)candidato[índicePosición]=candidatoComando[índicePosición];candidato[númeroElementosByte]=' ';
    }
    static int valorLadoDelantero(int leerCursor) { if (leerCursor > 0) { leerCursor--; while (leerCursor > 0 && (IntérpreteComandos.línea[leerCursor] & 192) == 128) leerCursor--; } return leerCursor; }
    static int valorLadoPosterior(int leerCursor) { if (leerCursor < tamaño) { leerCursor++; while (leerCursor < tamaño && (IntérpreteComandos.línea[leerCursor] & 192) == 128) leerCursor++; } return leerCursor; }
    static int extensiónRangoAnchura(int iniciarPosición, int índiceValorDestino) {
        int celdas = 0;
        for (int índiceBucle = iniciarPosición; índiceBucle < índiceValorDestino; índiceBucle++) { int datosByte = IntérpreteComandos.línea[índiceBucle]; if ((datosByte & 192) == 128) continue; celdas += datosByte >= 196 ? 2 : 1; }
        return celdas;
    }
    static void valorReintentar() {
        EntradaSalidaTerminal.escribir("\r\u001b[2K");
        EntradaSalidaTerminal.escribir(líneaComando ? "jkoros-native> " : "edit> ");
        líneasVisible();
    }
    // Moverse a izquierda y derecha dentro de una línea física. Redibujar una orden larga no debe borrar la salida superior.
    static int anchuraVisible() { int columnas = Placa.terminal(13) & 65535; return columnas - (líneaComando ? 18 : 9); }
    static void líneasVisible() {
        if (valorCursor < iniciarVentana) iniciarVentana = valorCursor;
        while (extensiónRangoAnchura(iniciarVentana, valorCursor) > anchuraVisible()) iniciarVentana = valorLadoPosterior(iniciarVentana);
        int posiciónFin = iniciarVentana;
        while (posiciónFin < tamaño && extensiónRangoAnchura(iniciarVentana, valorLadoPosterior(posiciónFin)) <= anchuraVisible()) posiciónFin = valorLadoPosterior(posiciónFin);
        EntradaSalidaTerminal.escribir("\r\u001b["); EntradaSalidaTerminal.númeroValor(líneaComando ? 16 : 7); EntradaSalidaTerminal.escribir("G\u001b[K");
        if (iniciarVentana > 0) EntradaSalidaTerminal.Caracteres('<');
        for (int índiceBucle = iniciarVentana; índiceBucle < posiciónFin; índiceBucle++) Placa.escribirSerie(IntérpreteComandos.línea[índiceBucle]);
        EntradaSalidaTerminal.Caracteres(posiciónFin < tamaño ? '>' : ' ');
        EntradaSalidaTerminal.escribir("\u001b["); EntradaSalidaTerminal.númeroValor(extensiónRangoAnchura(valorCursor, posiciónFin) + 1); EntradaSalidaTerminal.Caracteres('D');
        mostrarPosiciónHorizontal = iniciarVentana > 0 || posiciónFin < tamaño || extensiónRangoAnchura(0, tamaño) > anchuraVisible();
    }
    static void añadirFinalDiario() {
        if (!líneaComando || tamaño == 0 || tamaño > 1024) return;
        if (númeroElementosDiario > 0) {
            int posiciónÚltimo = (finRegistroEntradaDiario + 15) % 16; boolean esMismo = longitudDiario[posiciónÚltimo] == tamaño;
            for (int índiceBucle = 0; esMismo && índiceBucle < tamaño; índiceBucle++) if (registroEntradaDiario[posiciónÚltimo * 1024 + índiceBucle] != IntérpreteComandos.línea[índiceBucle]) esMismo = false;
            if (esMismo) return;
        }
        longitudDiario[finRegistroEntradaDiario] = tamaño; for (int índiceBucle = 0; índiceBucle < tamaño; índiceBucle++) registroEntradaDiario[finRegistroEntradaDiario * 1024 + índiceBucle] = IntérpreteComandos.línea[índiceBucle];
        finRegistroEntradaDiario = (finRegistroEntradaDiario + 1) % 16; if (númeroElementosDiario < 16) númeroElementosDiario++;
    }
    static void movimientoDiario(int valorVariación) {
        if (!líneaComando) return;
        if (buscarCoincidenciaValor == 0 && valorVariación > 0) { longitudAlmacenado = tamaño; for (int índiceBucle = 0; índiceBucle < tamaño; índiceBucle++) valorAlmacenar[índiceBucle] = IntérpreteComandos.línea[índiceBucle]; }
        int posiciónSiguiente = buscarCoincidenciaValor + valorVariación; if (posiciónSiguiente < 0 || posiciónSiguiente > númeroElementosDiario) return; buscarCoincidenciaValor = posiciónSiguiente;
        if (buscarCoincidenciaValor == 0) { tamaño = longitudAlmacenado; for (int índiceBucle = 0; índiceBucle < tamaño; índiceBucle++) IntérpreteComandos.línea[índiceBucle] = valorAlmacenar[índiceBucle]; }
        else { int ranuraPreservado = (finRegistroEntradaDiario + 16 - buscarCoincidenciaValor) % 16; tamaño = longitudDiario[ranuraPreservado]; for (int índiceBucle = 0; índiceBucle < tamaño; índiceBucle++) IntérpreteComandos.línea[índiceBucle] = registroEntradaDiario[ranuraPreservado * 1024 + índiceBucle]; }
        valorCursor = tamaño; valorReintentar();
    }
    static void mostrarDiario() {
        for (int númeroElementosEntradaElemento = 0; númeroElementosEntradaElemento < númeroElementosDiario; númeroElementosEntradaElemento++) {
            int ranuraPreservado = (finRegistroEntradaDiario + 16 - númeroElementosDiario + númeroElementosEntradaElemento) % 16; EntradaSalidaTerminal.númeroValor(númeroElementosEntradaElemento + 1); EntradaSalidaTerminal.escribir("  ");
            for (int índiceBucle = 0; índiceBucle < longitudDiario[ranuraPreservado]; índiceBucle++) Placa.escribirSerie(registroEntradaDiario[ranuraPreservado * 1024 + índiceBucle]); EntradaSalidaTerminal.Caracteres(10);
        }
    }
    static void añadirCandidato(int[] arregloDatos, int iniciarPosición, int númeroElementosEntradaElemento, int prefijo, int númeroElementosTotal, boolean númeroDirectorio) {
        if (númeroElementosEntradaElemento < númeroElementosTotal || númeroElementosEntradaElemento > 62) return;
        for (int índiceBucle = 0; índiceBucle < númeroElementosTotal; índiceBucle++) if (arregloDatos[iniciarPosición + índiceBucle] != IntérpreteComandos.línea[prefijo + índiceBucle]) return;
        númeroElementosCandidato++; longitudCandidato = númeroElementosEntradaElemento + 1;
        for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) candidato[índiceBucle] = arregloDatos[iniciarPosición + índiceBucle]; candidato[númeroElementosEntradaElemento] = númeroDirectorio ? '/' : ' ';
    }
    static void valorCompletado() {
        if (!líneaComando || valorCursor != tamaño) return;
        int puntoInicial = tamaño; while (puntoInicial > 0 && IntérpreteComandos.línea[puntoInicial - 1] != ' ') puntoInicial--;
        for (int índiceBucle = puntoInicial; índiceBucle < tamaño; índiceBucle++) if (IntérpreteComandos.línea[índiceBucle] == '/' || IntérpreteComandos.línea[índiceBucle] == '"' || IntérpreteComandos.línea[índiceBucle] == 39 || IntérpreteComandos.línea[índiceBucle] == '\\') return;
        númeroElementosCandidato = 0; int númeroElementosEntradaElemento = tamaño - puntoInicial;
        if (puntoInicial == 0) {
            for(int índiceLista=0;índiceLista<2;índiceLista++) {
                String listaEntradaElemento=índiceLista==0?listaComandos:ComandosAdministración.palabraCompletado();
                int leerCursor=0;
                while(leerCursor<listaEntradaElemento.length()) {
                    int posiciónFin=leerCursor;while(posiciónFin<listaEntradaElemento.length() && listaEntradaElemento.charAt(posiciónFin)!=' ')posiciónFin++;
                    añadirCandidatoComando(listaEntradaElemento,leerCursor,posiciónFin,númeroElementosEntradaElemento);leerCursor=posiciónFin+1;
                }
            }
        } else {
            ArchivosMemoria.iniciarRuta(1); ArchivosMemoria.byteRuta(0, '.'); ArchivosMemoria.normalizarValor();
            for (int índiceBucle = 0; índiceBucle < ArchivosMemoria.númeroElementosArchivo; índiceBucle++) {
                int iniciarPosición = ArchivosMemoria.iniciarEntradaElemento(ArchivosMemoria.nombre, índiceBucle * 64, ArchivosMemoria.longitudNombre[índiceBucle]);
                if (iniciarPosición >= 0) añadirCandidato(ArchivosMemoria.nombre, índiceBucle * 64 + iniciarPosición, ArchivosMemoria.longitudNombre[índiceBucle] - iniciarPosición, puntoInicial, númeroElementosEntradaElemento, false);
            }
            for (int índiceBucle = 0; índiceBucle < 16; índiceBucle++) {
                int iniciarPosición = ArchivosMemoria.iniciarEntradaElemento(ArchivosMemoria.nombreDirectorio, índiceBucle * 64, ArchivosMemoria.longitudDirectorio[índiceBucle]);
                if (iniciarPosición >= 0) añadirCandidato(ArchivosMemoria.nombreDirectorio, índiceBucle * 64 + iniciarPosición, ArchivosMemoria.longitudDirectorio[índiceBucle] - iniciarPosición, puntoInicial, númeroElementosEntradaElemento, true);
            }
        }
        if (númeroElementosCandidato != 1) { Placa.escribirSerie(7); return; }
        for (int índiceBucle = númeroElementosEntradaElemento; índiceBucle < longitudCandidato && tamaño < IntérpreteComandos.línea.length - 1; índiceBucle++) {
            if (candidato[índiceBucle] == ' ' && índiceBucle != longitudCandidato - 1) IntérpreteComandos.línea[tamaño++] = '\\';
            IntérpreteComandos.línea[tamaño++] = candidato[índiceBucle];
        }
        valorCursor = tamaño; valorReintentar();
    }
    static int leerEscapar() {
        int puntoInicial = Placa.milisegundos();
        while (Placa.milisegundos() - puntoInicial < 80) { int datosByte = Placa.leerSerie(); if (datosByte >= 0) return datosByte; Placa.cederProcesador(); }
        return -1;
    }
    static void valorEscapar() {
        int primero = leerEscapar(); if (primero != '[' && primero != 'O') return;
        int númeroElementosEntradaElemento = 0, posiciónFin = -1;
        for (int índiceBucle = 0; índiceBucle < 12; índiceBucle++) { int datosByte = leerEscapar(); if (datosByte < 0) return; if (datosByte >= '0' && datosByte <= '9') númeroElementosEntradaElemento = númeroElementosEntradaElemento * 10 + datosByte - '0'; else { posiciónFin = datosByte; break; } }
        if (posiciónFin == 'A') movimientoDiario(1);
        else if (posiciónFin == 'B') movimientoDiario(-1);
        else if (posiciónFin == 'C') { valorCursor = valorLadoPosterior(valorCursor); valorReintentar(); }
        else if (posiciónFin == 'D') { valorCursor = valorLadoDelantero(valorCursor); valorReintentar(); }
        else if (posiciónFin == 'H' || posiciónFin == '~' && (númeroElementosEntradaElemento == 1 || númeroElementosEntradaElemento == 7)) { valorCursor = 0; valorReintentar(); }
        else if (posiciónFin == 'F' || posiciónFin == '~' && (númeroElementosEntradaElemento == 4 || númeroElementosEntradaElemento == 8)) { valorCursor = tamaño; valorReintentar(); }
        else if (posiciónFin == '~' && númeroElementosEntradaElemento == 3 && valorCursor < tamaño) {
            int posiciónSiguiente = valorLadoPosterior(valorCursor); for (int índiceBucle = posiciónSiguiente; índiceBucle < tamaño; índiceBucle++) IntérpreteComandos.línea[índiceBucle - posiciónSiguiente + valorCursor] = IntérpreteComandos.línea[índiceBucle]; tamaño -= posiciónSiguiente - valorCursor; valorReintentar();
        }
        else if (posiciónFin == '~' && (númeroElementosEntradaElemento == 5 || númeroElementosEntradaElemento == 6)) Placa.terminal(númeroElementosEntradaElemento == 5 ? 5 : 6);
        else if (posiciónFin == '~' && númeroElementosEntradaElemento == 24 && líneaComando) { IntérpreteComandos.terminal(true); }
    }
    static int leer() {
        if (!sesiónVentana.leerContinuación) { tamaño = valorCursor = buscarCoincidenciaValor = iniciarVentana = 0; mostrarPosiciónHorizontal = false; }
        else { sesiónVentana.leerContinuación = false; valorReintentar(); } boolean desbordamiento = false;
        while (true) {
            int datosByte = Placa.leerSerie(); if (datosByte == -4096) return -3;
            if (Placa.terminal(14) != 0) valorReintentar(); if (datosByte < 0) { Placa.cederProcesador(); continue; }
            if (datosByte == 10 && IntérpreteComandos.líneaElementoPrevio) { IntérpreteComandos.líneaElementoPrevio = false; continue; } IntérpreteComandos.líneaElementoPrevio = datosByte == 13;
            if (datosByte == 27) { valorEscapar(); continue; }
            if (datosByte == 3) { EntradaSalidaTerminal.escribir("^C\n"); return -1; }
            if (datosByte == 4 && tamaño == 0 && líneaComando) { if (Placa.terminal(2) != 0) IntérpreteComandos.terminal(true); return -1; }
            if (datosByte == 13 || datosByte == 10) { EntradaSalidaTerminal.Caracteres(10); if (!desbordamiento) añadirFinalDiario(); return desbordamiento ? -2 : tamaño; }
            if (datosByte == 9 && líneaComando) { valorCompletado(); continue; }
            if (datosByte == 1 || datosByte == 5) { valorCursor = datosByte == 1 ? 0 : tamaño; valorReintentar(); continue; }
            if (datosByte == 8 || datosByte == 127 || datosByte == 21) {
                if (datosByte == 21) { for (int índiceBucle = valorCursor; índiceBucle < tamaño; índiceBucle++) IntérpreteComandos.línea[índiceBucle - valorCursor] = IntérpreteComandos.línea[índiceBucle]; tamaño -= valorCursor; valorCursor = 0; }
                else if (valorCursor > 0) { int cambiarAntes = valorLadoDelantero(valorCursor); for (int índiceBucle = valorCursor; índiceBucle < tamaño; índiceBucle++) IntérpreteComandos.línea[índiceBucle - valorCursor + cambiarAntes] = IntérpreteComandos.línea[índiceBucle]; tamaño -= valorCursor - cambiarAntes; valorCursor = cambiarAntes; }
                valorReintentar(); continue;
            }
            if (datosByte == 11) { tamaño = valorCursor; valorReintentar(); continue; }
            if (datosByte < 32 && datosByte != 9) continue;
            if (tamaño == IntérpreteComandos.línea.length) { desbordamiento = true; continue; }
            for (int índiceBucle = tamaño; índiceBucle > valorCursor; índiceBucle--) IntérpreteComandos.línea[índiceBucle] = IntérpreteComandos.línea[índiceBucle - 1];
            IntérpreteComandos.línea[valorCursor++] = datosByte; tamaño++;
            if (valorCursor == tamaño && !mostrarPosiciónHorizontal && extensiónRangoAnchura(0, tamaño) <= anchuraVisible()) Placa.escribirSerie(datosByte);
            else if (valorCursor == tamaño) líneasVisible(); else valorReintentar();
        }
    }
}
