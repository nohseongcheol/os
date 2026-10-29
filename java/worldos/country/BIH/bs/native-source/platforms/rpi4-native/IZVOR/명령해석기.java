// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 komandni_red. Citat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Linija = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], dužina_VALUE = new int[32];
    static int[] Uređivano_TOC = new int[16384], uređivati_naziv = new int[63];
    static int token_COUNT, uređivati_naziv_dužina, mjera;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { ploča.직렬쓰기(VALUE); }
    static int 줄읽기() { return redak_urednik.Čitaj(); }
    static boolean 나누기(int Veličina) {
        int Pozicija = 0, 끝 = 0; token_COUNT = 0;
        while (Pozicija < Veličina) {
            while (Pozicija < Veličina && (Linija[Pozicija] == 32 || Linija[Pozicija] == 9)) Pozicija++;
            if (Pozicija == Veličina) break;
            if (token_COUNT == 16) { 단말.Piši("Naredba raščlanjivati_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Citat_VALUE = 0;
            while (Pozicija < Veličina) {
                int VALUE = Linija[Pozicija++];
                if (Citat_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Citat_VALUE) { Citat_VALUE = 0; continue; }
                if (Citat_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Citat_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Citat_VALUE != 0) { 단말.Piši("Naredba raščlanjivati_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            dužina_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int položaj_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int kôd_znaka=Word_SMS.charAt(순번);
            if (kôd_znaka>=0xd800 && kôd_znaka<=0xdbff && 순번+1<Word_SMS.length()) kôd_znaka=0x10000+((kôd_znaka-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bajt_COUNT=kôd_znaka<128?1:kôd_znaka<2048?2:kôd_znaka<65536?3:4;
            for (int SEQUENCE_VALUE=bajt_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bajt_COUNT==1?kôd_znaka:SEQUENCE_VALUE==bajt_COUNT-1?(bajt_COUNT==2?0xc0:bajt_COUNT==3?0xe0:0xf0)|(kôd_znaka>>(6*SEQUENCE_VALUE)):0x80|((kôd_znaka>>(6*SEQUENCE_VALUE))&63);
                if (položaj_INDEX>=dužina_VALUE[INDEX] || token_VALUE[시작점[INDEX]+položaj_INDEX++]!=VALUE) return false;
            }
        }
        return položaj_INDEX==dužina_VALUE[INDEX];
    }
    static int Putanja(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int mjera = Memorija_Fajlovi.put_START(dužina_VALUE[INDEX]); if (mjera < 0) return mjera;
        for (int Loop_INDEX = 0; Loop_INDEX < dužina_VALUE[INDEX]; Loop_INDEX++) {
            mjera = Memorija_Fajlovi.put_bajt(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (mjera < 0) return mjera;
        }
        return 0;
    }
    static void GRESKA(int INDEX) { mjera = 1; 단말.Piši("GRESKA "); 단말.수(INDEX); 단말.문자(10); }
    static void Prikaz_VALUE() {
        if (token_COUNT != 2) { 단말.Piši("사용법: cat Fajl\n"); return; }
        int mjera = Putanja(1); if (mjera < 0) { GRESKA(mjera); return; }
        int Fajl = Memorija_Fajlovi.Otvori(0); if (Fajl < 0) { GRESKA(Fajl); return; }
        while (true) { int VALUE = Memorija_Fajlovi.Čitaj(Fajl); if (VALUE == 256) break; if (VALUE < 0) { GRESKA(VALUE); break; } 원바이트(VALUE); }
        Memorija_Fajlovi.Zatvori(Fajl); 단말.문자(10);
    }
    static void uređivati_VALUE() {
        if (token_COUNT != 2) { 단말.Piši("사용법: edit Fajl\n"); return; }
        int mjera = Putanja(1); if (mjera < 0) { GRESKA(mjera); return; }
        uređivati_naziv_dužina = dužina_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < uređivati_naziv_dužina; Loop_INDEX++) uređivati_naziv[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Piši("EDIT: Fajl 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Veličina = 0;
        while (true) {
            단말.Piši("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Piši("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Linija[0] == '.') break;
            if (입력 + 1 > Uređivano_TOC.length - Veličina) { 단말.Piši("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Uređivano_TOC[Veličina++] = Linija[Loop_INDEX];
            Uređivano_TOC[Veličina++] = 10;
        }
        Memorija_Fajlovi.put_START(uređivati_naziv_dužina);
        for (int Loop_INDEX = 0; Loop_INDEX < uređivati_naziv_dužina; Loop_INDEX++) Memorija_Fajlovi.put_bajt(Loop_INDEX, uređivati_naziv[Loop_INDEX]);
        int Fajl = Memorija_Fajlovi.Otvori(577); if (Fajl < 0) { GRESKA(Fajl); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Memorija_Fajlovi.Piši(Fajl, Uređivano_TOC[Loop_INDEX]);
        Memorija_Fajlovi.Zatvori(Fajl); 단말.Piši("SAVED "); 단말.수(Veličina); 단말.Piši("bajt_VALUE(주기억 Fajl)\n");
    }
    static int heksadecimalni_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.Piši("사용법: load Fajl | hex Fajl\n"); return; }
        int mjera = Putanja(1); if (mjera < 0) { GRESKA(mjera); return; }
        if (!넣기) {
            int Fajl = Memorija_Fajlovi.Otvori(0); if (Fajl < 0) { GRESKA(Fajl); return; }
            단말.Piši("HEX BEGIN "); 단말.수(Memorija_Fajlovi.Veličina(Fajl)); 단말.문자(10);
            int unos_COUNT = 0;
            while (true) {
                int VALUE = Memorija_Fajlovi.Čitaj(Fajl); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++unos_COUNT % 32 == 0) 단말.문자(10);
            }
            if (unos_COUNT % 32 != 0) 단말.문자(10);
            Memorija_Fajlovi.Zatvori(Fajl); 단말.Piši("HEX END\n"); return;
        }
        uređivati_naziv_dužina = dužina_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < uređivati_naziv_dužina; Loop_INDEX++) uređivati_naziv[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Piši("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Veličina = 0;
        while (true) {
            단말.Piši("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Piši("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Linija[0] == '.') break;
            int 앞 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Linija[Loop_INDEX] == 32 || Linija[Loop_INDEX] == 9) continue;
                int VALUE = heksadecimalni_VALUE(Linija[Loop_INDEX]);
                if (VALUE < 0 || Veličina >= Uređivano_TOC.length) { 단말.Piši("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = VALUE; else { Uređivano_TOC[Veličina++] = 앞 * 16 + VALUE; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Piši("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memorija_Fajlovi.put_START(uređivati_naziv_dužina);
        for (int Loop_INDEX = 0; Loop_INDEX < uređivati_naziv_dužina; Loop_INDEX++) Memorija_Fajlovi.put_bajt(Loop_INDEX, uređivati_naziv[Loop_INDEX]);
        int Fajl = Memorija_Fajlovi.Otvori(577); if (Fajl < 0) { GRESKA(Fajl); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Veličina; Loop_INDEX++) Memorija_Fajlovi.Piši(Fajl, Uređivano_TOC[Loop_INDEX]);
        Memorija_Fajlovi.Zatvori(Fajl); 단말.Piši("LOADED "); 단말.수(Veličina); 단말.Piši("bajt_VALUE(주기억 Fajl)\n");
    }
    static int Alati(int INDEX) {
        return alatka_unos(INDEX, 1);
    }
    static int alatka_unos(int INDEX, int Pokreni) {
        if (token_COUNT - Pokreni > 8) return -22;
        ploča.인수준비(token_COUNT - Pokreni);
        for (int 첫값 = Pokreni; 첫값 < token_COUNT; 첫값++) {
            if (dužina_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < dužina_VALUE[첫값]; Loop_INDEX++) ploča.argument_bajt(첫값 - Pokreni, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? ploča.리눅스파일실행() : INDEX < 0 ? ploča.Izvrši_korisnik_fajl() : ploča.niz_korisnik_program(INDEX);
    }
    static int PYTHON_paket() {
        if (token_COUNT > 8) return -22;
        ploča.인수준비(token_COUNT);
        String Putanja = "/lib/paket.py";
        // Java 문자열을 셸의 UTF-8 Argumenti 버퍼에 기록한다.
        int položaj_INDEX = 0;
        for (int 순번 = 0; 순번 < Putanja.length(); 순번++) {
            int znak_VALUE = Putanja.charAt(순번);
            if (znak_VALUE < 128) ploča.argument_bajt(0, položaj_INDEX++, znak_VALUE);
            else { ploča.argument_bajt(0, položaj_INDEX++, 0xe0 | (znak_VALUE >> 12)); ploča.argument_bajt(0, položaj_INDEX++, 0x80 | ((znak_VALUE >> 6) & 63)); ploča.argument_bajt(0, položaj_INDEX++, 0x80 | (znak_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (dužina_VALUE[순번] > 255) return -36;
            for (int znak_VALUE = 0; znak_VALUE < dužina_VALUE[순번]; znak_VALUE++) ploča.argument_bajt(순번, znak_VALUE, token_VALUE[시작점[순번] + znak_VALUE]);
        }
        return ploča.niz_korisnik_program(12);
    }
    static int 실행형식() {
        int 처리값 = Putanja(0); if (처리값 < 0) return 처리값;
        int Fajl = Memorija_Fajlovi.Otvori(0); if (Fajl < 0) return Fajl;
        int 첫값 = Memorija_Fajlovi.Čitaj(Fajl), bajt_podaci = Memorija_Fajlovi.Čitaj(Fajl), kôd_znaka = Memorija_Fajlovi.Čitaj(Fajl), 뒷값 = Memorija_Fajlovi.Čitaj(Fajl);
        Memorija_Fajlovi.Zatvori(Fajl);
        if (첫값 == 127 && bajt_podaci == 'E' && kôd_znaka == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bajt_podaci == 'K' && kôd_znaka == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumenti) {
        ploča.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumenti.length(); Loop_INDEX++) ploča.argument_bajt(0, Loop_INDEX, Argumenti.charAt(Loop_INDEX));
        return ploča.niz_korisnik_program(INDEX);
    }
    static void SMS_bajt(int Fajl, int VALUE) { Memorija_Fajlovi.Piši(Fajl, VALUE); }
    static void statični_fajl(String Naziv, String Sadržaj_VALUE) {
        // paket 파일명은 ASCII. Fajl 내용은 UTF-8로 저장한다.
        Memorija_Fajlovi.put_START(Naziv.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Naziv.length(); Loop_INDEX++) Memorija_Fajlovi.put_bajt(Loop_INDEX, Naziv.charAt(Loop_INDEX));
        int Fajl = Memorija_Fajlovi.Otvori(193); if (Fajl < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Sadržaj_VALUE.length(); Loop_INDEX++) {
            int kôd_znaka = Sadržaj_VALUE.charAt(Loop_INDEX);
            if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && Loop_INDEX + 1 < Sadržaj_VALUE.length()) kôd_znaka = 0x10000 + ((kôd_znaka - 0xd800) << 10) + Sadržaj_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (kôd_znaka < 128) SMS_bajt(Fajl, kôd_znaka);
            else {
                int 수 = kôd_znaka < 2048 ? 2 : kôd_znaka < 65536 ? 3 : 4;
                SMS_bajt(Fajl, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kôd_znaka >> (6 * (수 - 1))));
                for (int unos_COUNT = 수 - 1; unos_COUNT > 0; unos_COUNT--) SMS_bajt(Fajl, 0x80 | ((kôd_znaka >> (6 * (unos_COUNT - 1))) & 63));
            }
        }
        Memorija_Fajlovi.Zatvori(Fajl);
    }
    static void 한글도움말() {
        단말.Piši("F9 / Shift+Space: [EN] ↔ [bs]\n");
        단말.Piši("  [BS] keyboard; [EN] ASCII\n");
        단말.Piši("  a → a\n");
        단말.Piši("  F9: EN ↔ bs | Ctrl+Shift+V: UTF-8\n");
        단말.Piši("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Piši("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Naziv) {
        int bajt_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Naziv.length(); Loop_INDEX++) { int kôd_znaka = Naziv.charAt(Loop_INDEX); if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) return -22; bajt_COUNT += kôd_znaka < 128 ? 1 : kôd_znaka < 2048 ? 2 : 3; }
        int 처리값 = Memorija_Fajlovi.put_START(bajt_COUNT); if (처리값 < 0) return 처리값;
        int položaj_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Naziv.length(); Loop_INDEX++) {
            int kôd_znaka = Naziv.charAt(Loop_INDEX);
            if (kôd_znaka < 128) Memorija_Fajlovi.put_bajt(položaj_INDEX++, kôd_znaka);
            else if (kôd_znaka < 2048) { Memorija_Fajlovi.put_bajt(položaj_INDEX++, 0xc0 | (kôd_znaka >> 6)); Memorija_Fajlovi.put_bajt(položaj_INDEX++, 0x80 | (kôd_znaka & 63)); }
            else { Memorija_Fajlovi.put_bajt(položaj_INDEX++, 0xe0 | (kôd_znaka >> 12)); Memorija_Fajlovi.put_bajt(položaj_INDEX++, 0x80 | ((kôd_znaka >> 6) & 63)); Memorija_Fajlovi.put_bajt(položaj_INDEX++, 0x80 | (kôd_znaka & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Naziv) {
        int 처리값 = 예제경로(Naziv); if (처리값 < 0) return 처리값;
        처리값 = Memorija_Fajlovi.Create_Direktorij(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Naziv, String podaci) {
        int 처리값 = 예제경로(Naziv); if (처리값 < 0) return 처리값;
        int Fajl = Memorija_Fajlovi.Otvori(193); if (Fajl == -17) return 0; if (Fajl < 0) return Fajl;
        for (int Loop_INDEX = 0; Loop_INDEX < podaci.length(); Loop_INDEX += 2) {
            처리값 = Memorija_Fajlovi.Piši(Fajl, heksadecimalni_VALUE(podaci.charAt(Loop_INDEX)) * 16 + heksadecimalni_VALUE(podaci.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memorija_Fajlovi.Zatvori(Fajl); return 처리값; }
        }
        return Memorija_Fajlovi.Zatvori(Fajl);
    }
    static void program_pomoć() {
        sistem_alatka.program_pomoć();
        단말.Piši("sshd / sigurno_ljuska start|stop|status: SSH :22 (user, 장치별 lozinka_VALUE)\n");
        단말.Piši("vncd / udaljeno_ekran start|stop|status: VNC :5900 (장치별 lozinka_VALUE)\n");
        단말.Piši("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Piši("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Piši("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Piši("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Piši("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Piši("모서리 + 왼쪽 버튼 prevući_VALUE: Terminal Veličina promijeniti_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Piši("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Piši("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Piši("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Piši("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Piši("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Piši("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Piši("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Piši("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Piši("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Piši("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Piši("pip: MicroPython izvor_stablo instalirati_VALUE; organizator --network --pip 필요; /lib는 RAM\n");
        단말.Piši("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Piši("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Piši("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Piši("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && ploča.Terminal(2) != 0) { ploča.Terminal(0); 단말.Piši("TERMINAL CLOSED\n"); }
        else if (ploča.Terminal(1) < 0) GRESKA(-19);
        else 단말.Piši("TERMINAL READY — bs terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Naredba() {
        if (token_COUNT == 0) return;
        if (sistem_alatka.Izvrši_komanda()) return;
        if (같음(0,"sshd") || 같음(0,"sigurno_ljuska") || 같음(0,"vncd") || 같음(0,"udaljeno_ekran")) {
            int 종류=같음(0,"vncd")||같음(0,"udaljeno_ekran")?1:0;
            int radnja=같음(1,"start")||같음(1,"Pokreni")?1:같음(1,"stop")||같음(1,"Zaustavi")?0:2;
            int stanje_VALUE=ploča.daljinsko_upravljanje(종류,radnja);
            if(stanje_VALUE<0)GRESKA(stanje_VALUE);else 단말.Piši(ploča.daljinsko_upravljanje(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else program_pomoć(); }
        else if (같음(0, "info") || 같음(0, "i")) jezgro.msinfo32_exe();
        else if (같음(0, "pwd")) { Memorija_Fajlovi.trenutno_pisati(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Memorija_Fajlovi.put_START(1); 처리값 = Memorija_Fajlovi.put_bajt(0, '/'); } else 처리값 = token_COUNT == 2 ? Putanja(1) : -22;
            if (처리값 >= 0) 처리값 = Memorija_Fajlovi.promijeniti_Direktorij(); if (처리값 < 0) GRESKA(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argument_INDEX) { Memorija_Fajlovi.put_START(1); 처리값 = Memorija_Fajlovi.put_bajt(0, '.'); } else 처리값 = token_COUNT == argument_INDEX + 1 ? Putanja(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memorija_Fajlovi.경로목록(); if (처리값 < 0) GRESKA(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) ljuska_Alati.fajl_slučaj(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) ljuska_Alati.instanca_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) ljuska_Alati.Prikaz_VALUE();
        else if (같음(0, "wc")) ljuska_Alati.세기();
        else if (같음(0, "grep")) ljuska_Alati.FIND_unos();
        else if (같음(0, "head") || 같음(0, "tail")) ljuska_Alati.머리(같음(0, "tail"));
        else if (같음(0, "tee")) ljuska_Alati.함께쓰기();
        else if (같음(0, "env")) ljuska_sintaksa.program_operativno_okruženje();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) ljuska_sintaksa.program_operativno_okruženje();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = ljuska_sintaksa.operativno_okruženje_Postavke(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { mjera = 처리값; 단말.Piši("Naredba raščlanjivati_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 operativno_okruženje 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) ljuska_sintaksa.Izvrši_fajl();
        else if (같음(0, "true")) mjera = 0;
        else if (같음(0, "false")) mjera = 1;
        else if (같음(0, "history")) redak_urednik.program_LOG();
        else if (같음(0, "exit")) {
            if (ljuska_sintaksa.깊이 > 0) { mjera = token_COUNT == 1 ? ljuska_sintaksa.stanje_VALUE : ljuska_Alati.cifra_VALUE(1); if (mjera < 0 || mjera > 255) mjera = 2; ljuska_sintaksa.skripta_završiti = true; }
            else if (ploča.Terminal(2) != 0) Terminal(true);
            else 단말.Piši("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) uređivati_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { mjera = 2; 단말.Piši("사용법: rm Fajl...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = Putanja(Loop_INDEX); if (처리값 == 0) 처리값 = Memorija_Fajlovi.지우기(); if (처리값 < 0) GRESKA(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_položaj = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_položaj; 첫값 < token_COUNT; 첫값++) { if (첫값 > START_položaj) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < dužina_VALUE[첫값]; Loop_INDEX++) ploča.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (START_položaj == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Piši("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_paket() : Alati(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); mjera = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.Piši("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Alati(13); mjera = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Alati(15); mjera = 처리값 < 0 ? 126 : 처리값; if (!ljuska_sintaksa.연결중) { 단말.Piši("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Alati(16); mjera = 처리값 < 0 ? 126 : 처리값; if (!ljuska_sintaksa.연결중) { 단말.Piši("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Veličina = ploča.Terminal(13); 단말.Piši("TERMINAL SIZE "); 단말.수(Veličina & 65535); 단말.문자('x'); 단말.수(Veličina >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { ploča.Terminal(9); desktop.Izvrši_komanda(); }
        else if (같음(0, "c")) jezgro.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) jezgro.작업시험();
        else if (같음(0, "g")) jezgro.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) jezgro.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = ploča.niz_korisnik_program(0); if (처리값 == 0) 단말.Piši("ELF DEMO PASS\n"); else GRESKA(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? alatka_unos(-2, 2) : Alati(-1); mjera = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.Piši("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) jezgro.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = ploča.fajl_prijenos_usluga(1); if (처리값 < 0) GRESKA(처리값); else { 단말.Piši("FTP listening "); sistem_alatka.pisati_adresa(ploča.Mreža_stanje(0,0)); 단말.Piši(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { ploča.fajl_prijenos_usluga(0); 단말.Piši("FTP stopped\n"); }
            else 단말.Piši(ploča.fajl_prijenos_usluga(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { paket.Pripremiti(); 단말.Piši("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Jezik = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Jezik < 0) 단말.Piši("example java|c|python: Ispis, Fajl, 네트워크, 그래픽, Java Swing prozor 예제\n");
            else { int 처리값 = 예제꾸러미.instalirati_VALUE(Jezik); if (처리값 < 0) { GRESKA(처리값); if (처리값 == -28) 단말.Piši("RAM full: remove unused files, then retry example\n"); } else 단말.Piši("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = alatka_unos(format_VALUE == 1 ? -1 : 14, 0); mjera = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.Piši("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { mjera = 126; 단말.Piši("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { mjera = 127; 단말.Piši("Unknown command. help: commands\n"); }
        }
    }
    public static void Izvrši_komanda() {
        paket.Pripremiti();
        for (int Jezik = 0; Jezik < 3; Jezik++) { int 처리값 = 예제꾸러미.instalirati_VALUE(Jezik); if (처리값 < 0) GRESKA(처리값); }
        program_pomoć();
        while (true) {
            prozor_sesija.proces_VALUE_unos(); if (prozor_sesija.재개()) continue;
            if (!prozor_sesija.이어읽기) 단말.Piši("jkoros-native> "); redak_urednik.komandni_red = true; ploča.udaljeno_čekaj(1); int Veličina = 줄읽기(); ploča.udaljeno_čekaj(0); redak_urednik.komandni_red = false;
            if (Veličina == -3) continue;
            if (Veličina == -2) 단말.Piši("Naredba raščlanjivati_VALUE: 명령줄이 너무 깁니다\n");
            if (Veličina >= 0) { ljuska_sintaksa.skripta_završiti = false; ljuska_sintaksa.Izvrši_komanda(Linija, 0, Veličina, 0); } else ljuska_sintaksa.stanje_VALUE = 130;
            ploča.završiti_udaljeno_komanda(ljuska_sintaksa.stanje_VALUE);
            redak_urednik.Veličina = redak_urednik.kursor_VALUE = redak_urednik.START_prozor = 0;
        }
    }
}
