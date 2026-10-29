// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Pequeño formato de almacenamiento propio con sumas de comprobación y dos copias. Solo persiste al llamar fsync/sync. */
public final class PersistenciaArchivos {
    static int copiarPreservadoActual = -1, númeroGeneración = 0;
    static int[] tablaArchivo = new int[1024];
    static int bytesResumenHash(int valor, int Datos) { return (valor ^ Datos) * 16777619; }
    static void borrarContenidoDatos() {
        for (int número = 0; número < 512; número++) ConexiónAlmacenamiento.datosSección[número] = 0;
    }
    static int enteroValorTabla(int posición) {
        return tablaArchivo[posición] | tablaArchivo[posición + 1] << 8 | tablaArchivo[posición + 2] << 16 | tablaArchivo[posición + 3] << 24;
    }
    static void escribirEnteroValorTabla(int posición, int valor) {
        for (int número = 0; número < 4; número++) tablaArchivo[posición + número] = (valor >>> (número * 8)) & 255;
    }
    static boolean comprobarTabla() {
        for (int Archivo = 0; Archivo < 8; Archivo++) {
            int longitud = 0;
            for (int entradaElementoRanura = 0; entradaElementoRanura < 64; entradaElementoRanura++) SistemaArchivosMemoria.nombre[entradaElementoRanura] = tablaArchivo[Archivo * 72 + entradaElementoRanura];
            while (longitud < 64 && SistemaArchivosMemoria.nombre[longitud] != 0) longitud++;
            if (longitud == 0) continue;
            if (!SistemaArchivosMemoria.comprobarNombre(SistemaArchivosMemoria.nombre, longitud)
                || enteroValorTabla(Archivo * 72 + 64) < 0 || enteroValorTabla(Archivo * 72 + 64) > 16384) return false;
            for (int valorLadoDelantero = 0; valorLadoDelantero < Archivo; valorLadoDelantero++) {
                boolean textoIgual = tablaArchivo[valorLadoDelantero * 72 + longitud] == 0;
                for (int entradaElementoRanura = 0; entradaElementoRanura < longitud; entradaElementoRanura++) if (tablaArchivo[valorLadoDelantero * 72 + entradaElementoRanura] != SistemaArchivosMemoria.nombre[entradaElementoRanura]) textoIgual = false;
                if (textoIgual) return false;
            }
        }
        return true;
    }
    static int comprobarCopiarPreservado(int copiarPreservado) {
        int iniciarSección = 1 + copiarPreservado * 259;
        if (ConexiónAlmacenamiento.leer(iniciarSección) < 0 || ConexiónAlmacenamiento.analizarEnteroValor(0) != 0x4a4b534e) return -1;
        int valorGeneración = ConexiónAlmacenamiento.analizarEnteroValor(4), sumaComprobación = ConexiónAlmacenamiento.analizarEnteroValor(8);
        if (valorGeneración < 1 || ConexiónAlmacenamiento.analizarEnteroValor(12) != (valorGeneración ^ sumaComprobación ^ 0x4a4b534e)) return -1;
        int archivoResumenHash = 0x811c9dc5;
        for (int valorSección = 0; valorSección < 258; valorSección++) {
            if (ConexiónAlmacenamiento.leer(iniciarSección + 1 + valorSección) < 0) return -1;
            for (int entradaElementoRanura = 0; entradaElementoRanura < 512; entradaElementoRanura++) {
                int valor = ConexiónAlmacenamiento.datosSección[entradaElementoRanura];
                archivoResumenHash = bytesResumenHash(archivoResumenHash, valor);
                if (valorSección < 2) tablaArchivo[valorSección * 512 + entradaElementoRanura] = valor;
            }
        }
        return archivoResumenHash == sumaComprobación && comprobarTabla() ? valorGeneración : -1;
    }
    static int cargar(int copiarPreservado) {
        int iniciarSección = 1 + copiarPreservado * 259;
        for (int valorSección = 0; valorSección < 2; valorSección++) {
            if (ConexiónAlmacenamiento.leer(iniciarSección + 1 + valorSección) < 0) return -5;
            for (int entradaElementoRanura = 0; entradaElementoRanura < 512; entradaElementoRanura++) tablaArchivo[valorSección * 512 + entradaElementoRanura] = ConexiónAlmacenamiento.datosSección[entradaElementoRanura];
        }
        for (int Archivo = 0; Archivo < 8; Archivo++) {
            for (int entradaElementoRanura = 0; entradaElementoRanura < 64; entradaElementoRanura++) SistemaArchivosMemoria.listaNombres[Archivo * 64 + entradaElementoRanura] = tablaArchivo[Archivo * 72 + entradaElementoRanura];
            SistemaArchivosMemoria.listaTamaño[Archivo] = tablaArchivo[Archivo * 72] == 0 ? 0 : enteroValorTabla(Archivo * 72 + 64);
            SistemaArchivosMemoria.concesionesPermiso[Archivo] = enteroValorTabla(Archivo * 72 + 68) & 511;
            for (int valorSección = 0; valorSección < 32; valorSección++) {
                if (ConexiónAlmacenamiento.leer(iniciarSección + 3 + Archivo * 32 + valorSección) < 0) return -5;
                int dirección = Dispositivo.memoriaArchivo() + Archivo * 16384 + valorSección * 512;
                for (int entradaElementoRanura = 0; entradaElementoRanura < 512; entradaElementoRanura++) Dispositivo.escribirMemoria(dirección + entradaElementoRanura, ConexiónAlmacenamiento.datosSección[entradaElementoRanura]);
            }
        }
        return 0;
    }
    static void preparar() {
        if (ConexiónAlmacenamiento.leer(0) < 0 || ConexiónAlmacenamiento.analizarEnteroValor(0) != 0x54534b4a
            || ConexiónAlmacenamiento.analizarEnteroValor(4) != 0x3145524f || ConexiónAlmacenamiento.analizarEnteroValor(8) != 2048
            || ConexiónAlmacenamiento.analizarEnteroValor(12) != 0x3153464a) {
            TerminalTexto.escribir("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        ConexiónAlmacenamiento.esDisponible = true;
        int ordinalPrimero = comprobarCopiarPreservado(0), ordinalSegundo = comprobarCopiarPreservado(1);
        if (ordinalPrimero < 0 && ordinalSegundo < 0) { TerminalTexto.escribir("STORE ready; no valid snapshot\n"); return; }
        copiarPreservadoActual = ordinalPrimero >= ordinalSegundo ? 0 : 1; númeroGeneración = ordinalPrimero >= ordinalSegundo ? ordinalPrimero : ordinalSegundo;
        if (cargar(copiarPreservadoActual) < 0) {
            TerminalTexto.escribir("STORE read failed; halted to preserve files\n"); Dispositivo.ejecuciónDetenerMáquina();
        }
        TerminalTexto.escribir("STORE restored generation "); TerminalTexto.escribirNúmero(númeroGeneración); TerminalTexto.Caracteres(10);
    }
    static int sincronizar() {
        if (!ConexiónAlmacenamiento.esDisponible) return -19;
        if (númeroGeneración == 2147483647) return -75;
        int elementoListaSiguiente = copiarPreservadoActual == 0 ? 1 : 0, iniciarSección = 1 + elementoListaSiguiente * 259;
        // Invalidar el commit anterior y vaciar la caché del dispositivo antes de escribir el nuevo contenido.
        borrarContenidoDatos();
        if (ConexiónAlmacenamiento.escribir(iniciarSección) < 0 || ConexiónAlmacenamiento.salidaVaciarBúfer() < 0) return -5;
        for (int entradaElementoRanura = 0; entradaElementoRanura < 1024; entradaElementoRanura++) tablaArchivo[entradaElementoRanura] = 0;
        for (int Archivo = 0; Archivo < 8; Archivo++) if (SistemaArchivosMemoria.listaNombres[Archivo * 64] != 0) {
            for (int entradaElementoRanura = 0; entradaElementoRanura < 64; entradaElementoRanura++) tablaArchivo[Archivo * 72 + entradaElementoRanura] = SistemaArchivosMemoria.listaNombres[Archivo * 64 + entradaElementoRanura];
            escribirEnteroValorTabla(Archivo * 72 + 64, SistemaArchivosMemoria.listaTamaño[Archivo]);
            escribirEnteroValorTabla(Archivo * 72 + 68, SistemaArchivosMemoria.concesionesPermiso[Archivo]);
        }
        int archivoResumenHash = 0x811c9dc5;
        for (int valorSección = 0; valorSección < 258; valorSección++) {
            for (int entradaElementoRanura = 0; entradaElementoRanura < 512; entradaElementoRanura++) {
                int valor = 0;
                if (valorSección < 2) valor = tablaArchivo[valorSección * 512 + entradaElementoRanura];
                else {
                    int Archivo = (valorSección - 2) / 32, posición = (valorSección - 2) % 32 * 512 + entradaElementoRanura;
                    if (tablaArchivo[Archivo * 72] != 0 && posición < SistemaArchivosMemoria.listaTamaño[Archivo])
                        valor = Dispositivo.leerMemoria(Dispositivo.memoriaArchivo() + Archivo * 16384 + posición);
                }
                ConexiónAlmacenamiento.datosSección[entradaElementoRanura] = valor; archivoResumenHash = bytesResumenHash(archivoResumenHash, valor);
            }
            if (ConexiónAlmacenamiento.escribir(iniciarSección + 1 + valorSección) < 0) return -5;
        }
        if (ConexiónAlmacenamiento.salidaVaciarBúfer() < 0) return -5;
        borrarContenidoDatos(); ConexiónAlmacenamiento.escribirValorEnteroValor(0, 0x4a4b534e);
        ConexiónAlmacenamiento.escribirValorEnteroValor(4, númeroGeneración + 1); ConexiónAlmacenamiento.escribirValorEnteroValor(8, archivoResumenHash);
        ConexiónAlmacenamiento.escribirValorEnteroValor(12, (númeroGeneración + 1) ^ archivoResumenHash ^ 0x4a4b534e);
        if (ConexiónAlmacenamiento.escribir(iniciarSección) < 0 || ConexiónAlmacenamiento.salidaVaciarBúfer() < 0) return -5;
        copiarPreservadoActual = elementoListaSiguiente; númeroGeneración++;
        return 0;
    }
}
