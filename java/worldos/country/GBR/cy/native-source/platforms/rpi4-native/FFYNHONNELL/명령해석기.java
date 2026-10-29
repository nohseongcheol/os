// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 llinell_gorchymyn. Dyfyniad, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] llinell = new int[4096], tocyn_VALUE_eb540501 = new int[4096], 시작점 = new int[32], hyd_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], Golygu_enw = new int[63];
    static int tocyn_COUNT_3176ee99, Golygu_enw_hyd, mesur;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { bwrdd.직렬쓰기(VALUE); }
    static int 줄읽기() { return llinell_Editor.Darllen(); }
    static boolean 나누기(int Maint) {
        int safle = 0, 끝 = 0; tocyn_COUNT_3176ee99 = 0;
        while (safle < Maint) {
            while (safle < Maint && (llinell[safle] == 32 || llinell[safle] == 9)) safle++;
            if (safle == Maint) break;
            if (tocyn_COUNT_3176ee99 == 16) { 단말.Ysgrifennu("Gorchymyn dosrannu_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[tocyn_COUNT_3176ee99] = 끝; int Dyfyniad_VALUE = 0;
            while (safle < Maint) {
                int VALUE = llinell[safle++];
                if (Dyfyniad_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Dyfyniad_VALUE) { Dyfyniad_VALUE = 0; continue; }
                if (Dyfyniad_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Dyfyniad_VALUE = VALUE; continue; }
                tocyn_VALUE_eb540501[끝++] = VALUE;
            }
            if (Dyfyniad_VALUE != 0) { 단말.Ysgrifennu("Gorchymyn dosrannu_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            hyd_VALUE[tocyn_COUNT_3176ee99] = 끝 - 시작점[tocyn_COUNT_3176ee99]; tocyn_COUNT_3176ee99++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= tocyn_COUNT_3176ee99) return false;
        int safle_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int cod_nod=Word_SMS.charAt(순번);
            if (cod_nod>=0xd800 && cod_nod<=0xdbff && 순번+1<Word_SMS.length()) cod_nod=0x10000+((cod_nod-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int beit_COUNT=cod_nod<128?1:cod_nod<2048?2:cod_nod<65536?3:4;
            for (int SEQUENCE_VALUE=beit_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=beit_COUNT==1?cod_nod:SEQUENCE_VALUE==beit_COUNT-1?(beit_COUNT==2?0xc0:beit_COUNT==3?0xe0:0xf0)|(cod_nod>>(6*SEQUENCE_VALUE)):0x80|((cod_nod>>(6*SEQUENCE_VALUE))&63);
                if (safle_INDEX>=hyd_VALUE[INDEX] || tocyn_VALUE_eb540501[시작점[INDEX]+safle_INDEX++]!=VALUE) return false;
            }
        }
        return safle_INDEX==hyd_VALUE[INDEX];
    }
    static int LLWYBR(int INDEX) {
        if (INDEX >= tocyn_COUNT_3176ee99) return -22;
        int mesur = Cof_Ffeil.llwybr_START(hyd_VALUE[INDEX]); if (mesur < 0) return mesur;
        for (int Loop_INDEX = 0; Loop_INDEX < hyd_VALUE[INDEX]; Loop_INDEX++) {
            mesur = Cof_Ffeil.llwybr_beit(Loop_INDEX, tocyn_VALUE_eb540501[시작점[INDEX] + Loop_INDEX]); if (mesur < 0) return mesur;
        }
        return 0;
    }
    static void Gwall(int INDEX) { mesur = 1; 단말.Ysgrifennu("Gwall "); 단말.수(INDEX); 단말.문자(10); }
    static void Gwedd_VALUE() {
        if (tocyn_COUNT_3176ee99 != 2) { 단말.Ysgrifennu("사용법: cat Ffeil\n"); return; }
        int mesur = LLWYBR(1); if (mesur < 0) { Gwall(mesur); return; }
        int Ffeil = Cof_Ffeil.Agor(0); if (Ffeil < 0) { Gwall(Ffeil); return; }
        while (true) { int VALUE = Cof_Ffeil.Darllen(Ffeil); if (VALUE == 256) break; if (VALUE < 0) { Gwall(VALUE); break; } 원바이트(VALUE); }
        Cof_Ffeil.Cau(Ffeil); 단말.문자(10);
    }
    static void Golygu_VALUE() {
        if (tocyn_COUNT_3176ee99 != 2) { 단말.Ysgrifennu("사용법: edit Ffeil\n"); return; }
        int mesur = LLWYBR(1); if (mesur < 0) { Gwall(mesur); return; }
        Golygu_enw_hyd = hyd_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < Golygu_enw_hyd; Loop_INDEX++) Golygu_enw[Loop_INDEX] = tocyn_VALUE_eb540501[시작점[1] + Loop_INDEX];
        단말.Ysgrifennu("EDIT: Ffeil 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Maint = 0;
        while (true) {
            단말.Ysgrifennu("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Ysgrifennu("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && llinell[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Maint) { 단말.Ysgrifennu("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[Maint++] = llinell[Loop_INDEX];
            편집내용[Maint++] = 10;
        }
        Cof_Ffeil.llwybr_START(Golygu_enw_hyd);
        for (int Loop_INDEX = 0; Loop_INDEX < Golygu_enw_hyd; Loop_INDEX++) Cof_Ffeil.llwybr_beit(Loop_INDEX, Golygu_enw[Loop_INDEX]);
        int Ffeil = Cof_Ffeil.Agor(577); if (Ffeil < 0) { Gwall(Ffeil); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Maint; Loop_INDEX++) Cof_Ffeil.Ysgrifennu(Ffeil, 편집내용[Loop_INDEX]);
        Cof_Ffeil.Cau(Ffeil); 단말.Ysgrifennu("SAVED "); 단말.수(Maint); 단말.Ysgrifennu("beit_VALUE(주기억 Ffeil)\n");
    }
    static int hecs_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (tocyn_COUNT_3176ee99 != 2) { 단말.Ysgrifennu("사용법: load Ffeil | hex Ffeil\n"); return; }
        int mesur = LLWYBR(1); if (mesur < 0) { Gwall(mesur); return; }
        if (!넣기) {
            int Ffeil = Cof_Ffeil.Agor(0); if (Ffeil < 0) { Gwall(Ffeil); return; }
            단말.Ysgrifennu("HEX BEGIN "); 단말.수(Cof_Ffeil.Maint(Ffeil)); 단말.문자(10);
            int cofnod_COUNT = 0;
            while (true) {
                int VALUE = Cof_Ffeil.Darllen(Ffeil); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++cofnod_COUNT % 32 == 0) 단말.문자(10);
            }
            if (cofnod_COUNT % 32 != 0) 단말.문자(10);
            Cof_Ffeil.Cau(Ffeil); 단말.Ysgrifennu("HEX END\n"); return;
        }
        Golygu_enw_hyd = hyd_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < Golygu_enw_hyd; Loop_INDEX++) Golygu_enw[Loop_INDEX] = tocyn_VALUE_eb540501[시작점[1] + Loop_INDEX];
        단말.Ysgrifennu("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Maint = 0;
        while (true) {
            단말.Ysgrifennu("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Ysgrifennu("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && llinell[0] == '.') break;
            int 앞 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (llinell[Loop_INDEX] == 32 || llinell[Loop_INDEX] == 9) continue;
                int VALUE = hecs_VALUE(llinell[Loop_INDEX]);
                if (VALUE < 0 || Maint >= 편집내용.length) { 단말.Ysgrifennu("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = VALUE; else { 편집내용[Maint++] = 앞 * 16 + VALUE; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Ysgrifennu("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Cof_Ffeil.llwybr_START(Golygu_enw_hyd);
        for (int Loop_INDEX = 0; Loop_INDEX < Golygu_enw_hyd; Loop_INDEX++) Cof_Ffeil.llwybr_beit(Loop_INDEX, Golygu_enw[Loop_INDEX]);
        int Ffeil = Cof_Ffeil.Agor(577); if (Ffeil < 0) { Gwall(Ffeil); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Maint; Loop_INDEX++) Cof_Ffeil.Ysgrifennu(Ffeil, 편집내용[Loop_INDEX]);
        Cof_Ffeil.Cau(Ffeil); 단말.Ysgrifennu("LOADED "); 단말.수(Maint); 단말.Ysgrifennu("beit_VALUE(주기억 Ffeil)\n");
    }
    static int Offer(int INDEX) {
        return offeryn_cofnod(INDEX, 1);
    }
    static int offeryn_cofnod(int INDEX, int Gweithredu_2) {
        if (tocyn_COUNT_3176ee99 - Gweithredu_2 > 8) return -22;
        bwrdd.인수준비(tocyn_COUNT_3176ee99 - Gweithredu_2);
        for (int 첫값 = Gweithredu_2; 첫값 < tocyn_COUNT_3176ee99; 첫값++) {
            if (hyd_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < hyd_VALUE[첫값]; Loop_INDEX++) bwrdd.arg_beit(첫값 - Gweithredu_2, Loop_INDEX, tocyn_VALUE_eb540501[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? bwrdd.리눅스파일실행() : INDEX < 0 ? bwrdd.Gweithredu_defnyddiwr_ffeil() : bwrdd.rhedeg_defnyddiwr_Rhaglen(INDEX);
    }
    static int PYTHON_bwndel() {
        if (tocyn_COUNT_3176ee99 > 8) return -22;
        bwrdd.인수준비(tocyn_COUNT_3176ee99);
        String LLWYBR = "/lib/bwndel.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int safle_INDEX = 0;
        for (int 순번 = 0; 순번 < LLWYBR.length(); 순번++) {
            int nod_VALUE = LLWYBR.charAt(순번);
            if (nod_VALUE < 128) bwrdd.arg_beit(0, safle_INDEX++, nod_VALUE);
            else { bwrdd.arg_beit(0, safle_INDEX++, 0xe0 | (nod_VALUE >> 12)); bwrdd.arg_beit(0, safle_INDEX++, 0x80 | ((nod_VALUE >> 6) & 63)); bwrdd.arg_beit(0, safle_INDEX++, 0x80 | (nod_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < tocyn_COUNT_3176ee99; 순번++) {
            if (hyd_VALUE[순번] > 255) return -36;
            for (int nod_VALUE = 0; nod_VALUE < hyd_VALUE[순번]; nod_VALUE++) bwrdd.arg_beit(순번, nod_VALUE, tocyn_VALUE_eb540501[시작점[순번] + nod_VALUE]);
        }
        return bwrdd.rhedeg_defnyddiwr_Rhaglen(12);
    }
    static int 실행형식() {
        int 처리값 = LLWYBR(0); if (처리값 < 0) return 처리값;
        int Ffeil = Cof_Ffeil.Agor(0); if (Ffeil < 0) return Ffeil;
        int 첫값 = Cof_Ffeil.Darllen(Ffeil), beit_data = Cof_Ffeil.Darllen(Ffeil), cod_nod = Cof_Ffeil.Darllen(Ffeil), 뒷값 = Cof_Ffeil.Darllen(Ffeil);
        Cof_Ffeil.Cau(Ffeil);
        if (첫값 == 127 && beit_data == 'E' && cod_nod == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && beit_data == 'K' && cod_nod == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        bwrdd.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) bwrdd.arg_beit(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return bwrdd.rhedeg_defnyddiwr_Rhaglen(INDEX);
    }
    static void SMS_beit(int Ffeil, int VALUE) { Cof_Ffeil.Ysgrifennu(Ffeil, VALUE); }
    static void statig_ffeil(String Enw, String Cynnwys_VALUE) {
        // bwndel 파일명은 ASCII. Ffeil 내용은 UTF-8로 저장한다.
        Cof_Ffeil.llwybr_START(Enw.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Enw.length(); Loop_INDEX++) Cof_Ffeil.llwybr_beit(Loop_INDEX, Enw.charAt(Loop_INDEX));
        int Ffeil = Cof_Ffeil.Agor(193); if (Ffeil < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Cynnwys_VALUE.length(); Loop_INDEX++) {
            int cod_nod = Cynnwys_VALUE.charAt(Loop_INDEX);
            if (cod_nod >= 0xd800 && cod_nod <= 0xdbff && Loop_INDEX + 1 < Cynnwys_VALUE.length()) cod_nod = 0x10000 + ((cod_nod - 0xd800) << 10) + Cynnwys_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (cod_nod < 128) SMS_beit(Ffeil, cod_nod);
            else {
                int 수 = cod_nod < 2048 ? 2 : cod_nod < 65536 ? 3 : 4;
                SMS_beit(Ffeil, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (cod_nod >> (6 * (수 - 1))));
                for (int cofnod_COUNT = 수 - 1; cofnod_COUNT > 0; cofnod_COUNT--) SMS_beit(Ffeil, 0x80 | ((cod_nod >> (6 * (cofnod_COUNT - 1))) & 63));
            }
        }
        Cof_Ffeil.Cau(Ffeil);
    }
    static void 한글도움말() {
        단말.Ysgrifennu("F9 / Shift+Space: [EN] ↔ [cy]\n");
        단말.Ysgrifennu("  [CY] keyboard; [EN] ASCII\n");
        단말.Ysgrifennu("  a → a\n");
        단말.Ysgrifennu("  F9: EN ↔ cy | Ctrl+Shift+V: UTF-8\n");
        단말.Ysgrifennu("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Ysgrifennu("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Enw) {
        int beit_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Enw.length(); Loop_INDEX++) { int cod_nod = Enw.charAt(Loop_INDEX); if (cod_nod >= 0xd800 && cod_nod <= 0xdfff) return -22; beit_COUNT += cod_nod < 128 ? 1 : cod_nod < 2048 ? 2 : 3; }
        int 처리값 = Cof_Ffeil.llwybr_START(beit_COUNT); if (처리값 < 0) return 처리값;
        int safle_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Enw.length(); Loop_INDEX++) {
            int cod_nod = Enw.charAt(Loop_INDEX);
            if (cod_nod < 128) Cof_Ffeil.llwybr_beit(safle_INDEX++, cod_nod);
            else if (cod_nod < 2048) { Cof_Ffeil.llwybr_beit(safle_INDEX++, 0xc0 | (cod_nod >> 6)); Cof_Ffeil.llwybr_beit(safle_INDEX++, 0x80 | (cod_nod & 63)); }
            else { Cof_Ffeil.llwybr_beit(safle_INDEX++, 0xe0 | (cod_nod >> 12)); Cof_Ffeil.llwybr_beit(safle_INDEX++, 0x80 | ((cod_nod >> 6) & 63)); Cof_Ffeil.llwybr_beit(safle_INDEX++, 0x80 | (cod_nod & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Enw) {
        int 처리값 = 예제경로(Enw); if (처리값 < 0) return 처리값;
        처리값 = Cof_Ffeil.Creu_cyfeiriadur(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Enw, String data) {
        int 처리값 = 예제경로(Enw); if (처리값 < 0) return 처리값;
        int Ffeil = Cof_Ffeil.Agor(193); if (Ffeil == -17) return 0; if (Ffeil < 0) return Ffeil;
        for (int Loop_INDEX = 0; Loop_INDEX < data.length(); Loop_INDEX += 2) {
            처리값 = Cof_Ffeil.Ysgrifennu(Ffeil, hecs_VALUE(data.charAt(Loop_INDEX)) * 16 + hecs_VALUE(data.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Cof_Ffeil.Cau(Ffeil); return 처리값; }
        }
        return Cof_Ffeil.Cau(Ffeil);
    }
    static void sioe_help() {
        system_offeryn.sioe_help();
        단말.Ysgrifennu("sshd / diogel_cragen start|stop|status: SSH :22 (user, 장치별 cyfrinair_VALUE)\n");
        단말.Ysgrifennu("vncd / pell_dangos start|stop|status: VNC :5900 (장치별 cyfrinair_VALUE)\n");
        단말.Ysgrifennu("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Ysgrifennu("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Ysgrifennu("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Ysgrifennu("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Ysgrifennu("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Ysgrifennu("모서리 + 왼쪽 버튼 llusgo_VALUE: Terfynell Maint newid_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Ysgrifennu("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Ysgrifennu("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Ysgrifennu("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Ysgrifennu("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Ysgrifennu("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Ysgrifennu("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Ysgrifennu("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Ysgrifennu("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Ysgrifennu("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Ysgrifennu("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Ysgrifennu("pip: MicroPython ffynhonnell_coeden gosod_VALUE; lletya --network --pip 필요; /lib는 RAM\n");
        단말.Ysgrifennu("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Ysgrifennu("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Ysgrifennu("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Ysgrifennu("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terfynell(boolean 전환여부) {
        if (전환여부 && bwrdd.Terfynell(2) != 0) { bwrdd.Terfynell(0); 단말.Ysgrifennu("TERMINAL CLOSED\n"); }
        else if (bwrdd.Terfynell(1) < 0) Gwall(-19);
        else 단말.Ysgrifennu("TERMINAL READY — cy terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Gorchymyn() {
        if (tocyn_COUNT_3176ee99 == 0) return;
        if (system_offeryn.Gweithredu_gorchymyn()) return;
        if (같음(0,"sshd") || 같음(0,"diogel_cragen") || 같음(0,"vncd") || 같음(0,"pell_dangos")) {
            int 종류=같음(0,"vncd")||같음(0,"pell_dangos")?1:0;
            int Gweithrediad=같음(1,"start")||같음(1,"Gweithredu_2")?1:같음(1,"stop")||같음(1,"Atal")?0:2;
            int cyflwr_VALUE=bwrdd.cysgodi(종류,Gweithrediad);
            if(cyflwr_VALUE<0)Gwall(cyflwr_VALUE);else 단말.Ysgrifennu(bwrdd.cysgodi(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else sioe_help(); }
        else if (같음(0, "info") || 같음(0, "i")) cnewyllyn.msinfo32_exe();
        else if (같음(0, "pwd")) { Cof_Ffeil.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (tocyn_COUNT_3176ee99 == 1) { Cof_Ffeil.llwybr_START(1); 처리값 = Cof_Ffeil.llwybr_beit(0, '/'); } else 처리값 = tocyn_COUNT_3176ee99 == 2 ? LLWYBR(1) : -22;
            if (처리값 >= 0) 처리값 = Cof_Ffeil.newid_cyfeiriadur(); if (처리값 < 0) Gwall(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int arg_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (tocyn_COUNT_3176ee99 == arg_INDEX) { Cof_Ffeil.llwybr_START(1); 처리값 = Cof_Ffeil.llwybr_beit(0, '.'); } else 처리값 = tocyn_COUNT_3176ee99 == arg_INDEX + 1 ? LLWYBR(arg_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Cof_Ffeil.경로목록(); if (처리값 < 0) Gwall(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) cragen_Offer.ffeil_tasg(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) cragen_Offer.copïo_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) cragen_Offer.Gwedd_VALUE();
        else if (같음(0, "wc")) cragen_Offer.세기();
        else if (같음(0, "grep")) cragen_Offer.FIND_cofnod();
        else if (같음(0, "head") || 같음(0, "tail")) cragen_Offer.머리(같음(0, "tail"));
        else if (같음(0, "tee")) cragen_Offer.함께쓰기();
        else if (같음(0, "env")) cragen_cystrawen.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (tocyn_COUNT_3176ee99 == 1) cragen_cystrawen.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < tocyn_COUNT_3176ee99; Loop_INDEX++) { int 처리값 = cragen_cystrawen.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { mesur = 처리값; 단말.Ysgrifennu("Gorchymyn dosrannu_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) cragen_cystrawen.Gweithredu_ffeil();
        else if (같음(0, "true")) mesur = 0;
        else if (같음(0, "false")) mesur = 1;
        else if (같음(0, "history")) llinell_Editor.sioe_LOG();
        else if (같음(0, "exit")) {
            if (cragen_cystrawen.깊이 > 0) { mesur = tocyn_COUNT_3176ee99 == 1 ? cragen_cystrawen.cyflwr_VALUE : cragen_Offer.digid_VALUE(1); if (mesur < 0 || mesur > 255) mesur = 2; cragen_cystrawen.sgript_gorffen = true; }
            else if (bwrdd.Terfynell(2) != 0) Terfynell(true);
            else 단말.Ysgrifennu("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Golygu_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (tocyn_COUNT_3176ee99 < 2) { mesur = 2; 단말.Ysgrifennu("사용법: rm Ffeil...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < tocyn_COUNT_3176ee99; Loop_INDEX++) { int 처리값 = LLWYBR(Loop_INDEX); if (처리값 == 0) 처리값 = Cof_Ffeil.지우기(); if (처리값 < 0) Gwall(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_safle = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_safle; 첫값 < tocyn_COUNT_3176ee99; 첫값++) { if (첫값 > START_safle) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < hyd_VALUE[첫값]; Loop_INDEX++) bwrdd.직렬쓰기(tocyn_VALUE_eb540501[시작점[첫값] + Loop_INDEX]); }
            if (START_safle == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Ysgrifennu("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_bwndel() : Offer(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); mesur = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !cragen_cystrawen.연결중) { 단말.Ysgrifennu("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Offer(13); mesur = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Offer(15); mesur = 처리값 < 0 ? 126 : 처리값; if (!cragen_cystrawen.연결중) { 단말.Ysgrifennu("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Offer(16); mesur = 처리값 < 0 ? 126 : 처리값; if (!cragen_cystrawen.연결중) { 단말.Ysgrifennu("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Maint = bwrdd.Terfynell(13); 단말.Ysgrifennu("TERMINAL SIZE "); 단말.수(Maint & 65535); 단말.문자('x'); 단말.수(Maint >>> 16); 단말.문자(10); }
            else Terfynell(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { bwrdd.Terfynell(9); bwrdd_gwaith.Gweithredu_gorchymyn(); }
        else if (같음(0, "c")) cnewyllyn.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) cnewyllyn.작업시험();
        else if (같음(0, "g")) cnewyllyn.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) cnewyllyn.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = bwrdd.rhedeg_defnyddiwr_Rhaglen(0); if (처리값 == 0) 단말.Ysgrifennu("ELF DEMO PASS\n"); else Gwall(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? offeryn_cofnod(-2, 2) : Offer(-1); mesur = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !cragen_cystrawen.연결중) { 단말.Ysgrifennu("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) cnewyllyn.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = bwrdd.ffeil_trosglwyddo_gwasanaeth(1); if (처리값 < 0) Gwall(처리값); else { 단말.Ysgrifennu("FTP listening "); system_offeryn.ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(0,0)); 단말.Ysgrifennu(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { bwrdd.ffeil_trosglwyddo_gwasanaeth(0); 단말.Ysgrifennu("FTP stopped\n"); }
            else 단말.Ysgrifennu(bwrdd.ffeil_trosglwyddo_gwasanaeth(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { bwndel.Paratoi(); 단말.Ysgrifennu("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Iaith = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (tocyn_COUNT_3176ee99 != 2 || Iaith < 0) 단말.Ysgrifennu("example java|c|python: Allbwn, Ffeil, 네트워크, 그래픽, Java Swing ffenestr 예제\n");
            else { int 처리값 = 예제꾸러미.gosod_VALUE(Iaith); if (처리값 < 0) { Gwall(처리값); if (처리값 == -28) 단말.Ysgrifennu("RAM full: remove unused files, then retry example\n"); } else 단말.Ysgrifennu("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int fformat_VALUE = 실행형식();
            if (fformat_VALUE == 1 || fformat_VALUE == 2) {
                int 처리값 = offeryn_cofnod(fformat_VALUE == 1 ? -1 : 14, 0); mesur = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !cragen_cystrawen.연결중) { 단말.Ysgrifennu("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (fformat_VALUE == 0) { mesur = 126; 단말.Ysgrifennu("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { mesur = 127; 단말.Ysgrifennu("Unknown command. help: commands\n"); }
        }
    }
    public static void Gweithredu_gorchymyn() {
        bwndel.Paratoi();
        for (int Iaith = 0; Iaith < 3; Iaith++) { int 처리값 = 예제꾸러미.gosod_VALUE(Iaith); if (처리값 < 0) Gwall(처리값); }
        sioe_help();
        while (true) {
            ffenestr_sesiwn.Proses_VALUE_cofnod(); if (ffenestr_sesiwn.재개()) continue;
            if (!ffenestr_sesiwn.이어읽기) 단말.Ysgrifennu("jkoros-native> "); llinell_Editor.llinell_gorchymyn = true; bwrdd.pell_aros(1); int Maint = 줄읽기(); bwrdd.pell_aros(0); llinell_Editor.llinell_gorchymyn = false;
            if (Maint == -3) continue;
            if (Maint == -2) 단말.Ysgrifennu("Gorchymyn dosrannu_VALUE: 명령줄이 너무 깁니다\n");
            if (Maint >= 0) { cragen_cystrawen.sgript_gorffen = false; cragen_cystrawen.Gweithredu_gorchymyn(llinell, 0, Maint, 0); } else cragen_cystrawen.cyflwr_VALUE = 130;
            bwrdd.gorffen_pell_gorchymyn(cragen_cystrawen.cyflwr_VALUE);
            llinell_Editor.Maint = llinell_Editor.cyrchwr_VALUE = llinell_Editor.START_ffenestr = 0;
        }
    }
}
