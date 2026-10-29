// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int numero_ARVO(String teksti) {
        if (teksti == null || teksti.length() == 0) return -1;
        int TULOS = 0;
        for (int INDEKSI = 0; INDEKSI < teksti.length(); INDEKSI++) {
            int ARVO = teksti.charAt(INDEKSI) - '0';
            if (ARVO < 0 || ARVO > 9 || TULOS > 6553) return -1;
            TULOS = TULOS * 10 + ARVO;
            if (TULOS > 65535) return -1;
        }
        return TULOS;
    }
    static int OSOITE(String teksti) {
        if (teksti == null) return 0;
        int ARVO = 0, TULOS = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEKSI = 0; INDEKSI <= teksti.length(); INDEKSI++) {
            int 문자 = INDEKSI == teksti.length() ? '.' : teksti.charAt(INDEKSI);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                TULOS = (TULOS << 8) | ARVO; 부분++; ARVO = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                ARVO = ARVO * 10 + 문자 - '0';
                if (++자릿수 > 3 || ARVO > 255) return 0;
            }
        }
        return 부분 == 4 ? TULOS : 0;
    }
    public static int Suorita_2() {
        if (käyttäjätila.인수개수() != 3) { käyttäjätila.Kirjoitus("Usage: run udp IP PORT TEXT\n"); return 2; }
        int OSOITE = OSOITE(käyttäjätila.argumentit(0)), portti_ARVO = numero_ARVO(käyttäjätila.argumentit(1));
        String Sisältö_ARVO = käyttäjätila.argumentit(2);
        if (OSOITE == 0 || portti_ARVO < 1 || Sisältö_ARVO.length() > 1024) { käyttäjätila.Kirjoitus("Bad destination\n"); return 2; }
        int kahva_ARVO = käyttäjätila.avata_verkko(0);
        if (kahva_ARVO < 0) { käyttäjätila.Kirjoitus("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEKSI = 0; INDEKSI < Sisältö_ARVO.length(); INDEKSI++) data[INDEKSI] = Sisältö_ARVO.charAt(INDEKSI);
        if (käyttäjätila.lähettää_data_5b5410b2(kahva_ARVO, OSOITE, portti_ARVO, data, Sisältö_ARVO.length()) < 0) {
            käyttäjätila.Kirjoitus("UDP SEND FAILED\n"); käyttäjätila.Sulje_verkko(kahva_ARVO); return 4;
        }
        käyttäjätila.Kirjoitus("UDP SENT\n");
        int SAATU_HINTA_kesto = käyttäjätila.saada_data(kahva_ARVO, data, 1500);
        boolean 같음 = SAATU_HINTA_kesto == Sisältö_ARVO.length() && käyttäjätila.보낸주소(kahva_ARVO) == OSOITE && käyttäjätila.보낸창구(kahva_ARVO) == portti_ARVO;
        if (같음) for (int INDEKSI = 0; INDEKSI < SAATU_HINTA_kesto; INDEKSI++) if (data[INDEKSI] != Sisältö_ARVO.charAt(INDEKSI)) 같음 = false;
        käyttäjätila.Sulje_verkko(kahva_ARVO);
        if (SAATU_HINTA_kesto < 0) { käyttäjätila.Kirjoitus("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        käyttäjätila.Kirjoitus(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
