// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VÆRDI) {
        if (VÆRDI < 0x80) Tavle.직렬쓰기(VÆRDI);
        else if (VÆRDI < 0x800) {
            Tavle.직렬쓰기(0xc0 | (VÆRDI >> 6)); Tavle.직렬쓰기(0x80 | (VÆRDI & 63));
        } else if (VÆRDI < 0x10000) {
            Tavle.직렬쓰기(0xe0 | (VÆRDI >> 12)); Tavle.직렬쓰기(0x80 | ((VÆRDI >> 6) & 63)); Tavle.직렬쓰기(0x80 | (VÆRDI & 63));
        } else {
            Tavle.직렬쓰기(0xf0 | (VÆRDI >> 18)); Tavle.직렬쓰기(0x80 | ((VÆRDI >> 12) & 63));
            Tavle.직렬쓰기(0x80 | ((VÆRDI >> 6) & 63)); Tavle.직렬쓰기(0x80 | (VÆRDI & 63));
        }
    }
    static void Skrive(String Tekst) {
        for (int INDEKS = 0; INDEKS < Tekst.length(); INDEKS++) {
            int VÆRDI = Tekst.charAt(INDEKS);
            if (VÆRDI >= 0xd800 && VÆRDI <= 0xdbff && INDEKS + 1 < Tekst.length()) {
                int 아래 = Tekst.charAt(INDEKS + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VÆRDI = 0x10000 + ((VÆRDI - 0xd800) << 10) + 아래 - 0xdc00; INDEKS++;
                }
            }
            if (VÆRDI >= 0xd800 && VÆRDI <= 0xdfff) VÆRDI = 0xfffd;
            문자(VÆRDI);
        }
    }
    static void tal(int VÆRDI) {
        if (VÆRDI < 0) 문자('-'); else VÆRDI = -VÆRDI;
        int positionsindeks = 1000000000;
        boolean Kør_2 = false;
        while (positionsindeks > 0) {
            int ciffer_VÆRDI = -(VÆRDI / positionsindeks);
            if (ciffer_VÆRDI != 0 || Kør_2 || positionsindeks == 1) { 문자('0' + ciffer_VÆRDI); Kør_2 = true; }
            VÆRDI %= positionsindeks; positionsindeks /= 10;
        }
    }
}
