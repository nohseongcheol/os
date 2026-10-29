// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statyczny_WARTOŚĆ IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class sieć_Stos {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int maska_sieci = 0xffffff00; /* ip.conf:NETMASK */
    static final int brama_WARTOŚĆ = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] wejście_kadr = new int[1536], produkt_wyjściowy_kadr = new int[1536];
    static int[] 접속번호들 = new int[4], KWOTA_WYKUP_długość = new int[4], KWOTA_WYKUP_ADRES = new int[4], KWOTA_WYKUP_numer_portu = new int[4];
    static int[] KWOTA_WYKUP_dane = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identyfikator_WARTOŚĆ = 0, 폐기수 = 0;

    static int liczba_całkowita_PEGI_16(int[] kadr_INDEKS, int pozycja) { return (kadr_INDEKS[pozycja] << 8) | kadr_INDEKS[pozycja + 1]; }
    static int liczba_całkowita_32(int[] kadr_INDEKS, int pozycja) { return (liczba_całkowita_PEGI_16(kadr_INDEKS, pozycja) << 16) | liczba_całkowita_PEGI_16(kadr_INDEKS, pozycja + 2); }
    static void 넣기16(int[] kadr_INDEKS, int pozycja, int WARTOŚĆ) { kadr_INDEKS[pozycja] = (WARTOŚĆ >>> 8) & 255; kadr_INDEKS[pozycja + 1] = WARTOŚĆ & 255; }
    static void 넣기32(int[] kadr_INDEKS, int pozycja, int WARTOŚĆ) { 넣기16(kadr_INDEKS, pozycja, WARTOŚĆ >>> 16); 넣기16(kadr_INDEKS, pozycja + 2, WARTOŚĆ); }
    static int SUMA_WARTOŚĆ(int[] kadr_INDEKS, int Uruchom_2, int długość_WARTOŚĆ, int WARTOŚĆ) {
        for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS += 2)
            WARTOŚĆ += (kadr_INDEKS[Uruchom_2 + INDEKS] << 8) | (INDEKS + 1 < długość_WARTOŚĆ ? kadr_INDEKS[Uruchom_2 + INDEKS + 1] : 0);
        while ((WARTOŚĆ >>> 16) != 0) WARTOŚĆ = (WARTOŚĆ & 65535) + (WARTOŚĆ >>> 16);
        return WARTOŚĆ;
    }
    static int 가상머리합(int 출발, int 도착, int długość_WARTOŚĆ) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + długość_WARTOŚĆ;
    }

    static void OCZYŚĆ_Proces() {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) {
            접속번호들[INDEKS] = 0; KWOTA_WYKUP_długość[INDEKS] = -1; KWOTA_WYKUP_ADRES[INDEKS] = 0; KWOTA_WYKUP_numer_portu[INDEKS] = 0;
        }
        for (int INDEKS = 0; INDEKS < 64; INDEKS++) if (sieć_sterownik.odbierać(wejście_kadr) == 0) break;
    }
    static int INDEKS(int uchwyt_WARTOŚĆ) { return uchwyt_WARTOŚĆ >= 3 && uchwyt_WARTOŚĆ < 7 && 접속번호들[uchwyt_WARTOŚĆ - 3] != 0 ? uchwyt_WARTOŚĆ - 3 : -1; }
    static int Otwórz(int numer_portu) {
        if (sieć_sterownik.입출력기준주소 == 0) return -19;
        if (numer_portu < 0 || numer_portu > 65535) return -22;
        if (numer_portu != 0) for (int INDEKS = 0; INDEKS < 4; INDEKS++) if (접속번호들[INDEKS] == numer_portu) return -98;
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) if (접속번호들[INDEKS] == 0) {
            if (numer_portu == 0) {
                numer_portu = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int przód_WARTOŚĆ = 0; przód_WARTOŚĆ < 4; przód_WARTOŚĆ++) if (접속번호들[przód_WARTOŚĆ] == numer_portu) 겹침 = true;
                    if (겹침) numer_portu++;
                }
            }
            접속번호들[INDEKS] = numer_portu; KWOTA_WYKUP_długość[INDEKS] = -1;
            return INDEKS + 3;
        }
        return -24;
    }
    static int Zamknięte(int uchwyt_WARTOŚĆ) {
        int gniazdo_wpis = INDEKS(uchwyt_WARTOŚĆ);
        if (gniazdo_wpis < 0) return -9;
        접속번호들[gniazdo_wpis] = 0; KWOTA_WYKUP_długość[gniazdo_wpis] = -1;
        return 0;
    }
    static int węzeł_równorzędny_ADRES(int uchwyt_WARTOŚĆ) { int gniazdo_wpis = INDEKS(uchwyt_WARTOŚĆ); return gniazdo_wpis < 0 ? -9 : KWOTA_WYKUP_ADRES[gniazdo_wpis]; }
    static int węzeł_równorzędny_numer_portu(int uchwyt_WARTOŚĆ) { int gniazdo_wpis = INDEKS(uchwyt_WARTOŚĆ); return gniazdo_wpis < 0 ? -9 : KWOTA_WYKUP_numer_portu[gniazdo_wpis]; }

    static void 바깥머리(int Rodzaj_WARTOŚĆ, boolean emisja_WARTOŚĆ) {
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            produkt_wyjściowy_kadr[INDEKS] = emisja_WARTOŚĆ ? 255 : 찾은장치[INDEKS];
            produkt_wyjściowy_kadr[6 + INDEKS] = sieć_sterownik.urządzenie_ADRES[INDEKS];
        }
        넣기16(produkt_wyjściowy_kadr, 12, Rodzaj_WARTOŚĆ);
    }
    static void żądanie_ADRES(int cel_WARTOŚĆ) {
        바깥머리(0x0806, true);
        넣기16(produkt_wyjściowy_kadr, 14, 1); 넣기16(produkt_wyjściowy_kadr, 16, 0x0800);
        produkt_wyjściowy_kadr[18] = 6; produkt_wyjściowy_kadr[19] = 4; 넣기16(produkt_wyjściowy_kadr, 20, 1);
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            produkt_wyjściowy_kadr[22 + INDEKS] = sieć_sterownik.urządzenie_ADRES[INDEKS]; produkt_wyjściowy_kadr[32 + INDEKS] = 0;
        }
        넣기32(produkt_wyjściowy_kadr, 28, 내주소); 넣기32(produkt_wyjściowy_kadr, 38, cel_WARTOŚĆ);
        sieć_sterownik.wysłać(produkt_wyjściowy_kadr, 42);
    }
    static void Proces_ADRES(int długość_WARTOŚĆ) {
        if (długość_WARTOŚĆ < 42 || liczba_całkowita_PEGI_16(wejście_kadr, 14) != 1 || liczba_całkowita_PEGI_16(wejście_kadr, 16) != 0x0800
            || wejście_kadr[18] != 6 || wejście_kadr[19] != 4 || liczba_całkowita_32(wejście_kadr, 38) != 내주소) { 폐기수++; return; }
        int Rodzaj_WARTOŚĆ = liczba_całkowita_PEGI_16(wejście_kadr, 20), węzeł_równorzędny_WARTOŚĆ = liczba_całkowita_32(wejście_kadr, 28);
        if (Rodzaj_WARTOŚĆ == 2 && węzeł_równorzędny_WARTOŚĆ == 찾을주소) {
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
                if (wejście_kadr[6 + INDEKS] != wejście_kadr[22 + INDEKS] || wejście_kadr[32 + INDEKS] != sieć_sterownik.urządzenie_ADRES[INDEKS]) return;
            }
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) 찾은장치[INDEKS] = wejście_kadr[22 + INDEKS];
            찾은주소 = węzeł_równorzędny_WARTOŚĆ;
        } else if (Rodzaj_WARTOŚĆ == 1) {
            바깥머리(0x0806, false);
            넣기16(produkt_wyjściowy_kadr, 14, 1); 넣기16(produkt_wyjściowy_kadr, 16, 0x0800);
            produkt_wyjściowy_kadr[18] = 6; produkt_wyjściowy_kadr[19] = 4; 넣기16(produkt_wyjściowy_kadr, 20, 2);
            for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
                produkt_wyjściowy_kadr[INDEKS] = wejście_kadr[22 + INDEKS]; produkt_wyjściowy_kadr[32 + INDEKS] = wejście_kadr[22 + INDEKS];
                produkt_wyjściowy_kadr[22 + INDEKS] = sieć_sterownik.urządzenie_ADRES[INDEKS];
            }
            넣기32(produkt_wyjściowy_kadr, 28, 내주소); 넣기32(produkt_wyjściowy_kadr, 38, węzeł_równorzędny_WARTOŚĆ);
            sieć_sterownik.wysłać(produkt_wyjściowy_kadr, 42);
        }
    }

    static void Proces_kadr(int długość_WARTOŚĆ) {
        if (długość_WARTOŚĆ < 14 || długość_WARTOŚĆ > wejście_kadr.length) { 폐기수++; return; }
        boolean 자기 = true, emisja_WARTOŚĆ = true;
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) {
            if (wejście_kadr[INDEKS] != sieć_sterownik.urządzenie_ADRES[INDEKS]) 자기 = false;
            if (wejście_kadr[INDEKS] != 255) emisja_WARTOŚĆ = false;
        }
        if (!자기 && !emisja_WARTOŚĆ) return;
        if (liczba_całkowita_PEGI_16(wejście_kadr, 12) == 0x0806) { Proces_ADRES(długość_WARTOŚĆ); return; }
        if (liczba_całkowita_PEGI_16(wejście_kadr, 12) != 0x0800) return;
        if (długość_WARTOŚĆ < 34 || (wejście_kadr[14] >>> 4) != 4) { 폐기수++; return; }
        int Nagłówek_długość = (wejście_kadr[14] & 15) * 4, suma_długość = liczba_całkowita_PEGI_16(wejście_kadr, 16);
        if (Nagłówek_długość < 20 || Nagłówek_długość > 60 || suma_długość < Nagłówek_długość + 8 || suma_długość > długość_WARTOŚĆ - 14
            || (liczba_całkowita_PEGI_16(wejście_kadr, 20) & 0x3fff) != 0 || wejście_kadr[23] != 17
            || liczba_całkowita_32(wejście_kadr, 30) != 내주소 || SUMA_WARTOŚĆ(wejście_kadr, 14, Nagłówek_długość, 0) != 65535) { 폐기수++; return; }
        int Uruchom_2 = 14 + Nagłówek_długość, dane_długość = liczba_całkowita_PEGI_16(wejście_kadr, Uruchom_2 + 4);
        if (dane_długość < 8 || dane_długość != suma_długość - Nagłówek_długość || dane_długość > 1032) { 폐기수++; return; }
        int 출발 = liczba_całkowita_32(wejście_kadr, 26);
        if (liczba_całkowita_PEGI_16(wejście_kadr, Uruchom_2 + 6) != 0 && SUMA_WARTOŚĆ(wejście_kadr, Uruchom_2, dane_długość, 가상머리합(출발, 내주소, dane_długość)) != 65535) {
            폐기수++; return;
        }
        int cel_WARTOŚĆ = liczba_całkowita_PEGI_16(wejście_kadr, Uruchom_2 + 2);
        for (int gniazdo_wpis = 0; gniazdo_wpis < 4; gniazdo_wpis++) if (접속번호들[gniazdo_wpis] != 0 && 접속번호들[gniazdo_wpis] == cel_WARTOŚĆ) {
            if (KWOTA_WYKUP_długość[gniazdo_wpis] >= 0) { 폐기수++; return; }
            KWOTA_WYKUP_długość[gniazdo_wpis] = dane_długość - 8; KWOTA_WYKUP_ADRES[gniazdo_wpis] = 출발; KWOTA_WYKUP_numer_portu[gniazdo_wpis] = liczba_całkowita_PEGI_16(wejście_kadr, Uruchom_2);
            for (int INDEKS = 0; INDEKS < dane_długość - 8; INDEKS++) KWOTA_WYKUP_dane[gniazdo_wpis * 1024 + INDEKS] = wejście_kadr[Uruchom_2 + 8 + INDEKS];
            return;
        }
    }

    static void 확인() {
        for (int INDEKS = 0; INDEKS < 16; INDEKS++) {
            int długość_WARTOŚĆ = sieć_sterownik.odbierać(wejście_kadr);
            if (długość_WARTOŚĆ == 0) return;
            Proces_kadr(długość_WARTOŚĆ);
        }
    }
    static int ZNAJDŹ_ADRES(int Adres) {
        if (Adres == 0 || Adres == -1 || (Adres >>> 28) >= 14 || (Adres >>> 24) == 127 || Adres == 내주소) return -101;
        int Dalej_towar = (Adres & maska_sieci) == (내주소 & maska_sieci) ? Adres : brama_WARTOŚĆ;
        if (Dalej_towar == 찾은주소) return 0;
        찾을주소 = Dalej_towar;
        int Uruchom_2 = urządzenie_WARTOŚĆ.밀리초(), Dalej_żądanie = Uruchom_2;
        while (urządzenie_WARTOŚĆ.밀리초() - Uruchom_2 < 1000) {
            if (urządzenie_WARTOŚĆ.밀리초() - Dalej_żądanie >= 0) { żądanie_ADRES(Dalej_towar); Dalej_żądanie += 300; }
            확인();
            if (찾은주소 == Dalej_towar) return 0;
            urządzenie_WARTOŚĆ.잠시양보();
        }
        return -110;
    }
    static int wysłać(int uchwyt_WARTOŚĆ, int Adres, int numer_portu, int[] dane, int długość_WARTOŚĆ) {
        int gniazdo_wpis = INDEKS(uchwyt_WARTOŚĆ);
        if (gniazdo_wpis < 0) return -9;
        if (sieć_sterownik.입출력기준주소 == 0) return -19;
        if (numer_portu < 1 || numer_portu > 65535 || długość_WARTOŚĆ < 0 || długość_WARTOŚĆ > 1024) return -22;
        int WYNIK = ZNAJDŹ_ADRES(Adres);
        if (WYNIK < 0) return WYNIK;
        바깥머리(0x0800, false);
        produkt_wyjściowy_kadr[14] = 0x45; produkt_wyjściowy_kadr[15] = 0; 넣기16(produkt_wyjściowy_kadr, 16, 28 + długość_WARTOŚĆ);
        넣기16(produkt_wyjściowy_kadr, 18, identyfikator_WARTOŚĆ++); 넣기16(produkt_wyjściowy_kadr, 20, 0x4000);
        produkt_wyjściowy_kadr[22] = 64; produkt_wyjściowy_kadr[23] = 17; 넣기16(produkt_wyjściowy_kadr, 24, 0);
        넣기32(produkt_wyjściowy_kadr, 26, 내주소); 넣기32(produkt_wyjściowy_kadr, 30, Adres);
        넣기16(produkt_wyjściowy_kadr, 24, ~SUMA_WARTOŚĆ(produkt_wyjściowy_kadr, 14, 20, 0));
        넣기16(produkt_wyjściowy_kadr, 34, 접속번호들[gniazdo_wpis]); 넣기16(produkt_wyjściowy_kadr, 36, numer_portu);
        넣기16(produkt_wyjściowy_kadr, 38, długość_WARTOŚĆ + 8); 넣기16(produkt_wyjściowy_kadr, 40, 0);
        for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) produkt_wyjściowy_kadr[42 + INDEKS] = dane[INDEKS] & 255;
        int suma_kontrolna = (~SUMA_WARTOŚĆ(produkt_wyjściowy_kadr, 34, długość_WARTOŚĆ + 8, 가상머리합(내주소, Adres, długość_WARTOŚĆ + 8))) & 65535;
        넣기16(produkt_wyjściowy_kadr, 40, suma_kontrolna == 0 ? 65535 : suma_kontrolna);
        WYNIK = sieć_sterownik.wysłać(produkt_wyjściowy_kadr, długość_WARTOŚĆ + 42);
        return WYNIK < 0 ? WYNIK : długość_WARTOŚĆ;
    }
    static int odbierać(int uchwyt_WARTOŚĆ, int[] dane, int pojemność_WARTOŚĆ, int 제한) {
        int gniazdo_wpis = INDEKS(uchwyt_WARTOŚĆ);
        if (gniazdo_wpis < 0) return -9;
        int Uruchom_2 = urządzenie_WARTOŚĆ.밀리초();
        while (true) {
            확인();
            int długość_WARTOŚĆ = KWOTA_WYKUP_długość[gniazdo_wpis];
            if (długość_WARTOŚĆ >= 0) {
                KWOTA_WYKUP_długość[gniazdo_wpis] = -1;
                if (długość_WARTOŚĆ > pojemność_WARTOŚĆ) return -90;
                for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) dane[INDEKS] = KWOTA_WYKUP_dane[gniazdo_wpis * 1024 + INDEKS];
                return długość_WARTOŚĆ;
            }
            if (제한 == 0) return -11;
            if (urządzenie_WARTOŚĆ.밀리초() - Uruchom_2 >= 제한) return -110;
            urządzenie_WARTOŚĆ.잠시양보();
        }
    }
    static void Stan_WARTOŚĆ() {
        SMS_Terminal.Zapis(sieć_sterownik.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Zapis("TX: "); SMS_Terminal.zapis_identyfikator(sieć_sterownik.송신수);
        SMS_Terminal.Zapis(" RX: "); SMS_Terminal.zapis_identyfikator(sieć_sterownik.odbierać_ILE_LICZB);
        SMS_Terminal.Zapis(" DROP: "); SMS_Terminal.zapis_identyfikator(폐기수);
        SMS_Terminal.Zapis("\n");
    }
}
