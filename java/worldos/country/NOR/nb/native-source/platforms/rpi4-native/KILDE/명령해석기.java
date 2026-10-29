// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 kommandolinje. Sitat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Linje = new int[4096], token_VERDI = new int[4096], 시작점 = new int[32], lengde_VERDI = new int[32];
    static int[] Redigert_Innhold = new int[16384], Rediger_navn = new int[63];
    static int token_ANTALL, Rediger_navn_lengde, KR;
    static boolean Forrige_linje;
    static void 원바이트(int VERDI) { Tavle.직렬쓰기(VERDI); }
    static int 줄읽기() { return linje_Redaktør.Les(); }
    static boolean 나누기(int Størrelse) {
        int Posisjon = 0, 끝 = 0; token_ANTALL = 0;
        while (Posisjon < Størrelse) {
            while (Posisjon < Størrelse && (Linje[Posisjon] == 32 || Linje[Posisjon] == 9)) Posisjon++;
            if (Posisjon == Størrelse) break;
            if (token_ANTALL == 16) { 단말.Skriv("Kommando dele_opp_VERDI: 인수가 너무 많습니다\n"); return false; }
            시작점[token_ANTALL] = 끝; int Sitat_VERDI = 0;
            while (Posisjon < Størrelse) {
                int VERDI = Linje[Posisjon++];
                if (Sitat_VERDI == 0 && (VERDI == 32 || VERDI == 9)) break;
                if (VERDI == Sitat_VERDI) { Sitat_VERDI = 0; continue; }
                if (Sitat_VERDI == 0 && (VERDI == 39 || VERDI == 34)) { Sitat_VERDI = VERDI; continue; }
                token_VERDI[끝++] = VERDI;
            }
            if (Sitat_VERDI != 0) { 단말.Skriv("Kommando dele_opp_VERDI: 따옴표가 닫히지 않았습니다\n"); return false; }
            lengde_VERDI[token_ANTALL] = 끝 - 시작점[token_ANTALL]; token_ANTALL++;
        }
        return true;
    }
    static boolean 같음(int INDEKS, String ord_SMS) {
        if (INDEKS >= token_ANTALL) return false;
        int posisjonsindeks=0;
        for (int 순번=0; 순번<ord_SMS.length(); 순번++) {
            int tegnkode=ord_SMS.charAt(순번);
            if (tegnkode>=0xd800 && tegnkode<=0xdbff && 순번+1<ord_SMS.length()) tegnkode=0x10000+((tegnkode-0xd800)<<10)+ord_SMS.charAt(++순번)-0xdc00;
            int byte_ANTALL=tegnkode<128?1:tegnkode<2048?2:tegnkode<65536?3:4;
            for (int SEKVENS_VERDI=byte_ANTALL-1; SEKVENS_VERDI>=0; SEKVENS_VERDI--) {
                int VERDI=byte_ANTALL==1?tegnkode:SEKVENS_VERDI==byte_ANTALL-1?(byte_ANTALL==2?0xc0:byte_ANTALL==3?0xe0:0xf0)|(tegnkode>>(6*SEKVENS_VERDI)):0x80|((tegnkode>>(6*SEKVENS_VERDI))&63);
                if (posisjonsindeks>=lengde_VERDI[INDEKS] || token_VERDI[시작점[INDEKS]+posisjonsindeks++]!=VERDI) return false;
            }
        }
        return posisjonsindeks==lengde_VERDI[INDEKS];
    }
    static int Sti(int INDEKS) {
        if (INDEKS >= token_ANTALL) return -22;
        int KR = Minne_Filer.bane_START(lengde_VERDI[INDEKS]); if (KR < 0) return KR;
        for (int Loop_INDEKS = 0; Loop_INDEKS < lengde_VERDI[INDEKS]; Loop_INDEKS++) {
            KR = Minne_Filer.bane_byte(Loop_INDEKS, token_VERDI[시작점[INDEKS] + Loop_INDEKS]); if (KR < 0) return KR;
        }
        return 0;
    }
    static void feil(int INDEKS) { KR = 1; 단말.Skriv("feil "); 단말.nummer(INDEKS); 단말.문자(10); }
    static void vise_VERDI() {
        if (token_ANTALL != 2) { 단말.Skriv("사용법: cat Fil\n"); return; }
        int KR = Sti(1); if (KR < 0) { feil(KR); return; }
        int Fil = Minne_Filer.Åpne(0); if (Fil < 0) { feil(Fil); return; }
        while (true) { int VERDI = Minne_Filer.Les(Fil); if (VERDI == 256) break; if (VERDI < 0) { feil(VERDI); break; } 원바이트(VERDI); }
        Minne_Filer.Lukk(Fil); 단말.문자(10);
    }
    static void Rediger_VERDI() {
        if (token_ANTALL != 2) { 단말.Skriv("사용법: edit Fil\n"); return; }
        int KR = Sti(1); if (KR < 0) { feil(KR); return; }
        Rediger_navn_lengde = lengde_VERDI[1];
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rediger_navn_lengde; Loop_INDEKS++) Rediger_navn[Loop_INDEKS] = token_VERDI[시작점[1] + Loop_INDEKS];
        단말.Skriv("EDIT: Fil 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Størrelse = 0;
        while (true) {
            단말.Skriv("edit> "); int inndata_VERDI = 줄읽기();
            if (inndata_VERDI < 0) { 단말.Skriv("EDIT CANCELLED\n"); return; }
            if (inndata_VERDI == 1 && Linje[0] == '.') break;
            if (inndata_VERDI + 1 > Redigert_Innhold.length - Størrelse) { 단말.Skriv("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEKS = 0; Loop_INDEKS < inndata_VERDI; Loop_INDEKS++) Redigert_Innhold[Størrelse++] = Linje[Loop_INDEKS];
            Redigert_Innhold[Størrelse++] = 10;
        }
        Minne_Filer.bane_START(Rediger_navn_lengde);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rediger_navn_lengde; Loop_INDEKS++) Minne_Filer.bane_byte(Loop_INDEKS, Rediger_navn[Loop_INDEKS]);
        int Fil = Minne_Filer.Åpne(577); if (Fil < 0) { feil(Fil); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Minne_Filer.Skriv(Fil, Redigert_Innhold[Loop_INDEKS]);
        Minne_Filer.Lukk(Fil); 단말.Skriv("SAVED "); 단말.nummer(Størrelse); 단말.Skriv("byte_VERDI(주기억 Fil)\n");
    }
    static int heks_VERDI(int VERDI) {
        if (VERDI >= '0' && VERDI <= '9') return VERDI - '0';
        if (VERDI >= 'a' && VERDI <= 'f') return VERDI - 'a' + 10;
        if (VERDI >= 'A' && VERDI <= 'F') return VERDI - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_ANTALL != 2) { 단말.Skriv("사용법: load Fil | hex Fil\n"); return; }
        int KR = Sti(1); if (KR < 0) { feil(KR); return; }
        if (!넣기) {
            int Fil = Minne_Filer.Åpne(0); if (Fil < 0) { feil(Fil); return; }
            단말.Skriv("HEX BEGIN "); 단말.nummer(Minne_Filer.Størrelse(Fil)); 단말.문자(10);
            int oppføring_ANTALL = 0;
            while (true) {
                int VERDI = Minne_Filer.Les(Fil); if (VERDI < 0 || VERDI == 256) break;
                단말.문자("0123456789abcdef".charAt(VERDI >> 4)); 단말.문자("0123456789abcdef".charAt(VERDI & 15));
                if (++oppføring_ANTALL % 32 == 0) 단말.문자(10);
            }
            if (oppføring_ANTALL % 32 != 0) 단말.문자(10);
            Minne_Filer.Lukk(Fil); 단말.Skriv("HEX END\n"); return;
        }
        Rediger_navn_lengde = lengde_VERDI[1];
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rediger_navn_lengde; Loop_INDEKS++) Rediger_navn[Loop_INDEKS] = token_VERDI[시작점[1] + Loop_INDEKS];
        단말.Skriv("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Størrelse = 0;
        while (true) {
            단말.Skriv("hex> "); int inndata_VERDI = 줄읽기();
            if (inndata_VERDI < 0) { 단말.Skriv("LOAD CANCELLED\n"); return; }
            if (inndata_VERDI == 1 && Linje[0] == '.') break;
            int frontkamera_VERDI = -1;
            for (int Loop_INDEKS = 0; Loop_INDEKS < inndata_VERDI; Loop_INDEKS++) {
                if (Linje[Loop_INDEKS] == 32 || Linje[Loop_INDEKS] == 9) continue;
                int VERDI = heks_VERDI(Linje[Loop_INDEKS]);
                if (VERDI < 0 || Størrelse >= Redigert_Innhold.length) { 단말.Skriv("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (frontkamera_VERDI < 0) frontkamera_VERDI = VERDI; else { Redigert_Innhold[Størrelse++] = frontkamera_VERDI * 16 + VERDI; frontkamera_VERDI = -1; }
            }
            if (frontkamera_VERDI >= 0) { 단말.Skriv("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Minne_Filer.bane_START(Rediger_navn_lengde);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rediger_navn_lengde; Loop_INDEKS++) Minne_Filer.bane_byte(Loop_INDEKS, Rediger_navn[Loop_INDEKS]);
        int Fil = Minne_Filer.Åpne(577); if (Fil < 0) { feil(Fil); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Minne_Filer.Skriv(Fil, Redigert_Innhold[Loop_INDEKS]);
        Minne_Filer.Lukk(Fil); 단말.Skriv("LOADED "); 단말.nummer(Størrelse); 단말.Skriv("byte_VERDI(주기억 Fil)\n");
    }
    static int Verktøy(int INDEKS) {
        return verktøy_oppføring(INDEKS, 1);
    }
    static int verktøy_oppføring(int INDEKS, int Kjør_2) {
        if (token_ANTALL - Kjør_2 > 8) return -22;
        Tavle.인수준비(token_ANTALL - Kjør_2);
        for (int 첫값 = Kjør_2; 첫값 < token_ANTALL; 첫값++) {
            if (lengde_VERDI[첫값] > 255) return -36;
            for (int Loop_INDEKS = 0; Loop_INDEKS < lengde_VERDI[첫값]; Loop_INDEKS++) Tavle.argument_byte(첫값 - Kjør_2, Loop_INDEKS, token_VERDI[시작점[첫값] + Loop_INDEKS]);
        }
        return INDEKS == -2 ? Tavle.리눅스파일실행() : INDEKS < 0 ? Tavle.Utfør_bruker_Fil() : Tavle.kjøre_bruker_app(INDEKS);
    }
    static int PYTHON_bunt() {
        if (token_ANTALL > 8) return -22;
        Tavle.인수준비(token_ANTALL);
        String Sti = "/lib/bunt.py";
        // Java 문자열을 셸의 UTF-8 Argumenter 버퍼에 기록한다.
        int posisjonsindeks = 0;
        for (int 순번 = 0; 순번 < Sti.length(); 순번++) {
            int tegn_VERDI = Sti.charAt(순번);
            if (tegn_VERDI < 128) Tavle.argument_byte(0, posisjonsindeks++, tegn_VERDI);
            else { Tavle.argument_byte(0, posisjonsindeks++, 0xe0 | (tegn_VERDI >> 12)); Tavle.argument_byte(0, posisjonsindeks++, 0x80 | ((tegn_VERDI >> 6) & 63)); Tavle.argument_byte(0, posisjonsindeks++, 0x80 | (tegn_VERDI & 63)); }
        }
        for (int 순번 = 1; 순번 < token_ANTALL; 순번++) {
            if (lengde_VERDI[순번] > 255) return -36;
            for (int tegn_VERDI = 0; tegn_VERDI < lengde_VERDI[순번]; tegn_VERDI++) Tavle.argument_byte(순번, tegn_VERDI, token_VERDI[시작점[순번] + tegn_VERDI]);
        }
        return Tavle.kjøre_bruker_app(12);
    }
    static int kjøring_format() {
        int 처리값 = Sti(0); if (처리값 < 0) return 처리값;
        int Fil = Minne_Filer.Åpne(0); if (Fil < 0) return Fil;
        int 첫값 = Minne_Filer.Les(Fil), byte_data = Minne_Filer.Les(Fil), tegnkode = Minne_Filer.Les(Fil), 뒷값 = Minne_Filer.Les(Fil);
        Minne_Filer.Lukk(Fil);
        if (첫값 == 127 && byte_data == 'E' && tegnkode == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_data == 'K' && tegnkode == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEKS, String Argumenter) {
        Tavle.인수준비(1);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Argumenter.length(); Loop_INDEKS++) Tavle.argument_byte(0, Loop_INDEKS, Argumenter.charAt(Loop_INDEKS));
        return Tavle.kjøre_bruker_app(INDEKS);
    }
    static void SMS_byte(int Fil, int VERDI) { Minne_Filer.Skriv(Fil, VERDI); }
    static void statisk_Fil(String Navn, String Innhold_VERDI) {
        // bunt 파일명은 ASCII. Fil 내용은 UTF-8로 저장한다.
        Minne_Filer.bane_START(Navn.length());
        for (int Loop_INDEKS = 0; Loop_INDEKS < Navn.length(); Loop_INDEKS++) Minne_Filer.bane_byte(Loop_INDEKS, Navn.charAt(Loop_INDEKS));
        int Fil = Minne_Filer.Åpne(193); if (Fil < 0) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Innhold_VERDI.length(); Loop_INDEKS++) {
            int tegnkode = Innhold_VERDI.charAt(Loop_INDEKS);
            if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && Loop_INDEKS + 1 < Innhold_VERDI.length()) tegnkode = 0x10000 + ((tegnkode - 0xd800) << 10) + Innhold_VERDI.charAt(++Loop_INDEKS) - 0xdc00;
            if (tegnkode < 128) SMS_byte(Fil, tegnkode);
            else {
                int nummer = tegnkode < 2048 ? 2 : tegnkode < 65536 ? 3 : 4;
                SMS_byte(Fil, (nummer == 2 ? 0xc0 : nummer == 3 ? 0xe0 : 0xf0) | (tegnkode >> (6 * (nummer - 1))));
                for (int oppføring_ANTALL = nummer - 1; oppføring_ANTALL > 0; oppføring_ANTALL--) SMS_byte(Fil, 0x80 | ((tegnkode >> (6 * (oppføring_ANTALL - 1))) & 63));
            }
        }
        Minne_Filer.Lukk(Fil);
    }
    static void 한글도움말() {
        단말.Skriv("F9 eller Shift+Space bytter til norsk inntasting.\n");
        단말.Skriv("  [NB] keyboard; [EN] ASCII\n");
        단말.Skriv("  $ → ¤\n");
        단말.Skriv("  F9: EN ↔ nb | Ctrl+Shift+V: UTF-8\n");
        단말.Skriv("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Skriv("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Navn) {
        int byte_ANTALL = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Navn.length(); Loop_INDEKS++) { int tegnkode = Navn.charAt(Loop_INDEKS); if (tegnkode >= 0xd800 && tegnkode <= 0xdfff) return -22; byte_ANTALL += tegnkode < 128 ? 1 : tegnkode < 2048 ? 2 : 3; }
        int 처리값 = Minne_Filer.bane_START(byte_ANTALL); if (처리값 < 0) return 처리값;
        int posisjonsindeks = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Navn.length(); Loop_INDEKS++) {
            int tegnkode = Navn.charAt(Loop_INDEKS);
            if (tegnkode < 128) Minne_Filer.bane_byte(posisjonsindeks++, tegnkode);
            else if (tegnkode < 2048) { Minne_Filer.bane_byte(posisjonsindeks++, 0xc0 | (tegnkode >> 6)); Minne_Filer.bane_byte(posisjonsindeks++, 0x80 | (tegnkode & 63)); }
            else { Minne_Filer.bane_byte(posisjonsindeks++, 0xe0 | (tegnkode >> 12)); Minne_Filer.bane_byte(posisjonsindeks++, 0x80 | ((tegnkode >> 6) & 63)); Minne_Filer.bane_byte(posisjonsindeks++, 0x80 | (tegnkode & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Navn) {
        int 처리값 = 예제경로(Navn); if (처리값 < 0) return 처리값;
        처리값 = Minne_Filer.åpne_katalog(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Navn, String data) {
        int 처리값 = 예제경로(Navn); if (처리값 < 0) return 처리값;
        int Fil = Minne_Filer.Åpne(193); if (Fil == -17) return 0; if (Fil < 0) return Fil;
        for (int Loop_INDEKS = 0; Loop_INDEKS < data.length(); Loop_INDEKS += 2) {
            처리값 = Minne_Filer.Skriv(Fil, heks_VERDI(data.charAt(Loop_INDEKS)) * 16 + heks_VERDI(data.charAt(Loop_INDEKS + 1)));
            if (처리값 < 0) { Minne_Filer.Lukk(Fil); return 처리값; }
        }
        return Minne_Filer.Lukk(Fil);
    }
    static void vise_hjelp() {
        System_verktøy.vise_hjelp();
        단말.Skriv("sshd / sikker_Shell start|stop|status: SSH :22 (user, 장치별 passord_VERDI)\n");
        단말.Skriv("vncd / ekstern_vise start|stop|status: VNC :5900 (장치별 passord_VERDI)\n");
        단말.Skriv("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Skriv("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Skriv("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Skriv("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Skriv("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Skriv("모서리 + 왼쪽 버튼 dra_VERDI: Terminal Størrelse endre_VERDI; terminal size: spalte_VERDI/RAD_VERDI\n");
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
        단말.Skriv("pip: MicroPython kilde_tre installer_VERDI; vert --network --pip 필요; /lib는 RAM\n");
        단말.Skriv("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Skriv("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Skriv("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Skriv("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Tavle.Terminal(2) != 0) { Tavle.Terminal(0); 단말.Skriv("TERMINAL CLOSED\n"); }
        else if (Tavle.Terminal(1) < 0) feil(-19);
        else 단말.Skriv("TERMINAL READY — nb terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Kommando() {
        if (token_ANTALL == 0) return;
        if (System_verktøy.Utfør_kommando()) return;
        if (같음(0,"sshd") || 같음(0,"sikker_Shell") || 같음(0,"vncd") || 같음(0,"ekstern_vise")) {
            int 종류=같음(0,"vncd")||같음(0,"ekstern_vise")?1:0;
            int Handling=같음(1,"start")||같음(1,"Kjør_2")?1:같음(1,"stop")||같음(1,"Stopp")?0:2;
            int status_VERDI=Tavle.skygging(종류,Handling);
            if(status_VERDI<0)feil(status_VERDI);else 단말.Skriv(Tavle.skygging(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else vise_hjelp(); }
        else if (같음(0, "info") || 같음(0, "i")) kjerne.msinfo32_exe();
        else if (같음(0, "pwd")) { Minne_Filer.betalt_skrive(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_ANTALL == 1) { Minne_Filer.bane_START(1); 처리값 = Minne_Filer.bane_byte(0, '/'); } else 처리값 = token_ANTALL == 2 ? Sti(1) : -22;
            if (처리값 >= 0) 처리값 = Minne_Filer.endre_katalog(); if (처리값 < 0) feil(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEKS = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_ANTALL == argument_INDEKS) { Minne_Filer.bane_START(1); 처리값 = Minne_Filer.bane_byte(0, '.'); } else 처리값 = token_ANTALL == argument_INDEKS + 1 ? Sti(argument_INDEKS) : -22;
            if (처리값 >= 0) 처리값 = Minne_Filer.경로목록(); if (처리값 < 0) feil(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) Shell_Verktøy.Fil_sak(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) Shell_Verktøy.kopiere_VERDI(같음(0, "mv"));
        else if (같음(0, "cat")) Shell_Verktøy.vise_VERDI();
        else if (같음(0, "wc")) Shell_Verktøy.세기();
        else if (같음(0, "grep")) Shell_Verktøy.Søk_oppføring();
        else if (같음(0, "head") || 같음(0, "tail")) Shell_Verktøy.머리(같음(0, "tail"));
        else if (같음(0, "tee")) Shell_Verktøy.skrive_Sammen();
        else if (같음(0, "env")) Shell_syntaks.vise_miljø();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_ANTALL == 1) Shell_syntaks.vise_miljø();
            for (int Loop_INDEKS = 1; Loop_INDEKS < token_ANTALL; Loop_INDEKS++) { int 처리값 = Shell_syntaks.miljø_Innstillinger(Loop_INDEKS, 같음(0, "unset")); if (처리값 != 0) { KR = 처리값; 단말.Skriv("Kommando dele_opp_VERDI: variabel_VERDI 이름이 잘못되었거나 예약된 이름이거나 miljø 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) Shell_syntaks.Utfør_Fil();
        else if (같음(0, "true")) KR = 0;
        else if (같음(0, "false")) KR = 1;
        else if (같음(0, "history")) linje_Redaktør.vise_LOG();
        else if (같음(0, "exit")) {
            if (Shell_syntaks.깊이 > 0) { KR = token_ANTALL == 1 ? Shell_syntaks.status_VERDI : Shell_Verktøy.siffer_VERDI(1); if (KR < 0 || KR > 255) KR = 2; Shell_syntaks.skript_avslutte_en_samtale = true; }
            else if (Tavle.Terminal(2) != 0) Terminal(true);
            else 단말.Skriv("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Rediger_VERDI();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_ANTALL < 2) { KR = 2; 단말.Skriv("사용법: rm Fil...\n"); }
            for (int Loop_INDEKS = 1; Loop_INDEKS < token_ANTALL; Loop_INDEKS++) { int 처리값 = Sti(Loop_INDEKS); if (처리값 == 0) 처리값 = Minne_Filer.slette_oppføring(); if (처리값 < 0) feil(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_plassere = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_plassere; 첫값 < token_ANTALL; 첫값++) { if (첫값 > START_plassere) 단말.문자(32); for (int Loop_INDEKS = 0; Loop_INDEKS < lengde_VERDI[첫값]; Loop_INDEKS++) Tavle.직렬쓰기(token_VERDI[시작점[첫값] + Loop_INDEKS]); }
            if (START_plassere == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Skriv("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_bunt() : Verktøy(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !Shell_syntaks.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Verktøy(13); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Verktøy(15); KR = 처리값 < 0 ? 126 : 처리값; if (!Shell_syntaks.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Verktøy(16); KR = 처리값 < 0 ? 126 : 처리값; if (!Shell_syntaks.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Størrelse = Tavle.Terminal(13); 단말.Skriv("TERMINAL SIZE "); 단말.nummer(Størrelse & 65535); 단말.문자('x'); 단말.nummer(Størrelse >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tavle.Terminal(9); stasjonær.Utfør_kommando(); }
        else if (같음(0, "c")) kjerne.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) kjerne.test_Tasks();
        else if (같음(0, "g")) kjerne.skjermbilde();
        else if (같음(0, "selftest") || 같음(0, "u")) kjerne.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tavle.kjøre_bruker_app(0); if (처리값 == 0) 단말.Skriv("ELF DEMO PASS\n"); else feil(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? verktøy_oppføring(-2, 2) : Verktøy(-1); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !Shell_syntaks.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kjerne.test_Nettverk();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tavle.filoverføring_service(1); if (처리값 < 0) feil(처리값); else { 단말.Skriv("FTP listening "); System_verktøy.skrive_e_post(Tavle.nettverk_status(0,0)); 단말.Skriv(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tavle.filoverføring_service(0); 단말.Skriv("FTP stopped\n"); }
            else 단말.Skriv(Tavle.filoverføring_service(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { bunt.Forbered(); 단말.Skriv("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Språk = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_ANTALL != 2 || Språk < 0) 단말.Skriv("example java|c|python: Utgang, Fil, 네트워크, 그래픽, Java Swing Vindu 예제\n");
            else { int 처리값 = 예제꾸러미.installer_VERDI(Språk); if (처리값 < 0) { feil(처리값); if (처리값 == -28) 단말.Skriv("RAM full: remove unused files, then retry example\n"); } else 단말.Skriv("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VERDI = kjøring_format();
            if (format_VERDI == 1 || format_VERDI == 2) {
                int 처리값 = verktøy_oppføring(format_VERDI == 1 ? -1 : 14, 0); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !Shell_syntaks.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); }
            } else if (format_VERDI == 0) { KR = 126; 단말.Skriv("실행할 nummer 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { KR = 127; 단말.Skriv("Unknown command. help: commands\n"); }
        }
    }
    public static void Utfør_kommando() {
        bunt.Forbered();
        for (int Språk = 0; Språk < 3; Språk++) { int 처리값 = 예제꾸러미.installer_VERDI(Språk); if (처리값 < 0) feil(처리값); }
        vise_hjelp();
        while (true) {
            vindu_økt.Prosess_VERDI_oppføring(); if (vindu_økt.CV_kjøring()) continue;
            if (!vindu_økt.이어읽기) 단말.Skriv("jkoros-native> "); linje_Redaktør.kommandolinje = true; Tavle.ekstern_vent(1); int Størrelse = 줄읽기(); Tavle.ekstern_vent(0); linje_Redaktør.kommandolinje = false;
            if (Størrelse == -3) continue;
            if (Størrelse == -2) 단말.Skriv("Kommando dele_opp_VERDI: 명령줄이 너무 깁니다\n");
            if (Størrelse >= 0) { Shell_syntaks.skript_avslutte_en_samtale = false; Shell_syntaks.Utfør_kommando(Linje, 0, Størrelse, 0); } else Shell_syntaks.status_VERDI = 130;
            Tavle.avslutte_en_samtale_ekstern_kommando(Shell_syntaks.status_VERDI);
            linje_Redaktør.Størrelse = linje_Redaktør.markør_VERDI = linje_Redaktør.START_vindu = 0;
        }
    }
}
