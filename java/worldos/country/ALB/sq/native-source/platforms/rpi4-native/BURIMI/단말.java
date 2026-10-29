// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) panel.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            panel.직렬쓰기(0xc0 | (VALUE >> 6)); panel.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            panel.직렬쓰기(0xe0 | (VALUE >> 12)); panel.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); panel.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            panel.직렬쓰기(0xf0 | (VALUE >> 18)); panel.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            panel.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); panel.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Shkrimi(String Teksti) {
        for (int INDEX = 0; INDEX < Teksti.length(); INDEX++) {
            int VALUE = Teksti.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Teksti.length()) {
                int 아래 = Teksti.charAt(INDEX + 1);
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
        int pozicioni_INDEX = 1000000000;
        boolean Ekzekuto = false;
        while (pozicioni_INDEX > 0) {
            int shifër_VALUE = -(VALUE / pozicioni_INDEX);
            if (shifër_VALUE != 0 || Ekzekuto || pozicioni_INDEX == 1) { 문자('0' + shifër_VALUE); Ekzekuto = true; }
            VALUE %= pozicioni_INDEX; pozicioni_INDEX /= 10;
        }
    }
}
