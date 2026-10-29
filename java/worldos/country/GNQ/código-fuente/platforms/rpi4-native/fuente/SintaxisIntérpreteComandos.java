// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Gramática interactiva restringida. Las tuberías se ejecutan en secuencia; el entorno se comparte en el mismo intérprete. */
public final class SintaxisIntérpreteComandos {
    static int[] fuente = new int[4 * 4096], valorClaseTipo = new int[4 * 128], ponerEnMarcha = new int[4 * 128], terminación = new int[4 * 128];
    static int[] nombreVariable = new int[16 * 32], datosVariable = new int[16 * 256], longitudNombre = new int[16], longitudValor = new int[16];
    static int[] valorGuion = new int[4 * 16384];
    static int valorEstadoValor, valorProfundidad, escrito;
    static boolean esConexiónEnCurso, finGuion, errorExtensión;
    static boolean carácterNombre(int códigoCarácter) { return códigoCarácter >= 'a' && códigoCarácter <= 'z' || códigoCarácter >= 'A' && códigoCarácter <= 'Z' || códigoCarácter == '_' || códigoCarácter >= 128; }
    static boolean sufijoNombre(int códigoCarácter) { return carácterNombre(códigoCarácter) || códigoCarácter >= '0' && códigoCarácter <= '9'; }
    static void error(String texto) { Placa.entradaSalidaConmutar(0); EntradaSalidaTerminal.escribir("comando analizarValor: "); EntradaSalidaTerminal.escribir(texto); EntradaSalidaTerminal.Caracteres(10); valorEstadoValor = 2; }
    static int leer(int númeroElementosEntradaElemento, int profundidad) {
        int índiceActual = 0, númeroElementosTotal = 0, posiciónBase = profundidad * 4096, carácterEspecial = profundidad * 128;
        while (índiceActual < númeroElementosEntradaElemento) {
            while (índiceActual < númeroElementosEntradaElemento && (fuente[posiciónBase + índiceActual] == 32 || fuente[posiciónBase + índiceActual] == 9)) índiceActual++;
            if (índiceActual == númeroElementosEntradaElemento || fuente[posiciónBase + índiceActual] == '#') break;
            if (númeroElementosTotal == 128) { error("낱말이 너무 많습니다"); return -1; }
            int iniciarPosición = índiceActual, códigoCarácter = fuente[posiciónBase + índiceActual], claseTipoDatos = 0;
            if (códigoCarácter == ';') { claseTipoDatos = 1; índiceActual++; }
            else if (códigoCarácter == '&') { if (índiceActual + 1 >= númeroElementosEntradaElemento || fuente[posiciónBase + índiceActual + 1] != '&') { error("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } claseTipoDatos = 2; índiceActual += 2; }
            else if (códigoCarácter == '|') { índiceActual++; claseTipoDatos = índiceActual < númeroElementosEntradaElemento && fuente[posiciónBase + índiceActual] == '|' ? 3 : 4; if (claseTipoDatos == 3) índiceActual++; }
            else if (códigoCarácter == '>') { índiceActual++; claseTipoDatos = índiceActual < númeroElementosEntradaElemento && fuente[posiciónBase + índiceActual] == '>' ? 6 : 5; if (claseTipoDatos == 6) índiceActual++; }
            else if (códigoCarácter == '<') { claseTipoDatos = 7; índiceActual++; }
            else {
                int comilla = 0;
                while (índiceActual < númeroElementosEntradaElemento) {
                    códigoCarácter = fuente[posiciónBase + índiceActual];
                    if (códigoCarácter == '`' && comilla != 39 || códigoCarácter == '$' && comilla != 39 && índiceActual + 1 < númeroElementosEntradaElemento && fuente[posiciónBase + índiceActual + 1] == '(') { error("comando resultado 치환은 지원하지 않습니다"); return -1; }
                    if (códigoCarácter == '\\' && comilla != 39) { if (++índiceActual == númeroElementosEntradaElemento) { error("línea 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } índiceActual++; continue; }
                    if (códigoCarácter == comilla) { comilla = 0; índiceActual++; continue; }
                    if (comilla == 0 && (códigoCarácter == 39 || códigoCarácter == 34)) { comilla = códigoCarácter; índiceActual++; continue; }
                    if (comilla == 0 && (códigoCarácter == 32 || códigoCarácter == 9 || códigoCarácter == ';' || códigoCarácter == '&' || códigoCarácter == '|' || códigoCarácter == '<' || códigoCarácter == '>')) break;
                    índiceActual++;
                }
                if (comilla != 0) { error("따옴표가 닫히지 않았습니다"); return -1; }
                if (índiceActual < númeroElementosEntradaElemento && (fuente[posiciónBase + índiceActual] == '>' || fuente[posiciónBase + índiceActual] == '<')) {
                    boolean valorNumérico = índiceActual > iniciarPosición;
                    for (int índiceBucle = iniciarPosición; índiceBucle < índiceActual; índiceBucle++) if (fuente[posiciónBase + índiceBucle] < '0' || fuente[posiciónBase + índiceBucle] > '9') valorNumérico = false;
                    if (valorNumérico) { error("번호를 지정한 Archivo entradaElementoDescriptor salidaEntrada 전환은 지원하지 않습니다"); return -1; }
                }
            }
            valorClaseTipo[carácterEspecial + númeroElementosTotal] = claseTipoDatos; ponerEnMarcha[carácterEspecial + númeroElementosTotal] = iniciarPosición; terminación[carácterEspecial + númeroElementosTotal] = índiceActual; númeroElementosTotal++;
        }
        boolean palabraLéxico = false;
        for (int índiceBucle = 0; índiceBucle < númeroElementosTotal; índiceBucle++) {
            int datosTemporal = valorClaseTipo[carácterEspecial + índiceBucle];
            if (datosTemporal == 0) palabraLéxico = true;
            else if (datosTemporal >= 5) { if (++índiceBucle == númeroElementosTotal || valorClaseTipo[carácterEspecial + índiceBucle] != 0) { error("salidaEntrada 전환에 Archivo 이름이 필요합니다"); return -1; } }
            else { if (!palabraLéxico || índiceBucle == númeroElementosTotal - 1 && datosTemporal != 1) { error("명령이 빠졌습니다"); return -1; } palabraLéxico = false; }
        }
        if (númeroElementosTotal > 0 && !palabraLéxico && valorClaseTipo[carácterEspecial + númeroElementosTotal - 1] != 1) { error("명령이 빠졌습니다"); return -1; }
        return númeroElementosTotal;
    }
    static boolean textoRango(int[] arregloDatos, int iniciarLocal, int númeroElementosEntradaElemento, String posiciónCarácter) {
        if (númeroElementosEntradaElemento != posiciónCarácter.length()) return false; for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) if (arregloDatos[iniciarLocal + índiceBucle] != posiciónCarácter.charAt(índiceBucle)) return false; return true;
    }
    static void ponerValor(int datosByte) {
        if (escrito >= IntérpreteComandos.valorTokenLéxico.length) { if (!errorExtensión) error("변수를 펼친 명령이 너무 깁니다"); errorExtensión = true; return; }
        IntérpreteComandos.valorTokenLéxico[escrito++] = datosByte;
    }
    static void valorVariable(int[] arregloDatos, int iniciarPosición, int númeroElementosEntradaElemento) {
        if (textoRango(arregloDatos, iniciarPosición, númeroElementosEntradaElemento, "PWD")) { ponerValor('/'); for (int índiceBucle = 0; índiceBucle < ArchivosMemoria.longitudActual; índiceBucle++) ponerValor(ArchivosMemoria.elementoListaActual[índiceBucle]); return; }
        if (textoRango(arregloDatos, iniciarPosición, númeroElementosEntradaElemento, "HOME")) { ponerValor('/'); return; }
        if (textoRango(arregloDatos, iniciarPosición, númeroElementosEntradaElemento, "?")) {
            int valorDatos = valorEstadoValor, dígito = 100; boolean tieneIniciado = false;
            while (dígito > 0) { int valorPosiciónFinal = valorDatos / dígito; if (valorPosiciónFinal != 0 || tieneIniciado || dígito == 1) { ponerValor('0' + valorPosiciónFinal); tieneIniciado = true; } valorDatos %= dígito; dígito /= 10; } return;
        }
        for (int índiceBucle = 0; índiceBucle < 16; índiceBucle++) if (longitudNombre[índiceBucle] == númeroElementosEntradaElemento) {
            boolean coincide = true; for (int posiciónInterior = 0; posiciónInterior < númeroElementosEntradaElemento; posiciónInterior++) if (nombreVariable[índiceBucle * 32 + posiciónInterior] != arregloDatos[iniciarPosición + posiciónInterior]) coincide = false;
            if (coincide) { for (int posiciónInterior = 0; posiciónInterior < longitudValor[índiceBucle]; posiciónInterior++) ponerValor(datosVariable[índiceBucle * 256 + posiciónInterior]); return; }
        }
    }
    static boolean valorPalabra(int índicePalabraLéxico, int profundidad) {
        int leerCursor = ponerEnMarcha[profundidad * 128 + índicePalabraLéxico], posiciónFin = terminación[profundidad * 128 + índicePalabraLéxico], posiciónBase = profundidad * 4096, comilla = 0;
        if (leerCursor < posiciónFin && fuente[posiciónBase + leerCursor] == '~' && (leerCursor + 1 == posiciónFin || fuente[posiciónBase + leerCursor + 1] == '/')) { ponerValor('/'); leerCursor++; }
        while (leerCursor < posiciónFin) {
            int códigoCarácter = fuente[posiciónBase + leerCursor++];
            if (códigoCarácter == comilla) { comilla = 0; continue; }
            if (comilla == 0 && (códigoCarácter == 39 || códigoCarácter == 34)) { comilla = códigoCarácter; continue; }
            if (códigoCarácter == '\\' && comilla != 39) { int posiciónSiguiente = fuente[posiciónBase + leerCursor++]; if (comilla == 34 && posiciónSiguiente != '$' && posiciónSiguiente != '"' && posiciónSiguiente != '\\') ponerValor('\\'); ponerValor(posiciónSiguiente); continue; }
            if (códigoCarácter == '$' && comilla != 39 && leerCursor < posiciónFin) {
                boolean llave = fuente[posiciónBase + leerCursor] == '{'; if (llave) leerCursor++;
                int inicioPosición = leerCursor;
                if (leerCursor < posiciónFin && fuente[posiciónBase + leerCursor] == '?') leerCursor++;
                else while (leerCursor < posiciónFin && sufijoNombre(fuente[posiciónBase + leerCursor])) leerCursor++;
                if (llave && (leerCursor == posiciónFin || fuente[posiciónBase + leerCursor] != '}')) { error("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (leerCursor == inicioPosición && !llave) { ponerValor('$'); continue; }
                valorVariable(fuente, posiciónBase + inicioPosición, leerCursor - inicioPosición); if (llave) leerCursor++; continue;
            }
            ponerValor(códigoCarácter);
        }
        return !errorExtensión;
    }
    static int ajustesEntorno(int índiceArgumento, boolean eliminar) {
        int iniciarLocal = IntérpreteComandos.puntoInicial[índiceArgumento], posiciónFin = iniciarLocal + IntérpreteComandos.longitud[índiceArgumento], posiciónIgualdad = iniciarLocal;
        while (posiciónIgualdad < posiciónFin && IntérpreteComandos.valorTokenLéxico[posiciónIgualdad] != '=') posiciónIgualdad++;
        int númeroElementosEntradaElemento = posiciónIgualdad - iniciarLocal;
        if (númeroElementosEntradaElemento < 1 || númeroElementosEntradaElemento > 31 || !carácterNombre(IntérpreteComandos.valorTokenLéxico[iniciarLocal]) || !eliminar && posiciónIgualdad == posiciónFin || posiciónFin - posiciónIgualdad - 1 > 255) return 2;
        for (int índiceBucle = iniciarLocal; índiceBucle < posiciónIgualdad; índiceBucle++) if (!sufijoNombre(IntérpreteComandos.valorTokenLéxico[índiceBucle])) return 2;
        if (textoRango(IntérpreteComandos.valorTokenLéxico, iniciarLocal, númeroElementosEntradaElemento, "PWD") || textoRango(IntérpreteComandos.valorTokenLéxico, iniciarLocal, númeroElementosEntradaElemento, "HOME")) return 2;
        int encontradoEra = -1, esEstadoValorVacíoEstado = -1;
        for (int índiceBucle = 0; índiceBucle < 16; índiceBucle++) {
            if (longitudNombre[índiceBucle] == 0) esEstadoValorVacíoEstado = índiceBucle;
            if (longitudNombre[índiceBucle] != númeroElementosEntradaElemento) continue;
            boolean coincide = true; for (int posiciónInterior = 0; posiciónInterior < númeroElementosEntradaElemento; posiciónInterior++) if (nombreVariable[índiceBucle * 32 + posiciónInterior] != IntérpreteComandos.valorTokenLéxico[iniciarLocal + posiciónInterior]) coincide = false;
            if (coincide) encontradoEra = índiceBucle;
        }
        if (eliminar) { if (encontradoEra >= 0) longitudNombre[encontradoEra] = 0; return 0; }
        if (encontradoEra < 0) encontradoEra = esEstadoValorVacíoEstado; if (encontradoEra < 0) return 1;
        longitudNombre[encontradoEra] = númeroElementosEntradaElemento; longitudValor[encontradoEra] = posiciónFin - posiciónIgualdad - 1;
        for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) nombreVariable[encontradoEra * 32 + índiceBucle] = IntérpreteComandos.valorTokenLéxico[iniciarLocal + índiceBucle];
        for (int índiceBucle = posiciónIgualdad + 1; índiceBucle < posiciónFin; índiceBucle++) datosVariable[encontradoEra * 256 + índiceBucle - posiciónIgualdad - 1] = IntérpreteComandos.valorTokenLéxico[índiceBucle];
        return 0;
    }
    static void mostrarEntorno() {
        EntradaSalidaTerminal.escribir("HOME=/\nPWD="); ArchivosMemoria.escribirActual(); EntradaSalidaTerminal.Caracteres(10);
        for (int índiceBucle = 0; índiceBucle < 16; índiceBucle++) if (longitudNombre[índiceBucle] > 0) {
            for (int posiciónInterior = 0; posiciónInterior < longitudNombre[índiceBucle]; posiciónInterior++) Placa.escribirSerie(nombreVariable[índiceBucle * 32 + posiciónInterior]); EntradaSalidaTerminal.Caracteres('=');
            for (int posiciónInterior = 0; posiciónInterior < longitudValor[índiceBucle]; posiciónInterior++) Placa.escribirSerie(datosVariable[índiceBucle * 256 + posiciónInterior]); EntradaSalidaTerminal.Caracteres(10);
        }
    }
    static void ejecutarComando(int[] arregloDatos, int iniciarDesplazamiento, int númeroElementosEntradaElemento, int profundidad) {
        if (profundidad >= 4 || númeroElementosEntradaElemento > 4096) { error("comando 파일의 valorAnidamiento 또는 línea longitud 제한을 넘었습니다"); return; }
        for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) fuente[profundidad * 4096 + índiceBucle] = arregloDatos[iniciarDesplazamiento + índiceBucle];
        int númeroElementosTotal = leer(númeroElementosEntradaElemento, profundidad); if (númeroElementosTotal < 0) return;
        int leerCursor = 0, cumplidoCondición = 1;
        while (leerCursor < númeroElementosTotal) {
            int finGrupo = leerCursor;
            while (finGrupo < númeroElementosTotal && (valorClaseTipo[profundidad * 128 + finGrupo] == 0 || valorClaseTipo[profundidad * 128 + finGrupo] >= 4)) finGrupo++;
            boolean ejecutar = cumplidoCondición == 1 || cumplidoCondición == 2 && valorEstadoValor == 0 || cumplidoCondición == 3 && valorEstadoValor != 0;
            if (ejecutar) {
                boolean índiceElementoListaElementoPrevio = false;
                while (leerCursor < finGrupo) {
                    int posiciónSiguiente = leerCursor; while (posiciónSiguiente < finGrupo && valorClaseTipo[profundidad * 128 + posiciónSiguiente] != 4) posiciónSiguiente++;
                    boolean conectarFlujo = posiciónSiguiente < finGrupo; int páginaEntrada = -1, páginaSalida = -1, modoSaliente = 0;
                    IntérpreteComandos.númeroElementosTokenLéxico = 0; escrito = 0; errorExtensión = false;
                    for (int índiceBucle = leerCursor; índiceBucle < posiciónSiguiente; índiceBucle++) {
                        int claseTipoDatos = valorClaseTipo[profundidad * 128 + índiceBucle];
                        if (claseTipoDatos >= 5) { if (claseTipoDatos == 7) { if (páginaEntrada >= 0) { error("valorEntrada 전환이 겹쳤습니다"); return; } páginaEntrada = ++índiceBucle; } else { if (páginaSalida >= 0) { error("Salida 전환이 겹쳤습니다"); return; } páginaSalida = ++índiceBucle; modoSaliente = claseTipoDatos; } continue; }
                        if (IntérpreteComandos.númeroElementosTokenLéxico == 32) { error("인수가 너무 많습니다"); return; }
                        int índiceArgumento = IntérpreteComandos.númeroElementosTokenLéxico++; IntérpreteComandos.puntoInicial[índiceArgumento] = escrito;
                        if (!valorPalabra(índiceBucle, profundidad)) return;
                        IntérpreteComandos.longitud[índiceArgumento] = escrito - IntérpreteComandos.puntoInicial[índiceArgumento];
                    }
                    esConexiónEnCurso = índiceElementoListaElementoPrevio || conectarFlujo || páginaEntrada >= 0 || páginaSalida >= 0;
                    if (esConexiónEnCurso && (IntérpreteComandos.textoIgual(0, "vi") || IntérpreteComandos.textoIgual(0, "edit") || IntérpreteComandos.textoIgual(0, "load") || IntérpreteComandos.textoIgual(0, "gui") || IntérpreteComandos.textoIgual(0, "terminal") || IntérpreteComandos.textoIgual(0, "sh") || IntérpreteComandos.textoIgual(0, "source"))) { error("interactivo 명령과 comando 파일은 salidaEntrada 전환이나 valorFlujo 연결에 쓸 númeroValor 없습니다"); return; }
                    EntradaSalidaIntérpreteComandos.ponerEnMarcha(índiceElementoListaElementoPrevio, conectarFlujo);
                    for (int redirección = 0; redirección < 2; redirección++) {
                        int posiciónEntradaElemento = redirección == 0 ? páginaEntrada : páginaSalida; if (posiciónEntradaElemento < 0) continue;
                        int iniciarPosición = escrito; if (!valorPalabra(posiciónEntradaElemento, profundidad)) { EntradaSalidaIntérpreteComandos.terminación(); return; }
                        int valorProcesado = ArchivosMemoria.iniciarRuta(escrito - iniciarPosición);
                        for (int posiciónInterior = iniciarPosición; valorProcesado >= 0 && posiciónInterior < escrito; posiciónInterior++) valorProcesado = ArchivosMemoria.byteRuta(posiciónInterior - iniciarPosición, IntérpreteComandos.valorTokenLéxico[posiciónInterior]);
                        if (valorProcesado >= 0) valorProcesado = ArchivosMemoria.abrir(redirección == 0 ? 0 : modoSaliente == 6 ? 1089 : 577);
                        if (valorProcesado < 0) { EntradaSalidaIntérpreteComandos.terminación(); IntérpreteComandos.error(valorProcesado); valorEstadoValor = 1; return; }
                        if (redirección == 0) EntradaSalidaIntérpreteComandos.archivoEntrada = valorProcesado; else EntradaSalidaIntérpreteComandos.archivoSalida = valorProcesado;
                    }
                    EntradaSalidaIntérpreteComandos.permitirInteractivo = profundidad == 0 && leerCursor == 0 && posiciónSiguiente == númeroElementosTotal;
                    valorProfundidad = profundidad; IntérpreteComandos.resultado = 0; Placa.entradaSalidaConmutar(1);
                    IntérpreteComandos.comando();
                    Placa.terminal(3);
                    int valorDevuelto = IntérpreteComandos.resultado, errorFlujo = EntradaSalidaIntérpreteComandos.valorFallo;
                    EntradaSalidaIntérpreteComandos.terminación(); esConexiónEnCurso = false;
                    valorEstadoValor = errorFlujo < 0 ? 1 : valorDevuelto;
                    if (errorFlujo < 0) { IntérpreteComandos.error(errorFlujo); return; }
                    if (finGuion || valorDevuelto == -1005) return;
                    índiceElementoListaElementoPrevio = true; leerCursor = posiciónSiguiente + 1;
                }
            }
            if (finGrupo < númeroElementosTotal) cumplidoCondición = valorClaseTipo[profundidad * 128 + finGrupo];
            leerCursor = finGrupo + 1;
        }
    }
    static void ejecutarArchivo() {
        if (IntérpreteComandos.númeroElementosTokenLéxico != 2 || valorProfundidad >= 3) { IntérpreteComandos.resultado = 2; EntradaSalidaTerminal.escribir("사용법: sh Archivo (valorAnidamiento valorProfundidad <= 3)\n"); return; }
        int profundidad = valorProfundidad + 1, valorProcesado = IntérpreteComandos.ruta(1); if (valorProcesado >= 0) valorProcesado = ArchivosMemoria.abrir(0);
        if (valorProcesado < 0) { IntérpreteComandos.error(valorProcesado); return; }
        int númeroElementosEntradaElemento = 0, datosByte;
        while ((datosByte = ArchivosMemoria.leer(valorProcesado)) != 256 && datosByte >= 0 && númeroElementosEntradaElemento < 16384) valorGuion[profundidad * 16384 + númeroElementosEntradaElemento++] = datosByte;
        ArchivosMemoria.cerrar(valorProcesado); Placa.entradaSalidaConmutar(0);
        for (int leerCursor = 0; leerCursor < númeroElementosEntradaElemento && !finGuion;) {
            int posiciónFin = leerCursor; while (posiciónFin < númeroElementosEntradaElemento && valorGuion[profundidad * 16384 + posiciónFin] != 10) posiciónFin++;
            int longitudVálido = posiciónFin - leerCursor; if (longitudVálido > 0 && valorGuion[profundidad * 16384 + posiciónFin - 1] == 13) longitudVálido--;
            ejecutarComando(valorGuion, profundidad * 16384 + leerCursor, longitudVálido, profundidad); leerCursor = posiciónFin + 1;
        }
        IntérpreteComandos.resultado = valorEstadoValor; finGuion = false; valorProfundidad = profundidad - 1;
    }
}
