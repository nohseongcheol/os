// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 wiersz_polecenia. Cytat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class polecenie_interpreter {
    static int[] wiersz_wejścia = new int[4096], token_WARTOŚĆ = new int[4096], 시작점 = new int[32], długość_WARTOŚĆ = new int[32];
    static int[] Edytowane_Spis_treści = new int[16384], Edytuj_nazwa = new int[63];
    static int token_ILE_LICZB, Edytuj_nazwa_długość, WYNIK;
    static boolean Wstecz_linia;
    static void 원바이트(int WARTOŚĆ) { Tablica.직렬쓰기(WARTOŚĆ); }
    static int odczytaj_wiersz_wejścia() { return edytor_wierszowy.Odczyt(); }
    static boolean 나누기(int Rozmiar) {
        int pozycja = 0, 끝 = 0; token_ILE_LICZB = 0;
        while (pozycja < Rozmiar) {
            while (pozycja < Rozmiar && (wiersz_wejścia[pozycja] == 32 || wiersz_wejścia[pozycja] == 9)) pozycja++;
            if (pozycja == Rozmiar) break;
            if (token_ILE_LICZB == 16) { 단말.Zapis("polecenie analizować_WARTOŚĆ: 인수가 너무 많습니다\n"); return false; }
            시작점[token_ILE_LICZB] = 끝; int Cytat_WARTOŚĆ = 0;
            while (pozycja < Rozmiar) {
                int WARTOŚĆ = wiersz_wejścia[pozycja++];
                if (Cytat_WARTOŚĆ == 0 && (WARTOŚĆ == 32 || WARTOŚĆ == 9)) break;
                if (WARTOŚĆ == Cytat_WARTOŚĆ) { Cytat_WARTOŚĆ = 0; continue; }
                if (Cytat_WARTOŚĆ == 0 && (WARTOŚĆ == 39 || WARTOŚĆ == 34)) { Cytat_WARTOŚĆ = WARTOŚĆ; continue; }
                token_WARTOŚĆ[끝++] = WARTOŚĆ;
            }
            if (Cytat_WARTOŚĆ != 0) { 단말.Zapis("polecenie analizować_WARTOŚĆ: 따옴표가 닫히지 않았습니다\n"); return false; }
            długość_WARTOŚĆ[token_ILE_LICZB] = 끝 - 시작점[token_ILE_LICZB]; token_ILE_LICZB++;
        }
        return true;
    }
    static boolean 같음(int INDEKS, String Word_SMS) {
        if (INDEKS >= token_ILE_LICZB) return false;
        int indeks_pozycji=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int kod_znaku=Word_SMS.charAt(순번);
            if (kod_znaku>=0xd800 && kod_znaku<=0xdbff && 순번+1<Word_SMS.length()) kod_znaku=0x10000+((kod_znaku-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bajt_ILE_LICZB=kod_znaku<128?1:kod_znaku<2048?2:kod_znaku<65536?3:4;
            for (int SEKWENCJA_WARTOŚĆ=bajt_ILE_LICZB-1; SEKWENCJA_WARTOŚĆ>=0; SEKWENCJA_WARTOŚĆ--) {
                int WARTOŚĆ=bajt_ILE_LICZB==1?kod_znaku:SEKWENCJA_WARTOŚĆ==bajt_ILE_LICZB-1?(bajt_ILE_LICZB==2?0xc0:bajt_ILE_LICZB==3?0xe0:0xf0)|(kod_znaku>>(6*SEKWENCJA_WARTOŚĆ)):0x80|((kod_znaku>>(6*SEKWENCJA_WARTOŚĆ))&63);
                if (indeks_pozycji>=długość_WARTOŚĆ[INDEKS] || token_WARTOŚĆ[시작점[INDEKS]+indeks_pozycji++]!=WARTOŚĆ) return false;
            }
        }
        return indeks_pozycji==długość_WARTOŚĆ[INDEKS];
    }
    static int ścieżka_2(int INDEKS) {
        if (INDEKS >= token_ILE_LICZB) return -22;
        int WYNIK = Pamięć_Files.ścieżka_START(długość_WARTOŚĆ[INDEKS]); if (WYNIK < 0) return WYNIK;
        for (int Loop_INDEKS = 0; Loop_INDEKS < długość_WARTOŚĆ[INDEKS]; Loop_INDEKS++) {
            WYNIK = Pamięć_Files.ścieżka_bajt(Loop_INDEKS, token_WARTOŚĆ[시작점[INDEKS] + Loop_INDEKS]); if (WYNIK < 0) return WYNIK;
        }
        return 0;
    }
    static void błąd(int INDEKS) { WYNIK = 1; 단말.Zapis("błąd "); 단말.identyfikator(INDEKS); 단말.문자(10); }
    static void Widok_WARTOŚĆ() {
        if (token_ILE_LICZB != 2) { 단말.Zapis("사용법: cat nazwa_pliku\n"); return; }
        int WYNIK = ścieżka_2(1); if (WYNIK < 0) { błąd(WYNIK); return; }
        int nazwa_pliku = Pamięć_Files.Otwórz(0); if (nazwa_pliku < 0) { błąd(nazwa_pliku); return; }
        while (true) { int WARTOŚĆ = Pamięć_Files.Odczyt(nazwa_pliku); if (WARTOŚĆ == 256) break; if (WARTOŚĆ < 0) { błąd(WARTOŚĆ); break; } 원바이트(WARTOŚĆ); }
        Pamięć_Files.Zamknięte(nazwa_pliku); 단말.문자(10);
    }
    static void Edytuj_WARTOŚĆ() {
        if (token_ILE_LICZB != 2) { 단말.Zapis("사용법: edit nazwa_pliku\n"); return; }
        int WYNIK = ścieżka_2(1); if (WYNIK < 0) { błąd(WYNIK); return; }
        Edytuj_nazwa_długość = długość_WARTOŚĆ[1];
        for (int Loop_INDEKS = 0; Loop_INDEKS < Edytuj_nazwa_długość; Loop_INDEKS++) Edytuj_nazwa[Loop_INDEKS] = token_WARTOŚĆ[시작점[1] + Loop_INDEKS];
        단말.Zapis("EDIT: nazwa_pliku 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Rozmiar = 0;
        while (true) {
            단말.Zapis("edit> "); int wejście_WARTOŚĆ = odczytaj_wiersz_wejścia();
            if (wejście_WARTOŚĆ < 0) { 단말.Zapis("EDIT CANCELLED\n"); return; }
            if (wejście_WARTOŚĆ == 1 && wiersz_wejścia[0] == '.') break;
            if (wejście_WARTOŚĆ + 1 > Edytowane_Spis_treści.length - Rozmiar) { 단말.Zapis("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEKS = 0; Loop_INDEKS < wejście_WARTOŚĆ; Loop_INDEKS++) Edytowane_Spis_treści[Rozmiar++] = wiersz_wejścia[Loop_INDEKS];
            Edytowane_Spis_treści[Rozmiar++] = 10;
        }
        Pamięć_Files.ścieżka_START(Edytuj_nazwa_długość);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Edytuj_nazwa_długość; Loop_INDEKS++) Pamięć_Files.ścieżka_bajt(Loop_INDEKS, Edytuj_nazwa[Loop_INDEKS]);
        int nazwa_pliku = Pamięć_Files.Otwórz(577); if (nazwa_pliku < 0) { błąd(nazwa_pliku); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rozmiar; Loop_INDEKS++) Pamięć_Files.Zapis(nazwa_pliku, Edytowane_Spis_treści[Loop_INDEKS]);
        Pamięć_Files.Zamknięte(nazwa_pliku); 단말.Zapis("SAVED "); 단말.identyfikator(Rozmiar); 단말.Zapis("bajt_WARTOŚĆ(주기억 nazwa_pliku)\n");
    }
    static int wartość_szesnastkowa(int WARTOŚĆ) {
        if (WARTOŚĆ >= '0' && WARTOŚĆ <= '9') return WARTOŚĆ - '0';
        if (WARTOŚĆ >= 'a' && WARTOŚĆ <= 'f') return WARTOŚĆ - 'a' + 10;
        if (WARTOŚĆ >= 'A' && WARTOŚĆ <= 'F') return WARTOŚĆ - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_ILE_LICZB != 2) { 단말.Zapis("사용법: load nazwa_pliku | hex nazwa_pliku\n"); return; }
        int WYNIK = ścieżka_2(1); if (WYNIK < 0) { błąd(WYNIK); return; }
        if (!넣기) {
            int nazwa_pliku = Pamięć_Files.Otwórz(0); if (nazwa_pliku < 0) { błąd(nazwa_pliku); return; }
            단말.Zapis("HEX BEGIN "); 단말.identyfikator(Pamięć_Files.Rozmiar(nazwa_pliku)); 단말.문자(10);
            int wpis_ILE_LICZB = 0;
            while (true) {
                int WARTOŚĆ = Pamięć_Files.Odczyt(nazwa_pliku); if (WARTOŚĆ < 0 || WARTOŚĆ == 256) break;
                단말.문자("0123456789abcdef".charAt(WARTOŚĆ >> 4)); 단말.문자("0123456789abcdef".charAt(WARTOŚĆ & 15));
                if (++wpis_ILE_LICZB % 32 == 0) 단말.문자(10);
            }
            if (wpis_ILE_LICZB % 32 != 0) 단말.문자(10);
            Pamięć_Files.Zamknięte(nazwa_pliku); 단말.Zapis("HEX END\n"); return;
        }
        Edytuj_nazwa_długość = długość_WARTOŚĆ[1];
        for (int Loop_INDEKS = 0; Loop_INDEKS < Edytuj_nazwa_długość; Loop_INDEKS++) Edytuj_nazwa[Loop_INDEKS] = token_WARTOŚĆ[시작점[1] + Loop_INDEKS];
        단말.Zapis("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Rozmiar = 0;
        while (true) {
            단말.Zapis("hex> "); int wejście_WARTOŚĆ = odczytaj_wiersz_wejścia();
            if (wejście_WARTOŚĆ < 0) { 단말.Zapis("LOAD CANCELLED\n"); return; }
            if (wejście_WARTOŚĆ == 1 && wiersz_wejścia[0] == '.') break;
            int przód_WARTOŚĆ = -1;
            for (int Loop_INDEKS = 0; Loop_INDEKS < wejście_WARTOŚĆ; Loop_INDEKS++) {
                if (wiersz_wejścia[Loop_INDEKS] == 32 || wiersz_wejścia[Loop_INDEKS] == 9) continue;
                int WARTOŚĆ = wartość_szesnastkowa(wiersz_wejścia[Loop_INDEKS]);
                if (WARTOŚĆ < 0 || Rozmiar >= Edytowane_Spis_treści.length) { 단말.Zapis("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (przód_WARTOŚĆ < 0) przód_WARTOŚĆ = WARTOŚĆ; else { Edytowane_Spis_treści[Rozmiar++] = przód_WARTOŚĆ * 16 + WARTOŚĆ; przód_WARTOŚĆ = -1; }
            }
            if (przód_WARTOŚĆ >= 0) { 단말.Zapis("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Pamięć_Files.ścieżka_START(Edytuj_nazwa_długość);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Edytuj_nazwa_długość; Loop_INDEKS++) Pamięć_Files.ścieżka_bajt(Loop_INDEKS, Edytuj_nazwa[Loop_INDEKS]);
        int nazwa_pliku = Pamięć_Files.Otwórz(577); if (nazwa_pliku < 0) { błąd(nazwa_pliku); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rozmiar; Loop_INDEKS++) Pamięć_Files.Zapis(nazwa_pliku, Edytowane_Spis_treści[Loop_INDEKS]);
        Pamięć_Files.Zamknięte(nazwa_pliku); 단말.Zapis("LOADED "); 단말.identyfikator(Rozmiar); 단말.Zapis("bajt_WARTOŚĆ(주기억 nazwa_pliku)\n");
    }
    static int narzędzia(int INDEKS) {
        return narzędzie_wpis(INDEKS, 1);
    }
    static int narzędzie_wpis(int INDEKS, int Uruchom_2) {
        if (token_ILE_LICZB - Uruchom_2 > 8) return -22;
        Tablica.인수준비(token_ILE_LICZB - Uruchom_2);
        for (int 첫값 = Uruchom_2; 첫값 < token_ILE_LICZB; 첫값++) {
            if (długość_WARTOŚĆ[첫값] > 255) return -36;
            for (int Loop_INDEKS = 0; Loop_INDEKS < długość_WARTOŚĆ[첫값]; Loop_INDEKS++) Tablica.argument_bajt(첫값 - Uruchom_2, Loop_INDEKS, token_WARTOŚĆ[시작점[첫값] + Loop_INDEKS]);
        }
        return INDEKS == -2 ? Tablica.리눅스파일실행() : INDEKS < 0 ? Tablica.Wykonaj_użytkownik_Plik() : Tablica.przebieg_użytkownik_program(INDEKS);
    }
    static int PYTHON_pakiet() {
        if (token_ILE_LICZB > 8) return -22;
        Tablica.인수준비(token_ILE_LICZB);
        String ścieżka_2 = "/lib/pakiet.py";
        // Java 문자열을 셸의 UTF-8 argumenty 버퍼에 기록한다.
        int indeks_pozycji = 0;
        for (int 순번 = 0; 순번 < ścieżka_2.length(); 순번++) {
            int znak_WARTOŚĆ = ścieżka_2.charAt(순번);
            if (znak_WARTOŚĆ < 128) Tablica.argument_bajt(0, indeks_pozycji++, znak_WARTOŚĆ);
            else { Tablica.argument_bajt(0, indeks_pozycji++, 0xe0 | (znak_WARTOŚĆ >> 12)); Tablica.argument_bajt(0, indeks_pozycji++, 0x80 | ((znak_WARTOŚĆ >> 6) & 63)); Tablica.argument_bajt(0, indeks_pozycji++, 0x80 | (znak_WARTOŚĆ & 63)); }
        }
        for (int 순번 = 1; 순번 < token_ILE_LICZB; 순번++) {
            if (długość_WARTOŚĆ[순번] > 255) return -36;
            for (int znak_WARTOŚĆ = 0; znak_WARTOŚĆ < długość_WARTOŚĆ[순번]; znak_WARTOŚĆ++) Tablica.argument_bajt(순번, znak_WARTOŚĆ, token_WARTOŚĆ[시작점[순번] + znak_WARTOŚĆ]);
        }
        return Tablica.przebieg_użytkownik_program(12);
    }
    static int wykonanie_format() {
        int 처리값 = ścieżka_2(0); if (처리값 < 0) return 처리값;
        int nazwa_pliku = Pamięć_Files.Otwórz(0); if (nazwa_pliku < 0) return nazwa_pliku;
        int 첫값 = Pamięć_Files.Odczyt(nazwa_pliku), bajt_dane = Pamięć_Files.Odczyt(nazwa_pliku), kod_znaku = Pamięć_Files.Odczyt(nazwa_pliku), 뒷값 = Pamięć_Files.Odczyt(nazwa_pliku);
        Pamięć_Files.Zamknięte(nazwa_pliku);
        if (첫값 == 127 && bajt_dane == 'E' && kod_znaku == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bajt_dane == 'K' && kod_znaku == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEKS, String argumenty) {
        Tablica.인수준비(1);
        for (int Loop_INDEKS = 0; Loop_INDEKS < argumenty.length(); Loop_INDEKS++) Tablica.argument_bajt(0, Loop_INDEKS, argumenty.charAt(Loop_INDEKS));
        return Tablica.przebieg_użytkownik_program(INDEKS);
    }
    static void SMS_bajt(int nazwa_pliku, int WARTOŚĆ) { Pamięć_Files.Zapis(nazwa_pliku, WARTOŚĆ); }
    static void statyczny_Plik(String Nazwa, String treść_WARTOŚĆ_cb0f2404) {
        // pakiet 파일명은 ASCII. nazwa_pliku 내용은 UTF-8로 저장한다.
        Pamięć_Files.ścieżka_START(Nazwa.length());
        for (int Loop_INDEKS = 0; Loop_INDEKS < Nazwa.length(); Loop_INDEKS++) Pamięć_Files.ścieżka_bajt(Loop_INDEKS, Nazwa.charAt(Loop_INDEKS));
        int nazwa_pliku = Pamięć_Files.Otwórz(193); if (nazwa_pliku < 0) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < treść_WARTOŚĆ_cb0f2404.length(); Loop_INDEKS++) {
            int kod_znaku = treść_WARTOŚĆ_cb0f2404.charAt(Loop_INDEKS);
            if (kod_znaku >= 0xd800 && kod_znaku <= 0xdbff && Loop_INDEKS + 1 < treść_WARTOŚĆ_cb0f2404.length()) kod_znaku = 0x10000 + ((kod_znaku - 0xd800) << 10) + treść_WARTOŚĆ_cb0f2404.charAt(++Loop_INDEKS) - 0xdc00;
            if (kod_znaku < 128) SMS_bajt(nazwa_pliku, kod_znaku);
            else {
                int identyfikator = kod_znaku < 2048 ? 2 : kod_znaku < 65536 ? 3 : 4;
                SMS_bajt(nazwa_pliku, (identyfikator == 2 ? 0xc0 : identyfikator == 3 ? 0xe0 : 0xf0) | (kod_znaku >> (6 * (identyfikator - 1))));
                for (int wpis_ILE_LICZB = identyfikator - 1; wpis_ILE_LICZB > 0; wpis_ILE_LICZB--) SMS_bajt(nazwa_pliku, 0x80 | ((kod_znaku >> (6 * (wpis_ILE_LICZB - 1))) & 63));
            }
        }
        Pamięć_Files.Zamknięte(nazwa_pliku);
    }
    static void 한글도움말() {
        단말.Zapis("F9 lub Shift+Space przełącza na pisanie po polsku.\n");
        단말.Zapis("  [PL] keyboard; [EN] ASCII\n");
        단말.Zapis("  a → a\n");
        단말.Zapis("  F9: EN ↔ polski | Ctrl+Shift+V: UTF-8\n");
        단말.Zapis("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Zapis("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nazwa) {
        int bajt_ILE_LICZB = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Nazwa.length(); Loop_INDEKS++) { int kod_znaku = Nazwa.charAt(Loop_INDEKS); if (kod_znaku >= 0xd800 && kod_znaku <= 0xdfff) return -22; bajt_ILE_LICZB += kod_znaku < 128 ? 1 : kod_znaku < 2048 ? 2 : 3; }
        int 처리값 = Pamięć_Files.ścieżka_START(bajt_ILE_LICZB); if (처리값 < 0) return 처리값;
        int indeks_pozycji = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Nazwa.length(); Loop_INDEKS++) {
            int kod_znaku = Nazwa.charAt(Loop_INDEKS);
            if (kod_znaku < 128) Pamięć_Files.ścieżka_bajt(indeks_pozycji++, kod_znaku);
            else if (kod_znaku < 2048) { Pamięć_Files.ścieżka_bajt(indeks_pozycji++, 0xc0 | (kod_znaku >> 6)); Pamięć_Files.ścieżka_bajt(indeks_pozycji++, 0x80 | (kod_znaku & 63)); }
            else { Pamięć_Files.ścieżka_bajt(indeks_pozycji++, 0xe0 | (kod_znaku >> 12)); Pamięć_Files.ścieżka_bajt(indeks_pozycji++, 0x80 | ((kod_znaku >> 6) & 63)); Pamięć_Files.ścieżka_bajt(indeks_pozycji++, 0x80 | (kod_znaku & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nazwa) {
        int 처리값 = 예제경로(Nazwa); if (처리값 < 0) return 처리값;
        처리값 = Pamięć_Files.Twórca_Katalog(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nazwa, String dane) {
        int 처리값 = 예제경로(Nazwa); if (처리값 < 0) return 처리값;
        int nazwa_pliku = Pamięć_Files.Otwórz(193); if (nazwa_pliku == -17) return 0; if (nazwa_pliku < 0) return nazwa_pliku;
        for (int Loop_INDEKS = 0; Loop_INDEKS < dane.length(); Loop_INDEKS += 2) {
            처리값 = Pamięć_Files.Zapis(nazwa_pliku, wartość_szesnastkowa(dane.charAt(Loop_INDEKS)) * 16 + wartość_szesnastkowa(dane.charAt(Loop_INDEKS + 1)));
            if (처리값 < 0) { Pamięć_Files.Zamknięte(nazwa_pliku); return 처리값; }
        }
        return Pamięć_Files.Zamknięte(nazwa_pliku);
    }
    static void pokaż_pomoc() {
        System_narzędzie.pokaż_pomoc();
        단말.Zapis("sshd / SSH start|stop|status: SSH :22 (user, 장치별 hasło_WARTOŚĆ)\n");
        단말.Zapis("vncd / zdalny_wyświetlać start|stop|status: VNC :5900 (장치별 hasło_WARTOŚĆ)\n");
        단말.Zapis("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Zapis("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Zapis("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Zapis("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Zapis("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Zapis("모서리 + 왼쪽 버튼 przeciągnąć_WARTOŚĆ: interpretator_poleceń Rozmiar zmienić_WARTOŚĆ; terminal size: kolumna_WARTOŚĆ/WIERSZ_WARTOŚĆ\n");
        단말.Zapis("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Zapis("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Zapis("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Zapis("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Zapis("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Zapis("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Zapis("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Zapis("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Zapis("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Zapis("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Zapis("pip: MicroPython źródło_drzewo instalować_WARTOŚĆ; host --network --pip 필요; /lib는 RAM\n");
        단말.Zapis("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Zapis("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Zapis("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Zapis("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void interpretator_poleceń(boolean 전환여부) {
        if (전환여부 && Tablica.interpretator_poleceń(2) != 0) { Tablica.interpretator_poleceń(0); 단말.Zapis("TERMINAL CLOSED\n"); }
        else if (Tablica.interpretator_poleceń(1) < 0) błąd(-19);
        else 단말.Zapis("TERMINAL READY — polski terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void polecenie() {
        if (token_ILE_LICZB == 0) return;
        if (System_narzędzie.Wykonaj_polecenie()) return;
        if (같음(0,"sshd") || 같음(0,"SSH") || 같음(0,"vncd") || 같음(0,"zdalny_wyświetlać")) {
            int Rodzaj_WARTOŚĆ=같음(0,"vncd")||같음(0,"zdalny_wyświetlać")?1:0;
            int Akcja=같음(1,"start")||같음(1,"Uruchom_2")?1:같음(1,"stop")||같음(1,"Zatrzymaj")?0:2;
            int Stan_WARTOŚĆ=Tablica.obserwowanie(Rodzaj_WARTOŚĆ,Akcja);
            if(Stan_WARTOŚĆ<0)błąd(Stan_WARTOŚĆ);else 단말.Zapis(Tablica.obserwowanie(Rodzaj_WARTOŚĆ,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else pokaż_pomoc(); }
        else if (같음(0, "info") || 같음(0, "i")) jądro.msinfo32_exe();
        else if (같음(0, "pwd")) { Pamięć_Files.bieżący_zapis(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_ILE_LICZB == 1) { Pamięć_Files.ścieżka_START(1); 처리값 = Pamięć_Files.ścieżka_bajt(0, '/'); } else 처리값 = token_ILE_LICZB == 2 ? ścieżka_2(1) : -22;
            if (처리값 >= 0) 처리값 = Pamięć_Files.zmienić_Katalog(); if (처리값 < 0) błąd(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEKS = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_ILE_LICZB == argument_INDEKS) { Pamięć_Files.ścieżka_START(1); 처리값 = Pamięć_Files.ścieżka_bajt(0, '.'); } else 처리값 = token_ILE_LICZB == argument_INDEKS + 1 ? ścieżka_2(argument_INDEKS) : -22;
            if (처리값 >= 0) 처리값 = Pamięć_Files.경로목록(); if (처리값 < 0) błąd(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) powłoka_Narzędzia.Plik_sprawa(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) powłoka_Narzędzia.kopiować_WARTOŚĆ(같음(0, "mv"));
        else if (같음(0, "cat")) powłoka_Narzędzia.Widok_WARTOŚĆ();
        else if (같음(0, "wc")) powłoka_Narzędzia.세기();
        else if (같음(0, "grep")) powłoka_Narzędzia.ZNAJDŹ_wpis();
        else if (같음(0, "head") || 같음(0, "tail")) powłoka_Narzędzia.머리(같음(0, "tail"));
        else if (같음(0, "tee")) powłoka_Narzędzia.zapis_Razem();
        else if (같음(0, "env")) powłoka_składnia.program_środowisko();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_ILE_LICZB == 1) powłoka_składnia.program_środowisko();
            for (int Loop_INDEKS = 1; Loop_INDEKS < token_ILE_LICZB; Loop_INDEKS++) { int 처리값 = powłoka_składnia.środowisko_Ustawienia(Loop_INDEKS, 같음(0, "unset")); if (처리값 != 0) { WYNIK = 처리값; 단말.Zapis("polecenie analizować_WARTOŚĆ: zmienna_WARTOŚĆ 이름이 잘못되었거나 예약된 이름이거나 środowisko 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) powłoka_składnia.Wykonaj_Plik();
        else if (같음(0, "true")) WYNIK = 0;
        else if (같음(0, "false")) WYNIK = 1;
        else if (같음(0, "history")) edytor_wierszowy.program_LOG();
        else if (같음(0, "exit")) {
            if (powłoka_składnia.깊이 > 0) { WYNIK = token_ILE_LICZB == 1 ? powłoka_składnia.Stan_WARTOŚĆ : powłoka_Narzędzia.cyfra_WARTOŚĆ(1); if (WYNIK < 0 || WYNIK > 255) WYNIK = 2; powłoka_składnia.skrypt_Koniec = true; }
            else if (Tablica.interpretator_poleceń(2) != 0) interpretator_poleceń(true);
            else 단말.Zapis("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Edytuj_WARTOŚĆ();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_ILE_LICZB < 2) { WYNIK = 2; 단말.Zapis("사용법: rm nazwa_pliku...\n"); }
            for (int Loop_INDEKS = 1; Loop_INDEKS < token_ILE_LICZB; Loop_INDEKS++) { int 처리값 = ścieżka_2(Loop_INDEKS); if (처리값 == 0) 처리값 = Pamięć_Files.usunąć_wpis(); if (처리값 < 0) błąd(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_stanowisko = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_stanowisko; 첫값 < token_ILE_LICZB; 첫값++) { if (첫값 > START_stanowisko) 단말.문자(32); for (int Loop_INDEKS = 0; Loop_INDEKS < długość_WARTOŚĆ[첫값]; Loop_INDEKS++) Tablica.직렬쓰기(token_WARTOŚĆ[시작점[첫값] + Loop_INDEKS]); }
            if (START_stanowisko == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Zapis("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_pakiet() : narzędzia(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); WYNIK = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !powłoka_składnia.연결중) { 단말.Zapis("exit "); 단말.identyfikator(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = narzędzia(13); WYNIK = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = narzędzia(15); WYNIK = 처리값 < 0 ? 126 : 처리값; if (!powłoka_składnia.연결중) { 단말.Zapis("exit "); 단말.identyfikator(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = narzędzia(16); WYNIK = 처리값 < 0 ? 126 : 처리값; if (!powłoka_składnia.연결중) { 단말.Zapis("exit "); 단말.identyfikator(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Rozmiar = Tablica.interpretator_poleceń(13); 단말.Zapis("TERMINAL SIZE "); 단말.identyfikator(Rozmiar & 65535); 단말.문자('x'); 단말.identyfikator(Rozmiar >>> 16); 단말.문자(10); }
            else interpretator_poleceń(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tablica.interpretator_poleceń(9); Pulpit.Wykonaj_polecenie(); }
        else if (같음(0, "c")) jądro.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) jądro.test_Tasks();
        else if (같음(0, "g")) jądro.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) jądro.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tablica.przebieg_użytkownik_program(0); if (처리값 == 0) 단말.Zapis("ELF DEMO PASS\n"); else błąd(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? narzędzie_wpis(-2, 2) : narzędzia(-1); WYNIK = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !powłoka_składnia.연결중) { 단말.Zapis("exit "); 단말.identyfikator(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) jądro.test_Sieć();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tablica.transfer_plików_usługa(1); if (처리값 < 0) błąd(처리값); else { 단말.Zapis("FTP listening "); System_narzędzie.zapis_ADRES(Tablica.sieć_stan(0,0)); 단말.Zapis(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tablica.transfer_plików_usługa(0); 단말.Zapis("FTP stopped\n"); }
            else 단말.Zapis(Tablica.transfer_plików_usługa(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { pakiet.Przygotuj(); 단말.Zapis("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Język = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_ILE_LICZB != 2 || Język < 0) 단말.Zapis("example java|c|python: pozycja_wyjścia, nazwa_pliku, 네트워크, 그래픽, Java Swing Okno 예제\n");
            else { int 처리값 = 예제꾸러미.instalować_WARTOŚĆ(Język); if (처리값 < 0) { błąd(처리값); if (처리값 == -28) 단말.Zapis("RAM full: remove unused files, then retry example\n"); } else 단말.Zapis("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_WARTOŚĆ = wykonanie_format();
            if (format_WARTOŚĆ == 1 || format_WARTOŚĆ == 2) {
                int 처리값 = narzędzie_wpis(format_WARTOŚĆ == 1 ? -1 : 14, 0); WYNIK = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !powłoka_składnia.연결중) { 단말.Zapis("exit "); 단말.identyfikator(처리값); 단말.문자(10); }
            } else if (format_WARTOŚĆ == 0) { WYNIK = 126; 단말.Zapis("실행할 identyfikator 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { WYNIK = 127; 단말.Zapis("Unknown command. help: commands\n"); }
        }
    }
    public static void Wykonaj_polecenie() {
        pakiet.Przygotuj();
        for (int Język = 0; Język < 3; Język++) { int 처리값 = 예제꾸러미.instalować_WARTOŚĆ(Język); if (처리값 < 0) błąd(처리값); }
        pokaż_pomoc();
        while (true) {
            okno_sesja.Proces_WARTOŚĆ_wpis(); if (okno_sesja.CV_wykonanie()) continue;
            if (!okno_sesja.이어읽기) 단말.Zapis("jkoros-native> "); edytor_wierszowy.wiersz_polecenia = true; Tablica.zdalny_chwileczkę(1); int Rozmiar = odczytaj_wiersz_wejścia(); Tablica.zdalny_chwileczkę(0); edytor_wierszowy.wiersz_polecenia = false;
            if (Rozmiar == -3) continue;
            if (Rozmiar == -2) 단말.Zapis("polecenie analizować_WARTOŚĆ: 명령줄이 너무 깁니다\n");
            if (Rozmiar >= 0) { powłoka_składnia.skrypt_Koniec = false; powłoka_składnia.Wykonaj_polecenie(wiersz_wejścia, 0, Rozmiar, 0); } else powłoka_składnia.Stan_WARTOŚĆ = 130;
            Tablica.Koniec_zdalny_polecenie(powłoka_składnia.Stan_WARTOŚĆ);
            edytor_wierszowy.Rozmiar = edytor_wierszowy.kursor_WARTOŚĆ = edytor_wierszowy.START_okno = 0;
        }
    }
}
