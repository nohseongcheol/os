// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int değer) {
        if (değer < 0x80) Pano.직렬쓰기(değer);
        else if (değer < 0x800) {
            Pano.직렬쓰기(0xc0 | (değer >> 6)); Pano.직렬쓰기(0x80 | (değer & 63));
        } else if (değer < 0x10000) {
            Pano.직렬쓰기(0xe0 | (değer >> 12)); Pano.직렬쓰기(0x80 | ((değer >> 6) & 63)); Pano.직렬쓰기(0x80 | (değer & 63));
        } else {
            Pano.직렬쓰기(0xf0 | (değer >> 18)); Pano.직렬쓰기(0x80 | ((değer >> 12) & 63));
            Pano.직렬쓰기(0x80 | ((değer >> 6) & 63)); Pano.직렬쓰기(0x80 | (değer & 63));
        }
    }
    static void Yazma(String metin) {
        for (int Dizin = 0; Dizin < metin.length(); Dizin++) {
            int değer = metin.charAt(Dizin);
            if (değer >= 0xd800 && değer <= 0xdbff && Dizin + 1 < metin.length()) {
                int 아래 = metin.charAt(Dizin + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    değer = 0x10000 + ((değer - 0xd800) << 10) + 아래 - 0xdc00; Dizin++;
                }
            }
            if (değer >= 0xd800 && değer <= 0xdfff) değer = 0xfffd;
            문자(değer);
        }
    }
    static void 수(int değer) {
        if (değer < 0) 문자('-'); else değer = -değer;
        int konum_dizini = 1000000000;
        boolean çalıştır = false;
        while (konum_dizini > 0) {
            int rakam_değer = -(değer / konum_dizini);
            if (rakam_değer != 0 || çalıştır || konum_dizini == 1) { 문자('0' + rakam_değer); çalıştır = true; }
            değer %= konum_dizini; konum_dizini /= 10;
        }
    }
}
