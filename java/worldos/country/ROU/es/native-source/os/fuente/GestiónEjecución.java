// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Valida ELF32 en paquetes ejecutables de solo lectura, pasa argumentos y ejecuta un proceso de usuario cada vez. */
public final class GestiónEjecución {
    static final int iniciarProgramaUsuario = 0x04000000;
    static final int finUsuario = 0x04400000;
    static final int direcciónFinImagen = 0x04200000;
    static final int iniciarArgumento = 0x04300000;
    static int númeroElementosArgumento = 0;
    static int[] direcciónArgumento = new int[16];

    static boolean recortar(int dirección, int longitud) {
        return dirección >= iniciarProgramaUsuario && dirección < finUsuario && longitud >= 0 && longitud <= finUsuario - dirección;
    }

    static int númeroValor(int dirección) { return EspacioMemoria.analizarEnteroValor(dirección); }
    static int valorCorto(int dirección) { return Dispositivo.leerMemoria(dirección) | Dispositivo.leerMemoria(dirección + 1) << 8; }
    static void escribirNúmero(int dirección, int valor) {
        for (int número = 0; número < 4; número++) Dispositivo.escribirMemoria(dirección + número, valor >>> (número * 8));
    }

    static int númeroElementosGrupo() {
        int dirección = Dispositivo.PaqueteCódigoEjecutable();
        int tamaño = Dispositivo.tamañoPaqueteCódigoEjecutable();
        if (tamaño < 8 || númeroValor(dirección) != 0x50414b4a) return 0;
        int númeroElementosElementoLista = númeroValor(dirección + 4);
        return númeroElementosElementoLista >= 0 && númeroElementosElementoLista <= 32 && númeroElementosElementoLista <= (tamaño - 8) / 24 ? númeroElementosElementoLista : 0;
    }

    static void listaEntradaElemento() {
        for (int número = 0; número < númeroElementosGrupo(); número++) {
            int valorEntradaElemento = Dispositivo.PaqueteCódigoEjecutable() + 8 + número * 24;
            for (int valorCarácter = 0; valorCarácter < 16 && Dispositivo.leerMemoria(valorEntradaElemento + valorCarácter) != 0; valorCarácter++)
                TerminalTexto.Caracteres(Dispositivo.leerMemoria(valorEntradaElemento + valorCarácter));
            TerminalTexto.escribir("\n");
        }
    }

    static int encontrarEntradaElemento(int[] valorEntrada, int ponerEnMarcha, int longitud) {
        if (longitud <= 0 || longitud >= 16) return 0;
        for (int número = 0; número < númeroElementosGrupo(); número++) {
            int valorEntradaElemento = Dispositivo.PaqueteCódigoEjecutable() + 8 + número * 24;
            boolean textoIgual = Dispositivo.leerMemoria(valorEntradaElemento + longitud) == 0;
            for (int valorCarácter = 0; valorCarácter < longitud; valorCarácter++)
                if (valorEntrada[ponerEnMarcha + valorCarácter] != Dispositivo.leerMemoria(valorEntradaElemento + valorCarácter)) textoIgual = false;
            if (textoIgual) return valorEntradaElemento;
        }
        return 0;
    }

    static int validar(int Archivo, int longitud) {
        if (longitud < 52 || númeroValor(Archivo) != 0x464c457f || Dispositivo.leerMemoria(Archivo + 4) != 1
            || Dispositivo.leerMemoria(Archivo + 5) != 1 || Dispositivo.leerMemoria(Archivo + 6) != 1
            || valorCorto(Archivo + 16) != 2 || valorCorto(Archivo + 18) != 3 || númeroValor(Archivo + 20) != 1
            || valorCorto(Archivo + 40) != 52 || valorCorto(Archivo + 42) != 32) return -8;
        int valorPuntoEntradaElemento = númeroValor(Archivo + 24);
        int posiciónTabla = númeroValor(Archivo + 28);
        int númeroElementosElementoLista = valorCorto(Archivo + 44);
        if (númeroElementosElementoLista == 0 || númeroElementosElementoLista > 16 || posiciónTabla < 52 || posiciónTabla > longitud - númeroElementosElementoLista * 32) return -8;
        boolean esCódigoEjecutable = false;
        for (int número = 0; número < númeroElementosElementoLista; número++) {
            int Tabla = Archivo + posiciónTabla + número * 32;
            int valorClaseTipo = númeroValor(Tabla);
            if (valorClaseTipo == 2 || valorClaseTipo == 3) return -8; // No admite enlace dinámico ni intérprete.
            if (valorClaseTipo != 1) continue;
            int posición = númeroValor(Tabla + 4), dirección = númeroValor(Tabla + 8), tamañoArchivo = númeroValor(Tabla + 16), tamañoMemoria = númeroValor(Tabla + 20);
            int valorAlinear = númeroValor(Tabla + 28);
            if (dirección < iniciarProgramaUsuario || dirección >= direcciónFinImagen || tamañoMemoria < 0 || tamañoMemoria > direcciónFinImagen - dirección
                || tamañoArchivo < 0 || tamañoArchivo > tamañoMemoria || posición < 0 || (tamañoArchivo > 0 && posición > longitud - tamañoArchivo)
                || (valorAlinear != 0 && (valorAlinear < 0 || (valorAlinear & (valorAlinear - 1)) != 0
                    || ((dirección - posición) & (valorAlinear - 1)) != 0))) return -8;
            for (int valorLadoDelantero = 0; valorLadoDelantero < número; valorLadoDelantero++) {
                int elementoListaElementoPrevio = Archivo + posiciónTabla + valorLadoDelantero * 32;
                if (númeroValor(elementoListaElementoPrevio) == 1 && tamañoMemoria > 0 && númeroValor(elementoListaElementoPrevio + 20) > 0
                    && dirección < númeroValor(elementoListaElementoPrevio + 8) + númeroValor(elementoListaElementoPrevio + 20) && númeroValor(elementoListaElementoPrevio + 8) < dirección + tamañoMemoria) return -8;
            }
            if ((númeroValor(Tabla + 24) & 1) != 0 && valorPuntoEntradaElemento >= dirección && valorPuntoEntradaElemento - dirección < tamañoArchivo) esCódigoEjecutable = true;
        }
        return esCódigoEjecutable ? valorPuntoEntradaElemento : -8;
    }

    static int ejecutarComando(int[] valorEntrada, int ponerEnMarcha, int longitud) {
        while (ponerEnMarcha < longitud && valorEntrada[ponerEnMarcha] == ' ') ponerEnMarcha++;
        int terminación = ponerEnMarcha;
        while (terminación < longitud && valorEntrada[terminación] != ' ') terminación++;
        int valorEntradaElemento = encontrarEntradaElemento(valorEntrada, ponerEnMarcha, terminación - ponerEnMarcha);
        if (valorEntradaElemento == 0) return -2;
        int posición = númeroValor(valorEntradaElemento + 16), tamaño = númeroValor(valorEntradaElemento + 20);
        if (posición < 8 + númeroElementosGrupo() * 24 || tamaño < 52 || posición > Dispositivo.tamañoPaqueteCódigoEjecutable() - tamaño) return -8;
        int Archivo = Dispositivo.PaqueteCódigoEjecutable() + posición;
        int valorPuntoEntradaElemento = validar(Archivo, tamaño);
        if (valorPuntoEntradaElemento < 0) return valorPuntoEntradaElemento;
        Dispositivo.contenidoBorrarContenidoUsuario();
        int posiciónTabla = númeroValor(Archivo + 28), númeroElementosElementoLista = valorCorto(Archivo + 44);
        for (int número = 0; número < númeroElementosElementoLista; número++) {
            int Tabla = Archivo + posiciónTabla + número * 32;
            if (númeroValor(Tabla) != 1) continue;
            int original = Archivo + númeroValor(Tabla + 4), valorDestino = númeroValor(Tabla + 8), tamañoArchivo = númeroValor(Tabla + 16);
            for (int valorByte = 0; valorByte < tamañoArchivo; valorByte++) Dispositivo.escribirMemoria(valorDestino + valorByte, Dispositivo.leerMemoria(original + valorByte));
        }
        númeroElementosArgumento = 0;
        int valorAlmacenar = iniciarArgumento;
        while (terminación < longitud) {
            while (terminación < longitud && valorEntrada[terminación] == ' ') terminación++;
            if (terminación == longitud) break;
            if (númeroElementosArgumento == direcciónArgumento.length) return -22;
            ponerEnMarcha = terminación;
            while (terminación < longitud && valorEntrada[terminación] != ' ') terminación++;
            direcciónArgumento[númeroElementosArgumento++] = valorAlmacenar;
            escribirNúmero(valorAlmacenar, terminación - ponerEnMarcha);
            for (int valorCarácter = ponerEnMarcha; valorCarácter < terminación; valorCarácter++) escribirNúmero(valorAlmacenar + 4 + (valorCarácter - ponerEnMarcha) * 4, valorEntrada[valorCarácter]);
            valorAlmacenar += 4 + (terminación - ponerEnMarcha) * 4;
        }
        PilaRed.procesoLimpiar();
        GestiónDescriptoresArchivo.iniciarProceso();
        int resultado = Dispositivo.ponerEnMarchaProgramaUsuario(valorPuntoEntradaElemento, finUsuario - 16);
        GestiónDescriptoresArchivo.procesoLimpiar();
        PilaRed.procesoLimpiar();
        return resultado;
    }
}
