// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) bwrdd.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            bwrdd.직렬쓰기(0xc0 | (VALUE >> 6)); bwrdd.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            bwrdd.직렬쓰기(0xe0 | (VALUE >> 12)); bwrdd.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); bwrdd.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            bwrdd.직렬쓰기(0xf0 | (VALUE >> 18)); bwrdd.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            bwrdd.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); bwrdd.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Ysgrifennu(String Testun) {
        for (int INDEX = 0; INDEX < Testun.length(); INDEX++) {
            int VALUE = Testun.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Testun.length()) {
                int 아래 = Testun.charAt(INDEX + 1);
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
        int safle_INDEX = 1000000000;
        boolean Gweithredu_2 = false;
        while (safle_INDEX > 0) {
            int digid_VALUE = -(VALUE / safle_INDEX);
            if (digid_VALUE != 0 || Gweithredu_2 || safle_INDEX == 1) { 문자('0' + digid_VALUE); Gweithredu_2 = true; }
            VALUE %= safle_INDEX; safle_INDEX /= 10;
        }
    }
}
