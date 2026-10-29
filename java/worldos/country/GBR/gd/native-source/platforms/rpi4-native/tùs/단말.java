// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) bòrd.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            bòrd.직렬쓰기(0xc0 | (VALUE >> 6)); bòrd.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            bòrd.직렬쓰기(0xe0 | (VALUE >> 12)); bòrd.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); bòrd.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            bòrd.직렬쓰기(0xf0 | (VALUE >> 18)); bòrd.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            bòrd.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); bòrd.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void sgrìobh(String SMS) {
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
        int suidhich_INDEX = 1000000000;
        boolean ruith = false;
        while (suidhich_INDEX > 0) {
            int figear_VALUE = -(VALUE / suidhich_INDEX);
            if (figear_VALUE != 0 || ruith || suidhich_INDEX == 1) { 문자('0' + figear_VALUE); ruith = true; }
            VALUE %= suidhich_INDEX; suidhich_INDEX /= 10;
        }
    }
}
