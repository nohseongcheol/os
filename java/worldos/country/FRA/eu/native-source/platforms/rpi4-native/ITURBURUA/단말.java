// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int balio) {
        if (balio < 0x80) arbel.직렬쓰기(balio);
        else if (balio < 0x800) {
            arbel.직렬쓰기(0xc0 | (balio >> 6)); arbel.직렬쓰기(0x80 | (balio & 63));
        } else if (balio < 0x10000) {
            arbel.직렬쓰기(0xe0 | (balio >> 12)); arbel.직렬쓰기(0x80 | ((balio >> 6) & 63)); arbel.직렬쓰기(0x80 | (balio & 63));
        } else {
            arbel.직렬쓰기(0xf0 | (balio >> 18)); arbel.직렬쓰기(0x80 | ((balio >> 12) & 63));
            arbel.직렬쓰기(0x80 | ((balio >> 6) & 63)); arbel.직렬쓰기(0x80 | (balio & 63));
        }
    }
    static void Idatzi(String Testua) {
        for (int INDIZE = 0; INDIZE < Testua.length(); INDIZE++) {
            int balio = Testua.charAt(INDIZE);
            if (balio >= 0xd800 && balio <= 0xdbff && INDIZE + 1 < Testua.length()) {
                int 아래 = Testua.charAt(INDIZE + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    balio = 0x10000 + ((balio - 0xd800) << 10) + 아래 - 0xdc00; INDIZE++;
                }
            }
            if (balio >= 0xd800 && balio <= 0xdfff) balio = 0xfffd;
            문자(balio);
        }
    }
    static void 수(int balio) {
        if (balio < 0) 문자('-'); else balio = -balio;
        int kargu_INDIZE = 1000000000;
        boolean Exekutatu_2 = false;
        while (kargu_INDIZE > 0) {
            int digitu_balio = -(balio / kargu_INDIZE);
            if (digitu_balio != 0 || Exekutatu_2 || kargu_INDIZE == 1) { 문자('0' + digitu_balio); Exekutatu_2 = true; }
            balio %= kargu_INDIZE; kargu_INDIZE /= 10;
        }
    }
}
