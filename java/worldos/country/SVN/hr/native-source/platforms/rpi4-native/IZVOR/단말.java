// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) pano.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            pano.직렬쓰기(0xc0 | (VALUE >> 6)); pano.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            pano.직렬쓰기(0xe0 | (VALUE >> 12)); pano.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); pano.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            pano.직렬쓰기(0xf0 | (VALUE >> 18)); pano.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            pano.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); pano.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Zapisuj(String Tekst) {
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            int VALUE = Tekst.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Tekst.length()) {
                int 아래 = Tekst.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALUE = 0x10000 + ((VALUE - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (VALUE >= 0xd800 && VALUE <= 0xdfff) VALUE = 0xfffd;
            문자(VALUE);
        }
    }
    static void 수(int VALUE) {
        if (VALUE < 0) 문자('-'); else VALUE = -VALUE;
        int indeks_položaja = 1000000000;
        boolean Pokreni = false;
        while (indeks_položaja > 0) {
            int znamenka_VALUE = -(VALUE / indeks_položaja);
            if (znamenka_VALUE != 0 || Pokreni || indeks_položaja == 1) { 문자('0' + znamenka_VALUE); Pokreni = true; }
            VALUE %= indeks_položaja; indeks_položaja /= 10;
        }
    }
}
