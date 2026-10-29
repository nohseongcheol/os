// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Odczyt 전용 Wykonaj_polecenie 묶음의 ELF32 walidować, argumenty Dalej_WARTOŚĆ, 한 번에 한 przestrzeń_użytkownika Proces_WARTOŚĆ Wykonaj_polecenie. */
public final class wykonanie_Menedżer {
    static final int START_użytkownik_program = 0x04000000;
    static final int użytkownik_Koniec = 0x04400000;
    static final int OBRAZ_Koniec_ADRES = 0x04200000;
    static final int argument_START = 0x04300000;
    static int argument_ILE_LICZB = 0;
    static int[] argument_ADRES = new int[16];

    static boolean obcinać(int Adres, int długość_WARTOŚĆ) {
        return Adres >= START_użytkownik_program && Adres < użytkownik_Koniec && długość_WARTOŚĆ >= 0 && długość_WARTOŚĆ <= użytkownik_Koniec - Adres;
    }

    static int identyfikator(int Adres) { return Pamięć_region.analizować_liczba_całkowita(Adres); }
    static int 짧은수(int Adres) { return urządzenie_WARTOŚĆ.기억읽기(Adres) | urządzenie_WARTOŚĆ.기억읽기(Adres + 1) << 8; }
    static void zapis_identyfikator(int Adres, int WARTOŚĆ) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) urządzenie_WARTOŚĆ.zapis_Pamięć(Adres + INDEKS, WARTOŚĆ >>> (INDEKS * 8));
    }

    static int grupa_ILE_LICZB() {
        int Adres = urządzenie_WARTOŚĆ.wykonywalny_pakiet();
        int Rozmiar = urządzenie_WARTOŚĆ.wykonywalny_pakiet_zmienić_rozmiar();
        if (Rozmiar < 8 || identyfikator(Adres) != 0x50414b4a) return 0;
        int towar_ILE_LICZB = identyfikator(Adres + 4);
        return towar_ILE_LICZB >= 0 && towar_ILE_LICZB <= 32 && towar_ILE_LICZB <= (Rozmiar - 8) / 24 ? towar_ILE_LICZB : 0;
    }

    static void wpis_Lista() {
        for (int INDEKS = 0; INDEKS < grupa_ILE_LICZB(); INDEKS++) {
            int wpis_WARTOŚĆ = urządzenie_WARTOŚĆ.wykonywalny_pakiet() + 8 + INDEKS * 24;
            for (int znak_WARTOŚĆ = 0; znak_WARTOŚĆ < 16 && urządzenie_WARTOŚĆ.기억읽기(wpis_WARTOŚĆ + znak_WARTOŚĆ) != 0; znak_WARTOŚĆ++)
                SMS_Terminal.문자(urządzenie_WARTOŚĆ.기억읽기(wpis_WARTOŚĆ + znak_WARTOŚĆ));
            SMS_Terminal.Zapis("\n");
        }
    }

    static int ZNAJDŹ_wpis(int[] wejście_WARTOŚĆ, int Uruchom_2, int długość_WARTOŚĆ) {
        if (długość_WARTOŚĆ <= 0 || długość_WARTOŚĆ >= 16) return 0;
        for (int INDEKS = 0; INDEKS < grupa_ILE_LICZB(); INDEKS++) {
            int wpis_WARTOŚĆ = urządzenie_WARTOŚĆ.wykonywalny_pakiet() + 8 + INDEKS * 24;
            boolean 같음 = urządzenie_WARTOŚĆ.기억읽기(wpis_WARTOŚĆ + długość_WARTOŚĆ) == 0;
            for (int znak_WARTOŚĆ = 0; znak_WARTOŚĆ < długość_WARTOŚĆ; znak_WARTOŚĆ++)
                if (wejście_WARTOŚĆ[Uruchom_2 + znak_WARTOŚĆ] != urządzenie_WARTOŚĆ.기억읽기(wpis_WARTOŚĆ + znak_WARTOŚĆ)) 같음 = false;
            if (같음) return wpis_WARTOŚĆ;
        }
        return 0;
    }

    static int walidować(int nazwa_pliku, int długość_WARTOŚĆ) {
        if (długość_WARTOŚĆ < 52 || identyfikator(nazwa_pliku) != 0x464c457f || urządzenie_WARTOŚĆ.기억읽기(nazwa_pliku + 4) != 1
            || urządzenie_WARTOŚĆ.기억읽기(nazwa_pliku + 5) != 1 || urządzenie_WARTOŚĆ.기억읽기(nazwa_pliku + 6) != 1
            || 짧은수(nazwa_pliku + 16) != 2 || 짧은수(nazwa_pliku + 18) != 3 || identyfikator(nazwa_pliku + 20) != 1
            || 짧은수(nazwa_pliku + 40) != 52 || 짧은수(nazwa_pliku + 42) != 32) return -8;
        int punkt_wejścia_WARTOŚĆ = identyfikator(nazwa_pliku + 24);
        int tabela_stanowisko = identyfikator(nazwa_pliku + 28);
        int towar_ILE_LICZB = 짧은수(nazwa_pliku + 44);
        if (towar_ILE_LICZB == 0 || towar_ILE_LICZB > 16 || tabela_stanowisko < 52 || tabela_stanowisko > długość_WARTOŚĆ - towar_ILE_LICZB * 32) return -8;
        boolean systemy_informacyjne_wykonywalny = false;
        for (int INDEKS = 0; INDEKS < towar_ILE_LICZB; INDEKS++) {
            int WYSZUKAJ_tabela = nazwa_pliku + tabela_stanowisko + INDEKS * 32;
            int Rodzaj_WARTOŚĆ = identyfikator(WYSZUKAJ_tabela);
            if (Rodzaj_WARTOŚĆ == 2 || Rodzaj_WARTOŚĆ == 3) return -8; // 동적 Połącz/parser_48ee4b1b 미지원
            if (Rodzaj_WARTOŚĆ != 1) continue;
            int pozycja = identyfikator(WYSZUKAJ_tabela + 4), Adres = identyfikator(WYSZUKAJ_tabela + 8), rozmiar_pliku = identyfikator(WYSZUKAJ_tabela + 16), Pamięć_zmienić_rozmiar = identyfikator(WYSZUKAJ_tabela + 20);
            int wyrównać_WARTOŚĆ = identyfikator(WYSZUKAJ_tabela + 28);
            if (Adres < START_użytkownik_program || Adres >= OBRAZ_Koniec_ADRES || Pamięć_zmienić_rozmiar < 0 || Pamięć_zmienić_rozmiar > OBRAZ_Koniec_ADRES - Adres
                || rozmiar_pliku < 0 || rozmiar_pliku > Pamięć_zmienić_rozmiar || pozycja < 0 || (rozmiar_pliku > 0 && pozycja > długość_WARTOŚĆ - rozmiar_pliku)
                || (wyrównać_WARTOŚĆ != 0 && (wyrównać_WARTOŚĆ < 0 || (wyrównać_WARTOŚĆ & (wyrównać_WARTOŚĆ - 1)) != 0
                    || ((Adres - pozycja) & (wyrównać_WARTOŚĆ - 1)) != 0))) return -8;
            for (int przód_WARTOŚĆ = 0; przód_WARTOŚĆ < INDEKS; przód_WARTOŚĆ++) {
                int Wstecz_towar = nazwa_pliku + tabela_stanowisko + przód_WARTOŚĆ * 32;
                if (identyfikator(Wstecz_towar) == 1 && Pamięć_zmienić_rozmiar > 0 && identyfikator(Wstecz_towar + 20) > 0
                    && Adres < identyfikator(Wstecz_towar + 8) + identyfikator(Wstecz_towar + 20) && identyfikator(Wstecz_towar + 8) < Adres + Pamięć_zmienić_rozmiar) return -8;
            }
            if ((identyfikator(WYSZUKAJ_tabela + 24) & 1) != 0 && punkt_wejścia_WARTOŚĆ >= Adres && punkt_wejścia_WARTOŚĆ - Adres < rozmiar_pliku) systemy_informacyjne_wykonywalny = true;
        }
        return systemy_informacyjne_wykonywalny ? punkt_wejścia_WARTOŚĆ : -8;
    }

    static int Wykonaj_polecenie(int[] wejście_WARTOŚĆ, int Uruchom_2, int długość_WARTOŚĆ) {
        while (Uruchom_2 < długość_WARTOŚĆ && wejście_WARTOŚĆ[Uruchom_2] == ' ') Uruchom_2++;
        int 끝 = Uruchom_2;
        while (끝 < długość_WARTOŚĆ && wejście_WARTOŚĆ[끝] != ' ') 끝++;
        int wpis_WARTOŚĆ = ZNAJDŹ_wpis(wejście_WARTOŚĆ, Uruchom_2, 끝 - Uruchom_2);
        if (wpis_WARTOŚĆ == 0) return -2;
        int pozycja = identyfikator(wpis_WARTOŚĆ + 16), Rozmiar = identyfikator(wpis_WARTOŚĆ + 20);
        if (pozycja < 8 + grupa_ILE_LICZB() * 24 || Rozmiar < 52 || pozycja > urządzenie_WARTOŚĆ.wykonywalny_pakiet_zmienić_rozmiar() - Rozmiar) return -8;
        int nazwa_pliku = urządzenie_WARTOŚĆ.wykonywalny_pakiet() + pozycja;
        int punkt_wejścia_WARTOŚĆ = walidować(nazwa_pliku, Rozmiar);
        if (punkt_wejścia_WARTOŚĆ < 0) return punkt_wejścia_WARTOŚĆ;
        urządzenie_WARTOŚĆ.użytkownik_czyścić_Spis_treści();
        int tabela_stanowisko = identyfikator(nazwa_pliku + 28), towar_ILE_LICZB = 짧은수(nazwa_pliku + 44);
        for (int INDEKS = 0; INDEKS < towar_ILE_LICZB; INDEKS++) {
            int WYSZUKAJ_tabela = nazwa_pliku + tabela_stanowisko + INDEKS * 32;
            if (identyfikator(WYSZUKAJ_tabela) != 1) continue;
            int 원본 = nazwa_pliku + identyfikator(WYSZUKAJ_tabela + 4), cel_WARTOŚĆ = identyfikator(WYSZUKAJ_tabela + 8), rozmiar_pliku = identyfikator(WYSZUKAJ_tabela + 16);
            for (int bajt_WARTOŚĆ = 0; bajt_WARTOŚĆ < rozmiar_pliku; bajt_WARTOŚĆ++) urządzenie_WARTOŚĆ.zapis_Pamięć(cel_WARTOŚĆ + bajt_WARTOŚĆ, urządzenie_WARTOŚĆ.기억읽기(원본 + bajt_WARTOŚĆ));
        }
        argument_ILE_LICZB = 0;
        int Store_WARTOŚĆ = argument_START;
        while (끝 < długość_WARTOŚĆ) {
            while (끝 < długość_WARTOŚĆ && wejście_WARTOŚĆ[끝] == ' ') 끝++;
            if (끝 == długość_WARTOŚĆ) break;
            if (argument_ILE_LICZB == argument_ADRES.length) return -22;
            Uruchom_2 = 끝;
            while (끝 < długość_WARTOŚĆ && wejście_WARTOŚĆ[끝] != ' ') 끝++;
            argument_ADRES[argument_ILE_LICZB++] = Store_WARTOŚĆ;
            zapis_identyfikator(Store_WARTOŚĆ, 끝 - Uruchom_2);
            for (int znak_WARTOŚĆ = Uruchom_2; znak_WARTOŚĆ < 끝; znak_WARTOŚĆ++) zapis_identyfikator(Store_WARTOŚĆ + 4 + (znak_WARTOŚĆ - Uruchom_2) * 4, wejście_WARTOŚĆ[znak_WARTOŚĆ]);
            Store_WARTOŚĆ += 4 + (끝 - Uruchom_2) * 4;
        }
        sieć_Stos.OCZYŚĆ_Proces();
        Plik_deskryptor_Menedżer.START_Proces();
        int WYNIK = urządzenie_WARTOŚĆ.przebieg_użytkownik_program(punkt_wejścia_WARTOŚĆ, użytkownik_Koniec - 16);
        Plik_deskryptor_Menedżer.OCZYŚĆ_Proces();
        sieć_Stos.OCZYŚĆ_Proces();
        return WYNIK;
    }
}
