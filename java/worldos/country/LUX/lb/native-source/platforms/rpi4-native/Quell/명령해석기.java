// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 Befeelszeil. Zitat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Zeil = new int[4096], Token_VALUE = new int[4096], 시작점 = new int[32], Längt_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], Editéieren_Numm = new int[63];
    static int Token_COUNT, Editéieren_Numm_Längt, Mooss;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Board.직렬쓰기(VALUE); }
    static int 줄읽기() { return Zeil_Editeur.읽기(); }
    static boolean 나누기(int d_Gréisst_veränneren) {
        int positionéieren = 0, 끝 = 0; Token_COUNT = 0;
        while (positionéieren < d_Gréisst_veränneren) {
            while (positionéieren < d_Gréisst_veränneren && (Zeil[positionéieren] == 32 || Zeil[positionéieren] == 9)) positionéieren++;
            if (positionéieren == d_Gréisst_veränneren) break;
            if (Token_COUNT == 16) { 단말.schreiwen("Befeel analyséieren_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[Token_COUNT] = 끝; int Zitat_VALUE = 0;
            while (positionéieren < d_Gréisst_veränneren) {
                int VALUE = Zeil[positionéieren++];
                if (Zitat_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Zitat_VALUE) { Zitat_VALUE = 0; continue; }
                if (Zitat_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Zitat_VALUE = VALUE; continue; }
                Token_VALUE[끝++] = VALUE;
            }
            if (Zitat_VALUE != 0) { 단말.schreiwen("Befeel analyséieren_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            Längt_VALUE[Token_COUNT] = 끝 - 시작점[Token_COUNT]; Token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= Token_COUNT) return false;
        int positionéieren_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int Zeechecode=Word_SMS.charAt(순번);
            if (Zeechecode>=0xd800 && Zeechecode<=0xdbff && 순번+1<Word_SMS.length()) Zeechecode=0x10000+((Zeechecode-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int Byte_COUNT=Zeechecode<128?1:Zeechecode<2048?2:Zeechecode<65536?3:4;
            for (int SEQUENCE_VALUE=Byte_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=Byte_COUNT==1?Zeechecode:SEQUENCE_VALUE==Byte_COUNT-1?(Byte_COUNT==2?0xc0:Byte_COUNT==3?0xe0:0xf0)|(Zeechecode>>(6*SEQUENCE_VALUE)):0x80|((Zeechecode>>(6*SEQUENCE_VALUE))&63);
                if (positionéieren_INDEX>=Längt_VALUE[INDEX] || Token_VALUE[시작점[INDEX]+positionéieren_INDEX++]!=VALUE) return false;
            }
        }
        return positionéieren_INDEX==Längt_VALUE[INDEX];
    }
    static int Wee(int INDEX) {
        if (INDEX >= Token_COUNT) return -22;
        int Mooss = Späicher_Fichieren.Wee_Start(Längt_VALUE[INDEX]); if (Mooss < 0) return Mooss;
        for (int Loop_INDEX = 0; Loop_INDEX < Längt_VALUE[INDEX]; Loop_INDEX++) {
            Mooss = Späicher_Fichieren.Wee_Byte(Loop_INDEX, Token_VALUE[시작점[INDEX] + Loop_INDEX]); if (Mooss < 0) return Mooss;
        }
        return 0;
    }
    static void Feeler(int INDEX) { Mooss = 1; 단말.schreiwen("Feeler "); 단말.수(INDEX); 단말.문자(10); }
    static void Vue_VALUE() {
        if (Token_COUNT != 2) { 단말.schreiwen("사용법: cat Fichier\n"); return; }
        int Mooss = Wee(1); if (Mooss < 0) { Feeler(Mooss); return; }
        int Fichier = Späicher_Fichieren.ariichten(0); if (Fichier < 0) { Feeler(Fichier); return; }
        while (true) { int VALUE = Späicher_Fichieren.읽기(Fichier); if (VALUE == 256) break; if (VALUE < 0) { Feeler(VALUE); break; } 원바이트(VALUE); }
        Späicher_Fichieren.Clôture(Fichier); 단말.문자(10);
    }
    static void Editéieren_VALUE() {
        if (Token_COUNT != 2) { 단말.schreiwen("사용법: edit Fichier\n"); return; }
        int Mooss = Wee(1); if (Mooss < 0) { Feeler(Mooss); return; }
        Editéieren_Numm_Längt = Längt_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < Editéieren_Numm_Längt; Loop_INDEX++) Editéieren_Numm[Loop_INDEX] = Token_VALUE[시작점[1] + Loop_INDEX];
        단말.schreiwen("EDIT: Fichier 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int d_Gréisst_veränneren = 0;
        while (true) {
            단말.schreiwen("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.schreiwen("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Zeil[0] == '.') break;
            if (입력 + 1 > 편집내용.length - d_Gréisst_veränneren) { 단말.schreiwen("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[d_Gréisst_veränneren++] = Zeil[Loop_INDEX];
            편집내용[d_Gréisst_veränneren++] = 10;
        }
        Späicher_Fichieren.Wee_Start(Editéieren_Numm_Längt);
        for (int Loop_INDEX = 0; Loop_INDEX < Editéieren_Numm_Längt; Loop_INDEX++) Späicher_Fichieren.Wee_Byte(Loop_INDEX, Editéieren_Numm[Loop_INDEX]);
        int Fichier = Späicher_Fichieren.ariichten(577); if (Fichier < 0) { Feeler(Fichier); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) Späicher_Fichieren.schreiwen(Fichier, 편집내용[Loop_INDEX]);
        Späicher_Fichieren.Clôture(Fichier); 단말.schreiwen("SAVED "); 단말.수(d_Gréisst_veränneren); 단말.schreiwen("Byte_VALUE(주기억 Fichier)\n");
    }
    static int hex_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (Token_COUNT != 2) { 단말.schreiwen("사용법: load Fichier | hex Fichier\n"); return; }
        int Mooss = Wee(1); if (Mooss < 0) { Feeler(Mooss); return; }
        if (!넣기) {
            int Fichier = Späicher_Fichieren.ariichten(0); if (Fichier < 0) { Feeler(Fichier); return; }
            단말.schreiwen("HEX BEGIN "); 단말.수(Späicher_Fichieren.d_Gréisst_veränneren(Fichier)); 단말.문자(10);
            int Agab_COUNT = 0;
            while (true) {
                int VALUE = Späicher_Fichieren.읽기(Fichier); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++Agab_COUNT % 32 == 0) 단말.문자(10);
            }
            if (Agab_COUNT % 32 != 0) 단말.문자(10);
            Späicher_Fichieren.Clôture(Fichier); 단말.schreiwen("HEX END\n"); return;
        }
        Editéieren_Numm_Längt = Längt_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < Editéieren_Numm_Längt; Loop_INDEX++) Editéieren_Numm[Loop_INDEX] = Token_VALUE[시작점[1] + Loop_INDEX];
        단말.schreiwen("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int d_Gréisst_veränneren = 0;
        while (true) {
            단말.schreiwen("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.schreiwen("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Zeil[0] == '.') break;
            int 앞 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Zeil[Loop_INDEX] == 32 || Zeil[Loop_INDEX] == 9) continue;
                int VALUE = hex_VALUE(Zeil[Loop_INDEX]);
                if (VALUE < 0 || d_Gréisst_veränneren >= 편집내용.length) { 단말.schreiwen("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = VALUE; else { 편집내용[d_Gréisst_veränneren++] = 앞 * 16 + VALUE; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.schreiwen("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Späicher_Fichieren.Wee_Start(Editéieren_Numm_Längt);
        for (int Loop_INDEX = 0; Loop_INDEX < Editéieren_Numm_Längt; Loop_INDEX++) Späicher_Fichieren.Wee_Byte(Loop_INDEX, Editéieren_Numm[Loop_INDEX]);
        int Fichier = Späicher_Fichieren.ariichten(577); if (Fichier < 0) { Feeler(Fichier); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) Späicher_Fichieren.schreiwen(Fichier, 편집내용[Loop_INDEX]);
        Späicher_Fichieren.Clôture(Fichier); 단말.schreiwen("LOADED "); 단말.수(d_Gréisst_veränneren); 단말.schreiwen("Byte_VALUE(주기억 Fichier)\n");
    }
    static int Tools(int INDEX) {
        return Tool_Agab(INDEX, 1);
    }
    static int Tool_Agab(int INDEX, int Laf) {
        if (Token_COUNT - Laf > 8) return -22;
        Board.인수준비(Token_COUNT - Laf);
        for (int 첫값 = Laf; 첫값 < Token_COUNT; 첫값++) {
            if (Längt_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < Längt_VALUE[첫값]; Loop_INDEX++) Board.Argument_Byte(첫값 - Laf, Loop_INDEX, Token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Board.리눅스파일실행() : INDEX < 0 ? Board.ausféieren_Benotzer_Fichier() : Board.Laf_Benotzer_App(INDEX);
    }
    static int PYTHON_Bëndel() {
        if (Token_COUNT > 8) return -22;
        Board.인수준비(Token_COUNT);
        String Wee = "/lib/Bëndel.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int positionéieren_INDEX = 0;
        for (int 순번 = 0; 순번 < Wee.length(); 순번++) {
            int Zeechen_VALUE = Wee.charAt(순번);
            if (Zeechen_VALUE < 128) Board.Argument_Byte(0, positionéieren_INDEX++, Zeechen_VALUE);
            else { Board.Argument_Byte(0, positionéieren_INDEX++, 0xe0 | (Zeechen_VALUE >> 12)); Board.Argument_Byte(0, positionéieren_INDEX++, 0x80 | ((Zeechen_VALUE >> 6) & 63)); Board.Argument_Byte(0, positionéieren_INDEX++, 0x80 | (Zeechen_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < Token_COUNT; 순번++) {
            if (Längt_VALUE[순번] > 255) return -36;
            for (int Zeechen_VALUE = 0; Zeechen_VALUE < Längt_VALUE[순번]; Zeechen_VALUE++) Board.Argument_Byte(순번, Zeechen_VALUE, Token_VALUE[시작점[순번] + Zeechen_VALUE]);
        }
        return Board.Laf_Benotzer_App(12);
    }
    static int 실행형식() {
        int 처리값 = Wee(0); if (처리값 < 0) return 처리값;
        int Fichier = Späicher_Fichieren.ariichten(0); if (Fichier < 0) return Fichier;
        int 첫값 = Späicher_Fichieren.읽기(Fichier), Byte_Daten = Späicher_Fichieren.읽기(Fichier), Zeechecode = Späicher_Fichieren.읽기(Fichier), 뒷값 = Späicher_Fichieren.읽기(Fichier);
        Späicher_Fichieren.Clôture(Fichier);
        if (첫값 == 127 && Byte_Daten == 'E' && Zeechecode == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && Byte_Daten == 'K' && Zeechecode == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        Board.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) Board.Argument_Byte(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return Board.Laf_Benotzer_App(INDEX);
    }
    static void SMS_Byte(int Fichier, int VALUE) { Späicher_Fichieren.schreiwen(Fichier, VALUE); }
    static void statesch_Fichier(String Numm, String Inhalt_VALUE) {
        // Bëndel 파일명은 ASCII. Fichier 내용은 UTF-8로 저장한다.
        Späicher_Fichieren.Wee_Start(Numm.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Numm.length(); Loop_INDEX++) Späicher_Fichieren.Wee_Byte(Loop_INDEX, Numm.charAt(Loop_INDEX));
        int Fichier = Späicher_Fichieren.ariichten(193); if (Fichier < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Inhalt_VALUE.length(); Loop_INDEX++) {
            int Zeechecode = Inhalt_VALUE.charAt(Loop_INDEX);
            if (Zeechecode >= 0xd800 && Zeechecode <= 0xdbff && Loop_INDEX + 1 < Inhalt_VALUE.length()) Zeechecode = 0x10000 + ((Zeechecode - 0xd800) << 10) + Inhalt_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (Zeechecode < 128) SMS_Byte(Fichier, Zeechecode);
            else {
                int 수 = Zeechecode < 2048 ? 2 : Zeechecode < 65536 ? 3 : 4;
                SMS_Byte(Fichier, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (Zeechecode >> (6 * (수 - 1))));
                for (int Agab_COUNT = 수 - 1; Agab_COUNT > 0; Agab_COUNT--) SMS_Byte(Fichier, 0x80 | ((Zeechecode >> (6 * (Agab_COUNT - 1))) & 63));
            }
        }
        Späicher_Fichieren.Clôture(Fichier);
    }
    static void 한글도움말() {
        단말.schreiwen("F9 / Shift+Space: [EN] ↔ [lb]\n");
        단말.schreiwen("  [LB] keyboard; [EN] ASCII\n");
        단말.schreiwen("  a → a\n");
        단말.schreiwen("  F9: EN ↔ lb | Ctrl+Shift+V: UTF-8\n");
        단말.schreiwen("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.schreiwen("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Numm) {
        int Byte_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Numm.length(); Loop_INDEX++) { int Zeechecode = Numm.charAt(Loop_INDEX); if (Zeechecode >= 0xd800 && Zeechecode <= 0xdfff) return -22; Byte_COUNT += Zeechecode < 128 ? 1 : Zeechecode < 2048 ? 2 : 3; }
        int 처리값 = Späicher_Fichieren.Wee_Start(Byte_COUNT); if (처리값 < 0) return 처리값;
        int positionéieren_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Numm.length(); Loop_INDEX++) {
            int Zeechecode = Numm.charAt(Loop_INDEX);
            if (Zeechecode < 128) Späicher_Fichieren.Wee_Byte(positionéieren_INDEX++, Zeechecode);
            else if (Zeechecode < 2048) { Späicher_Fichieren.Wee_Byte(positionéieren_INDEX++, 0xc0 | (Zeechecode >> 6)); Späicher_Fichieren.Wee_Byte(positionéieren_INDEX++, 0x80 | (Zeechecode & 63)); }
            else { Späicher_Fichieren.Wee_Byte(positionéieren_INDEX++, 0xe0 | (Zeechecode >> 12)); Späicher_Fichieren.Wee_Byte(positionéieren_INDEX++, 0x80 | ((Zeechecode >> 6) & 63)); Späicher_Fichieren.Wee_Byte(positionéieren_INDEX++, 0x80 | (Zeechecode & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Numm) {
        int 처리값 = 예제경로(Numm); if (처리값 < 0) return 처리값;
        처리값 = Späicher_Fichieren.Create_Verzeechnes(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Numm, String Daten) {
        int 처리값 = 예제경로(Numm); if (처리값 < 0) return 처리값;
        int Fichier = Späicher_Fichieren.ariichten(193); if (Fichier == -17) return 0; if (Fichier < 0) return Fichier;
        for (int Loop_INDEX = 0; Loop_INDEX < Daten.length(); Loop_INDEX += 2) {
            처리값 = Späicher_Fichieren.schreiwen(Fichier, hex_VALUE(Daten.charAt(Loop_INDEX)) * 16 + hex_VALUE(Daten.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Späicher_Fichieren.Clôture(Fichier); return 처리값; }
        }
        return Späicher_Fichieren.Clôture(Fichier);
    }
    static void Show_Hëllef() {
        System_Tool.Show_Hëllef();
        단말.schreiwen("sshd / sécher_Shell start|stop|status: SSH :22 (user, 장치별 Passwuert_VALUE)\n");
        단말.schreiwen("vncd / extern_Bildschierm start|stop|status: VNC :5900 (장치별 Passwuert_VALUE)\n");
        단말.schreiwen("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.schreiwen("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.schreiwen("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.schreiwen("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.schreiwen("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.schreiwen("모서리 + 왼쪽 버튼 eriwwerzéien_VALUE: Terminal d_Gréisst_veränneren änneren_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.schreiwen("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.schreiwen("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.schreiwen("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.schreiwen("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.schreiwen("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.schreiwen("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.schreiwen("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.schreiwen("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.schreiwen("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.schreiwen("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.schreiwen("pip: MicroPython Quell_Bamstruktur installéieren_VALUE; Host --network --pip 필요; /lib는 RAM\n");
        단말.schreiwen("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.schreiwen("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.schreiwen("/example/java /example/c /example/python: examples ready at boot\n");
        단말.schreiwen("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Board.Terminal(2) != 0) { Board.Terminal(0); 단말.schreiwen("TERMINAL CLOSED\n"); }
        else if (Board.Terminal(1) < 0) Feeler(-19);
        else 단말.schreiwen("TERMINAL READY — lb terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Befeel() {
        if (Token_COUNT == 0) return;
        if (System_Tool.ausféieren_Befeel()) return;
        if (같음(0,"sshd") || 같음(0,"sécher_Shell") || 같음(0,"vncd") || 같음(0,"extern_Bildschierm")) {
            int 종류=같음(0,"vncd")||같음(0,"extern_Bildschierm")?1:0;
            int Aktioun=같음(1,"start")||같음(1,"Laf")?1:같음(1,"stop")||같음(1,"Stoppen")?0:2;
            int Status_VALUE=Board.Shadowing(종류,Aktioun);
            if(Status_VALUE<0)Feeler(Status_VALUE);else 단말.schreiwen(Board.Shadowing(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else Show_Hëllef(); }
        else if (같음(0, "info") || 같음(0, "i")) Kernel.msinfo32_exe();
        else if (같음(0, "pwd")) { Späicher_Fichieren.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (Token_COUNT == 1) { Späicher_Fichieren.Wee_Start(1); 처리값 = Späicher_Fichieren.Wee_Byte(0, '/'); } else 처리값 = Token_COUNT == 2 ? Wee(1) : -22;
            if (처리값 >= 0) 처리값 = Späicher_Fichieren.änneren_Verzeechnes(); if (처리값 < 0) Feeler(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int Argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (Token_COUNT == Argument_INDEX) { Späicher_Fichieren.Wee_Start(1); 처리값 = Späicher_Fichieren.Wee_Byte(0, '.'); } else 처리값 = Token_COUNT == Argument_INDEX + 1 ? Wee(Argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Späicher_Fichieren.경로목록(); if (처리값 < 0) Feeler(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) Shell_Tools.Fichier_Job(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) Shell_Tools.Instanz_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) Shell_Tools.Vue_VALUE();
        else if (같음(0, "wc")) Shell_Tools.세기();
        else if (같음(0, "grep")) Shell_Tools.FIND_Agab();
        else if (같음(0, "head") || 같음(0, "tail")) Shell_Tools.머리(같음(0, "tail"));
        else if (같음(0, "tee")) Shell_Tools.함께쓰기();
        else if (같음(0, "env")) Shell_Syntax.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (Token_COUNT == 1) Shell_Syntax.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < Token_COUNT; Loop_INDEX++) { int 처리값 = Shell_Syntax.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { Mooss = 처리값; 단말.schreiwen("Befeel analyséieren_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) Shell_Syntax.ausféieren_Fichier();
        else if (같음(0, "true")) Mooss = 0;
        else if (같음(0, "false")) Mooss = 1;
        else if (같음(0, "history")) Zeil_Editeur.Show_LOG();
        else if (같음(0, "exit")) {
            if (Shell_Syntax.깊이 > 0) { Mooss = Token_COUNT == 1 ? Shell_Syntax.Status_VALUE : Shell_Tools.Ziffer_VALUE(1); if (Mooss < 0 || Mooss > 255) Mooss = 2; Shell_Syntax.Skript_bëennegen = true; }
            else if (Board.Terminal(2) != 0) Terminal(true);
            else 단말.schreiwen("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Editéieren_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (Token_COUNT < 2) { Mooss = 2; 단말.schreiwen("사용법: rm Fichier...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < Token_COUNT; Loop_INDEX++) { int 처리값 = Wee(Loop_INDEX); if (처리값 == 0) 처리값 = Späicher_Fichieren.지우기(); if (처리값 < 0) Feeler(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_positionéieren = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_positionéieren; 첫값 < Token_COUNT; 첫값++) { if (첫값 > Start_positionéieren) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < Längt_VALUE[첫값]; Loop_INDEX++) Board.직렬쓰기(Token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Start_positionéieren == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.schreiwen("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_Bëndel() : Tools(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); Mooss = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !Shell_Syntax.연결중) { 단말.schreiwen("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Tools(13); Mooss = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Tools(15); Mooss = 처리값 < 0 ? 126 : 처리값; if (!Shell_Syntax.연결중) { 단말.schreiwen("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Tools(16); Mooss = 처리값 < 0 ? 126 : 처리값; if (!Shell_Syntax.연결중) { 단말.schreiwen("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int d_Gréisst_veränneren = Board.Terminal(13); 단말.schreiwen("TERMINAL SIZE "); 단말.수(d_Gréisst_veränneren & 65535); 단말.문자('x'); 단말.수(d_Gréisst_veränneren >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Board.Terminal(9); Desktop.ausféieren_Befeel(); }
        else if (같음(0, "c")) Kernel.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) Kernel.작업시험();
        else if (같음(0, "g")) Kernel.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) Kernel.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Board.Laf_Benotzer_App(0); if (처리값 == 0) 단말.schreiwen("ELF DEMO PASS\n"); else Feeler(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? Tool_Agab(-2, 2) : Tools(-1); Mooss = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !Shell_Syntax.연결중) { 단말.schreiwen("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) Kernel.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Board.Fichier_Transfer_Service(1); if (처리값 < 0) Feeler(처리값); else { 단말.schreiwen("FTP listening "); System_Tool.schreiwen_Adress(Board.Reseau_Status(0,0)); 단말.schreiwen(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Board.Fichier_Transfer_Service(0); 단말.schreiwen("FTP stopped\n"); }
            else 단말.schreiwen(Board.Fichier_Transfer_Service(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { Bëndel.Préparéieren(); 단말.schreiwen("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Sprooch = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (Token_COUNT != 2 || Sprooch < 0) 단말.schreiwen("example java|c|python: 출력, Fichier, 네트워크, 그래픽, Java Swing Fënster 예제\n");
            else { int 처리값 = 예제꾸러미.installéieren_VALUE(Sprooch); if (처리값 < 0) { Feeler(처리값); if (처리값 == -28) 단말.schreiwen("RAM full: remove unused files, then retry example\n"); } else 단말.schreiwen("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int Format_VALUE = 실행형식();
            if (Format_VALUE == 1 || Format_VALUE == 2) {
                int 처리값 = Tool_Agab(Format_VALUE == 1 ? -1 : 14, 0); Mooss = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !Shell_Syntax.연결중) { 단말.schreiwen("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (Format_VALUE == 0) { Mooss = 126; 단말.schreiwen("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { Mooss = 127; 단말.schreiwen("Unknown command. help: commands\n"); }
        }
    }
    public static void ausféieren_Befeel() {
        Bëndel.Préparéieren();
        for (int Sprooch = 0; Sprooch < 3; Sprooch++) { int 처리값 = 예제꾸러미.installéieren_VALUE(Sprooch); if (처리값 < 0) Feeler(처리값); }
        Show_Hëllef();
        while (true) {
            Fënster_Sessioun.Prozess_VALUE_Agab(); if (Fënster_Sessioun.재개()) continue;
            if (!Fënster_Sessioun.이어읽기) 단말.schreiwen("jkoros-native> "); Zeil_Editeur.Befeelszeil = true; Board.extern_Waart(1); int d_Gréisst_veränneren = 줄읽기(); Board.extern_Waart(0); Zeil_Editeur.Befeelszeil = false;
            if (d_Gréisst_veränneren == -3) continue;
            if (d_Gréisst_veränneren == -2) 단말.schreiwen("Befeel analyséieren_VALUE: 명령줄이 너무 깁니다\n");
            if (d_Gréisst_veränneren >= 0) { Shell_Syntax.Skript_bëennegen = false; Shell_Syntax.ausféieren_Befeel(Zeil, 0, d_Gréisst_veränneren, 0); } else Shell_Syntax.Status_VALUE = 130;
            Board.bëennegen_extern_Befeel(Shell_Syntax.Status_VALUE);
            Zeil_Editeur.d_Gréisst_veränneren = Zeil_Editeur.Curseur_VALUE = Zeil_Editeur.Start_Fënster = 0;
        }
    }
}
