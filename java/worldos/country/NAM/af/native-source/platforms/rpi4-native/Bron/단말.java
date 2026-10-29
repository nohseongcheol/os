// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) bord.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            bord.직렬쓰기(0xc0 | (VALUE >> 6)); bord.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            bord.직렬쓰기(0xe0 | (VALUE >> 12)); bord.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); bord.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            bord.직렬쓰기(0xf0 | (VALUE >> 18)); bord.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            bord.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); bord.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Skryf(String Teks) {
        for (int INDEX = 0; INDEX < Teks.length(); INDEX++) {
            int VALUE = Teks.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Teks.length()) {
                int 아래 = Teks.charAt(INDEX + 1);
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
        int plaas_INDEX = 1000000000;
        boolean Loop = false;
        while (plaas_INDEX > 0) {
            int syfer_VALUE = -(VALUE / plaas_INDEX);
            if (syfer_VALUE != 0 || Loop || plaas_INDEX == 1) { 문자('0' + syfer_VALUE); Loop = true; }
            VALUE %= plaas_INDEX; plaas_INDEX /= 10;
        }
    }
}
