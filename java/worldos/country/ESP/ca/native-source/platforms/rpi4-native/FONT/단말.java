// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALOR) {
        if (VALOR < 0x80) Tauler.직렬쓰기(VALOR);
        else if (VALOR < 0x800) {
            Tauler.직렬쓰기(0xc0 | (VALOR >> 6)); Tauler.직렬쓰기(0x80 | (VALOR & 63));
        } else if (VALOR < 0x10000) {
            Tauler.직렬쓰기(0xe0 | (VALOR >> 12)); Tauler.직렬쓰기(0x80 | ((VALOR >> 6) & 63)); Tauler.직렬쓰기(0x80 | (VALOR & 63));
        } else {
            Tauler.직렬쓰기(0xf0 | (VALOR >> 18)); Tauler.직렬쓰기(0x80 | ((VALOR >> 12) & 63));
            Tauler.직렬쓰기(0x80 | ((VALOR >> 6) & 63)); Tauler.직렬쓰기(0x80 | (VALOR & 63));
        }
    }
    static void Escriptura(String SMS) {
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int VALOR = SMS.charAt(INDEX);
            if (VALOR >= 0xd800 && VALOR <= 0xdbff && INDEX + 1 < SMS.length()) {
                int 아래 = SMS.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALOR = 0x10000 + ((VALOR - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (VALOR >= 0xd800 && VALOR <= 0xdfff) VALOR = 0xfffd;
            문자(VALOR);
        }
    }
    static void 수(int VALOR) {
        if (VALOR < 0) 문자('-'); else VALOR = -VALOR;
        int càrrec_INDEX = 1000000000;
        boolean Executa_2 = false;
        while (càrrec_INDEX > 0) {
            int dígit_VALOR = -(VALOR / càrrec_INDEX);
            if (dígit_VALOR != 0 || Executa_2 || càrrec_INDEX == 1) { 문자('0' + dígit_VALOR); Executa_2 = true; }
            VALOR %= càrrec_INDEX; càrrec_INDEX /= 10;
        }
    }
}
