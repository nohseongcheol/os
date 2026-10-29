// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int HODNOTA) {
        if (HODNOTA < 0x80) Panel.직렬쓰기(HODNOTA);
        else if (HODNOTA < 0x800) {
            Panel.직렬쓰기(0xc0 | (HODNOTA >> 6)); Panel.직렬쓰기(0x80 | (HODNOTA & 63));
        } else if (HODNOTA < 0x10000) {
            Panel.직렬쓰기(0xe0 | (HODNOTA >> 12)); Panel.직렬쓰기(0x80 | ((HODNOTA >> 6) & 63)); Panel.직렬쓰기(0x80 | (HODNOTA & 63));
        } else {
            Panel.직렬쓰기(0xf0 | (HODNOTA >> 18)); Panel.직렬쓰기(0x80 | ((HODNOTA >> 12) & 63));
            Panel.직렬쓰기(0x80 | ((HODNOTA >> 6) & 63)); Panel.직렬쓰기(0x80 | (HODNOTA & 63));
        }
    }
    static void Zápis(String text) {
        for (int INDEX = 0; INDEX < text.length(); INDEX++) {
            int HODNOTA = text.charAt(INDEX);
            if (HODNOTA >= 0xd800 && HODNOTA <= 0xdbff && INDEX + 1 < text.length()) {
                int 아래 = text.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    HODNOTA = 0x10000 + ((HODNOTA - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (HODNOTA >= 0xd800 && HODNOTA <= 0xdfff) HODNOTA = 0xfffd;
            문자(HODNOTA);
        }
    }
    static void číslo(int HODNOTA) {
        if (HODNOTA < 0) 문자('-'); else HODNOTA = -HODNOTA;
        int poziční_index = 1000000000;
        boolean Spustit_2 = false;
        while (poziční_index > 0) {
            int číslice_HODNOTA = -(HODNOTA / poziční_index);
            if (číslice_HODNOTA != 0 || Spustit_2 || poziční_index == 1) { 문자('0' + číslice_HODNOTA); Spustit_2 = true; }
            HODNOTA %= poziční_index; poziční_index /= 10;
        }
    }
}
