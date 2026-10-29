// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int uara) {
        if (uara < 0x80) papa.직렬쓰기(uara);
        else if (uara < 0x800) {
            papa.직렬쓰기(0xc0 | (uara >> 6)); papa.직렬쓰기(0x80 | (uara & 63));
        } else if (uara < 0x10000) {
            papa.직렬쓰기(0xe0 | (uara >> 12)); papa.직렬쓰기(0x80 | ((uara >> 6) & 63)); papa.직렬쓰기(0x80 | (uara & 63));
        } else {
            papa.직렬쓰기(0xf0 | (uara >> 18)); papa.직렬쓰기(0x80 | ((uara >> 12) & 63));
            papa.직렬쓰기(0x80 | ((uara >> 6) & 63)); papa.직렬쓰기(0x80 | (uara & 63));
        }
    }
    static void Tuhia(String Ngā_kupu) {
        for (int INDEX = 0; INDEX < Ngā_kupu.length(); INDEX++) {
            int uara = Ngā_kupu.charAt(INDEX);
            if (uara >= 0xd800 && uara <= 0xdbff && INDEX + 1 < Ngā_kupu.length()) {
                int 아래 = Ngā_kupu.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    uara = 0x10000 + ((uara - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (uara >= 0xd800 && uara <= 0xdfff) uara = 0xfffd;
            문자(uara);
        }
    }
    static void 수(int uara) {
        if (uara < 0) 문자('-'); else uara = -uara;
        int tūranga_INDEX = 1000000000;
        boolean whakahaere = false;
        while (tūranga_INDEX > 0) {
            int mati_uara = -(uara / tūranga_INDEX);
            if (mati_uara != 0 || whakahaere || tūranga_INDEX == 1) { 문자('0' + mati_uara); whakahaere = true; }
            uara %= tūranga_INDEX; tūranga_INDEX /= 10;
        }
    }
}
