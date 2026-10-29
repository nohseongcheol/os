// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int Daraja) {
        if (Daraja < 0x80) 보드.직렬쓰기(Daraja);
        else if (Daraja < 0x800) {
            보드.직렬쓰기(0xc0 | (Daraja >> 6)); 보드.직렬쓰기(0x80 | (Daraja & 63));
        } else if (Daraja < 0x10000) {
            보드.직렬쓰기(0xe0 | (Daraja >> 12)); 보드.직렬쓰기(0x80 | ((Daraja >> 6) & 63)); 보드.직렬쓰기(0x80 | (Daraja & 63));
        } else {
            보드.직렬쓰기(0xf0 | (Daraja >> 18)); 보드.직렬쓰기(0x80 | ((Daraja >> 12) & 63));
            보드.직렬쓰기(0x80 | ((Daraja >> 6) & 63)); 보드.직렬쓰기(0x80 | (Daraja & 63));
        }
    }
    static void Yi_Rubutu(String SMS) {
        for (int Indes = 0; Indes < SMS.length(); Indes++) {
            int Daraja = SMS.charAt(Indes);
            if (Daraja >= 0xd800 && Daraja <= 0xdbff && Indes + 1 < SMS.length()) {
                int 아래 = SMS.charAt(Indes + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    Daraja = 0x10000 + ((Daraja - 0xd800) << 10) + 아래 - 0xdc00; Indes++;
                }
            }
            if (Daraja >= 0xd800 && Daraja <= 0xdfff) Daraja = 0xfffd;
            문자(Daraja);
        }
    }
    static void 수(int Daraja) {
        if (Daraja < 0) 문자('-'); else Daraja = -Daraja;
        int 자리 = 1000000000;
        boolean Tafiyar_da = false;
        while (자리 > 0) {
            int lamba_Daraja = -(Daraja / 자리);
            if (lamba_Daraja != 0 || Tafiyar_da || 자리 == 1) { 문자('0' + lamba_Daraja); Tafiyar_da = true; }
            Daraja %= 자리; 자리 /= 10;
        }
    }
}
