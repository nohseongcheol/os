// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 przestrzeń_użytkownika 과정의 파일서술자와 열린 nazwa_pliku 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class Plik_deskryptor_Menedżer {
    static final int 서술자한도 = 32;
    static final int R_W_flaga = 2, Twórca_wpis = 64, 독점생성 = 128, czyścić_Spis_treści = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] otwarty_uchwyt = new int[서술자한도], set_deskryptor = new int[서술자한도];
    static int[] Rodzaj_WARTOŚĆ = new int[서술자한도], wartość_docelowa = new int[서술자한도];
    static int[] Plik_stanowisko = new int[서술자한도], otwarty_Ustawienia = new int[서술자한도], odwołanie_ILE_LICZB = new int[서술자한도];
    static int[] sieć_uchwyt = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] ścieżka_nazwa = new int[64], transfer_dane = new int[1024];

    static int ZNAJDŹ_deskryptor(int Plik_deskryptor) {
        if (Plik_deskryptor < 0 || Plik_deskryptor >= 서술자한도) return -9;
        return otwarty_uchwyt[Plik_deskryptor] - 1;
    }
    static int 빈서술자(int Uruchom_2) {
        for (int INDEKS = Uruchom_2; INDEKS < 서술자한도; INDEKS++) if (otwarty_uchwyt[INDEKS] == 0) return INDEKS;
        return -24;
    }
    static int 빈기술() {
        for (int INDEKS = 0; INDEKS < 서술자한도; INDEKS++) if (odwołanie_ILE_LICZB[INDEKS] == 0) return INDEKS;
        return -24;
    }
    static int Połącz(int deskryptor_wpis, int deskryptor_WARTOŚĆ, int Plik_Rodzaj, int Plik_wartość_docelowa, int Ustawienia) {
        otwarty_uchwyt[deskryptor_wpis] = deskryptor_WARTOŚĆ + 1; set_deskryptor[deskryptor_wpis] = (Ustawienia & 실행시닫기) != 0 ? 1 : 0;
        Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] = Plik_Rodzaj; wartość_docelowa[deskryptor_WARTOŚĆ] = Plik_wartość_docelowa; odwołanie_ILE_LICZB[deskryptor_WARTOŚĆ] = 1;
        otwarty_Ustawienia[deskryptor_WARTOŚĆ] = Ustawienia & (3 | 이어쓰기 | 기다리지않기); Plik_stanowisko[deskryptor_WARTOŚĆ] = 0;
        sieć_uchwyt[deskryptor_WARTOŚĆ] = 0; 수신대기밀리초[deskryptor_WARTOŚĆ] = 0;
        return deskryptor_wpis;
    }
    static void START_Proces() {
        OCZYŚĆ_Proces();
        for (int INDEKS = 0; INDEKS < 3; INDEKS++) Połącz(INDEKS, INDEKS, 1, INDEKS, INDEKS == 0 ? 0 : 1);
    }
    static void OCZYŚĆ_Proces() {
        for (int INDEKS = 0; INDEKS < 서술자한도; INDEKS++) if (otwarty_uchwyt[INDEKS] != 0) Zamknij_Plik(INDEKS);
    }
    static int Zamknij_Plik(int deskryptor_wpis) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return -9;
        otwarty_uchwyt[deskryptor_wpis] = 0; set_deskryptor[deskryptor_wpis] = 0;
        odwołanie_ILE_LICZB[deskryptor_WARTOŚĆ]--;
        if (odwołanie_ILE_LICZB[deskryptor_WARTOŚĆ] == 0) {
            if (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 2) Pamięć_system_plików.otwarty_ILE_LICZB[wartość_docelowa[deskryptor_WARTOŚĆ]]--;
            if (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 3 && sieć_uchwyt[deskryptor_WARTOŚĆ] != 0) sieć_Stos.Zamknięte(sieć_uchwyt[deskryptor_WARTOŚĆ]);
            Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 bajt_WARTOŚĆ 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int Adres) {
        if (!wykonanie_Menedżer.obcinać(Adres, 1)) return -14;
        int pozycja = urządzenie_WARTOŚĆ.기억읽기(Adres) == '/' ? 1 : 0;
        for (int długość_WARTOŚĆ = 0; długość_WARTOŚĆ < 64; długość_WARTOŚĆ++) {
            if (!wykonanie_Menedżer.obcinać(Adres + pozycja + długość_WARTOŚĆ, 1)) return -14;
            int WARTOŚĆ = urządzenie_WARTOŚĆ.기억읽기(Adres + pozycja + długość_WARTOŚĆ);
            ścieżka_nazwa[długość_WARTOŚĆ] = WARTOŚĆ;
            if (WARTOŚĆ == 0) return długość_WARTOŚĆ == 0 ? -2 : (Pamięć_system_plików.czek_nazwa(ścieżka_nazwa, długość_WARTOŚĆ) ? długość_WARTOŚĆ : -22);
            if (WARTOŚĆ == '/') return -20;
        }
        return -36;
    }
    static int otwarty_Plik(int nazwa_ADRES, int Ustawienia, int udzielenie_pozwolenie) {
        int długość_WARTOŚĆ = 경로읽기(nazwa_ADRES);
        if (długość_WARTOŚĆ < 0) return długość_WARTOŚĆ;
        if ((Ustawienia & ~(3 | Twórca_wpis | 독점생성 | czyścić_Spis_treści | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Ustawienia & 3) == 3 || ((Ustawienia & czyścić_Spis_treści) != 0 && (Ustawienia & 3) == 0)) return -22;
        int nazwa_pliku = Pamięć_system_plików.ZNAJDŹ_wpis(ścieżka_nazwa, długość_WARTOŚĆ);
        if (nazwa_pliku >= 0 && (Ustawienia & (Twórca_wpis | 독점생성)) == (Twórca_wpis | 독점생성)) return -17;
        if (nazwa_pliku == -2 && (Ustawienia & Twórca_wpis) == 0) return -2;
        int deskryptor_wpis = 빈서술자(0), deskryptor_WARTOŚĆ = 빈기술();
        if (deskryptor_wpis < 0 || deskryptor_WARTOŚĆ < 0) return -24;
        if (nazwa_pliku == -2) {
            int WYNIK = Pamięć_system_plików.Store_WARTOŚĆ(ścieżka_nazwa, długość_WARTOŚĆ, ścieżka_nazwa, 0);
            if (WYNIK < 0) return WYNIK;
            nazwa_pliku = Pamięć_system_plików.ZNAJDŹ_wpis(ścieżka_nazwa, długość_WARTOŚĆ);
            Pamięć_system_plików.허가들[nazwa_pliku] = udzielenie_pozwolenie & 511;
        }
        if (nazwa_pliku < 0) return nazwa_pliku;
        if ((Ustawienia & czyścić_Spis_treści) != 0) Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku] = 0;
        Pamięć_system_plików.otwarty_ILE_LICZB[nazwa_pliku]++;
        return Połącz(deskryptor_wpis, deskryptor_WARTOŚĆ, 2, nazwa_pliku, Ustawienia);
    }
    static int 파일읽기(int deskryptor_wpis, int dane_ADRES, int długość_WARTOŚĆ) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0 || (otwarty_Ustawienia[deskryptor_WARTOŚĆ] & 3) == 1) return -9;
        if (długość_WARTOŚĆ < 0) return -22;
        if (długość_WARTOŚĆ == 0) return 0;
        if (!wykonanie_Menedżer.obcinać(dane_ADRES, długość_WARTOŚĆ)) return -14;
        if (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 3) return odbierać_datagram_dane(deskryptor_wpis, dane_ADRES, długość_WARTOŚĆ, 0, 0);
        if (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 1) {
            int KWOTA_WYKUP_ILE_LICZB = 0;
            while (KWOTA_WYKUP_ILE_LICZB < długość_WARTOŚĆ) {
                int WARTOŚĆ = SMS_Terminal.직렬읽기();
                if (WARTOŚĆ < 0) WARTOŚĆ = klawiatura.Odczyt();
                if (WARTOŚĆ < 0) {
                    if (KWOTA_WYKUP_ILE_LICZB > 0) return KWOTA_WYKUP_ILE_LICZB;
                    if ((otwarty_Ustawienia[deskryptor_WARTOŚĆ] & 기다리지않기) != 0) return -11;
                    if (urządzenie_WARTOŚĆ.사용자남은밀리초() <= 10) return -11;
                    sieć_Stos.확인(); urządzenie_WARTOŚĆ.잠시양보();
                } else {
                    urządzenie_WARTOŚĆ.zapis_Pamięć(dane_ADRES + KWOTA_WYKUP_ILE_LICZB, WARTOŚĆ); KWOTA_WYKUP_ILE_LICZB++;
                }
            }
            return KWOTA_WYKUP_ILE_LICZB;
        }
        int nazwa_pliku = wartość_docelowa[deskryptor_WARTOŚĆ], pozycja = Plik_stanowisko[deskryptor_WARTOŚĆ];
        if (pozycja >= Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku]) return 0;
        if (długość_WARTOŚĆ > Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku] - pozycja) długość_WARTOŚĆ = Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku] - pozycja;
        int 원본주소 = urządzenie_WARTOŚĆ.Plik_Pamięć() + nazwa_pliku * Pamięć_system_plików.최대크기 + pozycja;
        for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) urządzenie_WARTOŚĆ.zapis_Pamięć(dane_ADRES + INDEKS, urządzenie_WARTOŚĆ.기억읽기(원본주소 + INDEKS));
        Plik_stanowisko[deskryptor_WARTOŚĆ] += długość_WARTOŚĆ;
        return długość_WARTOŚĆ;
    }
    static int zapis_Plik(int deskryptor_wpis, int dane_ADRES, int długość_WARTOŚĆ) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0 || (otwarty_Ustawienia[deskryptor_WARTOŚĆ] & 3) == 0) return -9;
        if (długość_WARTOŚĆ < 0) return -22;
        if (długość_WARTOŚĆ == 0) return 0;
        if (!wykonanie_Menedżer.obcinać(dane_ADRES, długość_WARTOŚĆ)) return -14;
        if (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 cel_WARTOŚĆ 주소가 필요하다.
        if (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 1) {
            if (długość_WARTOŚĆ > 16384) długość_WARTOŚĆ = 16384;
            for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) {
                int WARTOŚĆ = urządzenie_WARTOŚĆ.기억읽기(dane_ADRES + INDEKS);
                SMS_Terminal.직렬바이트(WARTOŚĆ); SMS_Terminal.화면문자(WARTOŚĆ);
            }
            return długość_WARTOŚĆ;
        }
        int nazwa_pliku = wartość_docelowa[deskryptor_WARTOŚĆ], Rozmiar = Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku];
        int pozycja = (otwarty_Ustawienia[deskryptor_WARTOŚĆ] & 이어쓰기) != 0 ? Rozmiar : Plik_stanowisko[deskryptor_WARTOŚĆ];
        if (pozycja >= Pamięć_system_plików.최대크기) return -27;
        if (długość_WARTOŚĆ > Pamięć_system_plików.최대크기 - pozycja) długość_WARTOŚĆ = Pamięć_system_plików.최대크기 - pozycja;
        int cel_ADRES_08bbd577 = urządzenie_WARTOŚĆ.Plik_Pamięć() + nazwa_pliku * Pamięć_system_plików.최대크기;
        for (int INDEKS = Rozmiar; INDEKS < pozycja; INDEKS++) urządzenie_WARTOŚĆ.zapis_Pamięć(cel_ADRES_08bbd577 + INDEKS, 0);
        for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) urządzenie_WARTOŚĆ.zapis_Pamięć(cel_ADRES_08bbd577 + pozycja + INDEKS, urządzenie_WARTOŚĆ.기억읽기(dane_ADRES + INDEKS));
        Plik_stanowisko[deskryptor_WARTOŚĆ] = pozycja + długość_WARTOŚĆ;
        if (pozycja + długość_WARTOŚĆ > Rozmiar) Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku] = pozycja + długość_WARTOŚĆ;
        return długość_WARTOŚĆ;
    }
    static int szukać_Plik(int deskryptor_wpis, int przesunąć_WARTOŚĆ_450fc799, int Project_korzeń) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return -9;
        if (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] != 2) return -29;
        if (Project_korzeń < 0 || Project_korzeń > 2) return -22;
        int Tło_WARTOŚĆ = Project_korzeń == 0 ? 0 : (Project_korzeń == 1 ? Plik_stanowisko[deskryptor_WARTOŚĆ] : Pamięć_system_plików.zmienić_rozmiar_Lista[wartość_docelowa[deskryptor_WARTOŚĆ]]);
        if (przesunąć_WARTOŚĆ_450fc799 > 0 && Tło_WARTOŚĆ > 2147483647 - przesunąć_WARTOŚĆ_450fc799) return -75;
        if (przesunąć_WARTOŚĆ_450fc799 < 0 && przesunąć_WARTOŚĆ_450fc799 < -Tło_WARTOŚĆ) return -22;
        Plik_stanowisko[deskryptor_WARTOŚĆ] = Tło_WARTOŚĆ + przesunąć_WARTOŚĆ_450fc799;
        return Plik_stanowisko[deskryptor_WARTOŚĆ];
    }
    static int Duplikuj_deskryptor(int deskryptor_wpis, int 새서술자, boolean Przypisz_WARTOŚĆ, int Ustawienia) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Przypisz_WARTOŚĆ ? -9 : -22;
        if (Przypisz_WARTOŚĆ && deskryptor_wpis == 새서술자) return 새서술자;
        if (Przypisz_WARTOŚĆ) { if (otwarty_uchwyt[새서술자] != 0) Zamknij_Plik(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        otwarty_uchwyt[새서술자] = deskryptor_WARTOŚĆ + 1; set_deskryptor[새서술자] = Ustawienia; odwołanie_ILE_LICZB[deskryptor_WARTOŚĆ]++;
        return 새서술자;
    }
    static int usuń_Plik_wpis_nazwa(int nazwa_ADRES) {
        int długość_WARTOŚĆ = 경로읽기(nazwa_ADRES);
        if (długość_WARTOŚĆ < 0) return długość_WARTOŚĆ;
        int nazwa_pliku = Pamięć_system_plików.ZNAJDŹ_wpis(ścieżka_nazwa, długość_WARTOŚĆ);
        if (nazwa_pliku < 0) return nazwa_pliku;
        Pamięć_system_plików.이름들[nazwa_pliku * 64] = 0;
        return 0;
    }
    static int set_Plik_długość(int deskryptor_wpis, int długość_WARTOŚĆ) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return -9;
        if (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] != 2 || (otwarty_Ustawienia[deskryptor_WARTOŚĆ] & 3) == 0 || długość_WARTOŚĆ < 0) return -22;
        if (długość_WARTOŚĆ > Pamięć_system_plików.최대크기) return -27;
        int nazwa_pliku = wartość_docelowa[deskryptor_WARTOŚĆ], Adres = urządzenie_WARTOŚĆ.Plik_Pamięć() + nazwa_pliku * Pamięć_system_plików.최대크기;
        for (int INDEKS = Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku]; INDEKS < długość_WARTOŚĆ; INDEKS++) urządzenie_WARTOŚĆ.zapis_Pamięć(Adres + INDEKS, 0);
        Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku] = długość_WARTOŚĆ;
        return 0;
    }
    static int 파일상태읽기(int deskryptor_wpis, int Adres) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return -9;
        if (!wykonanie_Menedżer.obcinać(Adres, 48)) return -14;
        for (int INDEKS = 0; INDEKS < 12; INDEKS++) wykonanie_Menedżer.zapis_identyfikator(Adres + INDEKS * 4, 0);
        int nazwa_pliku = wartość_docelowa[deskryptor_WARTOŚĆ], Rozmiar = Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 2 ? Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku] : 0;
        int udzielenie_pozwolenie = Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 2 ? Pamięć_system_plików.허가들[nazwa_pliku] : 438;
        wykonanie_Menedżer.zapis_identyfikator(Adres, 1);
        wykonanie_Menedżer.zapis_identyfikator(Adres + 4, Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 2 ? nazwa_pliku + 1 : 100 + deskryptor_WARTOŚĆ);
        wykonanie_Menedżer.zapis_identyfikator(Adres + 8, (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 2 ? 32768 : (Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 1 ? 8192 : 49152)) | udzielenie_pozwolenie);
        wykonanie_Menedżer.zapis_identyfikator(Adres + 12, Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 2 && Pamięć_system_plików.이름들[nazwa_pliku * 64] == 0 ? 0 : 1);
        wykonanie_Menedżer.zapis_identyfikator(Adres + 28, Rozmiar); wykonanie_Menedżer.zapis_identyfikator(Adres + 32, 512);
        wykonanie_Menedżer.zapis_identyfikator(Adres + 36, (Rozmiar + 511) / 512);
        return 0;
    }
    static int kontrola_deskryptor(int deskryptor_wpis, int polecenie, int WARTOŚĆ) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return -9;
        if (polecenie == 0 || polecenie == 1030) return Duplikuj_deskryptor(deskryptor_wpis, WARTOŚĆ, false, polecenie == 1030 ? 1 : 0);
        if (polecenie == 1) return set_deskryptor[deskryptor_wpis];
        if (polecenie == 2) { if ((WARTOŚĆ & ~1) != 0) return -22; set_deskryptor[deskryptor_wpis] = WARTOŚĆ; return 0; }
        if (polecenie == 3) return otwarty_Ustawienia[deskryptor_WARTOŚĆ];
        if (polecenie == 4) {
            if ((WARTOŚĆ & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            otwarty_Ustawienia[deskryptor_WARTOŚĆ] = (otwarty_Ustawienia[deskryptor_WARTOŚĆ] & 3) | (WARTOŚĆ & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Twórca_uczestnik(int 주소체계, int sieć_Rodzaj, int sprawa_identyfikator) {
        if (주소체계 != 2) return -97;
        if (sieć_Rodzaj != 2) return -93;
        if (sprawa_identyfikator != 0 && sprawa_identyfikator != 17) return -93;
        int deskryptor_wpis = 빈서술자(0), deskryptor_WARTOŚĆ = 빈기술();
        if (deskryptor_wpis < 0 || deskryptor_WARTOŚĆ < 0) return -24;
        return Połącz(deskryptor_wpis, deskryptor_WARTOŚĆ, 3, 0, R_W_flaga);
    }
    static int uczestnik_deskryptor(int deskryptor_wpis) {
        int deskryptor_WARTOŚĆ = ZNAJDŹ_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return -9;
        return Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] == 3 ? deskryptor_WARTOŚĆ : -88;
    }
    static int ADRES_32(int Adres) {
        return urządzenie_WARTOŚĆ.기억읽기(Adres) << 24 | urządzenie_WARTOŚĆ.기억읽기(Adres + 1) << 16
            | urządzenie_WARTOŚĆ.기억읽기(Adres + 2) << 8 | urządzenie_WARTOŚĆ.기억읽기(Adres + 3);
    }
    static int czek_ADRES(int Adres, int długość_WARTOŚĆ) {
        if (długość_WARTOŚĆ < 16) return -22;
        if (!wykonanie_Menedżer.obcinać(Adres, 16)) return -14;
        return wykonanie_Menedżer.짧은수(Adres) == 2 ? 0 : -97;
    }
    static int BIND_ADRES(int deskryptor_wpis, int Adres, int długość_WARTOŚĆ) {
        int deskryptor_WARTOŚĆ = uczestnik_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return deskryptor_WARTOŚĆ;
        int WYNIK = czek_ADRES(Adres, długość_WARTOŚĆ);
        if (WYNIK < 0) return WYNIK;
        if (sieć_uchwyt[deskryptor_WARTOŚĆ] != 0) return -22;
        int identyfikator_sieciowy = ADRES_32(Adres + 4);
        if (identyfikator_sieciowy != 0 && identyfikator_sieciowy != sieć_Stos.내주소) return -99;
        int numer_portu = urządzenie_WARTOŚĆ.기억읽기(Adres + 2) << 8 | urządzenie_WARTOŚĆ.기억읽기(Adres + 3);
        WYNIK = sieć_Stos.Otwórz(numer_portu);
        if (WYNIK < 0) return WYNIK;
        sieć_uchwyt[deskryptor_WARTOŚĆ] = WYNIK; wartość_docelowa[deskryptor_WARTOŚĆ] = identyfikator_sieciowy;
        return 0;
    }
    static int Automatyczny_BIND(int deskryptor_WARTOŚĆ) {
        if (sieć_uchwyt[deskryptor_WARTOŚĆ] != 0) return 0;
        int WYNIK = sieć_Stos.Otwórz(0);
        if (WYNIK < 0) return WYNIK;
        sieć_uchwyt[deskryptor_WARTOŚĆ] = WYNIK;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 żądanie 구조체로 전달한다.
    static int wysłać_datagram_dane(int deskryptor_wpis, int dane_ADRES, int długość_WARTOŚĆ, int Ustawienia, int wymagane_ADRES) {
        int deskryptor_WARTOŚĆ = uczestnik_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return deskryptor_WARTOŚĆ;
        if (Ustawienia != 0) return -95;
        if (długość_WARTOŚĆ < 0 || długość_WARTOŚĆ > 1024) return -90;
        if (długość_WARTOŚĆ != 0 && !wykonanie_Menedżer.obcinać(dane_ADRES, długość_WARTOŚĆ)) return -14;
        if (!wykonanie_Menedżer.obcinać(wymagane_ADRES, 8)) return -14;
        int Adres = wykonanie_Menedżer.identyfikator(wymagane_ADRES);
        int WYNIK = czek_ADRES(Adres, wykonanie_Menedżer.identyfikator(wymagane_ADRES + 4));
        if (WYNIK < 0) return WYNIK;
        int numer_portu = urządzenie_WARTOŚĆ.기억읽기(Adres + 2) << 8 | urządzenie_WARTOŚĆ.기억읽기(Adres + 3);
        if (numer_portu == 0) return -22;
        WYNIK = Automatyczny_BIND(deskryptor_WARTOŚĆ);
        if (WYNIK < 0) return WYNIK;
        for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ; INDEKS++) transfer_dane[INDEKS] = urządzenie_WARTOŚĆ.기억읽기(dane_ADRES + INDEKS);
        return sieć_Stos.wysłać(sieć_uchwyt[deskryptor_WARTOŚĆ], ADRES_32(Adres + 4), numer_portu, transfer_dane, długość_WARTOŚĆ);
    }
    static void zapis_ADRES(int Adres, int długość_WARTOŚĆ, int identyfikator_sieciowy, int numer_portu) {
        for (int INDEKS = 0; INDEKS < długość_WARTOŚĆ && INDEKS < 16; INDEKS++) {
            int WARTOŚĆ = 0;
            if (INDEKS == 0) WARTOŚĆ = 2;
            if (INDEKS == 2) WARTOŚĆ = numer_portu >>> 8;
            if (INDEKS == 3) WARTOŚĆ = numer_portu;
            if (INDEKS >= 4 && INDEKS < 8) WARTOŚĆ = identyfikator_sieciowy >>> (56 - INDEKS * 8);
            urządzenie_WARTOŚĆ.zapis_Pamięć(Adres + INDEKS, WARTOŚĆ & 255);
        }
    }
    static int odbierać_datagram_dane(int deskryptor_wpis, int dane_ADRES, int długość_WARTOŚĆ, int Ustawienia, int wymagane_ADRES) {
        int deskryptor_WARTOŚĆ = uczestnik_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return deskryptor_WARTOŚĆ;
        if ((Ustawienia & ~64) != 0) return -95;
        if (długość_WARTOŚĆ < 0) return -22;
        if (długość_WARTOŚĆ != 0 && !wykonanie_Menedżer.obcinać(dane_ADRES, długość_WARTOŚĆ)) return -14;
        int Adres = 0, ADRES_długość_ADRES = 0, ADRES_długość = 0;
        if (wymagane_ADRES != 0) {
            if (!wykonanie_Menedżer.obcinać(wymagane_ADRES, 8)) return -14;
            Adres = wykonanie_Menedżer.identyfikator(wymagane_ADRES); ADRES_długość_ADRES = wykonanie_Menedżer.identyfikator(wymagane_ADRES + 4);
            if (Adres != 0) {
                if (!wykonanie_Menedżer.obcinać(ADRES_długość_ADRES, 4)) return -14;
                ADRES_długość = wykonanie_Menedżer.identyfikator(ADRES_długość_ADRES);
                if (ADRES_długość < 0) return -22;
                if (!wykonanie_Menedżer.obcinać(Adres, ADRES_długość < 16 ? ADRES_długość : 16)) return -14;
            }
        }
        int WYNIK = Automatyczny_BIND(deskryptor_WARTOŚĆ);
        if (WYNIK < 0) return WYNIK;
        int Uruchom_2 = urządzenie_WARTOŚĆ.밀리초();
        while (true) {
            WYNIK = sieć_Stos.odbierać(sieć_uchwyt[deskryptor_WARTOŚĆ], transfer_dane, 1024, 0);
            if (WYNIK != -11) break;
            if ((Ustawienia & 64) != 0 || (otwarty_Ustawienia[deskryptor_WARTOŚĆ] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[deskryptor_WARTOŚĆ] > 0 && urządzenie_WARTOŚĆ.밀리초() - Uruchom_2 >= 수신대기밀리초[deskryptor_WARTOŚĆ]) return -11;
            if (urządzenie_WARTOŚĆ.사용자남은밀리초() <= 10) return -11;
            urządzenie_WARTOŚĆ.잠시양보();
        }
        if (WYNIK < 0) return WYNIK;
        if (WYNIK > długość_WARTOŚĆ) WYNIK = długość_WARTOŚĆ;
        for (int INDEKS = 0; INDEKS < WYNIK; INDEKS++) urządzenie_WARTOŚĆ.zapis_Pamięć(dane_ADRES + INDEKS, transfer_dane[INDEKS]);
        if (Adres != 0) {
            zapis_ADRES(Adres, ADRES_długość, sieć_Stos.węzeł_równorzędny_ADRES(sieć_uchwyt[deskryptor_WARTOŚĆ]), sieć_Stos.węzeł_równorzędny_numer_portu(sieć_uchwyt[deskryptor_WARTOŚĆ]));
            wykonanie_Menedżer.zapis_identyfikator(ADRES_długość_ADRES, 16);
        }
        return WYNIK;
    }
    static int 통신주소읽기(int deskryptor_wpis, int Adres, int długość_ADRES) {
        int deskryptor_WARTOŚĆ = uczestnik_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return deskryptor_WARTOŚĆ;
        if (!wykonanie_Menedżer.obcinać(długość_ADRES, 4)) return -14;
        int długość_WARTOŚĆ = wykonanie_Menedżer.identyfikator(długość_ADRES);
        if (długość_WARTOŚĆ < 0) return -22;
        if (!wykonanie_Menedżer.obcinać(Adres, długość_WARTOŚĆ < 16 ? długość_WARTOŚĆ : 16)) return -14;
        int gniazdo_wpis = sieć_Stos.INDEKS(sieć_uchwyt[deskryptor_WARTOŚĆ]);
        zapis_ADRES(Adres, długość_WARTOŚĆ, wartość_docelowa[deskryptor_WARTOŚĆ], gniazdo_wpis < 0 ? 0 : sieć_Stos.접속번호들[gniazdo_wpis]);
        wykonanie_Menedżer.zapis_identyfikator(długość_ADRES, 16);
        return 0;
    }
    static int set_odbierać_TIMEOUT(int deskryptor_wpis, int 밀리초) {
        int deskryptor_WARTOŚĆ = uczestnik_deskryptor(deskryptor_wpis);
        if (deskryptor_WARTOŚĆ < 0) return deskryptor_WARTOŚĆ;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[deskryptor_WARTOŚĆ] = 밀리초;
        return 0;
    }
}
