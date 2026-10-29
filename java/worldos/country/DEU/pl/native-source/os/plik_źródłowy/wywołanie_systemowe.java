// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 przestrzeń_użytkownika wskaźnik/길이는 dostęp_wpis 전에 검사한다. */
public final class wywołanie_systemowe {
    static int[] 임시자료 = new int[1024];

    static int TABLICA_długość(int Adres) {
        if (!wykonanie_Menedżer.obcinać(Adres, 4)) return -14;
        int długość_WARTOŚĆ = wykonanie_Menedżer.identyfikator(Adres);
        if (długość_WARTOŚĆ < 0 || długość_WARTOŚĆ > (wykonanie_Menedżer.użytkownik_Koniec - Adres - 4) / 4) return -14;
        return długość_WARTOŚĆ;
    }

    public static int Proces_WARTOŚĆ_wpis(int INDEKS, int 가, int SEKUNDA_operand, int 다, int 라, int 마) {
        if (INDEKS == 30) return Plik_deskryptor_Menedżer.otwarty_Plik(가, SEKUNDA_operand, 다);
        if (INDEKS == 31) return Plik_deskryptor_Menedżer.파일읽기(가, SEKUNDA_operand, 다);
        if (INDEKS == 32) return Plik_deskryptor_Menedżer.zapis_Plik(가, SEKUNDA_operand, 다);
        if (INDEKS == 33) return Plik_deskryptor_Menedżer.Zamknij_Plik(가);
        if (INDEKS == 34) return Plik_deskryptor_Menedżer.szukać_Plik(가, SEKUNDA_operand, 다);
        if (INDEKS == 35) return Plik_deskryptor_Menedżer.Duplikuj_deskryptor(가, 0, false, 0);
        if (INDEKS == 36) return Plik_deskryptor_Menedżer.Duplikuj_deskryptor(가, SEKUNDA_operand, true, 0);
        if (INDEKS == 37) return Plik_deskryptor_Menedżer.파일상태읽기(가, SEKUNDA_operand);
        if (INDEKS == 38) return Plik_deskryptor_Menedżer.usuń_Plik_wpis_nazwa(가);
        if (INDEKS == 39) return Plik_deskryptor_Menedżer.set_Plik_długość(가, SEKUNDA_operand);
        if (INDEKS == 40) return Plik_deskryptor_Menedżer.kontrola_deskryptor(가, SEKUNDA_operand, 다);
        if (INDEKS == 41) return Plik_deskryptor_Menedżer.Twórca_uczestnik(가, SEKUNDA_operand, 다);
        if (INDEKS == 42) return Plik_deskryptor_Menedżer.BIND_ADRES(가, SEKUNDA_operand, 다);
        if (INDEKS == 43) return Plik_deskryptor_Menedżer.wysłać_datagram_dane(가, SEKUNDA_operand, 다, 라, 마);
        if (INDEKS == 44) return Plik_deskryptor_Menedżer.odbierać_datagram_dane(가, SEKUNDA_operand, 다, 라, 마);
        if (INDEKS == 45) return Plik_deskryptor_Menedżer.통신주소읽기(가, SEKUNDA_operand, 다);
        if (INDEKS == 46) return Plik_deskryptor_Menedżer.set_odbierać_TIMEOUT(가, SEKUNDA_operand);
        if (INDEKS == 47) {
            int deskryptor_WARTOŚĆ = Plik_deskryptor_Menedżer.ZNAJDŹ_deskryptor(가);
            if (deskryptor_WARTOŚĆ < 0) return -9;
            if (Plik_deskryptor_Menedżer.Rodzaj_WARTOŚĆ[deskryptor_WARTOŚĆ] != 2) return -22;
            return 파일보존.synchronizować();
        }
        if (INDEKS == 1) {
            int długość_WARTOŚĆ = TABLICA_długość(가);
            if (długość_WARTOŚĆ < 0) return długość_WARTOŚĆ;
            if (długość_WARTOŚĆ > 4096) return -90;
            for (int znak_WARTOŚĆ = 0; znak_WARTOŚĆ < długość_WARTOŚĆ; znak_WARTOŚĆ++) SMS_Terminal.문자(wykonanie_Menedżer.identyfikator(가 + 4 + znak_WARTOŚĆ * 4) & 65535);
            return długość_WARTOŚĆ;
        }
        if (INDEKS == 2) return wykonanie_Menedżer.argument_ILE_LICZB;
        if (INDEKS == 3) return 가 >= 0 && 가 < wykonanie_Menedżer.argument_ILE_LICZB ? wykonanie_Menedżer.argument_ADRES[가] : 0;
        if (INDEKS == 10) return sieć_Stos.Otwórz(가);
        if (INDEKS == 11) {
            int długość_WARTOŚĆ = TABLICA_długość(라);
            if (długość_WARTOŚĆ < 0) return długość_WARTOŚĆ;
            if (마 < 0 || 마 > długość_WARTOŚĆ || 마 > 1024) return -90;
            for (int pozycja = 0; pozycja < 마; pozycja++) 임시자료[pozycja] = wykonanie_Menedżer.identyfikator(라 + 4 + pozycja * 4) & 255;
            return sieć_Stos.wysłać(가, SEKUNDA_operand, 다, 임시자료, 마);
        }
        if (INDEKS == 12) {
            int długość_WARTOŚĆ = TABLICA_długość(SEKUNDA_operand);
            if (długość_WARTOŚĆ < 0) return długość_WARTOŚĆ;
            if (다 < 0 || 다 > 2000) return -22;
            int WYNIK = sieć_Stos.odbierać(가, 임시자료, długość_WARTOŚĆ < 1024 ? długość_WARTOŚĆ : 1024, 다);
            if (WYNIK >= 0) for (int pozycja = 0; pozycja < WYNIK; pozycja++) wykonanie_Menedżer.zapis_identyfikator(SEKUNDA_operand + 4 + pozycja * 4, 임시자료[pozycja]);
            return WYNIK;
        }
        if (INDEKS == 13) return sieć_Stos.Zamknięte(가);
        if (INDEKS == 14) return sieć_Stos.내주소;
        if (INDEKS == 15) return sieć_Stos.węzeł_równorzędny_ADRES(가);
        if (INDEKS == 16) return sieć_Stos.węzeł_równorzędny_numer_portu(가);
        if (INDEKS == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEKS == 20 || INDEKS == 21) {
            int nazwa_zmienić_rozmiar = TABLICA_długość(가), dane_zmienić_rozmiar = TABLICA_długość(SEKUNDA_operand);
            if (nazwa_zmienić_rozmiar < 0 || dane_zmienić_rozmiar < 0) return -14;
            if (nazwa_zmienić_rozmiar < 1 || nazwa_zmienić_rozmiar > 64) return -22;
            int długość_WARTOŚĆ = 0;
            while (długość_WARTOŚĆ < nazwa_zmienić_rozmiar && wykonanie_Menedżer.identyfikator(가 + 4 + długość_WARTOŚĆ * 4) != 0) {
                Pamięć_system_plików.Nazwa[długość_WARTOŚĆ] = wykonanie_Menedżer.identyfikator(가 + 4 + długość_WARTOŚĆ * 4);
                długość_WARTOŚĆ++;
            }
            if (!Pamięć_system_plików.czek_nazwa(Pamięć_system_plików.Nazwa, długość_WARTOŚĆ)) return -22;
            if (INDEKS == 20) {
                int nazwa_pliku = Pamięć_system_plików.ZNAJDŹ_wpis(Pamięć_system_plików.Nazwa, długość_WARTOŚĆ);
                if (nazwa_pliku < 0) return nazwa_pliku;
                int Rozmiar = Pamięć_system_plików.zmienić_rozmiar_Lista[nazwa_pliku];
                if (Rozmiar > dane_zmienić_rozmiar) return -90;
                int Adres = urządzenie_WARTOŚĆ.Plik_Pamięć() + nazwa_pliku * Pamięć_system_plików.최대크기;
                for (int identyfikator = 0; identyfikator < Rozmiar; identyfikator++) wykonanie_Menedżer.zapis_identyfikator(SEKUNDA_operand + 4 + identyfikator * 4, urządzenie_WARTOŚĆ.기억읽기(Adres + identyfikator));
                return Rozmiar;
            }
            if (다 < 0 || 다 > dane_zmienić_rozmiar) return -22;
            if (다 > Pamięć_system_plików.최대크기) return -90;
            for (int identyfikator = 0; identyfikator < 다; identyfikator++) Pamięć_system_plików.Edytuj_WARTOŚĆ[identyfikator] = wykonanie_Menedżer.identyfikator(SEKUNDA_operand + 4 + identyfikator * 4) & 255;
            return Pamięć_system_plików.Store_WARTOŚĆ(Pamięć_system_plików.Nazwa, długość_WARTOŚĆ, Pamięć_system_plików.Edytuj_WARTOŚĆ, 다);
        }
        return -38;
    }
}
