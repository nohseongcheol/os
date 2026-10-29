// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class dane_komunikacja {
    static int cyfra_WARTOŚĆ(String tekst) {
        if (tekst == null || tekst.length() == 0) return -1;
        int WYNIK = 0;
        for (int INDEKS = 0; INDEKS < tekst.length(); INDEKS++) {
            int WARTOŚĆ = tekst.charAt(INDEKS) - '0';
            if (WARTOŚĆ < 0 || WARTOŚĆ > 9 || WYNIK > 6553) return -1;
            WYNIK = WYNIK * 10 + WARTOŚĆ;
            if (WYNIK > 65535) return -1;
        }
        return WYNIK;
    }
    static int Adres(String tekst) {
        if (tekst == null) return 0;
        int WARTOŚĆ = 0, WYNIK = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEKS = 0; INDEKS <= tekst.length(); INDEKS++) {
            int 문자 = INDEKS == tekst.length() ? '.' : tekst.charAt(INDEKS);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                WYNIK = (WYNIK << 8) | WARTOŚĆ; 부분++; WARTOŚĆ = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                WARTOŚĆ = WARTOŚĆ * 10 + 문자 - '0';
                if (++자릿수 > 3 || WARTOŚĆ > 255) return 0;
            }
        }
        return 부분 == 4 ? WYNIK : 0;
    }
    public static int Uruchom_2() {
        if (przestrzeń_użytkownika.인수개수() != 3) { przestrzeń_użytkownika.Zapis("Usage: run udp IP PORT TEXT\n"); return 2; }
        int Adres = Adres(przestrzeń_użytkownika.argumenty(0)), port_WARTOŚĆ = cyfra_WARTOŚĆ(przestrzeń_użytkownika.argumenty(1));
        String treść_WARTOŚĆ_cb0f2404 = przestrzeń_użytkownika.argumenty(2);
        if (Adres == 0 || port_WARTOŚĆ < 1 || treść_WARTOŚĆ_cb0f2404.length() > 1024) { przestrzeń_użytkownika.Zapis("Bad destination\n"); return 2; }
        int uchwyt_WARTOŚĆ = przestrzeń_użytkownika.otwarty_sieć(0);
        if (uchwyt_WARTOŚĆ < 0) { przestrzeń_użytkownika.Zapis("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] dane = new int[1024];
        for (int INDEKS = 0; INDEKS < treść_WARTOŚĆ_cb0f2404.length(); INDEKS++) dane[INDEKS] = treść_WARTOŚĆ_cb0f2404.charAt(INDEKS);
        if (przestrzeń_użytkownika.wysłać_dane(uchwyt_WARTOŚĆ, Adres, port_WARTOŚĆ, dane, treść_WARTOŚĆ_cb0f2404.length()) < 0) {
            przestrzeń_użytkownika.Zapis("UDP SEND FAILED\n"); przestrzeń_użytkownika.Zamknij_sieć(uchwyt_WARTOŚĆ); return 4;
        }
        przestrzeń_użytkownika.Zapis("UDP SENT\n");
        int KWOTA_WYKUP_długość = przestrzeń_użytkownika.odbierać_dane(uchwyt_WARTOŚĆ, dane, 1500);
        boolean 같음 = KWOTA_WYKUP_długość == treść_WARTOŚĆ_cb0f2404.length() && przestrzeń_użytkownika.보낸주소(uchwyt_WARTOŚĆ) == Adres && przestrzeń_użytkownika.보낸창구(uchwyt_WARTOŚĆ) == port_WARTOŚĆ;
        if (같음) for (int INDEKS = 0; INDEKS < KWOTA_WYKUP_długość; INDEKS++) if (dane[INDEKS] != treść_WARTOŚĆ_cb0f2404.charAt(INDEKS)) 같음 = false;
        przestrzeń_użytkownika.Zamknij_sieć(uchwyt_WARTOŚĆ);
        if (KWOTA_WYKUP_długość < 0) { przestrzeń_użytkownika.Zapis("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        przestrzeń_użytkownika.Zapis(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
