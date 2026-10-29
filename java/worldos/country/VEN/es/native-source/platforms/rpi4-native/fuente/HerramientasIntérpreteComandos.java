// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Herramientas integradas del intérprete que comparten RAM VFS y entrada/salida estándar. */
public final class HerramientasIntérpreteComandos {
    static int[] Datos = new int[16384];
    static int archivoEntrada = -1;
    static int abrirArchivo(int índiceArgumento, int modoProceso) {
        int valorProcesado = IntérpreteComandos.ruta(índiceArgumento); return valorProcesado < 0 ? valorProcesado : ArchivosMemoria.abrir(modoProceso);
    }
    static boolean prepararEntrada(int índiceArgumento) {
        archivoEntrada = -1;
        if (índiceArgumento < IntérpreteComandos.númeroElementosTokenLéxico) {
            archivoEntrada = abrirArchivo(índiceArgumento, 0);
            if (archivoEntrada < 0) { IntérpreteComandos.error(archivoEntrada); return false; }
        }
        return true;
    }
    static int leer() {
        if (archivoEntrada >= 3) return ArchivosMemoria.leer(archivoEntrada);
        while (true) {
            int datosByte = Placa.leerSerie(); if (datosByte == -2 || datosByte == 4) return 256;
            if (datosByte == 3) { IntérpreteComandos.resultado = 130; return 256; }
            if (datosByte >= 0) return datosByte; Placa.cederProcesador();
        }
    }
    static void cerrar() { if (archivoEntrada >= 3) ArchivosMemoria.cerrar(archivoEntrada); archivoEntrada = -1; }
    static void valorVista() {
        int posiciónÚltimo = IntérpreteComandos.númeroElementosTokenLéxico == 1 ? 2 : IntérpreteComandos.númeroElementosTokenLéxico;
        for (int índiceArgumento = 1; índiceArgumento < posiciónÚltimo; índiceArgumento++) {
            if (!prepararEntrada(índiceArgumento)) continue;
            int datosByte; while ((datosByte = leer()) != 256 && datosByte >= 0) Placa.escribirSerie(datosByte);
            if (datosByte < 0) IntérpreteComandos.error(datosByte); cerrar();
        }
    }
    static void trabajoUnidadArchivo(String númeroAcción) {
        if (IntérpreteComandos.númeroElementosTokenLéxico != 2) { IntérpreteComandos.resultado = 2; EntradaSalidaTerminal.escribir("사용법: mkdir/rmdir/touch Archivo\n"); return; }
        int valorProcesado = IntérpreteComandos.ruta(1);
        if (valorProcesado >= 0) {
            if (númeroAcción.charAt(0) == 'm') valorProcesado = ArchivosMemoria.crearDirectorio();
            else if (númeroAcción.charAt(0) == 'r') valorProcesado = ArchivosMemoria.eliminarDirectorio();
            else { valorProcesado = ArchivosMemoria.abrir(65); if (valorProcesado >= 3) valorProcesado = ArchivosMemoria.cerrar(valorProcesado); }
        }
        if (valorProcesado < 0) IntérpreteComandos.error(valorProcesado);
    }
    static void copiarValor(boolean tieneDesplazado) {
        if (IntérpreteComandos.númeroElementosTokenLéxico != 3) { IntérpreteComandos.resultado = 2; EntradaSalidaTerminal.escribir("사용법: cp/mv original extremoDestino (Archivo)\n"); return; }
        int valorProcesado = IntérpreteComandos.ruta(1); if (valorProcesado >= 0) valorProcesado = ArchivosMemoria.normalizarValor();
        if (valorProcesado < 0) { IntérpreteComandos.error(valorProcesado); return; }
        int númeroOriginal = ArchivosMemoria.encontrarEntradaElemento(); if (númeroOriginal < 0) { IntérpreteComandos.error(-2); return; }
        int númeroElementosEntradaElemento = ArchivosMemoria.longitud[númeroOriginal]; for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) Datos[índiceBucle] = ArchivosMemoria.leerDatos(númeroOriginal, índiceBucle);
        valorProcesado = IntérpreteComandos.ruta(2); if (valorProcesado >= 0) valorProcesado = ArchivosMemoria.normalizarValor();
        if (valorProcesado < 0) { IntérpreteComandos.error(valorProcesado); return; }
        if (ArchivosMemoria.encontrarEntradaElemento() == númeroOriginal) { if (!tieneDesplazado) IntérpreteComandos.error(-22); return; }
        if (tieneDesplazado) { valorProcesado = ArchivosMemoria.renombrarEntradaElemento(númeroOriginal); if (valorProcesado < 0) IntérpreteComandos.error(valorProcesado); return; }
        int númeroArchivoAbierto = ArchivosMemoria.abrir(577); if (númeroArchivoAbierto < 0) { IntérpreteComandos.error(númeroArchivoAbierto); return; }
        for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) { valorProcesado = ArchivosMemoria.escribir(númeroArchivoAbierto, Datos[índiceBucle]); if (valorProcesado < 0) { IntérpreteComandos.error(valorProcesado); break; } }
        ArchivosMemoria.cerrar(númeroArchivoAbierto);
    }
    static int valorDígito(int índiceArgumento) {
        if (índiceArgumento >= IntérpreteComandos.númeroElementosTokenLéxico) return -1;
        int númeroElementosEntradaElemento = 0; for (int índiceBucle = 0; índiceBucle < IntérpreteComandos.longitud[índiceArgumento]; índiceBucle++) { int códigoCarácter = IntérpreteComandos.valorTokenLéxico[IntérpreteComandos.puntoInicial[índiceArgumento] + índiceBucle]; if (códigoCarácter < '0' || códigoCarácter > '9' || númeroElementosEntradaElemento > 10000) return -1; númeroElementosEntradaElemento = númeroElementosEntradaElemento * 10 + códigoCarácter - '0'; } return númeroElementosEntradaElemento;
    }
    static void valorConteoEnCurso() {
        int índiceArgumento = 1, opción = 0;
        if (IntérpreteComandos.textoIgual(1, "-c") || IntérpreteComandos.textoIgual(1, "-l") || IntérpreteComandos.textoIgual(1, "-w")) { opción = IntérpreteComandos.textoIgual(1, "-c") ? 1 : IntérpreteComandos.textoIgual(1, "-l") ? 2 : 3; índiceArgumento++; }
        if (IntérpreteComandos.númeroElementosTokenLéxico > índiceArgumento + 1) { IntérpreteComandos.resultado = 2; EntradaSalidaTerminal.escribir("사용법: wc [-c|-l|-w] [Archivo]\n"); return; }
        if (!prepararEntrada(índiceArgumento)) return;
        int númeroElementosByte = 0, líneas = 0, númeroElementosPalabraLéxico = 0, datosByte; boolean palabraLéxico = false;
        while ((datosByte = leer()) >= 0 && datosByte != 256) { númeroElementosByte++; if (datosByte == 10) líneas++; boolean espacio = datosByte == 32 || datosByte >= 9 && datosByte <= 13; if (!espacio && !palabraLéxico) númeroElementosPalabraLéxico++; palabraLéxico = !espacio; }
        cerrar(); if (datosByte < 0) { IntérpreteComandos.error(datosByte); return; }
        if (opción != 0) EntradaSalidaTerminal.númeroValor(opción == 1 ? númeroElementosByte : opción == 2 ? líneas : númeroElementosPalabraLéxico);
        else { EntradaSalidaTerminal.númeroValor(líneas); EntradaSalidaTerminal.Caracteres(' '); EntradaSalidaTerminal.númeroValor(númeroElementosPalabraLéxico); EntradaSalidaTerminal.Caracteres(' '); EntradaSalidaTerminal.númeroValor(númeroElementosByte); } EntradaSalidaTerminal.Caracteres(10);
    }
    static void encontrarEntradaElemento() {
        if (IntérpreteComandos.númeroElementosTokenLéxico < 2 || IntérpreteComandos.númeroElementosTokenLéxico > 3) { IntérpreteComandos.resultado = 2; EntradaSalidaTerminal.escribir("사용법: grep 찾을문구 [Archivo]\n"); return; }
        if (!prepararEntrada(2)) return;
        int númeroElementosEntradaElemento = 0, datosByte, coincidencias = 0;
        while (true) {
            datosByte = leer();
            if (datosByte == 10 || datosByte == 256 || datosByte < 0) {
                boolean encontradoEra = false;
                for (int índiceBucle = 0; índiceBucle <= númeroElementosEntradaElemento - IntérpreteComandos.longitud[1]; índiceBucle++) {
                    boolean esMismo = true; for (int posiciónInterior = 0; posiciónInterior < IntérpreteComandos.longitud[1]; posiciónInterior++) if (Datos[índiceBucle + posiciónInterior] != IntérpreteComandos.valorTokenLéxico[IntérpreteComandos.puntoInicial[1] + posiciónInterior]) esMismo = false;
                    if (esMismo) encontradoEra = true;
                }
                if (encontradoEra && (númeroElementosEntradaElemento > 0 || datosByte == 10)) { for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) Placa.escribirSerie(Datos[índiceBucle]); EntradaSalidaTerminal.Caracteres(10); coincidencias++; }
                númeroElementosEntradaElemento = 0; if (datosByte != 10) break;
            } else if (númeroElementosEntradaElemento < Datos.length) Datos[númeroElementosEntradaElemento++] = datosByte;
            else { IntérpreteComandos.error(-28); cerrar(); return; }
        }
        cerrar(); if (datosByte < 0) IntérpreteComandos.error(datosByte); else if (IntérpreteComandos.resultado == 0) IntérpreteComandos.resultado = coincidencias == 0 ? 1 : 0;
    }
    static void valorCabecera(boolean posiciónTrasero) {
        int índiceArgumento = 1, líneas = 10;
        if (IntérpreteComandos.textoIgual(1, "-n")) { líneas = valorDígito(2); índiceArgumento = 3; }
        if (líneas < 0 || IntérpreteComandos.númeroElementosTokenLéxico > índiceArgumento + 1) { IntérpreteComandos.resultado = 2; EntradaSalidaTerminal.escribir("사용법: head/tail [-n líneas] [Archivo]\n"); return; }
        if (!prepararEntrada(índiceArgumento)) return;
        int númeroElementosEntradaElemento = 0, datosByte;
        while ((datosByte = leer()) != 256 && datosByte >= 0) { if (númeroElementosEntradaElemento == Datos.length) { IntérpreteComandos.error(-28); cerrar(); return; } Datos[númeroElementosEntradaElemento++] = datosByte; }
        cerrar(); if (datosByte < 0) { IntérpreteComandos.error(datosByte); return; }
        int iniciarLocal = 0, posiciónFin = númeroElementosEntradaElemento;
        if (líneas == 0) return;
        if (posiciónTrasero) { int númeroElementosTotal = 0; for (int índiceBucle = númeroElementosEntradaElemento - 2; índiceBucle >= 0; índiceBucle--) if (Datos[índiceBucle] == 10 && ++númeroElementosTotal == líneas) { iniciarLocal = índiceBucle + 1; break; } }
        else { int númeroElementosTotal = 0; for (int índiceBucle = 0; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) if (Datos[índiceBucle] == 10 && ++númeroElementosTotal == líneas) { posiciónFin = índiceBucle + 1; break; } }
        for (int índiceBucle = iniciarLocal; índiceBucle < posiciónFin; índiceBucle++) Placa.escribirSerie(Datos[índiceBucle]);
    }
    static void escribirJuntos() {
        boolean añadirFinal = IntérpreteComandos.textoIgual(1, "-a"); int índiceArgumento = añadirFinal ? 2 : 1;
        if (IntérpreteComandos.númeroElementosTokenLéxico != índiceArgumento + 1) { IntérpreteComandos.resultado = 2; EntradaSalidaTerminal.escribir("사용법: tee [-a] Archivo\n"); return; }
        int númeroArchivoAbierto = abrirArchivo(índiceArgumento, añadirFinal ? 1089 : 577); if (númeroArchivoAbierto < 0) { IntérpreteComandos.error(númeroArchivoAbierto); return; }
        archivoEntrada = -1; int datosByte;
        while ((datosByte = leer()) != 256 && datosByte >= 0) { int valorProcesado = ArchivosMemoria.escribir(númeroArchivoAbierto, datosByte); if (valorProcesado < 0) { IntérpreteComandos.error(valorProcesado); break; } Placa.escribirSerie(datosByte); }
        ArchivosMemoria.cerrar(númeroArchivoAbierto);
    }
}
