// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 linya_ng_utos. Quote, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] linya = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], haba_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], edit_pangalan = new int[63];
    static int token_COUNT, edit_pangalan_haba, sukat;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { board.직렬쓰기(VALUE); }
    static int 줄읽기() { return linya_Editor.읽기(); }
    static boolean 나누기(int sukat_82232621) {
        int posisyon = 0, 끝 = 0; token_COUNT = 0;
        while (posisyon < sukat_82232621) {
            while (posisyon < sukat_82232621 && (linya[posisyon] == 32 || linya[posisyon] == 9)) posisyon++;
            if (posisyon == sukat_82232621) break;
            if (token_COUNT == 16) { 단말.sumulat("utos mag_parse_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Quote_VALUE = 0;
            while (posisyon < sukat_82232621) {
                int VALUE = linya[posisyon++];
                if (Quote_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Quote_VALUE) { Quote_VALUE = 0; continue; }
                if (Quote_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Quote_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Quote_VALUE != 0) { 단말.sumulat("utos mag_parse_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            haba_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int posisyon_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int character_code=Word_SMS.charAt(순번);
            if (character_code>=0xd800 && character_code<=0xdbff && 순번+1<Word_SMS.length()) character_code=0x10000+((character_code-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_COUNT=character_code<128?1:character_code<2048?2:character_code<65536?3:4;
            for (int SEQUENCE_VALUE=byte_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=byte_COUNT==1?character_code:SEQUENCE_VALUE==byte_COUNT-1?(byte_COUNT==2?0xc0:byte_COUNT==3?0xe0:0xf0)|(character_code>>(6*SEQUENCE_VALUE)):0x80|((character_code>>(6*SEQUENCE_VALUE))&63);
                if (posisyon_INDEX>=haba_VALUE[INDEX] || token_VALUE[시작점[INDEX]+posisyon_INDEX++]!=VALUE) return false;
            }
        }
        return posisyon_INDEX==haba_VALUE[INDEX];
    }
    static int path(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int sukat = Memory_Mga_File.path_Start(haba_VALUE[INDEX]); if (sukat < 0) return sukat;
        for (int Loop_INDEX = 0; Loop_INDEX < haba_VALUE[INDEX]; Loop_INDEX++) {
            sukat = Memory_Mga_File.path_byte(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (sukat < 0) return sukat;
        }
        return 0;
    }
    static void error(int INDEX) { sukat = 1; 단말.sumulat("error "); 단말.수(INDEX); 단말.문자(10); }
    static void View_VALUE() {
        if (token_COUNT != 2) { 단말.sumulat("사용법: cat file\n"); return; }
        int sukat = path(1); if (sukat < 0) { error(sukat); return; }
        int file = Memory_Mga_File.buksan(0); if (file < 0) { error(file); return; }
        while (true) { int VALUE = Memory_Mga_File.읽기(file); if (VALUE == 256) break; if (VALUE < 0) { error(VALUE); break; } 원바이트(VALUE); }
        Memory_Mga_File.isara(file); 단말.문자(10);
    }
    static void edit_VALUE() {
        if (token_COUNT != 2) { 단말.sumulat("사용법: edit file\n"); return; }
        int sukat = path(1); if (sukat < 0) { error(sukat); return; }
        edit_pangalan_haba = haba_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < edit_pangalan_haba; Loop_INDEX++) edit_pangalan[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.sumulat("EDIT: file 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int sukat_82232621 = 0;
        while (true) {
            단말.sumulat("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.sumulat("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && linya[0] == '.') break;
            if (입력 + 1 > 편집내용.length - sukat_82232621) { 단말.sumulat("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[sukat_82232621++] = linya[Loop_INDEX];
            편집내용[sukat_82232621++] = 10;
        }
        Memory_Mga_File.path_Start(edit_pangalan_haba);
        for (int Loop_INDEX = 0; Loop_INDEX < edit_pangalan_haba; Loop_INDEX++) Memory_Mga_File.path_byte(Loop_INDEX, edit_pangalan[Loop_INDEX]);
        int file = Memory_Mga_File.buksan(577); if (file < 0) { error(file); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < sukat_82232621; Loop_INDEX++) Memory_Mga_File.sumulat(file, 편집내용[Loop_INDEX]);
        Memory_Mga_File.isara(file); 단말.sumulat("SAVED "); 단말.수(sukat_82232621); 단말.sumulat("byte_VALUE(주기억 file)\n");
    }
    static int hex_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.sumulat("사용법: load file | hex file\n"); return; }
        int sukat = path(1); if (sukat < 0) { error(sukat); return; }
        if (!넣기) {
            int file = Memory_Mga_File.buksan(0); if (file < 0) { error(file); return; }
            단말.sumulat("HEX BEGIN "); 단말.수(Memory_Mga_File.sukat_82232621(file)); 단말.문자(10);
            int pagpasok_COUNT = 0;
            while (true) {
                int VALUE = Memory_Mga_File.읽기(file); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++pagpasok_COUNT % 32 == 0) 단말.문자(10);
            }
            if (pagpasok_COUNT % 32 != 0) 단말.문자(10);
            Memory_Mga_File.isara(file); 단말.sumulat("HEX END\n"); return;
        }
        edit_pangalan_haba = haba_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < edit_pangalan_haba; Loop_INDEX++) edit_pangalan[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.sumulat("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int sukat_82232621 = 0;
        while (true) {
            단말.sumulat("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.sumulat("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && linya[0] == '.') break;
            int nasa_harap_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (linya[Loop_INDEX] == 32 || linya[Loop_INDEX] == 9) continue;
                int VALUE = hex_VALUE(linya[Loop_INDEX]);
                if (VALUE < 0 || sukat_82232621 >= 편집내용.length) { 단말.sumulat("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (nasa_harap_VALUE < 0) nasa_harap_VALUE = VALUE; else { 편집내용[sukat_82232621++] = nasa_harap_VALUE * 16 + VALUE; nasa_harap_VALUE = -1; }
            }
            if (nasa_harap_VALUE >= 0) { 단말.sumulat("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memory_Mga_File.path_Start(edit_pangalan_haba);
        for (int Loop_INDEX = 0; Loop_INDEX < edit_pangalan_haba; Loop_INDEX++) Memory_Mga_File.path_byte(Loop_INDEX, edit_pangalan[Loop_INDEX]);
        int file = Memory_Mga_File.buksan(577); if (file < 0) { error(file); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < sukat_82232621; Loop_INDEX++) Memory_Mga_File.sumulat(file, 편집내용[Loop_INDEX]);
        Memory_Mga_File.isara(file); 단말.sumulat("LOADED "); 단말.수(sukat_82232621); 단말.sumulat("byte_VALUE(주기억 file)\n");
    }
    static int Mga_Tool(int INDEX) {
        return tool_pagpasok(INDEX, 1);
    }
    static int tool_pagpasok(int INDEX, int run) {
        if (token_COUNT - run > 8) return -22;
        board.인수준비(token_COUNT - run);
        for (int 첫값 = run; 첫값 < token_COUNT; 첫값++) {
            if (haba_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < haba_VALUE[첫값]; Loop_INDEX++) board.argumento_byte(첫값 - run, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? board.리눅스파일실행() : INDEX < 0 ? board.Mag_execute_gumagamit_file() : board.run_gumagamit_app(INDEX);
    }
    static int PYTHON_bundle() {
        if (token_COUNT > 8) return -22;
        board.인수준비(token_COUNT);
        String path = "/lib/bundle.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int posisyon_INDEX = 0;
        for (int 순번 = 0; 순번 < path.length(); 순번++) {
            int karakter_VALUE = path.charAt(순번);
            if (karakter_VALUE < 128) board.argumento_byte(0, posisyon_INDEX++, karakter_VALUE);
            else { board.argumento_byte(0, posisyon_INDEX++, 0xe0 | (karakter_VALUE >> 12)); board.argumento_byte(0, posisyon_INDEX++, 0x80 | ((karakter_VALUE >> 6) & 63)); board.argumento_byte(0, posisyon_INDEX++, 0x80 | (karakter_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (haba_VALUE[순번] > 255) return -36;
            for (int karakter_VALUE = 0; karakter_VALUE < haba_VALUE[순번]; karakter_VALUE++) board.argumento_byte(순번, karakter_VALUE, token_VALUE[시작점[순번] + karakter_VALUE]);
        }
        return board.run_gumagamit_app(12);
    }
    static int 실행형식() {
        int 처리값 = path(0); if (처리값 < 0) return 처리값;
        int file = Memory_Mga_File.buksan(0); if (file < 0) return file;
        int 첫값 = Memory_Mga_File.읽기(file), byte_data = Memory_Mga_File.읽기(file), character_code = Memory_Mga_File.읽기(file), 뒷값 = Memory_Mga_File.읽기(file);
        Memory_Mga_File.isara(file);
        if (첫값 == 127 && byte_data == 'E' && character_code == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_data == 'K' && character_code == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        board.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) board.argumento_byte(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return board.run_gumagamit_app(INDEX);
    }
    static void SMS_byte(int file, int VALUE) { Memory_Mga_File.sumulat(file, VALUE); }
    static void hindi_nababago_file(String pangalan, String Nilalaman_VALUE) {
        // bundle 파일명은 ASCII. file 내용은 UTF-8로 저장한다.
        Memory_Mga_File.path_Start(pangalan.length());
        for (int Loop_INDEX = 0; Loop_INDEX < pangalan.length(); Loop_INDEX++) Memory_Mga_File.path_byte(Loop_INDEX, pangalan.charAt(Loop_INDEX));
        int file = Memory_Mga_File.buksan(193); if (file < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Nilalaman_VALUE.length(); Loop_INDEX++) {
            int character_code = Nilalaman_VALUE.charAt(Loop_INDEX);
            if (character_code >= 0xd800 && character_code <= 0xdbff && Loop_INDEX + 1 < Nilalaman_VALUE.length()) character_code = 0x10000 + ((character_code - 0xd800) << 10) + Nilalaman_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (character_code < 128) SMS_byte(file, character_code);
            else {
                int 수 = character_code < 2048 ? 2 : character_code < 65536 ? 3 : 4;
                SMS_byte(file, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (character_code >> (6 * (수 - 1))));
                for (int pagpasok_COUNT = 수 - 1; pagpasok_COUNT > 0; pagpasok_COUNT--) SMS_byte(file, 0x80 | ((character_code >> (6 * (pagpasok_COUNT - 1))) & 63));
            }
        }
        Memory_Mga_File.isara(file);
    }
    static void 한글도움말() {
        단말.sumulat("F9 / Shift+Space: [EN] ↔ [fil]\n");
        단말.sumulat("  [FIL] keyboard; [EN] ASCII\n");
        단말.sumulat("  a → a\n");
        단말.sumulat("  F9: EN ↔ fil | Ctrl+Shift+V: UTF-8\n");
        단말.sumulat("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.sumulat("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String pangalan) {
        int byte_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < pangalan.length(); Loop_INDEX++) { int character_code = pangalan.charAt(Loop_INDEX); if (character_code >= 0xd800 && character_code <= 0xdfff) return -22; byte_COUNT += character_code < 128 ? 1 : character_code < 2048 ? 2 : 3; }
        int 처리값 = Memory_Mga_File.path_Start(byte_COUNT); if (처리값 < 0) return 처리값;
        int posisyon_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < pangalan.length(); Loop_INDEX++) {
            int character_code = pangalan.charAt(Loop_INDEX);
            if (character_code < 128) Memory_Mga_File.path_byte(posisyon_INDEX++, character_code);
            else if (character_code < 2048) { Memory_Mga_File.path_byte(posisyon_INDEX++, 0xc0 | (character_code >> 6)); Memory_Mga_File.path_byte(posisyon_INDEX++, 0x80 | (character_code & 63)); }
            else { Memory_Mga_File.path_byte(posisyon_INDEX++, 0xe0 | (character_code >> 12)); Memory_Mga_File.path_byte(posisyon_INDEX++, 0x80 | ((character_code >> 6) & 63)); Memory_Mga_File.path_byte(posisyon_INDEX++, 0x80 | (character_code & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String pangalan) {
        int 처리값 = 예제경로(pangalan); if (처리값 < 0) return 처리값;
        처리값 = Memory_Mga_File.Create_Directory(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String pangalan, String data) {
        int 처리값 = 예제경로(pangalan); if (처리값 < 0) return 처리값;
        int file = Memory_Mga_File.buksan(193); if (file == -17) return 0; if (file < 0) return file;
        for (int Loop_INDEX = 0; Loop_INDEX < data.length(); Loop_INDEX += 2) {
            처리값 = Memory_Mga_File.sumulat(file, hex_VALUE(data.charAt(Loop_INDEX)) * 16 + hex_VALUE(data.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memory_Mga_File.isara(file); return 처리값; }
        }
        return Memory_Mga_File.isara(file);
    }
    static void ipakita_tulong() {
        system_tool.ipakita_tulong();
        단말.sumulat("sshd / secure_shell start|stop|status: SSH :22 (user, 장치별 password_VALUE)\n");
        단말.sumulat("vncd / malayuan_display start|stop|status: VNC :5900 (장치별 password_VALUE)\n");
        단말.sumulat("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.sumulat("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.sumulat("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.sumulat("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.sumulat("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.sumulat("모서리 + 왼쪽 버튼 mag_drag_VALUE: Terminal sukat_82232621 baguhin_VALUE; terminal size: kolum_VALUE/ROW_VALUE\n");
        단말.sumulat("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.sumulat("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.sumulat("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.sumulat("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.sumulat("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.sumulat("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.sumulat("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.sumulat("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.sumulat("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.sumulat("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.sumulat("pip: MicroPython pinagmulan_balangkas i_install_VALUE; host --network --pip 필요; /lib는 RAM\n");
        단말.sumulat("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.sumulat("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.sumulat("/example/java /example/c /example/python: examples ready at boot\n");
        단말.sumulat("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && board.Terminal(2) != 0) { board.Terminal(0); 단말.sumulat("TERMINAL CLOSED\n"); }
        else if (board.Terminal(1) < 0) error(-19);
        else 단말.sumulat("TERMINAL READY — fil terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void utos() {
        if (token_COUNT == 0) return;
        if (system_tool.Mag_execute_utos()) return;
        if (같음(0,"sshd") || 같음(0,"secure_shell") || 같음(0,"vncd") || 같음(0,"malayuan_display")) {
            int 종류=같음(0,"vncd")||같음(0,"malayuan_display")?1:0;
            int aksyon=같음(1,"start")||같음(1,"run")?1:같음(1,"stop")||같음(1,"Hinto")?0:2;
            int katayuan_VALUE=board.pag_shadow(종류,aksyon);
            if(katayuan_VALUE<0)error(katayuan_VALUE);else 단말.sumulat(board.pag_shadow(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else ipakita_tulong(); }
        else if (같음(0, "info") || 같음(0, "i")) kernel.msinfo32_exe();
        else if (같음(0, "pwd")) { Memory_Mga_File.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Memory_Mga_File.path_Start(1); 처리값 = Memory_Mga_File.path_byte(0, '/'); } else 처리값 = token_COUNT == 2 ? path(1) : -22;
            if (처리값 >= 0) 처리값 = Memory_Mga_File.baguhin_Directory(); if (처리값 < 0) error(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argumento_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argumento_INDEX) { Memory_Mga_File.path_Start(1); 처리값 = Memory_Mga_File.path_byte(0, '.'); } else 처리값 = token_COUNT == argumento_INDEX + 1 ? path(argumento_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memory_Mga_File.경로목록(); if (처리값 < 0) error(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) shell_Mga_Tool.file_kaso(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) shell_Mga_Tool.gumawa_ng_kopya_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) shell_Mga_Tool.View_VALUE();
        else if (같음(0, "wc")) shell_Mga_Tool.세기();
        else if (같음(0, "grep")) shell_Mga_Tool.FIND_pagpasok();
        else if (같음(0, "head") || 같음(0, "tail")) shell_Mga_Tool.머리(같음(0, "tail"));
        else if (같음(0, "tee")) shell_Mga_Tool.함께쓰기();
        else if (같음(0, "env")) shell_syntax.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) shell_syntax.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = shell_syntax.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { sukat = 처리값; 단말.sumulat("utos mag_parse_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) shell_syntax.Mag_execute_file();
        else if (같음(0, "true")) sukat = 0;
        else if (같음(0, "false")) sukat = 1;
        else if (같음(0, "history")) linya_Editor.ipakita_LOG();
        else if (같음(0, "exit")) {
            if (shell_syntax.깊이 > 0) { sukat = token_COUNT == 1 ? shell_syntax.katayuan_VALUE : shell_Mga_Tool.digit_VALUE(1); if (sukat < 0 || sukat > 255) sukat = 2; shell_syntax.script_tapusin = true; }
            else if (board.Terminal(2) != 0) Terminal(true);
            else 단말.sumulat("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) edit_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { sukat = 2; 단말.sumulat("사용법: rm file...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = path(Loop_INDEX); if (처리값 == 0) 처리값 = Memory_Mga_File.burahin_pagpasok(); if (처리값 < 0) error(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_posisyon = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_posisyon; 첫값 < token_COUNT; 첫값++) { if (첫값 > Start_posisyon) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < haba_VALUE[첫값]; Loop_INDEX++) board.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Start_posisyon == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.sumulat("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_bundle() : Mga_Tool(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); sukat = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !shell_syntax.연결중) { 단말.sumulat("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Mga_Tool(13); sukat = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Mga_Tool(15); sukat = 처리값 < 0 ? 126 : 처리값; if (!shell_syntax.연결중) { 단말.sumulat("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Mga_Tool(16); sukat = 처리값 < 0 ? 126 : 처리값; if (!shell_syntax.연결중) { 단말.sumulat("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int sukat_82232621 = board.Terminal(13); 단말.sumulat("TERMINAL SIZE "); 단말.수(sukat_82232621 & 65535); 단말.문자('x'); 단말.수(sukat_82232621 >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { board.Terminal(9); desktop.Mag_execute_utos(); }
        else if (같음(0, "c")) kernel.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kernel.작업시험();
        else if (같음(0, "g")) kernel.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kernel.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = board.run_gumagamit_app(0); if (처리값 == 0) 단말.sumulat("ELF DEMO PASS\n"); else error(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? tool_pagpasok(-2, 2) : Mga_Tool(-1); sukat = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !shell_syntax.연결중) { 단말.sumulat("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kernel.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = board.file_lipat_serbisyo(1); if (처리값 < 0) error(처리값); else { 단말.sumulat("FTP listening "); system_tool.sumulat_email(board.Network_katayuan(0,0)); 단말.sumulat(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { board.file_lipat_serbisyo(0); 단말.sumulat("FTP stopped\n"); }
            else 단말.sumulat(board.file_lipat_serbisyo(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { bundle.Ihanda(); 단말.sumulat("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Wika = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Wika < 0) 단말.sumulat("example java|c|python: 출력, file, 네트워크, 그래픽, Java Swing window 예제\n");
            else { int 처리값 = 예제꾸러미.i_install_VALUE(Wika); if (처리값 < 0) { error(처리값); if (처리값 == -28) 단말.sumulat("RAM full: remove unused files, then retry example\n"); } else 단말.sumulat("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = tool_pagpasok(format_VALUE == 1 ? -1 : 14, 0); sukat = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !shell_syntax.연결중) { 단말.sumulat("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { sukat = 126; 단말.sumulat("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { sukat = 127; 단말.sumulat("Unknown command. help: commands\n"); }
        }
    }
    public static void Mag_execute_utos() {
        bundle.Ihanda();
        for (int Wika = 0; Wika < 3; Wika++) { int 처리값 = 예제꾸러미.i_install_VALUE(Wika); if (처리값 < 0) error(처리값); }
        ipakita_tulong();
        while (true) {
            window_sesyon.Proseso_VALUE_pagpasok(); if (window_sesyon.재개()) continue;
            if (!window_sesyon.이어읽기) 단말.sumulat("jkoros-native> "); linya_Editor.linya_ng_utos = true; board.malayuan_maghintay(1); int sukat_82232621 = 줄읽기(); board.malayuan_maghintay(0); linya_Editor.linya_ng_utos = false;
            if (sukat_82232621 == -3) continue;
            if (sukat_82232621 == -2) 단말.sumulat("utos mag_parse_VALUE: 명령줄이 너무 깁니다\n");
            if (sukat_82232621 >= 0) { shell_syntax.script_tapusin = false; shell_syntax.Mag_execute_utos(linya, 0, sukat_82232621, 0); } else shell_syntax.katayuan_VALUE = 130;
            board.tapusin_malayuan_utos(shell_syntax.katayuan_VALUE);
            linya_Editor.sukat_82232621 = linya_Editor.kursor_VALUE = linya_Editor.Start_window = 0;
        }
    }
}
