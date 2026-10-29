// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interakcyjny powłoka 문법. 파이프는 순차 Wykonaj_polecenie, 환경은 같은 셸에서 공유한다. */
public final class powłoka_składnia {
    static int[] plik_źródłowy = new int[4 * 4096], Rodzaj_WARTOŚĆ = new int[4 * 128], Uruchom_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] zmienna_nazwa = new int[16 * 32], zmienna_dane = new int[16 * 256], 이름길이 = new int[16], WARTOŚĆ_długość = new int[16];
    static int[] skrypt_WARTOŚĆ = new int[4 * 16384];
    static int Stan_WARTOŚĆ, 깊이, 쓴수;
    static boolean 연결중, skrypt_Koniec, rozszerzenie_błąd;
    static boolean nazwa_znak(int kod_znaku) { return kod_znaku >= 'a' && kod_znaku <= 'z' || kod_znaku >= 'A' && kod_znaku <= 'Z' || kod_znaku == '_' || kod_znaku >= 128; }
    static boolean 이름뒤(int kod_znaku) { return nazwa_znak(kod_znaku) || kod_znaku >= '0' && kod_znaku <= '9'; }
    static void błąd(String tekst) { Tablica.입출력전환(0); 단말.Zapis("polecenie analizować_WARTOŚĆ: "); 단말.Zapis(tekst); 단말.문자(10); Stan_WARTOŚĆ = 2; }
    static int Odczyt(int wpis_ILE_LICZB, int 중첩깊이) {
        int bieżący_INDEKS = 0, suma_ILE_LICZB = 0, baza_stanowisko = 중첩깊이 * 4096, znak_specjalny = 중첩깊이 * 128;
        while (bieżący_INDEKS < wpis_ILE_LICZB) {
            while (bieżący_INDEKS < wpis_ILE_LICZB && (plik_źródłowy[baza_stanowisko + bieżący_INDEKS] == 32 || plik_źródłowy[baza_stanowisko + bieżący_INDEKS] == 9)) bieżący_INDEKS++;
            if (bieżący_INDEKS == wpis_ILE_LICZB || plik_źródłowy[baza_stanowisko + bieżący_INDEKS] == '#') break;
            if (suma_ILE_LICZB == 128) { błąd("낱말이 너무 많습니다"); return -1; }
            int START_stanowisko = bieżący_INDEKS, kod_znaku = plik_źródłowy[baza_stanowisko + bieżący_INDEKS], dane_Rodzaj = 0;
            if (kod_znaku == ';') { dane_Rodzaj = 1; bieżący_INDEKS++; }
            else if (kod_znaku == '&') { if (bieżący_INDEKS + 1 >= wpis_ILE_LICZB || plik_źródłowy[baza_stanowisko + bieżący_INDEKS + 1] != '&') { błąd("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } dane_Rodzaj = 2; bieżący_INDEKS += 2; }
            else if (kod_znaku == '|') { bieżący_INDEKS++; dane_Rodzaj = bieżący_INDEKS < wpis_ILE_LICZB && plik_źródłowy[baza_stanowisko + bieżący_INDEKS] == '|' ? 3 : 4; if (dane_Rodzaj == 3) bieżący_INDEKS++; }
            else if (kod_znaku == '>') { bieżący_INDEKS++; dane_Rodzaj = bieżący_INDEKS < wpis_ILE_LICZB && plik_źródłowy[baza_stanowisko + bieżący_INDEKS] == '>' ? 6 : 5; if (dane_Rodzaj == 6) bieżący_INDEKS++; }
            else if (kod_znaku == '<') { dane_Rodzaj = 7; bieżący_INDEKS++; }
            else {
                int Cytat = 0;
                while (bieżący_INDEKS < wpis_ILE_LICZB) {
                    kod_znaku = plik_źródłowy[baza_stanowisko + bieżący_INDEKS];
                    if (kod_znaku == '`' && Cytat != 39 || kod_znaku == '$' && Cytat != 39 && bieżący_INDEKS + 1 < wpis_ILE_LICZB && plik_źródłowy[baza_stanowisko + bieżący_INDEKS + 1] == '(') { błąd("polecenie WYNIK 치환은 지원하지 않습니다"); return -1; }
                    if (kod_znaku == '\\' && Cytat != 39) { if (++bieżący_INDEKS == wpis_ILE_LICZB) { błąd("wiersz_wejścia 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } bieżący_INDEKS++; continue; }
                    if (kod_znaku == Cytat) { Cytat = 0; bieżący_INDEKS++; continue; }
                    if (Cytat == 0 && (kod_znaku == 39 || kod_znaku == 34)) { Cytat = kod_znaku; bieżący_INDEKS++; continue; }
                    if (Cytat == 0 && (kod_znaku == 32 || kod_znaku == 9 || kod_znaku == ';' || kod_znaku == '&' || kod_znaku == '|' || kod_znaku == '<' || kod_znaku == '>')) break;
                    bieżący_INDEKS++;
                }
                if (Cytat != 0) { błąd("따옴표가 닫히지 않았습니다"); return -1; }
                if (bieżący_INDEKS < wpis_ILE_LICZB && (plik_źródłowy[baza_stanowisko + bieżący_INDEKS] == '>' || plik_źródłowy[baza_stanowisko + bieżący_INDEKS] == '<')) {
                    boolean 수치 = bieżący_INDEKS > START_stanowisko;
                    for (int Loop_INDEKS = START_stanowisko; Loop_INDEKS < bieżący_INDEKS; Loop_INDEKS++) if (plik_źródłowy[baza_stanowisko + Loop_INDEKS] < '0' || plik_źródłowy[baza_stanowisko + Loop_INDEKS] > '9') 수치 = false;
                    if (수치) { błąd("번호를 지정한 nazwa_pliku deskryptor_wpis We_Wy 전환은 지원하지 않습니다"); return -1; }
                }
            }
            Rodzaj_WARTOŚĆ[znak_specjalny + suma_ILE_LICZB] = dane_Rodzaj; Uruchom_2[znak_specjalny + suma_ILE_LICZB] = START_stanowisko; 끝[znak_specjalny + suma_ILE_LICZB] = bieżący_INDEKS; suma_ILE_LICZB++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEKS = 0; Loop_INDEKS < suma_ILE_LICZB; Loop_INDEKS++) {
            int 임시값 = Rodzaj_WARTOŚĆ[znak_specjalny + Loop_INDEKS];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEKS == suma_ILE_LICZB || Rodzaj_WARTOŚĆ[znak_specjalny + Loop_INDEKS] != 0) { błąd("We_Wy 전환에 nazwa_pliku 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEKS == suma_ILE_LICZB - 1 && 임시값 != 1) { błąd("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (suma_ILE_LICZB > 0 && !낱말 && Rodzaj_WARTOŚĆ[znak_specjalny + suma_ILE_LICZB - 1] != 1) { błąd("명령이 빠졌습니다"); return -1; }
        return suma_ILE_LICZB;
    }
    static boolean zakres_SMS(int[] dane_TABLICA, int lokalny_START, int wpis_ILE_LICZB, String znak_stanowisko) {
        if (wpis_ILE_LICZB != znak_stanowisko.length()) return false; for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) if (dane_TABLICA[lokalny_START + Loop_INDEKS] != znak_stanowisko.charAt(Loop_INDEKS)) return false; return true;
    }
    static void 넣기(int bajt_dane) {
        if (쓴수 >= polecenie_interpreter.token_WARTOŚĆ.length) { if (!rozszerzenie_błąd) błąd("변수를 펼친 명령이 너무 깁니다"); rozszerzenie_błąd = true; return; }
        polecenie_interpreter.token_WARTOŚĆ[쓴수++] = bajt_dane;
    }
    static void zmienna_WARTOŚĆ(int[] dane_TABLICA, int START_stanowisko, int wpis_ILE_LICZB) {
        if (zakres_SMS(dane_TABLICA, START_stanowisko, wpis_ILE_LICZB, "PWD")) { 넣기('/'); for (int Loop_INDEKS = 0; Loop_INDEKS < Pamięć_Files.bieżący_długość; Loop_INDEKS++) 넣기(Pamięć_Files.bieżący_towar[Loop_INDEKS]); return; }
        if (zakres_SMS(dane_TABLICA, START_stanowisko, wpis_ILE_LICZB, "HOME")) { 넣기('/'); return; }
        if (zakres_SMS(dane_TABLICA, START_stanowisko, wpis_ILE_LICZB, "?")) {
            int dane_WARTOŚĆ = Stan_WARTOŚĆ, cyfra = 100; boolean 시작여부 = false;
            while (cyfra > 0) { int 뒷값 = dane_WARTOŚĆ / cyfra; if (뒷값 != 0 || 시작여부 || cyfra == 1) { 넣기('0' + 뒷값); 시작여부 = true; } dane_WARTOŚĆ %= cyfra; cyfra /= 10; } return;
        }
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (이름길이[Loop_INDEKS] == wpis_ILE_LICZB) {
            boolean set = true; for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < wpis_ILE_LICZB; wewnętrzne_stanowisko++) if (zmienna_nazwa[Loop_INDEKS * 32 + wewnętrzne_stanowisko] != dane_TABLICA[START_stanowisko + wewnętrzne_stanowisko]) set = false;
            if (set) { for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < WARTOŚĆ_długość[Loop_INDEKS]; wewnętrzne_stanowisko++) 넣기(zmienna_dane[Loop_INDEKS * 256 + wewnętrzne_stanowisko]); return; }
        }
    }
    static boolean Word_WARTOŚĆ(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Uruchom_2[중첩깊이 * 128 + 낱말번호], Koniec_stanowisko = 끝[중첩깊이 * 128 + 낱말번호], baza_stanowisko = 중첩깊이 * 4096, Cytat = 0;
        if (읽는자리 < Koniec_stanowisko && plik_źródłowy[baza_stanowisko + 읽는자리] == '~' && (읽는자리 + 1 == Koniec_stanowisko || plik_źródłowy[baza_stanowisko + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < Koniec_stanowisko) {
            int kod_znaku = plik_źródłowy[baza_stanowisko + 읽는자리++];
            if (kod_znaku == Cytat) { Cytat = 0; continue; }
            if (Cytat == 0 && (kod_znaku == 39 || kod_znaku == 34)) { Cytat = kod_znaku; continue; }
            if (kod_znaku == '\\' && Cytat != 39) { int Dalej_stanowisko = plik_źródłowy[baza_stanowisko + 읽는자리++]; if (Cytat == 34 && Dalej_stanowisko != '$' && Dalej_stanowisko != '"' && Dalej_stanowisko != '\\') 넣기('\\'); 넣기(Dalej_stanowisko); continue; }
            if (kod_znaku == '$' && Cytat != 39 && 읽는자리 < Koniec_stanowisko) {
                boolean 중괄호자리 = plik_źródłowy[baza_stanowisko + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < Koniec_stanowisko && plik_źródłowy[baza_stanowisko + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < Koniec_stanowisko && 이름뒤(plik_źródłowy[baza_stanowisko + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == Koniec_stanowisko || plik_źródłowy[baza_stanowisko + 읽는자리] != '}')) { błąd("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                zmienna_WARTOŚĆ(plik_źródłowy, baza_stanowisko + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kod_znaku);
        }
        return !rozszerzenie_błąd;
    }
    static int środowisko_Ustawienia(int argument_INDEKS, boolean usuń) {
        int lokalny_START = polecenie_interpreter.시작점[argument_INDEKS], Koniec_stanowisko = lokalny_START + polecenie_interpreter.długość_WARTOŚĆ[argument_INDEKS], 같음자리 = lokalny_START;
        while (같음자리 < Koniec_stanowisko && polecenie_interpreter.token_WARTOŚĆ[같음자리] != '=') 같음자리++;
        int wpis_ILE_LICZB = 같음자리 - lokalny_START;
        if (wpis_ILE_LICZB < 1 || wpis_ILE_LICZB > 31 || !nazwa_znak(polecenie_interpreter.token_WARTOŚĆ[lokalny_START]) || !usuń && 같음자리 == Koniec_stanowisko || Koniec_stanowisko - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEKS = lokalny_START; Loop_INDEKS < 같음자리; Loop_INDEKS++) if (!이름뒤(polecenie_interpreter.token_WARTOŚĆ[Loop_INDEKS])) return 2;
        if (zakres_SMS(polecenie_interpreter.token_WARTOŚĆ, lokalny_START, wpis_ILE_LICZB, "PWD") || zakres_SMS(polecenie_interpreter.token_WARTOŚĆ, lokalny_START, wpis_ILE_LICZB, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
            if (이름길이[Loop_INDEKS] == 0) 빈여부 = Loop_INDEKS;
            if (이름길이[Loop_INDEKS] != wpis_ILE_LICZB) continue;
            boolean set = true; for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < wpis_ILE_LICZB; wewnętrzne_stanowisko++) if (zmienna_nazwa[Loop_INDEKS * 32 + wewnętrzne_stanowisko] != polecenie_interpreter.token_WARTOŚĆ[lokalny_START + wewnętrzne_stanowisko]) set = false;
            if (set) 찾은여부 = Loop_INDEKS;
        }
        if (usuń) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = wpis_ILE_LICZB; WARTOŚĆ_długość[찾은여부] = Koniec_stanowisko - 같음자리 - 1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) zmienna_nazwa[찾은여부 * 32 + Loop_INDEKS] = polecenie_interpreter.token_WARTOŚĆ[lokalny_START + Loop_INDEKS];
        for (int Loop_INDEKS = 같음자리 + 1; Loop_INDEKS < Koniec_stanowisko; Loop_INDEKS++) zmienna_dane[찾은여부 * 256 + Loop_INDEKS - 같음자리 - 1] = polecenie_interpreter.token_WARTOŚĆ[Loop_INDEKS];
        return 0;
    }
    static void program_środowisko() {
        단말.Zapis("HOME=/\nPWD="); Pamięć_Files.bieżący_zapis(); 단말.문자(10);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (이름길이[Loop_INDEKS] > 0) {
            for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < 이름길이[Loop_INDEKS]; wewnętrzne_stanowisko++) Tablica.직렬쓰기(zmienna_nazwa[Loop_INDEKS * 32 + wewnętrzne_stanowisko]); 단말.문자('=');
            for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < WARTOŚĆ_długość[Loop_INDEKS]; wewnętrzne_stanowisko++) Tablica.직렬쓰기(zmienna_dane[Loop_INDEKS * 256 + wewnętrzne_stanowisko]); 단말.문자(10);
        }
    }
    static void Wykonaj_polecenie(int[] dane_TABLICA, int 시작변위, int wpis_ILE_LICZB, int 중첩깊이) {
        if (중첩깊이 >= 4 || wpis_ILE_LICZB > 4096) { błąd("polecenie 파일의 zagnieżdżenie_WARTOŚĆ 또는 wiersz_wejścia długość_WARTOŚĆ 제한을 넘었습니다"); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) plik_źródłowy[중첩깊이 * 4096 + Loop_INDEKS] = dane_TABLICA[시작변위 + Loop_INDEKS];
        int suma_ILE_LICZB = Odczyt(wpis_ILE_LICZB, 중첩깊이); if (suma_ILE_LICZB < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < suma_ILE_LICZB) {
            int grupa_Koniec = 읽는자리;
            while (grupa_Koniec < suma_ILE_LICZB && (Rodzaj_WARTOŚĆ[중첩깊이 * 128 + grupa_Koniec] == 0 || Rodzaj_WARTOŚĆ[중첩깊이 * 128 + grupa_Koniec] >= 4)) grupa_Koniec++;
            boolean Wykonaj = 조건성립 == 1 || 조건성립 == 2 && Stan_WARTOŚĆ == 0 || 조건성립 == 3 && Stan_WARTOŚĆ != 0;
            if (Wykonaj) {
                boolean Wstecz_towar_INDEKS = false;
                while (읽는자리 < grupa_Koniec) {
                    int Dalej_stanowisko = 읽는자리; while (Dalej_stanowisko < grupa_Koniec && Rodzaj_WARTOŚĆ[중첩깊이 * 128 + Dalej_stanowisko] != 4) Dalej_stanowisko++;
                    boolean POŁĄCZ_Stream = Dalej_stanowisko < grupa_Koniec; int wejście_strona = -1, produkt_wyjściowy_strona = -1, 출력방식 = 0;
                    polecenie_interpreter.token_ILE_LICZB = 0; 쓴수 = 0; rozszerzenie_błąd = false;
                    for (int Loop_INDEKS = 읽는자리; Loop_INDEKS < Dalej_stanowisko; Loop_INDEKS++) {
                        int dane_Rodzaj = Rodzaj_WARTOŚĆ[중첩깊이 * 128 + Loop_INDEKS];
                        if (dane_Rodzaj >= 5) { if (dane_Rodzaj == 7) { if (wejście_strona >= 0) { błąd("wejście_WARTOŚĆ 전환이 겹쳤습니다"); return; } wejście_strona = ++Loop_INDEKS; } else { if (produkt_wyjściowy_strona >= 0) { błąd("pozycja_wyjścia 전환이 겹쳤습니다"); return; } produkt_wyjściowy_strona = ++Loop_INDEKS; 출력방식 = dane_Rodzaj; } continue; }
                        if (polecenie_interpreter.token_ILE_LICZB == 32) { błąd("인수가 너무 많습니다"); return; }
                        int argument_INDEKS = polecenie_interpreter.token_ILE_LICZB++; polecenie_interpreter.시작점[argument_INDEKS] = 쓴수;
                        if (!Word_WARTOŚĆ(Loop_INDEKS, 중첩깊이)) return;
                        polecenie_interpreter.długość_WARTOŚĆ[argument_INDEKS] = 쓴수 - polecenie_interpreter.시작점[argument_INDEKS];
                    }
                    연결중 = Wstecz_towar_INDEKS || POŁĄCZ_Stream || wejście_strona >= 0 || produkt_wyjściowy_strona >= 0;
                    if (연결중 && (polecenie_interpreter.같음(0, "vi") || polecenie_interpreter.같음(0, "edit") || polecenie_interpreter.같음(0, "load") || polecenie_interpreter.같음(0, "gui") || polecenie_interpreter.같음(0, "terminal") || polecenie_interpreter.같음(0, "sh") || polecenie_interpreter.같음(0, "source"))) { błąd("interakcyjny 명령과 polecenie 파일은 We_Wy 전환이나 Stream_WARTOŚĆ 연결에 쓸 identyfikator 없습니다"); return; }
                    셸입출력.Uruchom_2(Wstecz_towar_INDEKS, POŁĄCZ_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int wpis_stanowisko = 입출력바꿈 == 0 ? wejście_strona : produkt_wyjściowy_strona; if (wpis_stanowisko < 0) continue;
                        int START_stanowisko = 쓴수; if (!Word_WARTOŚĆ(wpis_stanowisko, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Pamięć_Files.ścieżka_START(쓴수 - START_stanowisko);
                        for (int wewnętrzne_stanowisko = START_stanowisko; 처리값 >= 0 && wewnętrzne_stanowisko < 쓴수; wewnętrzne_stanowisko++) 처리값 = Pamięć_Files.ścieżka_bajt(wewnętrzne_stanowisko - START_stanowisko, polecenie_interpreter.token_WARTOŚĆ[wewnętrzne_stanowisko]);
                        if (처리값 >= 0) 처리값 = Pamięć_Files.Otwórz(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); polecenie_interpreter.błąd(처리값); Stan_WARTOŚĆ = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.plik_wejściowy = 처리값; else 셸입출력.plik_wyjściowy = 처리값;
                    }
                    셸입출력.Zezwalaj_interakcyjny = 중첩깊이 == 0 && 읽는자리 == 0 && Dalej_stanowisko == suma_ILE_LICZB;
                    깊이 = 중첩깊이; polecenie_interpreter.WYNIK = 0; Tablica.입출력전환(1);
                    polecenie_interpreter.polecenie();
                    Tablica.interpretator_poleceń(3);
                    int 반환값 = polecenie_interpreter.WYNIK, Stream_błąd = 셸입출력.awaria_WARTOŚĆ;
                    셸입출력.끝(); 연결중 = false;
                    Stan_WARTOŚĆ = Stream_błąd < 0 ? 1 : 반환값;
                    if (Stream_błąd < 0) { polecenie_interpreter.błąd(Stream_błąd); return; }
                    if (skrypt_Koniec || 반환값 == -1005) return;
                    Wstecz_towar_INDEKS = true; 읽는자리 = Dalej_stanowisko + 1;
                }
            }
            if (grupa_Koniec < suma_ILE_LICZB) 조건성립 = Rodzaj_WARTOŚĆ[중첩깊이 * 128 + grupa_Koniec];
            읽는자리 = grupa_Koniec + 1;
        }
    }
    static void Wykonaj_Plik() {
        if (polecenie_interpreter.token_ILE_LICZB != 2 || 깊이 >= 3) { polecenie_interpreter.WYNIK = 2; 단말.Zapis("사용법: sh nazwa_pliku (zagnieżdżenie_WARTOŚĆ 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = polecenie_interpreter.ścieżka_2(1); if (처리값 >= 0) 처리값 = Pamięć_Files.Otwórz(0);
        if (처리값 < 0) { polecenie_interpreter.błąd(처리값); return; }
        int wpis_ILE_LICZB = 0, bajt_dane;
        while ((bajt_dane = Pamięć_Files.Odczyt(처리값)) != 256 && bajt_dane >= 0 && wpis_ILE_LICZB < 16384) skrypt_WARTOŚĆ[중첩깊이 * 16384 + wpis_ILE_LICZB++] = bajt_dane;
        Pamięć_Files.Zamknięte(처리값); Tablica.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < wpis_ILE_LICZB && !skrypt_Koniec;) {
            int Koniec_stanowisko = 읽는자리; while (Koniec_stanowisko < wpis_ILE_LICZB && skrypt_WARTOŚĆ[중첩깊이 * 16384 + Koniec_stanowisko] != 10) Koniec_stanowisko++;
            int prawidłowy_długość = Koniec_stanowisko - 읽는자리; if (prawidłowy_długość > 0 && skrypt_WARTOŚĆ[중첩깊이 * 16384 + Koniec_stanowisko - 1] == 13) prawidłowy_długość--;
            Wykonaj_polecenie(skrypt_WARTOŚĆ, 중첩깊이 * 16384 + 읽는자리, prawidłowy_długość, 중첩깊이); 읽는자리 = Koniec_stanowisko + 1;
        }
        polecenie_interpreter.WYNIK = Stan_WARTOŚĆ; skrypt_Koniec = false; 깊이 = 중첩깊이 - 1;
    }
}
