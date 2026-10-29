// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int WARTOŚĆ) {
        if (WARTOŚĆ < 0x80) Tablica.직렬쓰기(WARTOŚĆ);
        else if (WARTOŚĆ < 0x800) {
            Tablica.직렬쓰기(0xc0 | (WARTOŚĆ >> 6)); Tablica.직렬쓰기(0x80 | (WARTOŚĆ & 63));
        } else if (WARTOŚĆ < 0x10000) {
            Tablica.직렬쓰기(0xe0 | (WARTOŚĆ >> 12)); Tablica.직렬쓰기(0x80 | ((WARTOŚĆ >> 6) & 63)); Tablica.직렬쓰기(0x80 | (WARTOŚĆ & 63));
        } else {
            Tablica.직렬쓰기(0xf0 | (WARTOŚĆ >> 18)); Tablica.직렬쓰기(0x80 | ((WARTOŚĆ >> 12) & 63));
            Tablica.직렬쓰기(0x80 | ((WARTOŚĆ >> 6) & 63)); Tablica.직렬쓰기(0x80 | (WARTOŚĆ & 63));
        }
    }
    static void Zapis(String tekst) {
        for (int INDEKS = 0; INDEKS < tekst.length(); INDEKS++) {
            int WARTOŚĆ = tekst.charAt(INDEKS);
            if (WARTOŚĆ >= 0xd800 && WARTOŚĆ <= 0xdbff && INDEKS + 1 < tekst.length()) {
                int 아래 = tekst.charAt(INDEKS + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    WARTOŚĆ = 0x10000 + ((WARTOŚĆ - 0xd800) << 10) + 아래 - 0xdc00; INDEKS++;
                }
            }
            if (WARTOŚĆ >= 0xd800 && WARTOŚĆ <= 0xdfff) WARTOŚĆ = 0xfffd;
            문자(WARTOŚĆ);
        }
    }
    static void identyfikator(int WARTOŚĆ) {
        if (WARTOŚĆ < 0) 문자('-'); else WARTOŚĆ = -WARTOŚĆ;
        int indeks_pozycji = 1000000000;
        boolean Uruchom_2 = false;
        while (indeks_pozycji > 0) {
            int cyfra_WARTOŚĆ = -(WARTOŚĆ / indeks_pozycji);
            if (cyfra_WARTOŚĆ != 0 || Uruchom_2 || indeks_pozycji == 1) { 문자('0' + cyfra_WARTOŚĆ); Uruchom_2 = true; }
            WARTOŚĆ %= indeks_pozycji; indeks_pozycji /= 10;
        }
    }
}
