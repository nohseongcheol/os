// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int värde) {
        if (värde < 0x80) Tavla.직렬쓰기(värde);
        else if (värde < 0x800) {
            Tavla.직렬쓰기(0xc0 | (värde >> 6)); Tavla.직렬쓰기(0x80 | (värde & 63));
        } else if (värde < 0x10000) {
            Tavla.직렬쓰기(0xe0 | (värde >> 12)); Tavla.직렬쓰기(0x80 | ((värde >> 6) & 63)); Tavla.직렬쓰기(0x80 | (värde & 63));
        } else {
            Tavla.직렬쓰기(0xf0 | (värde >> 18)); Tavla.직렬쓰기(0x80 | ((värde >> 12) & 63));
            Tavla.직렬쓰기(0x80 | ((värde >> 6) & 63)); Tavla.직렬쓰기(0x80 | (värde & 63));
        }
    }
    static void Skriv(String text) {
        for (int INDEX = 0; INDEX < text.length(); INDEX++) {
            int värde = text.charAt(INDEX);
            if (värde >= 0xd800 && värde <= 0xdbff && INDEX + 1 < text.length()) {
                int 아래 = text.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    värde = 0x10000 + ((värde - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (värde >= 0xd800 && värde <= 0xdfff) värde = 0xfffd;
            문자(värde);
        }
    }
    static void nummer(int värde) {
        if (värde < 0) 문자('-'); else värde = -värde;
        int positionsindex = 1000000000;
        boolean Kör = false;
        while (positionsindex > 0) {
            int siffra_värde = -(värde / positionsindex);
            if (siffra_värde != 0 || Kör || positionsindex == 1) { 문자('0' + siffra_värde); Kör = true; }
            värde %= positionsindex; positionsindex /= 10;
        }
    }
}
