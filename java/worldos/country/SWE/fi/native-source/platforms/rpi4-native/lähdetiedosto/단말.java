// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int ARVO) {
        if (ARVO < 0x80) Taulu.직렬쓰기(ARVO);
        else if (ARVO < 0x800) {
            Taulu.직렬쓰기(0xc0 | (ARVO >> 6)); Taulu.직렬쓰기(0x80 | (ARVO & 63));
        } else if (ARVO < 0x10000) {
            Taulu.직렬쓰기(0xe0 | (ARVO >> 12)); Taulu.직렬쓰기(0x80 | ((ARVO >> 6) & 63)); Taulu.직렬쓰기(0x80 | (ARVO & 63));
        } else {
            Taulu.직렬쓰기(0xf0 | (ARVO >> 18)); Taulu.직렬쓰기(0x80 | ((ARVO >> 12) & 63));
            Taulu.직렬쓰기(0x80 | ((ARVO >> 6) & 63)); Taulu.직렬쓰기(0x80 | (ARVO & 63));
        }
    }
    static void Kirjoitus(String teksti) {
        for (int INDEKSI = 0; INDEKSI < teksti.length(); INDEKSI++) {
            int ARVO = teksti.charAt(INDEKSI);
            if (ARVO >= 0xd800 && ARVO <= 0xdbff && INDEKSI + 1 < teksti.length()) {
                int 아래 = teksti.charAt(INDEKSI + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    ARVO = 0x10000 + ((ARVO - 0xd800) << 10) + 아래 - 0xdc00; INDEKSI++;
                }
            }
            if (ARVO >= 0xd800 && ARVO <= 0xdfff) ARVO = 0xfffd;
            문자(ARVO);
        }
    }
    static void numero(int ARVO) {
        if (ARVO < 0) 문자('-'); else ARVO = -ARVO;
        int sijainti = 1000000000;
        boolean Suorita_2 = false;
        while (sijainti > 0) {
            int numero_ARVO = -(ARVO / sijainti);
            if (numero_ARVO != 0 || Suorita_2 || sijainti == 1) { 문자('0' + numero_ARVO); Suorita_2 = true; }
            ARVO %= sijainti; sijainti /= 10;
        }
    }
}
