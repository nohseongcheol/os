// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VERDI) {
        if (VERDI < 0x80) Tavle.직렬쓰기(VERDI);
        else if (VERDI < 0x800) {
            Tavle.직렬쓰기(0xc0 | (VERDI >> 6)); Tavle.직렬쓰기(0x80 | (VERDI & 63));
        } else if (VERDI < 0x10000) {
            Tavle.직렬쓰기(0xe0 | (VERDI >> 12)); Tavle.직렬쓰기(0x80 | ((VERDI >> 6) & 63)); Tavle.직렬쓰기(0x80 | (VERDI & 63));
        } else {
            Tavle.직렬쓰기(0xf0 | (VERDI >> 18)); Tavle.직렬쓰기(0x80 | ((VERDI >> 12) & 63));
            Tavle.직렬쓰기(0x80 | ((VERDI >> 6) & 63)); Tavle.직렬쓰기(0x80 | (VERDI & 63));
        }
    }
    static void Skriv(String Tekst) {
        for (int INDEKS = 0; INDEKS < Tekst.length(); INDEKS++) {
            int VERDI = Tekst.charAt(INDEKS);
            if (VERDI >= 0xd800 && VERDI <= 0xdbff && INDEKS + 1 < Tekst.length()) {
                int 아래 = Tekst.charAt(INDEKS + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VERDI = 0x10000 + ((VERDI - 0xd800) << 10) + 아래 - 0xdc00; INDEKS++;
                }
            }
            if (VERDI >= 0xd800 && VERDI <= 0xdfff) VERDI = 0xfffd;
            문자(VERDI);
        }
    }
    static void nummer(int VERDI) {
        if (VERDI < 0) 문자('-'); else VERDI = -VERDI;
        int posisjonsindeks = 1000000000;
        boolean Kjør_2 = false;
        while (posisjonsindeks > 0) {
            int siffer_VERDI = -(VERDI / posisjonsindeks);
            if (siffer_VERDI != 0 || Kjør_2 || posisjonsindeks == 1) { 문자('0' + siffer_VERDI); Kjør_2 = true; }
            VERDI %= posisjonsindeks; posisjonsindeks /= 10;
        }
    }
}
