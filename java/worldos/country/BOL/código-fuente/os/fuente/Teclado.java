// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Entrada PC/AT PS/2 por sondeo del conjunto traducido 1, con distribución estadounidense básica, Shift, Backspace y Enter. */
public final class Teclado {
    static boolean izquierdoDesplazar = false;
    static boolean derechoDesplazar = false;
    static boolean valorExtensión = false;
    static String valorPredeterminado = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String valorDesplazar = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int leer() {
        int valorEstadoValor = Dispositivo.leerByteEntradaSalida(0x64);
        if ((valorEstadoValor & 1) == 0) return -1;
        int valor = Dispositivo.leerByteEntradaSalida(0x60);
        if ((valorEstadoValor & 0x20) != 0) return -1;
        if (valor == 0xe0 || valor == 0xe1) { valorExtensión = true; return -1; }
        if (valorExtensión) { valorExtensión = false; return -1; }
        if (valor == 42 || valor == 170) { izquierdoDesplazar = valor == 42; return -1; }
        if (valor == 54 || valor == 182) { derechoDesplazar = valor == 54; return -1; }
        if (valor >= valorPredeterminado.length()) return -1;
        int Caracteres = (izquierdoDesplazar || derechoDesplazar) ? valorDesplazar.charAt(valor) : valorPredeterminado.charAt(valor);
        return Caracteres == 0 ? -1 : Caracteres;
    }
}
