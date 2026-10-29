// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALOR) {
        if (VALOR < 0x80) Panel.직렬쓰기(VALOR);
        else if (VALOR < 0x800) {
            Panel.직렬쓰기(0xc0 | (VALOR >> 6)); Panel.직렬쓰기(0x80 | (VALOR & 63));
        } else if (VALOR < 0x10000) {
            Panel.직렬쓰기(0xe0 | (VALOR >> 12)); Panel.직렬쓰기(0x80 | ((VALOR >> 6) & 63)); Panel.직렬쓰기(0x80 | (VALOR & 63));
        } else {
            Panel.직렬쓰기(0xf0 | (VALOR >> 18)); Panel.직렬쓰기(0x80 | ((VALOR >> 12) & 63));
            Panel.직렬쓰기(0x80 | ((VALOR >> 6) & 63)); Panel.직렬쓰기(0x80 | (VALOR & 63));
        }
    }
    static void Escritura(String Texto) {
        for (int ÍNDICE = 0; ÍNDICE < Texto.length(); ÍNDICE++) {
            int VALOR = Texto.charAt(ÍNDICE);
            if (VALOR >= 0xd800 && VALOR <= 0xdbff && ÍNDICE + 1 < Texto.length()) {
                int 아래 = Texto.charAt(ÍNDICE + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALOR = 0x10000 + ((VALOR - 0xd800) << 10) + 아래 - 0xdc00; ÍNDICE++;
                }
            }
            if (VALOR >= 0xd800 && VALOR <= 0xdfff) VALOR = 0xfffd;
            문자(VALOR);
        }
    }
    static void 수(int VALOR) {
        if (VALOR < 0) 문자('-'); else VALOR = -VALOR;
        int cargo_ÍNDICE = 1000000000;
        boolean Executar_2 = false;
        while (cargo_ÍNDICE > 0) {
            int díxito_VALOR = -(VALOR / cargo_ÍNDICE);
            if (díxito_VALOR != 0 || Executar_2 || cargo_ÍNDICE == 1) { 문자('0' + díxito_VALOR); Executar_2 = true; }
            VALOR %= cargo_ÍNDICE; cargo_ÍNDICE /= 10;
        }
    }
}
