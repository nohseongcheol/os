// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) Tavle.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            Tavle.직렬쓰기(0xc0 | (VALUE >> 6)); Tavle.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            Tavle.직렬쓰기(0xe0 | (VALUE >> 12)); Tavle.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Tavle.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            Tavle.직렬쓰기(0xf0 | (VALUE >> 18)); Tavle.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            Tavle.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Tavle.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Skriv(String Tekst) {
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
        int plassere_INDEX = 1000000000;
        boolean Køyr_2 = false;
        while (plassere_INDEX > 0) {
            int siffer_VALUE = -(VALUE / plassere_INDEX);
            if (siffer_VALUE != 0 || Køyr_2 || plassere_INDEX == 1) { 문자('0' + siffer_VALUE); Køyr_2 = true; }
            VALUE %= plassere_INDEX; plassere_INDEX /= 10;
        }
    }
}
