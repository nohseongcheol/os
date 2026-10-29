// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) bretti.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            bretti.직렬쓰기(0xc0 | (VALUE >> 6)); bretti.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            bretti.직렬쓰기(0xe0 | (VALUE >> 12)); bretti.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); bretti.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            bretti.직렬쓰기(0xf0 | (VALUE >> 18)); bretti.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            bretti.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); bretti.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Skrift(String Texti) {
        for (int INDEX = 0; INDEX < Texti.length(); INDEX++) {
            int VALUE = Texti.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Texti.length()) {
                int 아래 = Texti.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALUE = 0x10000 + ((VALUE - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (VALUE >= 0xd800 && VALUE <= 0xdfff) VALUE = 0xfffd;
            문자(VALUE);
        }
    }
    static void númer(int VALUE) {
        if (VALUE < 0) 문자('-'); else VALUE = -VALUE;
        int staða_INDEX = 1000000000;
        boolean Keyra_2 = false;
        while (staða_INDEX > 0) {
            int tölustafur_VALUE = -(VALUE / staða_INDEX);
            if (tölustafur_VALUE != 0 || Keyra_2 || staða_INDEX == 1) { 문자('0' + tölustafur_VALUE); Keyra_2 = true; }
            VALUE %= staða_INDEX; staða_INDEX /= 10;
        }
    }
}
