// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) такта.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            такта.직렬쓰기(0xc0 | (VALUE >> 6)); такта.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            такта.직렬쓰기(0xe0 | (VALUE >> 12)); такта.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); такта.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            такта.직렬쓰기(0xf0 | (VALUE >> 18)); такта.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            такта.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); такта.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void язу(String Mäten) {
        for (int INDEX = 0; INDEX < Mäten.length(); INDEX++) {
            int VALUE = Mäten.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Mäten.length()) {
                int 아래 = Mäten.charAt(INDEX + 1);
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
        int урнаштыру_INDEX = 1000000000;
        boolean эшләтү = false;
        while (урнаштыру_INDEX > 0) {
            int сан_VALUE = -(VALUE / урнаштыру_INDEX);
            if (сан_VALUE != 0 || эшләтү || урнаштыру_INDEX == 1) { 문자('0' + сан_VALUE); эшләтү = true; }
            VALUE %= урнаштыру_INDEX; урнаштыру_INDEX /= 10;
        }
    }
}
