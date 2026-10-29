// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) табла.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            табла.직렬쓰기(0xc0 | (VALUE >> 6)); табла.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            табла.직렬쓰기(0xe0 | (VALUE >> 12)); табла.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); табла.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            табла.직렬쓰기(0xf0 | (VALUE >> 18)); табла.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            табла.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); табла.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Запиши(String Текст) {
        for (int INDEX = 0; INDEX < Текст.length(); INDEX++) {
            int VALUE = Текст.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Текст.length()) {
                int 아래 = Текст.charAt(INDEX + 1);
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
        int позиционирање_INDEX = 1000000000;
        boolean Изврши_2 = false;
        while (позиционирање_INDEX > 0) {
            int цифра_VALUE = -(VALUE / позиционирање_INDEX);
            if (цифра_VALUE != 0 || Изврши_2 || позиционирање_INDEX == 1) { 문자('0' + цифра_VALUE); Изврши_2 = true; }
            VALUE %= позиционирање_INDEX; позиционирање_INDEX /= 10;
        }
    }
}
