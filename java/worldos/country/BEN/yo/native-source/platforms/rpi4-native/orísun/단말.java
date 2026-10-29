// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int iye) {
        if (iye < 0x80) 보드.직렬쓰기(iye);
        else if (iye < 0x800) {
            보드.직렬쓰기(0xc0 | (iye >> 6)); 보드.직렬쓰기(0x80 | (iye & 63));
        } else if (iye < 0x10000) {
            보드.직렬쓰기(0xe0 | (iye >> 12)); 보드.직렬쓰기(0x80 | ((iye >> 6) & 63)); 보드.직렬쓰기(0x80 | (iye & 63));
        } else {
            보드.직렬쓰기(0xf0 | (iye >> 18)); 보드.직렬쓰기(0x80 | ((iye >> 12) & 63));
            보드.직렬쓰기(0x80 | ((iye >> 6) & 63)); 보드.직렬쓰기(0x80 | (iye & 63));
        }
    }
    static void Kọ(String SMS) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < SMS.length(); wá_atọ̀ka_àkóónú++) {
            int iye = SMS.charAt(wá_atọ̀ka_àkóónú);
            if (iye >= 0xd800 && iye <= 0xdbff && wá_atọ̀ka_àkóónú + 1 < SMS.length()) {
                int 아래 = SMS.charAt(wá_atọ̀ka_àkóónú + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    iye = 0x10000 + ((iye - 0xd800) << 10) + 아래 - 0xdc00; wá_atọ̀ka_àkóónú++;
                }
            }
            if (iye >= 0xd800 && iye <= 0xdfff) iye = 0xfffd;
            문자(iye);
        }
    }
    static void 수(int iye) {
        if (iye < 0) 문자('-'); else iye = -iye;
        int 자리 = 1000000000;
        boolean Rọ́ọ̀nù = false;
        while (자리 > 0) {
            int díjììtì_iye = -(iye / 자리);
            if (díjììtì_iye != 0 || Rọ́ọ̀nù || 자리 == 1) { 문자('0' + díjììtì_iye); Rọ́ọ̀nù = true; }
            iye %= 자리; 자리 /= 10;
        }
    }
}
