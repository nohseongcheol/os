// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 komandrinda. Citāts, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Līniju = new int[4096], daļiņa_VALUE = new int[4096], 시작점 = new int[32], 길이 = new int[32];
    static int[] Rediģētie_Satura_rādītājs = new int[16384], Rediģēt_nosaukums = new int[63];
    static int daļiņa_COUNT, 편집이름길이, mērs;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Panelis.직렬쓰기(VALUE); }
    static int 줄읽기() { return rindiņas_redaktors.Lasīt(); }
    static boolean 나누기(int Izmērs) {
        int Novietojums = 0, 끝 = 0; daļiņa_COUNT = 0;
        while (Novietojums < Izmērs) {
            while (Novietojums < Izmērs && (Līniju[Novietojums] == 32 || Līniju[Novietojums] == 9)) Novietojums++;
            if (Novietojums == Izmērs) break;
            if (daļiņa_COUNT == 16) { 단말.Rakstīt("Komanda parsēt_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[daļiņa_COUNT] = 끝; int Citāts_VALUE = 0;
            while (Novietojums < Izmērs) {
                int VALUE = Līniju[Novietojums++];
                if (Citāts_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Citāts_VALUE) { Citāts_VALUE = 0; continue; }
                if (Citāts_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Citāts_VALUE = VALUE; continue; }
                daļiņa_VALUE[끝++] = VALUE;
            }
            if (Citāts_VALUE != 0) { 단말.Rakstīt("Komanda parsēt_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            길이[daļiņa_COUNT] = 끝 - 시작점[daļiņa_COUNT]; daļiņa_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= daļiņa_COUNT) return false;
        int pozīcijas_indekss=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int koda_punkts=Word_SMS.charAt(순번);
            if (koda_punkts>=0xd800 && koda_punkts<=0xdbff && 순번+1<Word_SMS.length()) koda_punkts=0x10000+((koda_punkts-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_COUNT=koda_punkts<128?1:koda_punkts<2048?2:koda_punkts<65536?3:4;
            for (int SEQUENCE_VALUE=byte_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=byte_COUNT==1?koda_punkts:SEQUENCE_VALUE==byte_COUNT-1?(byte_COUNT==2?0xc0:byte_COUNT==3?0xe0:0xf0)|(koda_punkts>>(6*SEQUENCE_VALUE)):0x80|((koda_punkts>>(6*SEQUENCE_VALUE))&63);
                if (pozīcijas_indekss>=길이[INDEX] || daļiņa_VALUE[시작점[INDEX]+pozīcijas_indekss++]!=VALUE) return false;
            }
        }
        return pozīcijas_indekss==길이[INDEX];
    }
    static int CEĻŠ(int INDEX) {
        if (INDEX >= daļiņa_COUNT) return -22;
        int mērs = atmiņa_Faili.ceļš_Sākt(길이[INDEX]); if (mērs < 0) return mērs;
        for (int Loop_INDEX = 0; Loop_INDEX < 길이[INDEX]; Loop_INDEX++) {
            mērs = atmiņa_Faili.ceļš_byte(Loop_INDEX, daļiņa_VALUE[시작점[INDEX] + Loop_INDEX]); if (mērs < 0) return mērs;
        }
        return 0;
    }
    static void Kļūda(int INDEX) { mērs = 1; 단말.Rakstīt("Kļūda "); 단말.numurs(INDEX); 단말.문자(10); }
    static void Skats_VALUE() {
        if (daļiņa_COUNT != 2) { 단말.Rakstīt("사용법: cat Fails\n"); return; }
        int mērs = CEĻŠ(1); if (mērs < 0) { Kļūda(mērs); return; }
        int Fails = atmiņa_Faili.Atvērt(0); if (Fails < 0) { Kļūda(Fails); return; }
        while (true) { int VALUE = atmiņa_Faili.Lasīt(Fails); if (VALUE == 256) break; if (VALUE < 0) { Kļūda(VALUE); break; } 원바이트(VALUE); }
        atmiņa_Faili.Aizvērt(Fails); 단말.문자(10);
    }
    static void Rediģēt_VALUE() {
        if (daļiņa_COUNT != 2) { 단말.Rakstīt("사용법: edit Fails\n"); return; }
        int mērs = CEĻŠ(1); if (mērs < 0) { Kļūda(mērs); return; }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Rediģēt_nosaukums[Loop_INDEX] = daļiņa_VALUE[시작점[1] + Loop_INDEX];
        단말.Rakstīt("EDIT: Fails 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Izmērs = 0;
        while (true) {
            단말.Rakstīt("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Rakstīt("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Līniju[0] == '.') break;
            if (입력 + 1 > Rediģētie_Satura_rādītājs.length - Izmērs) { 단말.Rakstīt("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Rediģētie_Satura_rādītājs[Izmērs++] = Līniju[Loop_INDEX];
            Rediģētie_Satura_rādītājs[Izmērs++] = 10;
        }
        atmiņa_Faili.ceļš_Sākt(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) atmiņa_Faili.ceļš_byte(Loop_INDEX, Rediģēt_nosaukums[Loop_INDEX]);
        int Fails = atmiņa_Faili.Atvērt(577); if (Fails < 0) { Kļūda(Fails); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Izmērs; Loop_INDEX++) atmiņa_Faili.Rakstīt(Fails, Rediģētie_Satura_rādītājs[Loop_INDEX]);
        atmiņa_Faili.Aizvērt(Fails); 단말.Rakstīt("SAVED "); 단말.numurs(Izmērs); 단말.Rakstīt("byte_VALUE(주기억 Fails)\n");
    }
    static int heksadecimāls_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (daļiņa_COUNT != 2) { 단말.Rakstīt("사용법: load Fails | hex Fails\n"); return; }
        int mērs = CEĻŠ(1); if (mērs < 0) { Kļūda(mērs); return; }
        if (!넣기) {
            int Fails = atmiņa_Faili.Atvērt(0); if (Fails < 0) { Kļūda(Fails); return; }
            단말.Rakstīt("HEX BEGIN "); 단말.numurs(atmiņa_Faili.Izmērs(Fails)); 단말.문자(10);
            int ievade_COUNT = 0;
            while (true) {
                int VALUE = atmiņa_Faili.Lasīt(Fails); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++ievade_COUNT % 32 == 0) 단말.문자(10);
            }
            if (ievade_COUNT % 32 != 0) 단말.문자(10);
            atmiņa_Faili.Aizvērt(Fails); 단말.Rakstīt("HEX END\n"); return;
        }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) Rediģēt_nosaukums[Loop_INDEX] = daļiņa_VALUE[시작점[1] + Loop_INDEX];
        단말.Rakstīt("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Izmērs = 0;
        while (true) {
            단말.Rakstīt("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Rakstīt("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Līniju[0] == '.') break;
            int priekšējā_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Līniju[Loop_INDEX] == 32 || Līniju[Loop_INDEX] == 9) continue;
                int VALUE = heksadecimāls_VALUE(Līniju[Loop_INDEX]);
                if (VALUE < 0 || Izmērs >= Rediģētie_Satura_rādītājs.length) { 단말.Rakstīt("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (priekšējā_VALUE < 0) priekšējā_VALUE = VALUE; else { Rediģētie_Satura_rādītājs[Izmērs++] = priekšējā_VALUE * 16 + VALUE; priekšējā_VALUE = -1; }
            }
            if (priekšējā_VALUE >= 0) { 단말.Rakstīt("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        atmiņa_Faili.ceļš_Sākt(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) atmiņa_Faili.ceļš_byte(Loop_INDEX, Rediģēt_nosaukums[Loop_INDEX]);
        int Fails = atmiņa_Faili.Atvērt(577); if (Fails < 0) { Kļūda(Fails); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Izmērs; Loop_INDEX++) atmiņa_Faili.Rakstīt(Fails, Rediģētie_Satura_rādītājs[Loop_INDEX]);
        atmiņa_Faili.Aizvērt(Fails); 단말.Rakstīt("LOADED "); 단말.numurs(Izmērs); 단말.Rakstīt("byte_VALUE(주기억 Fails)\n");
    }
    static int Rīki(int INDEX) {
        return rīks_ievade(INDEX, 1);
    }
    static int rīks_ievade(int INDEX, int Palaist) {
        if (daļiņa_COUNT - Palaist > 8) return -22;
        Panelis.인수준비(daļiņa_COUNT - Palaist);
        for (int 첫값 = Palaist; 첫값 < daļiņa_COUNT; 첫값++) {
            if (길이[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Panelis.arg_byte(첫값 - Palaist, Loop_INDEX, daļiņa_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Panelis.리눅스파일실행() : INDEX < 0 ? Panelis.Izpildīt_lietotājs_Fails() : Panelis.virkne_lietotājs_programma(INDEX);
    }
    static int PYTHON_saistīt() {
        if (daļiņa_COUNT > 8) return -22;
        Panelis.인수준비(daļiņa_COUNT);
        String CEĻŠ = "/lib/saistīt.py";
        // Java 문자열을 셸의 UTF-8 Parametri 버퍼에 기록한다.
        int pozīcijas_indekss = 0;
        for (int 순번 = 0; 순번 < CEĻŠ.length(); 순번++) {
            int rakstzīme_VALUE = CEĻŠ.charAt(순번);
            if (rakstzīme_VALUE < 128) Panelis.arg_byte(0, pozīcijas_indekss++, rakstzīme_VALUE);
            else { Panelis.arg_byte(0, pozīcijas_indekss++, 0xe0 | (rakstzīme_VALUE >> 12)); Panelis.arg_byte(0, pozīcijas_indekss++, 0x80 | ((rakstzīme_VALUE >> 6) & 63)); Panelis.arg_byte(0, pozīcijas_indekss++, 0x80 | (rakstzīme_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < daļiņa_COUNT; 순번++) {
            if (길이[순번] > 255) return -36;
            for (int rakstzīme_VALUE = 0; rakstzīme_VALUE < 길이[순번]; rakstzīme_VALUE++) Panelis.arg_byte(순번, rakstzīme_VALUE, daļiņa_VALUE[시작점[순번] + rakstzīme_VALUE]);
        }
        return Panelis.virkne_lietotājs_programma(12);
    }
    static int 실행형식() {
        int 처리값 = CEĻŠ(0); if (처리값 < 0) return 처리값;
        int Fails = atmiņa_Faili.Atvērt(0); if (Fails < 0) return Fails;
        int 첫값 = atmiņa_Faili.Lasīt(Fails), byte_dati = atmiņa_Faili.Lasīt(Fails), koda_punkts = atmiņa_Faili.Lasīt(Fails), 뒷값 = atmiņa_Faili.Lasīt(Fails);
        atmiņa_Faili.Aizvērt(Fails);
        if (첫값 == 127 && byte_dati == 'E' && koda_punkts == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_dati == 'K' && koda_punkts == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Parametri) {
        Panelis.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Parametri.length(); Loop_INDEX++) Panelis.arg_byte(0, Loop_INDEX, Parametri.charAt(Loop_INDEX));
        return Panelis.virkne_lietotājs_programma(INDEX);
    }
    static void SMS_byte(int Fails, int VALUE) { atmiņa_Faili.Rakstīt(Fails, VALUE); }
    static void 정적파일(String Nosaukums, String Saturs_VALUE) {
        // saistīt 파일명은 ASCII. Fails 내용은 UTF-8로 저장한다.
        atmiņa_Faili.ceļš_Sākt(Nosaukums.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Nosaukums.length(); Loop_INDEX++) atmiņa_Faili.ceļš_byte(Loop_INDEX, Nosaukums.charAt(Loop_INDEX));
        int Fails = atmiņa_Faili.Atvērt(193); if (Fails < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Saturs_VALUE.length(); Loop_INDEX++) {
            int koda_punkts = Saturs_VALUE.charAt(Loop_INDEX);
            if (koda_punkts >= 0xd800 && koda_punkts <= 0xdbff && Loop_INDEX + 1 < Saturs_VALUE.length()) koda_punkts = 0x10000 + ((koda_punkts - 0xd800) << 10) + Saturs_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (koda_punkts < 128) SMS_byte(Fails, koda_punkts);
            else {
                int numurs = koda_punkts < 2048 ? 2 : koda_punkts < 65536 ? 3 : 4;
                SMS_byte(Fails, (numurs == 2 ? 0xc0 : numurs == 3 ? 0xe0 : 0xf0) | (koda_punkts >> (6 * (numurs - 1))));
                for (int ievade_COUNT = numurs - 1; ievade_COUNT > 0; ievade_COUNT--) SMS_byte(Fails, 0x80 | ((koda_punkts >> (6 * (ievade_COUNT - 1))) & 63));
            }
        }
        atmiņa_Faili.Aizvērt(Fails);
    }
    static void 한글도움말() {
        단말.Rakstīt("F9 / Shift+Space: [EN] ↔ [lv]\n");
        단말.Rakstīt("  [LV] keyboard; [EN] ASCII\n");
        단말.Rakstīt("  a → a\n");
        단말.Rakstīt("  F9: EN ↔ lv | Ctrl+Shift+V: UTF-8\n");
        단말.Rakstīt("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Rakstīt("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nosaukums) {
        int byte_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nosaukums.length(); Loop_INDEX++) { int koda_punkts = Nosaukums.charAt(Loop_INDEX); if (koda_punkts >= 0xd800 && koda_punkts <= 0xdfff) return -22; byte_COUNT += koda_punkts < 128 ? 1 : koda_punkts < 2048 ? 2 : 3; }
        int 처리값 = atmiņa_Faili.ceļš_Sākt(byte_COUNT); if (처리값 < 0) return 처리값;
        int pozīcijas_indekss = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nosaukums.length(); Loop_INDEX++) {
            int koda_punkts = Nosaukums.charAt(Loop_INDEX);
            if (koda_punkts < 128) atmiņa_Faili.ceļš_byte(pozīcijas_indekss++, koda_punkts);
            else if (koda_punkts < 2048) { atmiņa_Faili.ceļš_byte(pozīcijas_indekss++, 0xc0 | (koda_punkts >> 6)); atmiņa_Faili.ceļš_byte(pozīcijas_indekss++, 0x80 | (koda_punkts & 63)); }
            else { atmiņa_Faili.ceļš_byte(pozīcijas_indekss++, 0xe0 | (koda_punkts >> 12)); atmiņa_Faili.ceļš_byte(pozīcijas_indekss++, 0x80 | ((koda_punkts >> 6) & 63)); atmiņa_Faili.ceļš_byte(pozīcijas_indekss++, 0x80 | (koda_punkts & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nosaukums) {
        int 처리값 = 예제경로(Nosaukums); if (처리값 < 0) return 처리값;
        처리값 = atmiņa_Faili.atvērt_Direktorijs(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nosaukums, String dati) {
        int 처리값 = 예제경로(Nosaukums); if (처리값 < 0) return 처리값;
        int Fails = atmiņa_Faili.Atvērt(193); if (Fails == -17) return 0; if (Fails < 0) return Fails;
        for (int Loop_INDEX = 0; Loop_INDEX < dati.length(); Loop_INDEX += 2) {
            처리값 = atmiņa_Faili.Rakstīt(Fails, heksadecimāls_VALUE(dati.charAt(Loop_INDEX)) * 16 + heksadecimāls_VALUE(dati.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { atmiņa_Faili.Aizvērt(Fails); return 처리값; }
        }
        return atmiņa_Faili.Aizvērt(Fails);
    }
    static void rādīt_palīdzība() {
        sistēma_rīks.rādīt_palīdzība();
        단말.Rakstīt("sshd / drošs_čaula start|stop|status: SSH :22 (user, 장치별 parole_VALUE)\n");
        단말.Rakstīt("vncd / attāls_rādīt start|stop|status: VNC :5900 (장치별 parole_VALUE)\n");
        단말.Rakstīt("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Rakstīt("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Rakstīt("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Rakstīt("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Rakstīt("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Rakstīt("모서리 + 왼쪽 버튼 vilkt_VALUE: Terminālis Izmērs mainīt_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Rakstīt("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Rakstīt("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Rakstīt("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Rakstīt("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Rakstīt("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Rakstīt("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Rakstīt("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Rakstīt("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Rakstīt("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Rakstīt("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Rakstīt("pip: MicroPython avots_koks instalēt_VALUE; viesot --network --pip 필요; /lib는 RAM\n");
        단말.Rakstīt("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Rakstīt("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Rakstīt("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Rakstīt("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminālis(boolean 전환여부) {
        if (전환여부 && Panelis.Terminālis(2) != 0) { Panelis.Terminālis(0); 단말.Rakstīt("TERMINAL CLOSED\n"); }
        else if (Panelis.Terminālis(1) < 0) Kļūda(-19);
        else 단말.Rakstīt("TERMINAL READY — lv terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Komanda() {
        if (daļiņa_COUNT == 0) return;
        if (sistēma_rīks.Izpildīt_komanda()) return;
        if (같음(0,"sshd") || 같음(0,"drošs_čaula") || 같음(0,"vncd") || 같음(0,"attāls_rādīt")) {
            int 종류=같음(0,"vncd")||같음(0,"attāls_rādīt")?1:0;
            int Darbība=같음(1,"start")||같음(1,"Palaist")?1:같음(1,"stop")||같음(1,"Pārtraukt")?0:2;
            int Statuss_VALUE=Panelis.attālā_vadība(종류,Darbība);
            if(Statuss_VALUE<0)Kļūda(Statuss_VALUE);else 단말.Rakstīt(Panelis.attālā_vadība(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else rādīt_palīdzība(); }
        else if (같음(0, "info") || 같음(0, "i")) kodols.msinfo32_exe();
        else if (같음(0, "pwd")) { atmiņa_Faili.pašreizējais_rakstīšana(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (daļiņa_COUNT == 1) { atmiņa_Faili.ceļš_Sākt(1); 처리값 = atmiņa_Faili.ceļš_byte(0, '/'); } else 처리값 = daļiņa_COUNT == 2 ? CEĻŠ(1) : -22;
            if (처리값 >= 0) 처리값 = atmiņa_Faili.mainīt_Direktorijs(); if (처리값 < 0) Kļūda(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int arg_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (daļiņa_COUNT == arg_INDEX) { atmiņa_Faili.ceļš_Sākt(1); 처리값 = atmiņa_Faili.ceļš_byte(0, '.'); } else 처리값 = daļiņa_COUNT == arg_INDEX + 1 ? CEĻŠ(arg_INDEX) : -22;
            if (처리값 >= 0) 처리값 = atmiņa_Faili.경로목록(); if (처리값 < 0) Kļūda(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) čaula_Rīki.Fails_Darbs(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) čaula_Rīki.kopēt_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) čaula_Rīki.Skats_VALUE();
        else if (같음(0, "wc")) čaula_Rīki.세기();
        else if (같음(0, "grep")) čaula_Rīki.FIND_ievade();
        else if (같음(0, "head") || 같음(0, "tail")) čaula_Rīki.머리(같음(0, "tail"));
        else if (같음(0, "tee")) čaula_Rīki.rakstīšana_Kopā();
        else if (같음(0, "env")) čaula_sintakse.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (daļiņa_COUNT == 1) čaula_sintakse.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < daļiņa_COUNT; Loop_INDEX++) { int 처리값 = čaula_sintakse.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { mērs = 처리값; 단말.Rakstīt("Komanda parsēt_VALUE: mainīgais_VALUE 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) čaula_sintakse.Izpildīt_Fails();
        else if (같음(0, "true")) mērs = 0;
        else if (같음(0, "false")) mērs = 1;
        else if (같음(0, "history")) rindiņas_redaktors.rādīt_LOG();
        else if (같음(0, "exit")) {
            if (čaula_sintakse.깊이 > 0) { mērs = daļiņa_COUNT == 1 ? čaula_sintakse.Statuss_VALUE : čaula_Rīki.cipars_VALUE(1); if (mērs < 0 || mērs > 255) mērs = 2; čaula_sintakse.skripts_beigt_zvanu = true; }
            else if (Panelis.Terminālis(2) != 0) Terminālis(true);
            else 단말.Rakstīt("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Rediģēt_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (daļiņa_COUNT < 2) { mērs = 2; 단말.Rakstīt("사용법: rm Fails...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < daļiņa_COUNT; Loop_INDEX++) { int 처리값 = CEĻŠ(Loop_INDEX); if (처리값 == 0) 처리값 = atmiņa_Faili.dzēst_ievade(); if (처리값 < 0) Kļūda(처리값); }
        }
        else if (같음(0, "echo")) {
            int Sākt_amats = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Sākt_amats; 첫값 < daļiņa_COUNT; 첫값++) { if (첫값 > Sākt_amats) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Panelis.직렬쓰기(daļiņa_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Sākt_amats == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Rakstīt("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_saistīt() : Rīki(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); mērs = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !čaula_sintakse.연결중) { 단말.Rakstīt("exit "); 단말.numurs(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Rīki(13); mērs = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Rīki(15); mērs = 처리값 < 0 ? 126 : 처리값; if (!čaula_sintakse.연결중) { 단말.Rakstīt("exit "); 단말.numurs(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Rīki(16); mērs = 처리값 < 0 ? 126 : 처리값; if (!čaula_sintakse.연결중) { 단말.Rakstīt("exit "); 단말.numurs(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Izmērs = Panelis.Terminālis(13); 단말.Rakstīt("TERMINAL SIZE "); 단말.numurs(Izmērs & 65535); 단말.문자('x'); 단말.numurs(Izmērs >>> 16); 단말.문자(10); }
            else Terminālis(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Panelis.Terminālis(9); dators.Izpildīt_komanda(); }
        else if (같음(0, "c")) kodols.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kodols.작업시험();
        else if (같음(0, "g")) kodols.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kodols.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Panelis.virkne_lietotājs_programma(0); if (처리값 == 0) 단말.Rakstīt("ELF DEMO PASS\n"); else Kļūda(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? rīks_ievade(-2, 2) : Rīki(-1); mērs = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !čaula_sintakse.연결중) { 단말.Rakstīt("exit "); 단말.numurs(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kodols.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Panelis.faila_pārsūtīšana_serviss(1); if (처리값 < 0) Kļūda(처리값); else { 단말.Rakstīt("FTP listening "); sistēma_rīks.rakstīšana_adrese(Panelis.tīkls_statuss(0,0)); 단말.Rakstīt(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Panelis.faila_pārsūtīšana_serviss(0); 단말.Rakstīt("FTP stopped\n"); }
            else 단말.Rakstīt(Panelis.faila_pārsūtīšana_serviss(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { saistīt.Sagatavot(); 단말.Rakstīt("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Valodas = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (daļiņa_COUNT != 2 || Valodas < 0) 단말.Rakstīt("example java|c|python: Izvade, Fails, 네트워크, 그래픽, Java Swing Logs 예제\n");
            else { int 처리값 = 예제꾸러미.instalēt_VALUE(Valodas); if (처리값 < 0) { Kļūda(처리값); if (처리값 == -28) 단말.Rakstīt("RAM full: remove unused files, then retry example\n"); } else 단말.Rakstīt("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formāts_VALUE = 실행형식();
            if (formāts_VALUE == 1 || formāts_VALUE == 2) {
                int 처리값 = rīks_ievade(formāts_VALUE == 1 ? -1 : 14, 0); mērs = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !čaula_sintakse.연결중) { 단말.Rakstīt("exit "); 단말.numurs(처리값); 단말.문자(10); }
            } else if (formāts_VALUE == 0) { mērs = 126; 단말.Rakstīt("실행할 numurs 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { mērs = 127; 단말.Rakstīt("Unknown command. help: commands\n"); }
        }
    }
    public static void Izpildīt_komanda() {
        saistīt.Sagatavot();
        for (int Valodas = 0; Valodas < 3; Valodas++) { int 처리값 = 예제꾸러미.instalēt_VALUE(Valodas); if (처리값 < 0) Kļūda(처리값); }
        rādīt_palīdzība();
        while (true) {
            logs_sesija.Process_VALUE_ievade(); if (logs_sesija.재개()) continue;
            if (!logs_sesija.이어읽기) 단말.Rakstīt("jkoros-native> "); rindiņas_redaktors.komandrinda = true; Panelis.attāls_pagaidi(1); int Izmērs = 줄읽기(); Panelis.attāls_pagaidi(0); rindiņas_redaktors.komandrinda = false;
            if (Izmērs == -3) continue;
            if (Izmērs == -2) 단말.Rakstīt("Komanda parsēt_VALUE: 명령줄이 너무 깁니다\n");
            if (Izmērs >= 0) { čaula_sintakse.skripts_beigt_zvanu = false; čaula_sintakse.Izpildīt_komanda(Līniju, 0, Izmērs, 0); } else čaula_sintakse.Statuss_VALUE = 130;
            Panelis.beigt_zvanu_attāls_komanda(čaula_sintakse.Statuss_VALUE);
            rindiņas_redaktors.Izmērs = rindiņas_redaktors.kursors_VALUE = rindiņas_redaktors.Sākt_logs = 0;
        }
    }
}
