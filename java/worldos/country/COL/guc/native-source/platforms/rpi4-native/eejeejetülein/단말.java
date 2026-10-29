// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int ajutuu) {
        if (ajutuu < 0x80) 보드.직렬쓰기(ajutuu);
        else if (ajutuu < 0x800) {
            보드.직렬쓰기(0xc0 | (ajutuu >> 6)); 보드.직렬쓰기(0x80 | (ajutuu & 63));
        } else if (ajutuu < 0x10000) {
            보드.직렬쓰기(0xe0 | (ajutuu >> 12)); 보드.직렬쓰기(0x80 | ((ajutuu >> 6) & 63)); 보드.직렬쓰기(0x80 | (ajutuu & 63));
        } else {
            보드.직렬쓰기(0xf0 | (ajutuu >> 18)); 보드.직렬쓰기(0x80 | ((ajutuu >> 12) & 63));
            보드.직렬쓰기(0x80 | ((ajutuu >> 6) & 63)); 보드.직렬쓰기(0x80 | (ajutuu & 63));
        }
    }
    static void ashajaa(String 글) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 글.length(); ee_iyatialujuna++) {
            int ajutuu = 글.charAt(ee_iyatialujuna);
            if (ajutuu >= 0xd800 && ajutuu <= 0xdbff && ee_iyatialujuna + 1 < 글.length()) {
                int 아래 = 글.charAt(ee_iyatialujuna + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    ajutuu = 0x10000 + ((ajutuu - 0xd800) << 10) + 아래 - 0xdc00; ee_iyatialujuna++;
                }
            }
            if (ajutuu >= 0xd800 && ajutuu <= 0xdfff) ajutuu = 0xfffd;
            문자(ajutuu);
        }
    }
    static void 수(int ajutuu) {
        if (ajutuu < 0) 문자('-'); else ajutuu = -ajutuu;
        int 자리 = 1000000000;
        boolean 시작 = false;
        while (자리 > 0) {
            int 숫자 = -(ajutuu / 자리);
            if (숫자 != 0 || 시작 || 자리 == 1) { 문자('0' + 숫자); 시작 = true; }
            ajutuu %= 자리; 자리 /= 10;
        }
    }
}
