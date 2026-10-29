// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Salida común de las herramientas invitadas y tratamiento de nombres de archivo ASCII. */
public final class HerramientaJava {
    /** Convierte un arreglo de bytes UTF-8 en unidades UTF-16 dentro del mismo arreglo. Rechaza entradas mal formadas. */
    static int decodificarFuente(int[] Datos, int longitud) {
        int leer = 0, escribir = 0;
        if (longitud >= 3 && Datos[0] == 239 && Datos[1] == 187 && Datos[2] == 191) leer = 3;
        while (leer < longitud) {
            int valor = Datos[leer++], númeroValor = 0, valorMínimo = 0;
            if (valor >= 194 && valor <= 223) { númeroValor = 1; valorMínimo = 128; valor &= 31; }
            else if (valor >= 224 && valor <= 239) { númeroValor = 2; valorMínimo = 2048; valor &= 15; }
            else if (valor >= 240 && valor <= 244) { númeroValor = 3; valorMínimo = 65536; valor &= 7; }
            else if (valor >= 128 || valor < 0) return -1;
            if (númeroValor > longitud - leer) return -1;
            for (int i = 0; i < númeroValor; i++) {
                int elementoListaSiguiente = Datos[leer++]; if ((elementoListaSiguiente & 192) != 128) return -1;
                valor = (valor << 6) | (elementoListaSiguiente & 63);
            }
            if (valor < valorMínimo || valor > 0x10ffff || (valor >= 0xd800 && valor <= 0xdfff)) return -1;
            if (valor >= 65536) { valor -= 65536; Datos[escribir++] = 0xd800 | (valor >> 10); Datos[escribir++] = 0xdc00 | (valor & 1023); }
            else Datos[escribir++] = valor;
        }
        return escribir;
    }
    static void escribirNúmero(int valor) {
        if (valor < 0) Usuario.escribirValorCarácter('-'); else valor = -valor;
        int índicePosición = 1000000000;
        boolean ponerEnMarcha = false;
        while (índicePosición != 0) {
            int númeroValor = -(valor / índicePosición);
            if (númeroValor != 0 || ponerEnMarcha || índicePosición == 1) { Usuario.escribirValorCarácter('0' + númeroValor); ponerEnMarcha = true; }
            valor %= índicePosición; índicePosición /= 10;
        }
    }
    static int nombre(int[] valorDestino, String original) {
        if (original.length() >= valorDestino.length) return -1;
        for (int númeroValor = 0; númeroValor < valorDestino.length; númeroValor++) valorDestino[númeroValor] = númeroValor < original.length() ? original.charAt(númeroValor) : 0;
        return original.length();
    }
    static boolean textoIgual(String operandoPrimero, String operandoSegundo) {
        if (operandoPrimero.length() != operandoSegundo.length()) return false;
        for (int númeroValor = 0; númeroValor < operandoPrimero.length(); númeroValor++) if (operandoPrimero.charAt(númeroValor) != operandoSegundo.charAt(númeroValor)) return false;
        return true;
    }
}
