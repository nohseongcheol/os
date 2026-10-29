// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) Lenta.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            Lenta.직렬쓰기(0xc0 | (VALUE >> 6)); Lenta.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            Lenta.직렬쓰기(0xe0 | (VALUE >> 12)); Lenta.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Lenta.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            Lenta.직렬쓰기(0xf0 | (VALUE >> 18)); Lenta.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            Lenta.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Lenta.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Rašymas(String Tekstas) {
        for (int INDEX = 0; INDEX < Tekstas.length(); INDEX++) {
            int VALUE = Tekstas.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Tekstas.length()) {
                int 아래 = Tekstas.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALUE = 0x10000 + ((VALUE - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (VALUE >= 0xd800 && VALUE <= 0xdfff) VALUE = 0xfffd;
            문자(VALUE);
        }
    }
    static void numeris(int VALUE) {
        if (VALUE < 0) 문자('-'); else VALUE = -VALUE;
        int vietos_rodyklė = 1000000000;
        boolean Paleisti = false;
        while (vietos_rodyklė > 0) {
            int skaitmuo_VALUE = -(VALUE / vietos_rodyklė);
            if (skaitmuo_VALUE != 0 || Paleisti || vietos_rodyklė == 1) { 문자('0' + skaitmuo_VALUE); Paleisti = true; }
            VALUE %= vietos_rodyklė; vietos_rodyklė /= 10;
        }
    }
}
