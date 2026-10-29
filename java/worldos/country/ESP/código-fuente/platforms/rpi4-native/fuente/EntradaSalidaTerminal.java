// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class EntradaSalidaTerminal {
    static void Caracteres(int valor) {
        if (valor < 0x80) Placa.escribirSerie(valor);
        else if (valor < 0x800) {
            Placa.escribirSerie(0xc0 | (valor >> 6)); Placa.escribirSerie(0x80 | (valor & 63));
        } else if (valor < 0x10000) {
            Placa.escribirSerie(0xe0 | (valor >> 12)); Placa.escribirSerie(0x80 | ((valor >> 6) & 63)); Placa.escribirSerie(0x80 | (valor & 63));
        } else {
            Placa.escribirSerie(0xf0 | (valor >> 18)); Placa.escribirSerie(0x80 | ((valor >> 12) & 63));
            Placa.escribirSerie(0x80 | ((valor >> 6) & 63)); Placa.escribirSerie(0x80 | (valor & 63));
        }
    }
    static void escribir(String texto) {
        for (int número = 0; número < texto.length(); número++) {
            int valor = texto.charAt(número);
            if (valor >= 0xd800 && valor <= 0xdbff && número + 1 < texto.length()) {
                int valorExtremoInferior = texto.charAt(número + 1);
                if (valorExtremoInferior >= 0xdc00 && valorExtremoInferior <= 0xdfff) {
                    valor = 0x10000 + ((valor - 0xd800) << 10) + valorExtremoInferior - 0xdc00; número++;
                }
            }
            if (valor >= 0xd800 && valor <= 0xdfff) valor = 0xfffd;
            Caracteres(valor);
        }
    }
    static void númeroValor(int valor) {
        if (valor < 0) Caracteres('-'); else valor = -valor;
        int índicePosición = 1000000000;
        boolean ponerEnMarcha = false;
        while (índicePosición > 0) {
            int valorDígito = -(valor / índicePosición);
            if (valorDígito != 0 || ponerEnMarcha || índicePosición == 1) { Caracteres('0' + valorDígito); ponerEnMarcha = true; }
            valor %= índicePosición; índicePosición /= 10;
        }
    }
}
