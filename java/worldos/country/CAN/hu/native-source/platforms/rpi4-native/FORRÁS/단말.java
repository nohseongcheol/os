// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int ÉRTÉK) {
        if (ÉRTÉK < 0x80) fal.직렬쓰기(ÉRTÉK);
        else if (ÉRTÉK < 0x800) {
            fal.직렬쓰기(0xc0 | (ÉRTÉK >> 6)); fal.직렬쓰기(0x80 | (ÉRTÉK & 63));
        } else if (ÉRTÉK < 0x10000) {
            fal.직렬쓰기(0xe0 | (ÉRTÉK >> 12)); fal.직렬쓰기(0x80 | ((ÉRTÉK >> 6) & 63)); fal.직렬쓰기(0x80 | (ÉRTÉK & 63));
        } else {
            fal.직렬쓰기(0xf0 | (ÉRTÉK >> 18)); fal.직렬쓰기(0x80 | ((ÉRTÉK >> 12) & 63));
            fal.직렬쓰기(0x80 | ((ÉRTÉK >> 6) & 63)); fal.직렬쓰기(0x80 | (ÉRTÉK & 63));
        }
    }
    static void Írás(String Szöveg) {
        for (int INDEX = 0; INDEX < Szöveg.length(); INDEX++) {
            int ÉRTÉK = Szöveg.charAt(INDEX);
            if (ÉRTÉK >= 0xd800 && ÉRTÉK <= 0xdbff && INDEX + 1 < Szöveg.length()) {
                int 아래 = Szöveg.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    ÉRTÉK = 0x10000 + ((ÉRTÉK - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (ÉRTÉK >= 0xd800 && ÉRTÉK <= 0xdfff) ÉRTÉK = 0xfffd;
            문자(ÉRTÉK);
        }
    }
    static void szám(int ÉRTÉK) {
        if (ÉRTÉK < 0) 문자('-'); else ÉRTÉK = -ÉRTÉK;
        int helyzetindex = 1000000000;
        boolean Futtatás = false;
        while (helyzetindex > 0) {
            int számjegy_ÉRTÉK = -(ÉRTÉK / helyzetindex);
            if (számjegy_ÉRTÉK != 0 || Futtatás || helyzetindex == 1) { 문자('0' + számjegy_ÉRTÉK); Futtatás = true; }
            ÉRTÉK %= helyzetindex; helyzetindex /= 10;
        }
    }
}
