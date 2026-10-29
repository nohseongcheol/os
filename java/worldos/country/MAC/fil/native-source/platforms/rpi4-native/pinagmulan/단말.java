// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) board.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            board.직렬쓰기(0xc0 | (VALUE >> 6)); board.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            board.직렬쓰기(0xe0 | (VALUE >> 12)); board.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); board.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            board.직렬쓰기(0xf0 | (VALUE >> 18)); board.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            board.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); board.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void sumulat(String SMS) {
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
        int posisyon_INDEX = 1000000000;
        boolean run = false;
        while (posisyon_INDEX > 0) {
            int digit_VALUE = -(VALUE / posisyon_INDEX);
            if (digit_VALUE != 0 || run || posisyon_INDEX == 1) { 문자('0' + digit_VALUE); run = true; }
            VALUE %= posisyon_INDEX; posisyon_INDEX /= 10;
        }
    }
}
