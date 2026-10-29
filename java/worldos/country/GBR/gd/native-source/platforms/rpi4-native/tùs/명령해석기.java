// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 loidhne_àithne. comharran_labhairt, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] loidhne = new int[4096], tòcan_VALUE = new int[4096], 시작점 = new int[32], faid_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], deasaich_ainm = new int[63];
    static int tòcan_COUNT, deasaich_ainm_faid, tomhas;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { bòrd.직렬쓰기(VALUE); }
    static int 줄읽기() { return loidhne_deasaiche.읽기(); }
    static boolean 나누기(int atharraich_am_meud) {
        int suidhich = 0, 끝 = 0; tòcan_COUNT = 0;
        while (suidhich < atharraich_am_meud) {
            while (suidhich < atharraich_am_meud && (loidhne[suidhich] == 32 || loidhne[suidhich] == 9)) suidhich++;
            if (suidhich == atharraich_am_meud) break;
            if (tòcan_COUNT == 16) { 단말.sgrìobh("àithne 해석: 인수가 너무 많습니다\n"); return false; }
            시작점[tòcan_COUNT] = 끝; int comharran_labhairt_VALUE = 0;
            while (suidhich < atharraich_am_meud) {
                int VALUE = loidhne[suidhich++];
                if (comharran_labhairt_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == comharran_labhairt_VALUE) { comharran_labhairt_VALUE = 0; continue; }
                if (comharran_labhairt_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { comharran_labhairt_VALUE = VALUE; continue; }
                tòcan_VALUE[끝++] = VALUE;
            }
            if (comharran_labhairt_VALUE != 0) { 단말.sgrìobh("àithne 해석: 따옴표가 닫히지 않았습니다\n"); return false; }
            faid_VALUE[tòcan_COUNT] = 끝 - 시작점[tòcan_COUNT]; tòcan_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= tòcan_COUNT) return false;
        int suidhich_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int còd_a_charactair=Word_SMS.charAt(순번);
            if (còd_a_charactair>=0xd800 && còd_a_charactair<=0xdbff && 순번+1<Word_SMS.length()) còd_a_charactair=0x10000+((còd_a_charactair-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int baidht_COUNT=còd_a_charactair<128?1:còd_a_charactair<2048?2:còd_a_charactair<65536?3:4;
            for (int SEQUENCE_VALUE=baidht_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=baidht_COUNT==1?còd_a_charactair:SEQUENCE_VALUE==baidht_COUNT-1?(baidht_COUNT==2?0xc0:baidht_COUNT==3?0xe0:0xf0)|(còd_a_charactair>>(6*SEQUENCE_VALUE)):0x80|((còd_a_charactair>>(6*SEQUENCE_VALUE))&63);
                if (suidhich_INDEX>=faid_VALUE[INDEX] || tòcan_VALUE[시작점[INDEX]+suidhich_INDEX++]!=VALUE) return false;
            }
        }
        return suidhich_INDEX==faid_VALUE[INDEX];
    }
    static int Slighe(int INDEX) {
        if (INDEX >= tòcan_COUNT) return -22;
        int tomhas = cuimhne_faidhlichean.slighe_Start(faid_VALUE[INDEX]); if (tomhas < 0) return tomhas;
        for (int lùb_INDEX = 0; lùb_INDEX < faid_VALUE[INDEX]; lùb_INDEX++) {
            tomhas = cuimhne_faidhlichean.slighe_baidht(lùb_INDEX, tòcan_VALUE[시작점[INDEX] + lùb_INDEX]); if (tomhas < 0) return tomhas;
        }
        return 0;
    }
    static void Mearachd(int INDEX) { tomhas = 1; 단말.sgrìobh("Mearachd "); 단말.수(INDEX); 단말.문자(10); }
    static void seall_VALUE() {
        if (tòcan_COUNT != 2) { 단말.sgrìobh("사용법: cat faidhle\n"); return; }
        int tomhas = Slighe(1); if (tomhas < 0) { Mearachd(tomhas); return; }
        int faidhle = cuimhne_faidhlichean.fosgail(0); if (faidhle < 0) { Mearachd(faidhle); return; }
        while (true) { int VALUE = cuimhne_faidhlichean.읽기(faidhle); if (VALUE == 256) break; if (VALUE < 0) { Mearachd(VALUE); break; } 원바이트(VALUE); }
        cuimhne_faidhlichean.dùin(faidhle); 단말.문자(10);
    }
    static void deasaich_VALUE() {
        if (tòcan_COUNT != 2) { 단말.sgrìobh("사용법: edit faidhle\n"); return; }
        int tomhas = Slighe(1); if (tomhas < 0) { Mearachd(tomhas); return; }
        deasaich_ainm_faid = faid_VALUE[1];
        for (int lùb_INDEX = 0; lùb_INDEX < deasaich_ainm_faid; lùb_INDEX++) deasaich_ainm[lùb_INDEX] = tòcan_VALUE[시작점[1] + lùb_INDEX];
        단말.sgrìobh("EDIT: faidhle 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int atharraich_am_meud = 0;
        while (true) {
            단말.sgrìobh("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.sgrìobh("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && loidhne[0] == '.') break;
            if (입력 + 1 > 편집내용.length - atharraich_am_meud) { 단말.sgrìobh("EDIT CANCELLED: file too large\n"); return; }
            for (int lùb_INDEX = 0; lùb_INDEX < 입력; lùb_INDEX++) 편집내용[atharraich_am_meud++] = loidhne[lùb_INDEX];
            편집내용[atharraich_am_meud++] = 10;
        }
        cuimhne_faidhlichean.slighe_Start(deasaich_ainm_faid);
        for (int lùb_INDEX = 0; lùb_INDEX < deasaich_ainm_faid; lùb_INDEX++) cuimhne_faidhlichean.slighe_baidht(lùb_INDEX, deasaich_ainm[lùb_INDEX]);
        int faidhle = cuimhne_faidhlichean.fosgail(577); if (faidhle < 0) { Mearachd(faidhle); return; }
        for (int lùb_INDEX = 0; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) cuimhne_faidhlichean.sgrìobh(faidhle, 편집내용[lùb_INDEX]);
        cuimhne_faidhlichean.dùin(faidhle); 단말.sgrìobh("SAVED "); 단말.수(atharraich_am_meud); 단말.sgrìobh("baidht_VALUE(주기억 faidhle)\n");
    }
    static int hex_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (tòcan_COUNT != 2) { 단말.sgrìobh("사용법: load faidhle | hex faidhle\n"); return; }
        int tomhas = Slighe(1); if (tomhas < 0) { Mearachd(tomhas); return; }
        if (!넣기) {
            int faidhle = cuimhne_faidhlichean.fosgail(0); if (faidhle < 0) { Mearachd(faidhle); return; }
            단말.sgrìobh("HEX BEGIN "); 단말.수(cuimhne_faidhlichean.atharraich_am_meud(faidhle)); 단말.문자(10);
            int cur_a_steach_COUNT = 0;
            while (true) {
                int VALUE = cuimhne_faidhlichean.읽기(faidhle); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++cur_a_steach_COUNT % 32 == 0) 단말.문자(10);
            }
            if (cur_a_steach_COUNT % 32 != 0) 단말.문자(10);
            cuimhne_faidhlichean.dùin(faidhle); 단말.sgrìobh("HEX END\n"); return;
        }
        deasaich_ainm_faid = faid_VALUE[1];
        for (int lùb_INDEX = 0; lùb_INDEX < deasaich_ainm_faid; lùb_INDEX++) deasaich_ainm[lùb_INDEX] = tòcan_VALUE[시작점[1] + lùb_INDEX];
        단말.sgrìobh("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int atharraich_am_meud = 0;
        while (true) {
            단말.sgrìobh("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.sgrìobh("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && loidhne[0] == '.') break;
            int 앞 = -1;
            for (int lùb_INDEX = 0; lùb_INDEX < 입력; lùb_INDEX++) {
                if (loidhne[lùb_INDEX] == 32 || loidhne[lùb_INDEX] == 9) continue;
                int VALUE = hex_VALUE(loidhne[lùb_INDEX]);
                if (VALUE < 0 || atharraich_am_meud >= 편집내용.length) { 단말.sgrìobh("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = VALUE; else { 편집내용[atharraich_am_meud++] = 앞 * 16 + VALUE; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.sgrìobh("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        cuimhne_faidhlichean.slighe_Start(deasaich_ainm_faid);
        for (int lùb_INDEX = 0; lùb_INDEX < deasaich_ainm_faid; lùb_INDEX++) cuimhne_faidhlichean.slighe_baidht(lùb_INDEX, deasaich_ainm[lùb_INDEX]);
        int faidhle = cuimhne_faidhlichean.fosgail(577); if (faidhle < 0) { Mearachd(faidhle); return; }
        for (int lùb_INDEX = 0; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) cuimhne_faidhlichean.sgrìobh(faidhle, 편집내용[lùb_INDEX]);
        cuimhne_faidhlichean.dùin(faidhle); 단말.sgrìobh("LOADED "); 단말.수(atharraich_am_meud); 단말.sgrìobh("baidht_VALUE(주기억 faidhle)\n");
    }
    static int innealan(int INDEX) {
        return inneal_cur_a_steach(INDEX, 1);
    }
    static int inneal_cur_a_steach(int INDEX, int ruith) {
        if (tòcan_COUNT - ruith > 8) return -22;
        bòrd.인수준비(tòcan_COUNT - ruith);
        for (int 첫값 = ruith; 첫값 < tòcan_COUNT; 첫값++) {
            if (faid_VALUE[첫값] > 255) return -36;
            for (int lùb_INDEX = 0; lùb_INDEX < faid_VALUE[첫값]; lùb_INDEX++) bòrd.argamaid_baidht(첫값 - ruith, lùb_INDEX, tòcan_VALUE[시작점[첫값] + lùb_INDEX]);
        }
        return INDEX == -2 ? bòrd.리눅스파일실행() : INDEX < 0 ? bòrd.gnìomhaich_cleachdaiche_faidhle() : bòrd.ruith_cleachdaiche_ap(INDEX);
    }
    static int PYTHON_trusgan() {
        if (tòcan_COUNT > 8) return -22;
        bòrd.인수준비(tòcan_COUNT);
        String Slighe = "/lib/trusgan.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int suidhich_INDEX = 0;
        for (int 순번 = 0; 순번 < Slighe.length(); 순번++) {
            int caractar_VALUE = Slighe.charAt(순번);
            if (caractar_VALUE < 128) bòrd.argamaid_baidht(0, suidhich_INDEX++, caractar_VALUE);
            else { bòrd.argamaid_baidht(0, suidhich_INDEX++, 0xe0 | (caractar_VALUE >> 12)); bòrd.argamaid_baidht(0, suidhich_INDEX++, 0x80 | ((caractar_VALUE >> 6) & 63)); bòrd.argamaid_baidht(0, suidhich_INDEX++, 0x80 | (caractar_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < tòcan_COUNT; 순번++) {
            if (faid_VALUE[순번] > 255) return -36;
            for (int caractar_VALUE = 0; caractar_VALUE < faid_VALUE[순번]; caractar_VALUE++) bòrd.argamaid_baidht(순번, caractar_VALUE, tòcan_VALUE[시작점[순번] + caractar_VALUE]);
        }
        return bòrd.ruith_cleachdaiche_ap(12);
    }
    static int 실행형식() {
        int 처리값 = Slighe(0); if (처리값 < 0) return 처리값;
        int faidhle = cuimhne_faidhlichean.fosgail(0); if (faidhle < 0) return faidhle;
        int 첫값 = cuimhne_faidhlichean.읽기(faidhle), baidht_dàta = cuimhne_faidhlichean.읽기(faidhle), còd_a_charactair = cuimhne_faidhlichean.읽기(faidhle), 뒷값 = cuimhne_faidhlichean.읽기(faidhle);
        cuimhne_faidhlichean.dùin(faidhle);
        if (첫값 == 127 && baidht_dàta == 'E' && còd_a_charactair == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && baidht_dàta == 'K' && còd_a_charactair == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        bòrd.인수준비(1);
        for (int lùb_INDEX = 0; lùb_INDEX < 인수.length(); lùb_INDEX++) bòrd.argamaid_baidht(0, lùb_INDEX, 인수.charAt(lùb_INDEX));
        return bòrd.ruith_cleachdaiche_ap(INDEX);
    }
    static void SMS_baidht(int faidhle, int VALUE) { cuimhne_faidhlichean.sgrìobh(faidhle, VALUE); }
    static void stadaigeach_faidhle(String Ainm, String susbaint_VALUE) {
        // trusgan 파일명은 ASCII. faidhle 내용은 UTF-8로 저장한다.
        cuimhne_faidhlichean.slighe_Start(Ainm.length());
        for (int lùb_INDEX = 0; lùb_INDEX < Ainm.length(); lùb_INDEX++) cuimhne_faidhlichean.slighe_baidht(lùb_INDEX, Ainm.charAt(lùb_INDEX));
        int faidhle = cuimhne_faidhlichean.fosgail(193); if (faidhle < 0) return;
        for (int lùb_INDEX = 0; lùb_INDEX < susbaint_VALUE.length(); lùb_INDEX++) {
            int còd_a_charactair = susbaint_VALUE.charAt(lùb_INDEX);
            if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdbff && lùb_INDEX + 1 < susbaint_VALUE.length()) còd_a_charactair = 0x10000 + ((còd_a_charactair - 0xd800) << 10) + susbaint_VALUE.charAt(++lùb_INDEX) - 0xdc00;
            if (còd_a_charactair < 128) SMS_baidht(faidhle, còd_a_charactair);
            else {
                int 수 = còd_a_charactair < 2048 ? 2 : còd_a_charactair < 65536 ? 3 : 4;
                SMS_baidht(faidhle, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (còd_a_charactair >> (6 * (수 - 1))));
                for (int cur_a_steach_COUNT = 수 - 1; cur_a_steach_COUNT > 0; cur_a_steach_COUNT--) SMS_baidht(faidhle, 0x80 | ((còd_a_charactair >> (6 * (cur_a_steach_COUNT - 1))) & 63));
            }
        }
        cuimhne_faidhlichean.dùin(faidhle);
    }
    static void 한글도움말() {
        단말.sgrìobh("F9 / Shift+Space: [EN] ↔ [gd]\n");
        단말.sgrìobh("  [GD] keyboard; [EN] ASCII\n");
        단말.sgrìobh("  a → a\n");
        단말.sgrìobh("  F9: EN ↔ gd | Ctrl+Shift+V: UTF-8\n");
        단말.sgrìobh("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.sgrìobh("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Ainm) {
        int baidht_COUNT = 0;
        for (int lùb_INDEX = 0; lùb_INDEX < Ainm.length(); lùb_INDEX++) { int còd_a_charactair = Ainm.charAt(lùb_INDEX); if (còd_a_charactair >= 0xd800 && còd_a_charactair <= 0xdfff) return -22; baidht_COUNT += còd_a_charactair < 128 ? 1 : còd_a_charactair < 2048 ? 2 : 3; }
        int 처리값 = cuimhne_faidhlichean.slighe_Start(baidht_COUNT); if (처리값 < 0) return 처리값;
        int suidhich_INDEX = 0;
        for (int lùb_INDEX = 0; lùb_INDEX < Ainm.length(); lùb_INDEX++) {
            int còd_a_charactair = Ainm.charAt(lùb_INDEX);
            if (còd_a_charactair < 128) cuimhne_faidhlichean.slighe_baidht(suidhich_INDEX++, còd_a_charactair);
            else if (còd_a_charactair < 2048) { cuimhne_faidhlichean.slighe_baidht(suidhich_INDEX++, 0xc0 | (còd_a_charactair >> 6)); cuimhne_faidhlichean.slighe_baidht(suidhich_INDEX++, 0x80 | (còd_a_charactair & 63)); }
            else { cuimhne_faidhlichean.slighe_baidht(suidhich_INDEX++, 0xe0 | (còd_a_charactair >> 12)); cuimhne_faidhlichean.slighe_baidht(suidhich_INDEX++, 0x80 | ((còd_a_charactair >> 6) & 63)); cuimhne_faidhlichean.slighe_baidht(suidhich_INDEX++, 0x80 | (còd_a_charactair & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Ainm) {
        int 처리값 = 예제경로(Ainm); if (처리값 < 0) return 처리값;
        처리값 = cuimhne_faidhlichean.Create_eòlaire(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Ainm, String dàta) {
        int 처리값 = 예제경로(Ainm); if (처리값 < 0) return 처리값;
        int faidhle = cuimhne_faidhlichean.fosgail(193); if (faidhle == -17) return 0; if (faidhle < 0) return faidhle;
        for (int lùb_INDEX = 0; lùb_INDEX < dàta.length(); lùb_INDEX += 2) {
            처리값 = cuimhne_faidhlichean.sgrìobh(faidhle, hex_VALUE(dàta.charAt(lùb_INDEX)) * 16 + hex_VALUE(dàta.charAt(lùb_INDEX + 1)));
            if (처리값 < 0) { cuimhne_faidhlichean.dùin(faidhle); return 처리값; }
        }
        return cuimhne_faidhlichean.dùin(faidhle);
    }
    static void show_cuideachadh() {
        siostam_inneal.show_cuideachadh();
        단말.sgrìobh("sshd / tèarainte_slige start|stop|status: SSH :22 (user, 장치별 facal_faire_VALUE)\n");
        단말.sgrìobh("vncd / cian_taisbean start|stop|status: VNC :5900 (장치별 facal_faire_VALUE)\n");
        단말.sgrìobh("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.sgrìobh("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.sgrìobh("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.sgrìobh("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.sgrìobh("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.sgrìobh("모서리 + 왼쪽 버튼 slaod_VALUE: tèirmineal atharraich_am_meud atharraich_VALUE; terminal size: colbh_VALUE/ROW_VALUE\n");
        단말.sgrìobh("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.sgrìobh("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.sgrìobh("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.sgrìobh("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.sgrìobh("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.sgrìobh("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.sgrìobh("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.sgrìobh("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.sgrìobh("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.sgrìobh("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.sgrìobh("pip: MicroPython tùs_craobh stàlaich_VALUE; òstair --network --pip 필요; /lib는 RAM\n");
        단말.sgrìobh("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.sgrìobh("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.sgrìobh("/example/java /example/c /example/python: examples ready at boot\n");
        단말.sgrìobh("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void tèirmineal(boolean 전환여부) {
        if (전환여부 && bòrd.tèirmineal(2) != 0) { bòrd.tèirmineal(0); 단말.sgrìobh("TERMINAL CLOSED\n"); }
        else if (bòrd.tèirmineal(1) < 0) Mearachd(-19);
        else 단말.sgrìobh("TERMINAL READY — gd terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void àithne() {
        if (tòcan_COUNT == 0) return;
        if (siostam_inneal.gnìomhaich_àithne()) return;
        if (같음(0,"sshd") || 같음(0,"tèarainte_slige") || 같음(0,"vncd") || 같음(0,"cian_taisbean")) {
            int 종류=같음(0,"vncd")||같음(0,"cian_taisbean")?1:0;
            int Gnìomh=같음(1,"start")||같음(1,"ruith")?1:같음(1,"stop")||같음(1,"Stad")?0:2;
            int cor_VALUE=bòrd.co_sheisean(종류,Gnìomh);
            if(cor_VALUE<0)Mearachd(cor_VALUE);else 단말.sgrìobh(bòrd.co_sheisean(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else show_cuideachadh(); }
        else if (같음(0, "info") || 같음(0, "i")) eitean.msinfo32_exe();
        else if (같음(0, "pwd")) { cuimhne_faidhlichean.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (tòcan_COUNT == 1) { cuimhne_faidhlichean.slighe_Start(1); 처리값 = cuimhne_faidhlichean.slighe_baidht(0, '/'); } else 처리값 = tòcan_COUNT == 2 ? Slighe(1) : -22;
            if (처리값 >= 0) 처리값 = cuimhne_faidhlichean.atharraich_eòlaire(); if (처리값 < 0) Mearachd(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argamaid_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (tòcan_COUNT == argamaid_INDEX) { cuimhne_faidhlichean.slighe_Start(1); 처리값 = cuimhne_faidhlichean.slighe_baidht(0, '.'); } else 처리값 = tòcan_COUNT == argamaid_INDEX + 1 ? Slighe(argamaid_INDEX) : -22;
            if (처리값 >= 0) 처리값 = cuimhne_faidhlichean.경로목록(); if (처리값 < 0) Mearachd(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) slige_innealan.faidhle_cùis(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) slige_innealan.ionstans_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) slige_innealan.seall_VALUE();
        else if (같음(0, "wc")) slige_innealan.세기();
        else if (같음(0, "grep")) slige_innealan.FIND_cur_a_steach();
        else if (같음(0, "head") || 같음(0, "tail")) slige_innealan.머리(같음(0, "tail"));
        else if (같음(0, "tee")) slige_innealan.함께쓰기();
        else if (같음(0, "env")) 셸문법.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (tòcan_COUNT == 1) 셸문법.환경보기();
            for (int lùb_INDEX = 1; lùb_INDEX < tòcan_COUNT; lùb_INDEX++) { int 처리값 = 셸문법.환경설정(lùb_INDEX, 같음(0, "unset")); if (처리값 != 0) { tomhas = 처리값; 단말.sgrìobh("àithne 해석: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) 셸문법.gnìomhaich_faidhle();
        else if (같음(0, "true")) tomhas = 0;
        else if (같음(0, "false")) tomhas = 1;
        else if (같음(0, "history")) loidhne_deasaiche.show_LOG();
        else if (같음(0, "exit")) {
            if (셸문법.깊이 > 0) { tomhas = tòcan_COUNT == 1 ? 셸문법.cor_VALUE : slige_innealan.figear_VALUE(1); if (tomhas < 0 || tomhas > 255) tomhas = 2; 셸문법.sgriobt_crìochnaich = true; }
            else if (bòrd.tèirmineal(2) != 0) tèirmineal(true);
            else 단말.sgrìobh("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) deasaich_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (tòcan_COUNT < 2) { tomhas = 2; 단말.sgrìobh("사용법: rm faidhle...\n"); }
            for (int lùb_INDEX = 1; lùb_INDEX < tòcan_COUNT; lùb_INDEX++) { int 처리값 = Slighe(lùb_INDEX); if (처리값 == 0) 처리값 = cuimhne_faidhlichean.지우기(); if (처리값 < 0) Mearachd(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_suidhich = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_suidhich; 첫값 < tòcan_COUNT; 첫값++) { if (첫값 > Start_suidhich) 단말.문자(32); for (int lùb_INDEX = 0; lùb_INDEX < faid_VALUE[첫값]; lùb_INDEX++) bòrd.직렬쓰기(tòcan_VALUE[시작점[첫값] + lùb_INDEX]); }
            if (Start_suidhich == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.sgrìobh("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_trusgan() : innealan(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); tomhas = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !셸문법.연결중) { 단말.sgrìobh("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = innealan(13); tomhas = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = innealan(15); tomhas = 처리값 < 0 ? 126 : 처리값; if (!셸문법.연결중) { 단말.sgrìobh("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = innealan(16); tomhas = 처리값 < 0 ? 126 : 처리값; if (!셸문법.연결중) { 단말.sgrìobh("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int atharraich_am_meud = bòrd.tèirmineal(13); 단말.sgrìobh("TERMINAL SIZE "); 단말.수(atharraich_am_meud & 65535); 단말.문자('x'); 단말.수(atharraich_am_meud >>> 16); 단말.문자(10); }
            else tèirmineal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { bòrd.tèirmineal(9); deasg.gnìomhaich_àithne(); }
        else if (같음(0, "c")) eitean.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) eitean.작업시험();
        else if (같음(0, "g")) eitean.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) eitean.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = bòrd.ruith_cleachdaiche_ap(0); if (처리값 == 0) 단말.sgrìobh("ELF DEMO PASS\n"); else Mearachd(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? inneal_cur_a_steach(-2, 2) : innealan(-1); tomhas = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !셸문법.연결중) { 단말.sgrìobh("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) eitean.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = bòrd.faidhle_tar_chur_seirbheis(1); if (처리값 < 0) Mearachd(처리값); else { 단말.sgrìobh("FTP listening "); siostam_inneal.sgrìobh_ADDRESS(bòrd.lìonra_cor(0,0)); 단말.sgrìobh(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { bòrd.faidhle_tar_chur_seirbheis(0); 단말.sgrìobh("FTP stopped\n"); }
            else 단말.sgrìobh(bòrd.faidhle_tar_chur_seirbheis(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { trusgan.Ullaich(); 단말.sgrìobh("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int cànan = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (tòcan_COUNT != 2 || cànan < 0) 단말.sgrìobh("example java|c|python: 출력, faidhle, 네트워크, 그래픽, Java Swing uinneag 예제\n");
            else { int 처리값 = 예제꾸러미.stàlaich_VALUE(cànan); if (처리값 < 0) { Mearachd(처리값); if (처리값 == -28) 단말.sgrìobh("RAM full: remove unused files, then retry example\n"); } else 단말.sgrìobh("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int fòrmat_VALUE = 실행형식();
            if (fòrmat_VALUE == 1 || fòrmat_VALUE == 2) {
                int 처리값 = inneal_cur_a_steach(fòrmat_VALUE == 1 ? -1 : 14, 0); tomhas = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !셸문법.연결중) { 단말.sgrìobh("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (fòrmat_VALUE == 0) { tomhas = 126; 단말.sgrìobh("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { tomhas = 127; 단말.sgrìobh("Unknown command. help: commands\n"); }
        }
    }
    public static void gnìomhaich_àithne() {
        trusgan.Ullaich();
        for (int cànan = 0; cànan < 3; cànan++) { int 처리값 = 예제꾸러미.stàlaich_VALUE(cànan); if (처리값 < 0) Mearachd(처리값); }
        show_cuideachadh();
        while (true) {
            uinneag_seisean.Pròiseas_VALUE_cur_a_steach(); if (uinneag_seisean.재개()) continue;
            if (!uinneag_seisean.이어읽기) 단말.sgrìobh("jkoros-native> "); loidhne_deasaiche.loidhne_àithne = true; bòrd.cian_fuirich(1); int atharraich_am_meud = 줄읽기(); bòrd.cian_fuirich(0); loidhne_deasaiche.loidhne_àithne = false;
            if (atharraich_am_meud == -3) continue;
            if (atharraich_am_meud == -2) 단말.sgrìobh("àithne 해석: 명령줄이 너무 깁니다\n");
            if (atharraich_am_meud >= 0) { 셸문법.sgriobt_crìochnaich = false; 셸문법.gnìomhaich_àithne(loidhne, 0, atharraich_am_meud, 0); } else 셸문법.cor_VALUE = 130;
            bòrd.crìochnaich_cian_àithne(셸문법.cor_VALUE);
            loidhne_deasaiche.atharraich_am_meud = loidhne_deasaiche.cursair_VALUE = loidhne_deasaiche.Start_uinneag = 0;
        }
    }
}
