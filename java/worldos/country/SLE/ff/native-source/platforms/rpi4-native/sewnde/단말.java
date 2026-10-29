// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int njaru) {
        if (njaru < 0x80) 보드.직렬쓰기(njaru);
        else if (njaru < 0x800) {
            보드.직렬쓰기(0xc0 | (njaru >> 6)); 보드.직렬쓰기(0x80 | (njaru & 63));
        } else if (njaru < 0x10000) {
            보드.직렬쓰기(0xe0 | (njaru >> 12)); 보드.직렬쓰기(0x80 | ((njaru >> 6) & 63)); 보드.직렬쓰기(0x80 | (njaru & 63));
        } else {
            보드.직렬쓰기(0xf0 | (njaru >> 18)); 보드.직렬쓰기(0x80 | ((njaru >> 12) & 63));
            보드.직렬쓰기(0x80 | ((njaru >> 6) & 63)); 보드.직렬쓰기(0x80 | (njaru & 63));
        }
    }
    static void winndude(String binndi) {
        for (int joopirdu = 0; joopirdu < binndi.length(); joopirdu++) {
            int njaru = binndi.charAt(joopirdu);
            if (njaru >= 0xd800 && njaru <= 0xdbff && joopirdu + 1 < binndi.length()) {
                int 아래 = binndi.charAt(joopirdu + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    njaru = 0x10000 + ((njaru - 0xd800) << 10) + 아래 - 0xdc00; joopirdu++;
                }
            }
            if (njaru >= 0xd800 && njaru <= 0xdfff) njaru = 0xfffd;
            문자(njaru);
        }
    }
    static void 수(int njaru) {
        if (njaru < 0) 문자('-'); else njaru = -njaru;
        int 자리 = 1000000000;
        boolean huutoraade = false;
        while (자리 > 0) {
            int 숫자 = -(njaru / 자리);
            if (숫자 != 0 || huutoraade || 자리 == 1) { 문자('0' + 숫자); huutoraade = true; }
            njaru %= 자리; 자리 /= 10;
        }
    }
}
