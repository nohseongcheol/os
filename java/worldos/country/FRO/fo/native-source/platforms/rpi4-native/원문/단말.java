// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int 값) {
        if (값 < 0x80) 보드.직렬쓰기(값);
        else if (값 < 0x800) {
            보드.직렬쓰기(0xc0 | (값 >> 6)); 보드.직렬쓰기(0x80 | (값 & 63));
        } else if (값 < 0x10000) {
            보드.직렬쓰기(0xe0 | (값 >> 12)); 보드.직렬쓰기(0x80 | ((값 >> 6) & 63)); 보드.직렬쓰기(0x80 | (값 & 63));
        } else {
            보드.직렬쓰기(0xf0 | (값 >> 18)); 보드.직렬쓰기(0x80 | ((값 >> 12) & 63));
            보드.직렬쓰기(0x80 | ((값 >> 6) & 63)); 보드.직렬쓰기(0x80 | (값 & 63));
        }
    }
    static void 쓰기(String 글) {
        for (int 번호 = 0; 번호 < 글.length(); 번호++) {
            int 값 = 글.charAt(번호);
            if (값 >= 0xd800 && 값 <= 0xdbff && 번호 + 1 < 글.length()) {
                int 아래 = 글.charAt(번호 + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    값 = 0x10000 + ((값 - 0xd800) << 10) + 아래 - 0xdc00; 번호++;
                }
            }
            if (값 >= 0xd800 && 값 <= 0xdfff) 값 = 0xfffd;
            문자(값);
        }
    }
    static void 수(int 값) {
        if (값 < 0) 문자('-'); else 값 = -값;
        int 자리 = 1000000000;
        boolean Koyr = false;
        while (자리 > 0) {
            int 숫자 = -(값 / 자리);
            if (숫자 != 0 || Koyr || 자리 == 1) { 문자('0' + 숫자); Koyr = true; }
            값 %= 자리; 자리 /= 10;
        }
    }
}
