// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int atuutilik) {
        if (atuutilik < 0x80) 보드.직렬쓰기(atuutilik);
        else if (atuutilik < 0x800) {
            보드.직렬쓰기(0xc0 | (atuutilik >> 6)); 보드.직렬쓰기(0x80 | (atuutilik & 63));
        } else if (atuutilik < 0x10000) {
            보드.직렬쓰기(0xe0 | (atuutilik >> 12)); 보드.직렬쓰기(0x80 | ((atuutilik >> 6) & 63)); 보드.직렬쓰기(0x80 | (atuutilik & 63));
        } else {
            보드.직렬쓰기(0xf0 | (atuutilik >> 18)); 보드.직렬쓰기(0x80 | ((atuutilik >> 12) & 63));
            보드.직렬쓰기(0x80 | ((atuutilik >> 6) & 63)); 보드.직렬쓰기(0x80 | (atuutilik & 63));
        }
    }
    static void titiraq(String titiqqaq) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < titiqqaq.length(); nalunaiqsimavik++) {
            int atuutilik = titiqqaq.charAt(nalunaiqsimavik);
            if (atuutilik >= 0xd800 && atuutilik <= 0xdbff && nalunaiqsimavik + 1 < titiqqaq.length()) {
                int 아래 = titiqqaq.charAt(nalunaiqsimavik + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    atuutilik = 0x10000 + ((atuutilik - 0xd800) << 10) + 아래 - 0xdc00; nalunaiqsimavik++;
                }
            }
            if (atuutilik >= 0xd800 && atuutilik <= 0xdfff) atuutilik = 0xfffd;
            문자(atuutilik);
        }
    }
    static void 수(int atuutilik) {
        if (atuutilik < 0) 문자('-'); else atuutilik = -atuutilik;
        int 자리 = 1000000000;
        boolean 시작 = false;
        while (자리 > 0) {
            int 숫자 = -(atuutilik / 자리);
            if (숫자 != 0 || 시작 || 자리 == 1) { 문자('0' + 숫자); 시작 = true; }
            atuutilik %= 자리; 자리 /= 10;
        }
    }
}
