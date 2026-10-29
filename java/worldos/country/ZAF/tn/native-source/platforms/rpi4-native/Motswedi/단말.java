// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int Boleng) {
        if (Boleng < 0x80) 보드.직렬쓰기(Boleng);
        else if (Boleng < 0x800) {
            보드.직렬쓰기(0xc0 | (Boleng >> 6)); 보드.직렬쓰기(0x80 | (Boleng & 63));
        } else if (Boleng < 0x10000) {
            보드.직렬쓰기(0xe0 | (Boleng >> 12)); 보드.직렬쓰기(0x80 | ((Boleng >> 6) & 63)); 보드.직렬쓰기(0x80 | (Boleng & 63));
        } else {
            보드.직렬쓰기(0xf0 | (Boleng >> 18)); 보드.직렬쓰기(0x80 | ((Boleng >> 12) & 63));
            보드.직렬쓰기(0x80 | ((Boleng >> 6) & 63)); 보드.직렬쓰기(0x80 | (Boleng & 63));
        }
    }
    static void kwala(String SMS) {
        for (int tshupane = 0; tshupane < SMS.length(); tshupane++) {
            int Boleng = SMS.charAt(tshupane);
            if (Boleng >= 0xd800 && Boleng <= 0xdbff && tshupane + 1 < SMS.length()) {
                int 아래 = SMS.charAt(tshupane + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    Boleng = 0x10000 + ((Boleng - 0xd800) << 10) + 아래 - 0xdc00; tshupane++;
                }
            }
            if (Boleng >= 0xd800 && Boleng <= 0xdfff) Boleng = 0xfffd;
            문자(Boleng);
        }
    }
    static void 수(int Boleng) {
        if (Boleng < 0) 문자('-'); else Boleng = -Boleng;
        int 자리 = 1000000000;
        boolean dirisa = false;
        while (자리 > 0) {
            int dijite_Boleng = -(Boleng / 자리);
            if (dijite_Boleng != 0 || dirisa || 자리 == 1) { 문자('0' + dijite_Boleng); dirisa = true; }
            Boleng %= 자리; 자리 /= 10;
        }
    }
}
