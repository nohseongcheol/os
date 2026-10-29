// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 kommandoline. Sitat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] linje = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], lengd_VALUE = new int[32];
    static int[] Redigert_Innhald = new int[16384], redigere_namn = new int[63];
    static int token_COUNT, redigere_namn_lengd, forretningsmål;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Tavle.직렬쓰기(VALUE); }
    static int 줄읽기() { return line_Redaktør.Les(); }
    static boolean 나누기(int Storleik) {
        int Posisjon = 0, 끝 = 0; token_COUNT = 0;
        while (Posisjon < Storleik) {
            while (Posisjon < Storleik && (linje[Posisjon] == 32 || linje[Posisjon] == 9)) Posisjon++;
            if (Posisjon == Storleik) break;
            if (token_COUNT == 16) { 단말.Skriv("Kommando dele_opp_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Sitat_VALUE = 0;
            while (Posisjon < Storleik) {
                int VALUE = linje[Posisjon++];
                if (Sitat_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Sitat_VALUE) { Sitat_VALUE = 0; continue; }
                if (Sitat_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Sitat_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Sitat_VALUE != 0) { 단말.Skriv("Kommando dele_opp_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            lengd_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int plassere_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int teiknkode=Word_SMS.charAt(순번);
            if (teiknkode>=0xd800 && teiknkode<=0xdbff && 순번+1<Word_SMS.length()) teiknkode=0x10000+((teiknkode-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_COUNT=teiknkode<128?1:teiknkode<2048?2:teiknkode<65536?3:4;
            for (int SEQUENCE_VALUE=byte_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=byte_COUNT==1?teiknkode:SEQUENCE_VALUE==byte_COUNT-1?(byte_COUNT==2?0xc0:byte_COUNT==3?0xe0:0xf0)|(teiknkode>>(6*SEQUENCE_VALUE)):0x80|((teiknkode>>(6*SEQUENCE_VALUE))&63);
                if (plassere_INDEX>=lengd_VALUE[INDEX] || token_VALUE[시작점[INDEX]+plassere_INDEX++]!=VALUE) return false;
            }
        }
        return plassere_INDEX==lengd_VALUE[INDEX];
    }
    static int STIGE(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int forretningsmål = Minne_Filer.bane_START(lengd_VALUE[INDEX]); if (forretningsmål < 0) return forretningsmål;
        for (int Loop_INDEX = 0; Loop_INDEX < lengd_VALUE[INDEX]; Loop_INDEX++) {
            forretningsmål = Minne_Filer.bane_byte(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (forretningsmål < 0) return forretningsmål;
        }
        return 0;
    }
    static void FEIL(int INDEX) { forretningsmål = 1; 단말.Skriv("FEIL "); 단말.수(INDEX); 단말.문자(10); }
    static void vise_VALUE() {
        if (token_COUNT != 2) { 단말.Skriv("사용법: cat Fil\n"); return; }
        int forretningsmål = STIGE(1); if (forretningsmål < 0) { FEIL(forretningsmål); return; }
        int Fil = Minne_Filer.Opna(0); if (Fil < 0) { FEIL(Fil); return; }
        while (true) { int VALUE = Minne_Filer.Les(Fil); if (VALUE == 256) break; if (VALUE < 0) { FEIL(VALUE); break; } 원바이트(VALUE); }
        Minne_Filer.Lukk(Fil); 단말.문자(10);
    }
    static void redigere_VALUE() {
        if (token_COUNT != 2) { 단말.Skriv("사용법: edit Fil\n"); return; }
        int forretningsmål = STIGE(1); if (forretningsmål < 0) { FEIL(forretningsmål); return; }
        redigere_namn_lengd = lengd_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < redigere_namn_lengd; Loop_INDEX++) redigere_namn[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Skriv("EDIT: Fil 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Storleik = 0;
        while (true) {
            단말.Skriv("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Skriv("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && linje[0] == '.') break;
            if (입력 + 1 > Redigert_Innhald.length - Storleik) { 단말.Skriv("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Redigert_Innhald[Storleik++] = linje[Loop_INDEX];
            Redigert_Innhald[Storleik++] = 10;
        }
        Minne_Filer.bane_START(redigere_namn_lengd);
        for (int Loop_INDEX = 0; Loop_INDEX < redigere_namn_lengd; Loop_INDEX++) Minne_Filer.bane_byte(Loop_INDEX, redigere_namn[Loop_INDEX]);
        int Fil = Minne_Filer.Opna(577); if (Fil < 0) { FEIL(Fil); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Storleik; Loop_INDEX++) Minne_Filer.Skriv(Fil, Redigert_Innhald[Loop_INDEX]);
        Minne_Filer.Lukk(Fil); 단말.Skriv("SAVED "); 단말.수(Storleik); 단말.Skriv("byte_VALUE(주기억 Fil)\n");
    }
    static int heks_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.Skriv("사용법: load Fil | hex Fil\n"); return; }
        int forretningsmål = STIGE(1); if (forretningsmål < 0) { FEIL(forretningsmål); return; }
        if (!넣기) {
            int Fil = Minne_Filer.Opna(0); if (Fil < 0) { FEIL(Fil); return; }
            단말.Skriv("HEX BEGIN "); 단말.수(Minne_Filer.Storleik(Fil)); 단말.문자(10);
            int oppføring_COUNT = 0;
            while (true) {
                int VALUE = Minne_Filer.Les(Fil); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++oppføring_COUNT % 32 == 0) 단말.문자(10);
            }
            if (oppføring_COUNT % 32 != 0) 단말.문자(10);
            Minne_Filer.Lukk(Fil); 단말.Skriv("HEX END\n"); return;
        }
        redigere_namn_lengd = lengd_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < redigere_namn_lengd; Loop_INDEX++) redigere_namn[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Skriv("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Storleik = 0;
        while (true) {
            단말.Skriv("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Skriv("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && linje[0] == '.') break;
            int 앞 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (linje[Loop_INDEX] == 32 || linje[Loop_INDEX] == 9) continue;
                int VALUE = heks_VALUE(linje[Loop_INDEX]);
                if (VALUE < 0 || Storleik >= Redigert_Innhald.length) { 단말.Skriv("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = VALUE; else { Redigert_Innhald[Storleik++] = 앞 * 16 + VALUE; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Skriv("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Minne_Filer.bane_START(redigere_namn_lengd);
        for (int Loop_INDEX = 0; Loop_INDEX < redigere_namn_lengd; Loop_INDEX++) Minne_Filer.bane_byte(Loop_INDEX, redigere_namn[Loop_INDEX]);
        int Fil = Minne_Filer.Opna(577); if (Fil < 0) { FEIL(Fil); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Storleik; Loop_INDEX++) Minne_Filer.Skriv(Fil, Redigert_Innhald[Loop_INDEX]);
        Minne_Filer.Lukk(Fil); 단말.Skriv("LOADED "); 단말.수(Storleik); 단말.Skriv("byte_VALUE(주기억 Fil)\n");
    }
    static int Verktøy(int INDEX) {
        return verktøy_oppføring(INDEX, 1);
    }
    static int verktøy_oppføring(int INDEX, int Køyr_2) {
        if (token_COUNT - Køyr_2 > 8) return -22;
        Tavle.인수준비(token_COUNT - Køyr_2);
        for (int 첫값 = Køyr_2; 첫값 < token_COUNT; 첫값++) {
            if (lengd_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < lengd_VALUE[첫값]; Loop_INDEX++) Tavle.argument_byte(첫값 - Køyr_2, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Tavle.리눅스파일실행() : INDEX < 0 ? Tavle.Utfør_brukar_fil() : Tavle.køyre_brukar_app(INDEX);
    }
    static int PYTHON_bunt() {
        if (token_COUNT > 8) return -22;
        Tavle.인수준비(token_COUNT);
        String STIGE = "/lib/bunt.py";
        // Java 문자열을 셸의 UTF-8 Argument 버퍼에 기록한다.
        int plassere_INDEX = 0;
        for (int 순번 = 0; 순번 < STIGE.length(); 순번++) {
            int teikn_VALUE = STIGE.charAt(순번);
            if (teikn_VALUE < 128) Tavle.argument_byte(0, plassere_INDEX++, teikn_VALUE);
            else { Tavle.argument_byte(0, plassere_INDEX++, 0xe0 | (teikn_VALUE >> 12)); Tavle.argument_byte(0, plassere_INDEX++, 0x80 | ((teikn_VALUE >> 6) & 63)); Tavle.argument_byte(0, plassere_INDEX++, 0x80 | (teikn_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (lengd_VALUE[순번] > 255) return -36;
            for (int teikn_VALUE = 0; teikn_VALUE < lengd_VALUE[순번]; teikn_VALUE++) Tavle.argument_byte(순번, teikn_VALUE, token_VALUE[시작점[순번] + teikn_VALUE]);
        }
        return Tavle.køyre_brukar_app(12);
    }
    static int 실행형식() {
        int 처리값 = STIGE(0); if (처리값 < 0) return 처리값;
        int Fil = Minne_Filer.Opna(0); if (Fil < 0) return Fil;
        int 첫값 = Minne_Filer.Les(Fil), byte_data = Minne_Filer.Les(Fil), teiknkode = Minne_Filer.Les(Fil), 뒷값 = Minne_Filer.Les(Fil);
        Minne_Filer.Lukk(Fil);
        if (첫값 == 127 && byte_data == 'E' && teiknkode == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_data == 'K' && teiknkode == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argument) {
        Tavle.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argument.length(); Loop_INDEX++) Tavle.argument_byte(0, Loop_INDEX, Argument.charAt(Loop_INDEX));
        return Tavle.køyre_brukar_app(INDEX);
    }
    static void SMS_byte(int Fil, int VALUE) { Minne_Filer.Skriv(Fil, VALUE); }
    static void statisk_fil(String Namn, String Innhald_VALUE) {
        // bunt 파일명은 ASCII. Fil 내용은 UTF-8로 저장한다.
        Minne_Filer.bane_START(Namn.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Namn.length(); Loop_INDEX++) Minne_Filer.bane_byte(Loop_INDEX, Namn.charAt(Loop_INDEX));
        int Fil = Minne_Filer.Opna(193); if (Fil < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Innhald_VALUE.length(); Loop_INDEX++) {
            int teiknkode = Innhald_VALUE.charAt(Loop_INDEX);
            if (teiknkode >= 0xd800 && teiknkode <= 0xdbff && Loop_INDEX + 1 < Innhald_VALUE.length()) teiknkode = 0x10000 + ((teiknkode - 0xd800) << 10) + Innhald_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (teiknkode < 128) SMS_byte(Fil, teiknkode);
            else {
                int 수 = teiknkode < 2048 ? 2 : teiknkode < 65536 ? 3 : 4;
                SMS_byte(Fil, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (teiknkode >> (6 * (수 - 1))));
                for (int oppføring_COUNT = 수 - 1; oppføring_COUNT > 0; oppføring_COUNT--) SMS_byte(Fil, 0x80 | ((teiknkode >> (6 * (oppføring_COUNT - 1))) & 63));
            }
        }
        Minne_Filer.Lukk(Fil);
    }
    static void 한글도움말() {
        단말.Skriv("F9 / Shift+Space: [EN] ↔ [nn]\n");
        단말.Skriv("  [NN] keyboard; [EN] ASCII\n");
        단말.Skriv("  a → a\n");
        단말.Skriv("  F9: EN ↔ nn | Ctrl+Shift+V: UTF-8\n");
        단말.Skriv("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Skriv("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Namn) {
        int byte_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Namn.length(); Loop_INDEX++) { int teiknkode = Namn.charAt(Loop_INDEX); if (teiknkode >= 0xd800 && teiknkode <= 0xdfff) return -22; byte_COUNT += teiknkode < 128 ? 1 : teiknkode < 2048 ? 2 : 3; }
        int 처리값 = Minne_Filer.bane_START(byte_COUNT); if (처리값 < 0) return 처리값;
        int plassere_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Namn.length(); Loop_INDEX++) {
            int teiknkode = Namn.charAt(Loop_INDEX);
            if (teiknkode < 128) Minne_Filer.bane_byte(plassere_INDEX++, teiknkode);
            else if (teiknkode < 2048) { Minne_Filer.bane_byte(plassere_INDEX++, 0xc0 | (teiknkode >> 6)); Minne_Filer.bane_byte(plassere_INDEX++, 0x80 | (teiknkode & 63)); }
            else { Minne_Filer.bane_byte(plassere_INDEX++, 0xe0 | (teiknkode >> 12)); Minne_Filer.bane_byte(plassere_INDEX++, 0x80 | ((teiknkode >> 6) & 63)); Minne_Filer.bane_byte(plassere_INDEX++, 0x80 | (teiknkode & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Namn) {
        int 처리값 = 예제경로(Namn); if (처리값 < 0) return 처리값;
        처리값 = Minne_Filer.Opprett_katalog(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Namn, String data) {
        int 처리값 = 예제경로(Namn); if (처리값 < 0) return 처리값;
        int Fil = Minne_Filer.Opna(193); if (Fil == -17) return 0; if (Fil < 0) return Fil;
        for (int Loop_INDEX = 0; Loop_INDEX < data.length(); Loop_INDEX += 2) {
            처리값 = Minne_Filer.Skriv(Fil, heks_VALUE(data.charAt(Loop_INDEX)) * 16 + heks_VALUE(data.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Minne_Filer.Lukk(Fil); return 처리값; }
        }
        return Minne_Filer.Lukk(Fil);
    }
    static void vise_hjelp() {
        system_verktøy.vise_hjelp();
        단말.Skriv("sshd / sikker_grensesnitt start|stop|status: SSH :22 (user, 장치별 passord_VALUE)\n");
        단말.Skriv("vncd / fjern_vise start|stop|status: VNC :5900 (장치별 passord_VALUE)\n");
        단말.Skriv("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Skriv("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Skriv("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Skriv("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Skriv("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Skriv("모서리 + 왼쪽 버튼 dra_VALUE: Terminal Storleik endre_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Skriv("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Skriv("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Skriv("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Skriv("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Skriv("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Skriv("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Skriv("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Skriv("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Skriv("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Skriv("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Skriv("pip: MicroPython kjelde_tre installere_VALUE; vert --network --pip 필요; /lib는 RAM\n");
        단말.Skriv("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Skriv("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Skriv("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Skriv("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Tavle.Terminal(2) != 0) { Tavle.Terminal(0); 단말.Skriv("TERMINAL CLOSED\n"); }
        else if (Tavle.Terminal(1) < 0) FEIL(-19);
        else 단말.Skriv("TERMINAL READY — nn terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Kommando() {
        if (token_COUNT == 0) return;
        if (system_verktøy.Utfør_kommando()) return;
        if (같음(0,"sshd") || 같음(0,"sikker_grensesnitt") || 같음(0,"vncd") || 같음(0,"fjern_vise")) {
            int 종류=같음(0,"vncd")||같음(0,"fjern_vise")?1:0;
            int Handling=같음(1,"start")||같음(1,"Køyr_2")?1:같음(1,"stop")||같음(1,"Stopp")?0:2;
            int status_VALUE=Tavle.skygging(종류,Handling);
            if(status_VALUE<0)FEIL(status_VALUE);else 단말.Skriv(Tavle.skygging(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else vise_hjelp(); }
        else if (같음(0, "info") || 같음(0, "i")) kjerne.msinfo32_exe();
        else if (같음(0, "pwd")) { Minne_Filer.betalt_skrive(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Minne_Filer.bane_START(1); 처리값 = Minne_Filer.bane_byte(0, '/'); } else 처리값 = token_COUNT == 2 ? STIGE(1) : -22;
            if (처리값 >= 0) 처리값 = Minne_Filer.endre_katalog(); if (처리값 < 0) FEIL(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argument_INDEX) { Minne_Filer.bane_START(1); 처리값 = Minne_Filer.bane_byte(0, '.'); } else 처리값 = token_COUNT == argument_INDEX + 1 ? STIGE(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Minne_Filer.경로목록(); if (처리값 < 0) FEIL(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) grensesnitt_Verktøy.fil_sak(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) grensesnitt_Verktøy.kopiere_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) grensesnitt_Verktøy.vise_VALUE();
        else if (같음(0, "wc")) grensesnitt_Verktøy.세기();
        else if (같음(0, "grep")) grensesnitt_Verktøy.Søk_oppføring();
        else if (같음(0, "head") || 같음(0, "tail")) grensesnitt_Verktøy.머리(같음(0, "tail"));
        else if (같음(0, "tee")) grensesnitt_Verktøy.함께쓰기();
        else if (같음(0, "env")) grensesnitt_syntaks.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) grensesnitt_syntaks.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = grensesnitt_syntaks.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { forretningsmål = 처리값; 단말.Skriv("Kommando dele_opp_VALUE: variabel_VALUE 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) grensesnitt_syntaks.Utfør_fil();
        else if (같음(0, "true")) forretningsmål = 0;
        else if (같음(0, "false")) forretningsmål = 1;
        else if (같음(0, "history")) line_Redaktør.vise_LOG();
        else if (같음(0, "exit")) {
            if (grensesnitt_syntaks.깊이 > 0) { forretningsmål = token_COUNT == 1 ? grensesnitt_syntaks.status_VALUE : grensesnitt_Verktøy.siffer_VALUE(1); if (forretningsmål < 0 || forretningsmål > 255) forretningsmål = 2; grensesnitt_syntaks.skript_avslutte = true; }
            else if (Tavle.Terminal(2) != 0) Terminal(true);
            else 단말.Skriv("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) redigere_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { forretningsmål = 2; 단말.Skriv("사용법: rm Fil...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = STIGE(Loop_INDEX); if (처리값 == 0) 처리값 = Minne_Filer.지우기(); if (처리값 < 0) FEIL(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_plassere = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_plassere; 첫값 < token_COUNT; 첫값++) { if (첫값 > START_plassere) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < lengd_VALUE[첫값]; Loop_INDEX++) Tavle.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (START_plassere == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Skriv("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_bunt() : Verktøy(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); forretningsmål = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !grensesnitt_syntaks.연결중) { 단말.Skriv("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Verktøy(13); forretningsmål = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Verktøy(15); forretningsmål = 처리값 < 0 ? 126 : 처리값; if (!grensesnitt_syntaks.연결중) { 단말.Skriv("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Verktøy(16); forretningsmål = 처리값 < 0 ? 126 : 처리값; if (!grensesnitt_syntaks.연결중) { 단말.Skriv("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Storleik = Tavle.Terminal(13); 단말.Skriv("TERMINAL SIZE "); 단말.수(Storleik & 65535); 단말.문자('x'); 단말.수(Storleik >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tavle.Terminal(9); stasjonær.Utfør_kommando(); }
        else if (같음(0, "c")) kjerne.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kjerne.작업시험();
        else if (같음(0, "g")) kjerne.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kjerne.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tavle.køyre_brukar_app(0); if (처리값 == 0) 단말.Skriv("ELF DEMO PASS\n"); else FEIL(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? verktøy_oppføring(-2, 2) : Verktøy(-1); forretningsmål = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !grensesnitt_syntaks.연결중) { 단말.Skriv("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kjerne.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tavle.fil_Overfør_teneste(1); if (처리값 < 0) FEIL(처리값); else { 단말.Skriv("FTP listening "); system_verktøy.skrive_ADDRESS(Tavle.Nettverk_merkje(0,0)); 단말.Skriv(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tavle.fil_Overfør_teneste(0); 단말.Skriv("FTP stopped\n"); }
            else 단말.Skriv(Tavle.fil_Overfør_teneste(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { bunt.Klargjer(); 단말.Skriv("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Språk = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Språk < 0) 단말.Skriv("example java|c|python: Utdata, Fil, 네트워크, 그래픽, Java Swing vindauge 예제\n");
            else { int 처리값 = 예제꾸러미.installere_VALUE(Språk); if (처리값 < 0) { FEIL(처리값); if (처리값 == -28) 단말.Skriv("RAM full: remove unused files, then retry example\n"); } else 단말.Skriv("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = verktøy_oppføring(format_VALUE == 1 ? -1 : 14, 0); forretningsmål = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !grensesnitt_syntaks.연결중) { 단말.Skriv("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { forretningsmål = 126; 단말.Skriv("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { forretningsmål = 127; 단말.Skriv("Unknown command. help: commands\n"); }
        }
    }
    public static void Utfør_kommando() {
        bunt.Klargjer();
        for (int Språk = 0; Språk < 3; Språk++) { int 처리값 = 예제꾸러미.installere_VALUE(Språk); if (처리값 < 0) FEIL(처리값); }
        vise_hjelp();
        while (true) {
            vindauge_økt.Prosess_VALUE_oppføring(); if (vindauge_økt.재개()) continue;
            if (!vindauge_økt.이어읽기) 단말.Skriv("jkoros-native> "); line_Redaktør.kommandoline = true; Tavle.fjern_vent(1); int Storleik = 줄읽기(); Tavle.fjern_vent(0); line_Redaktør.kommandoline = false;
            if (Storleik == -3) continue;
            if (Storleik == -2) 단말.Skriv("Kommando dele_opp_VALUE: 명령줄이 너무 깁니다\n");
            if (Storleik >= 0) { grensesnitt_syntaks.skript_avslutte = false; grensesnitt_syntaks.Utfør_kommando(linje, 0, Storleik, 0); } else grensesnitt_syntaks.status_VALUE = 130;
            Tavle.avslutte_fjern_kommando(grensesnitt_syntaks.status_VALUE);
            line_Redaktør.Storleik = line_Redaktør.markør_VALUE = line_Redaktør.START_vindauge = 0;
        }
    }
}
