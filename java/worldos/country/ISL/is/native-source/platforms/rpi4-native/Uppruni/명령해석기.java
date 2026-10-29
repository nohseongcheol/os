// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 skipanalína. Tilvitnun, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Lína = new int[4096], tákn_VALUE_eb540501 = new int[4096], 시작점 = new int[32], lengd_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], breyta_heiti = new int[63];
    static int tákn_COUNT, breyta_heiti_lengd, NIÐURSTAÐA;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { bretti.직렬쓰기(VALUE); }
    static int 줄읽기() { return lína_ritill.Lestur(); }
    static boolean 나누기(int Stærð) {
        int Staðsetning = 0, 끝 = 0; tákn_COUNT = 0;
        while (Staðsetning < Stærð) {
            while (Staðsetning < Stærð && (Lína[Staðsetning] == 32 || Lína[Staðsetning] == 9)) Staðsetning++;
            if (Staðsetning == Stærð) break;
            if (tákn_COUNT == 16) { 단말.Skrift("Skipun þátta_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[tákn_COUNT] = 끝; int Tilvitnun_VALUE = 0;
            while (Staðsetning < Stærð) {
                int VALUE = Lína[Staðsetning++];
                if (Tilvitnun_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Tilvitnun_VALUE) { Tilvitnun_VALUE = 0; continue; }
                if (Tilvitnun_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Tilvitnun_VALUE = VALUE; continue; }
                tákn_VALUE_eb540501[끝++] = VALUE;
            }
            if (Tilvitnun_VALUE != 0) { 단말.Skrift("Skipun þátta_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            lengd_VALUE[tákn_COUNT] = 끝 - 시작점[tákn_COUNT]; tákn_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= tákn_COUNT) return false;
        int staða_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int stafkóði=Word_SMS.charAt(순번);
            if (stafkóði>=0xd800 && stafkóði<=0xdbff && 순번+1<Word_SMS.length()) stafkóði=0x10000+((stafkóði-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bæti_COUNT=stafkóði<128?1:stafkóði<2048?2:stafkóði<65536?3:4;
            for (int SEQUENCE_VALUE=bæti_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bæti_COUNT==1?stafkóði:SEQUENCE_VALUE==bæti_COUNT-1?(bæti_COUNT==2?0xc0:bæti_COUNT==3?0xe0:0xf0)|(stafkóði>>(6*SEQUENCE_VALUE)):0x80|((stafkóði>>(6*SEQUENCE_VALUE))&63);
                if (staða_INDEX>=lengd_VALUE[INDEX] || tákn_VALUE_eb540501[시작점[INDEX]+staða_INDEX++]!=VALUE) return false;
            }
        }
        return staða_INDEX==lengd_VALUE[INDEX];
    }
    static int SLÓÐ(int INDEX) {
        if (INDEX >= tákn_COUNT) return -22;
        int NIÐURSTAÐA = Minni_Skrár.slóð_Opna(lengd_VALUE[INDEX]); if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        for (int Loop_INDEX = 0; Loop_INDEX < lengd_VALUE[INDEX]; Loop_INDEX++) {
            NIÐURSTAÐA = Minni_Skrár.slóð_bæti(Loop_INDEX, tákn_VALUE_eb540501[시작점[INDEX] + Loop_INDEX]); if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        }
        return 0;
    }
    static void Villa(int INDEX) { NIÐURSTAÐA = 1; 단말.Skrift("Villa "); 단말.númer(INDEX); 단말.문자(10); }
    static void Sýn_VALUE() {
        if (tákn_COUNT != 2) { 단말.Skrift("사용법: cat Skrá\n"); return; }
        int NIÐURSTAÐA = SLÓÐ(1); if (NIÐURSTAÐA < 0) { Villa(NIÐURSTAÐA); return; }
        int Skrá = Minni_Skrár.Opna(0); if (Skrá < 0) { Villa(Skrá); return; }
        while (true) { int VALUE = Minni_Skrár.Lestur(Skrá); if (VALUE == 256) break; if (VALUE < 0) { Villa(VALUE); break; } 원바이트(VALUE); }
        Minni_Skrár.Loka(Skrá); 단말.문자(10);
    }
    static void breyta_VALUE() {
        if (tákn_COUNT != 2) { 단말.Skrift("사용법: edit Skrá\n"); return; }
        int NIÐURSTAÐA = SLÓÐ(1); if (NIÐURSTAÐA < 0) { Villa(NIÐURSTAÐA); return; }
        breyta_heiti_lengd = lengd_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < breyta_heiti_lengd; Loop_INDEX++) breyta_heiti[Loop_INDEX] = tákn_VALUE_eb540501[시작점[1] + Loop_INDEX];
        단말.Skrift("EDIT: Skrá 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Stærð = 0;
        while (true) {
            단말.Skrift("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Skrift("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Lína[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Stærð) { 단말.Skrift("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[Stærð++] = Lína[Loop_INDEX];
            편집내용[Stærð++] = 10;
        }
        Minni_Skrár.slóð_Opna(breyta_heiti_lengd);
        for (int Loop_INDEX = 0; Loop_INDEX < breyta_heiti_lengd; Loop_INDEX++) Minni_Skrár.slóð_bæti(Loop_INDEX, breyta_heiti[Loop_INDEX]);
        int Skrá = Minni_Skrár.Opna(577); if (Skrá < 0) { Villa(Skrá); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Stærð; Loop_INDEX++) Minni_Skrár.Skrift(Skrá, 편집내용[Loop_INDEX]);
        Minni_Skrár.Loka(Skrá); 단말.Skrift("SAVED "); 단말.númer(Stærð); 단말.Skrift("bæti_VALUE(주기억 Skrá)\n");
    }
    static int sextándakerfi_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (tákn_COUNT != 2) { 단말.Skrift("사용법: load Skrá | hex Skrá\n"); return; }
        int NIÐURSTAÐA = SLÓÐ(1); if (NIÐURSTAÐA < 0) { Villa(NIÐURSTAÐA); return; }
        if (!넣기) {
            int Skrá = Minni_Skrár.Opna(0); if (Skrá < 0) { Villa(Skrá); return; }
            단말.Skrift("HEX BEGIN "); 단말.númer(Minni_Skrár.Stærð(Skrá)); 단말.문자(10);
            int færsla_COUNT = 0;
            while (true) {
                int VALUE = Minni_Skrár.Lestur(Skrá); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++færsla_COUNT % 32 == 0) 단말.문자(10);
            }
            if (færsla_COUNT % 32 != 0) 단말.문자(10);
            Minni_Skrár.Loka(Skrá); 단말.Skrift("HEX END\n"); return;
        }
        breyta_heiti_lengd = lengd_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < breyta_heiti_lengd; Loop_INDEX++) breyta_heiti[Loop_INDEX] = tákn_VALUE_eb540501[시작점[1] + Loop_INDEX];
        단말.Skrift("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Stærð = 0;
        while (true) {
            단말.Skrift("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Skrift("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Lína[0] == '.') break;
            int myndavél_að_framan_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Lína[Loop_INDEX] == 32 || Lína[Loop_INDEX] == 9) continue;
                int VALUE = sextándakerfi_VALUE(Lína[Loop_INDEX]);
                if (VALUE < 0 || Stærð >= 편집내용.length) { 단말.Skrift("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (myndavél_að_framan_VALUE < 0) myndavél_að_framan_VALUE = VALUE; else { 편집내용[Stærð++] = myndavél_að_framan_VALUE * 16 + VALUE; myndavél_að_framan_VALUE = -1; }
            }
            if (myndavél_að_framan_VALUE >= 0) { 단말.Skrift("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Minni_Skrár.slóð_Opna(breyta_heiti_lengd);
        for (int Loop_INDEX = 0; Loop_INDEX < breyta_heiti_lengd; Loop_INDEX++) Minni_Skrár.slóð_bæti(Loop_INDEX, breyta_heiti[Loop_INDEX]);
        int Skrá = Minni_Skrár.Opna(577); if (Skrá < 0) { Villa(Skrá); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Stærð; Loop_INDEX++) Minni_Skrár.Skrift(Skrá, 편집내용[Loop_INDEX]);
        Minni_Skrár.Loka(Skrá); 단말.Skrift("LOADED "); 단말.númer(Stærð); 단말.Skrift("bæti_VALUE(주기억 Skrá)\n");
    }
    static int Verkfæri(int INDEX) {
        return verkfæri_færsla(INDEX, 1);
    }
    static int verkfæri_færsla(int INDEX, int Keyra_2) {
        if (tákn_COUNT - Keyra_2 > 8) return -22;
        bretti.인수준비(tákn_COUNT - Keyra_2);
        for (int 첫값 = Keyra_2; 첫값 < tákn_COUNT; 첫값++) {
            if (lengd_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < lengd_VALUE[첫값]; Loop_INDEX++) bretti.frumbreyta_bæti(첫값 - Keyra_2, Loop_INDEX, tákn_VALUE_eb540501[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? bretti.리눅스파일실행() : INDEX < 0 ? bretti.keyra_notandi_skrá() : bretti.runa_notandi_forrit(INDEX);
    }
    static int PYTHON_búnt() {
        if (tákn_COUNT > 8) return -22;
        bretti.인수준비(tákn_COUNT);
        String SLÓÐ = "/lib/búnt.py";
        // Java 문자열을 셸의 UTF-8 Viðföng 버퍼에 기록한다.
        int staða_INDEX = 0;
        for (int 순번 = 0; 순번 < SLÓÐ.length(); 순번++) {
            int stafur_VALUE = SLÓÐ.charAt(순번);
            if (stafur_VALUE < 128) bretti.frumbreyta_bæti(0, staða_INDEX++, stafur_VALUE);
            else { bretti.frumbreyta_bæti(0, staða_INDEX++, 0xe0 | (stafur_VALUE >> 12)); bretti.frumbreyta_bæti(0, staða_INDEX++, 0x80 | ((stafur_VALUE >> 6) & 63)); bretti.frumbreyta_bæti(0, staða_INDEX++, 0x80 | (stafur_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < tákn_COUNT; 순번++) {
            if (lengd_VALUE[순번] > 255) return -36;
            for (int stafur_VALUE = 0; stafur_VALUE < lengd_VALUE[순번]; stafur_VALUE++) bretti.frumbreyta_bæti(순번, stafur_VALUE, tákn_VALUE_eb540501[시작점[순번] + stafur_VALUE]);
        }
        return bretti.runa_notandi_forrit(12);
    }
    static int 실행형식() {
        int 처리값 = SLÓÐ(0); if (처리값 < 0) return 처리값;
        int Skrá = Minni_Skrár.Opna(0); if (Skrá < 0) return Skrá;
        int 첫값 = Minni_Skrár.Lestur(Skrá), bæti_gögn = Minni_Skrár.Lestur(Skrá), stafkóði = Minni_Skrár.Lestur(Skrá), 뒷값 = Minni_Skrár.Lestur(Skrá);
        Minni_Skrár.Loka(Skrá);
        if (첫값 == 127 && bæti_gögn == 'E' && stafkóði == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bæti_gögn == 'K' && stafkóði == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Viðföng) {
        bretti.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Viðföng.length(); Loop_INDEX++) bretti.frumbreyta_bæti(0, Loop_INDEX, Viðföng.charAt(Loop_INDEX));
        return bretti.runa_notandi_forrit(INDEX);
    }
    static void SMS_bæti(int Skrá, int VALUE) { Minni_Skrár.Skrift(Skrá, VALUE); }
    static void fast_skrá(String Heiti, String Efni_VALUE) {
        // búnt 파일명은 ASCII. Skrá 내용은 UTF-8로 저장한다.
        Minni_Skrár.slóð_Opna(Heiti.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Heiti.length(); Loop_INDEX++) Minni_Skrár.slóð_bæti(Loop_INDEX, Heiti.charAt(Loop_INDEX));
        int Skrá = Minni_Skrár.Opna(193); if (Skrá < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Efni_VALUE.length(); Loop_INDEX++) {
            int stafkóði = Efni_VALUE.charAt(Loop_INDEX);
            if (stafkóði >= 0xd800 && stafkóði <= 0xdbff && Loop_INDEX + 1 < Efni_VALUE.length()) stafkóði = 0x10000 + ((stafkóði - 0xd800) << 10) + Efni_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (stafkóði < 128) SMS_bæti(Skrá, stafkóði);
            else {
                int númer = stafkóði < 2048 ? 2 : stafkóði < 65536 ? 3 : 4;
                SMS_bæti(Skrá, (númer == 2 ? 0xc0 : númer == 3 ? 0xe0 : 0xf0) | (stafkóði >> (6 * (númer - 1))));
                for (int færsla_COUNT = númer - 1; færsla_COUNT > 0; færsla_COUNT--) SMS_bæti(Skrá, 0x80 | ((stafkóði >> (6 * (færsla_COUNT - 1))) & 63));
            }
        }
        Minni_Skrár.Loka(Skrá);
    }
    static void 한글도움말() {
        단말.Skrift("F9 / Shift+Space: [EN] ↔ [is]\n");
        단말.Skrift("  [IS] keyboard; [EN] ASCII\n");
        단말.Skrift("  _ → Ö\n");
        단말.Skrift("  F9: EN ↔ is | Ctrl+Shift+V: UTF-8\n");
        단말.Skrift("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Skrift("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Heiti) {
        int bæti_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Heiti.length(); Loop_INDEX++) { int stafkóði = Heiti.charAt(Loop_INDEX); if (stafkóði >= 0xd800 && stafkóði <= 0xdfff) return -22; bæti_COUNT += stafkóði < 128 ? 1 : stafkóði < 2048 ? 2 : 3; }
        int 처리값 = Minni_Skrár.slóð_Opna(bæti_COUNT); if (처리값 < 0) return 처리값;
        int staða_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Heiti.length(); Loop_INDEX++) {
            int stafkóði = Heiti.charAt(Loop_INDEX);
            if (stafkóði < 128) Minni_Skrár.slóð_bæti(staða_INDEX++, stafkóði);
            else if (stafkóði < 2048) { Minni_Skrár.slóð_bæti(staða_INDEX++, 0xc0 | (stafkóði >> 6)); Minni_Skrár.slóð_bæti(staða_INDEX++, 0x80 | (stafkóði & 63)); }
            else { Minni_Skrár.slóð_bæti(staða_INDEX++, 0xe0 | (stafkóði >> 12)); Minni_Skrár.slóð_bæti(staða_INDEX++, 0x80 | ((stafkóði >> 6) & 63)); Minni_Skrár.slóð_bæti(staða_INDEX++, 0x80 | (stafkóði & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Heiti) {
        int 처리값 = 예제경로(Heiti); if (처리값 < 0) return 처리값;
        처리값 = Minni_Skrár.stofna_skráasafn(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Heiti, String gögn) {
        int 처리값 = 예제경로(Heiti); if (처리값 < 0) return 처리값;
        int Skrá = Minni_Skrár.Opna(193); if (Skrá == -17) return 0; if (Skrá < 0) return Skrá;
        for (int Loop_INDEX = 0; Loop_INDEX < gögn.length(); Loop_INDEX += 2) {
            처리값 = Minni_Skrár.Skrift(Skrá, sextándakerfi_VALUE(gögn.charAt(Loop_INDEX)) * 16 + sextándakerfi_VALUE(gögn.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Minni_Skrár.Loka(Skrá); return 처리값; }
        }
        return Minni_Skrár.Loka(Skrá);
    }
    static void sýna_hjálp() {
        kerfi_verkfæri.sýna_hjálp();
        단말.Skrift("sshd / öruggt_skel start|stop|status: SSH :22 (user, 장치별 aðgangsorð_VALUE)\n");
        단말.Skrift("vncd / fjartengdur_birta start|stop|status: VNC :5900 (장치별 aðgangsorð_VALUE)\n");
        단말.Skrift("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Skrift("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Skrift("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Skrift("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Skrift("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Skrift("모서리 + 왼쪽 버튼 draga_VALUE: Skjáhermir Stærð breyta_VALUE_16f64fe4; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Skrift("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Skrift("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Skrift("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Skrift("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Skrift("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Skrift("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Skrift("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Skrift("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Skrift("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Skrift("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Skrift("pip: MicroPython uppruni_tré setja_upp_VALUE; hýsa --network --pip 필요; /lib는 RAM\n");
        단말.Skrift("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Skrift("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Skrift("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Skrift("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Skjáhermir(boolean 전환여부) {
        if (전환여부 && bretti.Skjáhermir(2) != 0) { bretti.Skjáhermir(0); 단말.Skrift("TERMINAL CLOSED\n"); }
        else if (bretti.Skjáhermir(1) < 0) Villa(-19);
        else 단말.Skrift("TERMINAL READY — is terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Skipun() {
        if (tákn_COUNT == 0) return;
        if (kerfi_verkfæri.keyra_skipun()) return;
        if (같음(0,"sshd") || 같음(0,"öruggt_skel") || 같음(0,"vncd") || 같음(0,"fjartengdur_birta")) {
            int 종류=같음(0,"vncd")||같음(0,"fjartengdur_birta")?1:0;
            int Aðgerð=같음(1,"start")||같음(1,"Keyra_2")?1:같음(1,"stop")||같음(1,"Stopp")?0:2;
            int staða_VALUE_e10195a1=bretti.fjarvöktun(종류,Aðgerð);
            if(staða_VALUE_e10195a1<0)Villa(staða_VALUE_e10195a1);else 단말.Skrift(bretti.fjarvöktun(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else sýna_hjálp(); }
        else if (같음(0, "info") || 같음(0, "i")) kjarni.msinfo32_exe();
        else if (같음(0, "pwd")) { Minni_Skrár.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (tákn_COUNT == 1) { Minni_Skrár.slóð_Opna(1); 처리값 = Minni_Skrár.slóð_bæti(0, '/'); } else 처리값 = tákn_COUNT == 2 ? SLÓÐ(1) : -22;
            if (처리값 >= 0) 처리값 = Minni_Skrár.breyta_skráasafn(); if (처리값 < 0) Villa(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int frumbreyta_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (tákn_COUNT == frumbreyta_INDEX) { Minni_Skrár.slóð_Opna(1); 처리값 = Minni_Skrár.slóð_bæti(0, '.'); } else 처리값 = tákn_COUNT == frumbreyta_INDEX + 1 ? SLÓÐ(frumbreyta_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Minni_Skrár.경로목록(); if (처리값 < 0) Villa(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) skel_Verkfæri.skrá_mál(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) skel_Verkfæri.afrita_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) skel_Verkfæri.Sýn_VALUE();
        else if (같음(0, "wc")) skel_Verkfæri.세기();
        else if (같음(0, "grep")) skel_Verkfæri.FIND_færsla();
        else if (같음(0, "head") || 같음(0, "tail")) skel_Verkfæri.머리(같음(0, "tail"));
        else if (같음(0, "tee")) skel_Verkfæri.함께쓰기();
        else if (같음(0, "env")) skel_málskipan.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (tákn_COUNT == 1) skel_málskipan.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < tákn_COUNT; Loop_INDEX++) { int 처리값 = skel_málskipan.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { NIÐURSTAÐA = 처리값; 단말.Skrift("Skipun þátta_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) skel_málskipan.keyra_skrá();
        else if (같음(0, "true")) NIÐURSTAÐA = 0;
        else if (같음(0, "false")) NIÐURSTAÐA = 1;
        else if (같음(0, "history")) lína_ritill.sýna_LOG();
        else if (같음(0, "exit")) {
            if (skel_málskipan.깊이 > 0) { NIÐURSTAÐA = tákn_COUNT == 1 ? skel_málskipan.staða_VALUE_e10195a1 : skel_Verkfæri.tölustafur_VALUE(1); if (NIÐURSTAÐA < 0 || NIÐURSTAÐA > 255) NIÐURSTAÐA = 2; skel_málskipan.forskrift_ljúka = true; }
            else if (bretti.Skjáhermir(2) != 0) Skjáhermir(true);
            else 단말.Skrift("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) breyta_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (tákn_COUNT < 2) { NIÐURSTAÐA = 2; 단말.Skrift("사용법: rm Skrá...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < tákn_COUNT; Loop_INDEX++) { int 처리값 = SLÓÐ(Loop_INDEX); if (처리값 == 0) 처리값 = Minni_Skrár.eyða_færsla(); if (처리값 < 0) Villa(처리값); }
        }
        else if (같음(0, "echo")) {
            int Opna_staða = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Opna_staða; 첫값 < tákn_COUNT; 첫값++) { if (첫값 > Opna_staða) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < lengd_VALUE[첫값]; Loop_INDEX++) bretti.직렬쓰기(tákn_VALUE_eb540501[시작점[첫값] + Loop_INDEX]); }
            if (Opna_staða == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Skrift("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_búnt() : Verkfæri(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); NIÐURSTAÐA = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !skel_málskipan.연결중) { 단말.Skrift("exit "); 단말.númer(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Verkfæri(13); NIÐURSTAÐA = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Verkfæri(15); NIÐURSTAÐA = 처리값 < 0 ? 126 : 처리값; if (!skel_málskipan.연결중) { 단말.Skrift("exit "); 단말.númer(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Verkfæri(16); NIÐURSTAÐA = 처리값 < 0 ? 126 : 처리값; if (!skel_málskipan.연결중) { 단말.Skrift("exit "); 단말.númer(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Stærð = bretti.Skjáhermir(13); 단말.Skrift("TERMINAL SIZE "); 단말.númer(Stærð & 65535); 단말.문자('x'); 단말.númer(Stærð >>> 16); 단말.문자(10); }
            else Skjáhermir(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { bretti.Skjáhermir(9); skjáborð.keyra_skipun(); }
        else if (같음(0, "c")) kjarni.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kjarni.작업시험();
        else if (같음(0, "g")) kjarni.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kjarni.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = bretti.runa_notandi_forrit(0); if (처리값 == 0) 단말.Skrift("ELF DEMO PASS\n"); else Villa(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? verkfæri_færsla(-2, 2) : Verkfæri(-1); NIÐURSTAÐA = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !skel_málskipan.연결중) { 단말.Skrift("exit "); 단말.númer(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kjarni.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = bretti.skrá_flytja_þjónusta(1); if (처리값 < 0) Villa(처리값); else { 단말.Skrift("FTP listening "); kerfi_verkfæri.skrifa_slóð(bretti.Net_staða(0,0)); 단말.Skrift(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { bretti.skrá_flytja_þjónusta(0); 단말.Skrift("FTP stopped\n"); }
            else 단말.Skrift(bretti.skrá_flytja_þjónusta(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { búnt.Undirbúa(); 단말.Skrift("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Tungumál = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (tákn_COUNT != 2 || Tungumál < 0) 단말.Skrift("example java|c|python: úttak, Skrá, 네트워크, 그래픽, Java Swing Gluggi 예제\n");
            else { int 처리값 = 예제꾸러미.setja_upp_VALUE(Tungumál); if (처리값 < 0) { Villa(처리값); if (처리값 == -28) 단말.Skrift("RAM full: remove unused files, then retry example\n"); } else 단말.Skrift("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int snið_VALUE = 실행형식();
            if (snið_VALUE == 1 || snið_VALUE == 2) {
                int 처리값 = verkfæri_færsla(snið_VALUE == 1 ? -1 : 14, 0); NIÐURSTAÐA = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !skel_málskipan.연결중) { 단말.Skrift("exit "); 단말.númer(처리값); 단말.문자(10); }
            } else if (snið_VALUE == 0) { NIÐURSTAÐA = 126; 단말.Skrift("실행할 númer 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { NIÐURSTAÐA = 127; 단말.Skrift("Unknown command. help: commands\n"); }
        }
    }
    public static void keyra_skipun() {
        búnt.Undirbúa();
        for (int Tungumál = 0; Tungumál < 3; Tungumál++) { int 처리값 = 예제꾸러미.setja_upp_VALUE(Tungumál); if (처리값 < 0) Villa(처리값); }
        sýna_hjálp();
        while (true) {
            gluggi_lota.Ferli_VALUE_færsla(); if (gluggi_lota.재개()) continue;
            if (!gluggi_lota.이어읽기) 단말.Skrift("jkoros-native> "); lína_ritill.skipanalína = true; bretti.fjartengdur_Bíddu(1); int Stærð = 줄읽기(); bretti.fjartengdur_Bíddu(0); lína_ritill.skipanalína = false;
            if (Stærð == -3) continue;
            if (Stærð == -2) 단말.Skrift("Skipun þátta_VALUE: 명령줄이 너무 깁니다\n");
            if (Stærð >= 0) { skel_málskipan.forskrift_ljúka = false; skel_málskipan.keyra_skipun(Lína, 0, Stærð, 0); } else skel_málskipan.staða_VALUE_e10195a1 = 130;
            bretti.ljúka_fjartengdur_skipun(skel_málskipan.staða_VALUE_e10195a1);
            lína_ritill.Stærð = lína_ritill.bendill_VALUE = lína_ritill.Opna_gluggi = 0;
        }
    }
}
