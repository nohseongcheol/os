// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 příkazový_řádek. Citát, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class příkaz_interpret {
    static int[] vstupní_řádek = new int[4096], token_HODNOTA = new int[4096], 시작점 = new int[32], délka_HODNOTA = new int[32];
    static int[] Upraveno_Obsah = new int[16384], úprava_název = new int[63];
    static int token_POČET, úprava_název_délka, VÝSLEDEK;
    static boolean Předchozí_čára;
    static void 원바이트(int HODNOTA) { Panel.직렬쓰기(HODNOTA); }
    static int číst_vstupní_řádek() { return čára_Editor.Čtení(); }
    static boolean 나누기(int Velikost) {
        int pozice = 0, 끝 = 0; token_POČET = 0;
        while (pozice < Velikost) {
            while (pozice < Velikost && (vstupní_řádek[pozice] == 32 || vstupní_řádek[pozice] == 9)) pozice++;
            if (pozice == Velikost) break;
            if (token_POČET == 16) { 단말.Zápis("příkaz parsovat_HODNOTA: 인수가 너무 많습니다\n"); return false; }
            시작점[token_POČET] = 끝; int Citát_HODNOTA = 0;
            while (pozice < Velikost) {
                int HODNOTA = vstupní_řádek[pozice++];
                if (Citát_HODNOTA == 0 && (HODNOTA == 32 || HODNOTA == 9)) break;
                if (HODNOTA == Citát_HODNOTA) { Citát_HODNOTA = 0; continue; }
                if (Citát_HODNOTA == 0 && (HODNOTA == 39 || HODNOTA == 34)) { Citát_HODNOTA = HODNOTA; continue; }
                token_HODNOTA[끝++] = HODNOTA;
            }
            if (Citát_HODNOTA != 0) { 단말.Zápis("příkaz parsovat_HODNOTA: 따옴표가 닫히지 않았습니다\n"); return false; }
            délka_HODNOTA[token_POČET] = 끝 - 시작점[token_POČET]; token_POČET++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_POČET) return false;
        int poziční_index=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int bod_kódu=Word_SMS.charAt(순번);
            if (bod_kódu>=0xd800 && bod_kódu<=0xdbff && 순번+1<Word_SMS.length()) bod_kódu=0x10000+((bod_kódu-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bajt_POČET=bod_kódu<128?1:bod_kódu<2048?2:bod_kódu<65536?3:4;
            for (int SEQUENCE_HODNOTA=bajt_POČET-1; SEQUENCE_HODNOTA>=0; SEQUENCE_HODNOTA--) {
                int HODNOTA=bajt_POČET==1?bod_kódu:SEQUENCE_HODNOTA==bajt_POČET-1?(bajt_POČET==2?0xc0:bajt_POČET==3?0xe0:0xf0)|(bod_kódu>>(6*SEQUENCE_HODNOTA)):0x80|((bod_kódu>>(6*SEQUENCE_HODNOTA))&63);
                if (poziční_index>=délka_HODNOTA[INDEX] || token_HODNOTA[시작점[INDEX]+poziční_index++]!=HODNOTA) return false;
            }
        }
        return poziční_index==délka_HODNOTA[INDEX];
    }
    static int cesta_2(int INDEX) {
        if (INDEX >= token_POČET) return -22;
        int VÝSLEDEK = Paměť_Files.cesta_START(délka_HODNOTA[INDEX]); if (VÝSLEDEK < 0) return VÝSLEDEK;
        for (int Loop_INDEX = 0; Loop_INDEX < délka_HODNOTA[INDEX]; Loop_INDEX++) {
            VÝSLEDEK = Paměť_Files.cesta_bajt(Loop_INDEX, token_HODNOTA[시작점[INDEX] + Loop_INDEX]); if (VÝSLEDEK < 0) return VÝSLEDEK;
        }
        return 0;
    }
    static void chyba(int INDEX) { VÝSLEDEK = 1; 단말.Zápis("chyba "); 단말.číslo(INDEX); 단말.문자(10); }
    static void pohled_HODNOTA() {
        if (token_POČET != 2) { 단말.Zápis("사용법: cat název_souboru\n"); return; }
        int VÝSLEDEK = cesta_2(1); if (VÝSLEDEK < 0) { chyba(VÝSLEDEK); return; }
        int název_souboru = Paměť_Files.Otevřít(0); if (název_souboru < 0) { chyba(název_souboru); return; }
        while (true) { int HODNOTA = Paměť_Files.Čtení(název_souboru); if (HODNOTA == 256) break; if (HODNOTA < 0) { chyba(HODNOTA); break; } 원바이트(HODNOTA); }
        Paměť_Files.Zavřené(název_souboru); 단말.문자(10);
    }
    static void úprava_HODNOTA() {
        if (token_POČET != 2) { 단말.Zápis("사용법: edit název_souboru\n"); return; }
        int VÝSLEDEK = cesta_2(1); if (VÝSLEDEK < 0) { chyba(VÝSLEDEK); return; }
        úprava_název_délka = délka_HODNOTA[1];
        for (int Loop_INDEX = 0; Loop_INDEX < úprava_název_délka; Loop_INDEX++) úprava_název[Loop_INDEX] = token_HODNOTA[시작점[1] + Loop_INDEX];
        단말.Zápis("EDIT: název_souboru 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Velikost = 0;
        while (true) {
            단말.Zápis("edit> "); int vstup_HODNOTA = číst_vstupní_řádek();
            if (vstup_HODNOTA < 0) { 단말.Zápis("EDIT CANCELLED\n"); return; }
            if (vstup_HODNOTA == 1 && vstupní_řádek[0] == '.') break;
            if (vstup_HODNOTA + 1 > Upraveno_Obsah.length - Velikost) { 단말.Zápis("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < vstup_HODNOTA; Loop_INDEX++) Upraveno_Obsah[Velikost++] = vstupní_řádek[Loop_INDEX];
            Upraveno_Obsah[Velikost++] = 10;
        }
        Paměť_Files.cesta_START(úprava_název_délka);
        for (int Loop_INDEX = 0; Loop_INDEX < úprava_název_délka; Loop_INDEX++) Paměť_Files.cesta_bajt(Loop_INDEX, úprava_název[Loop_INDEX]);
        int název_souboru = Paměť_Files.Otevřít(577); if (název_souboru < 0) { chyba(název_souboru); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) Paměť_Files.Zápis(název_souboru, Upraveno_Obsah[Loop_INDEX]);
        Paměť_Files.Zavřené(název_souboru); 단말.Zápis("SAVED "); 단말.číslo(Velikost); 단말.Zápis("bajt_HODNOTA(주기억 název_souboru)\n");
    }
    static int šestnáctková_hodnota(int HODNOTA) {
        if (HODNOTA >= '0' && HODNOTA <= '9') return HODNOTA - '0';
        if (HODNOTA >= 'a' && HODNOTA <= 'f') return HODNOTA - 'a' + 10;
        if (HODNOTA >= 'A' && HODNOTA <= 'F') return HODNOTA - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_POČET != 2) { 단말.Zápis("사용법: load název_souboru | hex název_souboru\n"); return; }
        int VÝSLEDEK = cesta_2(1); if (VÝSLEDEK < 0) { chyba(VÝSLEDEK); return; }
        if (!넣기) {
            int název_souboru = Paměť_Files.Otevřít(0); if (název_souboru < 0) { chyba(název_souboru); return; }
            단말.Zápis("HEX BEGIN "); 단말.číslo(Paměť_Files.Velikost(název_souboru)); 단말.문자(10);
            int položka_POČET = 0;
            while (true) {
                int HODNOTA = Paměť_Files.Čtení(název_souboru); if (HODNOTA < 0 || HODNOTA == 256) break;
                단말.문자("0123456789abcdef".charAt(HODNOTA >> 4)); 단말.문자("0123456789abcdef".charAt(HODNOTA & 15));
                if (++položka_POČET % 32 == 0) 단말.문자(10);
            }
            if (položka_POČET % 32 != 0) 단말.문자(10);
            Paměť_Files.Zavřené(název_souboru); 단말.Zápis("HEX END\n"); return;
        }
        úprava_název_délka = délka_HODNOTA[1];
        for (int Loop_INDEX = 0; Loop_INDEX < úprava_název_délka; Loop_INDEX++) úprava_název[Loop_INDEX] = token_HODNOTA[시작점[1] + Loop_INDEX];
        단말.Zápis("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Velikost = 0;
        while (true) {
            단말.Zápis("hex> "); int vstup_HODNOTA = číst_vstupní_řádek();
            if (vstup_HODNOTA < 0) { 단말.Zápis("LOAD CANCELLED\n"); return; }
            if (vstup_HODNOTA == 1 && vstupní_řádek[0] == '.') break;
            int přední_fotoaparát_HODNOTA = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < vstup_HODNOTA; Loop_INDEX++) {
                if (vstupní_řádek[Loop_INDEX] == 32 || vstupní_řádek[Loop_INDEX] == 9) continue;
                int HODNOTA = šestnáctková_hodnota(vstupní_řádek[Loop_INDEX]);
                if (HODNOTA < 0 || Velikost >= Upraveno_Obsah.length) { 단말.Zápis("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (přední_fotoaparát_HODNOTA < 0) přední_fotoaparát_HODNOTA = HODNOTA; else { Upraveno_Obsah[Velikost++] = přední_fotoaparát_HODNOTA * 16 + HODNOTA; přední_fotoaparát_HODNOTA = -1; }
            }
            if (přední_fotoaparát_HODNOTA >= 0) { 단말.Zápis("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Paměť_Files.cesta_START(úprava_název_délka);
        for (int Loop_INDEX = 0; Loop_INDEX < úprava_název_délka; Loop_INDEX++) Paměť_Files.cesta_bajt(Loop_INDEX, úprava_název[Loop_INDEX]);
        int název_souboru = Paměť_Files.Otevřít(577); if (název_souboru < 0) { chyba(název_souboru); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) Paměť_Files.Zápis(název_souboru, Upraveno_Obsah[Loop_INDEX]);
        Paměť_Files.Zavřené(název_souboru); 단말.Zápis("LOADED "); 단말.číslo(Velikost); 단말.Zápis("bajt_HODNOTA(주기억 název_souboru)\n");
    }
    static int nástroje(int INDEX) {
        return nástroj_položka(INDEX, 1);
    }
    static int nástroj_položka(int INDEX, int Spustit_2) {
        if (token_POČET - Spustit_2 > 8) return -22;
        Panel.인수준비(token_POČET - Spustit_2);
        for (int 첫값 = Spustit_2; 첫값 < token_POČET; 첫값++) {
            if (délka_HODNOTA[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < délka_HODNOTA[첫값]; Loop_INDEX++) Panel.argument_bajt(첫값 - Spustit_2, Loop_INDEX, token_HODNOTA[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Panel.리눅스파일실행() : INDEX < 0 ? Panel.Provést_uživatel_Soubor() : Panel.spustit_uživatel_program(INDEX);
    }
    static int PYTHON_sada() {
        if (token_POČET > 8) return -22;
        Panel.인수준비(token_POČET);
        String cesta_2 = "/lib/sada.py";
        // Java 문자열을 셸의 UTF-8 argumenty 버퍼에 기록한다.
        int poziční_index = 0;
        for (int 순번 = 0; 순번 < cesta_2.length(); 순번++) {
            int znak_HODNOTA = cesta_2.charAt(순번);
            if (znak_HODNOTA < 128) Panel.argument_bajt(0, poziční_index++, znak_HODNOTA);
            else { Panel.argument_bajt(0, poziční_index++, 0xe0 | (znak_HODNOTA >> 12)); Panel.argument_bajt(0, poziční_index++, 0x80 | ((znak_HODNOTA >> 6) & 63)); Panel.argument_bajt(0, poziční_index++, 0x80 | (znak_HODNOTA & 63)); }
        }
        for (int 순번 = 1; 순번 < token_POČET; 순번++) {
            if (délka_HODNOTA[순번] > 255) return -36;
            for (int znak_HODNOTA = 0; znak_HODNOTA < délka_HODNOTA[순번]; znak_HODNOTA++) Panel.argument_bajt(순번, znak_HODNOTA, token_HODNOTA[시작점[순번] + znak_HODNOTA]);
        }
        return Panel.spustit_uživatel_program(12);
    }
    static int spuštění_formát() {
        int 처리값 = cesta_2(0); if (처리값 < 0) return 처리값;
        int název_souboru = Paměť_Files.Otevřít(0); if (název_souboru < 0) return název_souboru;
        int 첫값 = Paměť_Files.Čtení(název_souboru), bajt_data = Paměť_Files.Čtení(název_souboru), bod_kódu = Paměť_Files.Čtení(název_souboru), 뒷값 = Paměť_Files.Čtení(název_souboru);
        Paměť_Files.Zavřené(název_souboru);
        if (첫값 == 127 && bajt_data == 'E' && bod_kódu == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bajt_data == 'K' && bod_kódu == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String argumenty) {
        Panel.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < argumenty.length(); Loop_INDEX++) Panel.argument_bajt(0, Loop_INDEX, argumenty.charAt(Loop_INDEX));
        return Panel.spustit_uživatel_program(INDEX);
    }
    static void SMS_bajt(int název_souboru, int HODNOTA) { Paměť_Files.Zápis(název_souboru, HODNOTA); }
    static void statický_Soubor(String Název, String Obsah_HODNOTA) {
        // sada 파일명은 ASCII. název_souboru 내용은 UTF-8로 저장한다.
        Paměť_Files.cesta_START(Název.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Název.length(); Loop_INDEX++) Paměť_Files.cesta_bajt(Loop_INDEX, Název.charAt(Loop_INDEX));
        int název_souboru = Paměť_Files.Otevřít(193); if (název_souboru < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Obsah_HODNOTA.length(); Loop_INDEX++) {
            int bod_kódu = Obsah_HODNOTA.charAt(Loop_INDEX);
            if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && Loop_INDEX + 1 < Obsah_HODNOTA.length()) bod_kódu = 0x10000 + ((bod_kódu - 0xd800) << 10) + Obsah_HODNOTA.charAt(++Loop_INDEX) - 0xdc00;
            if (bod_kódu < 128) SMS_bajt(název_souboru, bod_kódu);
            else {
                int číslo = bod_kódu < 2048 ? 2 : bod_kódu < 65536 ? 3 : 4;
                SMS_bajt(název_souboru, (číslo == 2 ? 0xc0 : číslo == 3 ? 0xe0 : 0xf0) | (bod_kódu >> (6 * (číslo - 1))));
                for (int položka_POČET = číslo - 1; položka_POČET > 0; položka_POČET--) SMS_bajt(název_souboru, 0x80 | ((bod_kódu >> (6 * (položka_POČET - 1))) & 63));
            }
        }
        Paměť_Files.Zavřené(název_souboru);
    }
    static void 한글도움말() {
        단말.Zápis("F9 nebo Shift+Space přepne na české zadávání.\n");
        단말.Zápis("  [CS] keyboard; [EN] ASCII\n");
        단말.Zápis("  [ → ú\n");
        단말.Zápis("  F9: EN ↔ čeština | Ctrl+Shift+V: UTF-8\n");
        단말.Zápis("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Zápis("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Název) {
        int bajt_POČET = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Název.length(); Loop_INDEX++) { int bod_kódu = Název.charAt(Loop_INDEX); if (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) return -22; bajt_POČET += bod_kódu < 128 ? 1 : bod_kódu < 2048 ? 2 : 3; }
        int 처리값 = Paměť_Files.cesta_START(bajt_POČET); if (처리값 < 0) return 처리값;
        int poziční_index = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Název.length(); Loop_INDEX++) {
            int bod_kódu = Název.charAt(Loop_INDEX);
            if (bod_kódu < 128) Paměť_Files.cesta_bajt(poziční_index++, bod_kódu);
            else if (bod_kódu < 2048) { Paměť_Files.cesta_bajt(poziční_index++, 0xc0 | (bod_kódu >> 6)); Paměť_Files.cesta_bajt(poziční_index++, 0x80 | (bod_kódu & 63)); }
            else { Paměť_Files.cesta_bajt(poziční_index++, 0xe0 | (bod_kódu >> 12)); Paměť_Files.cesta_bajt(poziční_index++, 0x80 | ((bod_kódu >> 6) & 63)); Paměť_Files.cesta_bajt(poziční_index++, 0x80 | (bod_kódu & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Název) {
        int 처리값 = 예제경로(Název); if (처리값 < 0) return 처리값;
        처리값 = Paměť_Files.Create_Adresář(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Název, String data) {
        int 처리값 = 예제경로(Název); if (처리값 < 0) return 처리값;
        int název_souboru = Paměť_Files.Otevřít(193); if (název_souboru == -17) return 0; if (název_souboru < 0) return název_souboru;
        for (int Loop_INDEX = 0; Loop_INDEX < data.length(); Loop_INDEX += 2) {
            처리값 = Paměť_Files.Zápis(název_souboru, šestnáctková_hodnota(data.charAt(Loop_INDEX)) * 16 + šestnáctková_hodnota(data.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Paměť_Files.Zavřené(název_souboru); return 처리값; }
        }
        return Paměť_Files.Zavřené(název_souboru);
    }
    static void zobrazit_nápovědu() {
        Systém_nástroj.zobrazit_nápovědu();
        단말.Zápis("sshd / SSH start|stop|status: SSH :22 (user, 장치별 heslo_HODNOTA)\n");
        단말.Zápis("vncd / vzdálený_displej start|stop|status: VNC :5900 (장치별 heslo_HODNOTA)\n");
        단말.Zápis("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Zápis("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Zápis("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Zápis("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Zápis("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Zápis("모서리 + 왼쪽 버튼 přetáhnout_HODNOTA: interpret_příkazů Velikost změnit_HODNOTA; terminal size: SLOUPEC_HODNOTA/ŘÁDEK_HODNOTA\n");
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
        단말.Zápis("pip: MicroPython zdroj_strom instalovat_HODNOTA; hostit --network --pip 필요; /lib는 RAM\n");
        단말.Zápis("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Zápis("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Zápis("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Zápis("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void interpret_příkazů(boolean 전환여부) {
        if (전환여부 && Panel.interpret_příkazů(2) != 0) { Panel.interpret_příkazů(0); 단말.Zápis("TERMINAL CLOSED\n"); }
        else if (Panel.interpret_příkazů(1) < 0) chyba(-19);
        else 단말.Zápis("TERMINAL READY — čeština terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void příkaz() {
        if (token_POČET == 0) return;
        if (Systém_nástroj.Provést_příkaz()) return;
        if (같음(0,"sshd") || 같음(0,"SSH") || 같음(0,"vncd") || 같음(0,"vzdálený_displej")) {
            int Druh_HODNOTA=같음(0,"vncd")||같음(0,"vzdálený_displej")?1:0;
            int Akce=같음(1,"start")||같음(1,"Spustit_2")?1:같음(1,"stop")||같음(1,"Zastavit")?0:2;
            int Stav_HODNOTA=Panel.stínový_provoz(Druh_HODNOTA,Akce);
            if(Stav_HODNOTA<0)chyba(Stav_HODNOTA);else 단말.Zápis(Panel.stínový_provoz(Druh_HODNOTA,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else zobrazit_nápovědu(); }
        else if (같음(0, "info") || 같음(0, "i")) jádro.Informace_o_systému();
        else if (같음(0, "pwd")) { Paměť_Files.dobrá_zápis(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_POČET == 1) { Paměť_Files.cesta_START(1); 처리값 = Paměť_Files.cesta_bajt(0, '/'); } else 처리값 = token_POČET == 2 ? cesta_2(1) : -22;
            if (처리값 >= 0) 처리값 = Paměť_Files.změnit_Adresář(); if (처리값 < 0) chyba(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_POČET == argument_INDEX) { Paměť_Files.cesta_START(1); 처리값 = Paměť_Files.cesta_bajt(0, '.'); } else 처리값 = token_POČET == argument_INDEX + 1 ? cesta_2(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Paměť_Files.경로목록(); if (처리값 < 0) chyba(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) prostředí_Nástroje.Soubor_Úkol(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) prostředí_Nástroje.instance_HODNOTA(같음(0, "mv"));
        else if (같음(0, "cat")) prostředí_Nástroje.pohled_HODNOTA();
        else if (같음(0, "wc")) prostředí_Nástroje.세기();
        else if (같음(0, "grep")) prostředí_Nástroje.NAJÍT_položka();
        else if (같음(0, "head") || 같음(0, "tail")) prostředí_Nástroje.머리(같음(0, "tail"));
        else if (같음(0, "tee")) prostředí_Nástroje.zápis_Společné_chvíle();
        else if (같음(0, "env")) prostředí_syntaxe.zobrazit_prostředí();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_POČET == 1) prostředí_syntaxe.zobrazit_prostředí();
            for (int Loop_INDEX = 1; Loop_INDEX < token_POČET; Loop_INDEX++) { int 처리값 = prostředí_syntaxe.prostředí_Nastavení(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { VÝSLEDEK = 처리값; 단말.Zápis("příkaz parsovat_HODNOTA: proměnná_HODNOTA 이름이 잘못되었거나 예약된 이름이거나 prostředí_5d36e09c 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) prostředí_syntaxe.Provést_Soubor();
        else if (같음(0, "true")) VÝSLEDEK = 0;
        else if (같음(0, "false")) VÝSLEDEK = 1;
        else if (같음(0, "history")) čára_Editor.zobrazit_LOGZ();
        else if (같음(0, "exit")) {
            if (prostředí_syntaxe.깊이 > 0) { VÝSLEDEK = token_POČET == 1 ? prostředí_syntaxe.Stav_HODNOTA : prostředí_Nástroje.číslice_HODNOTA(1); if (VÝSLEDEK < 0 || VÝSLEDEK > 255) VÝSLEDEK = 2; prostředí_syntaxe.skript_konec = true; }
            else if (Panel.interpret_příkazů(2) != 0) interpret_příkazů(true);
            else 단말.Zápis("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) úprava_HODNOTA();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_POČET < 2) { VÝSLEDEK = 2; 단말.Zápis("사용법: rm název_souboru...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_POČET; Loop_INDEX++) { int 처리값 = cesta_2(Loop_INDEX); if (처리값 == 0) 처리값 = Paměť_Files.vymazat_položka(); if (처리값 < 0) chyba(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_pozice = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_pozice; 첫값 < token_POČET; 첫값++) { if (첫값 > START_pozice) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < délka_HODNOTA[첫값]; Loop_INDEX++) Panel.직렬쓰기(token_HODNOTA[시작점[첫값] + Loop_INDEX]); }
            if (START_pozice == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Zápis("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_sada() : nástroje(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); VÝSLEDEK = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !prostředí_syntaxe.연결중) { 단말.Zápis("exit "); 단말.číslo(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = nástroje(13); VÝSLEDEK = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = nástroje(15); VÝSLEDEK = 처리값 < 0 ? 126 : 처리값; if (!prostředí_syntaxe.연결중) { 단말.Zápis("exit "); 단말.číslo(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = nástroje(16); VÝSLEDEK = 처리값 < 0 ? 126 : 처리값; if (!prostředí_syntaxe.연결중) { 단말.Zápis("exit "); 단말.číslo(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Velikost = Panel.interpret_příkazů(13); 단말.Zápis("TERMINAL SIZE "); 단말.číslo(Velikost & 65535); 단말.문자('x'); 단말.číslo(Velikost >>> 16); 단말.문자(10); }
            else interpret_příkazů(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Panel.interpret_příkazů(9); Plocha.Provést_příkaz(); }
        else if (같음(0, "c")) jádro.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) jádro.test_Tasks();
        else if (같음(0, "g")) jádro.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) jádro.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Panel.spustit_uživatel_program(0); if (처리값 == 0) 단말.Zápis("ELF DEMO PASS\n"); else chyba(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? nástroj_položka(-2, 2) : nástroje(-1); VÝSLEDEK = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !prostředí_syntaxe.연결중) { 단말.Zápis("exit "); 단말.číslo(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) jádro.test_Sítě();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Panel.přenos_souborů_servis(1); if (처리값 < 0) chyba(처리값); else { 단말.Zápis("FTP listening "); Systém_nástroj.zápis_ODKAZ(Panel.síť_stav(0,0)); 단말.Zápis(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Panel.přenos_souborů_servis(0); 단말.Zápis("FTP stopped\n"); }
            else 단말.Zápis(Panel.přenos_souborů_servis(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { sada.Připravit(); 단말.Zápis("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Jazyk = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_POČET != 2 || Jazyk < 0) 단말.Zápis("example java|c|python: výstupní_pozice, název_souboru, 네트워크, 그래픽, Java Swing Okno 예제\n");
            else { int 처리값 = 예제꾸러미.instalovat_HODNOTA(Jazyk); if (처리값 < 0) { chyba(처리값); if (처리값 == -28) 단말.Zápis("RAM full: remove unused files, then retry example\n"); } else 단말.Zápis("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formát_HODNOTA = spuštění_formát();
            if (formát_HODNOTA == 1 || formát_HODNOTA == 2) {
                int 처리값 = nástroj_položka(formát_HODNOTA == 1 ? -1 : 14, 0); VÝSLEDEK = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !prostředí_syntaxe.연결중) { 단말.Zápis("exit "); 단말.číslo(처리값); 단말.문자(10); }
            } else if (formát_HODNOTA == 0) { VÝSLEDEK = 126; 단말.Zápis("실행할 číslo 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { VÝSLEDEK = 127; 단말.Zápis("Unknown command. help: commands\n"); }
        }
    }
    public static void Provést_příkaz() {
        sada.Připravit();
        for (int Jazyk = 0; Jazyk < 3; Jazyk++) { int 처리값 = 예제꾸러미.instalovat_HODNOTA(Jazyk); if (처리값 < 0) chyba(처리값); }
        zobrazit_nápovědu();
        while (true) {
            okno_relace.Proces_HODNOTA_položka(); if (okno_relace.pokračovat_spuštění()) continue;
            if (!okno_relace.이어읽기) 단말.Zápis("jkoros-native> "); čára_Editor.příkazový_řádek = true; Panel.vzdálený_počkej(1); int Velikost = číst_vstupní_řádek(); Panel.vzdálený_počkej(0); čára_Editor.příkazový_řádek = false;
            if (Velikost == -3) continue;
            if (Velikost == -2) 단말.Zápis("příkaz parsovat_HODNOTA: 명령줄이 너무 깁니다\n");
            if (Velikost >= 0) { prostředí_syntaxe.skript_konec = false; prostředí_syntaxe.Provést_příkaz(vstupní_řádek, 0, Velikost, 0); } else prostředí_syntaxe.Stav_HODNOTA = 130;
            Panel.konec_vzdálený_příkaz(prostředí_syntaxe.Stav_HODNOTA);
            čára_Editor.Velikost = čára_Editor.kurzor_HODNOTA = čára_Editor.START_okno = 0;
        }
    }
}
