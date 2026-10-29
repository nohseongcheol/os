// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) Papan.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            Papan.직렬쓰기(0xc0 | (VALUE >> 6)); Papan.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            Papan.직렬쓰기(0xe0 | (VALUE >> 12)); Papan.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Papan.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            Papan.직렬쓰기(0xf0 | (VALUE >> 18)); Papan.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            Papan.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Papan.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Tulis(String Teks) {
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
        int jawatan_INDEX = 1000000000;
        boolean Jalan = false;
        while (jawatan_INDEX > 0) {
            int digit_VALUE = -(VALUE / jawatan_INDEX);
            if (digit_VALUE != 0 || Jalan || jawatan_INDEX == 1) { 문자('0' + digit_VALUE); Jalan = true; }
            VALUE %= jawatan_INDEX; jawatan_INDEX /= 10;
        }
    }
}
