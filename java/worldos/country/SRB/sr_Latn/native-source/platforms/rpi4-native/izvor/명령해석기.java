// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 komandna_linija. Citat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] red = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], 길이 = new int[32];
    static int[] Uređivano_Sadržaj = new int[16384], Uredi_ime = new int[63];
    static int token_COUNT, 편집이름길이, KR;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Tabla.직렬쓰기(VALUE); }
    static int 줄읽기() { return red_Uređivač.읽기(); }
    static boolean 나누기(int promeniti_veličinu) {
        int pozicija = 0, 끝 = 0; token_COUNT = 0;
        while (pozicija < promeniti_veličinu) {
            while (pozicija < promeniti_veličinu && (red[pozicija] == 32 || red[pozicija] == 9)) pozicija++;
            if (pozicija == promeniti_veličinu) break;
            if (token_COUNT == 16) { 단말.쓰기("komanda raščlaniti_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Citat_VALUE = 0;
            while (pozicija < promeniti_veličinu) {
                int VALUE = red[pozicija++];
                if (Citat_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Citat_VALUE) { Citat_VALUE = 0; continue; }
                if (Citat_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Citat_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Citat_VALUE != 0) { 단말.쓰기("komanda raščlaniti_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            길이[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int indeks_pozicije=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int kôd_znaka=Word_SMS.charAt(순번);
            if (kôd_znaka>=0xd800 && kôd_znaka<=0xdbff && 순번+1<Word_SMS.length()) kôd_znaka=0x10000+((kôd_znaka-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bajt_COUNT=kôd_znaka<128?1:kôd_znaka<2048?2:kôd_znaka<65536?3:4;
            for (int SEQUENCE_VALUE=bajt_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bajt_COUNT==1?kôd_znaka:SEQUENCE_VALUE==bajt_COUNT-1?(bajt_COUNT==2?0xc0:bajt_COUNT==3?0xe0:0xf0)|(kôd_znaka>>(6*SEQUENCE_VALUE)):0x80|((kôd_znaka>>(6*SEQUENCE_VALUE))&63);
                if (indeks_pozicije>=길이[INDEX] || token_VALUE[시작점[INDEX]+indeks_pozicije++]!=VALUE) return false;
            }
        }
        return indeks_pozicije==길이[INDEX];
    }
    static int putanja(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int KR = Memorija_Datoteke.putanja_START(길이[INDEX]); if (KR < 0) return KR;
        for (int Loop_INDEX = 0; Loop_INDEX < 길이[INDEX]; Loop_INDEX++) {
            KR = Memorija_Datoteke.putanja_bajt(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (KR < 0) return KR;
        }
        return 0;
    }
    static void greška(int INDEX) { KR = 1; 단말.쓰기("greška "); 단말.수(INDEX); 단말.문자(10); }
    static void Prikaz_VALUE() {
        if (token_COUNT != 2) { 단말.쓰기("사용법: cat Datoteka\n"); return; }
        int KR = putanja(1); if (KR < 0) { greška(KR); return; }
        int Datoteka = Memorija_Datoteke.otvoren(0); if (Datoteka < 0) { greška(Datoteka); return; }
        while (true) { int VALUE = Memorija_Datoteke.읽기(Datoteka); if (VALUE == 256) break; if (VALUE < 0) { greška(VALUE); break; } 원바이트(VALUE); }
        Memorija_Datoteke.Zatvori(Datoteka); 단말.문자(10);
    }
    static void Uredi_VALUE() {
        if (token_COUNT != 2) { 단말.쓰기("사용법: edit Datoteka\n"); return; }
        int KR = putanja(1); if (KR < 0) { greška(KR); return; }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Uredi_ime[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.쓰기("EDIT: Datoteka 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int promeniti_veličinu = 0;
        while (true) {
            단말.쓰기("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.쓰기("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && red[0] == '.') break;
            if (입력 + 1 > Uređivano_Sadržaj.length - promeniti_veličinu) { 단말.쓰기("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Uređivano_Sadržaj[promeniti_veličinu++] = red[Loop_INDEX];
            Uređivano_Sadržaj[promeniti_veličinu++] = 10;
        }
        Memorija_Datoteke.putanja_START(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Memorija_Datoteke.putanja_bajt(Loop_INDEX, Uredi_ime[Loop_INDEX]);
        int Datoteka = Memorija_Datoteke.otvoren(577); if (Datoteka < 0) { greška(Datoteka); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) Memorija_Datoteke.쓰기(Datoteka, Uređivano_Sadržaj[Loop_INDEX]);
        Memorija_Datoteke.Zatvori(Datoteka); 단말.쓰기("SAVED "); 단말.수(promeniti_veličinu); 단말.쓰기("bajt_VALUE(주기억 Datoteka)\n");
    }
    static int heksadecimalni_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.쓰기("사용법: load Datoteka | hex Datoteka\n"); return; }
        int KR = putanja(1); if (KR < 0) { greška(KR); return; }
        if (!넣기) {
            int Datoteka = Memorija_Datoteke.otvoren(0); if (Datoteka < 0) { greška(Datoteka); return; }
            단말.쓰기("HEX BEGIN "); 단말.수(Memorija_Datoteke.promeniti_veličinu(Datoteka)); 단말.문자(10);
            int stavka_COUNT_8f7753a1 = 0;
            while (true) {
                int VALUE = Memorija_Datoteke.읽기(Datoteka); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++stavka_COUNT_8f7753a1 % 32 == 0) 단말.문자(10);
            }
            if (stavka_COUNT_8f7753a1 % 32 != 0) 단말.문자(10);
            Memorija_Datoteke.Zatvori(Datoteka); 단말.쓰기("HEX END\n"); return;
        }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Uredi_ime[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.쓰기("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int promeniti_veličinu = 0;
        while (true) {
            단말.쓰기("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.쓰기("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && red[0] == '.') break;
            int čeona_kamera_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (red[Loop_INDEX] == 32 || red[Loop_INDEX] == 9) continue;
                int VALUE = heksadecimalni_VALUE(red[Loop_INDEX]);
                if (VALUE < 0 || promeniti_veličinu >= Uređivano_Sadržaj.length) { 단말.쓰기("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (čeona_kamera_VALUE < 0) čeona_kamera_VALUE = VALUE; else { Uređivano_Sadržaj[promeniti_veličinu++] = čeona_kamera_VALUE * 16 + VALUE; čeona_kamera_VALUE = -1; }
            }
            if (čeona_kamera_VALUE >= 0) { 단말.쓰기("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memorija_Datoteke.putanja_START(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Memorija_Datoteke.putanja_bajt(Loop_INDEX, Uredi_ime[Loop_INDEX]);
        int Datoteka = Memorija_Datoteke.otvoren(577); if (Datoteka < 0) { greška(Datoteka); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < promeniti_veličinu; Loop_INDEX++) Memorija_Datoteke.쓰기(Datoteka, Uređivano_Sadržaj[Loop_INDEX]);
        Memorija_Datoteke.Zatvori(Datoteka); 단말.쓰기("LOADED "); 단말.수(promeniti_veličinu); 단말.쓰기("bajt_VALUE(주기억 Datoteka)\n");
    }
    static int Alatke(int INDEX) {
        return alatka_stavka(INDEX, 1);
    }
    static int alatka_stavka(int INDEX, int koristiti) {
        if (token_COUNT - koristiti > 8) return -22;
        Tabla.인수준비(token_COUNT - koristiti);
        for (int 첫값 = koristiti; 첫값 < token_COUNT; 첫값++) {
            if (길이[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Tabla.argument_bajt(첫값 - koristiti, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Tabla.리눅스파일실행() : INDEX < 0 ? Tabla.Izvrši_korisnik_Datoteka() : Tabla.koristiti_korisnik_program(INDEX);
    }
    static int PYTHON_komplet() {
        if (token_COUNT > 8) return -22;
        Tabla.인수준비(token_COUNT);
        String putanja = "/lib/komplet.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int indeks_pozicije = 0;
        for (int 순번 = 0; 순번 < putanja.length(); 순번++) {
            int znak_VALUE = putanja.charAt(순번);
            if (znak_VALUE < 128) Tabla.argument_bajt(0, indeks_pozicije++, znak_VALUE);
            else { Tabla.argument_bajt(0, indeks_pozicije++, 0xe0 | (znak_VALUE >> 12)); Tabla.argument_bajt(0, indeks_pozicije++, 0x80 | ((znak_VALUE >> 6) & 63)); Tabla.argument_bajt(0, indeks_pozicije++, 0x80 | (znak_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (길이[순번] > 255) return -36;
            for (int znak_VALUE = 0; znak_VALUE < 길이[순번]; znak_VALUE++) Tabla.argument_bajt(순번, znak_VALUE, token_VALUE[시작점[순번] + znak_VALUE]);
        }
        return Tabla.koristiti_korisnik_program(12);
    }
    static int 실행형식() {
        int 처리값 = putanja(0); if (처리값 < 0) return 처리값;
        int Datoteka = Memorija_Datoteke.otvoren(0); if (Datoteka < 0) return Datoteka;
        int 첫값 = Memorija_Datoteke.읽기(Datoteka), bajt_podaci = Memorija_Datoteke.읽기(Datoteka), kôd_znaka = Memorija_Datoteke.읽기(Datoteka), 뒷값 = Memorija_Datoteke.읽기(Datoteka);
        Memorija_Datoteke.Zatvori(Datoteka);
        if (첫값 == 127 && bajt_podaci == 'E' && kôd_znaka == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bajt_podaci == 'K' && kôd_znaka == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        Tabla.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) Tabla.argument_bajt(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return Tabla.koristiti_korisnik_program(INDEX);
    }
    static void SMS_bajt(int Datoteka, int VALUE) { Memorija_Datoteke.쓰기(Datoteka, VALUE); }
    static void 정적파일(String ime, String Sadržaj_VALUE) {
        // komplet 파일명은 ASCII. Datoteka 내용은 UTF-8로 저장한다.
        Memorija_Datoteke.putanja_START(ime.length());
        for (int Loop_INDEX = 0; Loop_INDEX < ime.length(); Loop_INDEX++) Memorija_Datoteke.putanja_bajt(Loop_INDEX, ime.charAt(Loop_INDEX));
        int Datoteka = Memorija_Datoteke.otvoren(193); if (Datoteka < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Sadržaj_VALUE.length(); Loop_INDEX++) {
            int kôd_znaka = Sadržaj_VALUE.charAt(Loop_INDEX);
            if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && Loop_INDEX + 1 < Sadržaj_VALUE.length()) kôd_znaka = 0x10000 + ((kôd_znaka - 0xd800) << 10) + Sadržaj_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (kôd_znaka < 128) SMS_bajt(Datoteka, kôd_znaka);
            else {
                int 수 = kôd_znaka < 2048 ? 2 : kôd_znaka < 65536 ? 3 : 4;
                SMS_bajt(Datoteka, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kôd_znaka >> (6 * (수 - 1))));
                for (int stavka_COUNT_8f7753a1 = 수 - 1; stavka_COUNT_8f7753a1 > 0; stavka_COUNT_8f7753a1--) SMS_bajt(Datoteka, 0x80 | ((kôd_znaka >> (6 * (stavka_COUNT_8f7753a1 - 1))) & 63));
            }
        }
        Memorija_Datoteke.Zatvori(Datoteka);
    }
    static void 한글도움말() {
        단말.쓰기("F9 / Shift+Space: [EN] ↔ [sr_Latn]\n");
        단말.쓰기("  [SR_LATN] keyboard; [EN] ASCII\n");
        단말.쓰기("  [ → š\n");
        단말.쓰기("  F9: EN ↔ sr_Latn | Ctrl+Shift+V: UTF-8\n");
        단말.쓰기("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.쓰기("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String ime) {
        int bajt_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < ime.length(); Loop_INDEX++) { int kôd_znaka = ime.charAt(Loop_INDEX); if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) return -22; bajt_COUNT += kôd_znaka < 128 ? 1 : kôd_znaka < 2048 ? 2 : 3; }
        int 처리값 = Memorija_Datoteke.putanja_START(bajt_COUNT); if (처리값 < 0) return 처리값;
        int indeks_pozicije = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < ime.length(); Loop_INDEX++) {
            int kôd_znaka = ime.charAt(Loop_INDEX);
            if (kôd_znaka < 128) Memorija_Datoteke.putanja_bajt(indeks_pozicije++, kôd_znaka);
            else if (kôd_znaka < 2048) { Memorija_Datoteke.putanja_bajt(indeks_pozicije++, 0xc0 | (kôd_znaka >> 6)); Memorija_Datoteke.putanja_bajt(indeks_pozicije++, 0x80 | (kôd_znaka & 63)); }
            else { Memorija_Datoteke.putanja_bajt(indeks_pozicije++, 0xe0 | (kôd_znaka >> 12)); Memorija_Datoteke.putanja_bajt(indeks_pozicije++, 0x80 | ((kôd_znaka >> 6) & 63)); Memorija_Datoteke.putanja_bajt(indeks_pozicije++, 0x80 | (kôd_znaka & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String ime) {
        int 처리값 = 예제경로(ime); if (처리값 < 0) return 처리값;
        처리값 = Memorija_Datoteke.Create_Imenik(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String ime, String podaci) {
        int 처리값 = 예제경로(ime); if (처리값 < 0) return 처리값;
        int Datoteka = Memorija_Datoteke.otvoren(193); if (Datoteka == -17) return 0; if (Datoteka < 0) return Datoteka;
        for (int Loop_INDEX = 0; Loop_INDEX < podaci.length(); Loop_INDEX += 2) {
            처리값 = Memorija_Datoteke.쓰기(Datoteka, heksadecimalni_VALUE(podaci.charAt(Loop_INDEX)) * 16 + heksadecimalni_VALUE(podaci.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memorija_Datoteke.Zatvori(Datoteka); return 처리값; }
        }
        return Memorija_Datoteke.Zatvori(Datoteka);
    }
    static void emisija_pomoć_na_mreži() {
        sistem_alatka.emisija_pomoć_na_mreži();
        단말.쓰기("sshd / bezbedan_ljuska start|stop|status: SSH :22 (user, 장치별 lozinka_VALUE)\n");
        단말.쓰기("vncd / udaljen_ekran start|stop|status: VNC :5900 (장치별 lozinka_VALUE)\n");
        단말.쓰기("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.쓰기("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.쓰기("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.쓰기("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.쓰기("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.쓰기("모서리 + 왼쪽 버튼 prevući_VALUE: Terminal promeniti_veličinu promeniti_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.쓰기("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.쓰기("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.쓰기("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.쓰기("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.쓰기("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.쓰기("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.쓰기("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.쓰기("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.쓰기("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.쓰기("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.쓰기("pip: MicroPython izvor_stablo instaliraj_VALUE; host --network --pip 필요; /lib는 RAM\n");
        단말.쓰기("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.쓰기("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.쓰기("/example/java /example/c /example/python: examples ready at boot\n");
        단말.쓰기("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Tabla.Terminal(2) != 0) { Tabla.Terminal(0); 단말.쓰기("TERMINAL CLOSED\n"); }
        else if (Tabla.Terminal(1) < 0) greška(-19);
        else 단말.쓰기("TERMINAL READY — sr_Latn terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void komanda() {
        if (token_COUNT == 0) return;
        if (sistem_alatka.Izvrši_komanda()) return;
        if (같음(0,"sshd") || 같음(0,"bezbedan_ljuska") || 같음(0,"vncd") || 같음(0,"udaljen_ekran")) {
            int 종류=같음(0,"vncd")||같음(0,"udaljen_ekran")?1:0;
            int radnja=같음(1,"start")||같음(1,"koristiti")?1:같음(1,"stop")||같음(1,"Stani")?0:2;
            int Status_VALUE=Tabla.daljinska_kontrola(종류,radnja);
            if(Status_VALUE<0)greška(Status_VALUE);else 단말.쓰기(Tabla.daljinska_kontrola(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else emisija_pomoć_na_mreži(); }
        else if (같음(0, "info") || 같음(0, "i")) jezgro.msinfo32_exe();
        else if (같음(0, "pwd")) { Memorija_Datoteke.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Memorija_Datoteke.putanja_START(1); 처리값 = Memorija_Datoteke.putanja_bajt(0, '/'); } else 처리값 = token_COUNT == 2 ? putanja(1) : -22;
            if (처리값 >= 0) 처리값 = Memorija_Datoteke.promeniti_Imenik(); if (처리값 < 0) greška(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argument_INDEX) { Memorija_Datoteke.putanja_START(1); 처리값 = Memorija_Datoteke.putanja_bajt(0, '.'); } else 처리값 = token_COUNT == argument_INDEX + 1 ? putanja(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memorija_Datoteke.경로목록(); if (처리값 < 0) greška(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) ljuska_Alatke.Datoteka_Posao(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) ljuska_Alatke.instanca_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) ljuska_Alatke.Prikaz_VALUE();
        else if (같음(0, "wc")) ljuska_Alatke.세기();
        else if (같음(0, "grep")) ljuska_Alatke.FIND_stavka();
        else if (같음(0, "head") || 같음(0, "tail")) ljuska_Alatke.머리(같음(0, "tail"));
        else if (같음(0, "tee")) ljuska_Alatke.함께쓰기();
        else if (같음(0, "env")) ljuska_sintaksa.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) ljuska_sintaksa.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = ljuska_sintaksa.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { KR = 처리값; 단말.쓰기("komanda raščlaniti_VALUE: promenljiva_VALUE 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) ljuska_sintaksa.Izvrši_Datoteka();
        else if (같음(0, "true")) KR = 0;
        else if (같음(0, "false")) KR = 1;
        else if (같음(0, "history")) red_Uređivač.emisija_LOG();
        else if (같음(0, "exit")) {
            if (ljuska_sintaksa.깊이 > 0) { KR = token_COUNT == 1 ? ljuska_sintaksa.Status_VALUE : ljuska_Alatke.cifra_VALUE(1); if (KR < 0 || KR > 255) KR = 2; ljuska_sintaksa.skripta_završiti_razgovor = true; }
            else if (Tabla.Terminal(2) != 0) Terminal(true);
            else 단말.쓰기("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Uredi_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { KR = 2; 단말.쓰기("사용법: rm Datoteka...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = putanja(Loop_INDEX); if (처리값 == 0) 처리값 = Memorija_Datoteke.obrisati_stavka(); if (처리값 < 0) greška(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_pozicija = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_pozicija; 첫값 < token_COUNT; 첫값++) { if (첫값 > START_pozicija) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Tabla.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (START_pozicija == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.쓰기("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_komplet() : Alatke(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Alatke(13); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Alatke(15); KR = 처리값 < 0 ? 126 : 처리값; if (!ljuska_sintaksa.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Alatke(16); KR = 처리값 < 0 ? 126 : 처리값; if (!ljuska_sintaksa.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int promeniti_veličinu = Tabla.Terminal(13); 단말.쓰기("TERMINAL SIZE "); 단말.수(promeniti_veličinu & 65535); 단말.문자('x'); 단말.수(promeniti_veličinu >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tabla.Terminal(9); desktop.Izvrši_komanda(); }
        else if (같음(0, "c")) jezgro.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) jezgro.작업시험();
        else if (같음(0, "g")) jezgro.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) jezgro.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tabla.koristiti_korisnik_program(0); if (처리값 == 0) 단말.쓰기("ELF DEMO PASS\n"); else greška(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? alatka_stavka(-2, 2) : Alatke(-1); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) jezgro.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tabla.prenos_datoteka_usluga(1); if (처리값 < 0) greška(처리값); else { 단말.쓰기("FTP listening "); sistem_alatka.주소쓰기(Tabla.Mreža_status(0,0)); 단말.쓰기(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tabla.prenos_datoteka_usluga(0); 단말.쓰기("FTP stopped\n"); }
            else 단말.쓰기(Tabla.prenos_datoteka_usluga(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { komplet.Pripremi(); 단말.쓰기("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int jezik = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || jezik < 0) 단말.쓰기("example java|c|python: 출력, Datoteka, 네트워크, 그래픽, Java Swing prozor 예제\n");
            else { int 처리값 = 예제꾸러미.instaliraj_VALUE(jezik); if (처리값 < 0) { greška(처리값); if (처리값 == -28) 단말.쓰기("RAM full: remove unused files, then retry example\n"); } else 단말.쓰기("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = alatka_stavka(format_VALUE == 1 ? -1 : 14, 0); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !ljuska_sintaksa.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { KR = 126; 단말.쓰기("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { KR = 127; 단말.쓰기("Unknown command. help: commands\n"); }
        }
    }
    public static void Izvrši_komanda() {
        komplet.Pripremi();
        for (int jezik = 0; jezik < 3; jezik++) { int 처리값 = 예제꾸러미.instaliraj_VALUE(jezik); if (처리값 < 0) greška(처리값); }
        emisija_pomoć_na_mreži();
        while (true) {
            prozor_sesija.Proces_VALUE_stavka(); if (prozor_sesija.재개()) continue;
            if (!prozor_sesija.이어읽기) 단말.쓰기("jkoros-native> "); red_Uređivač.komandna_linija = true; Tabla.udaljen_čekaj(1); int promeniti_veličinu = 줄읽기(); Tabla.udaljen_čekaj(0); red_Uređivač.komandna_linija = false;
            if (promeniti_veličinu == -3) continue;
            if (promeniti_veličinu == -2) 단말.쓰기("komanda raščlaniti_VALUE: 명령줄이 너무 깁니다\n");
            if (promeniti_veličinu >= 0) { ljuska_sintaksa.skripta_završiti_razgovor = false; ljuska_sintaksa.Izvrši_komanda(red, 0, promeniti_veličinu, 0); } else ljuska_sintaksa.Status_VALUE = 130;
            Tabla.završiti_razgovor_udaljen_komanda(ljuska_sintaksa.Status_VALUE);
            red_Uređivač.promeniti_veličinu = red_Uređivač.kursor_VALUE = red_Uređivač.START_prozor = 0;
        }
    }
}
