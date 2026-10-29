// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 powłoka Stan_WARTOŚĆ. nazwa_pliku 저장소는 공유하고 ścieżka_2/zmienna_WARTOŚĆ/LOG_zapis/입력은 분리한다. */
public final class okno_sesja {
    static int[] 보관 = new int[4 * 30000], Przygotuj = new int[4];
    static int bieżący_towar, pozycja;
    static boolean 이어읽기;
    static void TABLICA_WARTOŚĆ(int[] dane, boolean Store_WARTOŚĆ) {
        for (int Loop_INDEKS = 0; Loop_INDEKS < dane.length; Loop_INDEKS++) { if (Store_WARTOŚĆ) 보관[pozycja++] = dane[Loop_INDEKS]; else dane[Loop_INDEKS] = 보관[pozycja++]; }
    }
    static int WARTOŚĆ(int dane_WARTOŚĆ, boolean 저장여부) { if (저장여부) { 보관[pozycja++] = dane_WARTOŚĆ; return dane_WARTOŚĆ; } return 보관[pozycja++]; }
    static void szukać_stanowisko(int 보관칸, boolean 저장여부) {
        pozycja = 보관칸 * 30000;
        TABLICA_WARTOŚĆ(Pamięć_Files.bieżący_towar, 저장여부); Pamięć_Files.bieżący_długość = WARTOŚĆ(Pamięć_Files.bieżący_długość, 저장여부);
        TABLICA_WARTOŚĆ(powłoka_składnia.zmienna_nazwa, 저장여부); TABLICA_WARTOŚĆ(powłoka_składnia.zmienna_dane, 저장여부); TABLICA_WARTOŚĆ(powłoka_składnia.이름길이, 저장여부); TABLICA_WARTOŚĆ(powłoka_składnia.WARTOŚĆ_długość, 저장여부);
        powłoka_składnia.Stan_WARTOŚĆ = WARTOŚĆ(powłoka_składnia.Stan_WARTOŚĆ, 저장여부);
        TABLICA_WARTOŚĆ(edytor_wierszowy.LOG_zapis, 저장여부); TABLICA_WARTOŚĆ(edytor_wierszowy.LOG_długość, 저장여부); TABLICA_WARTOŚĆ(edytor_wierszowy.Store_WARTOŚĆ, 저장여부); TABLICA_WARTOŚĆ(polecenie_interpreter.wiersz_wejścia, 저장여부);
        edytor_wierszowy.LOG_ILE_LICZB = WARTOŚĆ(edytor_wierszowy.LOG_ILE_LICZB, 저장여부); edytor_wierszowy.LOG_zapis_Koniec = WARTOŚĆ(edytor_wierszowy.LOG_zapis_Koniec, 저장여부);
        edytor_wierszowy.Search_WARTOŚĆ = WARTOŚĆ(edytor_wierszowy.Search_WARTOŚĆ, 저장여부); edytor_wierszowy.저장길이 = WARTOŚĆ(edytor_wierszowy.저장길이, 저장여부);
        edytor_wierszowy.Rozmiar = WARTOŚĆ(edytor_wierszowy.Rozmiar, 저장여부); edytor_wierszowy.kursor_WARTOŚĆ = WARTOŚĆ(edytor_wierszowy.kursor_WARTOŚĆ, 저장여부); edytor_wierszowy.START_okno = WARTOŚĆ(edytor_wierszowy.START_okno, 저장여부);
        Przygotuj[보관칸] = 1;
    }
    static void Proces_WARTOŚĆ_wpis() {
        int konkurs_identyfikator = Tablica.interpretator_poleceń(12); if (konkurs_identyfikator == 0) return;
        szukać_stanowisko(bieżący_towar, true);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 4; Loop_INDEKS++) {
            if ((konkurs_identyfikator & (1 << (8 + Loop_INDEKS))) != 0) { Tablica.kontrola_użytkownik_program(32 + Loop_INDEKS); Przygotuj[Loop_INDEKS] = 0; }
            if ((konkurs_identyfikator & (1 << (4 + Loop_INDEKS))) != 0 && Loop_INDEKS != bieżący_towar) Przygotuj[Loop_INDEKS] = 0;
        }
        int Dalej_stanowisko = (konkurs_identyfikator & 15) - 1; if (Dalej_stanowisko < 0) Dalej_stanowisko = 0;
        if (Przygotuj[Dalej_stanowisko] == 0) for (int Loop_INDEKS = 0; Loop_INDEKS < 30000; Loop_INDEKS++) 보관[Dalej_stanowisko * 30000 + Loop_INDEKS] = 0;
        bieżący_towar = Dalej_stanowisko; szukać_stanowisko(bieżący_towar, false); Tablica.interpretator_poleceń(100 + bieżący_towar); 이어읽기 = true;
        단말.Zapis("\nTERMINAL FOCUS "); 단말.identyfikator(bieżący_towar + 1); 단말.문자(10);
    }
    static boolean CV_wykonanie() {
        if (Tablica.kontrola_użytkownik_program(16 + bieżący_towar) == 0) return false;
        셸입출력.Zezwalaj_interakcyjny = true; 셸입출력.Uruchom_2(false, false); Tablica.입출력전환(1);
        int 처리값 = Tablica.kontrola_użytkownik_program(bieżący_towar); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; powłoka_składnia.Stan_WARTOŚĆ = 처리값 < 0 ? 126 : 처리값; 단말.Zapis("exit "); 단말.identyfikator(처리값); 단말.문자(10); Tablica.interpretator_poleceń(3); }
        return true;
    }
}
