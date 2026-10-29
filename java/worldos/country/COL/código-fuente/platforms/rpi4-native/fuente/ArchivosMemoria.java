// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 64 archivos RAM de 16384 bytes cada uno y 16 descriptores. Todos los datos y reglas están en Java. Las llamadas no ceden la ejecución, por lo que son atómicas entre tareas cooperativas en el único núcleo actual. No es almacenamiento en disco ni una implementación completa de POSIX. Los resultados negativos son números de error. */
public final class ArchivosMemoria {
    static final int númeroElementosArchivo = 64;
    static int[] nombre = new int[númeroElementosArchivo * 64];
    static int[] longitudNombre = new int[númeroElementosArchivo];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] valorContenidoValor = new int[númeroElementosArchivo * 4096];
    static int[] longitud = new int[númeroElementosArchivo];
    static int[] númeroElementosReferencia = new int[númeroElementosArchivo];
    static int[] valorUsar = new int[16];
    static int[] valorObjetivo = new int[16];
    static int[] posición = new int[16];
    static int[] modoMétodo = new int[16];
    static int[] ruta = new int[64];
    static int longitudRuta;

    public static int límiteArchivo() { return númeroElementosArchivo; }
    static int leerDatos(int Archivo, int índicePosición) { return (valorContenidoValor[Archivo * 4096 + índicePosición / 4] >>> ((índicePosición & 3) * 8)) & 255; }
    static void escribirDatos(int Archivo, int índicePosición, int valor) {
        int entradaElementoRanura = Archivo * 4096 + índicePosición / 4, valorMover = (índicePosición & 3) * 8;
        valorContenidoValor[entradaElementoRanura] = (valorContenidoValor[entradaElementoRanura] & ~(255 << valorMover)) | ((valor & 255) << valorMover);
    }

    public static int iniciarRuta(int tamaño) {
        longitudRuta = 0;
        if (tamaño < 1 || tamaño > 63) return -36;
        longitudRuta = tamaño;
        for (int índiceBucle = 0; índiceBucle < tamaño; índiceBucle++) ruta[índiceBucle] = 0;
        return 0;
    }
    public static int byteRuta(int número, int valor) {
        if (número < 0 || número >= longitudRuta || valor < 1 || valor > 255) return -22;
        ruta[número] = valor; return 0;
    }
    static int encontrarEntradaElemento() {
        for (int índiceArchivo = 0; índiceArchivo < númeroElementosArchivo; índiceArchivo++) if (longitudNombre[índiceArchivo] > 0 && longitudNombre[índiceArchivo] == longitudCanónico && valorPrefijo(nombre, índiceArchivo * 64, longitudNombre[índiceArchivo], valorCanónico, longitudCanónico)) return índiceArchivo;
        return -1;
    }
    public static int abrir(int valorBanderas) {
        if (longitudRuta == 0 || (valorBanderas & ~0x6c3) != 0 || (valorBanderas & 3) == 3) return -22;
        for (int índiceBucle = 0; índiceBucle < longitudRuta; índiceBucle++) if (ruta[índiceBucle] == 0) return -22;
        if ((valorBanderas & 0x200) != 0 && (valorBanderas & 3) == 0) return -22;
        int resultado = normalizarValor(); if (resultado < 0) return resultado;
        if (encontrarDirectorio(longitudCanónico) >= 0) return -21;
        resultado = comprobarPadre(); if (resultado < 0) return resultado;
        int Archivo = encontrarEntradaElemento();
        if (Archivo >= 0 && (valorBanderas & 0xc0) == 0xc0) return -17;
        if (Archivo < 0 && (valorBanderas & 0x40) == 0) return -2;
        int entradaElementoDescriptor = -1;
        for (int índiceBucle = 0; índiceBucle < 16; índiceBucle++) if (valorUsar[índiceBucle] == 0) { entradaElementoDescriptor = índiceBucle; break; }
        if (entradaElementoDescriptor < 0) return -24;
        if (Archivo < 0) {
            for (int índiceBucle = 0; índiceBucle < númeroElementosArchivo; índiceBucle++) if (longitudNombre[índiceBucle] == 0 && númeroElementosReferencia[índiceBucle] == 0) { Archivo = índiceBucle; break; }
            if (Archivo < 0) return -28;
            longitudNombre[Archivo] = longitudCanónico;
            for (int índiceBucle = 0; índiceBucle < longitudCanónico; índiceBucle++) nombre[Archivo * 64 + índiceBucle] = valorCanónico[índiceBucle];
            longitud[Archivo] = 0;
        }
        if ((valorBanderas & 0x200) != 0) longitud[Archivo] = 0;
        valorUsar[entradaElementoDescriptor] = 1; valorObjetivo[entradaElementoDescriptor] = Archivo; posición[entradaElementoDescriptor] = 0; modoMétodo[entradaElementoDescriptor] = valorBanderas;
        númeroElementosReferencia[Archivo]++;
        return entradaElementoDescriptor + 3;
    }
    static int verificar(int entradaElementoDescriptor) {
        return entradaElementoDescriptor >= 3 && entradaElementoDescriptor < 19 && valorUsar[entradaElementoDescriptor - 3] != 0 ? entradaElementoDescriptor - 3 : -1;
    }
    public static int leer(int entradaElementoDescriptor) {
        int entradaElementoRanura = verificar(entradaElementoDescriptor);
        if (entradaElementoRanura < 0 || (modoMétodo[entradaElementoRanura] & 3) == 1) return -9;
        int Archivo = valorObjetivo[entradaElementoRanura];
        if (posición[entradaElementoRanura] >= longitud[Archivo]) return 256; // Distinguir EOF de los bytes reales 0x00..0xff.
        return leerDatos(Archivo, posición[entradaElementoRanura]++);
    }
    public static int escribir(int entradaElementoDescriptor, int valor) {
        int entradaElementoRanura = verificar(entradaElementoDescriptor);
        if (entradaElementoRanura < 0 || (modoMétodo[entradaElementoRanura] & 3) == 0) return -9;
        int Archivo = valorObjetivo[entradaElementoRanura];
        if ((modoMétodo[entradaElementoRanura] & 0x400) != 0) posición[entradaElementoRanura] = longitud[Archivo];
        if (posición[entradaElementoRanura] >= 16384) return -28;
        while (longitud[Archivo] < posición[entradaElementoRanura]) escribirDatos(Archivo, longitud[Archivo]++, 0);
        escribirDatos(Archivo, posición[entradaElementoRanura]++, valor);
        if (longitud[Archivo] < posición[entradaElementoRanura]) longitud[Archivo] = posición[entradaElementoRanura];
        return 1;
    }
    public static int posicionarPosición(int entradaElementoDescriptor, int valorDistancia, int raízProyecto) {
        int entradaElementoRanura = verificar(entradaElementoDescriptor);
        if (entradaElementoRanura < 0) return -9;
        if (raízProyecto < 0 || raízProyecto > 2 || valorDistancia < -16384 || valorDistancia > 16384) return -22;
        int posiciónNuevo = valorDistancia + (raízProyecto == 0 ? 0 : raízProyecto == 1 ? posición[entradaElementoRanura] : longitud[valorObjetivo[entradaElementoRanura]]);
        if (posiciónNuevo < 0 || posiciónNuevo > 16384) return -22;
        posición[entradaElementoRanura] = posiciónNuevo; return posiciónNuevo;
    }
    public static int cerrar(int entradaElementoDescriptor) {
        int entradaElementoRanura = verificar(entradaElementoDescriptor);
        if (entradaElementoRanura < 0) return -9;
        númeroElementosReferencia[valorObjetivo[entradaElementoRanura]]--; valorUsar[entradaElementoRanura] = 0; return 0;
    }
    public static int tamaño(int entradaElementoDescriptor) {
        int entradaElementoRanura = verificar(entradaElementoDescriptor); return entradaElementoRanura < 0 ? -9 : longitud[valorObjetivo[entradaElementoRanura]];
    }
    public static int establecerLongitud(int entradaElementoDescriptor, int tamaño) {
        int entradaElementoRanura = verificar(entradaElementoDescriptor);
        if (entradaElementoRanura < 0 || (modoMétodo[entradaElementoRanura] & 3) == 0) return -9;
        if (tamaño < 0 || tamaño > 16384) return -22;
        int Archivo = valorObjetivo[entradaElementoRanura];
        while (longitud[Archivo] < tamaño) escribirDatos(Archivo, longitud[Archivo]++, 0);
        longitud[Archivo] = tamaño; return 0;
    }
    public static int borrarEntradaElemento() {
        if (longitudRuta == 0) return -22;
        int resultado = normalizarValor(); if (resultado < 0) return resultado;
        if (encontrarDirectorio(longitudCanónico) >= 0) return -21;
        resultado = comprobarPadre(); if (resultado < 0) return resultado;
        int Archivo = encontrarEntradaElemento();
        if (Archivo < 0) return -2;
        longitudNombre[Archivo] = 0; return 0; // Conservar un archivo abierto hasta el último close.
    }
    static void listaEntradaElemento() {
        iniciarRuta(1); byteRuta(0, '.'); entradasRuta();
    }
    public static int longitudNombreExportado(int número) {
        if (número < 0 || número >= númeroElementosArchivo || longitudNombre[número] == 0) return 0;
        for (int índiceBucle = 0; índiceBucle < longitudNombre[número]; índiceBucle++) if (nombre[número * 64 + índiceBucle] == '/') return 0;
        return longitudNombre[número];
    }
    public static int byteNombreExportado(int número, int índicePosición) {
        return número >= 0 && número < númeroElementosArchivo && índicePosición >= 0 && índicePosición < longitudNombre[número] ? nombre[número * 64 + índicePosición] : -22;
    }
    public static int tamañoArchivoExportado(int número) { return número >= 0 && número < númeroElementosArchivo ? longitud[número] : -22; }
    static int[] valorCanónico = new int[64], elementoListaActual = new int[64], nombreDirectorio = new int[16 * 64], longitudDirectorio = new int[16];
    static int longitudCanónico, longitudActual;
    static boolean valorPrefijo(int[] listaNombres, int ponerEnMarcha, int valorRuta, int[] valorLadoDelantero, int rutaPrevio) {
        if (valorRuta < rutaPrevio) return false;
        for (int índiceBucle = 0; índiceBucle < rutaPrevio; índiceBucle++) if (listaNombres[ponerEnMarcha + índiceBucle] != valorLadoDelantero[índiceBucle]) return false;
        return true;
    }
    static int normalizarValor() {
        if (longitudRuta == 0) return -22;
        longitudCanónico = ruta[0] == '/' ? 0 : longitudActual;
        for (int índiceBucle = 0; índiceBucle < longitudCanónico; índiceBucle++) valorCanónico[índiceBucle] = elementoListaActual[índiceBucle];
        int leerCursor = 0;
        while (leerCursor < longitudRuta) {
            while (leerCursor < longitudRuta && ruta[leerCursor] == '/') leerCursor++;
            int iniciarPosición = leerCursor; while (leerCursor < longitudRuta && ruta[leerCursor] != '/') { if (ruta[leerCursor] == 0) return -22; leerCursor++; }
            int númeroElementosEntradaElemento = leerCursor - iniciarPosición; if (númeroElementosEntradaElemento == 0 || númeroElementosEntradaElemento == 1 && ruta[iniciarPosición] == '.') continue;
            if (númeroElementosEntradaElemento == 2 && ruta[iniciarPosición] == '.' && ruta[iniciarPosición + 1] == '.') {
                while (longitudCanónico > 0 && valorCanónico[longitudCanónico - 1] != '/') longitudCanónico--;
                if (longitudCanónico > 0) longitudCanónico--;
                continue;
            }
            if (longitudCanónico + númeroElementosEntradaElemento + (longitudCanónico == 0 ? 0 : 1) > 63) return -36;
            if (longitudCanónico > 0) valorCanónico[longitudCanónico++] = '/';
            for (int índiceBucle = iniciarPosición; índiceBucle < leerCursor; índiceBucle++) valorCanónico[longitudCanónico++] = ruta[índiceBucle];
        }
        return 0;
    }
    static int encontrarDirectorio(int númeroElementosEntradaElemento) {
        if (númeroElementosEntradaElemento == 0) return 0;
        for (int índiceBucle = 1; índiceBucle < 16; índiceBucle++) if (longitudDirectorio[índiceBucle] == númeroElementosEntradaElemento && valorPrefijo(nombreDirectorio, índiceBucle * 64, númeroElementosEntradaElemento, valorCanónico, númeroElementosEntradaElemento)) return índiceBucle;
        return -1;
    }
    static int comprobarPadre() {
        int númeroElementosEntradaElemento = longitudCanónico; while (númeroElementosEntradaElemento > 0 && valorCanónico[númeroElementosEntradaElemento - 1] != '/') númeroElementosEntradaElemento--;
        return encontrarDirectorio(númeroElementosEntradaElemento == 0 ? 0 : númeroElementosEntradaElemento - 1) < 0 ? -2 : 0;
    }
    public static int crearDirectorio() {
        int valorProcesado = normalizarValor(); if (valorProcesado < 0) return valorProcesado;
        if (encontrarDirectorio(longitudCanónico) >= 0 || encontrarEntradaElemento() >= 0) return -17;
        valorProcesado = comprobarPadre(); if (valorProcesado < 0) return valorProcesado;
        for (int índiceBucle = 1; índiceBucle < 16; índiceBucle++) if (longitudDirectorio[índiceBucle] == 0) {
            longitudDirectorio[índiceBucle] = longitudCanónico; for (int posiciónInterior = 0; posiciónInterior < longitudCanónico; posiciónInterior++) nombreDirectorio[índiceBucle * 64 + posiciónInterior] = valorCanónico[posiciónInterior]; return 0;
        }
        return -28;
    }
    public static int claseTipoEntradaElemento() {
        int valorProcesado = normalizarValor(); if (valorProcesado < 0) return valorProcesado;
        if (encontrarDirectorio(longitudCanónico) >= 0) return 2;
        return encontrarEntradaElemento() >= 0 ? 1 : 0;
    }
    public static int cambiarDirectorio() {
        int valorProcesado = normalizarValor(); if (valorProcesado < 0) return valorProcesado;
        if (encontrarDirectorio(longitudCanónico) < 0) return -2;
        longitudActual = longitudCanónico; for (int índiceBucle = 0; índiceBucle < longitudActual; índiceBucle++) elementoListaActual[índiceBucle] = valorCanónico[índiceBucle]; return 0;
    }
    public static int eliminarDirectorio() {
        int valorProcesado = normalizarValor(); if (valorProcesado < 0) return valorProcesado;
        int númeroDirectorio = encontrarDirectorio(longitudCanónico); if (númeroDirectorio < 0) return -2; if (númeroDirectorio == 0) return -16;
        if (longitudActual == longitudCanónico && valorPrefijo(elementoListaActual, 0, longitudActual, valorCanónico, longitudCanónico)) return -16;
        for (int índiceBucle = 0; índiceBucle < númeroElementosArchivo; índiceBucle++) {
            if (longitudNombre[índiceBucle] > longitudCanónico && valorPrefijo(nombre, índiceBucle * 64, longitudNombre[índiceBucle], valorCanónico, longitudCanónico) && nombre[índiceBucle * 64 + longitudCanónico] == '/') return -39;
        }
        for (int índiceBucle = 0; índiceBucle < 16; índiceBucle++) {
            if (longitudDirectorio[índiceBucle] > longitudCanónico && valorPrefijo(nombreDirectorio, índiceBucle * 64, longitudDirectorio[índiceBucle], valorCanónico, longitudCanónico) && nombreDirectorio[índiceBucle * 64 + longitudCanónico] == '/') return -39;
        }
        longitudDirectorio[númeroDirectorio] = 0; return 0;
    }
    public static int renombrarEntradaElemento(int númeroOriginal) {
        if (númeroOriginal < 0 || númeroOriginal >= númeroElementosArchivo || longitudNombre[númeroOriginal] == 0) return -2;
        int valorProcesado = normalizarValor(); if (valorProcesado < 0) return valorProcesado;
        if (encontrarDirectorio(longitudCanónico) >= 0) return -21;
        valorProcesado = comprobarPadre(); if (valorProcesado < 0) return valorProcesado;
        int valorElementoPrevio = encontrarEntradaElemento(); if (valorElementoPrevio == númeroOriginal) return 0;
        if (valorElementoPrevio >= 0) longitudNombre[valorElementoPrevio] = 0;
        longitudNombre[númeroOriginal] = longitudCanónico; for (int índiceBucle = 0; índiceBucle < longitudCanónico; índiceBucle++) nombre[númeroOriginal * 64 + índiceBucle] = valorCanónico[índiceBucle]; return 0;
    }
    static int iniciarEntradaElemento(int[] arregloDatos, int puntoInicial, int númeroElementosEntradaElemento) {
        if (!valorPrefijo(arregloDatos, puntoInicial, númeroElementosEntradaElemento, valorCanónico, longitudCanónico)) return -1;
        int iniciarPosición = longitudCanónico;
        if (iniciarPosición > 0) { if (númeroElementosEntradaElemento <= iniciarPosición || arregloDatos[puntoInicial + iniciarPosición] != '/') return -1; iniciarPosición++; }
        if (númeroElementosEntradaElemento <= iniciarPosición) return -1;
        for (int índiceBucle = iniciarPosición; índiceBucle < númeroElementosEntradaElemento; índiceBucle++) if (arregloDatos[puntoInicial + índiceBucle] == '/') return -1;
        return iniciarPosición;
    }
    static void escribirActual() { EntradaSalidaTerminal.Caracteres('/'); for (int índiceBucle = 0; índiceBucle < longitudActual; índiceBucle++) Placa.escribirSerie(elementoListaActual[índiceBucle]); }
    static int entradasRuta() {
        int valorProcesado = normalizarValor(); if (valorProcesado < 0) return valorProcesado;
        int valorObjetivoArchivo = encontrarEntradaElemento();
        if (valorObjetivoArchivo >= 0) { for (int índiceBucle = 0; índiceBucle < longitudCanónico; índiceBucle++) Placa.escribirSerie(valorCanónico[índiceBucle]); EntradaSalidaTerminal.escribir("  "); EntradaSalidaTerminal.númeroValor(longitud[valorObjetivoArchivo]); EntradaSalidaTerminal.escribir("valorByte(주기억 Archivo)\n"); return 0; }
        if (encontrarDirectorio(longitudCanónico) < 0) return -2;
        for (int valorPosiciónFinal = 1; valorPosiciónFinal < 16; valorPosiciónFinal++) if (longitudDirectorio[valorPosiciónFinal] > 0) {
            int iniciarPosición = iniciarEntradaElemento(nombreDirectorio, valorPosiciónFinal * 64, longitudDirectorio[valorPosiciónFinal]); if (iniciarPosición < 0) continue;
            for (int índiceBucle = iniciarPosición; índiceBucle < longitudDirectorio[valorPosiciónFinal]; índiceBucle++) Placa.escribirSerie(nombreDirectorio[valorPosiciónFinal * 64 + índiceBucle]); EntradaSalidaTerminal.escribir("/\n");
        }
        for (int índiceArchivo = 0; índiceArchivo < númeroElementosArchivo; índiceArchivo++) if (longitudNombre[índiceArchivo] > 0) {
            int iniciarPosición = iniciarEntradaElemento(nombre, índiceArchivo * 64, longitudNombre[índiceArchivo]); if (iniciarPosición < 0) continue;
            for (int índiceBucle = iniciarPosición; índiceBucle < longitudNombre[índiceArchivo]; índiceBucle++) Placa.escribirSerie(nombre[índiceArchivo * 64 + índiceBucle]);
            EntradaSalidaTerminal.escribir("  "); EntradaSalidaTerminal.númeroValor(longitud[índiceArchivo]); EntradaSalidaTerminal.escribir("valorByte(주기억 Archivo)\n");
        }
        return 0;
    }
}
