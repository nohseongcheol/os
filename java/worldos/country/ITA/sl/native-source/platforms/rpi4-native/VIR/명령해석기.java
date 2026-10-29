// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 ukazna_vrstica. Navedek, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Črtni = new int[4096], žeton_VALUE = new int[4096], 시작점 = new int[32], 길이 = new int[32];
    static int[] Urejeno_Vsebina = new int[16384], Uredi_ime = new int[63];
    static int žeton_COUNT, 편집이름길이, REZULTAT;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Tabla.직렬쓰기(VALUE); }
    static int 줄읽기() { return linija_Urejevalnik.Branje(); }
    static boolean 나누기(int Velikost) {
        int Položaj = 0, 끝 = 0; žeton_COUNT = 0;
        while (Položaj < Velikost) {
            while (Položaj < Velikost && (Črtni[Položaj] == 32 || Črtni[Položaj] == 9)) Položaj++;
            if (Položaj == Velikost) break;
            if (žeton_COUNT == 16) { 단말.Pisanje("Ukaz razčlenjevati_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[žeton_COUNT] = 끝; int Navedek_VALUE = 0;
            while (Položaj < Velikost) {
                int VALUE = Črtni[Položaj++];
                if (Navedek_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Navedek_VALUE) { Navedek_VALUE = 0; continue; }
                if (Navedek_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Navedek_VALUE = VALUE; continue; }
                žeton_VALUE[끝++] = VALUE;
            }
            if (Navedek_VALUE != 0) { 단말.Pisanje("Ukaz razčlenjevati_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            길이[žeton_COUNT] = 끝 - 시작점[žeton_COUNT]; žeton_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= žeton_COUNT) return false;
        int kazalec_mesta=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int koda_znaka=Word_SMS.charAt(순번);
            if (koda_znaka>=0xd800 && koda_znaka<=0xdbff && 순번+1<Word_SMS.length()) koda_znaka=0x10000+((koda_znaka-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bajt_COUNT=koda_znaka<128?1:koda_znaka<2048?2:koda_znaka<65536?3:4;
            for (int SEQUENCE_VALUE=bajt_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bajt_COUNT==1?koda_znaka:SEQUENCE_VALUE==bajt_COUNT-1?(bajt_COUNT==2?0xc0:bajt_COUNT==3?0xe0:0xf0)|(koda_znaka>>(6*SEQUENCE_VALUE)):0x80|((koda_znaka>>(6*SEQUENCE_VALUE))&63);
                if (kazalec_mesta>=길이[INDEX] || žeton_VALUE[시작점[INDEX]+kazalec_mesta++]!=VALUE) return false;
            }
        }
        return kazalec_mesta==길이[INDEX];
    }
    static int POT(int INDEX) {
        if (INDEX >= žeton_COUNT) return -22;
        int REZULTAT = pomnilnik_Datoteke.pot_Start(길이[INDEX]); if (REZULTAT < 0) return REZULTAT;
        for (int Loop_INDEX = 0; Loop_INDEX < 길이[INDEX]; Loop_INDEX++) {
            REZULTAT = pomnilnik_Datoteke.pot_bajt(Loop_INDEX, žeton_VALUE[시작점[INDEX] + Loop_INDEX]); if (REZULTAT < 0) return REZULTAT;
        }
        return 0;
    }
    static void NAPAKA(int INDEX) { REZULTAT = 1; 단말.Pisanje("NAPAKA "); 단말.수(INDEX); 단말.문자(10); }
    static void Pogled_VALUE() {
        if (žeton_COUNT != 2) { 단말.Pisanje("사용법: cat Datoteka\n"); return; }
        int REZULTAT = POT(1); if (REZULTAT < 0) { NAPAKA(REZULTAT); return; }
        int Datoteka = pomnilnik_Datoteke.Odpri(0); if (Datoteka < 0) { NAPAKA(Datoteka); return; }
        while (true) { int VALUE = pomnilnik_Datoteke.Branje(Datoteka); if (VALUE == 256) break; if (VALUE < 0) { NAPAKA(VALUE); break; } 원바이트(VALUE); }
        pomnilnik_Datoteke.Zapri(Datoteka); 단말.문자(10);
    }
    static void Uredi_VALUE() {
        if (žeton_COUNT != 2) { 단말.Pisanje("사용법: edit Datoteka\n"); return; }
        int REZULTAT = POT(1); if (REZULTAT < 0) { NAPAKA(REZULTAT); return; }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Uredi_ime[Loop_INDEX] = žeton_VALUE[시작점[1] + Loop_INDEX];
        단말.Pisanje("EDIT: Datoteka 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Velikost = 0;
        while (true) {
            단말.Pisanje("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Pisanje("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Črtni[0] == '.') break;
            if (입력 + 1 > Urejeno_Vsebina.length - Velikost) { 단말.Pisanje("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Urejeno_Vsebina[Velikost++] = Črtni[Loop_INDEX];
            Urejeno_Vsebina[Velikost++] = 10;
        }
        pomnilnik_Datoteke.pot_Start(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) pomnilnik_Datoteke.pot_bajt(Loop_INDEX, Uredi_ime[Loop_INDEX]);
        int Datoteka = pomnilnik_Datoteke.Odpri(577); if (Datoteka < 0) { NAPAKA(Datoteka); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) pomnilnik_Datoteke.Pisanje(Datoteka, Urejeno_Vsebina[Loop_INDEX]);
        pomnilnik_Datoteke.Zapri(Datoteka); 단말.Pisanje("SAVED "); 단말.수(Velikost); 단말.Pisanje("bajt_VALUE(주기억 Datoteka)\n");
    }
    static int šestnajstiško_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (žeton_COUNT != 2) { 단말.Pisanje("사용법: load Datoteka | hex Datoteka\n"); return; }
        int REZULTAT = POT(1); if (REZULTAT < 0) { NAPAKA(REZULTAT); return; }
        if (!넣기) {
            int Datoteka = pomnilnik_Datoteke.Odpri(0); if (Datoteka < 0) { NAPAKA(Datoteka); return; }
            단말.Pisanje("HEX BEGIN "); 단말.수(pomnilnik_Datoteke.Velikost(Datoteka)); 단말.문자(10);
            int vnos_COUNT = 0;
            while (true) {
                int VALUE = pomnilnik_Datoteke.Branje(Datoteka); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++vnos_COUNT % 32 == 0) 단말.문자(10);
            }
            if (vnos_COUNT % 32 != 0) 단말.문자(10);
            pomnilnik_Datoteke.Zapri(Datoteka); 단말.Pisanje("HEX END\n"); return;
        }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Uredi_ime[Loop_INDEX] = žeton_VALUE[시작점[1] + Loop_INDEX];
        단말.Pisanje("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Velikost = 0;
        while (true) {
            단말.Pisanje("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Pisanje("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Črtni[0] == '.') break;
            int sprednja_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Črtni[Loop_INDEX] == 32 || Črtni[Loop_INDEX] == 9) continue;
                int VALUE = šestnajstiško_VALUE(Črtni[Loop_INDEX]);
                if (VALUE < 0 || Velikost >= Urejeno_Vsebina.length) { 단말.Pisanje("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (sprednja_VALUE < 0) sprednja_VALUE = VALUE; else { Urejeno_Vsebina[Velikost++] = sprednja_VALUE * 16 + VALUE; sprednja_VALUE = -1; }
            }
            if (sprednja_VALUE >= 0) { 단말.Pisanje("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        pomnilnik_Datoteke.pot_Start(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) pomnilnik_Datoteke.pot_bajt(Loop_INDEX, Uredi_ime[Loop_INDEX]);
        int Datoteka = pomnilnik_Datoteke.Odpri(577); if (Datoteka < 0) { NAPAKA(Datoteka); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Velikost; Loop_INDEX++) pomnilnik_Datoteke.Pisanje(Datoteka, Urejeno_Vsebina[Loop_INDEX]);
        pomnilnik_Datoteke.Zapri(Datoteka); 단말.Pisanje("LOADED "); 단말.수(Velikost); 단말.Pisanje("bajt_VALUE(주기억 Datoteka)\n");
    }
    static int Orodja(int INDEX) {
        return orodje_vnos(INDEX, 1);
    }
    static int orodje_vnos(int INDEX, int Zaženi) {
        if (žeton_COUNT - Zaženi > 8) return -22;
        Tabla.인수준비(žeton_COUNT - Zaženi);
        for (int 첫값 = Zaženi; 첫값 < žeton_COUNT; 첫값++) {
            if (길이[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Tabla.argument_bajt(첫값 - Zaženi, Loop_INDEX, žeton_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Tabla.리눅스파일실행() : INDEX < 0 ? Tabla.Izvedi_uporabnik_Datoteka() : Tabla.izvajati_uporabnik_aplikacija(INDEX);
    }
    static int PYTHON_sveženj() {
        if (žeton_COUNT > 8) return -22;
        Tabla.인수준비(žeton_COUNT);
        String POT = "/lib/sveženj.py";
        // Java 문자열을 셸의 UTF-8 Argumenti 버퍼에 기록한다.
        int kazalec_mesta = 0;
        for (int 순번 = 0; 순번 < POT.length(); 순번++) {
            int znak_VALUE = POT.charAt(순번);
            if (znak_VALUE < 128) Tabla.argument_bajt(0, kazalec_mesta++, znak_VALUE);
            else { Tabla.argument_bajt(0, kazalec_mesta++, 0xe0 | (znak_VALUE >> 12)); Tabla.argument_bajt(0, kazalec_mesta++, 0x80 | ((znak_VALUE >> 6) & 63)); Tabla.argument_bajt(0, kazalec_mesta++, 0x80 | (znak_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < žeton_COUNT; 순번++) {
            if (길이[순번] > 255) return -36;
            for (int znak_VALUE = 0; znak_VALUE < 길이[순번]; znak_VALUE++) Tabla.argument_bajt(순번, znak_VALUE, žeton_VALUE[시작점[순번] + znak_VALUE]);
        }
        return Tabla.izvajati_uporabnik_aplikacija(12);
    }
    static int 실행형식() {
        int 처리값 = POT(0); if (처리값 < 0) return 처리값;
        int Datoteka = pomnilnik_Datoteke.Odpri(0); if (Datoteka < 0) return Datoteka;
        int 첫값 = pomnilnik_Datoteke.Branje(Datoteka), bajt_podatki = pomnilnik_Datoteke.Branje(Datoteka), koda_znaka = pomnilnik_Datoteke.Branje(Datoteka), 뒷값 = pomnilnik_Datoteke.Branje(Datoteka);
        pomnilnik_Datoteke.Zapri(Datoteka);
        if (첫값 == 127 && bajt_podatki == 'E' && koda_znaka == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bajt_podatki == 'K' && koda_znaka == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumenti) {
        Tabla.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumenti.length(); Loop_INDEX++) Tabla.argument_bajt(0, Loop_INDEX, Argumenti.charAt(Loop_INDEX));
        return Tabla.izvajati_uporabnik_aplikacija(INDEX);
    }
    static void SMS_bajt(int Datoteka, int VALUE) { pomnilnik_Datoteke.Pisanje(Datoteka, VALUE); }
    static void statičen_Datoteka(String Ime, String vsebina_VALUE) {
        // sveženj 파일명은 ASCII. Datoteka 내용은 UTF-8로 저장한다.
        pomnilnik_Datoteke.pot_Start(Ime.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Ime.length(); Loop_INDEX++) pomnilnik_Datoteke.pot_bajt(Loop_INDEX, Ime.charAt(Loop_INDEX));
        int Datoteka = pomnilnik_Datoteke.Odpri(193); if (Datoteka < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < vsebina_VALUE.length(); Loop_INDEX++) {
            int koda_znaka = vsebina_VALUE.charAt(Loop_INDEX);
            if (koda_znaka >= 0xd800 && koda_znaka <= 0xdbff && Loop_INDEX + 1 < vsebina_VALUE.length()) koda_znaka = 0x10000 + ((koda_znaka - 0xd800) << 10) + vsebina_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (koda_znaka < 128) SMS_bajt(Datoteka, koda_znaka);
            else {
                int 수 = koda_znaka < 2048 ? 2 : koda_znaka < 65536 ? 3 : 4;
                SMS_bajt(Datoteka, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (koda_znaka >> (6 * (수 - 1))));
                for (int vnos_COUNT = 수 - 1; vnos_COUNT > 0; vnos_COUNT--) SMS_bajt(Datoteka, 0x80 | ((koda_znaka >> (6 * (vnos_COUNT - 1))) & 63));
            }
        }
        pomnilnik_Datoteke.Zapri(Datoteka);
    }
    static void 한글도움말() {
        단말.Pisanje("F9 / Shift+Space: [EN] ↔ [sl]\n");
        단말.Pisanje("  [SL] keyboard; [EN] ASCII\n");
        단말.Pisanje("  [ → š\n");
        단말.Pisanje("  F9: EN ↔ sl | Ctrl+Shift+V: UTF-8\n");
        단말.Pisanje("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Pisanje("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Ime) {
        int bajt_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ime.length(); Loop_INDEX++) { int koda_znaka = Ime.charAt(Loop_INDEX); if (koda_znaka >= 0xd800 && koda_znaka <= 0xdfff) return -22; bajt_COUNT += koda_znaka < 128 ? 1 : koda_znaka < 2048 ? 2 : 3; }
        int 처리값 = pomnilnik_Datoteke.pot_Start(bajt_COUNT); if (처리값 < 0) return 처리값;
        int kazalec_mesta = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ime.length(); Loop_INDEX++) {
            int koda_znaka = Ime.charAt(Loop_INDEX);
            if (koda_znaka < 128) pomnilnik_Datoteke.pot_bajt(kazalec_mesta++, koda_znaka);
            else if (koda_znaka < 2048) { pomnilnik_Datoteke.pot_bajt(kazalec_mesta++, 0xc0 | (koda_znaka >> 6)); pomnilnik_Datoteke.pot_bajt(kazalec_mesta++, 0x80 | (koda_znaka & 63)); }
            else { pomnilnik_Datoteke.pot_bajt(kazalec_mesta++, 0xe0 | (koda_znaka >> 12)); pomnilnik_Datoteke.pot_bajt(kazalec_mesta++, 0x80 | ((koda_znaka >> 6) & 63)); pomnilnik_Datoteke.pot_bajt(kazalec_mesta++, 0x80 | (koda_znaka & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Ime) {
        int 처리값 = 예제경로(Ime); if (처리값 < 0) return 처리값;
        처리값 = pomnilnik_Datoteke.Ustvari_Imenik(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Ime, String podatki) {
        int 처리값 = 예제경로(Ime); if (처리값 < 0) return 처리값;
        int Datoteka = pomnilnik_Datoteke.Odpri(193); if (Datoteka == -17) return 0; if (Datoteka < 0) return Datoteka;
        for (int Loop_INDEX = 0; Loop_INDEX < podatki.length(); Loop_INDEX += 2) {
            처리값 = pomnilnik_Datoteke.Pisanje(Datoteka, šestnajstiško_VALUE(podatki.charAt(Loop_INDEX)) * 16 + šestnajstiško_VALUE(podatki.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { pomnilnik_Datoteke.Zapri(Datoteka); return 처리값; }
        }
        return pomnilnik_Datoteke.Zapri(Datoteka);
    }
    static void oddaja_spletna_pomoč() {
        sistem_orodje.oddaja_spletna_pomoč();
        단말.Pisanje("sshd / varen_lupina start|stop|status: SSH :22 (user, 장치별 geslo_VALUE)\n");
        단말.Pisanje("vncd / oddaljen_zaslon start|stop|status: VNC :5900 (장치별 geslo_VALUE)\n");
        단말.Pisanje("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Pisanje("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Pisanje("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Pisanje("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Pisanje("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Pisanje("모서리 + 왼쪽 버튼 povleči_VALUE: Terminal Velikost spremeniti_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Pisanje("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Pisanje("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Pisanje("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Pisanje("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Pisanje("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Pisanje("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Pisanje("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Pisanje("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Pisanje("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Pisanje("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Pisanje("pip: MicroPython vir_drevo namesti_VALUE; gostiti --network --pip 필요; /lib는 RAM\n");
        단말.Pisanje("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Pisanje("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Pisanje("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Pisanje("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Tabla.Terminal(2) != 0) { Tabla.Terminal(0); 단말.Pisanje("TERMINAL CLOSED\n"); }
        else if (Tabla.Terminal(1) < 0) NAPAKA(-19);
        else 단말.Pisanje("TERMINAL READY — sl terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Ukaz() {
        if (žeton_COUNT == 0) return;
        if (sistem_orodje.Izvedi_ukaz()) return;
        if (같음(0,"sshd") || 같음(0,"varen_lupina") || 같음(0,"vncd") || 같음(0,"oddaljen_zaslon")) {
            int 종류=같음(0,"vncd")||같음(0,"oddaljen_zaslon")?1:0;
            int Dejanje=같음(1,"start")||같음(1,"Zaženi")?1:같음(1,"stop")||같음(1,"Zaustavi")?0:2;
            int stanje_VALUE=Tabla.oddaljeni_nadzor(종류,Dejanje);
            if(stanje_VALUE<0)NAPAKA(stanje_VALUE);else 단말.Pisanje(Tabla.oddaljeni_nadzor(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else oddaja_spletna_pomoč(); }
        else if (같음(0, "info") || 같음(0, "i")) jedro.msinfo32_exe();
        else if (같음(0, "pwd")) { pomnilnik_Datoteke.sprotno_pisati(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (žeton_COUNT == 1) { pomnilnik_Datoteke.pot_Start(1); 처리값 = pomnilnik_Datoteke.pot_bajt(0, '/'); } else 처리값 = žeton_COUNT == 2 ? POT(1) : -22;
            if (처리값 >= 0) 처리값 = pomnilnik_Datoteke.spremeniti_Imenik(); if (처리값 < 0) NAPAKA(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (žeton_COUNT == argument_INDEX) { pomnilnik_Datoteke.pot_Start(1); 처리값 = pomnilnik_Datoteke.pot_bajt(0, '.'); } else 처리값 = žeton_COUNT == argument_INDEX + 1 ? POT(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = pomnilnik_Datoteke.경로목록(); if (처리값 < 0) NAPAKA(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) lupina_Orodja.Datoteka_posel(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) lupina_Orodja.kopirati_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) lupina_Orodja.Pogled_VALUE();
        else if (같음(0, "wc")) lupina_Orodja.세기();
        else if (같음(0, "grep")) lupina_Orodja.FIND_vnos();
        else if (같음(0, "head") || 같음(0, "tail")) lupina_Orodja.머리(같음(0, "tail"));
        else if (같음(0, "tee")) lupina_Orodja.pisati_Skupaj();
        else if (같음(0, "env")) lupina_sintaksa.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (žeton_COUNT == 1) lupina_sintaksa.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < žeton_COUNT; Loop_INDEX++) { int 처리값 = lupina_sintaksa.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { REZULTAT = 처리값; 단말.Pisanje("Ukaz razčlenjevati_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) lupina_sintaksa.Izvedi_Datoteka();
        else if (같음(0, "true")) REZULTAT = 0;
        else if (같음(0, "false")) REZULTAT = 1;
        else if (같음(0, "history")) linija_Urejevalnik.oddaja_LOG();
        else if (같음(0, "exit")) {
            if (lupina_sintaksa.깊이 > 0) { REZULTAT = žeton_COUNT == 1 ? lupina_sintaksa.stanje_VALUE : lupina_Orodja.številka_VALUE(1); if (REZULTAT < 0 || REZULTAT > 255) REZULTAT = 2; lupina_sintaksa.skript_končati_klic = true; }
            else if (Tabla.Terminal(2) != 0) Terminal(true);
            else 단말.Pisanje("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Uredi_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (žeton_COUNT < 2) { REZULTAT = 2; 단말.Pisanje("사용법: rm Datoteka...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < žeton_COUNT; Loop_INDEX++) { int 처리값 = POT(Loop_INDEX); if (처리값 == 0) 처리값 = pomnilnik_Datoteke.izbrisati_vnos(); if (처리값 < 0) NAPAKA(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_položaj = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_položaj; 첫값 < žeton_COUNT; 첫값++) { if (첫값 > Start_položaj) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Tabla.직렬쓰기(žeton_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Start_položaj == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Pisanje("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_sveženj() : Orodja(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); REZULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !lupina_sintaksa.연결중) { 단말.Pisanje("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Orodja(13); REZULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Orodja(15); REZULTAT = 처리값 < 0 ? 126 : 처리값; if (!lupina_sintaksa.연결중) { 단말.Pisanje("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Orodja(16); REZULTAT = 처리값 < 0 ? 126 : 처리값; if (!lupina_sintaksa.연결중) { 단말.Pisanje("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Velikost = Tabla.Terminal(13); 단말.Pisanje("TERMINAL SIZE "); 단말.수(Velikost & 65535); 단말.문자('x'); 단말.수(Velikost >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tabla.Terminal(9); namizje.Izvedi_ukaz(); }
        else if (같음(0, "c")) jedro.preskusiti_C();
        else if (같음(0, "tasks") || 같음(0, "t")) jedro.preskusiti_Tasks();
        else if (같음(0, "g")) jedro.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) jedro.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tabla.izvajati_uporabnik_aplikacija(0); if (처리값 == 0) 단말.Pisanje("ELF DEMO PASS\n"); else NAPAKA(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? orodje_vnos(-2, 2) : Orodja(-1); REZULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !lupina_sintaksa.연결중) { 단말.Pisanje("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) jedro.preskusiti_Uporaba_omrežij();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tabla.prenos_datotek_storitev(1); if (처리값 < 0) NAPAKA(처리값); else { 단말.Pisanje("FTP listening "); sistem_orodje.pisati_naslov(Tabla.mreža_stanje(0,0)); 단말.Pisanje(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tabla.prenos_datotek_storitev(0); 단말.Pisanje("FTP stopped\n"); }
            else 단말.Pisanje(Tabla.prenos_datotek_storitev(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { sveženj.Pripravi(); 단말.Pisanje("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int jezik = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (žeton_COUNT != 2 || jezik < 0) 단말.Pisanje("example java|c|python: Izpis, Datoteka, 네트워크, 그래픽, Java Swing okno 예제\n");
            else { int 처리값 = 예제꾸러미.namesti_VALUE(jezik); if (처리값 < 0) { NAPAKA(처리값); if (처리값 == -28) 단말.Pisanje("RAM full: remove unused files, then retry example\n"); } else 단말.Pisanje("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int oblika_VALUE = 실행형식();
            if (oblika_VALUE == 1 || oblika_VALUE == 2) {
                int 처리값 = orodje_vnos(oblika_VALUE == 1 ? -1 : 14, 0); REZULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !lupina_sintaksa.연결중) { 단말.Pisanje("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (oblika_VALUE == 0) { REZULTAT = 126; 단말.Pisanje("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { REZULTAT = 127; 단말.Pisanje("Unknown command. help: commands\n"); }
        }
    }
    public static void Izvedi_ukaz() {
        sveženj.Pripravi();
        for (int jezik = 0; jezik < 3; jezik++) { int 처리값 = 예제꾸러미.namesti_VALUE(jezik); if (처리값 < 0) NAPAKA(처리값); }
        oddaja_spletna_pomoč();
        while (true) {
            okno_seja.Proces_VALUE_vnos(); if (okno_seja.재개()) continue;
            if (!okno_seja.이어읽기) 단말.Pisanje("jkoros-native> "); linija_Urejevalnik.ukazna_vrstica = true; Tabla.oddaljen_počakaj(1); int Velikost = 줄읽기(); Tabla.oddaljen_počakaj(0); linija_Urejevalnik.ukazna_vrstica = false;
            if (Velikost == -3) continue;
            if (Velikost == -2) 단말.Pisanje("Ukaz razčlenjevati_VALUE: 명령줄이 너무 깁니다\n");
            if (Velikost >= 0) { lupina_sintaksa.skript_končati_klic = false; lupina_sintaksa.Izvedi_ukaz(Črtni, 0, Velikost, 0); } else lupina_sintaksa.stanje_VALUE = 130;
            Tabla.končati_klic_oddaljen_ukaz(lupina_sintaksa.stanje_VALUE);
            linija_Urejevalnik.Velikost = linija_Urejevalnik.kazalec_VALUE = linija_Urejevalnik.Start_okno = 0;
        }
    }
}
