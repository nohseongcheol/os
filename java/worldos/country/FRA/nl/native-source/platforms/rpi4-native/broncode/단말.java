// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int WAARDE) {
        if (WAARDE < 0x80) Bord.직렬쓰기(WAARDE);
        else if (WAARDE < 0x800) {
            Bord.직렬쓰기(0xc0 | (WAARDE >> 6)); Bord.직렬쓰기(0x80 | (WAARDE & 63));
        } else if (WAARDE < 0x10000) {
            Bord.직렬쓰기(0xe0 | (WAARDE >> 12)); Bord.직렬쓰기(0x80 | ((WAARDE >> 6) & 63)); Bord.직렬쓰기(0x80 | (WAARDE & 63));
        } else {
            Bord.직렬쓰기(0xf0 | (WAARDE >> 18)); Bord.직렬쓰기(0x80 | ((WAARDE >> 12) & 63));
            Bord.직렬쓰기(0x80 | ((WAARDE >> 6) & 63)); Bord.직렬쓰기(0x80 | (WAARDE & 63));
        }
    }
    static void Schrijven(String tekst) {
        for (int INDEX = 0; INDEX < tekst.length(); INDEX++) {
            int WAARDE = tekst.charAt(INDEX);
            if (WAARDE >= 0xd800 && WAARDE <= 0xdbff && INDEX + 1 < tekst.length()) {
                int 아래 = tekst.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    WAARDE = 0x10000 + ((WAARDE - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (WAARDE >= 0xd800 && WAARDE <= 0xdfff) WAARDE = 0xfffd;
            문자(WAARDE);
        }
    }
    static void nummer(int WAARDE) {
        if (WAARDE < 0) 문자('-'); else WAARDE = -WAARDE;
        int plaatsingsindex = 1000000000;
        boolean starten = false;
        while (plaatsingsindex > 0) {
            int cijfer_WAARDE = -(WAARDE / plaatsingsindex);
            if (cijfer_WAARDE != 0 || starten || plaatsingsindex == 1) { 문자('0' + cijfer_WAARDE); starten = true; }
            WAARDE %= plaatsingsindex; plaatsingsindex /= 10;
        }
    }
}
