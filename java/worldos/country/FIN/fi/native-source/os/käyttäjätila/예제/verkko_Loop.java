// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Koko/홀수 kesto_ARVO 데이터그램으로 todellinen_data RTL8139 saada_ARVO Loop_ARVO 순환을 시험한다. */
public final class verkko_Loop {
    public static int Suorita_2() {
        if (käyttäjätila.인수개수() != 1) { käyttäjätila.Kirjoitus("Usage: run stress PORT\n"); return 2; }
        String teksti = käyttäjätila.argumentit(0);
        int portti_ARVO = 0;
        for (int INDEKSI = 0; INDEKSI < teksti.length(); INDEKSI++) {
            if (teksti.charAt(INDEKSI) < '0' || teksti.charAt(INDEKSI) > '9' || portti_ARVO > 6553) return 2;
            portti_ARVO = portti_ARVO * 10 + teksti.charAt(INDEKSI) - '0';
        }
        if (portti_ARVO < 1 || portti_ARVO > 65535) return 2;
        int kahva_ARVO = käyttäjätila.avata_verkko(0);
        if (kahva_ARVO < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int kesto_ARVO = 1024 - (회차 & 1);
            for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) data[INDEKSI] = (INDEKSI + 회차) & 255;
            if (käyttäjätila.lähettää_data_5b5410b2(kahva_ARVO, 0x0a000202, portti_ARVO, data, kesto_ARVO) != kesto_ARVO) return 4;
            if (käyttäjätila.saada_data(kahva_ARVO, data, 300) != kesto_ARVO) return 5;
            for (int INDEKSI = 0; INDEKSI < kesto_ARVO; INDEKSI++) if (data[INDEKSI] != ((INDEKSI + 회차) & 255)) return 6;
        }
        käyttäjätila.Sulje_verkko(kahva_ARVO);
        käyttäjätila.Kirjoitus("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
