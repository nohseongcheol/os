// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bajt_WARTOŚĆ 경계를 지키는 삽입/삭제, 방향키, polecenie LOG_zapis, Tab Wykonane_WARTOŚĆ. */
public final class edytor_wierszowy {
    static boolean wiersz_polecenia;
    static int[] LOG_zapis = new int[16 * 1024], LOG_długość = new int[16], Store_WARTOŚĆ = new int[4096], kandydat = new int[64];
    static int LOG_ILE_LICZB, LOG_zapis_Koniec, Search_WARTOŚĆ, 저장길이, Rozmiar, kursor_WARTOŚĆ, kandydat_ILE_LICZB, kandydat_długość, START_okno;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd SSH zdalny_wyświetlać run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] polecenie_kandydat = new int[128];
    static void Dodaj_polecenie_kandydat(String wpis_Lista, int START_stanowisko, int Koniec_stanowisko, int wejście_długość) {
        int bajt_ILE_LICZB=0;
        for(int indeks_pozycji=START_stanowisko;indeks_pozycji<Koniec_stanowisko;indeks_pozycji++) {
            int kod_znaku=wpis_Lista.charAt(indeks_pozycji);
            if(kod_znaku>=0xd800 && kod_znaku<=0xdbff && indeks_pozycji+1<Koniec_stanowisko)kod_znaku=0x10000+((kod_znaku-0xd800)<<10)+wpis_Lista.charAt(++indeks_pozycji)-0xdc00;
            int identyfikator=kod_znaku<128?1:kod_znaku<2048?2:kod_znaku<65536?3:4;
            if(bajt_ILE_LICZB+identyfikator>62)return;
            for(int SEKWENCJA_WARTOŚĆ=identyfikator-1;SEKWENCJA_WARTOŚĆ>=0;SEKWENCJA_WARTOŚĆ--)polecenie_kandydat[bajt_ILE_LICZB++]=identyfikator==1?kod_znaku:SEKWENCJA_WARTOŚĆ==identyfikator-1?(identyfikator==2?0xc0:identyfikator==3?0xe0:0xf0)|(kod_znaku>>(6*SEKWENCJA_WARTOŚĆ)):0x80|((kod_znaku>>(6*SEKWENCJA_WARTOŚĆ))&63);
        }
        if(bajt_ILE_LICZB<wejście_długość)return;
        for(int indeks_pozycji=0;indeks_pozycji<wejście_długość;indeks_pozycji++)if(polecenie_kandydat[indeks_pozycji]!=polecenie_interpreter.wiersz_wejścia[indeks_pozycji])return;
        kandydat_ILE_LICZB++;kandydat_długość=bajt_ILE_LICZB+1;
        for(int indeks_pozycji=0;indeks_pozycji<bajt_ILE_LICZB;indeks_pozycji++)kandydat[indeks_pozycji]=polecenie_kandydat[indeks_pozycji];kandydat[bajt_ILE_LICZB]=' ';
    }
    static int przód_WARTOŚĆ(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (polecenie_interpreter.wiersz_wejścia[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_WARTOŚĆ(int 읽는자리) { if (읽는자리 < Rozmiar) { 읽는자리++; while (읽는자리 < Rozmiar && (polecenie_interpreter.wiersz_wejścia[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_stanowisko, int cel_WARTOŚĆ_INDEKS) {
        int 글칸수 = 0;
        for (int Loop_INDEKS = START_stanowisko; Loop_INDEKS < cel_WARTOŚĆ_INDEKS; Loop_INDEKS++) { int bajt_dane = polecenie_interpreter.wiersz_wejścia[Loop_INDEKS]; if ((bajt_dane & 192) == 128) continue; 글칸수 += bajt_dane >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Zapis("\r\u001b[2K");
        단말.Zapis(wiersz_polecenia ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 wiersz_wejścia 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int LICZBA_KOLUMN = Tablica.interpretator_poleceń(13) & 65535; return LICZBA_KOLUMN - (wiersz_polecenia ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_WARTOŚĆ < START_okno) START_okno = kursor_WARTOŚĆ;
        while (폭(START_okno, kursor_WARTOŚĆ) > 보이는폭()) START_okno = BACK_WARTOŚĆ(START_okno);
        int Koniec_stanowisko = START_okno;
        while (Koniec_stanowisko < Rozmiar && 폭(START_okno, BACK_WARTOŚĆ(Koniec_stanowisko)) <= 보이는폭()) Koniec_stanowisko = BACK_WARTOŚĆ(Koniec_stanowisko);
        단말.Zapis("\r\u001b["); 단말.identyfikator(wiersz_polecenia ? 16 : 7); 단말.Zapis("G\u001b[K");
        if (START_okno > 0) 단말.문자('<');
        for (int Loop_INDEKS = START_okno; Loop_INDEKS < Koniec_stanowisko; Loop_INDEKS++) Tablica.직렬쓰기(polecenie_interpreter.wiersz_wejścia[Loop_INDEKS]);
        단말.문자(Koniec_stanowisko < Rozmiar ? '>' : ' ');
        단말.Zapis("\u001b["); 단말.identyfikator(폭(kursor_WARTOŚĆ, Koniec_stanowisko) + 1); 단말.문자('D');
        가로보기 = START_okno > 0 || Koniec_stanowisko < Rozmiar || 폭(0, Rozmiar) > 보이는폭();
    }
    static void dołączać_LOG() {
        if (!wiersz_polecenia || Rozmiar == 0 || Rozmiar > 1024) return;
        if (LOG_ILE_LICZB > 0) {
            int 마지막자리 = (LOG_zapis_Koniec + 15) % 16; boolean 같은여부 = LOG_długość[마지막자리] == Rozmiar;
            for (int Loop_INDEKS = 0; 같은여부 && Loop_INDEKS < Rozmiar; Loop_INDEKS++) if (LOG_zapis[마지막자리 * 1024 + Loop_INDEKS] != polecenie_interpreter.wiersz_wejścia[Loop_INDEKS]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_długość[LOG_zapis_Koniec] = Rozmiar; for (int Loop_INDEKS = 0; Loop_INDEKS < Rozmiar; Loop_INDEKS++) LOG_zapis[LOG_zapis_Koniec * 1024 + Loop_INDEKS] = polecenie_interpreter.wiersz_wejścia[Loop_INDEKS];
        LOG_zapis_Koniec = (LOG_zapis_Koniec + 1) % 16; if (LOG_ILE_LICZB < 16) LOG_ILE_LICZB++;
    }
    static void 기록이동(int CZY_RÓWNE_WARTOŚĆ) {
        if (!wiersz_polecenia) return;
        if (Search_WARTOŚĆ == 0 && CZY_RÓWNE_WARTOŚĆ > 0) { 저장길이 = Rozmiar; for (int Loop_INDEKS = 0; Loop_INDEKS < Rozmiar; Loop_INDEKS++) Store_WARTOŚĆ[Loop_INDEKS] = polecenie_interpreter.wiersz_wejścia[Loop_INDEKS]; }
        int Dalej_stanowisko = Search_WARTOŚĆ + CZY_RÓWNE_WARTOŚĆ; if (Dalej_stanowisko < 0 || Dalej_stanowisko > LOG_ILE_LICZB) return; Search_WARTOŚĆ = Dalej_stanowisko;
        if (Search_WARTOŚĆ == 0) { Rozmiar = 저장길이; for (int Loop_INDEKS = 0; Loop_INDEKS < Rozmiar; Loop_INDEKS++) polecenie_interpreter.wiersz_wejścia[Loop_INDEKS] = Store_WARTOŚĆ[Loop_INDEKS]; }
        else { int 보관칸 = (LOG_zapis_Koniec + 16 - Search_WARTOŚĆ) % 16; Rozmiar = LOG_długość[보관칸]; for (int Loop_INDEKS = 0; Loop_INDEKS < Rozmiar; Loop_INDEKS++) polecenie_interpreter.wiersz_wejścia[Loop_INDEKS] = LOG_zapis[보관칸 * 1024 + Loop_INDEKS]; }
        kursor_WARTOŚĆ = Rozmiar; 다시();
    }
    static void program_LOG() {
        for (int wpis_ILE_LICZB = 0; wpis_ILE_LICZB < LOG_ILE_LICZB; wpis_ILE_LICZB++) {
            int 보관칸 = (LOG_zapis_Koniec + 16 - LOG_ILE_LICZB + wpis_ILE_LICZB) % 16; 단말.identyfikator(wpis_ILE_LICZB + 1); 단말.Zapis("  ");
            for (int Loop_INDEKS = 0; Loop_INDEKS < LOG_długość[보관칸]; Loop_INDEKS++) Tablica.직렬쓰기(LOG_zapis[보관칸 * 1024 + Loop_INDEKS]); 단말.문자(10);
        }
    }
    static void Dodaj_kandydat(int[] dane_TABLICA, int START_stanowisko, int wpis_ILE_LICZB, int 접두말, int suma_ILE_LICZB, boolean Katalog_identyfikator) {
        if (wpis_ILE_LICZB < suma_ILE_LICZB || wpis_ILE_LICZB > 62) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < suma_ILE_LICZB; Loop_INDEKS++) if (dane_TABLICA[START_stanowisko + Loop_INDEKS] != polecenie_interpreter.wiersz_wejścia[접두말 + Loop_INDEKS]) return;
        kandydat_ILE_LICZB++; kandydat_długość = wpis_ILE_LICZB + 1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < wpis_ILE_LICZB; Loop_INDEKS++) kandydat[Loop_INDEKS] = dane_TABLICA[START_stanowisko + Loop_INDEKS]; kandydat[wpis_ILE_LICZB] = Katalog_identyfikator ? '/' : ' ';
    }
    static void Wykonane_WARTOŚĆ() {
        if (!wiersz_polecenia || kursor_WARTOŚĆ != Rozmiar) return;
        int 시작점 = Rozmiar; while (시작점 > 0 && polecenie_interpreter.wiersz_wejścia[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEKS = 시작점; Loop_INDEKS < Rozmiar; Loop_INDEKS++) if (polecenie_interpreter.wiersz_wejścia[Loop_INDEKS] == '/' || polecenie_interpreter.wiersz_wejścia[Loop_INDEKS] == '"' || polecenie_interpreter.wiersz_wejścia[Loop_INDEKS] == 39 || polecenie_interpreter.wiersz_wejścia[Loop_INDEKS] == '\\') return;
        kandydat_ILE_LICZB = 0; int wpis_ILE_LICZB = Rozmiar - 시작점;
        if (시작점 == 0) {
            for(int indeks_listy=0;indeks_listy<2;indeks_listy++) {
                String wpis_Lista=indeks_listy==0?명령들:관리명령.Wykonane_Word();
                int 읽는자리=0;
                while(읽는자리<wpis_Lista.length()) {
                    int Koniec_stanowisko=읽는자리;while(Koniec_stanowisko<wpis_Lista.length() && wpis_Lista.charAt(Koniec_stanowisko)!=' ')Koniec_stanowisko++;
                    Dodaj_polecenie_kandydat(wpis_Lista,읽는자리,Koniec_stanowisko,wpis_ILE_LICZB);읽는자리=Koniec_stanowisko+1;
                }
            }
        } else {
            Pamięć_Files.ścieżka_START(1); Pamięć_Files.ścieżka_bajt(0, '.'); Pamięć_Files.normalizować_WARTOŚĆ();
            for (int Loop_INDEKS = 0; Loop_INDEKS < Pamięć_Files.Plik_ILE_LICZB; Loop_INDEKS++) {
                int START_stanowisko = Pamięć_Files.wpis_START(Pamięć_Files.Nazwa, Loop_INDEKS * 64, Pamięć_Files.이름길이[Loop_INDEKS]);
                if (START_stanowisko >= 0) Dodaj_kandydat(Pamięć_Files.Nazwa, Loop_INDEKS * 64 + START_stanowisko, Pamięć_Files.이름길이[Loop_INDEKS] - START_stanowisko, 시작점, wpis_ILE_LICZB, false);
            }
            for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
                int START_stanowisko = Pamięć_Files.wpis_START(Pamięć_Files.Katalog_nazwa, Loop_INDEKS * 64, Pamięć_Files.Katalog_długość[Loop_INDEKS]);
                if (START_stanowisko >= 0) Dodaj_kandydat(Pamięć_Files.Katalog_nazwa, Loop_INDEKS * 64 + START_stanowisko, Pamięć_Files.Katalog_długość[Loop_INDEKS] - START_stanowisko, 시작점, wpis_ILE_LICZB, true);
            }
        }
        if (kandydat_ILE_LICZB != 1) { Tablica.직렬쓰기(7); return; }
        for (int Loop_INDEKS = wpis_ILE_LICZB; Loop_INDEKS < kandydat_długość && Rozmiar < polecenie_interpreter.wiersz_wejścia.length - 1; Loop_INDEKS++) {
            if (kandydat[Loop_INDEKS] == ' ' && Loop_INDEKS != kandydat_długość - 1) polecenie_interpreter.wiersz_wejścia[Rozmiar++] = '\\';
            polecenie_interpreter.wiersz_wejścia[Rozmiar++] = kandydat[Loop_INDEKS];
        }
        kursor_WARTOŚĆ = Rozmiar; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = Tablica.밀리초();
        while (Tablica.밀리초() - 시작점 < 80) { int bajt_dane = Tablica.직렬읽기(); if (bajt_dane >= 0) return bajt_dane; Tablica.Dochód_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int wpis_ILE_LICZB = 0, Koniec_stanowisko = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 12; Loop_INDEKS++) { int bajt_dane = 탈출읽기(); if (bajt_dane < 0) return; if (bajt_dane >= '0' && bajt_dane <= '9') wpis_ILE_LICZB = wpis_ILE_LICZB * 10 + bajt_dane - '0'; else { Koniec_stanowisko = bajt_dane; break; } }
        if (Koniec_stanowisko == 'A') 기록이동(1);
        else if (Koniec_stanowisko == 'B') 기록이동(-1);
        else if (Koniec_stanowisko == 'C') { kursor_WARTOŚĆ = BACK_WARTOŚĆ(kursor_WARTOŚĆ); 다시(); }
        else if (Koniec_stanowisko == 'D') { kursor_WARTOŚĆ = przód_WARTOŚĆ(kursor_WARTOŚĆ); 다시(); }
        else if (Koniec_stanowisko == 'H' || Koniec_stanowisko == '~' && (wpis_ILE_LICZB == 1 || wpis_ILE_LICZB == 7)) { kursor_WARTOŚĆ = 0; 다시(); }
        else if (Koniec_stanowisko == 'F' || Koniec_stanowisko == '~' && (wpis_ILE_LICZB == 4 || wpis_ILE_LICZB == 8)) { kursor_WARTOŚĆ = Rozmiar; 다시(); }
        else if (Koniec_stanowisko == '~' && wpis_ILE_LICZB == 3 && kursor_WARTOŚĆ < Rozmiar) {
            int Dalej_stanowisko = BACK_WARTOŚĆ(kursor_WARTOŚĆ); for (int Loop_INDEKS = Dalej_stanowisko; Loop_INDEKS < Rozmiar; Loop_INDEKS++) polecenie_interpreter.wiersz_wejścia[Loop_INDEKS - Dalej_stanowisko + kursor_WARTOŚĆ] = polecenie_interpreter.wiersz_wejścia[Loop_INDEKS]; Rozmiar -= Dalej_stanowisko - kursor_WARTOŚĆ; 다시();
        }
        else if (Koniec_stanowisko == '~' && (wpis_ILE_LICZB == 5 || wpis_ILE_LICZB == 6)) Tablica.interpretator_poleceń(wpis_ILE_LICZB == 5 ? 5 : 6);
        else if (Koniec_stanowisko == '~' && wpis_ILE_LICZB == 24 && wiersz_polecenia) { polecenie_interpreter.interpretator_poleceń(true); }
    }
    static int Odczyt() {
        if (!okno_sesja.이어읽기) { Rozmiar = kursor_WARTOŚĆ = Search_WARTOŚĆ = START_okno = 0; 가로보기 = false; }
        else { okno_sesja.이어읽기 = false; 다시(); } boolean przepełnienie = false;
        while (true) {
            int bajt_dane = Tablica.직렬읽기(); if (bajt_dane == -4096) return -3;
            if (Tablica.interpretator_poleceń(14) != 0) 다시(); if (bajt_dane < 0) { Tablica.Dochód_CPU(); continue; }
            if (bajt_dane == 10 && polecenie_interpreter.Wstecz_linia) { polecenie_interpreter.Wstecz_linia = false; continue; } polecenie_interpreter.Wstecz_linia = bajt_dane == 13;
            if (bajt_dane == 27) { 탈출(); continue; }
            if (bajt_dane == 3) { 단말.Zapis("^C\n"); return -1; }
            if (bajt_dane == 4 && Rozmiar == 0 && wiersz_polecenia) { if (Tablica.interpretator_poleceń(2) != 0) polecenie_interpreter.interpretator_poleceń(true); return -1; }
            if (bajt_dane == 13 || bajt_dane == 10) { 단말.문자(10); if (!przepełnienie) dołączać_LOG(); return przepełnienie ? -2 : Rozmiar; }
            if (bajt_dane == 9 && wiersz_polecenia) { Wykonane_WARTOŚĆ(); continue; }
            if (bajt_dane == 1 || bajt_dane == 5) { kursor_WARTOŚĆ = bajt_dane == 1 ? 0 : Rozmiar; 다시(); continue; }
            if (bajt_dane == 8 || bajt_dane == 127 || bajt_dane == 21) {
                if (bajt_dane == 21) { for (int Loop_INDEKS = kursor_WARTOŚĆ; Loop_INDEKS < Rozmiar; Loop_INDEKS++) polecenie_interpreter.wiersz_wejścia[Loop_INDEKS - kursor_WARTOŚĆ] = polecenie_interpreter.wiersz_wejścia[Loop_INDEKS]; Rozmiar -= kursor_WARTOŚĆ; kursor_WARTOŚĆ = 0; }
                else if (kursor_WARTOŚĆ > 0) { int 변경전 = przód_WARTOŚĆ(kursor_WARTOŚĆ); for (int Loop_INDEKS = kursor_WARTOŚĆ; Loop_INDEKS < Rozmiar; Loop_INDEKS++) polecenie_interpreter.wiersz_wejścia[Loop_INDEKS - kursor_WARTOŚĆ + 변경전] = polecenie_interpreter.wiersz_wejścia[Loop_INDEKS]; Rozmiar -= kursor_WARTOŚĆ - 변경전; kursor_WARTOŚĆ = 변경전; }
                다시(); continue;
            }
            if (bajt_dane == 11) { Rozmiar = kursor_WARTOŚĆ; 다시(); continue; }
            if (bajt_dane < 32 && bajt_dane != 9) continue;
            if (Rozmiar == polecenie_interpreter.wiersz_wejścia.length) { przepełnienie = true; continue; }
            for (int Loop_INDEKS = Rozmiar; Loop_INDEKS > kursor_WARTOŚĆ; Loop_INDEKS--) polecenie_interpreter.wiersz_wejścia[Loop_INDEKS] = polecenie_interpreter.wiersz_wejścia[Loop_INDEKS - 1];
            polecenie_interpreter.wiersz_wejścia[kursor_WARTOŚĆ++] = bajt_dane; Rozmiar++;
            if (kursor_WARTOŚĆ == Rozmiar && !가로보기 && 폭(0, Rozmiar) <= 보이는폭()) Tablica.직렬쓰기(bajt_dane);
            else if (kursor_WARTOŚĆ == Rozmiar) 보이는줄(); else 다시();
        }
    }
}
