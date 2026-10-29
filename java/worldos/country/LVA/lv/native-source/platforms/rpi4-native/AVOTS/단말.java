// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) Panelis.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            Panelis.직렬쓰기(0xc0 | (VALUE >> 6)); Panelis.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            Panelis.직렬쓰기(0xe0 | (VALUE >> 12)); Panelis.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Panelis.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            Panelis.직렬쓰기(0xf0 | (VALUE >> 18)); Panelis.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            Panelis.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Panelis.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Rakstīt(String Teksts) {
        for (int INDEX = 0; INDEX < Teksts.length(); INDEX++) {
            int VALUE = Teksts.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Teksts.length()) {
                int 아래 = Teksts.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALUE = 0x10000 + ((VALUE - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (VALUE >= 0xd800 && VALUE <= 0xdfff) VALUE = 0xfffd;
            문자(VALUE);
        }
    }
    static void numurs(int VALUE) {
        if (VALUE < 0) 문자('-'); else VALUE = -VALUE;
        int pozīcijas_indekss = 1000000000;
        boolean Palaist = false;
        while (pozīcijas_indekss > 0) {
            int cipars_VALUE = -(VALUE / pozīcijas_indekss);
            if (cipars_VALUE != 0 || Palaist || pozīcijas_indekss == 1) { 문자('0' + cipars_VALUE); Palaist = true; }
            VALUE %= pozīcijas_indekss; pozīcijas_indekss /= 10;
        }
    }
}
