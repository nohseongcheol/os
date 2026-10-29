// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 bevelreël. Aanhaling, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] lyn = new int[4096], kenteken_VALUE = new int[4096], 시작점 = new int[32], lengte_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], redigeer_naam = new int[63];
    static int kenteken_COUNT, redigeer_naam_lengte, maatreël;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { bord.직렬쓰기(VALUE); }
    static int 줄읽기() { return lyn_Redigeerder.Lees(); }
    static boolean 나누기(int Grootte) {
        int Posisie = 0, 끝 = 0; kenteken_COUNT = 0;
        while (Posisie < Grootte) {
            while (Posisie < Grootte && (lyn[Posisie] == 32 || lyn[Posisie] == 9)) Posisie++;
            if (Posisie == Grootte) break;
            if (kenteken_COUNT == 16) { 단말.Skryf("Opdrag ontleed_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[kenteken_COUNT] = 끝; int Aanhaling_VALUE = 0;
            while (Posisie < Grootte) {
                int VALUE = lyn[Posisie++];
                if (Aanhaling_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Aanhaling_VALUE) { Aanhaling_VALUE = 0; continue; }
                if (Aanhaling_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Aanhaling_VALUE = VALUE; continue; }
                kenteken_VALUE[끝++] = VALUE;
            }
            if (Aanhaling_VALUE != 0) { 단말.Skryf("Opdrag ontleed_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            lengte_VALUE[kenteken_COUNT] = 끝 - 시작점[kenteken_COUNT]; kenteken_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= kenteken_COUNT) return false;
        int plaas_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int karakterkode=Word_SMS.charAt(순번);
            if (karakterkode>=0xd800 && karakterkode<=0xdbff && 순번+1<Word_SMS.length()) karakterkode=0x10000+((karakterkode-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int greep_COUNT=karakterkode<128?1:karakterkode<2048?2:karakterkode<65536?3:4;
            for (int SEQUENCE_VALUE=greep_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=greep_COUNT==1?karakterkode:SEQUENCE_VALUE==greep_COUNT-1?(greep_COUNT==2?0xc0:greep_COUNT==3?0xe0:0xf0)|(karakterkode>>(6*SEQUENCE_VALUE)):0x80|((karakterkode>>(6*SEQUENCE_VALUE))&63);
                if (plaas_INDEX>=lengte_VALUE[INDEX] || kenteken_VALUE[시작점[INDEX]+plaas_INDEX++]!=VALUE) return false;
            }
        }
        return plaas_INDEX==lengte_VALUE[INDEX];
    }
    static int Pad(int INDEX) {
        if (INDEX >= kenteken_COUNT) return -22;
        int maatreël = Geheue_Lêers.pad_BEGIN(lengte_VALUE[INDEX]); if (maatreël < 0) return maatreël;
        for (int lus_INDEX = 0; lus_INDEX < lengte_VALUE[INDEX]; lus_INDEX++) {
            maatreël = Geheue_Lêers.pad_greep(lus_INDEX, kenteken_VALUE[시작점[INDEX] + lus_INDEX]); if (maatreël < 0) return maatreël;
        }
        return 0;
    }
    static void Fout(int INDEX) { maatreël = 1; 단말.Skryf("Fout "); 단말.수(INDEX); 단말.문자(10); }
    static void bekyk_VALUE() {
        if (kenteken_COUNT != 2) { 단말.Skryf("사용법: cat Lêer\n"); return; }
        int maatreël = Pad(1); if (maatreël < 0) { Fout(maatreël); return; }
        int Lêer = Geheue_Lêers.skep(0); if (Lêer < 0) { Fout(Lêer); return; }
        while (true) { int VALUE = Geheue_Lêers.Lees(Lêer); if (VALUE == 256) break; if (VALUE < 0) { Fout(VALUE); break; } 원바이트(VALUE); }
        Geheue_Lêers.Sluit(Lêer); 단말.문자(10);
    }
    static void redigeer_VALUE() {
        if (kenteken_COUNT != 2) { 단말.Skryf("사용법: edit Lêer\n"); return; }
        int maatreël = Pad(1); if (maatreël < 0) { Fout(maatreël); return; }
        redigeer_naam_lengte = lengte_VALUE[1];
        for (int lus_INDEX = 0; lus_INDEX < redigeer_naam_lengte; lus_INDEX++) redigeer_naam[lus_INDEX] = kenteken_VALUE[시작점[1] + lus_INDEX];
        단말.Skryf("EDIT: Lêer 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Grootte = 0;
        while (true) {
            단말.Skryf("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Skryf("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && lyn[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Grootte) { 단말.Skryf("EDIT CANCELLED: file too large\n"); return; }
            for (int lus_INDEX = 0; lus_INDEX < 입력; lus_INDEX++) 편집내용[Grootte++] = lyn[lus_INDEX];
            편집내용[Grootte++] = 10;
        }
        Geheue_Lêers.pad_BEGIN(redigeer_naam_lengte);
        for (int lus_INDEX = 0; lus_INDEX < redigeer_naam_lengte; lus_INDEX++) Geheue_Lêers.pad_greep(lus_INDEX, redigeer_naam[lus_INDEX]);
        int Lêer = Geheue_Lêers.skep(577); if (Lêer < 0) { Fout(Lêer); return; }
        for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) Geheue_Lêers.Skryf(Lêer, 편집내용[lus_INDEX]);
        Geheue_Lêers.Sluit(Lêer); 단말.Skryf("SAVED "); 단말.수(Grootte); 단말.Skryf("greep_VALUE(주기억 Lêer)\n");
    }
    static int hex_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (kenteken_COUNT != 2) { 단말.Skryf("사용법: load Lêer | hex Lêer\n"); return; }
        int maatreël = Pad(1); if (maatreël < 0) { Fout(maatreël); return; }
        if (!넣기) {
            int Lêer = Geheue_Lêers.skep(0); if (Lêer < 0) { Fout(Lêer); return; }
            단말.Skryf("HEX BEGIN "); 단말.수(Geheue_Lêers.Grootte(Lêer)); 단말.문자(10);
            int inskrywing_COUNT = 0;
            while (true) {
                int VALUE = Geheue_Lêers.Lees(Lêer); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++inskrywing_COUNT % 32 == 0) 단말.문자(10);
            }
            if (inskrywing_COUNT % 32 != 0) 단말.문자(10);
            Geheue_Lêers.Sluit(Lêer); 단말.Skryf("HEX END\n"); return;
        }
        redigeer_naam_lengte = lengte_VALUE[1];
        for (int lus_INDEX = 0; lus_INDEX < redigeer_naam_lengte; lus_INDEX++) redigeer_naam[lus_INDEX] = kenteken_VALUE[시작점[1] + lus_INDEX];
        단말.Skryf("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Grootte = 0;
        while (true) {
            단말.Skryf("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Skryf("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && lyn[0] == '.') break;
            int voor_VALUE = -1;
            for (int lus_INDEX = 0; lus_INDEX < 입력; lus_INDEX++) {
                if (lyn[lus_INDEX] == 32 || lyn[lus_INDEX] == 9) continue;
                int VALUE = hex_VALUE(lyn[lus_INDEX]);
                if (VALUE < 0 || Grootte >= 편집내용.length) { 단말.Skryf("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (voor_VALUE < 0) voor_VALUE = VALUE; else { 편집내용[Grootte++] = voor_VALUE * 16 + VALUE; voor_VALUE = -1; }
            }
            if (voor_VALUE >= 0) { 단말.Skryf("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Geheue_Lêers.pad_BEGIN(redigeer_naam_lengte);
        for (int lus_INDEX = 0; lus_INDEX < redigeer_naam_lengte; lus_INDEX++) Geheue_Lêers.pad_greep(lus_INDEX, redigeer_naam[lus_INDEX]);
        int Lêer = Geheue_Lêers.skep(577); if (Lêer < 0) { Fout(Lêer); return; }
        for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) Geheue_Lêers.Skryf(Lêer, 편집내용[lus_INDEX]);
        Geheue_Lêers.Sluit(Lêer); 단말.Skryf("LOADED "); 단말.수(Grootte); 단말.Skryf("greep_VALUE(주기억 Lêer)\n");
    }
    static int Nutsmiddels(int INDEX) {
        return nutsmiddel_inskrywing(INDEX, 1);
    }
    static int nutsmiddel_inskrywing(int INDEX, int Loop) {
        if (kenteken_COUNT - Loop > 8) return -22;
        bord.인수준비(kenteken_COUNT - Loop);
        for (int 첫값 = Loop; 첫값 < kenteken_COUNT; 첫값++) {
            if (lengte_VALUE[첫값] > 255) return -36;
            for (int lus_INDEX = 0; lus_INDEX < lengte_VALUE[첫값]; lus_INDEX++) bord.argument_greep(첫값 - Loop, lus_INDEX, kenteken_VALUE[시작점[첫값] + lus_INDEX]);
        }
        return INDEX == -2 ? bord.리눅스파일실행() : INDEX < 0 ? bord.uitvoer_gebruiker_lêer() : bord.ry_gebruiker_program(INDEX);
    }
    static int PYTHON_bondel() {
        if (kenteken_COUNT > 8) return -22;
        bord.인수준비(kenteken_COUNT);
        String Pad = "/lib/bondel.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int plaas_INDEX = 0;
        for (int 순번 = 0; 순번 < Pad.length(); 순번++) {
            int karakter_VALUE = Pad.charAt(순번);
            if (karakter_VALUE < 128) bord.argument_greep(0, plaas_INDEX++, karakter_VALUE);
            else { bord.argument_greep(0, plaas_INDEX++, 0xe0 | (karakter_VALUE >> 12)); bord.argument_greep(0, plaas_INDEX++, 0x80 | ((karakter_VALUE >> 6) & 63)); bord.argument_greep(0, plaas_INDEX++, 0x80 | (karakter_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < kenteken_COUNT; 순번++) {
            if (lengte_VALUE[순번] > 255) return -36;
            for (int karakter_VALUE = 0; karakter_VALUE < lengte_VALUE[순번]; karakter_VALUE++) bord.argument_greep(순번, karakter_VALUE, kenteken_VALUE[시작점[순번] + karakter_VALUE]);
        }
        return bord.ry_gebruiker_program(12);
    }
    static int 실행형식() {
        int 처리값 = Pad(0); if (처리값 < 0) return 처리값;
        int Lêer = Geheue_Lêers.skep(0); if (Lêer < 0) return Lêer;
        int 첫값 = Geheue_Lêers.Lees(Lêer), greep_data = Geheue_Lêers.Lees(Lêer), karakterkode = Geheue_Lêers.Lees(Lêer), 뒷값 = Geheue_Lêers.Lees(Lêer);
        Geheue_Lêers.Sluit(Lêer);
        if (첫값 == 127 && greep_data == 'E' && karakterkode == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && greep_data == 'K' && karakterkode == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        bord.인수준비(1);
        for (int lus_INDEX = 0; lus_INDEX < 인수.length(); lus_INDEX++) bord.argument_greep(0, lus_INDEX, 인수.charAt(lus_INDEX));
        return bord.ry_gebruiker_program(INDEX);
    }
    static void SMS_greep(int Lêer, int VALUE) { Geheue_Lêers.Skryf(Lêer, VALUE); }
    static void staties_lêer(String Naam, String Inhoud_VALUE) {
        // bondel 파일명은 ASCII. Lêer 내용은 UTF-8로 저장한다.
        Geheue_Lêers.pad_BEGIN(Naam.length());
        for (int lus_INDEX = 0; lus_INDEX < Naam.length(); lus_INDEX++) Geheue_Lêers.pad_greep(lus_INDEX, Naam.charAt(lus_INDEX));
        int Lêer = Geheue_Lêers.skep(193); if (Lêer < 0) return;
        for (int lus_INDEX = 0; lus_INDEX < Inhoud_VALUE.length(); lus_INDEX++) {
            int karakterkode = Inhoud_VALUE.charAt(lus_INDEX);
            if (karakterkode >= 0xd800 && karakterkode <= 0xdbff && lus_INDEX + 1 < Inhoud_VALUE.length()) karakterkode = 0x10000 + ((karakterkode - 0xd800) << 10) + Inhoud_VALUE.charAt(++lus_INDEX) - 0xdc00;
            if (karakterkode < 128) SMS_greep(Lêer, karakterkode);
            else {
                int 수 = karakterkode < 2048 ? 2 : karakterkode < 65536 ? 3 : 4;
                SMS_greep(Lêer, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (karakterkode >> (6 * (수 - 1))));
                for (int inskrywing_COUNT = 수 - 1; inskrywing_COUNT > 0; inskrywing_COUNT--) SMS_greep(Lêer, 0x80 | ((karakterkode >> (6 * (inskrywing_COUNT - 1))) & 63));
            }
        }
        Geheue_Lêers.Sluit(Lêer);
    }
    static void 한글도움말() {
        단말.Skryf("F9 / Shift+Space: [EN] ↔ [af]\n");
        단말.Skryf("  [AF] keyboard; [EN] ASCII\n");
        단말.Skryf("  a → a\n");
        단말.Skryf("  F9: EN ↔ af | Ctrl+Shift+V: UTF-8\n");
        단말.Skryf("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Skryf("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Naam) {
        int greep_COUNT = 0;
        for (int lus_INDEX = 0; lus_INDEX < Naam.length(); lus_INDEX++) { int karakterkode = Naam.charAt(lus_INDEX); if (karakterkode >= 0xd800 && karakterkode <= 0xdfff) return -22; greep_COUNT += karakterkode < 128 ? 1 : karakterkode < 2048 ? 2 : 3; }
        int 처리값 = Geheue_Lêers.pad_BEGIN(greep_COUNT); if (처리값 < 0) return 처리값;
        int plaas_INDEX = 0;
        for (int lus_INDEX = 0; lus_INDEX < Naam.length(); lus_INDEX++) {
            int karakterkode = Naam.charAt(lus_INDEX);
            if (karakterkode < 128) Geheue_Lêers.pad_greep(plaas_INDEX++, karakterkode);
            else if (karakterkode < 2048) { Geheue_Lêers.pad_greep(plaas_INDEX++, 0xc0 | (karakterkode >> 6)); Geheue_Lêers.pad_greep(plaas_INDEX++, 0x80 | (karakterkode & 63)); }
            else { Geheue_Lêers.pad_greep(plaas_INDEX++, 0xe0 | (karakterkode >> 12)); Geheue_Lêers.pad_greep(plaas_INDEX++, 0x80 | ((karakterkode >> 6) & 63)); Geheue_Lêers.pad_greep(plaas_INDEX++, 0x80 | (karakterkode & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Naam) {
        int 처리값 = 예제경로(Naam); if (처리값 < 0) return 처리값;
        처리값 = Geheue_Lêers.Skep_gids(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Naam, String data) {
        int 처리값 = 예제경로(Naam); if (처리값 < 0) return 처리값;
        int Lêer = Geheue_Lêers.skep(193); if (Lêer == -17) return 0; if (Lêer < 0) return Lêer;
        for (int lus_INDEX = 0; lus_INDEX < data.length(); lus_INDEX += 2) {
            처리값 = Geheue_Lêers.Skryf(Lêer, hex_VALUE(data.charAt(lus_INDEX)) * 16 + hex_VALUE(data.charAt(lus_INDEX + 1)));
            if (처리값 < 0) { Geheue_Lêers.Sluit(Lêer); return 처리값; }
        }
        return Geheue_Lêers.Sluit(Lêer);
    }
    static void wys_hulp() {
        stelsel_nutsmiddel.wys_hulp();
        단말.Skryf("sshd / beveiligde_dop start|stop|status: SSH :22 (user, 장치별 wagwoord_VALUE)\n");
        단말.Skryf("vncd / afstands_wys start|stop|status: VNC :5900 (장치별 wagwoord_VALUE)\n");
        단말.Skryf("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Skryf("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Skryf("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Skryf("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Skryf("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Skryf("모서리 + 왼쪽 버튼 sleep_VALUE: Terminaal Grootte verander_VALUE; terminal size: kolom_VALUE/ry_VALUE\n");
        단말.Skryf("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Skryf("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Skryf("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Skryf("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Skryf("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Skryf("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Skryf("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Skryf("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Skryf("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Skryf("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Skryf("pip: MicroPython bron_boom installeer_VALUE; hou --network --pip 필요; /lib는 RAM\n");
        단말.Skryf("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Skryf("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Skryf("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Skryf("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminaal(boolean 전환여부) {
        if (전환여부 && bord.Terminaal(2) != 0) { bord.Terminaal(0); 단말.Skryf("TERMINAL CLOSED\n"); }
        else if (bord.Terminaal(1) < 0) Fout(-19);
        else 단말.Skryf("TERMINAL READY — af terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Opdrag() {
        if (kenteken_COUNT == 0) return;
        if (stelsel_nutsmiddel.uitvoer_bevel()) return;
        if (같음(0,"sshd") || 같음(0,"beveiligde_dop") || 같음(0,"vncd") || 같음(0,"afstands_wys")) {
            int 종류=같음(0,"vncd")||같음(0,"afstands_wys")?1:0;
            int Aksie=같음(1,"start")||같음(1,"Loop")?1:같음(1,"stop")||같음(1,"Stop")?0:2;
            int stand_VALUE=bord.skaduwing(종류,Aksie);
            if(stand_VALUE<0)Fout(stand_VALUE);else 단말.Skryf(bord.skaduwing(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else wys_hulp(); }
        else if (같음(0, "info") || 같음(0, "i")) kern.Stelselinfo();
        else if (같음(0, "pwd")) { Geheue_Lêers.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (kenteken_COUNT == 1) { Geheue_Lêers.pad_BEGIN(1); 처리값 = Geheue_Lêers.pad_greep(0, '/'); } else 처리값 = kenteken_COUNT == 2 ? Pad(1) : -22;
            if (처리값 >= 0) 처리값 = Geheue_Lêers.verander_gids(); if (처리값 < 0) Fout(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (kenteken_COUNT == argument_INDEX) { Geheue_Lêers.pad_BEGIN(1); 처리값 = Geheue_Lêers.pad_greep(0, '.'); } else 처리값 = kenteken_COUNT == argument_INDEX + 1 ? Pad(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Geheue_Lêers.경로목록(); if (처리값 < 0) Fout(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) dop_Nutsmiddels.lêer_saak(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) dop_Nutsmiddels.geval_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) dop_Nutsmiddels.bekyk_VALUE();
        else if (같음(0, "wc")) dop_Nutsmiddels.세기();
        else if (같음(0, "grep")) dop_Nutsmiddels.FIND_inskrywing();
        else if (같음(0, "head") || 같음(0, "tail")) dop_Nutsmiddels.머리(같음(0, "tail"));
        else if (같음(0, "tee")) dop_Nutsmiddels.함께쓰기();
        else if (같음(0, "env")) dop_sintaksis.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (kenteken_COUNT == 1) dop_sintaksis.환경보기();
            for (int lus_INDEX = 1; lus_INDEX < kenteken_COUNT; lus_INDEX++) { int 처리값 = dop_sintaksis.환경설정(lus_INDEX, 같음(0, "unset")); if (처리값 != 0) { maatreël = 처리값; 단말.Skryf("Opdrag ontleed_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) dop_sintaksis.uitvoer_lêer();
        else if (같음(0, "true")) maatreël = 0;
        else if (같음(0, "false")) maatreël = 1;
        else if (같음(0, "history")) lyn_Redigeerder.wys_LOG();
        else if (같음(0, "exit")) {
            if (dop_sintaksis.깊이 > 0) { maatreël = kenteken_COUNT == 1 ? dop_sintaksis.stand_VALUE : dop_Nutsmiddels.syfer_VALUE(1); if (maatreël < 0 || maatreël > 255) maatreël = 2; dop_sintaksis.skrip_beëindig = true; }
            else if (bord.Terminaal(2) != 0) Terminaal(true);
            else 단말.Skryf("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) redigeer_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (kenteken_COUNT < 2) { maatreël = 2; 단말.Skryf("사용법: rm Lêer...\n"); }
            for (int lus_INDEX = 1; lus_INDEX < kenteken_COUNT; lus_INDEX++) { int 처리값 = Pad(lus_INDEX); if (처리값 == 0) 처리값 = Geheue_Lêers.vee_uit_inskrywing(); if (처리값 < 0) Fout(처리값); }
        }
        else if (같음(0, "echo")) {
            int BEGIN_plaas = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = BEGIN_plaas; 첫값 < kenteken_COUNT; 첫값++) { if (첫값 > BEGIN_plaas) 단말.문자(32); for (int lus_INDEX = 0; lus_INDEX < lengte_VALUE[첫값]; lus_INDEX++) bord.직렬쓰기(kenteken_VALUE[시작점[첫값] + lus_INDEX]); }
            if (BEGIN_plaas == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Skryf("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_bondel() : Nutsmiddels(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); maatreël = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !dop_sintaksis.연결중) { 단말.Skryf("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Nutsmiddels(13); maatreël = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Nutsmiddels(15); maatreël = 처리값 < 0 ? 126 : 처리값; if (!dop_sintaksis.연결중) { 단말.Skryf("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Nutsmiddels(16); maatreël = 처리값 < 0 ? 126 : 처리값; if (!dop_sintaksis.연결중) { 단말.Skryf("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Grootte = bord.Terminaal(13); 단말.Skryf("TERMINAL SIZE "); 단말.수(Grootte & 65535); 단말.문자('x'); 단말.수(Grootte >>> 16); 단말.문자(10); }
            else Terminaal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { bord.Terminaal(9); werkskerm.uitvoer_bevel(); }
        else if (같음(0, "c")) kern.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kern.작업시험();
        else if (같음(0, "g")) kern.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kern.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = bord.ry_gebruiker_program(0); if (처리값 == 0) 단말.Skryf("ELF DEMO PASS\n"); else Fout(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? nutsmiddel_inskrywing(-2, 2) : Nutsmiddels(-1); maatreël = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !dop_sintaksis.연결중) { 단말.Skryf("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kern.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = bord.lêer_oordra_diens(1); if (처리값 < 0) Fout(처리값); else { 단말.Skryf("FTP listening "); stelsel_nutsmiddel.skryf_adres(bord.Netwerk_stand(0,0)); 단말.Skryf(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { bord.lêer_oordra_diens(0); 단말.Skryf("FTP stopped\n"); }
            else 단말.Skryf(bord.lêer_oordra_diens(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { bondel.Maak_gereed(); 단말.Skryf("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Taal = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (kenteken_COUNT != 2 || Taal < 0) 단말.Skryf("example java|c|python: Afvoer, Lêer, 네트워크, 그래픽, Java Swing venster 예제\n");
            else { int 처리값 = 예제꾸러미.installeer_VALUE(Taal); if (처리값 < 0) { Fout(처리값); if (처리값 == -28) 단말.Skryf("RAM full: remove unused files, then retry example\n"); } else 단말.Skryf("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formaat_VALUE = 실행형식();
            if (formaat_VALUE == 1 || formaat_VALUE == 2) {
                int 처리값 = nutsmiddel_inskrywing(formaat_VALUE == 1 ? -1 : 14, 0); maatreël = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !dop_sintaksis.연결중) { 단말.Skryf("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (formaat_VALUE == 0) { maatreël = 126; 단말.Skryf("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { maatreël = 127; 단말.Skryf("Unknown command. help: commands\n"); }
        }
    }
    public static void uitvoer_bevel() {
        bondel.Maak_gereed();
        for (int Taal = 0; Taal < 3; Taal++) { int 처리값 = 예제꾸러미.installeer_VALUE(Taal); if (처리값 < 0) Fout(처리값); }
        wys_hulp();
        while (true) {
            venster_sessie.Proses_VALUE_inskrywing(); if (venster_sessie.재개()) continue;
            if (!venster_sessie.이어읽기) 단말.Skryf("jkoros-native> "); lyn_Redigeerder.bevelreël = true; bord.afstands_wag(1); int Grootte = 줄읽기(); bord.afstands_wag(0); lyn_Redigeerder.bevelreël = false;
            if (Grootte == -3) continue;
            if (Grootte == -2) 단말.Skryf("Opdrag ontleed_VALUE: 명령줄이 너무 깁니다\n");
            if (Grootte >= 0) { dop_sintaksis.skrip_beëindig = false; dop_sintaksis.uitvoer_bevel(lyn, 0, Grootte, 0); } else dop_sintaksis.stand_VALUE = 130;
            bord.beëindig_afstands_bevel(dop_sintaksis.stand_VALUE);
            lyn_Redigeerder.Grootte = lyn_Redigeerder.loper_VALUE = lyn_Redigeerder.BEGIN_venster = 0;
        }
    }
}
