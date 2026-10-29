// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 líne_na_n_orduithe. Athfhriotail, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Líne = new int[4096], licín_VALUE = new int[4096], 시작점 = new int[32], fad_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], cuir_in_eagar_ainm = new int[63];
    static int licín_COUNT, cuir_in_eagar_ainm_fad, tomhas;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { clár.직렬쓰기(VALUE); }
    static int 줄읽기() { return líne_Eagarthóir.Léigh(); }
    static boolean 나누기(int Méid) {
        int suíomh = 0, 끝 = 0; licín_COUNT = 0;
        while (suíomh < Méid) {
            while (suíomh < Méid && (Líne[suíomh] == 32 || Líne[suíomh] == 9)) suíomh++;
            if (suíomh == Méid) break;
            if (licín_COUNT == 16) { 단말.Scríobh("Ordú parsáil_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[licín_COUNT] = 끝; int Athfhriotail_VALUE = 0;
            while (suíomh < Méid) {
                int VALUE = Líne[suíomh++];
                if (Athfhriotail_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Athfhriotail_VALUE) { Athfhriotail_VALUE = 0; continue; }
                if (Athfhriotail_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Athfhriotail_VALUE = VALUE; continue; }
                licín_VALUE[끝++] = VALUE;
            }
            if (Athfhriotail_VALUE != 0) { 단말.Scríobh("Ordú parsáil_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            fad_VALUE[licín_COUNT] = 끝 - 시작점[licín_COUNT]; licín_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= licín_COUNT) return false;
        int suíomh_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int pointe_cóid=Word_SMS.charAt(순번);
            if (pointe_cóid>=0xd800 && pointe_cóid<=0xdbff && 순번+1<Word_SMS.length()) pointe_cóid=0x10000+((pointe_cóid-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int beart_COUNT=pointe_cóid<128?1:pointe_cóid<2048?2:pointe_cóid<65536?3:4;
            for (int SEQUENCE_VALUE=beart_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=beart_COUNT==1?pointe_cóid:SEQUENCE_VALUE==beart_COUNT-1?(beart_COUNT==2?0xc0:beart_COUNT==3?0xe0:0xf0)|(pointe_cóid>>(6*SEQUENCE_VALUE)):0x80|((pointe_cóid>>(6*SEQUENCE_VALUE))&63);
                if (suíomh_INDEX>=fad_VALUE[INDEX] || licín_VALUE[시작점[INDEX]+suíomh_INDEX++]!=VALUE) return false;
            }
        }
        return suíomh_INDEX==fad_VALUE[INDEX];
    }
    static int CONAIR(int INDEX) {
        if (INDEX >= licín_COUNT) return -22;
        int tomhas = Cuimhne_Comhaid.cosán_Start(fad_VALUE[INDEX]); if (tomhas < 0) return tomhas;
        for (int lúb_INDEX = 0; lúb_INDEX < fad_VALUE[INDEX]; lúb_INDEX++) {
            tomhas = Cuimhne_Comhaid.cosán_beart(lúb_INDEX, licín_VALUE[시작점[INDEX] + lúb_INDEX]); if (tomhas < 0) return tomhas;
        }
        return 0;
    }
    static void ERREÁID(int INDEX) { tomhas = 1; 단말.Scríobh("ERREÁID "); 단말.수(INDEX); 단말.문자(10); }
    static void Amharc_VALUE() {
        if (licín_COUNT != 2) { 단말.Scríobh("사용법: cat Comhad\n"); return; }
        int tomhas = CONAIR(1); if (tomhas < 0) { ERREÁID(tomhas); return; }
        int Comhad = Cuimhne_Comhaid.Oscail(0); if (Comhad < 0) { ERREÁID(Comhad); return; }
        while (true) { int VALUE = Cuimhne_Comhaid.Léigh(Comhad); if (VALUE == 256) break; if (VALUE < 0) { ERREÁID(VALUE); break; } 원바이트(VALUE); }
        Cuimhne_Comhaid.Dún(Comhad); 단말.문자(10);
    }
    static void cuir_in_eagar_VALUE() {
        if (licín_COUNT != 2) { 단말.Scríobh("사용법: edit Comhad\n"); return; }
        int tomhas = CONAIR(1); if (tomhas < 0) { ERREÁID(tomhas); return; }
        cuir_in_eagar_ainm_fad = fad_VALUE[1];
        for (int lúb_INDEX = 0; lúb_INDEX < cuir_in_eagar_ainm_fad; lúb_INDEX++) cuir_in_eagar_ainm[lúb_INDEX] = licín_VALUE[시작점[1] + lúb_INDEX];
        단말.Scríobh("EDIT: Comhad 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Méid = 0;
        while (true) {
            단말.Scríobh("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Scríobh("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Líne[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Méid) { 단말.Scríobh("EDIT CANCELLED: file too large\n"); return; }
            for (int lúb_INDEX = 0; lúb_INDEX < 입력; lúb_INDEX++) 편집내용[Méid++] = Líne[lúb_INDEX];
            편집내용[Méid++] = 10;
        }
        Cuimhne_Comhaid.cosán_Start(cuir_in_eagar_ainm_fad);
        for (int lúb_INDEX = 0; lúb_INDEX < cuir_in_eagar_ainm_fad; lúb_INDEX++) Cuimhne_Comhaid.cosán_beart(lúb_INDEX, cuir_in_eagar_ainm[lúb_INDEX]);
        int Comhad = Cuimhne_Comhaid.Oscail(577); if (Comhad < 0) { ERREÁID(Comhad); return; }
        for (int lúb_INDEX = 0; lúb_INDEX < Méid; lúb_INDEX++) Cuimhne_Comhaid.Scríobh(Comhad, 편집내용[lúb_INDEX]);
        Cuimhne_Comhaid.Dún(Comhad); 단말.Scríobh("SAVED "); 단말.수(Méid); 단말.Scríobh("beart_VALUE(주기억 Comhad)\n");
    }
    static int heics_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (licín_COUNT != 2) { 단말.Scríobh("사용법: load Comhad | hex Comhad\n"); return; }
        int tomhas = CONAIR(1); if (tomhas < 0) { ERREÁID(tomhas); return; }
        if (!넣기) {
            int Comhad = Cuimhne_Comhaid.Oscail(0); if (Comhad < 0) { ERREÁID(Comhad); return; }
            단말.Scríobh("HEX BEGIN "); 단말.수(Cuimhne_Comhaid.Méid(Comhad)); 단말.문자(10);
            int iontráil_COUNT = 0;
            while (true) {
                int VALUE = Cuimhne_Comhaid.Léigh(Comhad); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++iontráil_COUNT % 32 == 0) 단말.문자(10);
            }
            if (iontráil_COUNT % 32 != 0) 단말.문자(10);
            Cuimhne_Comhaid.Dún(Comhad); 단말.Scríobh("HEX END\n"); return;
        }
        cuir_in_eagar_ainm_fad = fad_VALUE[1];
        for (int lúb_INDEX = 0; lúb_INDEX < cuir_in_eagar_ainm_fad; lúb_INDEX++) cuir_in_eagar_ainm[lúb_INDEX] = licín_VALUE[시작점[1] + lúb_INDEX];
        단말.Scríobh("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Méid = 0;
        while (true) {
            단말.Scríobh("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Scríobh("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Líne[0] == '.') break;
            int 앞 = -1;
            for (int lúb_INDEX = 0; lúb_INDEX < 입력; lúb_INDEX++) {
                if (Líne[lúb_INDEX] == 32 || Líne[lúb_INDEX] == 9) continue;
                int VALUE = heics_VALUE(Líne[lúb_INDEX]);
                if (VALUE < 0 || Méid >= 편집내용.length) { 단말.Scríobh("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = VALUE; else { 편집내용[Méid++] = 앞 * 16 + VALUE; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Scríobh("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Cuimhne_Comhaid.cosán_Start(cuir_in_eagar_ainm_fad);
        for (int lúb_INDEX = 0; lúb_INDEX < cuir_in_eagar_ainm_fad; lúb_INDEX++) Cuimhne_Comhaid.cosán_beart(lúb_INDEX, cuir_in_eagar_ainm[lúb_INDEX]);
        int Comhad = Cuimhne_Comhaid.Oscail(577); if (Comhad < 0) { ERREÁID(Comhad); return; }
        for (int lúb_INDEX = 0; lúb_INDEX < Méid; lúb_INDEX++) Cuimhne_Comhaid.Scríobh(Comhad, 편집내용[lúb_INDEX]);
        Cuimhne_Comhaid.Dún(Comhad); 단말.Scríobh("LOADED "); 단말.수(Méid); 단말.Scríobh("beart_VALUE(주기억 Comhad)\n");
    }
    static int Uirlisí(int INDEX) {
        return uirlis_iontráil(INDEX, 1);
    }
    static int uirlis_iontráil(int INDEX, int Rith_2) {
        if (licín_COUNT - Rith_2 > 8) return -22;
        clár.인수준비(licín_COUNT - Rith_2);
        for (int 첫값 = Rith_2; 첫값 < licín_COUNT; 첫값++) {
            if (fad_VALUE[첫값] > 255) return -36;
            for (int lúb_INDEX = 0; lúb_INDEX < fad_VALUE[첫값]; lúb_INDEX++) clár.argóint_beart(첫값 - Rith_2, lúb_INDEX, licín_VALUE[시작점[첫값] + lúb_INDEX]);
        }
        return INDEX == -2 ? clár.리눅스파일실행() : INDEX < 0 ? clár.Rith_úsáideoir_comhad() : clár.rith_úsáideoir_clár(INDEX);
    }
    static int PYTHON_beart() {
        if (licín_COUNT > 8) return -22;
        clár.인수준비(licín_COUNT);
        String CONAIR = "/lib/beart.py";
        // Java 문자열을 셸의 UTF-8 Argóintí 버퍼에 기록한다.
        int suíomh_INDEX = 0;
        for (int 순번 = 0; 순번 < CONAIR.length(); 순번++) {
            int carachtar_VALUE = CONAIR.charAt(순번);
            if (carachtar_VALUE < 128) clár.argóint_beart(0, suíomh_INDEX++, carachtar_VALUE);
            else { clár.argóint_beart(0, suíomh_INDEX++, 0xe0 | (carachtar_VALUE >> 12)); clár.argóint_beart(0, suíomh_INDEX++, 0x80 | ((carachtar_VALUE >> 6) & 63)); clár.argóint_beart(0, suíomh_INDEX++, 0x80 | (carachtar_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < licín_COUNT; 순번++) {
            if (fad_VALUE[순번] > 255) return -36;
            for (int carachtar_VALUE = 0; carachtar_VALUE < fad_VALUE[순번]; carachtar_VALUE++) clár.argóint_beart(순번, carachtar_VALUE, licín_VALUE[시작점[순번] + carachtar_VALUE]);
        }
        return clár.rith_úsáideoir_clár(12);
    }
    static int 실행형식() {
        int 처리값 = CONAIR(0); if (처리값 < 0) return 처리값;
        int Comhad = Cuimhne_Comhaid.Oscail(0); if (Comhad < 0) return Comhad;
        int 첫값 = Cuimhne_Comhaid.Léigh(Comhad), beart_sonraí = Cuimhne_Comhaid.Léigh(Comhad), pointe_cóid = Cuimhne_Comhaid.Léigh(Comhad), 뒷값 = Cuimhne_Comhaid.Léigh(Comhad);
        Cuimhne_Comhaid.Dún(Comhad);
        if (첫값 == 127 && beart_sonraí == 'E' && pointe_cóid == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && beart_sonraí == 'K' && pointe_cóid == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argóintí) {
        clár.인수준비(1);
        for (int lúb_INDEX = 0; lúb_INDEX < Argóintí.length(); lúb_INDEX++) clár.argóint_beart(0, lúb_INDEX, Argóintí.charAt(lúb_INDEX));
        return clár.rith_úsáideoir_clár(INDEX);
    }
    static void SMS_beart(int Comhad, int VALUE) { Cuimhne_Comhaid.Scríobh(Comhad, VALUE); }
    static void statach_comhad(String Ainm, String Inneachar_VALUE) {
        // beart 파일명은 ASCII. Comhad 내용은 UTF-8로 저장한다.
        Cuimhne_Comhaid.cosán_Start(Ainm.length());
        for (int lúb_INDEX = 0; lúb_INDEX < Ainm.length(); lúb_INDEX++) Cuimhne_Comhaid.cosán_beart(lúb_INDEX, Ainm.charAt(lúb_INDEX));
        int Comhad = Cuimhne_Comhaid.Oscail(193); if (Comhad < 0) return;
        for (int lúb_INDEX = 0; lúb_INDEX < Inneachar_VALUE.length(); lúb_INDEX++) {
            int pointe_cóid = Inneachar_VALUE.charAt(lúb_INDEX);
            if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdbff && lúb_INDEX + 1 < Inneachar_VALUE.length()) pointe_cóid = 0x10000 + ((pointe_cóid - 0xd800) << 10) + Inneachar_VALUE.charAt(++lúb_INDEX) - 0xdc00;
            if (pointe_cóid < 128) SMS_beart(Comhad, pointe_cóid);
            else {
                int 수 = pointe_cóid < 2048 ? 2 : pointe_cóid < 65536 ? 3 : 4;
                SMS_beart(Comhad, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (pointe_cóid >> (6 * (수 - 1))));
                for (int iontráil_COUNT = 수 - 1; iontráil_COUNT > 0; iontráil_COUNT--) SMS_beart(Comhad, 0x80 | ((pointe_cóid >> (6 * (iontráil_COUNT - 1))) & 63));
            }
        }
        Cuimhne_Comhaid.Dún(Comhad);
    }
    static void 한글도움말() {
        단말.Scríobh("F9 / Shift+Space: [EN] ↔ [ga]\n");
        단말.Scríobh("  [GA] keyboard; [EN] ASCII\n");
        단말.Scríobh("  a → a\n");
        단말.Scríobh("  F9: EN ↔ ga | Ctrl+Shift+V: UTF-8\n");
        단말.Scríobh("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Scríobh("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Ainm) {
        int beart_COUNT = 0;
        for (int lúb_INDEX = 0; lúb_INDEX < Ainm.length(); lúb_INDEX++) { int pointe_cóid = Ainm.charAt(lúb_INDEX); if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdfff) return -22; beart_COUNT += pointe_cóid < 128 ? 1 : pointe_cóid < 2048 ? 2 : 3; }
        int 처리값 = Cuimhne_Comhaid.cosán_Start(beart_COUNT); if (처리값 < 0) return 처리값;
        int suíomh_INDEX = 0;
        for (int lúb_INDEX = 0; lúb_INDEX < Ainm.length(); lúb_INDEX++) {
            int pointe_cóid = Ainm.charAt(lúb_INDEX);
            if (pointe_cóid < 128) Cuimhne_Comhaid.cosán_beart(suíomh_INDEX++, pointe_cóid);
            else if (pointe_cóid < 2048) { Cuimhne_Comhaid.cosán_beart(suíomh_INDEX++, 0xc0 | (pointe_cóid >> 6)); Cuimhne_Comhaid.cosán_beart(suíomh_INDEX++, 0x80 | (pointe_cóid & 63)); }
            else { Cuimhne_Comhaid.cosán_beart(suíomh_INDEX++, 0xe0 | (pointe_cóid >> 12)); Cuimhne_Comhaid.cosán_beart(suíomh_INDEX++, 0x80 | ((pointe_cóid >> 6) & 63)); Cuimhne_Comhaid.cosán_beart(suíomh_INDEX++, 0x80 | (pointe_cóid & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Ainm) {
        int 처리값 = 예제경로(Ainm); if (처리값 < 0) return 처리값;
        처리값 = Cuimhne_Comhaid.Create_eolaire(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Ainm, String sonraí) {
        int 처리값 = 예제경로(Ainm); if (처리값 < 0) return 처리값;
        int Comhad = Cuimhne_Comhaid.Oscail(193); if (Comhad == -17) return 0; if (Comhad < 0) return Comhad;
        for (int lúb_INDEX = 0; lúb_INDEX < sonraí.length(); lúb_INDEX += 2) {
            처리값 = Cuimhne_Comhaid.Scríobh(Comhad, heics_VALUE(sonraí.charAt(lúb_INDEX)) * 16 + heics_VALUE(sonraí.charAt(lúb_INDEX + 1)));
            if (처리값 < 0) { Cuimhne_Comhaid.Dún(Comhad); return 처리값; }
        }
        return Cuimhne_Comhaid.Dún(Comhad);
    }
    static void seó_cabhair() {
        córas_uirlis.seó_cabhair();
        단말.Scríobh("sshd / slán_blaosc start|stop|status: SSH :22 (user, 장치별 pasfhocal_VALUE)\n");
        단말.Scríobh("vncd / cianda_taispeáin start|stop|status: VNC :5900 (장치별 pasfhocal_VALUE)\n");
        단말.Scríobh("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Scríobh("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Scríobh("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Scríobh("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Scríobh("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Scríobh("모서리 + 왼쪽 버튼 tarraing_VALUE: Teirminéal Méid athraigh_VALUE; terminal size: colún_VALUE/ró_VALUE\n");
        단말.Scríobh("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Scríobh("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Scríobh("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Scríobh("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Scríobh("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Scríobh("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Scríobh("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Scríobh("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Scríobh("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Scríobh("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Scríobh("pip: MicroPython foinse_crann suiteáil_VALUE; óstach --network --pip 필요; /lib는 RAM\n");
        단말.Scríobh("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Scríobh("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Scríobh("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Scríobh("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Teirminéal(boolean 전환여부) {
        if (전환여부 && clár.Teirminéal(2) != 0) { clár.Teirminéal(0); 단말.Scríobh("TERMINAL CLOSED\n"); }
        else if (clár.Teirminéal(1) < 0) ERREÁID(-19);
        else 단말.Scríobh("TERMINAL READY — ga terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Ordú() {
        if (licín_COUNT == 0) return;
        if (córas_uirlis.Rith_ordú()) return;
        if (같음(0,"sshd") || 같음(0,"slán_blaosc") || 같음(0,"vncd") || 같음(0,"cianda_taispeáin")) {
            int 종류=같음(0,"vncd")||같음(0,"cianda_taispeáin")?1:0;
            int Gníomh=같음(1,"start")||같음(1,"Rith_2")?1:같음(1,"stop")||같음(1,"Stad")?0:2;
            int staid_VALUE=clár.scáthú(종류,Gníomh);
            if(staid_VALUE<0)ERREÁID(staid_VALUE);else 단말.Scríobh(clár.scáthú(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else seó_cabhair(); }
        else if (같음(0, "info") || 같음(0, "i")) eithne.msinfo32_exe();
        else if (같음(0, "pwd")) { Cuimhne_Comhaid.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (licín_COUNT == 1) { Cuimhne_Comhaid.cosán_Start(1); 처리값 = Cuimhne_Comhaid.cosán_beart(0, '/'); } else 처리값 = licín_COUNT == 2 ? CONAIR(1) : -22;
            if (처리값 >= 0) 처리값 = Cuimhne_Comhaid.athraigh_eolaire(); if (처리값 < 0) ERREÁID(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argóint_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (licín_COUNT == argóint_INDEX) { Cuimhne_Comhaid.cosán_Start(1); 처리값 = Cuimhne_Comhaid.cosán_beart(0, '.'); } else 처리값 = licín_COUNT == argóint_INDEX + 1 ? CONAIR(argóint_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Cuimhne_Comhaid.경로목록(); if (처리값 < 0) ERREÁID(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) blaosc_Uirlisí.comhad_cás(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) blaosc_Uirlisí.ásc_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) blaosc_Uirlisí.Amharc_VALUE();
        else if (같음(0, "wc")) blaosc_Uirlisí.세기();
        else if (같음(0, "grep")) blaosc_Uirlisí.FIND_iontráil();
        else if (같음(0, "head") || 같음(0, "tail")) blaosc_Uirlisí.머리(같음(0, "tail"));
        else if (같음(0, "tee")) blaosc_Uirlisí.함께쓰기();
        else if (같음(0, "env")) blaosc_comhréir.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (licín_COUNT == 1) blaosc_comhréir.환경보기();
            for (int lúb_INDEX = 1; lúb_INDEX < licín_COUNT; lúb_INDEX++) { int 처리값 = blaosc_comhréir.환경설정(lúb_INDEX, 같음(0, "unset")); if (처리값 != 0) { tomhas = 처리값; 단말.Scríobh("Ordú parsáil_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) blaosc_comhréir.Rith_comhad();
        else if (같음(0, "true")) tomhas = 0;
        else if (같음(0, "false")) tomhas = 1;
        else if (같음(0, "history")) líne_Eagarthóir.seó_LOG();
        else if (같음(0, "exit")) {
            if (blaosc_comhréir.깊이 > 0) { tomhas = licín_COUNT == 1 ? blaosc_comhréir.staid_VALUE : blaosc_Uirlisí.digit_VALUE(1); if (tomhas < 0 || tomhas > 255) tomhas = 2; blaosc_comhréir.script_cuir_deireadh_le = true; }
            else if (clár.Teirminéal(2) != 0) Teirminéal(true);
            else 단말.Scríobh("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) cuir_in_eagar_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (licín_COUNT < 2) { tomhas = 2; 단말.Scríobh("사용법: rm Comhad...\n"); }
            for (int lúb_INDEX = 1; lúb_INDEX < licín_COUNT; lúb_INDEX++) { int 처리값 = CONAIR(lúb_INDEX); if (처리값 == 0) 처리값 = Cuimhne_Comhaid.지우기(); if (처리값 < 0) ERREÁID(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_suíomh = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_suíomh; 첫값 < licín_COUNT; 첫값++) { if (첫값 > Start_suíomh) 단말.문자(32); for (int lúb_INDEX = 0; lúb_INDEX < fad_VALUE[첫값]; lúb_INDEX++) clár.직렬쓰기(licín_VALUE[시작점[첫값] + lúb_INDEX]); }
            if (Start_suíomh == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Scríobh("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_beart() : Uirlisí(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); tomhas = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !blaosc_comhréir.연결중) { 단말.Scríobh("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Uirlisí(13); tomhas = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Uirlisí(15); tomhas = 처리값 < 0 ? 126 : 처리값; if (!blaosc_comhréir.연결중) { 단말.Scríobh("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Uirlisí(16); tomhas = 처리값 < 0 ? 126 : 처리값; if (!blaosc_comhréir.연결중) { 단말.Scríobh("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Méid = clár.Teirminéal(13); 단말.Scríobh("TERMINAL SIZE "); 단말.수(Méid & 65535); 단말.문자('x'); 단말.수(Méid >>> 16); 단말.문자(10); }
            else Teirminéal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { clár.Teirminéal(9); deasc.Rith_ordú(); }
        else if (같음(0, "c")) eithne.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) eithne.작업시험();
        else if (같음(0, "g")) eithne.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) eithne.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = clár.rith_úsáideoir_clár(0); if (처리값 == 0) 단말.Scríobh("ELF DEMO PASS\n"); else ERREÁID(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? uirlis_iontráil(-2, 2) : Uirlisí(-1); tomhas = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !blaosc_comhréir.연결중) { 단말.Scríobh("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) eithne.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = clár.comhad_traschur_seirbhís(1); if (처리값 < 0) ERREÁID(처리값); else { 단말.Scríobh("FTP listening "); córas_uirlis.scríobh_ADDRESS(clár.Líonra_staid(0,0)); 단말.Scríobh(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { clár.comhad_traschur_seirbhís(0); 단말.Scríobh("FTP stopped\n"); }
            else 단말.Scríobh(clár.comhad_traschur_seirbhís(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { beart.Ullmhaigh(); 단말.Scríobh("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Teanga = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (licín_COUNT != 2 || Teanga < 0) 단말.Scríobh("example java|c|python: Aschur, Comhad, 네트워크, 그래픽, Java Swing fuinneog 예제\n");
            else { int 처리값 = 예제꾸러미.suiteáil_VALUE(Teanga); if (처리값 < 0) { ERREÁID(처리값); if (처리값 == -28) 단말.Scríobh("RAM full: remove unused files, then retry example\n"); } else 단말.Scríobh("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formáid_VALUE = 실행형식();
            if (formáid_VALUE == 1 || formáid_VALUE == 2) {
                int 처리값 = uirlis_iontráil(formáid_VALUE == 1 ? -1 : 14, 0); tomhas = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !blaosc_comhréir.연결중) { 단말.Scríobh("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (formáid_VALUE == 0) { tomhas = 126; 단말.Scríobh("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { tomhas = 127; 단말.Scríobh("Unknown command. help: commands\n"); }
        }
    }
    public static void Rith_ordú() {
        beart.Ullmhaigh();
        for (int Teanga = 0; Teanga < 3; Teanga++) { int 처리값 = 예제꾸러미.suiteáil_VALUE(Teanga); if (처리값 < 0) ERREÁID(처리값); }
        seó_cabhair();
        while (true) {
            fuinneog_seisiún.Próiseas_VALUE_iontráil(); if (fuinneog_seisiún.재개()) continue;
            if (!fuinneog_seisiún.이어읽기) 단말.Scríobh("jkoros-native> "); líne_Eagarthóir.líne_na_n_orduithe = true; clár.원격대기(1); int Méid = 줄읽기(); clár.원격대기(0); líne_Eagarthóir.líne_na_n_orduithe = false;
            if (Méid == -3) continue;
            if (Méid == -2) 단말.Scríobh("Ordú parsáil_VALUE: 명령줄이 너무 깁니다\n");
            if (Méid >= 0) { blaosc_comhréir.script_cuir_deireadh_le = false; blaosc_comhréir.Rith_ordú(Líne, 0, Méid, 0); } else blaosc_comhréir.staid_VALUE = 130;
            clár.cuir_deireadh_le_cianda_ordú(blaosc_comhréir.staid_VALUE);
            líne_Eagarthóir.Méid = líne_Eagarthóir.cúrsóir_VALUE = líne_Eagarthóir.Start_fuinneog = 0;
        }
    }
}
