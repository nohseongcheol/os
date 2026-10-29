// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) Tabla.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            Tabla.직렬쓰기(0xc0 | (VALUE >> 6)); Tabla.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            Tabla.직렬쓰기(0xe0 | (VALUE >> 12)); Tabla.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Tabla.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            Tabla.직렬쓰기(0xf0 | (VALUE >> 18)); Tabla.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            Tabla.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Tabla.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void 쓰기(String SMS) {
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int VALUE = SMS.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < SMS.length()) {
                int 아래 = SMS.charAt(INDEX + 1);
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
        int indeks_pozicije = 1000000000;
        boolean koristiti = false;
        while (indeks_pozicije > 0) {
            int cifra_VALUE = -(VALUE / indeks_pozicije);
            if (cifra_VALUE != 0 || koristiti || indeks_pozicije == 1) { 문자('0' + cifra_VALUE); koristiti = true; }
            VALUE %= indeks_pozicije; indeks_pozicije /= 10;
        }
    }
}
