// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Rozmiar/홀수 długość_WARTOŚĆ 데이터그램으로 rzeczywisty_dane RTL8139 odbierać_WARTOŚĆ Loop_WARTOŚĆ 순환을 시험한다. */
public final class sieć_Loop {
    public static int Uruchom_2() {
        if (przestrzeń_użytkownika.인수개수() != 1) { przestrzeń_użytkownika.Zapis("Usage: run stress PORT\n"); return 2; }
        String tekst = przestrzeń_użytkownika.argumenty(0);
        int port_WARTOŚĆ = 0;
        for (int INDEKS = 0; INDEKS < tekst.length(); INDEKS++) {
            if (tekst.charAt(INDEKS) < '0' || tekst.charAt(INDEKS) > '9' || port_WARTOŚĆ > 6553) return 2;
            port_WARTOŚĆ = port_WARTOŚĆ * 10 + tekst.charAt(INDEKS) - '0';
        }
        if (port_WARTOŚĆ < 1 || port_WARTOŚĆ > 65535) return 2;
        int uchwyt_WARTOŚĆ = przestrzeń_użytkownika.otwarty_sieć(0);
        if (uchwyt_WARTOŚĆ < 0) return 3;
        int[] dane = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int długość_WARTOŚĆ = 1024 - (회차 & 1);
            for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) dane[INDEKS] = (INDEKS + 회차) & 255;
            if (przestrzeń_użytkownika.wysłać_dane(uchwyt_WARTOŚĆ, 0x0a000202, port_WARTOŚĆ, dane, długość_WARTOŚĆ) != długość_WARTOŚĆ) return 4;
            if (przestrzeń_użytkownika.odbierać_dane(uchwyt_WARTOŚĆ, dane, 300) != długość_WARTOŚĆ) return 5;
            for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) if (dane[INDEKS] != ((INDEKS + 회차) & 255)) return 6;
        }
        przestrzeń_użytkownika.Zamknij_sieć(uchwyt_WARTOŚĆ);
        przestrzeń_użytkownika.Zapis("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
