// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 naredbeni_redak. Citat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] red = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], 길이 = new int[32];
    static int[] Uređivano_Sadržaj = new int[16384], Uredi_naziv = new int[63];
    static int token_COUNT, 편집이름길이, REZULTAT;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { pano.직렬쓰기(VALUE); }
    static int 줄읽기() { return uređivač_redaka.Čitaj(); }
    static boolean 나누기(int Veličina) {
        int Položaj = 0, 끝 = 0; token_COUNT = 0;
        while (Položaj < Veličina) {
            while (Položaj < Veličina && (red[Položaj] == 32 || red[Položaj] == 9)) Položaj++;
            if (Položaj == Veličina) break;
            if (token_COUNT == 16) { 단말.Zapisuj("Naredba rastavljati_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Citat_VALUE = 0;
            while (Položaj < Veličina) {
                int VALUE = red[Položaj++];
                if (Citat_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Citat_VALUE) { Citat_VALUE = 0; continue; }
                if (Citat_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Citat_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Citat_VALUE != 0) { 단말.Zapisuj("Naredba rastavljati_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            길이[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int indeks_položaja=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int kodna_točka=Word_SMS.charAt(순번);
            if (kodna_točka>=0xd800 && kodna_točka<=0xdbff && 순번+1<Word_SMS.length()) kodna_točka=0x10000+((kodna_točka-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bajt_COUNT=kodna_točka<128?1:kodna_točka<2048?2:kodna_točka<65536?3:4;
            for (int SEQUENCE_VALUE=bajt_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bajt_COUNT==1?kodna_točka:SEQUENCE_VALUE==bajt_COUNT-1?(bajt_COUNT==2?0xc0:bajt_COUNT==3?0xe0:0xf0)|(kodna_točka>>(6*SEQUENCE_VALUE)):0x80|((kodna_točka>>(6*SEQUENCE_VALUE))&63);
                if (indeks_položaja>=길이[INDEX] || token_VALUE[시작점[INDEX]+indeks_položaja++]!=VALUE) return false;
            }
        }
        return indeks_položaja==길이[INDEX];
    }
    static int PUTANJA(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int REZULTAT = Memorija_Datoteke.put_START(길이[INDEX]); if (REZULTAT < 0) return REZULTAT;
        for (int Loop_INDEX = 0; Loop_INDEX < 길이[INDEX]; Loop_INDEX++) {
            REZULTAT = Memorija_Datoteke.put_bajt(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (REZULTAT < 0) return REZULTAT;
        }
        return 0;
    }
    static void GREŠKA(int INDEX) { REZULTAT = 1; 단말.Zapisuj("GREŠKA "); 단말.수(INDEX); 단말.문자(10); }
    static void Prikaz_VALUE() {
        if (token_COUNT != 2) { 단말.Zapisuj("사용법: cat Datoteka\n"); return; }
        int REZULTAT = PUTANJA(1); if (REZULTAT < 0) { GREŠKA(REZULTAT); return; }
        int Datoteka = Memorija_Datoteke.Otvori(0); if (Datoteka < 0) { GREŠKA(Datoteka); return; }
        while (true) { int VALUE = Memorija_Datoteke.Čitaj(Datoteka); if (VALUE == 256) break; if (VALUE < 0) { GREŠKA(VALUE); break; } 원바이트(VALUE); }
        Memorija_Datoteke.Zatvori(Datoteka); 단말.문자(10);
    }
    static void Uredi_VALUE() {
        if (token_COUNT != 2) { 단말.Zapisuj("사용법: edit Datoteka\n"); return; }
        int REZULTAT = PUTANJA(1); if (REZULTAT < 0) { GREŠKA(REZULTAT); return; }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Uredi_naziv[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Zapisuj("EDIT: Datoteka 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Veličina = 0;
        while (true) {
            단말.Zapisuj("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Zapisuj("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && red[0] == '.') break;
            if (입력 + 1 > Uređivano_Sadržaj.length - Veličina) { 단말.Zapisuj("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Uređivano_Sadržaj[Veličina++] = red[Loop_INDEX];
            Uređivano_Sadržaj[Veličina++] = 10;
        }
        Memorija_Datoteke.put_START(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Memorija_Datoteke.put_bajt(Loop_INDEX, Uredi_naziv[Loop_INDEX]);
        int Datoteka = Memorija_Datoteke.Otvori(577); if (Datoteka < 0) { GREŠKA(Datoteka); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Memorija_Datoteke.Zapisuj(Datoteka, Uređivano_Sadržaj[Loop_INDEX]);
        Memorija_Datoteke.Zatvori(Datoteka); 단말.Zapisuj("SAVED "); 단말.수(Veličina); 단말.Zapisuj("bajt_VALUE(주기억 Datoteka)\n");
    }
    static int heksadekadski_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.Zapisuj("사용법: load Datoteka | hex Datoteka\n"); return; }
        int REZULTAT = PUTANJA(1); if (REZULTAT < 0) { GREŠKA(REZULTAT); return; }
        if (!넣기) {
            int Datoteka = Memorija_Datoteke.Otvori(0); if (Datoteka < 0) { GREŠKA(Datoteka); return; }
            단말.Zapisuj("HEX BEGIN "); 단말.수(Memorija_Datoteke.Veličina(Datoteka)); 단말.문자(10);
            int unos_COUNT = 0;
            while (true) {
                int VALUE = Memorija_Datoteke.Čitaj(Datoteka); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++unos_COUNT % 32 == 0) 단말.문자(10);
            }
            if (unos_COUNT % 32 != 0) 단말.문자(10);
            Memorija_Datoteke.Zatvori(Datoteka); 단말.Zapisuj("HEX END\n"); return;
        }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Uredi_naziv[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Zapisuj("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Veličina = 0;
        while (true) {
            단말.Zapisuj("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Zapisuj("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && red[0] == '.') break;
            int prednja_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (red[Loop_INDEX] == 32 || red[Loop_INDEX] == 9) continue;
                int VALUE = heksadekadski_VALUE(red[Loop_INDEX]);
                if (VALUE < 0 || Veličina >= Uređivano_Sadržaj.length) { 단말.Zapisuj("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (prednja_VALUE < 0) prednja_VALUE = VALUE; else { Uređivano_Sadržaj[Veličina++] = prednja_VALUE * 16 + VALUE; prednja_VALUE = -1; }
            }
            if (prednja_VALUE >= 0) { 단말.Zapisuj("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memorija_Datoteke.put_START(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Memorija_Datoteke.put_bajt(Loop_INDEX, Uredi_naziv[Loop_INDEX]);
        int Datoteka = Memorija_Datoteke.Otvori(577); if (Datoteka < 0) { GREŠKA(Datoteka); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Memorija_Datoteke.Zapisuj(Datoteka, Uređivano_Sadržaj[Loop_INDEX]);
        Memorija_Datoteke.Zatvori(Datoteka); 단말.Zapisuj("LOADED "); 단말.수(Veličina); 단말.Zapisuj("bajt_VALUE(주기억 Datoteka)\n");
    }
    static int Alati(int INDEX) {
        return alat_unos(INDEX, 1);
    }
    static int alat_unos(int INDEX, int Pokreni) {
        if (token_COUNT - Pokreni > 8) return -22;
        pano.인수준비(token_COUNT - Pokreni);
        for (int 첫값 = Pokreni; 첫값 < token_COUNT; 첫값++) {
            if (길이[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) pano.argument_bajt(첫값 - Pokreni, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? pano.리눅스파일실행() : INDEX < 0 ? pano.Izvrši_korisnik_Datoteka() : pano.izvršiti_korisnik_program(INDEX);
    }
    static int PYTHON_komplet() {
        if (token_COUNT > 8) return -22;
        pano.인수준비(token_COUNT);
        String PUTANJA = "/lib/komplet.py";
        // Java 문자열을 셸의 UTF-8 Argumenti 버퍼에 기록한다.
        int indeks_položaja = 0;
        for (int 순번 = 0; 순번 < PUTANJA.length(); 순번++) {
            int znak_VALUE = PUTANJA.charAt(순번);
            if (znak_VALUE < 128) pano.argument_bajt(0, indeks_položaja++, znak_VALUE);
            else { pano.argument_bajt(0, indeks_položaja++, 0xe0 | (znak_VALUE >> 12)); pano.argument_bajt(0, indeks_položaja++, 0x80 | ((znak_VALUE >> 6) & 63)); pano.argument_bajt(0, indeks_položaja++, 0x80 | (znak_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (길이[순번] > 255) return -36;
            for (int znak_VALUE = 0; znak_VALUE < 길이[순번]; znak_VALUE++) pano.argument_bajt(순번, znak_VALUE, token_VALUE[시작점[순번] + znak_VALUE]);
        }
        return pano.izvršiti_korisnik_program(12);
    }
    static int 실행형식() {
        int 처리값 = PUTANJA(0); if (처리값 < 0) return 처리값;
        int Datoteka = Memorija_Datoteke.Otvori(0); if (Datoteka < 0) return Datoteka;
        int 첫값 = Memorija_Datoteke.Čitaj(Datoteka), bajt_podaci = Memorija_Datoteke.Čitaj(Datoteka), kodna_točka = Memorija_Datoteke.Čitaj(Datoteka), 뒷값 = Memorija_Datoteke.Čitaj(Datoteka);
        Memorija_Datoteke.Zatvori(Datoteka);
        if (첫값 == 127 && bajt_podaci == 'E' && kodna_točka == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bajt_podaci == 'K' && kodna_točka == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumenti) {
        pano.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumenti.length(); Loop_INDEX++) pano.argument_bajt(0, Loop_INDEX, Argumenti.charAt(Loop_INDEX));
        return pano.izvršiti_korisnik_program(INDEX);
    }
    static void SMS_bajt(int Datoteka, int VALUE) { Memorija_Datoteke.Zapisuj(Datoteka, VALUE); }
    static void 정적파일(String Ime, String Sadržaj_VALUE) {
        // komplet 파일명은 ASCII. Datoteka 내용은 UTF-8로 저장한다.
        Memorija_Datoteke.put_START(Ime.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Ime.length(); Loop_INDEX++) Memorija_Datoteke.put_bajt(Loop_INDEX, Ime.charAt(Loop_INDEX));
        int Datoteka = Memorija_Datoteke.Otvori(193); if (Datoteka < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Sadržaj_VALUE.length(); Loop_INDEX++) {
            int kodna_točka = Sadržaj_VALUE.charAt(Loop_INDEX);
            if (kodna_točka >= 0xd800 && kodna_točka <= 0xdbff && Loop_INDEX + 1 < Sadržaj_VALUE.length()) kodna_točka = 0x10000 + ((kodna_točka - 0xd800) << 10) + Sadržaj_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (kodna_točka < 128) SMS_bajt(Datoteka, kodna_točka);
            else {
                int 수 = kodna_točka < 2048 ? 2 : kodna_točka < 65536 ? 3 : 4;
                SMS_bajt(Datoteka, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kodna_točka >> (6 * (수 - 1))));
                for (int unos_COUNT = 수 - 1; unos_COUNT > 0; unos_COUNT--) SMS_bajt(Datoteka, 0x80 | ((kodna_točka >> (6 * (unos_COUNT - 1))) & 63));
            }
        }
        Memorija_Datoteke.Zatvori(Datoteka);
    }
    static void 한글도움말() {
        단말.Zapisuj("F9 / Shift+Space: [EN] ↔ [hrvatski]\n");
        단말.Zapisuj("  [HR] keyboard; [EN] ASCII\n");
        단말.Zapisuj("  [ → š\n");
        단말.Zapisuj("  F9: EN ↔ hrvatski | Ctrl+Shift+V: UTF-8\n");
        단말.Zapisuj("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Zapisuj("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Ime) {
        int bajt_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ime.length(); Loop_INDEX++) { int kodna_točka = Ime.charAt(Loop_INDEX); if (kodna_točka >= 0xd800 && kodna_točka <= 0xdfff) return -22; bajt_COUNT += kodna_točka < 128 ? 1 : kodna_točka < 2048 ? 2 : 3; }
        int 처리값 = Memorija_Datoteke.put_START(bajt_COUNT); if (처리값 < 0) return 처리값;
        int indeks_položaja = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ime.length(); Loop_INDEX++) {
            int kodna_točka = Ime.charAt(Loop_INDEX);
            if (kodna_točka < 128) Memorija_Datoteke.put_bajt(indeks_položaja++, kodna_točka);
            else if (kodna_točka < 2048) { Memorija_Datoteke.put_bajt(indeks_položaja++, 0xc0 | (kodna_točka >> 6)); Memorija_Datoteke.put_bajt(indeks_položaja++, 0x80 | (kodna_točka & 63)); }
            else { Memorija_Datoteke.put_bajt(indeks_položaja++, 0xe0 | (kodna_točka >> 12)); Memorija_Datoteke.put_bajt(indeks_položaja++, 0x80 | ((kodna_točka >> 6) & 63)); Memorija_Datoteke.put_bajt(indeks_položaja++, 0x80 | (kodna_točka & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Ime) {
        int 처리값 = 예제경로(Ime); if (처리값 < 0) return 처리값;
        처리값 = Memorija_Datoteke.Create_imenik(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Ime, String podaci) {
        int 처리값 = 예제경로(Ime); if (처리값 < 0) return 처리값;
        int Datoteka = Memorija_Datoteke.Otvori(193); if (Datoteka == -17) return 0; if (Datoteka < 0) return Datoteka;
        for (int Loop_INDEX = 0; Loop_INDEX < podaci.length(); Loop_INDEX += 2) {
            처리값 = Memorija_Datoteke.Zapisuj(Datoteka, heksadekadski_VALUE(podaci.charAt(Loop_INDEX)) * 16 + heksadekadski_VALUE(podaci.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memorija_Datoteke.Zatvori(Datoteka); return 처리값; }
        }
        return Memorija_Datoteke.Zatvori(Datoteka);
    }
    static void emisija_pomoć() {
        sustav_alat.emisija_pomoć();
        단말.Zapisuj("sshd / sigurno_ljuska start|stop|status: SSH :22 (user, 장치별 lozinka_VALUE)\n");
        단말.Zapisuj("vncd / udaljeno_zaslon start|stop|status: VNC :5900 (장치별 lozinka_VALUE)\n");
        단말.Zapisuj("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Zapisuj("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Zapisuj("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Zapisuj("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Zapisuj("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Zapisuj("모서리 + 왼쪽 버튼 vući_VALUE: Terminal Veličina promijeniti_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Zapisuj("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Zapisuj("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Zapisuj("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Zapisuj("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Zapisuj("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Zapisuj("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Zapisuj("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Zapisuj("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Zapisuj("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Zapisuj("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Zapisuj("pip: MicroPython izvor_stablo instaliraj_VALUE; domaćin --network --pip 필요; /lib는 RAM\n");
        단말.Zapisuj("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Zapisuj("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Zapisuj("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Zapisuj("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && pano.Terminal(2) != 0) { pano.Terminal(0); 단말.Zapisuj("TERMINAL CLOSED\n"); }
        else if (pano.Terminal(1) < 0) GREŠKA(-19);
        else 단말.Zapisuj("TERMINAL READY — hrvatski terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Naredba() {
        if (token_COUNT == 0) return;
        if (sustav_alat.Izvrši_naredba()) return;
        if (같음(0,"sshd") || 같음(0,"sigurno_ljuska") || 같음(0,"vncd") || 같음(0,"udaljeno_zaslon")) {
            int 종류=같음(0,"vncd")||같음(0,"udaljeno_zaslon")?1:0;
            int Aktivnost=같음(1,"start")||같음(1,"Pokreni")?1:같음(1,"stop")||같음(1,"Zaustavi")?0:2;
            int Stanje_VALUE=pano.paralelna_sesija(종류,Aktivnost);
            if(Stanje_VALUE<0)GREŠKA(Stanje_VALUE);else 단말.Zapisuj(pano.paralelna_sesija(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else emisija_pomoć(); }
        else if (같음(0, "info") || 같음(0, "i")) jezgra_sustava.Podaci_o_sustavu();
        else if (같음(0, "pwd")) { Memorija_Datoteke.redovno_zapisivanje(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Memorija_Datoteke.put_START(1); 처리값 = Memorija_Datoteke.put_bajt(0, '/'); } else 처리값 = token_COUNT == 2 ? PUTANJA(1) : -22;
            if (처리값 >= 0) 처리값 = Memorija_Datoteke.promijeniti_imenik(); if (처리값 < 0) GREŠKA(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argument_INDEX) { Memorija_Datoteke.put_START(1); 처리값 = Memorija_Datoteke.put_bajt(0, '.'); } else 처리값 = token_COUNT == argument_INDEX + 1 ? PUTANJA(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memorija_Datoteke.경로목록(); if (처리값 < 0) GREŠKA(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) ljuska_Alati.Datoteka_Posao(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) ljuska_Alati.instanca_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) ljuska_Alati.Prikaz_VALUE();
        else if (같음(0, "wc")) ljuska_Alati.세기();
        else if (같음(0, "grep")) ljuska_Alati.FIND_unos();
        else if (같음(0, "head") || 같음(0, "tail")) ljuska_Alati.머리(같음(0, "tail"));
        else if (같음(0, "tee")) ljuska_Alati.zapisivanje_Zajedno();
        else if (같음(0, "env")) ljuska_sintaksa.emisija_okruženje();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) ljuska_sintaksa.emisija_okruženje();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = ljuska_sintaksa.okruženje_Postavke(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { REZULTAT = 처리값; 단말.Zapisuj("Naredba rastavljati_VALUE: varijabla_VALUE 이름이 잘못되었거나 예약된 이름이거나 okruženje 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) ljuska_sintaksa.Izvrši_Datoteka();
        else if (같음(0, "true")) REZULTAT = 0;
        else if (같음(0, "false")) REZULTAT = 1;
        else if (같음(0, "history")) uređivač_redaka.emisija_LOG();
        else if (같음(0, "exit")) {
            if (ljuska_sintaksa.깊이 > 0) { REZULTAT = token_COUNT == 1 ? ljuska_sintaksa.Stanje_VALUE : ljuska_Alati.znamenka_VALUE(1); if (REZULTAT < 0 || REZULTAT > 255) REZULTAT = 2; ljuska_sintaksa.skripta_završiti_razgovor = true; }
            else if (pano.Terminal(2) != 0) Terminal(true);
            else 단말.Zapisuj("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Uredi_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { REZULTAT = 2; 단말.Zapisuj("사용법: rm Datoteka...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = PUTANJA(Loop_INDEX); if (처리값 == 0) 처리값 = Memorija_Datoteke.izbrisati_unos(); if (처리값 < 0) GREŠKA(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_položaj = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_položaj; 첫값 < token_COUNT; 첫값++) { if (첫값 > START_položaj) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) pano.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (START_položaj == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Zapisuj("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_komplet() : Alati(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); REZULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.Zapisuj("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Alati(13); REZULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Alati(15); REZULTAT = 처리값 < 0 ? 126 : 처리값; if (!ljuska_sintaksa.연결중) { 단말.Zapisuj("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Alati(16); REZULTAT = 처리값 < 0 ? 126 : 처리값; if (!ljuska_sintaksa.연결중) { 단말.Zapisuj("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Veličina = pano.Terminal(13); 단말.Zapisuj("TERMINAL SIZE "); 단말.수(Veličina & 65535); 단말.문자('x'); 단말.수(Veličina >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { pano.Terminal(9); stolni.Izvrši_naredba(); }
        else if (같음(0, "c")) jezgra_sustava.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) jezgra_sustava.작업시험();
        else if (같음(0, "g")) jezgra_sustava.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) jezgra_sustava.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = pano.izvršiti_korisnik_program(0); if (처리값 == 0) 단말.Zapisuj("ELF DEMO PASS\n"); else GREŠKA(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? alat_unos(-2, 2) : Alati(-1); REZULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.Zapisuj("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) jezgra_sustava.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = pano.prijenos_datoteka_servis(1); if (처리값 < 0) GREŠKA(처리값); else { 단말.Zapisuj("FTP listening "); sustav_alat.zapisivanje_adresa(pano.mreža_stanje(0,0)); 단말.Zapisuj(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { pano.prijenos_datoteka_servis(0); 단말.Zapisuj("FTP stopped\n"); }
            else 단말.Zapisuj(pano.prijenos_datoteka_servis(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { komplet.Pripremi(); 단말.Zapisuj("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Jezik = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Jezik < 0) 단말.Zapisuj("example java|c|python: Izlaz, Datoteka, 네트워크, 그래픽, Java Swing Prozor 예제\n");
            else { int 처리값 = 예제꾸러미.instaliraj_VALUE(Jezik); if (처리값 < 0) { GREŠKA(처리값); if (처리값 == -28) 단말.Zapisuj("RAM full: remove unused files, then retry example\n"); } else 단말.Zapisuj("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int oblik_VALUE = 실행형식();
            if (oblik_VALUE == 1 || oblik_VALUE == 2) {
                int 처리값 = alat_unos(oblik_VALUE == 1 ? -1 : 14, 0); REZULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.Zapisuj("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (oblik_VALUE == 0) { REZULTAT = 126; 단말.Zapisuj("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { REZULTAT = 127; 단말.Zapisuj("Unknown command. help: commands\n"); }
        }
    }
    public static void Izvrši_naredba() {
        komplet.Pripremi();
        for (int Jezik = 0; Jezik < 3; Jezik++) { int 처리값 = 예제꾸러미.instaliraj_VALUE(Jezik); if (처리값 < 0) GREŠKA(처리값); }
        emisija_pomoć();
        while (true) {
            prozor_sesija.Proces_VALUE_unos(); if (prozor_sesija.재개()) continue;
            if (!prozor_sesija.이어읽기) 단말.Zapisuj("jkoros-native> "); uređivač_redaka.naredbeni_redak = true; pano.udaljeno_čekaj(1); int Veličina = 줄읽기(); pano.udaljeno_čekaj(0); uređivač_redaka.naredbeni_redak = false;
            if (Veličina == -3) continue;
            if (Veličina == -2) 단말.Zapisuj("Naredba rastavljati_VALUE: 명령줄이 너무 깁니다\n");
            if (Veličina >= 0) { ljuska_sintaksa.skripta_završiti_razgovor = false; ljuska_sintaksa.Izvrši_naredba(red, 0, Veličina, 0); } else ljuska_sintaksa.Stanje_VALUE = 130;
            pano.završiti_razgovor_udaljeno_naredba(ljuska_sintaksa.Stanje_VALUE);
            uređivač_redaka.Veličina = uređivač_redaka.kursor_VALUE = uređivač_redaka.START_prozor = 0;
        }
    }
}
