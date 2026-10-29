// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 príkazový_riadok. Citát, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] riadok = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], dĺžka_VALUE = new int[32];
    static int[] Upravené_Obsah = new int[16384], úprava_názov = new int[63];
    static int token_COUNT, úprava_názov_dĺžka, KR;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Panel.직렬쓰기(VALUE); }
    static int 줄읽기() { return riadkový_editor.Čítanie(); }
    static boolean 나누기(int Veľkosť) {
        int Pozícia = 0, 끝 = 0; token_COUNT = 0;
        while (Pozícia < Veľkosť) {
            while (Pozícia < Veľkosť && (riadok[Pozícia] == 32 || riadok[Pozícia] == 9)) Pozícia++;
            if (Pozícia == Veľkosť) break;
            if (token_COUNT == 16) { 단말.Zápis("Príkaz analyzovať_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Citát_VALUE = 0;
            while (Pozícia < Veľkosť) {
                int VALUE = riadok[Pozícia++];
                if (Citát_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Citát_VALUE) { Citát_VALUE = 0; continue; }
                if (Citát_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Citát_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Citát_VALUE != 0) { 단말.Zápis("Príkaz analyzovať_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            dĺžka_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int pozičný_index=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int bod_kódu=Word_SMS.charAt(순번);
            if (bod_kódu>=0xd800 && bod_kódu<=0xdbff && 순번+1<Word_SMS.length()) bod_kódu=0x10000+((bod_kódu-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int Byte_COUNT=bod_kódu<128?1:bod_kódu<2048?2:bod_kódu<65536?3:4;
            for (int SEQUENCE_VALUE=Byte_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=Byte_COUNT==1?bod_kódu:SEQUENCE_VALUE==Byte_COUNT-1?(Byte_COUNT==2?0xc0:Byte_COUNT==3?0xe0:0xf0)|(bod_kódu>>(6*SEQUENCE_VALUE)):0x80|((bod_kódu>>(6*SEQUENCE_VALUE))&63);
                if (pozičný_index>=dĺžka_VALUE[INDEX] || token_VALUE[시작점[INDEX]+pozičný_index++]!=VALUE) return false;
            }
        }
        return pozičný_index==dĺžka_VALUE[INDEX];
    }
    static int Cesta(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int KR = Pamäť_Súbory.cesta_START(dĺžka_VALUE[INDEX]); if (KR < 0) return KR;
        for (int Loop_INDEX = 0; Loop_INDEX < dĺžka_VALUE[INDEX]; Loop_INDEX++) {
            KR = Pamäť_Súbory.cesta_Byte(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (KR < 0) return KR;
        }
        return 0;
    }
    static void chyba(int INDEX) { KR = 1; 단말.Zápis("chyba "); 단말.수(INDEX); 단말.문자(10); }
    static void zobraziť_VALUE() {
        if (token_COUNT != 2) { 단말.Zápis("사용법: cat Súbor\n"); return; }
        int KR = Cesta(1); if (KR < 0) { chyba(KR); return; }
        int Súbor = Pamäť_Súbory.Otvoriť(0); if (Súbor < 0) { chyba(Súbor); return; }
        while (true) { int VALUE = Pamäť_Súbory.Čítanie(Súbor); if (VALUE == 256) break; if (VALUE < 0) { chyba(VALUE); break; } 원바이트(VALUE); }
        Pamäť_Súbory.Zatvoriť(Súbor); 단말.문자(10);
    }
    static void úprava_VALUE() {
        if (token_COUNT != 2) { 단말.Zápis("사용법: edit Súbor\n"); return; }
        int KR = Cesta(1); if (KR < 0) { chyba(KR); return; }
        úprava_názov_dĺžka = dĺžka_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < úprava_názov_dĺžka; Loop_INDEX++) úprava_názov[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Zápis("EDIT: Súbor 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Veľkosť = 0;
        while (true) {
            단말.Zápis("edit> "); int vstup_VALUE = 줄읽기();
            if (vstup_VALUE < 0) { 단말.Zápis("EDIT CANCELLED\n"); return; }
            if (vstup_VALUE == 1 && riadok[0] == '.') break;
            if (vstup_VALUE + 1 > Upravené_Obsah.length - Veľkosť) { 단말.Zápis("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < vstup_VALUE; Loop_INDEX++) Upravené_Obsah[Veľkosť++] = riadok[Loop_INDEX];
            Upravené_Obsah[Veľkosť++] = 10;
        }
        Pamäť_Súbory.cesta_START(úprava_názov_dĺžka);
        for (int Loop_INDEX = 0; Loop_INDEX < úprava_názov_dĺžka; Loop_INDEX++) Pamäť_Súbory.cesta_Byte(Loop_INDEX, úprava_názov[Loop_INDEX]);
        int Súbor = Pamäť_Súbory.Otvoriť(577); if (Súbor < 0) { chyba(Súbor); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Veľkosť; Loop_INDEX++) Pamäť_Súbory.Zápis(Súbor, Upravené_Obsah[Loop_INDEX]);
        Pamäť_Súbory.Zatvoriť(Súbor); 단말.Zápis("SAVED "); 단말.수(Veľkosť); 단말.Zápis("Byte_VALUE(주기억 Súbor)\n");
    }
    static int šestnástkový_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.Zápis("사용법: load Súbor | hex Súbor\n"); return; }
        int KR = Cesta(1); if (KR < 0) { chyba(KR); return; }
        if (!넣기) {
            int Súbor = Pamäť_Súbory.Otvoriť(0); if (Súbor < 0) { chyba(Súbor); return; }
            단말.Zápis("HEX BEGIN "); 단말.수(Pamäť_Súbory.Veľkosť(Súbor)); 단말.문자(10);
            int položka_COUNT_8f7753a1 = 0;
            while (true) {
                int VALUE = Pamäť_Súbory.Čítanie(Súbor); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++položka_COUNT_8f7753a1 % 32 == 0) 단말.문자(10);
            }
            if (položka_COUNT_8f7753a1 % 32 != 0) 단말.문자(10);
            Pamäť_Súbory.Zatvoriť(Súbor); 단말.Zápis("HEX END\n"); return;
        }
        úprava_názov_dĺžka = dĺžka_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < úprava_názov_dĺžka; Loop_INDEX++) úprava_názov[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Zápis("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Veľkosť = 0;
        while (true) {
            단말.Zápis("hex> "); int vstup_VALUE = 줄읽기();
            if (vstup_VALUE < 0) { 단말.Zápis("LOAD CANCELLED\n"); return; }
            if (vstup_VALUE == 1 && riadok[0] == '.') break;
            int predný_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < vstup_VALUE; Loop_INDEX++) {
                if (riadok[Loop_INDEX] == 32 || riadok[Loop_INDEX] == 9) continue;
                int VALUE = šestnástkový_VALUE(riadok[Loop_INDEX]);
                if (VALUE < 0 || Veľkosť >= Upravené_Obsah.length) { 단말.Zápis("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (predný_VALUE < 0) predný_VALUE = VALUE; else { Upravené_Obsah[Veľkosť++] = predný_VALUE * 16 + VALUE; predný_VALUE = -1; }
            }
            if (predný_VALUE >= 0) { 단말.Zápis("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Pamäť_Súbory.cesta_START(úprava_názov_dĺžka);
        for (int Loop_INDEX = 0; Loop_INDEX < úprava_názov_dĺžka; Loop_INDEX++) Pamäť_Súbory.cesta_Byte(Loop_INDEX, úprava_názov[Loop_INDEX]);
        int Súbor = Pamäť_Súbory.Otvoriť(577); if (Súbor < 0) { chyba(Súbor); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Veľkosť; Loop_INDEX++) Pamäť_Súbory.Zápis(Súbor, Upravené_Obsah[Loop_INDEX]);
        Pamäť_Súbory.Zatvoriť(Súbor); 단말.Zápis("LOADED "); 단말.수(Veľkosť); 단말.Zápis("Byte_VALUE(주기억 Súbor)\n");
    }
    static int Nástroje(int INDEX) {
        return nástroj_položka(INDEX, 1);
    }
    static int nástroj_položka(int INDEX, int Spustiť_2) {
        if (token_COUNT - Spustiť_2 > 8) return -22;
        Panel.인수준비(token_COUNT - Spustiť_2);
        for (int 첫값 = Spustiť_2; 첫값 < token_COUNT; 첫값++) {
            if (dĺžka_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < dĺžka_VALUE[첫값]; Loop_INDEX++) Panel.argument_Byte(첫값 - Spustiť_2, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Panel.리눅스파일실행() : INDEX < 0 ? Panel.Vykonať_používateľ_Súbor() : Panel.spustiť_používateľ_program(INDEX);
    }
    static int PYTHON_zväzok() {
        if (token_COUNT > 8) return -22;
        Panel.인수준비(token_COUNT);
        String Cesta = "/lib/zväzok.py";
        // Java 문자열을 셸의 UTF-8 Argumenty 버퍼에 기록한다.
        int pozičný_index = 0;
        for (int 순번 = 0; 순번 < Cesta.length(); 순번++) {
            int znak_VALUE = Cesta.charAt(순번);
            if (znak_VALUE < 128) Panel.argument_Byte(0, pozičný_index++, znak_VALUE);
            else { Panel.argument_Byte(0, pozičný_index++, 0xe0 | (znak_VALUE >> 12)); Panel.argument_Byte(0, pozičný_index++, 0x80 | ((znak_VALUE >> 6) & 63)); Panel.argument_Byte(0, pozičný_index++, 0x80 | (znak_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (dĺžka_VALUE[순번] > 255) return -36;
            for (int znak_VALUE = 0; znak_VALUE < dĺžka_VALUE[순번]; znak_VALUE++) Panel.argument_Byte(순번, znak_VALUE, token_VALUE[시작점[순번] + znak_VALUE]);
        }
        return Panel.spustiť_používateľ_program(12);
    }
    static int 실행형식() {
        int 처리값 = Cesta(0); if (처리값 < 0) return 처리값;
        int Súbor = Pamäť_Súbory.Otvoriť(0); if (Súbor < 0) return Súbor;
        int 첫값 = Pamäť_Súbory.Čítanie(Súbor), Byte_údaje = Pamäť_Súbory.Čítanie(Súbor), bod_kódu = Pamäť_Súbory.Čítanie(Súbor), 뒷값 = Pamäť_Súbory.Čítanie(Súbor);
        Pamäť_Súbory.Zatvoriť(Súbor);
        if (첫값 == 127 && Byte_údaje == 'E' && bod_kódu == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && Byte_údaje == 'K' && bod_kódu == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumenty) {
        Panel.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumenty.length(); Loop_INDEX++) Panel.argument_Byte(0, Loop_INDEX, Argumenty.charAt(Loop_INDEX));
        return Panel.spustiť_používateľ_program(INDEX);
    }
    static void SMS_Byte(int Súbor, int VALUE) { Pamäť_Súbory.Zápis(Súbor, VALUE); }
    static void 정적파일(String Názov, String obsah_VALUE) {
        // zväzok 파일명은 ASCII. Súbor 내용은 UTF-8로 저장한다.
        Pamäť_Súbory.cesta_START(Názov.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Názov.length(); Loop_INDEX++) Pamäť_Súbory.cesta_Byte(Loop_INDEX, Názov.charAt(Loop_INDEX));
        int Súbor = Pamäť_Súbory.Otvoriť(193); if (Súbor < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < obsah_VALUE.length(); Loop_INDEX++) {
            int bod_kódu = obsah_VALUE.charAt(Loop_INDEX);
            if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && Loop_INDEX + 1 < obsah_VALUE.length()) bod_kódu = 0x10000 + ((bod_kódu - 0xd800) << 10) + obsah_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (bod_kódu < 128) SMS_Byte(Súbor, bod_kódu);
            else {
                int 수 = bod_kódu < 2048 ? 2 : bod_kódu < 65536 ? 3 : 4;
                SMS_Byte(Súbor, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (bod_kódu >> (6 * (수 - 1))));
                for (int položka_COUNT_8f7753a1 = 수 - 1; položka_COUNT_8f7753a1 > 0; položka_COUNT_8f7753a1--) SMS_Byte(Súbor, 0x80 | ((bod_kódu >> (6 * (položka_COUNT_8f7753a1 - 1))) & 63));
            }
        }
        Pamäť_Súbory.Zatvoriť(Súbor);
    }
    static void 한글도움말() {
        단말.Zápis("F9 alebo Shift+Space prepne na slovenské zadávanie.\n");
        단말.Zápis("  [SK] keyboard; [EN] ASCII\n");
        단말.Zápis("  [ → ú\n");
        단말.Zápis("  F9: EN ↔ Slovenský | Ctrl+Shift+V: UTF-8\n");
        단말.Zápis("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Zápis("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Názov) {
        int Byte_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Názov.length(); Loop_INDEX++) { int bod_kódu = Názov.charAt(Loop_INDEX); if (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) return -22; Byte_COUNT += bod_kódu < 128 ? 1 : bod_kódu < 2048 ? 2 : 3; }
        int 처리값 = Pamäť_Súbory.cesta_START(Byte_COUNT); if (처리값 < 0) return 처리값;
        int pozičný_index = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Názov.length(); Loop_INDEX++) {
            int bod_kódu = Názov.charAt(Loop_INDEX);
            if (bod_kódu < 128) Pamäť_Súbory.cesta_Byte(pozičný_index++, bod_kódu);
            else if (bod_kódu < 2048) { Pamäť_Súbory.cesta_Byte(pozičný_index++, 0xc0 | (bod_kódu >> 6)); Pamäť_Súbory.cesta_Byte(pozičný_index++, 0x80 | (bod_kódu & 63)); }
            else { Pamäť_Súbory.cesta_Byte(pozičný_index++, 0xe0 | (bod_kódu >> 12)); Pamäť_Súbory.cesta_Byte(pozičný_index++, 0x80 | ((bod_kódu >> 6) & 63)); Pamäť_Súbory.cesta_Byte(pozičný_index++, 0x80 | (bod_kódu & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Názov) {
        int 처리값 = 예제경로(Názov); if (처리값 < 0) return 처리값;
        처리값 = Pamäť_Súbory.Create_Adresár(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Názov, String údaje) {
        int 처리값 = 예제경로(Názov); if (처리값 < 0) return 처리값;
        int Súbor = Pamäť_Súbory.Otvoriť(193); if (Súbor == -17) return 0; if (Súbor < 0) return Súbor;
        for (int Loop_INDEX = 0; Loop_INDEX < údaje.length(); Loop_INDEX += 2) {
            처리값 = Pamäť_Súbory.Zápis(Súbor, šestnástkový_VALUE(údaje.charAt(Loop_INDEX)) * 16 + šestnástkový_VALUE(údaje.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Pamäť_Súbory.Zatvoriť(Súbor); return 처리값; }
        }
        return Pamäť_Súbory.Zatvoriť(Súbor);
    }
    static void zobraziť_Pomocník() {
        systém_nástroj.zobraziť_Pomocník();
        단말.Zápis("sshd / 보안셸 start|stop|status: SSH :22 (user, 장치별 heslo_VALUE)\n");
        단말.Zápis("vncd / vzdialený_displej start|stop|status: VNC :5900 (장치별 heslo_VALUE)\n");
        단말.Zápis("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Zápis("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Zápis("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Zápis("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Zápis("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Zápis("모서리 + 왼쪽 버튼 presunúť_VALUE: Terminál Veľkosť zmeniť_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Zápis("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Zápis("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Zápis("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Zápis("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Zápis("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Zápis("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Zápis("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Zápis("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Zápis("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Zápis("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Zápis("pip: MicroPython zdroj_strom inštalovať_VALUE; hostiteľ --network --pip 필요; /lib는 RAM\n");
        단말.Zápis("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Zápis("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Zápis("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Zápis("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminál(boolean 전환여부) {
        if (전환여부 && Panel.Terminál(2) != 0) { Panel.Terminál(0); 단말.Zápis("TERMINAL CLOSED\n"); }
        else if (Panel.Terminál(1) < 0) chyba(-19);
        else 단말.Zápis("TERMINAL READY — Slovenský terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Príkaz() {
        if (token_COUNT == 0) return;
        if (systém_nástroj.Vykonať_príkaz()) return;
        if (같음(0,"sshd") || 같음(0,"보안셸") || 같음(0,"vncd") || 같음(0,"vzdialený_displej")) {
            int 종류=같음(0,"vncd")||같음(0,"vzdialený_displej")?1:0;
            int Akcia=같음(1,"start")||같음(1,"Spustiť_2")?1:같음(1,"stop")||같음(1,"Zastaviť")?0:2;
            int Stav_VALUE=Panel.tieňové_ovládanie(종류,Akcia);
            if(Stav_VALUE<0)chyba(Stav_VALUE);else 단말.Zápis(Panel.tieňové_ovládanie(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else zobraziť_Pomocník(); }
        else if (같음(0, "info") || 같음(0, "i")) jadro.Systémové_informácie();
        else if (같음(0, "pwd")) { Pamäť_Súbory.v_termíne_splatnosti_zapísať(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Pamäť_Súbory.cesta_START(1); 처리값 = Pamäť_Súbory.cesta_Byte(0, '/'); } else 처리값 = token_COUNT == 2 ? Cesta(1) : -22;
            if (처리값 >= 0) 처리값 = Pamäť_Súbory.zmeniť_Adresár(); if (처리값 < 0) chyba(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argument_INDEX) { Pamäť_Súbory.cesta_START(1); 처리값 = Pamäť_Súbory.cesta_Byte(0, '.'); } else 처리값 = token_COUNT == argument_INDEX + 1 ? Cesta(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Pamäť_Súbory.경로목록(); if (처리값 < 0) chyba(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) 셸도구.Súbor_Úloha(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) 셸도구.inštancia_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) 셸도구.zobraziť_VALUE();
        else if (같음(0, "wc")) 셸도구.세기();
        else if (같음(0, "grep")) 셸도구.FIND_položka();
        else if (같음(0, "head") || 같음(0, "tail")) 셸도구.머리(같음(0, "tail"));
        else if (같음(0, "tee")) 셸도구.zapísať_Navždy_spolu();
        else if (같음(0, "env")) 셸문법.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) 셸문법.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = 셸문법.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { KR = 처리값; 단말.Zápis("Príkaz analyzovať_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) 셸문법.Vykonať_Súbor();
        else if (같음(0, "true")) KR = 0;
        else if (같음(0, "false")) KR = 1;
        else if (같음(0, "history")) riadkový_editor.zobraziť_LOG();
        else if (같음(0, "exit")) {
            if (셸문법.깊이 > 0) { KR = token_COUNT == 1 ? 셸문법.Stav_VALUE : 셸도구.číslica_VALUE(1); if (KR < 0 || KR > 255) KR = 2; 셸문법.skript_ukončiť_hovor = true; }
            else if (Panel.Terminál(2) != 0) Terminál(true);
            else 단말.Zápis("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) úprava_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { KR = 2; 단말.Zápis("사용법: rm Súbor...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = Cesta(Loop_INDEX); if (처리값 == 0) 처리값 = Pamäť_Súbory.vymazať_položka(); if (처리값 < 0) chyba(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_pozícia = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_pozícia; 첫값 < token_COUNT; 첫값++) { if (첫값 > START_pozícia) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < dĺžka_VALUE[첫값]; Loop_INDEX++) Panel.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (START_pozícia == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Zápis("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_zväzok() : Nástroje(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !셸문법.연결중) { 단말.Zápis("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Nástroje(13); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Nástroje(15); KR = 처리값 < 0 ? 126 : 처리값; if (!셸문법.연결중) { 단말.Zápis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Nástroje(16); KR = 처리값 < 0 ? 126 : 처리값; if (!셸문법.연결중) { 단말.Zápis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Veľkosť = Panel.Terminál(13); 단말.Zápis("TERMINAL SIZE "); 단말.수(Veľkosť & 65535); 단말.문자('x'); 단말.수(Veľkosť >>> 16); 단말.문자(10); }
            else Terminál(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Panel.Terminál(9); počítač.Vykonať_príkaz(); }
        else if (같음(0, "c")) jadro.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) jadro.test_Tasks();
        else if (같음(0, "g")) jadro.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) jadro.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Panel.spustiť_používateľ_program(0); if (처리값 == 0) 단말.Zápis("ELF DEMO PASS\n"); else chyba(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? nástroj_položka(-2, 2) : Nástroje(-1); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !셸문법.연결중) { 단말.Zápis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) jadro.test_Siete();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Panel.prenos_súborov_služba(1); if (처리값 < 0) chyba(처리값); else { 단말.Zápis("FTP listening "); systém_nástroj.zapísať_adresa(Panel.sieť_stav(0,0)); 단말.Zápis(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Panel.prenos_súborov_služba(0); 단말.Zápis("FTP stopped\n"); }
            else 단말.Zápis(Panel.prenos_súborov_služba(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { zväzok.Pripraviť(); 단말.Zápis("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Jazyky = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Jazyky < 0) 단말.Zápis("example java|c|python: Výstup, Súbor, 네트워크, 그래픽, Java Swing Okno 예제\n");
            else { int 처리값 = 예제꾸러미.inštalovať_VALUE(Jazyky); if (처리값 < 0) { chyba(처리값); if (처리값 == -28) 단말.Zápis("RAM full: remove unused files, then retry example\n"); } else 단말.Zápis("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formát_VALUE = 실행형식();
            if (formát_VALUE == 1 || formát_VALUE == 2) {
                int 처리값 = nástroj_položka(formát_VALUE == 1 ? -1 : 14, 0); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !셸문법.연결중) { 단말.Zápis("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (formát_VALUE == 0) { KR = 126; 단말.Zápis("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { KR = 127; 단말.Zápis("Unknown command. help: commands\n"); }
        }
    }
    public static void Vykonať_príkaz() {
        zväzok.Pripraviť();
        for (int Jazyky = 0; Jazyky < 3; Jazyky++) { int 처리값 = 예제꾸러미.inštalovať_VALUE(Jazyky); if (처리값 < 0) chyba(처리값); }
        zobraziť_Pomocník();
        while (true) {
            okno_relácia.Proces_VALUE_položka(); if (okno_relácia.재개()) continue;
            if (!okno_relácia.이어읽기) 단말.Zápis("jkoros-native> "); riadkový_editor.príkazový_riadok = true; Panel.vzdialený_počkaj(1); int Veľkosť = 줄읽기(); Panel.vzdialený_počkaj(0); riadkový_editor.príkazový_riadok = false;
            if (Veľkosť == -3) continue;
            if (Veľkosť == -2) 단말.Zápis("Príkaz analyzovať_VALUE: 명령줄이 너무 깁니다\n");
            if (Veľkosť >= 0) { 셸문법.skript_ukončiť_hovor = false; 셸문법.Vykonať_príkaz(riadok, 0, Veľkosť, 0); } else 셸문법.Stav_VALUE = 130;
            Panel.ukončiť_hovor_vzdialený_príkaz(셸문법.Stav_VALUE);
            riadkový_editor.Veľkosť = riadkový_editor.kurzor_VALUE = riadkový_editor.START_okno = 0;
        }
    }
}
