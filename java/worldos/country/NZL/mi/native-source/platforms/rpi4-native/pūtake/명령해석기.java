// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 rārangi_tono. Kī_horipū, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] hononga = new int[4096], tohu_uara_eb540501 = new int[4096], 시작점 = new int[32], roa_uara = new int[32];
    static int[] 편집내용 = new int[16384], whakatika_ingoa = new int[63];
    static int tohu_COUNT, whakatika_ingoa_roa, mēhua;
    static boolean 앞줄;
    static void 원바이트(int uara) { papa.직렬쓰기(uara); }
    static int 줄읽기() { return hononga_Pūwhakatika.Pānuitia(); }
    static boolean 나누기(int rahi) {
        int tūranga = 0, 끝 = 0; tohu_COUNT = 0;
        while (tūranga < rahi) {
            while (tūranga < rahi && (hononga[tūranga] == 32 || hononga[tūranga] == 9)) tūranga++;
            if (tūranga == rahi) break;
            if (tohu_COUNT == 16) { 단말.Tuhia("tono poroporo_uara: 인수가 너무 많습니다\n"); return false; }
            시작점[tohu_COUNT] = 끝; int Kī_horipū_uara = 0;
            while (tūranga < rahi) {
                int uara = hononga[tūranga++];
                if (Kī_horipū_uara == 0 && (uara == 32 || uara == 9)) break;
                if (uara == Kī_horipū_uara) { Kī_horipū_uara = 0; continue; }
                if (Kī_horipū_uara == 0 && (uara == 39 || uara == 34)) { Kī_horipū_uara = uara; continue; }
                tohu_uara_eb540501[끝++] = uara;
            }
            if (Kī_horipū_uara != 0) { 단말.Tuhia("tono poroporo_uara: 따옴표가 닫히지 않았습니다\n"); return false; }
            roa_uara[tohu_COUNT] = 끝 - 시작점[tohu_COUNT]; tohu_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_TEXT) {
        if (INDEX >= tohu_COUNT) return false;
        int tūranga_INDEX=0;
        for (int 순번=0; 순번<Word_TEXT.length(); 순번++) {
            int waehere_pūāhua=Word_TEXT.charAt(순번);
            if (waehere_pūāhua>=0xd800 && waehere_pūāhua<=0xdbff && 순번+1<Word_TEXT.length()) waehere_pūāhua=0x10000+((waehere_pūāhua-0xd800)<<10)+Word_TEXT.charAt(++순번)-0xdc00;
            int paita_COUNT=waehere_pūāhua<128?1:waehere_pūāhua<2048?2:waehere_pūāhua<65536?3:4;
            for (int SEQUENCE_uara=paita_COUNT-1; SEQUENCE_uara>=0; SEQUENCE_uara--) {
                int uara=paita_COUNT==1?waehere_pūāhua:SEQUENCE_uara==paita_COUNT-1?(paita_COUNT==2?0xc0:paita_COUNT==3?0xe0:0xf0)|(waehere_pūāhua>>(6*SEQUENCE_uara)):0x80|((waehere_pūāhua>>(6*SEQUENCE_uara))&63);
                if (tūranga_INDEX>=roa_uara[INDEX] || tohu_uara_eb540501[시작점[INDEX]+tūranga_INDEX++]!=uara) return false;
            }
        }
        return tūranga_INDEX==roa_uara[INDEX];
    }
    static int ara(int INDEX) {
        if (INDEX >= tohu_COUNT) return -22;
        int mēhua = Pūmahara_Ngā_Kōnae.ara_Start(roa_uara[INDEX]); if (mēhua < 0) return mēhua;
        for (int Loop_INDEX = 0; Loop_INDEX < roa_uara[INDEX]; Loop_INDEX++) {
            mēhua = Pūmahara_Ngā_Kōnae.ara_paita(Loop_INDEX, tohu_uara_eb540501[시작점[INDEX] + Loop_INDEX]); if (mēhua < 0) return mēhua;
        }
        return 0;
    }
    static void Pōhēhē(int INDEX) { mēhua = 1; 단말.Tuhia("Pōhēhē "); 단말.수(INDEX); 단말.문자(10); }
    static void tiro_uara() {
        if (tohu_COUNT != 2) { 단말.Tuhia("사용법: cat Kōnae\n"); return; }
        int mēhua = ara(1); if (mēhua < 0) { Pōhēhē(mēhua); return; }
        int Kōnae = Pūmahara_Ngā_Kōnae.Huaki(0); if (Kōnae < 0) { Pōhēhē(Kōnae); return; }
        while (true) { int uara = Pūmahara_Ngā_Kōnae.Pānuitia(Kōnae); if (uara == 256) break; if (uara < 0) { Pōhēhē(uara); break; } 원바이트(uara); }
        Pūmahara_Ngā_Kōnae.Kati(Kōnae); 단말.문자(10);
    }
    static void whakatika_uara() {
        if (tohu_COUNT != 2) { 단말.Tuhia("사용법: edit Kōnae\n"); return; }
        int mēhua = ara(1); if (mēhua < 0) { Pōhēhē(mēhua); return; }
        whakatika_ingoa_roa = roa_uara[1];
        for (int Loop_INDEX = 0; Loop_INDEX < whakatika_ingoa_roa; Loop_INDEX++) whakatika_ingoa[Loop_INDEX] = tohu_uara_eb540501[시작점[1] + Loop_INDEX];
        단말.Tuhia("EDIT: Kōnae 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int rahi = 0;
        while (true) {
            단말.Tuhia("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Tuhia("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && hononga[0] == '.') break;
            if (입력 + 1 > 편집내용.length - rahi) { 단말.Tuhia("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[rahi++] = hononga[Loop_INDEX];
            편집내용[rahi++] = 10;
        }
        Pūmahara_Ngā_Kōnae.ara_Start(whakatika_ingoa_roa);
        for (int Loop_INDEX = 0; Loop_INDEX < whakatika_ingoa_roa; Loop_INDEX++) Pūmahara_Ngā_Kōnae.ara_paita(Loop_INDEX, whakatika_ingoa[Loop_INDEX]);
        int Kōnae = Pūmahara_Ngā_Kōnae.Huaki(577); if (Kōnae < 0) { Pōhēhē(Kōnae); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < rahi; Loop_INDEX++) Pūmahara_Ngā_Kōnae.Tuhia(Kōnae, 편집내용[Loop_INDEX]);
        Pūmahara_Ngā_Kōnae.Kati(Kōnae); 단말.Tuhia("SAVED "); 단말.수(rahi); 단말.Tuhia("paita_uara(주기억 Kōnae)\n");
    }
    static int ira_a_ono_uara(int uara) {
        if (uara >= '0' && uara <= '9') return uara - '0';
        if (uara >= 'a' && uara <= 'f') return uara - 'a' + 10;
        if (uara >= 'A' && uara <= 'F') return uara - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (tohu_COUNT != 2) { 단말.Tuhia("사용법: load Kōnae | hex Kōnae\n"); return; }
        int mēhua = ara(1); if (mēhua < 0) { Pōhēhē(mēhua); return; }
        if (!넣기) {
            int Kōnae = Pūmahara_Ngā_Kōnae.Huaki(0); if (Kōnae < 0) { Pōhēhē(Kōnae); return; }
            단말.Tuhia("HEX BEGIN "); 단말.수(Pūmahara_Ngā_Kōnae.rahi(Kōnae)); 단말.문자(10);
            int tāurunga_COUNT = 0;
            while (true) {
                int uara = Pūmahara_Ngā_Kōnae.Pānuitia(Kōnae); if (uara < 0 || uara == 256) break;
                단말.문자("0123456789abcdef".charAt(uara >> 4)); 단말.문자("0123456789abcdef".charAt(uara & 15));
                if (++tāurunga_COUNT % 32 == 0) 단말.문자(10);
            }
            if (tāurunga_COUNT % 32 != 0) 단말.문자(10);
            Pūmahara_Ngā_Kōnae.Kati(Kōnae); 단말.Tuhia("HEX END\n"); return;
        }
        whakatika_ingoa_roa = roa_uara[1];
        for (int Loop_INDEX = 0; Loop_INDEX < whakatika_ingoa_roa; Loop_INDEX++) whakatika_ingoa[Loop_INDEX] = tohu_uara_eb540501[시작점[1] + Loop_INDEX];
        단말.Tuhia("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int rahi = 0;
        while (true) {
            단말.Tuhia("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Tuhia("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && hononga[0] == '.') break;
            int 앞 = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (hononga[Loop_INDEX] == 32 || hononga[Loop_INDEX] == 9) continue;
                int uara = ira_a_ono_uara(hononga[Loop_INDEX]);
                if (uara < 0 || rahi >= 편집내용.length) { 단말.Tuhia("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = uara; else { 편집내용[rahi++] = 앞 * 16 + uara; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Tuhia("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Pūmahara_Ngā_Kōnae.ara_Start(whakatika_ingoa_roa);
        for (int Loop_INDEX = 0; Loop_INDEX < whakatika_ingoa_roa; Loop_INDEX++) Pūmahara_Ngā_Kōnae.ara_paita(Loop_INDEX, whakatika_ingoa[Loop_INDEX]);
        int Kōnae = Pūmahara_Ngā_Kōnae.Huaki(577); if (Kōnae < 0) { Pōhēhē(Kōnae); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < rahi; Loop_INDEX++) Pūmahara_Ngā_Kōnae.Tuhia(Kōnae, 편집내용[Loop_INDEX]);
        Pūmahara_Ngā_Kōnae.Kati(Kōnae); 단말.Tuhia("LOADED "); 단말.수(rahi); 단말.Tuhia("paita_uara(주기억 Kōnae)\n");
    }
    static int Ngā_Utauta(int INDEX) {
        return utauta_tāurunga(INDEX, 1);
    }
    static int utauta_tāurunga(int INDEX, int whakahaere) {
        if (tohu_COUNT - whakahaere > 8) return -22;
        papa.인수준비(tohu_COUNT - whakahaere);
        for (int 첫값 = whakahaere; 첫값 < tohu_COUNT; 첫값++) {
            if (roa_uara[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < roa_uara[첫값]; Loop_INDEX++) papa.tohenga_paita(첫값 - whakahaere, Loop_INDEX, tohu_uara_eb540501[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? papa.리눅스파일실행() : INDEX < 0 ? papa.kawe_kaiwhakamahi_kōnae() : papa.whakahaere_kaiwhakamahi_kaupapa(INDEX);
    }
    static int PYTHON_pūpū() {
        if (tohu_COUNT > 8) return -22;
        papa.인수준비(tohu_COUNT);
        String ara = "/lib/pūpū.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int tūranga_INDEX = 0;
        for (int 순번 = 0; 순번 < ara.length(); 순번++) {
            int pūāhua_uara = ara.charAt(순번);
            if (pūāhua_uara < 128) papa.tohenga_paita(0, tūranga_INDEX++, pūāhua_uara);
            else { papa.tohenga_paita(0, tūranga_INDEX++, 0xe0 | (pūāhua_uara >> 12)); papa.tohenga_paita(0, tūranga_INDEX++, 0x80 | ((pūāhua_uara >> 6) & 63)); papa.tohenga_paita(0, tūranga_INDEX++, 0x80 | (pūāhua_uara & 63)); }
        }
        for (int 순번 = 1; 순번 < tohu_COUNT; 순번++) {
            if (roa_uara[순번] > 255) return -36;
            for (int pūāhua_uara = 0; pūāhua_uara < roa_uara[순번]; pūāhua_uara++) papa.tohenga_paita(순번, pūāhua_uara, tohu_uara_eb540501[시작점[순번] + pūāhua_uara]);
        }
        return papa.whakahaere_kaiwhakamahi_kaupapa(12);
    }
    static int 실행형식() {
        int 처리값 = ara(0); if (처리값 < 0) return 처리값;
        int Kōnae = Pūmahara_Ngā_Kōnae.Huaki(0); if (Kōnae < 0) return Kōnae;
        int 첫값 = Pūmahara_Ngā_Kōnae.Pānuitia(Kōnae), paita_raraunga = Pūmahara_Ngā_Kōnae.Pānuitia(Kōnae), waehere_pūāhua = Pūmahara_Ngā_Kōnae.Pānuitia(Kōnae), 뒷값 = Pūmahara_Ngā_Kōnae.Pānuitia(Kōnae);
        Pūmahara_Ngā_Kōnae.Kati(Kōnae);
        if (첫값 == 127 && paita_raraunga == 'E' && waehere_pūāhua == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && paita_raraunga == 'K' && waehere_pūāhua == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        papa.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) papa.tohenga_paita(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return papa.whakahaere_kaiwhakamahi_kaupapa(INDEX);
    }
    static void TEXT_paita(int Kōnae, int uara) { Pūmahara_Ngā_Kōnae.Tuhia(Kōnae, uara); }
    static void pateko_kōnae(String Ingoa, String Ihirangi_uara) {
        // pūpū 파일명은 ASCII. Kōnae 내용은 UTF-8로 저장한다.
        Pūmahara_Ngā_Kōnae.ara_Start(Ingoa.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Ingoa.length(); Loop_INDEX++) Pūmahara_Ngā_Kōnae.ara_paita(Loop_INDEX, Ingoa.charAt(Loop_INDEX));
        int Kōnae = Pūmahara_Ngā_Kōnae.Huaki(193); if (Kōnae < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Ihirangi_uara.length(); Loop_INDEX++) {
            int waehere_pūāhua = Ihirangi_uara.charAt(Loop_INDEX);
            if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdbff && Loop_INDEX + 1 < Ihirangi_uara.length()) waehere_pūāhua = 0x10000 + ((waehere_pūāhua - 0xd800) << 10) + Ihirangi_uara.charAt(++Loop_INDEX) - 0xdc00;
            if (waehere_pūāhua < 128) TEXT_paita(Kōnae, waehere_pūāhua);
            else {
                int 수 = waehere_pūāhua < 2048 ? 2 : waehere_pūāhua < 65536 ? 3 : 4;
                TEXT_paita(Kōnae, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (waehere_pūāhua >> (6 * (수 - 1))));
                for (int tāurunga_COUNT = 수 - 1; tāurunga_COUNT > 0; tāurunga_COUNT--) TEXT_paita(Kōnae, 0x80 | ((waehere_pūāhua >> (6 * (tāurunga_COUNT - 1))) & 63));
            }
        }
        Pūmahara_Ngā_Kōnae.Kati(Kōnae);
    }
    static void 한글도움말() {
        단말.Tuhia("F9 / Shift+Space: [EN] ↔ [mi]\n");
        단말.Tuhia("  [MI] keyboard; [EN] ASCII\n");
        단말.Tuhia("  a → a\n");
        단말.Tuhia("  F9: EN ↔ mi | Ctrl+Shift+V: UTF-8\n");
        단말.Tuhia("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Tuhia("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Ingoa) {
        int paita_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ingoa.length(); Loop_INDEX++) { int waehere_pūāhua = Ingoa.charAt(Loop_INDEX); if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdfff) return -22; paita_COUNT += waehere_pūāhua < 128 ? 1 : waehere_pūāhua < 2048 ? 2 : 3; }
        int 처리값 = Pūmahara_Ngā_Kōnae.ara_Start(paita_COUNT); if (처리값 < 0) return 처리값;
        int tūranga_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ingoa.length(); Loop_INDEX++) {
            int waehere_pūāhua = Ingoa.charAt(Loop_INDEX);
            if (waehere_pūāhua < 128) Pūmahara_Ngā_Kōnae.ara_paita(tūranga_INDEX++, waehere_pūāhua);
            else if (waehere_pūāhua < 2048) { Pūmahara_Ngā_Kōnae.ara_paita(tūranga_INDEX++, 0xc0 | (waehere_pūāhua >> 6)); Pūmahara_Ngā_Kōnae.ara_paita(tūranga_INDEX++, 0x80 | (waehere_pūāhua & 63)); }
            else { Pūmahara_Ngā_Kōnae.ara_paita(tūranga_INDEX++, 0xe0 | (waehere_pūāhua >> 12)); Pūmahara_Ngā_Kōnae.ara_paita(tūranga_INDEX++, 0x80 | ((waehere_pūāhua >> 6) & 63)); Pūmahara_Ngā_Kōnae.ara_paita(tūranga_INDEX++, 0x80 | (waehere_pūāhua & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Ingoa) {
        int 처리값 = 예제경로(Ingoa); if (처리값 < 0) return 처리값;
        처리값 = Pūmahara_Ngā_Kōnae.Waihanga_whaiaronga(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Ingoa, String raraunga) {
        int 처리값 = 예제경로(Ingoa); if (처리값 < 0) return 처리값;
        int Kōnae = Pūmahara_Ngā_Kōnae.Huaki(193); if (Kōnae == -17) return 0; if (Kōnae < 0) return Kōnae;
        for (int Loop_INDEX = 0; Loop_INDEX < raraunga.length(); Loop_INDEX += 2) {
            처리값 = Pūmahara_Ngā_Kōnae.Tuhia(Kōnae, ira_a_ono_uara(raraunga.charAt(Loop_INDEX)) * 16 + ira_a_ono_uara(raraunga.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Pūmahara_Ngā_Kōnae.Kati(Kōnae); return 처리값; }
        }
        return Pūmahara_Ngā_Kōnae.Kati(Kōnae);
    }
    static void whakaatu_āwhina() {
        pūnaha_utauta.whakaatu_āwhina();
        단말.Tuhia("sshd / haumaru_anga start|stop|status: SSH :22 (user, 장치별 kupuhipa_uara)\n");
        단말.Tuhia("vncd / mamao_whakaatu start|stop|status: VNC :5900 (장치별 kupuhipa_uara)\n");
        단말.Tuhia("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Tuhia("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Tuhia("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Tuhia("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Tuhia("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Tuhia("모서리 + 왼쪽 버튼 tō_uara: Tauranga rahi huri_uara; terminal size: tīwae_uara/ROW_uara\n");
        단말.Tuhia("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Tuhia("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Tuhia("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Tuhia("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Tuhia("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Tuhia("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Tuhia("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Tuhia("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Tuhia("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Tuhia("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Tuhia("pip: MicroPython pūtake_rākau tāuta_uara; taurima --network --pip 필요; /lib는 RAM\n");
        단말.Tuhia("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Tuhia("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Tuhia("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Tuhia("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Tauranga(boolean 전환여부) {
        if (전환여부 && papa.Tauranga(2) != 0) { papa.Tauranga(0); 단말.Tuhia("TERMINAL CLOSED\n"); }
        else if (papa.Tauranga(1) < 0) Pōhēhē(-19);
        else 단말.Tuhia("TERMINAL READY — mi terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void tono() {
        if (tohu_COUNT == 0) return;
        if (pūnaha_utauta.kawe_tono()) return;
        if (같음(0,"sshd") || 같음(0,"haumaru_anga") || 같음(0,"vncd") || 같음(0,"mamao_whakaatu")) {
            int 종류=같음(0,"vncd")||같음(0,"mamao_whakaatu")?1:0;
            int hohenga=같음(1,"start")||같음(1,"whakahaere")?1:같음(1,"stop")||같음(1,"Whakamutua")?0:2;
            int tūnga_uara=papa.mātaki(종류,hohenga);
            if(tūnga_uara<0)Pōhēhē(tūnga_uara);else 단말.Tuhia(papa.mātaki(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else whakaatu_āwhina(); }
        else if (같음(0, "info") || 같음(0, "i")) kākano.msinfo32_exe();
        else if (같음(0, "pwd")) { Pūmahara_Ngā_Kōnae.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (tohu_COUNT == 1) { Pūmahara_Ngā_Kōnae.ara_Start(1); 처리값 = Pūmahara_Ngā_Kōnae.ara_paita(0, '/'); } else 처리값 = tohu_COUNT == 2 ? ara(1) : -22;
            if (처리값 >= 0) 처리값 = Pūmahara_Ngā_Kōnae.huri_whaiaronga(); if (처리값 < 0) Pōhēhē(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int tohenga_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (tohu_COUNT == tohenga_INDEX) { Pūmahara_Ngā_Kōnae.ara_Start(1); 처리값 = Pūmahara_Ngā_Kōnae.ara_paita(0, '.'); } else 처리값 = tohu_COUNT == tohenga_INDEX + 1 ? ara(tohenga_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Pūmahara_Ngā_Kōnae.경로목록(); if (처리값 < 0) Pōhēhē(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) anga_Ngā_Utauta.kōnae_kēhi(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) anga_Ngā_Utauta.tārua_uara(같음(0, "mv"));
        else if (같음(0, "cat")) anga_Ngā_Utauta.tiro_uara();
        else if (같음(0, "wc")) anga_Ngā_Utauta.세기();
        else if (같음(0, "grep")) anga_Ngā_Utauta.FIND_tāurunga();
        else if (같음(0, "head") || 같음(0, "tail")) anga_Ngā_Utauta.머리(같음(0, "tail"));
        else if (같음(0, "tee")) anga_Ngā_Utauta.함께쓰기();
        else if (같음(0, "env")) anga_wetereo.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (tohu_COUNT == 1) anga_wetereo.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < tohu_COUNT; Loop_INDEX++) { int 처리값 = anga_wetereo.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { mēhua = 처리값; 단말.Tuhia("tono poroporo_uara: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) anga_wetereo.kawe_kōnae();
        else if (같음(0, "true")) mēhua = 0;
        else if (같음(0, "false")) mēhua = 1;
        else if (같음(0, "history")) hononga_Pūwhakatika.whakaatu_LOG();
        else if (같음(0, "exit")) {
            if (anga_wetereo.깊이 > 0) { mēhua = tohu_COUNT == 1 ? anga_wetereo.tūnga_uara : anga_Ngā_Utauta.mati_uara(1); if (mēhua < 0 || mēhua > 255) mēhua = 2; anga_wetereo.hōtuhi_mutu = true; }
            else if (papa.Tauranga(2) != 0) Tauranga(true);
            else 단말.Tuhia("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) whakatika_uara();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (tohu_COUNT < 2) { mēhua = 2; 단말.Tuhia("사용법: rm Kōnae...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < tohu_COUNT; Loop_INDEX++) { int 처리값 = ara(Loop_INDEX); if (처리값 == 0) 처리값 = Pūmahara_Ngā_Kōnae.지우기(); if (처리값 < 0) Pōhēhē(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_tūranga = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_tūranga; 첫값 < tohu_COUNT; 첫값++) { if (첫값 > Start_tūranga) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < roa_uara[첫값]; Loop_INDEX++) papa.직렬쓰기(tohu_uara_eb540501[시작점[첫값] + Loop_INDEX]); }
            if (Start_tūranga == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Tuhia("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_pūpū() : Ngā_Utauta(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); mēhua = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !anga_wetereo.연결중) { 단말.Tuhia("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Ngā_Utauta(13); mēhua = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Ngā_Utauta(15); mēhua = 처리값 < 0 ? 126 : 처리값; if (!anga_wetereo.연결중) { 단말.Tuhia("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Ngā_Utauta(16); mēhua = 처리값 < 0 ? 126 : 처리값; if (!anga_wetereo.연결중) { 단말.Tuhia("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int rahi = papa.Tauranga(13); 단말.Tuhia("TERMINAL SIZE "); 단말.수(rahi & 65535); 단말.문자('x'); 단말.수(rahi >>> 16); 단말.문자(10); }
            else Tauranga(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { papa.Tauranga(9); papamahi.kawe_tono(); }
        else if (같음(0, "c")) kākano.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kākano.작업시험();
        else if (같음(0, "g")) kākano.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kākano.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = papa.whakahaere_kaiwhakamahi_kaupapa(0); if (처리값 == 0) 단말.Tuhia("ELF DEMO PASS\n"); else Pōhēhē(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? utauta_tāurunga(-2, 2) : Ngā_Utauta(-1); mēhua = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !anga_wetereo.연결중) { 단말.Tuhia("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kākano.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = papa.kōnae_whakawhiti_ratonga(1); if (처리값 < 0) Pōhēhē(처리값); else { 단말.Tuhia("FTP listening "); pūnaha_utauta.tuhi_ADDRESS(papa.whatunga_tūnga(0,0)); 단말.Tuhia(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { papa.kōnae_whakawhiti_ratonga(0); 단말.Tuhia("FTP stopped\n"); }
            else 단말.Tuhia(papa.kōnae_whakawhiti_ratonga(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { pūpū.Whakarite(); 단말.Tuhia("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int reo = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (tohu_COUNT != 2 || reo < 0) 단말.Tuhia("example java|c|python: 출력, Kōnae, 네트워크, 그래픽, Java Swing matapihi 예제\n");
            else { int 처리값 = 예제꾸러미.tāuta_uara(reo); if (처리값 < 0) { Pōhēhē(처리값); if (처리값 == -28) 단말.Tuhia("RAM full: remove unused files, then retry example\n"); } else 단말.Tuhia("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int hōputu_uara = 실행형식();
            if (hōputu_uara == 1 || hōputu_uara == 2) {
                int 처리값 = utauta_tāurunga(hōputu_uara == 1 ? -1 : 14, 0); mēhua = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !anga_wetereo.연결중) { 단말.Tuhia("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (hōputu_uara == 0) { mēhua = 126; 단말.Tuhia("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { mēhua = 127; 단말.Tuhia("Unknown command. help: commands\n"); }
        }
    }
    public static void kawe_tono() {
        pūpū.Whakarite();
        for (int reo = 0; reo < 3; reo++) { int 처리값 = 예제꾸러미.tāuta_uara(reo); if (처리값 < 0) Pōhēhē(처리값); }
        whakaatu_āwhina();
        while (true) {
            matapihi_wātū.Hātepe_uara_tāurunga(); if (matapihi_wātū.재개()) continue;
            if (!matapihi_wātū.이어읽기) 단말.Tuhia("jkoros-native> "); hononga_Pūwhakatika.rārangi_tono = true; papa.원격대기(1); int rahi = 줄읽기(); papa.원격대기(0); hononga_Pūwhakatika.rārangi_tono = false;
            if (rahi == -3) continue;
            if (rahi == -2) 단말.Tuhia("tono poroporo_uara: 명령줄이 너무 깁니다\n");
            if (rahi >= 0) { anga_wetereo.hōtuhi_mutu = false; anga_wetereo.kawe_tono(hononga, 0, rahi, 0); } else anga_wetereo.tūnga_uara = 130;
            papa.mutu_mamao_tono(anga_wetereo.tūnga_uara);
            hononga_Pūwhakatika.rahi = hononga_Pūwhakatika.pehu_uara = hononga_Pūwhakatika.Start_matapihi = 0;
        }
    }
}
