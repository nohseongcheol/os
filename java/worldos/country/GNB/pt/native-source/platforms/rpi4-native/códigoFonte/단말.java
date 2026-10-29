// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALOR) {
        if (VALOR < 0x80) Quadro.직렬쓰기(VALOR);
        else if (VALOR < 0x800) {
            Quadro.직렬쓰기(0xc0 | (VALOR >> 6)); Quadro.직렬쓰기(0x80 | (VALOR & 63));
        } else if (VALOR < 0x10000) {
            Quadro.직렬쓰기(0xe0 | (VALOR >> 12)); Quadro.직렬쓰기(0x80 | ((VALOR >> 6) & 63)); Quadro.직렬쓰기(0x80 | (VALOR & 63));
        } else {
            Quadro.직렬쓰기(0xf0 | (VALOR >> 18)); Quadro.직렬쓰기(0x80 | ((VALOR >> 12) & 63));
            Quadro.직렬쓰기(0x80 | ((VALOR >> 6) & 63)); Quadro.직렬쓰기(0x80 | (VALOR & 63));
        }
    }
    static void Escrita(String texto) {
        for (int ÍNDICE = 0; ÍNDICE < texto.length(); ÍNDICE++) {
            int VALOR = texto.charAt(ÍNDICE);
            if (VALOR >= 0xd800 && VALOR <= 0xdbff && ÍNDICE + 1 < texto.length()) {
                int 아래 = texto.charAt(ÍNDICE + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALOR = 0x10000 + ((VALOR - 0xd800) << 10) + 아래 - 0xdc00; ÍNDICE++;
                }
            }
            if (VALOR >= 0xd800 && VALOR <= 0xdfff) VALOR = 0xfffd;
            문자(VALOR);
        }
    }
    static void número(int VALOR) {
        if (VALOR < 0) 문자('-'); else VALOR = -VALOR;
        int cargo_ÍNDICE = 1000000000;
        boolean iniciar = false;
        while (cargo_ÍNDICE > 0) {
            int dígito_VALOR = -(VALOR / cargo_ÍNDICE);
            if (dígito_VALOR != 0 || iniciar || cargo_ÍNDICE == 1) { 문자('0' + dígito_VALOR); iniciar = true; }
            VALOR %= cargo_ÍNDICE; cargo_ÍNDICE /= 10;
        }
    }
}
