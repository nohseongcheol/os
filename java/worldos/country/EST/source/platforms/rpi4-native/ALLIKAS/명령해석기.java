// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 käsurida. Tsitaat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Joon = new int[4096], luba_VALUE_eb540501 = new int[4096], 시작점 = new int[32], 길이 = new int[32];
    static int[] Redigeeritud_Sisu = new int[16384], muudatus_nimetus = new int[63];
    static int luba_COUNT, 편집이름길이, TULEMUS;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Tahvel.직렬쓰기(VALUE); }
    static int 줄읽기() { return rearedaktor.Lugemine(); }
    static boolean 나누기(int Suurus) {
        int Asukoht = 0, 끝 = 0; luba_COUNT = 0;
        while (Asukoht < Suurus) {
            while (Asukoht < Suurus && (Joon[Asukoht] == 32 || Joon[Asukoht] == 9)) Asukoht++;
            if (Asukoht == Suurus) break;
            if (luba_COUNT == 16) { 단말.Kirjutamine("Käsk sõeluma_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[luba_COUNT] = 끝; int Tsitaat_VALUE = 0;
            while (Asukoht < Suurus) {
                int VALUE = Joon[Asukoht++];
                if (Tsitaat_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Tsitaat_VALUE) { Tsitaat_VALUE = 0; continue; }
                if (Tsitaat_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Tsitaat_VALUE = VALUE; continue; }
                luba_VALUE_eb540501[끝++] = VALUE;
            }
            if (Tsitaat_VALUE != 0) { 단말.Kirjutamine("Käsk sõeluma_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            길이[luba_COUNT] = 끝 - 시작점[luba_COUNT]; luba_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= luba_COUNT) return false;
        int asukohaindeks=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int koodipunkt=Word_SMS.charAt(순번);
            if (koodipunkt>=0xd800 && koodipunkt<=0xdbff && 순번+1<Word_SMS.length()) koodipunkt=0x10000+((koodipunkt-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bait_COUNT=koodipunkt<128?1:koodipunkt<2048?2:koodipunkt<65536?3:4;
            for (int SEQUENCE_VALUE=bait_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bait_COUNT==1?koodipunkt:SEQUENCE_VALUE==bait_COUNT-1?(bait_COUNT==2?0xc0:bait_COUNT==3?0xe0:0xf0)|(koodipunkt>>(6*SEQUENCE_VALUE)):0x80|((koodipunkt>>(6*SEQUENCE_VALUE))&63);
                if (asukohaindeks>=길이[INDEX] || luba_VALUE_eb540501[시작점[INDEX]+asukohaindeks++]!=VALUE) return false;
            }
        }
        return asukohaindeks==길이[INDEX];
    }
    static int RADA(int INDEX) {
        if (INDEX >= luba_COUNT) return -22;
        int TULEMUS = Mälu_Failid.tee_START(길이[INDEX]); if (TULEMUS < 0) return TULEMUS;
        for (int Loop_INDEX = 0; Loop_INDEX < 길이[INDEX]; Loop_INDEX++) {
            TULEMUS = Mälu_Failid.tee_bait(Loop_INDEX, luba_VALUE_eb540501[시작점[INDEX] + Loop_INDEX]); if (TULEMUS < 0) return TULEMUS;
        }
        return 0;
    }
    static void VIGA(int INDEX) { TULEMUS = 1; 단말.Kirjutamine("VIGA "); 단말.number(INDEX); 단말.문자(10); }
    static void Kuva_VALUE() {
        if (luba_COUNT != 2) { 단말.Kirjutamine("사용법: cat Fail\n"); return; }
        int TULEMUS = RADA(1); if (TULEMUS < 0) { VIGA(TULEMUS); return; }
        int Fail = Mälu_Failid.Ava(0); if (Fail < 0) { VIGA(Fail); return; }
        while (true) { int VALUE = Mälu_Failid.Lugemine(Fail); if (VALUE == 256) break; if (VALUE < 0) { VIGA(VALUE); break; } 원바이트(VALUE); }
        Mälu_Failid.Suletud(Fail); 단말.문자(10);
    }
    static void muudatus_VALUE() {
        if (luba_COUNT != 2) { 단말.Kirjutamine("사용법: edit Fail\n"); return; }
        int TULEMUS = RADA(1); if (TULEMUS < 0) { VIGA(TULEMUS); return; }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) muudatus_nimetus[Loop_INDEX] = luba_VALUE_eb540501[시작점[1] + Loop_INDEX];
        단말.Kirjutamine("EDIT: Fail 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Suurus = 0;
        while (true) {
            단말.Kirjutamine("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Kirjutamine("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Joon[0] == '.') break;
            if (입력 + 1 > Redigeeritud_Sisu.length - Suurus) { 단말.Kirjutamine("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Redigeeritud_Sisu[Suurus++] = Joon[Loop_INDEX];
            Redigeeritud_Sisu[Suurus++] = 10;
        }
        Mälu_Failid.tee_START(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Mälu_Failid.tee_bait(Loop_INDEX, muudatus_nimetus[Loop_INDEX]);
        int Fail = Mälu_Failid.Ava(577); if (Fail < 0) { VIGA(Fail); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Suurus; Loop_INDEX++) Mälu_Failid.Kirjutamine(Fail, Redigeeritud_Sisu[Loop_INDEX]);
        Mälu_Failid.Suletud(Fail); 단말.Kirjutamine("SAVED "); 단말.number(Suurus); 단말.Kirjutamine("bait_VALUE(주기억 Fail)\n");
    }
    static int kuueteistkümnend_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (luba_COUNT != 2) { 단말.Kirjutamine("사용법: load Fail | hex Fail\n"); return; }
        int TULEMUS = RADA(1); if (TULEMUS < 0) { VIGA(TULEMUS); return; }
        if (!넣기) {
            int Fail = Mälu_Failid.Ava(0); if (Fail < 0) { VIGA(Fail); return; }
            단말.Kirjutamine("HEX BEGIN "); 단말.number(Mälu_Failid.Suurus(Fail)); 단말.문자(10);
            int kirje_COUNT = 0;
            while (true) {
                int VALUE = Mälu_Failid.Lugemine(Fail); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++kirje_COUNT % 32 == 0) 단말.문자(10);
            }
            if (kirje_COUNT % 32 != 0) 단말.문자(10);
            Mälu_Failid.Suletud(Fail); 단말.Kirjutamine("HEX END\n"); return;
        }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) muudatus_nimetus[Loop_INDEX] = luba_VALUE_eb540501[시작점[1] + Loop_INDEX];
        단말.Kirjutamine("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Suurus = 0;
        while (true) {
            단말.Kirjutamine("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Kirjutamine("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Joon[0] == '.') break;
            int esikaamera_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Joon[Loop_INDEX] == 32 || Joon[Loop_INDEX] == 9) continue;
                int VALUE = kuueteistkümnend_VALUE(Joon[Loop_INDEX]);
                if (VALUE < 0 || Suurus >= Redigeeritud_Sisu.length) { 단말.Kirjutamine("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (esikaamera_VALUE < 0) esikaamera_VALUE = VALUE; else { Redigeeritud_Sisu[Suurus++] = esikaamera_VALUE * 16 + VALUE; esikaamera_VALUE = -1; }
            }
            if (esikaamera_VALUE >= 0) { 단말.Kirjutamine("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Mälu_Failid.tee_START(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Mälu_Failid.tee_bait(Loop_INDEX, muudatus_nimetus[Loop_INDEX]);
        int Fail = Mälu_Failid.Ava(577); if (Fail < 0) { VIGA(Fail); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Suurus; Loop_INDEX++) Mälu_Failid.Kirjutamine(Fail, Redigeeritud_Sisu[Loop_INDEX]);
        Mälu_Failid.Suletud(Fail); 단말.Kirjutamine("LOADED "); 단말.number(Suurus); 단말.Kirjutamine("bait_VALUE(주기억 Fail)\n");
    }
    static int Tööriistad(int INDEX) {
        return tööriist_kirje(INDEX, 1);
    }
    static int tööriist_kirje(int INDEX, int Käivita_2) {
        if (luba_COUNT - Käivita_2 > 8) return -22;
        Tahvel.인수준비(luba_COUNT - Käivita_2);
        for (int 첫값 = Käivita_2; 첫값 < luba_COUNT; 첫값++) {
            if (길이[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Tahvel.argument_bait(첫값 - Käivita_2, Loop_INDEX, luba_VALUE_eb540501[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Tahvel.리눅스파일실행() : INDEX < 0 ? Tahvel.Täida_kasutaja_Fail() : Tahvel.sari_kasutaja_programm(INDEX);
    }
    static int PYTHON_kogum() {
        if (luba_COUNT > 8) return -22;
        Tahvel.인수준비(luba_COUNT);
        String RADA = "/lib/kogum.py";
        // Java 문자열을 셸의 UTF-8 Argumendid 버퍼에 기록한다.
        int asukohaindeks = 0;
        for (int 순번 = 0; 순번 < RADA.length(); 순번++) {
            int märk_VALUE = RADA.charAt(순번);
            if (märk_VALUE < 128) Tahvel.argument_bait(0, asukohaindeks++, märk_VALUE);
            else { Tahvel.argument_bait(0, asukohaindeks++, 0xe0 | (märk_VALUE >> 12)); Tahvel.argument_bait(0, asukohaindeks++, 0x80 | ((märk_VALUE >> 6) & 63)); Tahvel.argument_bait(0, asukohaindeks++, 0x80 | (märk_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < luba_COUNT; 순번++) {
            if (길이[순번] > 255) return -36;
            for (int märk_VALUE = 0; märk_VALUE < 길이[순번]; märk_VALUE++) Tahvel.argument_bait(순번, märk_VALUE, luba_VALUE_eb540501[시작점[순번] + märk_VALUE]);
        }
        return Tahvel.sari_kasutaja_programm(12);
    }
    static int 실행형식() {
        int 처리값 = RADA(0); if (처리값 < 0) return 처리값;
        int Fail = Mälu_Failid.Ava(0); if (Fail < 0) return Fail;
        int 첫값 = Mälu_Failid.Lugemine(Fail), bait_andmed = Mälu_Failid.Lugemine(Fail), koodipunkt = Mälu_Failid.Lugemine(Fail), 뒷값 = Mälu_Failid.Lugemine(Fail);
        Mälu_Failid.Suletud(Fail);
        if (첫값 == 127 && bait_andmed == 'E' && koodipunkt == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bait_andmed == 'K' && koodipunkt == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumendid) {
        Tahvel.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumendid.length(); Loop_INDEX++) Tahvel.argument_bait(0, Loop_INDEX, Argumendid.charAt(Loop_INDEX));
        return Tahvel.sari_kasutaja_programm(INDEX);
    }
    static void SMS_bait(int Fail, int VALUE) { Mälu_Failid.Kirjutamine(Fail, VALUE); }
    static void 정적파일(String Nimi_2, String Sisu_VALUE) {
        // kogum 파일명은 ASCII. Fail 내용은 UTF-8로 저장한다.
        Mälu_Failid.tee_START(Nimi_2.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Nimi_2.length(); Loop_INDEX++) Mälu_Failid.tee_bait(Loop_INDEX, Nimi_2.charAt(Loop_INDEX));
        int Fail = Mälu_Failid.Ava(193); if (Fail < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Sisu_VALUE.length(); Loop_INDEX++) {
            int koodipunkt = Sisu_VALUE.charAt(Loop_INDEX);
            if (koodipunkt >= 0xd800 && koodipunkt <= 0xdbff && Loop_INDEX + 1 < Sisu_VALUE.length()) koodipunkt = 0x10000 + ((koodipunkt - 0xd800) << 10) + Sisu_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (koodipunkt < 128) SMS_bait(Fail, koodipunkt);
            else {
                int number = koodipunkt < 2048 ? 2 : koodipunkt < 65536 ? 3 : 4;
                SMS_bait(Fail, (number == 2 ? 0xc0 : number == 3 ? 0xe0 : 0xf0) | (koodipunkt >> (6 * (number - 1))));
                for (int kirje_COUNT = number - 1; kirje_COUNT > 0; kirje_COUNT--) SMS_bait(Fail, 0x80 | ((koodipunkt >> (6 * (kirje_COUNT - 1))) & 63));
            }
        }
        Mälu_Failid.Suletud(Fail);
    }
    static void 한글도움말() {
        단말.Kirjutamine("F9 / Shift+Space: [EN] ↔ [Eesti]\n");
        단말.Kirjutamine("  [ET] keyboard; [EN] ASCII\n");
        단말.Kirjutamine("  $ → ¤\n");
        단말.Kirjutamine("  F9: EN ↔ Eesti | Ctrl+Shift+V: UTF-8\n");
        단말.Kirjutamine("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Kirjutamine("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nimi_2) {
        int bait_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nimi_2.length(); Loop_INDEX++) { int koodipunkt = Nimi_2.charAt(Loop_INDEX); if (koodipunkt >= 0xd800 && koodipunkt <= 0xdfff) return -22; bait_COUNT += koodipunkt < 128 ? 1 : koodipunkt < 2048 ? 2 : 3; }
        int 처리값 = Mälu_Failid.tee_START(bait_COUNT); if (처리값 < 0) return 처리값;
        int asukohaindeks = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nimi_2.length(); Loop_INDEX++) {
            int koodipunkt = Nimi_2.charAt(Loop_INDEX);
            if (koodipunkt < 128) Mälu_Failid.tee_bait(asukohaindeks++, koodipunkt);
            else if (koodipunkt < 2048) { Mälu_Failid.tee_bait(asukohaindeks++, 0xc0 | (koodipunkt >> 6)); Mälu_Failid.tee_bait(asukohaindeks++, 0x80 | (koodipunkt & 63)); }
            else { Mälu_Failid.tee_bait(asukohaindeks++, 0xe0 | (koodipunkt >> 12)); Mälu_Failid.tee_bait(asukohaindeks++, 0x80 | ((koodipunkt >> 6) & 63)); Mälu_Failid.tee_bait(asukohaindeks++, 0x80 | (koodipunkt & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nimi_2) {
        int 처리값 = 예제경로(Nimi_2); if (처리값 < 0) return 처리값;
        처리값 = Mälu_Failid.avama_kaust(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nimi_2, String andmed) {
        int 처리값 = 예제경로(Nimi_2); if (처리값 < 0) return 처리값;
        int Fail = Mälu_Failid.Ava(193); if (Fail == -17) return 0; if (Fail < 0) return Fail;
        for (int Loop_INDEX = 0; Loop_INDEX < andmed.length(); Loop_INDEX += 2) {
            처리값 = Mälu_Failid.Kirjutamine(Fail, kuueteistkümnend_VALUE(andmed.charAt(Loop_INDEX)) * 16 + kuueteistkümnend_VALUE(andmed.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Mälu_Failid.Suletud(Fail); return 처리값; }
        }
        return Mälu_Failid.Suletud(Fail);
    }
    static void saade_spikker() {
        süsteem_tööriist.saade_spikker();
        단말.Kirjutamine("sshd / turvaline_kest start|stop|status: SSH :22 (user, 장치별 parool_VALUE)\n");
        단말.Kirjutamine("vncd / kauge_ekraan start|stop|status: VNC :5900 (장치별 parool_VALUE)\n");
        단말.Kirjutamine("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Kirjutamine("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Kirjutamine("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Kirjutamine("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Kirjutamine("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Kirjutamine("모서리 + 왼쪽 버튼 lohistama_VALUE: terminal Suurus muutma_VALUE; terminal size: veerg_VALUE/ROW_VALUE\n");
        단말.Kirjutamine("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Kirjutamine("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Kirjutamine("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Kirjutamine("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Kirjutamine("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Kirjutamine("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Kirjutamine("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Kirjutamine("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Kirjutamine("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Kirjutamine("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Kirjutamine("pip: MicroPython lähe_puu installima_VALUE; host --network --pip 필요; /lib는 RAM\n");
        단말.Kirjutamine("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Kirjutamine("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Kirjutamine("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Kirjutamine("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void terminal(boolean 전환여부) {
        if (전환여부 && Tahvel.terminal(2) != 0) { Tahvel.terminal(0); 단말.Kirjutamine("TERMINAL CLOSED\n"); }
        else if (Tahvel.terminal(1) < 0) VIGA(-19);
        else 단말.Kirjutamine("TERMINAL READY — Eesti terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Käsk() {
        if (luba_COUNT == 0) return;
        if (süsteem_tööriist.Täida_käsk()) return;
        if (같음(0,"sshd") || 같음(0,"turvaline_kest") || 같음(0,"vncd") || 같음(0,"kauge_ekraan")) {
            int 종류=같음(0,"vncd")||같음(0,"kauge_ekraan")?1:0;
            int Nimi=같음(1,"start")||같음(1,"Käivita_2")?1:같음(1,"stop")||같음(1,"Peata")?0:2;
            int Olek_VALUE=Tahvel.varikasutus(종류,Nimi);
            if(Olek_VALUE<0)VIGA(Olek_VALUE);else 단말.Kirjutamine(Tahvel.varikasutus(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else saade_spikker(); }
        else if (같음(0, "info") || 같음(0, "i")) tuum.msinfo32_exe();
        else if (같음(0, "pwd")) { Mälu_Failid.tähtaja_piires_kirjutamine(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (luba_COUNT == 1) { Mälu_Failid.tee_START(1); 처리값 = Mälu_Failid.tee_bait(0, '/'); } else 처리값 = luba_COUNT == 2 ? RADA(1) : -22;
            if (처리값 >= 0) 처리값 = Mälu_Failid.muutma_kaust(); if (처리값 < 0) VIGA(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (luba_COUNT == argument_INDEX) { Mälu_Failid.tee_START(1); 처리값 = Mälu_Failid.tee_bait(0, '.'); } else 처리값 = luba_COUNT == argument_INDEX + 1 ? RADA(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Mälu_Failid.경로목록(); if (처리값 < 0) VIGA(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) kest_Tööriistad.Fail_Töö(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) kest_Tööriistad.eksemplar_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) kest_Tööriistad.Kuva_VALUE();
        else if (같음(0, "wc")) kest_Tööriistad.세기();
        else if (같음(0, "grep")) kest_Tööriistad.FIND_kirje();
        else if (같음(0, "head") || 같음(0, "tail")) kest_Tööriistad.머리(같음(0, "tail"));
        else if (같음(0, "tee")) kest_Tööriistad.함께쓰기();
        else if (같음(0, "env")) kest_süntaks.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (luba_COUNT == 1) kest_süntaks.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < luba_COUNT; Loop_INDEX++) { int 처리값 = kest_süntaks.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { TULEMUS = 처리값; 단말.Kirjutamine("Käsk sõeluma_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) kest_süntaks.Täida_Fail();
        else if (같음(0, "true")) TULEMUS = 0;
        else if (같음(0, "false")) TULEMUS = 1;
        else if (같음(0, "history")) rearedaktor.saade_LOG();
        else if (같음(0, "exit")) {
            if (kest_süntaks.깊이 > 0) { TULEMUS = luba_COUNT == 1 ? kest_süntaks.Olek_VALUE : kest_Tööriistad.number_VALUE(1); if (TULEMUS < 0 || TULEMUS > 255) TULEMUS = 2; kest_süntaks.skript_lõpeta_kõne = true; }
            else if (Tahvel.terminal(2) != 0) terminal(true);
            else 단말.Kirjutamine("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) muudatus_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (luba_COUNT < 2) { TULEMUS = 2; 단말.Kirjutamine("사용법: rm Fail...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < luba_COUNT; Loop_INDEX++) { int 처리값 = RADA(Loop_INDEX); if (처리값 == 0) 처리값 = Mälu_Failid.kustutama_kirje(); if (처리값 < 0) VIGA(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_ametikoht = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_ametikoht; 첫값 < luba_COUNT; 첫값++) { if (첫값 > START_ametikoht) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Tahvel.직렬쓰기(luba_VALUE_eb540501[시작점[첫값] + Loop_INDEX]); }
            if (START_ametikoht == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Kirjutamine("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_kogum() : Tööriistad(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); TULEMUS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !kest_süntaks.연결중) { 단말.Kirjutamine("exit "); 단말.number(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Tööriistad(13); TULEMUS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Tööriistad(15); TULEMUS = 처리값 < 0 ? 126 : 처리값; if (!kest_süntaks.연결중) { 단말.Kirjutamine("exit "); 단말.number(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Tööriistad(16); TULEMUS = 처리값 < 0 ? 126 : 처리값; if (!kest_süntaks.연결중) { 단말.Kirjutamine("exit "); 단말.number(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Suurus = Tahvel.terminal(13); 단말.Kirjutamine("TERMINAL SIZE "); 단말.number(Suurus & 65535); 단말.문자('x'); 단말.number(Suurus >>> 16); 단말.문자(10); }
            else terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tahvel.terminal(9); töölaud.Täida_käsk(); }
        else if (같음(0, "c")) tuum.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) tuum.작업시험();
        else if (같음(0, "g")) tuum.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) tuum.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tahvel.sari_kasutaja_programm(0); if (처리값 == 0) 단말.Kirjutamine("ELF DEMO PASS\n"); else VIGA(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? tööriist_kirje(-2, 2) : Tööriistad(-1); TULEMUS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !kest_süntaks.연결중) { 단말.Kirjutamine("exit "); 단말.number(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) tuum.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tahvel.failiedastus_teenus(1); if (처리값 < 0) VIGA(처리값); else { 단말.Kirjutamine("FTP listening "); süsteem_tööriist.kirjutamine_ADDRESS(Tahvel.võrk_olek(0,0)); 단말.Kirjutamine(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tahvel.failiedastus_teenus(0); 단말.Kirjutamine("FTP stopped\n"); }
            else 단말.Kirjutamine(Tahvel.failiedastus_teenus(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { kogum.Ettevalmistamine(); 단말.Kirjutamine("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Keeled = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (luba_COUNT != 2 || Keeled < 0) 단말.Kirjutamine("example java|c|python: Väljund, Fail, 네트워크, 그래픽, Java Swing aken 예제\n");
            else { int 처리값 = 예제꾸러미.installima_VALUE(Keeled); if (처리값 < 0) { VIGA(처리값); if (처리값 == -28) 단말.Kirjutamine("RAM full: remove unused files, then retry example\n"); } else 단말.Kirjutamine("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int vorming_VALUE = 실행형식();
            if (vorming_VALUE == 1 || vorming_VALUE == 2) {
                int 처리값 = tööriist_kirje(vorming_VALUE == 1 ? -1 : 14, 0); TULEMUS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !kest_süntaks.연결중) { 단말.Kirjutamine("exit "); 단말.number(처리값); 단말.문자(10); }
            } else if (vorming_VALUE == 0) { TULEMUS = 126; 단말.Kirjutamine("실행할 number 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { TULEMUS = 127; 단말.Kirjutamine("Unknown command. help: commands\n"); }
        }
    }
    public static void Täida_käsk() {
        kogum.Ettevalmistamine();
        for (int Keeled = 0; Keeled < 3; Keeled++) { int 처리값 = 예제꾸러미.installima_VALUE(Keeled); if (처리값 < 0) VIGA(처리값); }
        saade_spikker();
        while (true) {
            aken_seanss.Joonis_VALUE_kirje(); if (aken_seanss.재개()) continue;
            if (!aken_seanss.이어읽기) 단말.Kirjutamine("jkoros-native> "); rearedaktor.käsurida = true; Tahvel.kauge_Oota(1); int Suurus = 줄읽기(); Tahvel.kauge_Oota(0); rearedaktor.käsurida = false;
            if (Suurus == -3) continue;
            if (Suurus == -2) 단말.Kirjutamine("Käsk sõeluma_VALUE: 명령줄이 너무 깁니다\n");
            if (Suurus >= 0) { kest_süntaks.skript_lõpeta_kõne = false; kest_süntaks.Täida_käsk(Joon, 0, Suurus, 0); } else kest_süntaks.Olek_VALUE = 130;
            Tahvel.lõpeta_kõne_kauge_käsk(kest_süntaks.Olek_VALUE);
            rearedaktor.Suurus = rearedaktor.kursor_VALUE = rearedaktor.START_aken = 0;
        }
    }
}
