// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) Panel.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            Panel.직렬쓰기(0xc0 | (VALUE >> 6)); Panel.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            Panel.직렬쓰기(0xe0 | (VALUE >> 12)); Panel.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Panel.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            Panel.직렬쓰기(0xf0 | (VALUE >> 18)); Panel.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            Panel.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Panel.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Zápis(String Spracovanie_textu) {
        for (int INDEX = 0; INDEX < Spracovanie_textu.length(); INDEX++) {
            int VALUE = Spracovanie_textu.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Spracovanie_textu.length()) {
                int 아래 = Spracovanie_textu.charAt(INDEX + 1);
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
        int pozičný_index = 1000000000;
        boolean Spustiť_2 = false;
        while (pozičný_index > 0) {
            int číslica_VALUE = -(VALUE / pozičný_index);
            if (číslica_VALUE != 0 || Spustiť_2 || pozičný_index == 1) { 문자('0' + číslica_VALUE); Spustiť_2 = true; }
            VALUE %= pozičný_index; pozičný_index /= 10;
        }
    }
}
