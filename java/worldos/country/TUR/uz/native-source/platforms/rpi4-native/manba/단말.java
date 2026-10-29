// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) yozuv_taxtasi.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            yozuv_taxtasi.직렬쓰기(0xc0 | (VALUE >> 6)); yozuv_taxtasi.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            yozuv_taxtasi.직렬쓰기(0xe0 | (VALUE >> 12)); yozuv_taxtasi.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); yozuv_taxtasi.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            yozuv_taxtasi.직렬쓰기(0xf0 | (VALUE >> 18)); yozuv_taxtasi.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            yozuv_taxtasi.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); yozuv_taxtasi.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Yozish(String Matn) {
        for (int INDEX = 0; INDEX < Matn.length(); INDEX++) {
            int VALUE = Matn.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Matn.length()) {
                int 아래 = Matn.charAt(INDEX + 1);
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
        int holat_INDEX = 1000000000;
        boolean Bajarish = false;
        while (holat_INDEX > 0) {
            int raqam_VALUE = -(VALUE / holat_INDEX);
            if (raqam_VALUE != 0 || Bajarish || holat_INDEX == 1) { 문자('0' + raqam_VALUE); Bajarish = true; }
            VALUE %= holat_INDEX; holat_INDEX /= 10;
        }
    }
}
