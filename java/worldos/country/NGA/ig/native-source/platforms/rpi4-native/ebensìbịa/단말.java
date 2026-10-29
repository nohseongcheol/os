// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int valuu) {
        if (valuu < 0x80) 보드.직렬쓰기(valuu);
        else if (valuu < 0x800) {
            보드.직렬쓰기(0xc0 | (valuu >> 6)); 보드.직렬쓰기(0x80 | (valuu & 63));
        } else if (valuu < 0x10000) {
            보드.직렬쓰기(0xe0 | (valuu >> 12)); 보드.직렬쓰기(0x80 | ((valuu >> 6) & 63)); 보드.직렬쓰기(0x80 | (valuu & 63));
        } else {
            보드.직렬쓰기(0xf0 | (valuu >> 18)); 보드.직렬쓰기(0x80 | ((valuu >> 12) & 63));
            보드.직렬쓰기(0x80 | ((valuu >> 6) & 63)); 보드.직렬쓰기(0x80 | (valuu & 63));
        }
    }
    static void Chekwaa_ozi(String SMS) {
        for (int indèks = 0; indèks < SMS.length(); indèks++) {
            int valuu = SMS.charAt(indèks);
            if (valuu >= 0xd800 && valuu <= 0xdbff && indèks + 1 < SMS.length()) {
                int 아래 = SMS.charAt(indèks + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    valuu = 0x10000 + ((valuu - 0xd800) << 10) + 아래 - 0xdc00; indèks++;
                }
            }
            if (valuu >= 0xd800 && valuu <= 0xdfff) valuu = 0xfffd;
            문자(valuu);
        }
    }
    static void 수(int valuu) {
        if (valuu < 0) 문자('-'); else valuu = -valuu;
        int 자리 = 1000000000;
        boolean Bido = false;
        while (자리 > 0) {
            int ọbula_valuu = -(valuu / 자리);
            if (ọbula_valuu != 0 || Bido || 자리 == 1) { 문자('0' + ọbula_valuu); Bido = true; }
            valuu %= 자리; 자리 /= 10;
        }
    }
}
