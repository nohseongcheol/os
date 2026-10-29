// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 powłoka 내장 narzędzia. */
public final class powłoka_Narzędzia {
    static int[] dane = new int[16384];
    static int plik_wejściowy = -1;
    static int otwarty_Plik(int argument_INDEKS, int Proces_tryb) {
        int 처리값 = polecenie_interpreter.ścieżka_2(argument_INDEKS); return 처리값 < 0 ? 처리값 : Pamięć_Files.Otwórz(Proces_tryb);
    }
    static boolean Przygotuj_wejście(int argument_INDEKS) {
        plik_wejściowy = -1;
        if (argument_INDEKS < polecenie_interpreter.token_ILE_LICZB) {
            plik_wejściowy = otwarty_Plik(argument_INDEKS, 0);
            if (plik_wejściowy < 0) { polecenie_interpreter.błąd(plik_wejściowy); return false; }
        }
        return true;
    }
    static int Odczyt() {
        if (plik_wejściowy >= 3) return Pamięć_Files.Odczyt(plik_wejściowy);
        while (true) {
            int bajt_dane = Tablica.직렬읽기(); if (bajt_dane == -2 || bajt_dane == 4) return 256;
            if (bajt_dane == 3) { polecenie_interpreter.WYNIK = 130; return 256; }
            if (bajt_dane >= 0) return bajt_dane; Tablica.Dochód_CPU();
        }
    }
    static void Zamknięte() { if (plik_wejściowy >= 3) Pamięć_Files.Zamknięte(plik_wejściowy); plik_wejściowy = -1; }
    static void Widok_WARTOŚĆ() {
        int 마지막자리 = polecenie_interpreter.token_ILE_LICZB == 1 ? 2 : polecenie_interpreter.token_ILE_LICZB;
        for (int argument_INDEKS = 1; argument_INDEKS < 마지막자리; argument_INDEKS++) {
            if (!Przygotuj_wejście(argument_INDEKS)) continue;
            int bajt_dane; while ((bajt_dane = Odczyt()) != 256 && bajt_dane >= 0) Tablica.직렬쓰기(bajt_dane);
            if (bajt_dane < 0) polecenie_interpreter.błąd(bajt_dane); Zamknięte();
        }
    }
    static void Plik_sprawa(String akcja_identyfikator) {
        if (polecenie_interpreter.token_ILE_LICZB != 2) { polecenie_interpreter.WYNIK = 2; 단말.Zapis("사용법: mkdir/rmdir/touch nazwa_pliku\n"); return; }
        int 처리값 = polecenie_interpreter.ścieżka_2(1);
        if (처리값 >= 0) {
            if (akcja_identyfikator.charAt(0) == 'm') 처리값 = Pamięć_Files.Twórca_Katalog();
            else if (akcja_identyfikator.charAt(0) == 'r') 처리값 = Pamięć_Files.usuń_Katalog();
            else { 처리값 = Pamięć_Files.Otwórz(65); if (처리값 >= 3) 처리값 = Pamięć_Files.Zamknięte(처리값); }
        }
        if (처리값 < 0) polecenie_interpreter.błąd(처리값);
    }
    static void kopiować_WARTOŚĆ(boolean 이동여부) {
        if (polecenie_interpreter.token_ILE_LICZB != 3) { polecenie_interpreter.WYNIK = 2; 단말.Zapis("사용법: cp/mv 원본 cel_uczestnik (nazwa_pliku)\n"); return; }
        int 처리값 = polecenie_interpreter.ścieżka_2(1); if (처리값 >= 0) 처리값 = Pamięć_Files.normalizować_WARTOŚĆ();
        if (처리값 < 0) { polecenie_interpreter.błąd(처리값); return; }
        int 원본번호 = Pamięć_Files.ZNAJDŹ_wpis(); if (원본번호 < 0) { polecenie_interpreter.błąd(-2); return; }
        int wpis_ILE_LICZB = Pamięć_Files.długość_WARTOŚĆ[원본번호]; for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) dane[Loop_INDEKS] = Pamięć_Files.자료읽기(원본번호, Loop_INDEKS);
        처리값 = polecenie_interpreter.ścieżka_2(2); if (처리값 >= 0) 처리값 = Pamięć_Files.normalizować_WARTOŚĆ();
        if (처리값 < 0) { polecenie_interpreter.błąd(처리값); return; }
        if (Pamięć_Files.ZNAJDŹ_wpis() == 원본번호) { if (!이동여부) polecenie_interpreter.błąd(-22); return; }
        if (이동여부) { 처리값 = Pamięć_Files.Zmień_nazwę_wpis(원본번호); if (처리값 < 0) polecenie_interpreter.błąd(처리값); return; }
        int 열린파일번호 = Pamięć_Files.Otwórz(577); if (열린파일번호 < 0) { polecenie_interpreter.błąd(열린파일번호); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) { 처리값 = Pamięć_Files.Zapis(열린파일번호, dane[Loop_INDEKS]); if (처리값 < 0) { polecenie_interpreter.błąd(처리값); break; } }
        Pamięć_Files.Zamknięte(열린파일번호);
    }
    static int cyfra_WARTOŚĆ(int argument_INDEKS) {
        if (argument_INDEKS >= polecenie_interpreter.token_ILE_LICZB) return -1;
        int wpis_ILE_LICZB = 0; for (int Loop_INDEKS = 0; Loop_INDEKS < polecenie_interpreter.długość_WARTOŚĆ[argument_INDEKS]; Loop_INDEKS++) { int kod_znaku = polecenie_interpreter.token_WARTOŚĆ[polecenie_interpreter.시작점[argument_INDEKS] + Loop_INDEKS]; if (kod_znaku < '0' || kod_znaku > '9' || wpis_ILE_LICZB > 10000) return -1; wpis_ILE_LICZB = wpis_ILE_LICZB * 10 + kod_znaku - '0'; } return wpis_ILE_LICZB;
    }
    static void 세기() {
        int argument_INDEKS = 1, 선택번호 = 0;
        if (polecenie_interpreter.같음(1, "-c") || polecenie_interpreter.같음(1, "-l") || polecenie_interpreter.같음(1, "-w")) { 선택번호 = polecenie_interpreter.같음(1, "-c") ? 1 : polecenie_interpreter.같음(1, "-l") ? 2 : 3; argument_INDEKS++; }
        if (polecenie_interpreter.token_ILE_LICZB > argument_INDEKS + 1) { polecenie_interpreter.WYNIK = 2; 단말.Zapis("사용법: wc [-c|-l|-w] [nazwa_pliku]\n"); return; }
        if (!Przygotuj_wejście(argument_INDEKS)) return;
        int bajt_ILE_LICZB = 0, 줄수 = 0, 낱말수 = 0, bajt_dane; boolean 낱말 = false;
        while ((bajt_dane = Odczyt()) >= 0 && bajt_dane != 256) { bajt_ILE_LICZB++; if (bajt_dane == 10) 줄수++; boolean SPACJA = bajt_dane == 32 || bajt_dane >= 9 && bajt_dane <= 13; if (!SPACJA && !낱말) 낱말수++; 낱말 = !SPACJA; }
        Zamknięte(); if (bajt_dane < 0) { polecenie_interpreter.błąd(bajt_dane); return; }
        if (선택번호 != 0) 단말.identyfikator(선택번호 == 1 ? bajt_ILE_LICZB : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.identyfikator(줄수); 단말.문자(' '); 단말.identyfikator(낱말수); 단말.문자(' '); 단말.identyfikator(bajt_ILE_LICZB); } 단말.문자(10);
    }
    static void ZNAJDŹ_wpis() {
        if (polecenie_interpreter.token_ILE_LICZB < 2 || polecenie_interpreter.token_ILE_LICZB > 3) { polecenie_interpreter.WYNIK = 2; 단말.Zapis("사용법: grep 찾을문구 [nazwa_pliku]\n"); return; }
        if (!Przygotuj_wejście(2)) return;
        int wpis_ILE_LICZB = 0, bajt_dane, 일치수 = 0;
        while (true) {
            bajt_dane = Odczyt();
            if (bajt_dane == 10 || bajt_dane == 256 || bajt_dane < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEKS = 0; Loop_INDEKS <= wpis_ILE_LICZB - polecenie_interpreter.długość_WARTOŚĆ[1]; Loop_INDEKS++) {
                    boolean 같은여부 = true; for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < polecenie_interpreter.długość_WARTOŚĆ[1]; wewnętrzne_stanowisko++) if (dane[Loop_INDEKS + wewnętrzne_stanowisko] != polecenie_interpreter.token_WARTOŚĆ[polecenie_interpreter.시작점[1] + wewnętrzne_stanowisko]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (wpis_ILE_LICZB > 0 || bajt_dane == 10)) { for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) Tablica.직렬쓰기(dane[Loop_INDEKS]); 단말.문자(10); 일치수++; }
                wpis_ILE_LICZB = 0; if (bajt_dane != 10) break;
            } else if (wpis_ILE_LICZB < dane.length) dane[wpis_ILE_LICZB++] = bajt_dane;
            else { polecenie_interpreter.błąd(-28); Zamknięte(); return; }
        }
        Zamknięte(); if (bajt_dane < 0) polecenie_interpreter.błąd(bajt_dane); else if (polecenie_interpreter.WYNIK == 0) polecenie_interpreter.WYNIK = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEKS = 1, 줄수 = 10;
        if (polecenie_interpreter.같음(1, "-n")) { 줄수 = cyfra_WARTOŚĆ(2); argument_INDEKS = 3; }
        if (줄수 < 0 || polecenie_interpreter.token_ILE_LICZB > argument_INDEKS + 1) { polecenie_interpreter.WYNIK = 2; 단말.Zapis("사용법: head/tail [-n 줄수] [nazwa_pliku]\n"); return; }
        if (!Przygotuj_wejście(argument_INDEKS)) return;
        int wpis_ILE_LICZB = 0, bajt_dane;
        while ((bajt_dane = Odczyt()) != 256 && bajt_dane >= 0) { if (wpis_ILE_LICZB == dane.length) { polecenie_interpreter.błąd(-28); Zamknięte(); return; } dane[wpis_ILE_LICZB++] = bajt_dane; }
        Zamknięte(); if (bajt_dane < 0) { polecenie_interpreter.błąd(bajt_dane); return; }
        int lokalny_START = 0, Koniec_stanowisko = wpis_ILE_LICZB;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int suma_ILE_LICZB = 0; for (int Loop_INDEKS = wpis_ILE_LICZB - 2; Loop_INDEKS >= 0; Loop_INDEKS--) if (dane[Loop_INDEKS] == 10 && ++suma_ILE_LICZB == 줄수) { lokalny_START = Loop_INDEKS + 1; break; } }
        else { int suma_ILE_LICZB = 0; for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) if (dane[Loop_INDEKS] == 10 && ++suma_ILE_LICZB == 줄수) { Koniec_stanowisko = Loop_INDEKS + 1; break; } }
        for (int Loop_INDEKS = lokalny_START; Loop_INDEKS < Koniec_stanowisko; Loop_INDEKS++) Tablica.직렬쓰기(dane[Loop_INDEKS]);
    }
    static void zapis_Razem() {
        boolean dołączać = polecenie_interpreter.같음(1, "-a"); int argument_INDEKS = dołączać ? 2 : 1;
        if (polecenie_interpreter.token_ILE_LICZB != argument_INDEKS + 1) { polecenie_interpreter.WYNIK = 2; 단말.Zapis("사용법: tee [-a] nazwa_pliku\n"); return; }
        int 열린파일번호 = otwarty_Plik(argument_INDEKS, dołączać ? 1089 : 577); if (열린파일번호 < 0) { polecenie_interpreter.błąd(열린파일번호); return; }
        plik_wejściowy = -1; int bajt_dane;
        while ((bajt_dane = Odczyt()) != 256 && bajt_dane >= 0) { int 처리값 = Pamięć_Files.Zapis(열린파일번호, bajt_dane); if (처리값 < 0) { polecenie_interpreter.błąd(처리값); break; } Tablica.직렬쓰기(bajt_dane); }
        Pamięć_Files.Zamknięte(열린파일번호);
    }
}
