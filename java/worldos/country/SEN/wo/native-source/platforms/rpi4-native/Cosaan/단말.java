// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int xëyma) {
        if (xëyma < 0x80) 보드.직렬쓰기(xëyma);
        else if (xëyma < 0x800) {
            보드.직렬쓰기(0xc0 | (xëyma >> 6)); 보드.직렬쓰기(0x80 | (xëyma & 63));
        } else if (xëyma < 0x10000) {
            보드.직렬쓰기(0xe0 | (xëyma >> 12)); 보드.직렬쓰기(0x80 | ((xëyma >> 6) & 63)); 보드.직렬쓰기(0x80 | (xëyma & 63));
        } else {
            보드.직렬쓰기(0xf0 | (xëyma >> 18)); 보드.직렬쓰기(0x80 | ((xëyma >> 12) & 63));
            보드.직렬쓰기(0x80 | ((xëyma >> 6) & 63)); 보드.직렬쓰기(0x80 | (xëyma & 63));
        }
    }
    static void biir(String Tekst) {
        for (int àlluwa_tur = 0; àlluwa_tur < Tekst.length(); àlluwa_tur++) {
            int xëyma = Tekst.charAt(àlluwa_tur);
            if (xëyma >= 0xd800 && xëyma <= 0xdbff && àlluwa_tur + 1 < Tekst.length()) {
                int 아래 = Tekst.charAt(àlluwa_tur + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    xëyma = 0x10000 + ((xëyma - 0xd800) << 10) + 아래 - 0xdc00; àlluwa_tur++;
                }
            }
            if (xëyma >= 0xd800 && xëyma <= 0xdfff) xëyma = 0xfffd;
            문자(xëyma);
        }
    }
    static void 수(int xëyma) {
        if (xëyma < 0) 문자('-'); else xëyma = -xëyma;
        int 자리 = 1000000000;
        boolean daw = false;
        while (자리 > 0) {
            int siifar_xëyma = -(xëyma / 자리);
            if (siifar_xëyma != 0 || daw || 자리 == 1) { 문자('0' + siifar_xëyma); daw = true; }
            xëyma %= 자리; 자리 /= 10;
        }
    }
}
