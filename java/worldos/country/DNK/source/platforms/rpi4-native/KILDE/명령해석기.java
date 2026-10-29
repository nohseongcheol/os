// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 kommandolinje. Citat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Linje = new int[4096], token_VÆRDI = new int[4096], 시작점 = new int[32], varighed_VÆRDI = new int[32];
    static int[] Redigeret_Indhold = new int[16384], Rediger_navn = new int[63];
    static int token_TÆL, Rediger_navn_varighed, KR;
    static boolean Forrige_linje;
    static void 원바이트(int VÆRDI) { Tavle.직렬쓰기(VÆRDI); }
    static int 줄읽기() { return linjeeditor.Læse(); }
    static boolean 나누기(int Størrelse) {
        int Placering = 0, 끝 = 0; token_TÆL = 0;
        while (Placering < Størrelse) {
            while (Placering < Størrelse && (Linje[Placering] == 32 || Linje[Placering] == 9)) Placering++;
            if (Placering == Størrelse) break;
            if (token_TÆL == 16) { 단말.Skrive("Kommando opdele_tekst_VÆRDI: 인수가 너무 많습니다\n"); return false; }
            시작점[token_TÆL] = 끝; int Citat_VÆRDI = 0;
            while (Placering < Størrelse) {
                int VÆRDI = Linje[Placering++];
                if (Citat_VÆRDI == 0 && (VÆRDI == 32 || VÆRDI == 9)) break;
                if (VÆRDI == Citat_VÆRDI) { Citat_VÆRDI = 0; continue; }
                if (Citat_VÆRDI == 0 && (VÆRDI == 39 || VÆRDI == 34)) { Citat_VÆRDI = VÆRDI; continue; }
                token_VÆRDI[끝++] = VÆRDI;
            }
            if (Citat_VÆRDI != 0) { 단말.Skrive("Kommando opdele_tekst_VÆRDI: 따옴표가 닫히지 않았습니다\n"); return false; }
            varighed_VÆRDI[token_TÆL] = 끝 - 시작점[token_TÆL]; token_TÆL++;
        }
        return true;
    }
    static boolean 같음(int INDEKS, String Ord_sms) {
        if (INDEKS >= token_TÆL) return false;
        int positionsindeks=0;
        for (int 순번=0; 순번<Ord_sms.length(); 순번++) {
            int tegnkode=Ord_sms.charAt(순번);
            if (tegnkode>=0xd800 && tegnkode<=0xdbff && 순번+1<Ord_sms.length()) tegnkode=0x10000+((tegnkode-0xd800)<<10)+Ord_sms.charAt(++순번)-0xdc00;
            int byte_TÆL=tegnkode<128?1:tegnkode<2048?2:tegnkode<65536?3:4;
            for (int SEKVENS_VÆRDI=byte_TÆL-1; SEKVENS_VÆRDI>=0; SEKVENS_VÆRDI--) {
                int VÆRDI=byte_TÆL==1?tegnkode:SEKVENS_VÆRDI==byte_TÆL-1?(byte_TÆL==2?0xc0:byte_TÆL==3?0xe0:0xf0)|(tegnkode>>(6*SEKVENS_VÆRDI)):0x80|((tegnkode>>(6*SEKVENS_VÆRDI))&63);
                if (positionsindeks>=varighed_VÆRDI[INDEKS] || token_VÆRDI[시작점[INDEKS]+positionsindeks++]!=VÆRDI) return false;
            }
        }
        return positionsindeks==varighed_VÆRDI[INDEKS];
    }
    static int Sti(int INDEKS) {
        if (INDEKS >= token_TÆL) return -22;
        int KR = Hukommelse_Filer.sti_START(varighed_VÆRDI[INDEKS]); if (KR < 0) return KR;
        for (int Loop_INDEKS = 0; Loop_INDEKS < varighed_VÆRDI[INDEKS]; Loop_INDEKS++) {
            KR = Hukommelse_Filer.sti_byte(Loop_INDEKS, token_VÆRDI[시작점[INDEKS] + Loop_INDEKS]); if (KR < 0) return KR;
        }
        return 0;
    }
    static void fejl(int INDEKS) { KR = 1; 단말.Skrive("fejl "); 단말.tal(INDEKS); 단말.문자(10); }
    static void Visning_VÆRDI() {
        if (token_TÆL != 2) { 단말.Skrive("사용법: cat Fil\n"); return; }
        int KR = Sti(1); if (KR < 0) { fejl(KR); return; }
        int Fil = Hukommelse_Filer.Åbn(0); if (Fil < 0) { fejl(Fil); return; }
        while (true) { int VÆRDI = Hukommelse_Filer.Læse(Fil); if (VÆRDI == 256) break; if (VÆRDI < 0) { fejl(VÆRDI); break; } 원바이트(VÆRDI); }
        Hukommelse_Filer.Luk(Fil); 단말.문자(10);
    }
    static void Rediger_VÆRDI() {
        if (token_TÆL != 2) { 단말.Skrive("사용법: edit Fil\n"); return; }
        int KR = Sti(1); if (KR < 0) { fejl(KR); return; }
        Rediger_navn_varighed = varighed_VÆRDI[1];
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rediger_navn_varighed; Loop_INDEKS++) Rediger_navn[Loop_INDEKS] = token_VÆRDI[시작점[1] + Loop_INDEKS];
        단말.Skrive("EDIT: Fil 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Størrelse = 0;
        while (true) {
            단말.Skrive("edit> "); int input_VÆRDI = 줄읽기();
            if (input_VÆRDI < 0) { 단말.Skrive("EDIT CANCELLED\n"); return; }
            if (input_VÆRDI == 1 && Linje[0] == '.') break;
            if (input_VÆRDI + 1 > Redigeret_Indhold.length - Størrelse) { 단말.Skrive("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEKS = 0; Loop_INDEKS < input_VÆRDI; Loop_INDEKS++) Redigeret_Indhold[Størrelse++] = Linje[Loop_INDEKS];
            Redigeret_Indhold[Størrelse++] = 10;
        }
        Hukommelse_Filer.sti_START(Rediger_navn_varighed);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rediger_navn_varighed; Loop_INDEKS++) Hukommelse_Filer.sti_byte(Loop_INDEKS, Rediger_navn[Loop_INDEKS]);
        int Fil = Hukommelse_Filer.Åbn(577); if (Fil < 0) { fejl(Fil); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Hukommelse_Filer.Skrive(Fil, Redigeret_Indhold[Loop_INDEKS]);
        Hukommelse_Filer.Luk(Fil); 단말.Skrive("SAVED "); 단말.tal(Størrelse); 단말.Skrive("byte_VÆRDI(주기억 Fil)\n");
    }
    static int hexadecimal_VÆRDI(int VÆRDI) {
        if (VÆRDI >= '0' && VÆRDI <= '9') return VÆRDI - '0';
        if (VÆRDI >= 'a' && VÆRDI <= 'f') return VÆRDI - 'a' + 10;
        if (VÆRDI >= 'A' && VÆRDI <= 'F') return VÆRDI - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_TÆL != 2) { 단말.Skrive("사용법: load Fil | hex Fil\n"); return; }
        int KR = Sti(1); if (KR < 0) { fejl(KR); return; }
        if (!넣기) {
            int Fil = Hukommelse_Filer.Åbn(0); if (Fil < 0) { fejl(Fil); return; }
            단말.Skrive("HEX BEGIN "); 단말.tal(Hukommelse_Filer.Størrelse(Fil)); 단말.문자(10);
            int post_TÆL_8f7753a1 = 0;
            while (true) {
                int VÆRDI = Hukommelse_Filer.Læse(Fil); if (VÆRDI < 0 || VÆRDI == 256) break;
                단말.문자("0123456789abcdef".charAt(VÆRDI >> 4)); 단말.문자("0123456789abcdef".charAt(VÆRDI & 15));
                if (++post_TÆL_8f7753a1 % 32 == 0) 단말.문자(10);
            }
            if (post_TÆL_8f7753a1 % 32 != 0) 단말.문자(10);
            Hukommelse_Filer.Luk(Fil); 단말.Skrive("HEX END\n"); return;
        }
        Rediger_navn_varighed = varighed_VÆRDI[1];
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rediger_navn_varighed; Loop_INDEKS++) Rediger_navn[Loop_INDEKS] = token_VÆRDI[시작점[1] + Loop_INDEKS];
        단말.Skrive("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Størrelse = 0;
        while (true) {
            단말.Skrive("hex> "); int input_VÆRDI = 줄읽기();
            if (input_VÆRDI < 0) { 단말.Skrive("LOAD CANCELLED\n"); return; }
            if (input_VÆRDI == 1 && Linje[0] == '.') break;
            int frontvendt_VÆRDI = -1;
            for (int Loop_INDEKS = 0; Loop_INDEKS < input_VÆRDI; Loop_INDEKS++) {
                if (Linje[Loop_INDEKS] == 32 || Linje[Loop_INDEKS] == 9) continue;
                int VÆRDI = hexadecimal_VÆRDI(Linje[Loop_INDEKS]);
                if (VÆRDI < 0 || Størrelse >= Redigeret_Indhold.length) { 단말.Skrive("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (frontvendt_VÆRDI < 0) frontvendt_VÆRDI = VÆRDI; else { Redigeret_Indhold[Størrelse++] = frontvendt_VÆRDI * 16 + VÆRDI; frontvendt_VÆRDI = -1; }
            }
            if (frontvendt_VÆRDI >= 0) { 단말.Skrive("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Hukommelse_Filer.sti_START(Rediger_navn_varighed);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Rediger_navn_varighed; Loop_INDEKS++) Hukommelse_Filer.sti_byte(Loop_INDEKS, Rediger_navn[Loop_INDEKS]);
        int Fil = Hukommelse_Filer.Åbn(577); if (Fil < 0) { fejl(Fil); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Hukommelse_Filer.Skrive(Fil, Redigeret_Indhold[Loop_INDEKS]);
        Hukommelse_Filer.Luk(Fil); 단말.Skrive("LOADED "); 단말.tal(Størrelse); 단말.Skrive("byte_VÆRDI(주기억 Fil)\n");
    }
    static int Værktøjer(int INDEKS) {
        return værktøj_post(INDEKS, 1);
    }
    static int værktøj_post(int INDEKS, int Kør_2) {
        if (token_TÆL - Kør_2 > 8) return -22;
        Tavle.인수준비(token_TÆL - Kør_2);
        for (int 첫값 = Kør_2; 첫값 < token_TÆL; 첫값++) {
            if (varighed_VÆRDI[첫값] > 255) return -36;
            for (int Loop_INDEKS = 0; Loop_INDEKS < varighed_VÆRDI[첫값]; Loop_INDEKS++) Tavle.argument_byte(첫값 - Kør_2, Loop_INDEKS, token_VÆRDI[시작점[첫값] + Loop_INDEKS]);
        }
        return INDEKS == -2 ? Tavle.리눅스파일실행() : INDEKS < 0 ? Tavle.Udfør_bruger_fil() : Tavle.køre_bruger_app(INDEKS);
    }
    static int PYTHON_bundt() {
        if (token_TÆL > 8) return -22;
        Tavle.인수준비(token_TÆL);
        String Sti = "/lib/bundt.py";
        // Java 문자열을 셸의 UTF-8 Argumenter 버퍼에 기록한다.
        int positionsindeks = 0;
        for (int 순번 = 0; 순번 < Sti.length(); 순번++) {
            int tegn_VÆRDI = Sti.charAt(순번);
            if (tegn_VÆRDI < 128) Tavle.argument_byte(0, positionsindeks++, tegn_VÆRDI);
            else { Tavle.argument_byte(0, positionsindeks++, 0xe0 | (tegn_VÆRDI >> 12)); Tavle.argument_byte(0, positionsindeks++, 0x80 | ((tegn_VÆRDI >> 6) & 63)); Tavle.argument_byte(0, positionsindeks++, 0x80 | (tegn_VÆRDI & 63)); }
        }
        for (int 순번 = 1; 순번 < token_TÆL; 순번++) {
            if (varighed_VÆRDI[순번] > 255) return -36;
            for (int tegn_VÆRDI = 0; tegn_VÆRDI < varighed_VÆRDI[순번]; tegn_VÆRDI++) Tavle.argument_byte(순번, tegn_VÆRDI, token_VÆRDI[시작점[순번] + tegn_VÆRDI]);
        }
        return Tavle.køre_bruger_app(12);
    }
    static int udførelse_format() {
        int 처리값 = Sti(0); if (처리값 < 0) return 처리값;
        int Fil = Hukommelse_Filer.Åbn(0); if (Fil < 0) return Fil;
        int 첫값 = Hukommelse_Filer.Læse(Fil), byte_data = Hukommelse_Filer.Læse(Fil), tegnkode = Hukommelse_Filer.Læse(Fil), 뒷값 = Hukommelse_Filer.Læse(Fil);
        Hukommelse_Filer.Luk(Fil);
        if (첫값 == 127 && byte_data == 'E' && tegnkode == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_data == 'K' && tegnkode == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEKS, String Argumenter) {
        Tavle.인수준비(1);
        for (int Loop_INDEKS = 0; Loop_INDEKS < Argumenter.length(); Loop_INDEKS++) Tavle.argument_byte(0, Loop_INDEKS, Argumenter.charAt(Loop_INDEKS));
        return Tavle.køre_bruger_app(INDEKS);
    }
    static void sms_byte(int Fil, int VÆRDI) { Hukommelse_Filer.Skrive(Fil, VÆRDI); }
    static void statisk_fil(String Navn, String Indhold_VÆRDI) {
        // bundt 파일명은 ASCII. Fil 내용은 UTF-8로 저장한다.
        Hukommelse_Filer.sti_START(Navn.length());
        for (int Loop_INDEKS = 0; Loop_INDEKS < Navn.length(); Loop_INDEKS++) Hukommelse_Filer.sti_byte(Loop_INDEKS, Navn.charAt(Loop_INDEKS));
        int Fil = Hukommelse_Filer.Åbn(193); if (Fil < 0) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Indhold_VÆRDI.length(); Loop_INDEKS++) {
            int tegnkode = Indhold_VÆRDI.charAt(Loop_INDEKS);
            if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && Loop_INDEKS + 1 < Indhold_VÆRDI.length()) tegnkode = 0x10000 + ((tegnkode - 0xd800) << 10) + Indhold_VÆRDI.charAt(++Loop_INDEKS) - 0xdc00;
            if (tegnkode < 128) sms_byte(Fil, tegnkode);
            else {
                int tal = tegnkode < 2048 ? 2 : tegnkode < 65536 ? 3 : 4;
                sms_byte(Fil, (tal == 2 ? 0xc0 : tal == 3 ? 0xe0 : 0xf0) | (tegnkode >> (6 * (tal - 1))));
                for (int post_TÆL_8f7753a1 = tal - 1; post_TÆL_8f7753a1 > 0; post_TÆL_8f7753a1--) sms_byte(Fil, 0x80 | ((tegnkode >> (6 * (post_TÆL_8f7753a1 - 1))) & 63));
            }
        }
        Hukommelse_Filer.Luk(Fil);
    }
    static void 한글도움말() {
        단말.Skrive("F9 eller Shift+Space skifter til dansk indtastning.\n");
        단말.Skrive("  [DA] keyboard; [EN] ASCII\n");
        단말.Skrive("  $ → ¤\n");
        단말.Skrive("  F9: EN ↔ Dansk | Ctrl+Shift+V: UTF-8\n");
        단말.Skrive("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Skrive("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Navn) {
        int byte_TÆL = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Navn.length(); Loop_INDEKS++) { int tegnkode = Navn.charAt(Loop_INDEKS); if (tegnkode >= 0xd800 && tegnkode <= 0xdfff) return -22; byte_TÆL += tegnkode < 128 ? 1 : tegnkode < 2048 ? 2 : 3; }
        int 처리값 = Hukommelse_Filer.sti_START(byte_TÆL); if (처리값 < 0) return 처리값;
        int positionsindeks = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Navn.length(); Loop_INDEKS++) {
            int tegnkode = Navn.charAt(Loop_INDEKS);
            if (tegnkode < 128) Hukommelse_Filer.sti_byte(positionsindeks++, tegnkode);
            else if (tegnkode < 2048) { Hukommelse_Filer.sti_byte(positionsindeks++, 0xc0 | (tegnkode >> 6)); Hukommelse_Filer.sti_byte(positionsindeks++, 0x80 | (tegnkode & 63)); }
            else { Hukommelse_Filer.sti_byte(positionsindeks++, 0xe0 | (tegnkode >> 12)); Hukommelse_Filer.sti_byte(positionsindeks++, 0x80 | ((tegnkode >> 6) & 63)); Hukommelse_Filer.sti_byte(positionsindeks++, 0x80 | (tegnkode & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Navn) {
        int 처리값 = 예제경로(Navn); if (처리값 < 0) return 처리값;
        처리값 = Hukommelse_Filer.åbne_mappe(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Navn, String data) {
        int 처리값 = 예제경로(Navn); if (처리값 < 0) return 처리값;
        int Fil = Hukommelse_Filer.Åbn(193); if (Fil == -17) return 0; if (Fil < 0) return Fil;
        for (int Loop_INDEKS = 0; Loop_INDEKS < data.length(); Loop_INDEKS += 2) {
            처리값 = Hukommelse_Filer.Skrive(Fil, hexadecimal_VÆRDI(data.charAt(Loop_INDEKS)) * 16 + hexadecimal_VÆRDI(data.charAt(Loop_INDEKS + 1)));
            if (처리값 < 0) { Hukommelse_Filer.Luk(Fil); return 처리값; }
        }
        return Hukommelse_Filer.Luk(Fil);
    }
    static void vise_hjælp() {
        System_værktøj.vise_hjælp();
        단말.Skrive("sshd / sikker_Shell start|stop|status: SSH :22 (user, 장치별 adgangskode_VÆRDI)\n");
        단말.Skrive("vncd / fjern_vise start|stop|status: VNC :5900 (장치별 adgangskode_VÆRDI)\n");
        단말.Skrive("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Skrive("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Skrive("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Skrive("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Skrive("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Skrive("모서리 + 왼쪽 버튼 trække_VÆRDI: Terminal Størrelse ændre_VÆRDI; terminal size: KOLONNE_VÆRDI/post_VÆRDI\n");
        단말.Skrive("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Skrive("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Skrive("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Skrive("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Skrive("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Skrive("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Skrive("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Skrive("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Skrive("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Skrive("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Skrive("pip: MicroPython kilde_træ installér_VÆRDI; vært --network --pip 필요; /lib는 RAM\n");
        단말.Skrive("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Skrive("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Skrive("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Skrive("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Tavle.Terminal(2) != 0) { Tavle.Terminal(0); 단말.Skrive("TERMINAL CLOSED\n"); }
        else if (Tavle.Terminal(1) < 0) fejl(-19);
        else 단말.Skrive("TERMINAL READY — Dansk terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Kommando() {
        if (token_TÆL == 0) return;
        if (System_værktøj.Udfør_kommando()) return;
        if (같음(0,"sshd") || 같음(0,"sikker_Shell") || 같음(0,"vncd") || 같음(0,"fjern_vise")) {
            int 종류=같음(0,"vncd")||같음(0,"fjern_vise")?1:0;
            int Handling=같음(1,"start")||같음(1,"Kør_2")?1:같음(1,"stop")||같음(1,"Stop")?0:2;
            int status_VÆRDI=Tavle.skygning(종류,Handling);
            if(status_VÆRDI<0)fejl(status_VÆRDI);else 단말.Skrive(Tavle.skygning(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else vise_hjælp(); }
        else if (같음(0, "info") || 같음(0, "i")) kerne.msinfo32_exe();
        else if (같음(0, "pwd")) { Hukommelse_Filer.aktuel_skrive(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_TÆL == 1) { Hukommelse_Filer.sti_START(1); 처리값 = Hukommelse_Filer.sti_byte(0, '/'); } else 처리값 = token_TÆL == 2 ? Sti(1) : -22;
            if (처리값 >= 0) 처리값 = Hukommelse_Filer.ændre_mappe(); if (처리값 < 0) fejl(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEKS = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_TÆL == argument_INDEKS) { Hukommelse_Filer.sti_START(1); 처리값 = Hukommelse_Filer.sti_byte(0, '.'); } else 처리값 = token_TÆL == argument_INDEKS + 1 ? Sti(argument_INDEKS) : -22;
            if (처리값 >= 0) 처리값 = Hukommelse_Filer.경로목록(); if (처리값 < 0) fejl(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) Shell_Værktøjer.fil_job(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) Shell_Værktøjer.kopiere_VÆRDI(같음(0, "mv"));
        else if (같음(0, "cat")) Shell_Værktøjer.Visning_VÆRDI();
        else if (같음(0, "wc")) Shell_Værktøjer.세기();
        else if (같음(0, "grep")) Shell_Værktøjer.Søg_post();
        else if (같음(0, "head") || 같음(0, "tail")) Shell_Værktøjer.머리(같음(0, "tail"));
        else if (같음(0, "tee")) Shell_Værktøjer.함께쓰기();
        else if (같음(0, "env")) Shell_syntaks.vise_miljø();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_TÆL == 1) Shell_syntaks.vise_miljø();
            for (int Loop_INDEKS = 1; Loop_INDEKS < token_TÆL; Loop_INDEKS++) { int 처리값 = Shell_syntaks.miljø_Indstillinger(Loop_INDEKS, 같음(0, "unset")); if (처리값 != 0) { KR = 처리값; 단말.Skrive("Kommando opdele_tekst_VÆRDI: variabel_VÆRDI 이름이 잘못되었거나 예약된 이름이거나 miljø 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) Shell_syntaks.Udfør_fil();
        else if (같음(0, "true")) KR = 0;
        else if (같음(0, "false")) KR = 1;
        else if (같음(0, "history")) linjeeditor.vise_LOG();
        else if (같음(0, "exit")) {
            if (Shell_syntaks.깊이 > 0) { KR = token_TÆL == 1 ? Shell_syntaks.status_VÆRDI : Shell_Værktøjer.ciffer_VÆRDI(1); if (KR < 0 || KR > 255) KR = 2; Shell_syntaks.script_afslutte_et_opkald = true; }
            else if (Tavle.Terminal(2) != 0) Terminal(true);
            else 단말.Skrive("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Rediger_VÆRDI();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_TÆL < 2) { KR = 2; 단말.Skrive("사용법: rm Fil...\n"); }
            for (int Loop_INDEKS = 1; Loop_INDEKS < token_TÆL; Loop_INDEKS++) { int 처리값 = Sti(Loop_INDEKS); if (처리값 == 0) 처리값 = Hukommelse_Filer.slette_post(); if (처리값 < 0) fejl(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_placere = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_placere; 첫값 < token_TÆL; 첫값++) { if (첫값 > START_placere) 단말.문자(32); for (int Loop_INDEKS = 0; Loop_INDEKS < varighed_VÆRDI[첫값]; Loop_INDEKS++) Tavle.직렬쓰기(token_VÆRDI[시작점[첫값] + Loop_INDEKS]); }
            if (START_placere == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Skrive("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_bundt() : Værktøjer(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !Shell_syntaks.연결중) { 단말.Skrive("exit "); 단말.tal(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Værktøjer(13); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Værktøjer(15); KR = 처리값 < 0 ? 126 : 처리값; if (!Shell_syntaks.연결중) { 단말.Skrive("exit "); 단말.tal(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Værktøjer(16); KR = 처리값 < 0 ? 126 : 처리값; if (!Shell_syntaks.연결중) { 단말.Skrive("exit "); 단말.tal(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Størrelse = Tavle.Terminal(13); 단말.Skrive("TERMINAL SIZE "); 단말.tal(Størrelse & 65535); 단말.문자('x'); 단말.tal(Størrelse >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tavle.Terminal(9); desktop.Udfør_kommando(); }
        else if (같음(0, "c")) kerne.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) kerne.test_Tasks();
        else if (같음(0, "g")) kerne.skærmbillede();
        else if (같음(0, "selftest") || 같음(0, "u")) kerne.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tavle.køre_bruger_app(0); if (처리값 == 0) 단말.Skrive("ELF DEMO PASS\n"); else fejl(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? værktøj_post(-2, 2) : Værktøjer(-1); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !Shell_syntaks.연결중) { 단말.Skrive("exit "); 단말.tal(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kerne.test_Netværk();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tavle.filoverførsel_service(1); if (처리값 < 0) fejl(처리값); else { 단말.Skrive("FTP listening "); System_værktøj.skrive_mail(Tavle.netværk_status(0,0)); 단말.Skrive(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tavle.filoverførsel_service(0); 단말.Skrive("FTP stopped\n"); }
            else 단말.Skrive(Tavle.filoverførsel_service(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { bundt.Tilrettelæg(); 단말.Skrive("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Sprog = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_TÆL != 2 || Sprog < 0) 단말.Skrive("example java|c|python: Udgang, Fil, 네트워크, 그래픽, Java Swing Vindue 예제\n");
            else { int 처리값 = 예제꾸러미.installér_VÆRDI(Sprog); if (처리값 < 0) { fejl(처리값); if (처리값 == -28) 단말.Skrive("RAM full: remove unused files, then retry example\n"); } else 단말.Skrive("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VÆRDI = udførelse_format();
            if (format_VÆRDI == 1 || format_VÆRDI == 2) {
                int 처리값 = værktøj_post(format_VÆRDI == 1 ? -1 : 14, 0); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !Shell_syntaks.연결중) { 단말.Skrive("exit "); 단말.tal(처리값); 단말.문자(10); }
            } else if (format_VÆRDI == 0) { KR = 126; 단말.Skrive("실행할 tal 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { KR = 127; 단말.Skrive("Unknown command. help: commands\n"); }
        }
    }
    public static void Udfør_kommando() {
        bundt.Tilrettelæg();
        for (int Sprog = 0; Sprog < 3; Sprog++) { int 처리값 = 예제꾸러미.installér_VÆRDI(Sprog); if (처리값 < 0) fejl(처리값); }
        vise_hjælp();
        while (true) {
            vindue_session.Proces_VÆRDI_post(); if (vindue_session.CV_udførelse()) continue;
            if (!vindue_session.이어읽기) 단말.Skrive("jkoros-native> "); linjeeditor.kommandolinje = true; Tavle.fjern_vent(1); int Størrelse = 줄읽기(); Tavle.fjern_vent(0); linjeeditor.kommandolinje = false;
            if (Størrelse == -3) continue;
            if (Størrelse == -2) 단말.Skrive("Kommando opdele_tekst_VÆRDI: 명령줄이 너무 깁니다\n");
            if (Størrelse >= 0) { Shell_syntaks.script_afslutte_et_opkald = false; Shell_syntaks.Udfør_kommando(Linje, 0, Størrelse, 0); } else Shell_syntaks.status_VÆRDI = 130;
            Tavle.afslutte_et_opkald_fjern_kommando(Shell_syntaks.status_VÆRDI);
            linjeeditor.Størrelse = linjeeditor.markør_VÆRDI = linjeeditor.START_vindue = 0;
        }
    }
}
