// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 linja_ta_kmand. Kwotazzjoni, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] linja = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], tul_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], editja_isem = new int[63];
    static int token_COUNT, editja_isem_tul, miżura;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { bord.직렬쓰기(VALUE); }
    static int 줄읽기() { return linja_Editur.읽기(); }
    static boolean 나누기(int daqqas) {
        int pożizzjoni = 0, 끝 = 0; token_COUNT = 0;
        while (pożizzjoni < daqqas) {
            while (pożizzjoni < daqqas && (linja[pożizzjoni] == 32 || linja[pożizzjoni] == 9)) pożizzjoni++;
            if (pożizzjoni == daqqas) break;
            if (token_COUNT == 16) { 단말.kiteb("kmand analizza_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Kwotazzjoni_VALUE = 0;
            while (pożizzjoni < daqqas) {
                int VALUE = linja[pożizzjoni++];
                if (Kwotazzjoni_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Kwotazzjoni_VALUE) { Kwotazzjoni_VALUE = 0; continue; }
                if (Kwotazzjoni_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Kwotazzjoni_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Kwotazzjoni_VALUE != 0) { 단말.kiteb("kmand analizza_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            tul_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int pożizzjoni_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int kodiċi_tal_karattru=Word_SMS.charAt(순번);
            if (kodiċi_tal_karattru>=0xd800 && kodiċi_tal_karattru<=0xdbff && 순번+1<Word_SMS.length()) kodiċi_tal_karattru=0x10000+((kodiċi_tal_karattru-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_COUNT=kodiċi_tal_karattru<128?1:kodiċi_tal_karattru<2048?2:kodiċi_tal_karattru<65536?3:4;
            for (int SEQUENCE_VALUE=byte_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=byte_COUNT==1?kodiċi_tal_karattru:SEQUENCE_VALUE==byte_COUNT-1?(byte_COUNT==2?0xc0:byte_COUNT==3?0xe0:0xf0)|(kodiċi_tal_karattru>>(6*SEQUENCE_VALUE)):0x80|((kodiċi_tal_karattru>>(6*SEQUENCE_VALUE))&63);
                if (pożizzjoni_INDEX>=tul_VALUE[INDEX] || token_VALUE[시작점[INDEX]+pożizzjoni_INDEX++]!=VALUE) return false;
            }
        }
        return pożizzjoni_INDEX==tul_VALUE[INDEX];
    }
    static int mogħdija(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int miżura = Memorja_Fajls.mogħdija_Bidu(tul_VALUE[INDEX]); if (miżura < 0) return miżura;
        for (int Loop_INDEX = 0; Loop_INDEX < tul_VALUE[INDEX]; Loop_INDEX++) {
            miżura = Memorja_Fajls.mogħdija_byte(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (miżura < 0) return miżura;
        }
        return 0;
    }
    static void żball(int INDEX) { miżura = 1; 단말.kiteb("żball "); 단말.수(INDEX); 단말.문자(10); }
    static void wera_VALUE() {
        if (token_COUNT != 2) { 단말.kiteb("사용법: cat fajl\n"); return; }
        int miżura = mogħdija(1); if (miżura < 0) { żball(miżura); return; }
        int fajl = Memorja_Fajls.fetaħ(0); if (fajl < 0) { żball(fajl); return; }
        while (true) { int VALUE = Memorja_Fajls.읽기(fajl); if (VALUE == 256) break; if (VALUE < 0) { żball(VALUE); break; } 원바이트(VALUE); }
        Memorja_Fajls.agħlaq(fajl); 단말.문자(10);
    }
    static void editja_VALUE() {
        if (token_COUNT != 2) { 단말.kiteb("사용법: edit fajl\n"); return; }
        int miżura = mogħdija(1); if (miżura < 0) { żball(miżura); return; }
        editja_isem_tul = tul_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < editja_isem_tul; Loop_INDEX++) editja_isem[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.kiteb("EDIT: fajl 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int daqqas = 0;
        while (true) {
            단말.kiteb("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.kiteb("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && linja[0] == '.') break;
            if (입력 + 1 > 편집내용.length - daqqas) { 단말.kiteb("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[daqqas++] = linja[Loop_INDEX];
            편집내용[daqqas++] = 10;
        }
        Memorja_Fajls.mogħdija_Bidu(editja_isem_tul);
        for (int Loop_INDEX = 0; Loop_INDEX < editja_isem_tul; Loop_INDEX++) Memorja_Fajls.mogħdija_byte(Loop_INDEX, editja_isem[Loop_INDEX]);
        int fajl = Memorja_Fajls.fetaħ(577); if (fajl < 0) { żball(fajl); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < daqqas; Loop_INDEX++) Memorja_Fajls.kiteb(fajl, 편집내용[Loop_INDEX]);
        Memorja_Fajls.agħlaq(fajl); 단말.kiteb("SAVED "); 단말.수(daqqas); 단말.kiteb("byte_VALUE(주기억 fajl)\n");
    }
    static int hex_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.kiteb("사용법: load fajl | hex fajl\n"); return; }
        int miżura = mogħdija(1); if (miżura < 0) { żball(miżura); return; }
        if (!넣기) {
            int fajl = Memorja_Fajls.fetaħ(0); if (fajl < 0) { żball(fajl); return; }
            단말.kiteb("HEX BEGIN "); 단말.수(Memorja_Fajls.daqqas(fajl)); 단말.문자(10);
            int entrata_COUNT = 0;
            while (true) {
                int VALUE = Memorja_Fajls.읽기(fajl); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++entrata_COUNT % 32 == 0) 단말.문자(10);
            }
            if (entrata_COUNT % 32 != 0) 단말.문자(10);
            Memorja_Fajls.agħlaq(fajl); 단말.kiteb("HEX END\n"); return;
        }
        editja_isem_tul = tul_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < editja_isem_tul; Loop_INDEX++) editja_isem[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.kiteb("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int daqqas = 0;
        while (true) {
            단말.kiteb("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.kiteb("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && linja[0] == '.') break;
            int 앞 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (linja[Loop_INDEX] == 32 || linja[Loop_INDEX] == 9) continue;
                int VALUE = hex_VALUE(linja[Loop_INDEX]);
                if (VALUE < 0 || daqqas >= 편집내용.length) { 단말.kiteb("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = VALUE; else { 편집내용[daqqas++] = 앞 * 16 + VALUE; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.kiteb("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memorja_Fajls.mogħdija_Bidu(editja_isem_tul);
        for (int Loop_INDEX = 0; Loop_INDEX < editja_isem_tul; Loop_INDEX++) Memorja_Fajls.mogħdija_byte(Loop_INDEX, editja_isem[Loop_INDEX]);
        int fajl = Memorja_Fajls.fetaħ(577); if (fajl < 0) { żball(fajl); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < daqqas; Loop_INDEX++) Memorja_Fajls.kiteb(fajl, 편집내용[Loop_INDEX]);
        Memorja_Fajls.agħlaq(fajl); 단말.kiteb("LOADED "); 단말.수(daqqas); 단말.kiteb("byte_VALUE(주기억 fajl)\n");
    }
    static int Għodod(int INDEX) {
        return għodda_entrata(INDEX, 1);
    }
    static int għodda_entrata(int INDEX, int serje) {
        if (token_COUNT - serje > 8) return -22;
        bord.인수준비(token_COUNT - serje);
        for (int 첫값 = serje; 첫값 < token_COUNT; 첫값++) {
            if (tul_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < tul_VALUE[첫값]; Loop_INDEX++) bord.argument_byte(첫값 - serje, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? bord.리눅스파일실행() : INDEX < 0 ? bord.eżegwixxa_utent_fajl() : bord.serje_utent_programm(INDEX);
    }
    static int PYTHON_lott() {
        if (token_COUNT > 8) return -22;
        bord.인수준비(token_COUNT);
        String mogħdija = "/lib/lott.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int pożizzjoni_INDEX = 0;
        for (int 순번 = 0; 순번 < mogħdija.length(); 순번++) {
            int karattru_VALUE = mogħdija.charAt(순번);
            if (karattru_VALUE < 128) bord.argument_byte(0, pożizzjoni_INDEX++, karattru_VALUE);
            else { bord.argument_byte(0, pożizzjoni_INDEX++, 0xe0 | (karattru_VALUE >> 12)); bord.argument_byte(0, pożizzjoni_INDEX++, 0x80 | ((karattru_VALUE >> 6) & 63)); bord.argument_byte(0, pożizzjoni_INDEX++, 0x80 | (karattru_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (tul_VALUE[순번] > 255) return -36;
            for (int karattru_VALUE = 0; karattru_VALUE < tul_VALUE[순번]; karattru_VALUE++) bord.argument_byte(순번, karattru_VALUE, token_VALUE[시작점[순번] + karattru_VALUE]);
        }
        return bord.serje_utent_programm(12);
    }
    static int 실행형식() {
        int 처리값 = mogħdija(0); if (처리값 < 0) return 처리값;
        int fajl = Memorja_Fajls.fetaħ(0); if (fajl < 0) return fajl;
        int 첫값 = Memorja_Fajls.읽기(fajl), byte_data = Memorja_Fajls.읽기(fajl), kodiċi_tal_karattru = Memorja_Fajls.읽기(fajl), 뒷값 = Memorja_Fajls.읽기(fajl);
        Memorja_Fajls.agħlaq(fajl);
        if (첫값 == 127 && byte_data == 'E' && kodiċi_tal_karattru == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_data == 'K' && kodiċi_tal_karattru == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        bord.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) bord.argument_byte(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return bord.serje_utent_programm(INDEX);
    }
    static void SMS_byte(int fajl, int VALUE) { Memorja_Fajls.kiteb(fajl, VALUE); }
    static void statiku_fajl(String isem, String Kontenut_VALUE) {
        // lott 파일명은 ASCII. fajl 내용은 UTF-8로 저장한다.
        Memorja_Fajls.mogħdija_Bidu(isem.length());
        for (int Loop_INDEX = 0; Loop_INDEX < isem.length(); Loop_INDEX++) Memorja_Fajls.mogħdija_byte(Loop_INDEX, isem.charAt(Loop_INDEX));
        int fajl = Memorja_Fajls.fetaħ(193); if (fajl < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Kontenut_VALUE.length(); Loop_INDEX++) {
            int kodiċi_tal_karattru = Kontenut_VALUE.charAt(Loop_INDEX);
            if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdbff && Loop_INDEX + 1 < Kontenut_VALUE.length()) kodiċi_tal_karattru = 0x10000 + ((kodiċi_tal_karattru - 0xd800) << 10) + Kontenut_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (kodiċi_tal_karattru < 128) SMS_byte(fajl, kodiċi_tal_karattru);
            else {
                int 수 = kodiċi_tal_karattru < 2048 ? 2 : kodiċi_tal_karattru < 65536 ? 3 : 4;
                SMS_byte(fajl, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kodiċi_tal_karattru >> (6 * (수 - 1))));
                for (int entrata_COUNT = 수 - 1; entrata_COUNT > 0; entrata_COUNT--) SMS_byte(fajl, 0x80 | ((kodiċi_tal_karattru >> (6 * (entrata_COUNT - 1))) & 63));
            }
        }
        Memorja_Fajls.agħlaq(fajl);
    }
    static void 한글도움말() {
        단말.kiteb("F9 / Shift+Space: [EN] ↔ [mt]\n");
        단말.kiteb("  [MT] keyboard; [EN] ASCII\n");
        단말.kiteb("  # → €\n");
        단말.kiteb("  F9: EN ↔ mt | Ctrl+Shift+V: UTF-8\n");
        단말.kiteb("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.kiteb("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String isem) {
        int byte_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < isem.length(); Loop_INDEX++) { int kodiċi_tal_karattru = isem.charAt(Loop_INDEX); if (kodiċi_tal_karattru >= 0xd800 && kodiċi_tal_karattru <= 0xdfff) return -22; byte_COUNT += kodiċi_tal_karattru < 128 ? 1 : kodiċi_tal_karattru < 2048 ? 2 : 3; }
        int 처리값 = Memorja_Fajls.mogħdija_Bidu(byte_COUNT); if (처리값 < 0) return 처리값;
        int pożizzjoni_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < isem.length(); Loop_INDEX++) {
            int kodiċi_tal_karattru = isem.charAt(Loop_INDEX);
            if (kodiċi_tal_karattru < 128) Memorja_Fajls.mogħdija_byte(pożizzjoni_INDEX++, kodiċi_tal_karattru);
            else if (kodiċi_tal_karattru < 2048) { Memorja_Fajls.mogħdija_byte(pożizzjoni_INDEX++, 0xc0 | (kodiċi_tal_karattru >> 6)); Memorja_Fajls.mogħdija_byte(pożizzjoni_INDEX++, 0x80 | (kodiċi_tal_karattru & 63)); }
            else { Memorja_Fajls.mogħdija_byte(pożizzjoni_INDEX++, 0xe0 | (kodiċi_tal_karattru >> 12)); Memorja_Fajls.mogħdija_byte(pożizzjoni_INDEX++, 0x80 | ((kodiċi_tal_karattru >> 6) & 63)); Memorja_Fajls.mogħdija_byte(pożizzjoni_INDEX++, 0x80 | (kodiċi_tal_karattru & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String isem) {
        int 처리값 = 예제경로(isem); if (처리값 < 0) return 처리값;
        처리값 = Memorja_Fajls.ħalaq_direttorju(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String isem, String data) {
        int 처리값 = 예제경로(isem); if (처리값 < 0) return 처리값;
        int fajl = Memorja_Fajls.fetaħ(193); if (fajl == -17) return 0; if (fajl < 0) return fajl;
        for (int Loop_INDEX = 0; Loop_INDEX < data.length(); Loop_INDEX += 2) {
            처리값 = Memorja_Fajls.kiteb(fajl, hex_VALUE(data.charAt(Loop_INDEX)) * 16 + hex_VALUE(data.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memorja_Fajls.agħlaq(fajl); return 처리값; }
        }
        return Memorja_Fajls.agħlaq(fajl);
    }
    static void wera_għajnuna() {
        sistema_għodda.wera_għajnuna();
        단말.kiteb("sshd / sigur_shell start|stop|status: SSH :22 (user, 장치별 password_VALUE)\n");
        단말.kiteb("vncd / mill_bogħod_wera start|stop|status: VNC :5900 (장치별 password_VALUE)\n");
        단말.kiteb("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.kiteb("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.kiteb("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.kiteb("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.kiteb("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.kiteb("모서리 + 왼쪽 버튼 dreggja_VALUE: Terminal daqqas bidel_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.kiteb("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.kiteb("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.kiteb("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.kiteb("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.kiteb("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.kiteb("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.kiteb("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.kiteb("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.kiteb("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.kiteb("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.kiteb("pip: MicroPython sors_siġra installa_VALUE; host --network --pip 필요; /lib는 RAM\n");
        단말.kiteb("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.kiteb("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.kiteb("/example/java /example/c /example/python: examples ready at boot\n");
        단말.kiteb("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && bord.Terminal(2) != 0) { bord.Terminal(0); 단말.kiteb("TERMINAL CLOSED\n"); }
        else if (bord.Terminal(1) < 0) żball(-19);
        else 단말.kiteb("TERMINAL READY — mt terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void kmand() {
        if (token_COUNT == 0) return;
        if (sistema_għodda.eżegwixxa_kmand()) return;
        if (같음(0,"sshd") || 같음(0,"sigur_shell") || 같음(0,"vncd") || 같음(0,"mill_bogħod_wera")) {
            int 종류=같음(0,"vncd")||같음(0,"mill_bogħod_wera")?1:0;
            int azzjoni=같음(1,"start")||같음(1,"serje")?1:같음(1,"stop")||같음(1,"waqqaf")?0:2;
            int stat_VALUE=bord.insegwiment(종류,azzjoni);
            if(stat_VALUE<0)żball(stat_VALUE);else 단말.kiteb(bord.insegwiment(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else wera_għajnuna(); }
        else if (같음(0, "info") || 같음(0, "i")) kernel.msinfo32_exe();
        else if (같음(0, "pwd")) { Memorja_Fajls.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Memorja_Fajls.mogħdija_Bidu(1); 처리값 = Memorja_Fajls.mogħdija_byte(0, '/'); } else 처리값 = token_COUNT == 2 ? mogħdija(1) : -22;
            if (처리값 >= 0) 처리값 = Memorja_Fajls.bidel_direttorju(); if (처리값 < 0) żball(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argument_INDEX) { Memorja_Fajls.mogħdija_Bidu(1); 처리값 = Memorja_Fajls.mogħdija_byte(0, '.'); } else 처리값 = token_COUNT == argument_INDEX + 1 ? mogħdija(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memorja_Fajls.경로목록(); if (처리값 < 0) żball(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) shell_Għodod.fajl_każ(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) shell_Għodod.kkopja_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) shell_Għodod.wera_VALUE();
        else if (같음(0, "wc")) shell_Għodod.세기();
        else if (같음(0, "grep")) shell_Għodod.sab_entrata();
        else if (같음(0, "head") || 같음(0, "tail")) shell_Għodod.머리(같음(0, "tail"));
        else if (같음(0, "tee")) shell_Għodod.함께쓰기();
        else if (같음(0, "env")) shell_sintassi.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) shell_sintassi.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = shell_sintassi.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { miżura = 처리값; 단말.kiteb("kmand analizza_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) shell_sintassi.eżegwixxa_fajl();
        else if (같음(0, "true")) miżura = 0;
        else if (같음(0, "false")) miżura = 1;
        else if (같음(0, "history")) linja_Editur.wera_LOG();
        else if (같음(0, "exit")) {
            if (shell_sintassi.깊이 > 0) { miżura = token_COUNT == 1 ? shell_sintassi.stat_VALUE : shell_Għodod.ċifra_VALUE(1); if (miżura < 0 || miżura > 255) miżura = 2; shell_sintassi.skript_ttermina = true; }
            else if (bord.Terminal(2) != 0) Terminal(true);
            else 단말.kiteb("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) editja_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { miżura = 2; 단말.kiteb("사용법: rm fajl...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = mogħdija(Loop_INDEX); if (처리값 == 0) 처리값 = Memorja_Fajls.지우기(); if (처리값 < 0) żball(처리값); }
        }
        else if (같음(0, "echo")) {
            int Bidu_pożizzjoni = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Bidu_pożizzjoni; 첫값 < token_COUNT; 첫값++) { if (첫값 > Bidu_pożizzjoni) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < tul_VALUE[첫값]; Loop_INDEX++) bord.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Bidu_pożizzjoni == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.kiteb("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_lott() : Għodod(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); miżura = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !shell_sintassi.연결중) { 단말.kiteb("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Għodod(13); miżura = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Għodod(15); miżura = 처리값 < 0 ? 126 : 처리값; if (!shell_sintassi.연결중) { 단말.kiteb("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Għodod(16); miżura = 처리값 < 0 ? 126 : 처리값; if (!shell_sintassi.연결중) { 단말.kiteb("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int daqqas = bord.Terminal(13); 단말.kiteb("TERMINAL SIZE "); 단말.수(daqqas & 65535); 단말.문자('x'); 단말.수(daqqas >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { bord.Terminal(9); desktop.eżegwixxa_kmand(); }
        else if (같음(0, "c")) kernel.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kernel.작업시험();
        else if (같음(0, "g")) kernel.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kernel.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = bord.serje_utent_programm(0); if (처리값 == 0) 단말.kiteb("ELF DEMO PASS\n"); else żball(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? għodda_entrata(-2, 2) : Għodod(-1); miżura = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !shell_sintassi.연결중) { 단말.kiteb("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kernel.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = bord.fajl_trasferiment_servizz(1); if (처리값 < 0) żball(처리값); else { 단말.kiteb("FTP listening "); sistema_għodda.kiteb_ADDRESS(bord.netwerk_stat(0,0)); 단말.kiteb(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { bord.fajl_trasferiment_servizz(0); 단말.kiteb("FTP stopped\n"); }
            else 단말.kiteb(bord.fajl_trasferiment_servizz(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { lott.Ħejji(); 단말.kiteb("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Lingwa = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Lingwa < 0) 단말.kiteb("example java|c|python: 출력, fajl, 네트워크, 그래픽, Java Swing tieqa 예제\n");
            else { int 처리값 = 예제꾸러미.installa_VALUE(Lingwa); if (처리값 < 0) { żball(처리값); if (처리값 == -28) 단말.kiteb("RAM full: remove unused files, then retry example\n"); } else 단말.kiteb("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = għodda_entrata(format_VALUE == 1 ? -1 : 14, 0); miżura = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !shell_sintassi.연결중) { 단말.kiteb("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { miżura = 126; 단말.kiteb("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { miżura = 127; 단말.kiteb("Unknown command. help: commands\n"); }
        }
    }
    public static void eżegwixxa_kmand() {
        lott.Ħejji();
        for (int Lingwa = 0; Lingwa < 3; Lingwa++) { int 처리값 = 예제꾸러미.installa_VALUE(Lingwa); if (처리값 < 0) żball(처리값); }
        wera_għajnuna();
        while (true) {
            tieqa_sessjoni.Proċess_VALUE_entrata(); if (tieqa_sessjoni.재개()) continue;
            if (!tieqa_sessjoni.이어읽기) 단말.kiteb("jkoros-native> "); linja_Editur.linja_ta_kmand = true; bord.원격대기(1); int daqqas = 줄읽기(); bord.원격대기(0); linja_Editur.linja_ta_kmand = false;
            if (daqqas == -3) continue;
            if (daqqas == -2) 단말.kiteb("kmand analizza_VALUE: 명령줄이 너무 깁니다\n");
            if (daqqas >= 0) { shell_sintassi.skript_ttermina = false; shell_sintassi.eżegwixxa_kmand(linja, 0, daqqas, 0); } else shell_sintassi.stat_VALUE = 130;
            bord.ttermina_mill_bogħod_kmand(shell_sintassi.stat_VALUE);
            linja_Editur.daqqas = linja_Editur.kerser_VALUE = linja_Editur.Bidu_tieqa = 0;
        }
    }
}
