// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 rreshti_i_komandës. Citim, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] linjë = new int[4096], kodi_VALUE = new int[4096], 시작점 = new int[32], gjatësi_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], redaktim_emër = new int[63];
    static int kodi_COUNT, redaktim_emër_gjatësi, llogaritje;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { panel.직렬쓰기(VALUE); }
    static int 줄읽기() { return linjë_Redaktori.Leximi(); }
    static boolean 나누기(int Madhësi) {
        int Pozicioni = 0, 끝 = 0; kodi_COUNT = 0;
        while (Pozicioni < Madhësi) {
            while (Pozicioni < Madhësi && (linjë[Pozicioni] == 32 || linjë[Pozicioni] == 9)) Pozicioni++;
            if (Pozicioni == Madhësi) break;
            if (kodi_COUNT == 16) { 단말.Shkrimi("Komanda analizoj_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[kodi_COUNT] = 끝; int Citim_VALUE = 0;
            while (Pozicioni < Madhësi) {
                int VALUE = linjë[Pozicioni++];
                if (Citim_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Citim_VALUE) { Citim_VALUE = 0; continue; }
                if (Citim_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Citim_VALUE = VALUE; continue; }
                kodi_VALUE[끝++] = VALUE;
            }
            if (Citim_VALUE != 0) { 단말.Shkrimi("Komanda analizoj_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            gjatësi_VALUE[kodi_COUNT] = 끝 - 시작점[kodi_COUNT]; kodi_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= kodi_COUNT) return false;
        int pozicioni_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int kodi_i_karakterit=Word_SMS.charAt(순번);
            if (kodi_i_karakterit>=0xd800 && kodi_i_karakterit<=0xdbff && 순번+1<Word_SMS.length()) kodi_i_karakterit=0x10000+((kodi_i_karakterit-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bajt_COUNT=kodi_i_karakterit<128?1:kodi_i_karakterit<2048?2:kodi_i_karakterit<65536?3:4;
            for (int SEQUENCE_VALUE=bajt_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bajt_COUNT==1?kodi_i_karakterit:SEQUENCE_VALUE==bajt_COUNT-1?(bajt_COUNT==2?0xc0:bajt_COUNT==3?0xe0:0xf0)|(kodi_i_karakterit>>(6*SEQUENCE_VALUE)):0x80|((kodi_i_karakterit>>(6*SEQUENCE_VALUE))&63);
                if (pozicioni_INDEX>=gjatësi_VALUE[INDEX] || kodi_VALUE[시작점[INDEX]+pozicioni_INDEX++]!=VALUE) return false;
            }
        }
        return pozicioni_INDEX==gjatësi_VALUE[INDEX];
    }
    static int POZICIONI(int INDEX) {
        if (INDEX >= kodi_COUNT) return -22;
        int llogaritje = Memorie_Skedarët.shteg_nis(gjatësi_VALUE[INDEX]); if (llogaritje < 0) return llogaritje;
        for (int Loop_INDEX = 0; Loop_INDEX < gjatësi_VALUE[INDEX]; Loop_INDEX++) {
            llogaritje = Memorie_Skedarët.shteg_bajt(Loop_INDEX, kodi_VALUE[시작점[INDEX] + Loop_INDEX]); if (llogaritje < 0) return llogaritje;
        }
        return 0;
    }
    static void GABIM(int INDEX) { llogaritje = 1; 단말.Shkrimi("GABIM "); 단말.수(INDEX); 단말.문자(10); }
    static void Pamja_VALUE() {
        if (kodi_COUNT != 2) { 단말.Shkrimi("사용법: cat Kartelë\n"); return; }
        int llogaritje = POZICIONI(1); if (llogaritje < 0) { GABIM(llogaritje); return; }
        int Kartelë = Memorie_Skedarët.Hap(0); if (Kartelë < 0) { GABIM(Kartelë); return; }
        while (true) { int VALUE = Memorie_Skedarët.Leximi(Kartelë); if (VALUE == 256) break; if (VALUE < 0) { GABIM(VALUE); break; } 원바이트(VALUE); }
        Memorie_Skedarët.Mbyll(Kartelë); 단말.문자(10);
    }
    static void redaktim_VALUE() {
        if (kodi_COUNT != 2) { 단말.Shkrimi("사용법: edit Kartelë\n"); return; }
        int llogaritje = POZICIONI(1); if (llogaritje < 0) { GABIM(llogaritje); return; }
        redaktim_emër_gjatësi = gjatësi_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < redaktim_emër_gjatësi; Loop_INDEX++) redaktim_emër[Loop_INDEX] = kodi_VALUE[시작점[1] + Loop_INDEX];
        단말.Shkrimi("EDIT: Kartelë 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Madhësi = 0;
        while (true) {
            단말.Shkrimi("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Shkrimi("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && linjë[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Madhësi) { 단말.Shkrimi("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[Madhësi++] = linjë[Loop_INDEX];
            편집내용[Madhësi++] = 10;
        }
        Memorie_Skedarët.shteg_nis(redaktim_emër_gjatësi);
        for (int Loop_INDEX = 0; Loop_INDEX < redaktim_emër_gjatësi; Loop_INDEX++) Memorie_Skedarët.shteg_bajt(Loop_INDEX, redaktim_emër[Loop_INDEX]);
        int Kartelë = Memorie_Skedarët.Hap(577); if (Kartelë < 0) { GABIM(Kartelë); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Madhësi; Loop_INDEX++) Memorie_Skedarët.Shkrimi(Kartelë, 편집내용[Loop_INDEX]);
        Memorie_Skedarët.Mbyll(Kartelë); 단말.Shkrimi("SAVED "); 단말.수(Madhësi); 단말.Shkrimi("bajt_VALUE(주기억 Kartelë)\n");
    }
    static int hekzadecimal_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (kodi_COUNT != 2) { 단말.Shkrimi("사용법: load Kartelë | hex Kartelë\n"); return; }
        int llogaritje = POZICIONI(1); if (llogaritje < 0) { GABIM(llogaritje); return; }
        if (!넣기) {
            int Kartelë = Memorie_Skedarët.Hap(0); if (Kartelë < 0) { GABIM(Kartelë); return; }
            단말.Shkrimi("HEX BEGIN "); 단말.수(Memorie_Skedarët.Madhësi(Kartelë)); 단말.문자(10);
            int futje_COUNT = 0;
            while (true) {
                int VALUE = Memorie_Skedarët.Leximi(Kartelë); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++futje_COUNT % 32 == 0) 단말.문자(10);
            }
            if (futje_COUNT % 32 != 0) 단말.문자(10);
            Memorie_Skedarët.Mbyll(Kartelë); 단말.Shkrimi("HEX END\n"); return;
        }
        redaktim_emër_gjatësi = gjatësi_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < redaktim_emër_gjatësi; Loop_INDEX++) redaktim_emër[Loop_INDEX] = kodi_VALUE[시작점[1] + Loop_INDEX];
        단말.Shkrimi("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Madhësi = 0;
        while (true) {
            단말.Shkrimi("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Shkrimi("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && linjë[0] == '.') break;
            int e_përparme_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (linjë[Loop_INDEX] == 32 || linjë[Loop_INDEX] == 9) continue;
                int VALUE = hekzadecimal_VALUE(linjë[Loop_INDEX]);
                if (VALUE < 0 || Madhësi >= 편집내용.length) { 단말.Shkrimi("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (e_përparme_VALUE < 0) e_përparme_VALUE = VALUE; else { 편집내용[Madhësi++] = e_përparme_VALUE * 16 + VALUE; e_përparme_VALUE = -1; }
            }
            if (e_përparme_VALUE >= 0) { 단말.Shkrimi("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memorie_Skedarët.shteg_nis(redaktim_emër_gjatësi);
        for (int Loop_INDEX = 0; Loop_INDEX < redaktim_emër_gjatësi; Loop_INDEX++) Memorie_Skedarët.shteg_bajt(Loop_INDEX, redaktim_emër[Loop_INDEX]);
        int Kartelë = Memorie_Skedarët.Hap(577); if (Kartelë < 0) { GABIM(Kartelë); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Madhësi; Loop_INDEX++) Memorie_Skedarët.Shkrimi(Kartelë, 편집내용[Loop_INDEX]);
        Memorie_Skedarët.Mbyll(Kartelë); 단말.Shkrimi("LOADED "); 단말.수(Madhësi); 단말.Shkrimi("bajt_VALUE(주기억 Kartelë)\n");
    }
    static int Mjete(int INDEX) {
        return vegël_futje(INDEX, 1);
    }
    static int vegël_futje(int INDEX, int Ekzekuto) {
        if (kodi_COUNT - Ekzekuto > 8) return -22;
        panel.인수준비(kodi_COUNT - Ekzekuto);
        for (int 첫값 = Ekzekuto; 첫값 < kodi_COUNT; 첫값++) {
            if (gjatësi_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < gjatësi_VALUE[첫값]; Loop_INDEX++) panel.argument_bajt(첫값 - Ekzekuto, Loop_INDEX, kodi_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? panel.리눅스파일실행() : INDEX < 0 ? panel.zbatoj_përdorues_skedar() : panel.varg_përdorues_program(INDEX);
    }
    static int PYTHON_grupoj() {
        if (kodi_COUNT > 8) return -22;
        panel.인수준비(kodi_COUNT);
        String POZICIONI = "/lib/grupoj.py";
        // Java 문자열을 셸의 UTF-8 Argumente 버퍼에 기록한다.
        int pozicioni_INDEX = 0;
        for (int 순번 = 0; 순번 < POZICIONI.length(); 순번++) {
            int karakter_VALUE = POZICIONI.charAt(순번);
            if (karakter_VALUE < 128) panel.argument_bajt(0, pozicioni_INDEX++, karakter_VALUE);
            else { panel.argument_bajt(0, pozicioni_INDEX++, 0xe0 | (karakter_VALUE >> 12)); panel.argument_bajt(0, pozicioni_INDEX++, 0x80 | ((karakter_VALUE >> 6) & 63)); panel.argument_bajt(0, pozicioni_INDEX++, 0x80 | (karakter_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < kodi_COUNT; 순번++) {
            if (gjatësi_VALUE[순번] > 255) return -36;
            for (int karakter_VALUE = 0; karakter_VALUE < gjatësi_VALUE[순번]; karakter_VALUE++) panel.argument_bajt(순번, karakter_VALUE, kodi_VALUE[시작점[순번] + karakter_VALUE]);
        }
        return panel.varg_përdorues_program(12);
    }
    static int 실행형식() {
        int 처리값 = POZICIONI(0); if (처리값 < 0) return 처리값;
        int Kartelë = Memorie_Skedarët.Hap(0); if (Kartelë < 0) return Kartelë;
        int 첫값 = Memorie_Skedarët.Leximi(Kartelë), bajt_të_dhëna = Memorie_Skedarët.Leximi(Kartelë), kodi_i_karakterit = Memorie_Skedarët.Leximi(Kartelë), 뒷값 = Memorie_Skedarët.Leximi(Kartelë);
        Memorie_Skedarët.Mbyll(Kartelë);
        if (첫값 == 127 && bajt_të_dhëna == 'E' && kodi_i_karakterit == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bajt_të_dhëna == 'K' && kodi_i_karakterit == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumente) {
        panel.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumente.length(); Loop_INDEX++) panel.argument_bajt(0, Loop_INDEX, Argumente.charAt(Loop_INDEX));
        return panel.varg_përdorues_program(INDEX);
    }
    static void SMS_bajt(int Kartelë, int VALUE) { Memorie_Skedarët.Shkrimi(Kartelë, VALUE); }
    static void statik_skedar(String Emër, String Përmbajtje_VALUE) {
        // grupoj 파일명은 ASCII. Kartelë 내용은 UTF-8로 저장한다.
        Memorie_Skedarët.shteg_nis(Emër.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Emër.length(); Loop_INDEX++) Memorie_Skedarët.shteg_bajt(Loop_INDEX, Emër.charAt(Loop_INDEX));
        int Kartelë = Memorie_Skedarët.Hap(193); if (Kartelë < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Përmbajtje_VALUE.length(); Loop_INDEX++) {
            int kodi_i_karakterit = Përmbajtje_VALUE.charAt(Loop_INDEX);
            if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdbff && Loop_INDEX + 1 < Përmbajtje_VALUE.length()) kodi_i_karakterit = 0x10000 + ((kodi_i_karakterit - 0xd800) << 10) + Përmbajtje_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (kodi_i_karakterit < 128) SMS_bajt(Kartelë, kodi_i_karakterit);
            else {
                int 수 = kodi_i_karakterit < 2048 ? 2 : kodi_i_karakterit < 65536 ? 3 : 4;
                SMS_bajt(Kartelë, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kodi_i_karakterit >> (6 * (수 - 1))));
                for (int futje_COUNT = 수 - 1; futje_COUNT > 0; futje_COUNT--) SMS_bajt(Kartelë, 0x80 | ((kodi_i_karakterit >> (6 * (futje_COUNT - 1))) & 63));
            }
        }
        Memorie_Skedarët.Mbyll(Kartelë);
    }
    static void 한글도움말() {
        단말.Shkrimi("F9 / Shift+Space: [EN] ↔ [sq]\n");
        단말.Shkrimi("  [SQ] keyboard; [EN] ASCII\n");
        단말.Shkrimi("  [ → ç\n");
        단말.Shkrimi("  F9: EN ↔ sq | Ctrl+Shift+V: UTF-8\n");
        단말.Shkrimi("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Shkrimi("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Emër) {
        int bajt_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Emër.length(); Loop_INDEX++) { int kodi_i_karakterit = Emër.charAt(Loop_INDEX); if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdfff) return -22; bajt_COUNT += kodi_i_karakterit < 128 ? 1 : kodi_i_karakterit < 2048 ? 2 : 3; }
        int 처리값 = Memorie_Skedarët.shteg_nis(bajt_COUNT); if (처리값 < 0) return 처리값;
        int pozicioni_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Emër.length(); Loop_INDEX++) {
            int kodi_i_karakterit = Emër.charAt(Loop_INDEX);
            if (kodi_i_karakterit < 128) Memorie_Skedarët.shteg_bajt(pozicioni_INDEX++, kodi_i_karakterit);
            else if (kodi_i_karakterit < 2048) { Memorie_Skedarët.shteg_bajt(pozicioni_INDEX++, 0xc0 | (kodi_i_karakterit >> 6)); Memorie_Skedarët.shteg_bajt(pozicioni_INDEX++, 0x80 | (kodi_i_karakterit & 63)); }
            else { Memorie_Skedarët.shteg_bajt(pozicioni_INDEX++, 0xe0 | (kodi_i_karakterit >> 12)); Memorie_Skedarët.shteg_bajt(pozicioni_INDEX++, 0x80 | ((kodi_i_karakterit >> 6) & 63)); Memorie_Skedarët.shteg_bajt(pozicioni_INDEX++, 0x80 | (kodi_i_karakterit & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Emër) {
        int 처리값 = 예제경로(Emër); if (처리값 < 0) return 처리값;
        처리값 = Memorie_Skedarët.Krijo_direktori(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Emër, String të_dhëna) {
        int 처리값 = 예제경로(Emër); if (처리값 < 0) return 처리값;
        int Kartelë = Memorie_Skedarët.Hap(193); if (Kartelë == -17) return 0; if (Kartelë < 0) return Kartelë;
        for (int Loop_INDEX = 0; Loop_INDEX < të_dhëna.length(); Loop_INDEX += 2) {
            처리값 = Memorie_Skedarët.Shkrimi(Kartelë, hekzadecimal_VALUE(të_dhëna.charAt(Loop_INDEX)) * 16 + hekzadecimal_VALUE(të_dhëna.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memorie_Skedarët.Mbyll(Kartelë); return 처리값; }
        }
        return Memorie_Skedarët.Mbyll(Kartelë);
    }
    static void shfaq_ndihmë() {
        sistem_vegël.shfaq_ndihmë();
        단말.Shkrimi("sshd / i_sigurt_pasues start|stop|status: SSH :22 (user, 장치별 fjalëkalim_VALUE)\n");
        단말.Shkrimi("vncd / në_largësi_afishim start|stop|status: VNC :5900 (장치별 fjalëkalim_VALUE)\n");
        단말.Shkrimi("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Shkrimi("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Shkrimi("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Shkrimi("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Shkrimi("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Shkrimi("모서리 + 왼쪽 버튼 zvarrit_VALUE: Terminali Madhësi ndryshoj_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Shkrimi("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Shkrimi("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Shkrimi("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Shkrimi("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Shkrimi("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Shkrimi("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Shkrimi("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Shkrimi("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Shkrimi("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Shkrimi("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Shkrimi("pip: MicroPython burim_degëzim instaloj_VALUE; pritës --network --pip 필요; /lib는 RAM\n");
        단말.Shkrimi("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Shkrimi("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Shkrimi("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Shkrimi("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminali(boolean 전환여부) {
        if (전환여부 && panel.Terminali(2) != 0) { panel.Terminali(0); 단말.Shkrimi("TERMINAL CLOSED\n"); }
        else if (panel.Terminali(1) < 0) GABIM(-19);
        else 단말.Shkrimi("TERMINAL READY — sq terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Komanda() {
        if (kodi_COUNT == 0) return;
        if (sistem_vegël.zbatoj_komandë()) return;
        if (같음(0,"sshd") || 같음(0,"i_sigurt_pasues") || 같음(0,"vncd") || 같음(0,"në_largësi_afishim")) {
            int 종류=같음(0,"vncd")||같음(0,"në_largësi_afishim")?1:0;
            int Veprim=같음(1,"start")||같음(1,"Ekzekuto")?1:같음(1,"stop")||같음(1,"Ndalo")?0:2;
            int status_VALUE=panel.ndjekja_paralele(종류,Veprim);
            if(status_VALUE<0)GABIM(status_VALUE);else 단말.Shkrimi(panel.ndjekja_paralele(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else shfaq_ndihmë(); }
        else if (같음(0, "info") || 같음(0, "i")) bërthamë.msinfo32_exe();
        else if (같음(0, "pwd")) { Memorie_Skedarët.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (kodi_COUNT == 1) { Memorie_Skedarët.shteg_nis(1); 처리값 = Memorie_Skedarët.shteg_bajt(0, '/'); } else 처리값 = kodi_COUNT == 2 ? POZICIONI(1) : -22;
            if (처리값 >= 0) 처리값 = Memorie_Skedarët.ndryshoj_direktori(); if (처리값 < 0) GABIM(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (kodi_COUNT == argument_INDEX) { Memorie_Skedarët.shteg_nis(1); 처리값 = Memorie_Skedarët.shteg_bajt(0, '.'); } else 처리값 = kodi_COUNT == argument_INDEX + 1 ? POZICIONI(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memorie_Skedarët.경로목록(); if (처리값 < 0) GABIM(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) pasues_Mjete.skedar_punë(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) pasues_Mjete.kopjoj_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) pasues_Mjete.Pamja_VALUE();
        else if (같음(0, "wc")) pasues_Mjete.세기();
        else if (같음(0, "grep")) pasues_Mjete.FIND_futje();
        else if (같음(0, "head") || 같음(0, "tail")) pasues_Mjete.머리(같음(0, "tail"));
        else if (같음(0, "tee")) pasues_Mjete.함께쓰기();
        else if (같음(0, "env")) pasues_sintaksë.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (kodi_COUNT == 1) pasues_sintaksë.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < kodi_COUNT; Loop_INDEX++) { int 처리값 = pasues_sintaksë.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { llogaritje = 처리값; 단말.Shkrimi("Komanda analizoj_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) pasues_sintaksë.zbatoj_skedar();
        else if (같음(0, "true")) llogaritje = 0;
        else if (같음(0, "false")) llogaritje = 1;
        else if (같음(0, "history")) linjë_Redaktori.shfaq_LOG();
        else if (같음(0, "exit")) {
            if (pasues_sintaksë.깊이 > 0) { llogaritje = kodi_COUNT == 1 ? pasues_sintaksë.status_VALUE : pasues_Mjete.shifër_VALUE(1); if (llogaritje < 0 || llogaritje > 255) llogaritje = 2; pasues_sintaksë.skript_mbaroj = true; }
            else if (panel.Terminali(2) != 0) Terminali(true);
            else 단말.Shkrimi("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) redaktim_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (kodi_COUNT < 2) { llogaritje = 2; 단말.Shkrimi("사용법: rm Kartelë...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < kodi_COUNT; Loop_INDEX++) { int 처리값 = POZICIONI(Loop_INDEX); if (처리값 == 0) 처리값 = Memorie_Skedarët.spastroj_futje(); if (처리값 < 0) GABIM(처리값); }
        }
        else if (같음(0, "echo")) {
            int nis_pozicioni = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = nis_pozicioni; 첫값 < kodi_COUNT; 첫값++) { if (첫값 > nis_pozicioni) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < gjatësi_VALUE[첫값]; Loop_INDEX++) panel.직렬쓰기(kodi_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (nis_pozicioni == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Shkrimi("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_grupoj() : Mjete(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); llogaritje = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !pasues_sintaksë.연결중) { 단말.Shkrimi("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Mjete(13); llogaritje = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Mjete(15); llogaritje = 처리값 < 0 ? 126 : 처리값; if (!pasues_sintaksë.연결중) { 단말.Shkrimi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Mjete(16); llogaritje = 처리값 < 0 ? 126 : 처리값; if (!pasues_sintaksë.연결중) { 단말.Shkrimi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Madhësi = panel.Terminali(13); 단말.Shkrimi("TERMINAL SIZE "); 단말.수(Madhësi & 65535); 단말.문자('x'); 단말.수(Madhësi >>> 16); 단말.문자(10); }
            else Terminali(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { panel.Terminali(9); desktop.zbatoj_komandë(); }
        else if (같음(0, "c")) bërthamë.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) bërthamë.작업시험();
        else if (같음(0, "g")) bërthamë.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) bërthamë.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = panel.varg_përdorues_program(0); if (처리값 == 0) 단말.Shkrimi("ELF DEMO PASS\n"); else GABIM(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? vegël_futje(-2, 2) : Mjete(-1); llogaritje = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !pasues_sintaksë.연결중) { 단말.Shkrimi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) bërthamë.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = panel.skedar_transferim_shërbim(1); if (처리값 < 0) GABIM(처리값); else { 단말.Shkrimi("FTP listening "); sistem_vegël.shkruaj_email(panel.rrjet_status(0,0)); 단말.Shkrimi(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { panel.skedar_transferim_shërbim(0); 단말.Shkrimi("FTP stopped\n"); }
            else 단말.Shkrimi(panel.skedar_transferim_shërbim(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { grupoj.Përgatit(); 단말.Shkrimi("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Gjuha = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (kodi_COUNT != 2 || Gjuha < 0) 단말.Shkrimi("example java|c|python: 출력, Kartelë, 네트워크, 그래픽, Java Swing Dritare 예제\n");
            else { int 처리값 = 예제꾸러미.instaloj_VALUE(Gjuha); if (처리값 < 0) { GABIM(처리값); if (처리값 == -28) 단말.Shkrimi("RAM full: remove unused files, then retry example\n"); } else 단말.Shkrimi("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = vegël_futje(format_VALUE == 1 ? -1 : 14, 0); llogaritje = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !pasues_sintaksë.연결중) { 단말.Shkrimi("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { llogaritje = 126; 단말.Shkrimi("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { llogaritje = 127; 단말.Shkrimi("Unknown command. help: commands\n"); }
        }
    }
    public static void zbatoj_komandë() {
        grupoj.Përgatit();
        for (int Gjuha = 0; Gjuha < 3; Gjuha++) { int 처리값 = 예제꾸러미.instaloj_VALUE(Gjuha); if (처리값 < 0) GABIM(처리값); }
        shfaq_ndihmë();
        while (true) {
            dritare_sesion.Proces_VALUE_futje(); if (dritare_sesion.재개()) continue;
            if (!dritare_sesion.이어읽기) 단말.Shkrimi("jkoros-native> "); linjë_Redaktori.rreshti_i_komandës = true; panel.në_largësi_Prit(1); int Madhësi = 줄읽기(); panel.në_largësi_Prit(0); linjë_Redaktori.rreshti_i_komandës = false;
            if (Madhësi == -3) continue;
            if (Madhësi == -2) 단말.Shkrimi("Komanda analizoj_VALUE: 명령줄이 너무 깁니다\n");
            if (Madhësi >= 0) { pasues_sintaksë.skript_mbaroj = false; pasues_sintaksë.zbatoj_komandë(linjë, 0, Madhësi, 0); } else pasues_sintaksë.status_VALUE = 130;
            panel.mbaroj_në_largësi_komandë(pasues_sintaksë.status_VALUE);
            linjë_Redaktori.Madhësi = linjë_Redaktori.kursor_VALUE = linjë_Redaktori.nis_dritare = 0;
        }
    }
}
