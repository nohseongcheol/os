// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int baha) {
        if (baha < 0x80) 보드.직렬쓰기(baha);
        else if (baha < 0x800) {
            보드.직렬쓰기(0xc0 | (baha >> 6)); 보드.직렬쓰기(0x80 | (baha & 63));
        } else if (baha < 0x10000) {
            보드.직렬쓰기(0xe0 | (baha >> 12)); 보드.직렬쓰기(0x80 | ((baha >> 6) & 63)); 보드.직렬쓰기(0x80 | (baha & 63));
        } else {
            보드.직렬쓰기(0xf0 | (baha >> 18)); 보드.직렬쓰기(0x80 | ((baha >> 12) & 63));
            보드.직렬쓰기(0x80 | ((baha >> 6) & 63)); 보드.직렬쓰기(0x80 | (baha & 63));
        }
    }
    static void Ýaz(String Metin) {
        for (int indeks = 0; indeks < Metin.length(); indeks++) {
            int baha = Metin.charAt(indeks);
            if (baha >= 0xd800 && baha <= 0xdbff && indeks + 1 < Metin.length()) {
                int 아래 = Metin.charAt(indeks + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    baha = 0x10000 + ((baha - 0xd800) << 10) + 아래 - 0xdc00; indeks++;
                }
            }
            if (baha >= 0xd800 && baha <= 0xdfff) baha = 0xfffd;
            문자(baha);
        }
    }
    static void 수(int baha) {
        if (baha < 0) 문자('-'); else baha = -baha;
        int 자리 = 1000000000;
        boolean Bitir = false;
        while (자리 > 0) {
            int san_baha = -(baha / 자리);
            if (san_baha != 0 || Bitir || 자리 == 1) { 문자('0' + san_baha); Bitir = true; }
            baha %= 자리; 자리 /= 10;
        }
    }
}
