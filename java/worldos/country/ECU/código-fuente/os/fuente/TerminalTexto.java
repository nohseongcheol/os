// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Salida serie COM1 y pantalla de texto VGA 80x25. El texto Unicode se envía al terminal serie como UTF-8. */
public final class TerminalTexto {
    static int entradaElementoRanura = 0;
    static int valorColor = 7;

    static void preparar() {
        Dispositivo.escribirByteEntradaSalida(0x3f9, 0);
        Dispositivo.escribirByteEntradaSalida(0x3fb, 0x80);
        Dispositivo.escribirByteEntradaSalida(0x3f8, 1);
        Dispositivo.escribirByteEntradaSalida(0x3f9, 0);
        Dispositivo.escribirByteEntradaSalida(0x3fb, 3);
        Dispositivo.escribirByteEntradaSalida(0x3fa, 0xc7);
        Dispositivo.escribirByteEntradaSalida(0x3fc, 0x0b);
        borrarEntradaElemento();
    }

    static void byteSerie(int valor) {
        int númeroElementosRepetición = 100000;
        while ((Dispositivo.leerByteEntradaSalida(0x3fd) & 0x20) == 0 && númeroElementosRepetición > 0) númeroElementosRepetición--;
        if (númeroElementosRepetición > 0) Dispositivo.escribirByteEntradaSalida(0x3f8, valor);
    }

    static void borrarEntradaElemento() {
        for (int número = 0; número < 2000; número++) {
            Dispositivo.escribirMemoria(0xb8000 + número * 2, 32);
            Dispositivo.escribirMemoria(0xb8001 + número * 2, valorColor);
        }
        entradaElementoRanura = 0;
        valorCursor();
    }

    static void valorCursor() {
        Dispositivo.escribirByteEntradaSalida(0x3d4, 14);
        Dispositivo.escribirByteEntradaSalida(0x3d5, entradaElementoRanura >> 8);
        Dispositivo.escribirByteEntradaSalida(0x3d4, 15);
        Dispositivo.escribirByteEntradaSalida(0x3d5, entradaElementoRanura & 255);
    }

    static void carácterPantalla(int valor) {
        if (valor == 13) return;
        if (valor == 10) {
            entradaElementoRanura = (entradaElementoRanura / 80 + 1) * 80;
        } else if (valor == 8) {
            if (entradaElementoRanura > 0) {
                entradaElementoRanura--;
                Dispositivo.escribirMemoria(0xb8000 + entradaElementoRanura * 2, 32);
            }
        } else {
            Dispositivo.escribirMemoria(0xb8000 + entradaElementoRanura * 2, valor < 128 ? valor : '?');
            Dispositivo.escribirMemoria(0xb8001 + entradaElementoRanura * 2, valorColor);
            entradaElementoRanura++;
        }
        if (entradaElementoRanura >= 2000) {
            for (int número = 0; número < 3840; número++)
                Dispositivo.escribirMemoria(0xb8000 + número, Dispositivo.leerMemoria(0xb80a0 + número));
            for (int número = 1920; número < 2000; número++) {
                Dispositivo.escribirMemoria(0xb8000 + número * 2, 32);
                Dispositivo.escribirMemoria(0xb8001 + número * 2, valorColor);
            }
            entradaElementoRanura = 1920;
        }
        valorCursor();
    }

    static void Caracteres(int valor) {
        if (valor < 128) {
            if (valor == 10) byteSerie(13);
            byteSerie(valor);
        } else if (valor < 2048) {
            byteSerie(0xc0 | (valor >> 6));
            byteSerie(0x80 | (valor & 63));
        } else {
            byteSerie(0xe0 | (valor >> 12));
            byteSerie(0x80 | ((valor >> 6) & 63));
            byteSerie(0x80 | (valor & 63));
        }
        carácterPantalla(valor);
    }

    static void escribir(String valorContenidoValor) {
        for (int número = 0; número < valorContenidoValor.length(); número++) Caracteres(valorContenidoValor.charAt(número));
    }

    static void escribirNúmero(int valor) {
        // No convierte a positivo, por lo que Integer.MIN_VALUE también es seguro.
        if (valor < 0) Caracteres('-');
        else valor = -valor;
        int índicePosición = 1000000000;
        boolean ponerEnMarcha = false;
        while (índicePosición > 0) {
            int valorDígito = -(valor / índicePosición);
            if (valorDígito != 0 || ponerEnMarcha || índicePosición == 1) {
                Caracteres('0' + valorDígito);
                ponerEnMarcha = true;
            }
            valor %= índicePosición;
            índicePosición /= 10;
        }
    }

    static int leerSerie() {
        if ((Dispositivo.leerByteEntradaSalida(0x3fd) & 1) != 0) return Dispositivo.leerByteEntradaSalida(0x3f8);
        return -1;
    }
}
