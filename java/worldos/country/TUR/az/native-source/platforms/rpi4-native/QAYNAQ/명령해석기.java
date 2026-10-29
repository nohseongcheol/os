// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 əmr_sətri. Dırnaqarası, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Giriş = new int[4096], nişan_VALUE = new int[4096], 시작점 = new int[32], uzunluq_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], redaktə_ad = new int[63];
    static int nişan_COUNT, redaktə_ad_uzunluq, ölçü;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { lövhə.직렬쓰기(VALUE); }
    static int 줄읽기() { return xətt_Redaktor.Oxuma(); }
    static boolean 나누기(int Böyüklük) {
        int yerinə_qoymaq = 0, 끝 = 0; nişan_COUNT = 0;
        while (yerinə_qoymaq < Böyüklük) {
            while (yerinə_qoymaq < Böyüklük && (Giriş[yerinə_qoymaq] == 32 || Giriş[yerinə_qoymaq] == 9)) yerinə_qoymaq++;
            if (yerinə_qoymaq == Böyüklük) break;
            if (nişan_COUNT == 16) { 단말.Yazma("Əmr parselləmək_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[nişan_COUNT] = 끝; int Dırnaqarası_VALUE = 0;
            while (yerinə_qoymaq < Böyüklük) {
                int VALUE = Giriş[yerinə_qoymaq++];
                if (Dırnaqarası_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Dırnaqarası_VALUE) { Dırnaqarası_VALUE = 0; continue; }
                if (Dırnaqarası_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Dırnaqarası_VALUE = VALUE; continue; }
                nişan_VALUE[끝++] = VALUE;
            }
            if (Dırnaqarası_VALUE != 0) { 단말.Yazma("Əmr parselləmək_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            uzunluq_VALUE[nişan_COUNT] = 끝 - 시작점[nişan_COUNT]; nişan_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Söz_SMS) {
        if (INDEX >= nişan_COUNT) return false;
        int yerinə_qoymaq_INDEX=0;
        for (int 순번=0; 순번<Söz_SMS.length(); 순번++) {
            int simvol_kodu=Söz_SMS.charAt(순번);
            if (simvol_kodu>=0xd800 && simvol_kodu<=0xdbff && 순번+1<Söz_SMS.length()) simvol_kodu=0x10000+((simvol_kodu-0xd800)<<10)+Söz_SMS.charAt(++순번)-0xdc00;
            int bayt_COUNT=simvol_kodu<128?1:simvol_kodu<2048?2:simvol_kodu<65536?3:4;
            for (int SEQUENCE_VALUE=bayt_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bayt_COUNT==1?simvol_kodu:SEQUENCE_VALUE==bayt_COUNT-1?(bayt_COUNT==2?0xc0:bayt_COUNT==3?0xe0:0xf0)|(simvol_kodu>>(6*SEQUENCE_VALUE)):0x80|((simvol_kodu>>(6*SEQUENCE_VALUE))&63);
                if (yerinə_qoymaq_INDEX>=uzunluq_VALUE[INDEX] || nişan_VALUE[시작점[INDEX]+yerinə_qoymaq_INDEX++]!=VALUE) return false;
            }
        }
        return yerinə_qoymaq_INDEX==uzunluq_VALUE[INDEX];
    }
    static int Cığır(int INDEX) {
        if (INDEX >= nişan_COUNT) return -22;
        int ölçü = Yaddaş_Fayllar.yol_Başla(uzunluq_VALUE[INDEX]); if (ölçü < 0) return ölçü;
        for (int Loop_INDEX = 0; Loop_INDEX < uzunluq_VALUE[INDEX]; Loop_INDEX++) {
            ölçü = Yaddaş_Fayllar.yol_bayt(Loop_INDEX, nişan_VALUE[시작점[INDEX] + Loop_INDEX]); if (ölçü < 0) return ölçü;
        }
        return 0;
    }
    static void XƏTA(int INDEX) { ölçü = 1; 단말.Yazma("XƏTA "); 단말.수(INDEX); 단말.문자(10); }
    static void baxmaq_VALUE() {
        if (nişan_COUNT != 2) { 단말.Yazma("사용법: cat FAYL\n"); return; }
        int ölçü = Cığır(1); if (ölçü < 0) { XƏTA(ölçü); return; }
        int FAYL = Yaddaş_Fayllar.Aç(0); if (FAYL < 0) { XƏTA(FAYL); return; }
        while (true) { int VALUE = Yaddaş_Fayllar.Oxuma(FAYL); if (VALUE == 256) break; if (VALUE < 0) { XƏTA(VALUE); break; } 원바이트(VALUE); }
        Yaddaş_Fayllar.Bağla(FAYL); 단말.문자(10);
    }
    static void redaktə_VALUE() {
        if (nişan_COUNT != 2) { 단말.Yazma("사용법: edit FAYL\n"); return; }
        int ölçü = Cığır(1); if (ölçü < 0) { XƏTA(ölçü); return; }
        redaktə_ad_uzunluq = uzunluq_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < redaktə_ad_uzunluq; Loop_INDEX++) redaktə_ad[Loop_INDEX] = nişan_VALUE[시작점[1] + Loop_INDEX];
        단말.Yazma("EDIT: FAYL 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Böyüklük = 0;
        while (true) {
            단말.Yazma("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Yazma("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Giriş[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Böyüklük) { 단말.Yazma("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[Böyüklük++] = Giriş[Loop_INDEX];
            편집내용[Böyüklük++] = 10;
        }
        Yaddaş_Fayllar.yol_Başla(redaktə_ad_uzunluq);
        for (int Loop_INDEX = 0; Loop_INDEX < redaktə_ad_uzunluq; Loop_INDEX++) Yaddaş_Fayllar.yol_bayt(Loop_INDEX, redaktə_ad[Loop_INDEX]);
        int FAYL = Yaddaş_Fayllar.Aç(577); if (FAYL < 0) { XƏTA(FAYL); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Böyüklük; Loop_INDEX++) Yaddaş_Fayllar.Yazma(FAYL, 편집내용[Loop_INDEX]);
        Yaddaş_Fayllar.Bağla(FAYL); 단말.Yazma("SAVED "); 단말.수(Böyüklük); 단말.Yazma("bayt_VALUE(주기억 FAYL)\n");
    }
    static int onaltılıq_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (nişan_COUNT != 2) { 단말.Yazma("사용법: load FAYL | hex FAYL\n"); return; }
        int ölçü = Cığır(1); if (ölçü < 0) { XƏTA(ölçü); return; }
        if (!넣기) {
            int FAYL = Yaddaş_Fayllar.Aç(0); if (FAYL < 0) { XƏTA(FAYL); return; }
            단말.Yazma("HEX BEGIN "); 단말.수(Yaddaş_Fayllar.Böyüklük(FAYL)); 단말.문자(10);
            int daxiletmə_COUNT = 0;
            while (true) {
                int VALUE = Yaddaş_Fayllar.Oxuma(FAYL); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++daxiletmə_COUNT % 32 == 0) 단말.문자(10);
            }
            if (daxiletmə_COUNT % 32 != 0) 단말.문자(10);
            Yaddaş_Fayllar.Bağla(FAYL); 단말.Yazma("HEX END\n"); return;
        }
        redaktə_ad_uzunluq = uzunluq_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < redaktə_ad_uzunluq; Loop_INDEX++) redaktə_ad[Loop_INDEX] = nişan_VALUE[시작점[1] + Loop_INDEX];
        단말.Yazma("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Böyüklük = 0;
        while (true) {
            단말.Yazma("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Yazma("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Giriş[0] == '.') break;
            int ön_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Giriş[Loop_INDEX] == 32 || Giriş[Loop_INDEX] == 9) continue;
                int VALUE = onaltılıq_VALUE(Giriş[Loop_INDEX]);
                if (VALUE < 0 || Böyüklük >= 편집내용.length) { 단말.Yazma("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (ön_VALUE < 0) ön_VALUE = VALUE; else { 편집내용[Böyüklük++] = ön_VALUE * 16 + VALUE; ön_VALUE = -1; }
            }
            if (ön_VALUE >= 0) { 단말.Yazma("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Yaddaş_Fayllar.yol_Başla(redaktə_ad_uzunluq);
        for (int Loop_INDEX = 0; Loop_INDEX < redaktə_ad_uzunluq; Loop_INDEX++) Yaddaş_Fayllar.yol_bayt(Loop_INDEX, redaktə_ad[Loop_INDEX]);
        int FAYL = Yaddaş_Fayllar.Aç(577); if (FAYL < 0) { XƏTA(FAYL); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Böyüklük; Loop_INDEX++) Yaddaş_Fayllar.Yazma(FAYL, 편집내용[Loop_INDEX]);
        Yaddaş_Fayllar.Bağla(FAYL); 단말.Yazma("LOADED "); 단말.수(Böyüklük); 단말.Yazma("bayt_VALUE(주기억 FAYL)\n");
    }
    static int Alətlər(int INDEX) {
        return alət_daxiletmə(INDEX, 1);
    }
    static int alət_daxiletmə(int INDEX, int İcra_Et) {
        if (nişan_COUNT - İcra_Et > 8) return -22;
        lövhə.인수준비(nişan_COUNT - İcra_Et);
        for (int 첫값 = İcra_Et; 첫값 < nişan_COUNT; 첫값++) {
            if (uzunluq_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < uzunluq_VALUE[첫값]; Loop_INDEX++) lövhə.arqument_bayt(첫값 - İcra_Et, Loop_INDEX, nişan_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? lövhə.리눅스파일실행() : INDEX < 0 ? lövhə.icra_etmək_istifadəçi_fayl() : lövhə.icra_istifadəçi_proqram(INDEX);
    }
    static int PYTHON_paket() {
        if (nişan_COUNT > 8) return -22;
        lövhə.인수준비(nişan_COUNT);
        String Cığır = "/lib/paket.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int yerinə_qoymaq_INDEX = 0;
        for (int 순번 = 0; 순번 < Cığır.length(); 순번++) {
            int simvol_VALUE_068c2631 = Cığır.charAt(순번);
            if (simvol_VALUE_068c2631 < 128) lövhə.arqument_bayt(0, yerinə_qoymaq_INDEX++, simvol_VALUE_068c2631);
            else { lövhə.arqument_bayt(0, yerinə_qoymaq_INDEX++, 0xe0 | (simvol_VALUE_068c2631 >> 12)); lövhə.arqument_bayt(0, yerinə_qoymaq_INDEX++, 0x80 | ((simvol_VALUE_068c2631 >> 6) & 63)); lövhə.arqument_bayt(0, yerinə_qoymaq_INDEX++, 0x80 | (simvol_VALUE_068c2631 & 63)); }
        }
        for (int 순번 = 1; 순번 < nişan_COUNT; 순번++) {
            if (uzunluq_VALUE[순번] > 255) return -36;
            for (int simvol_VALUE_068c2631 = 0; simvol_VALUE_068c2631 < uzunluq_VALUE[순번]; simvol_VALUE_068c2631++) lövhə.arqument_bayt(순번, simvol_VALUE_068c2631, nişan_VALUE[시작점[순번] + simvol_VALUE_068c2631]);
        }
        return lövhə.icra_istifadəçi_proqram(12);
    }
    static int 실행형식() {
        int 처리값 = Cığır(0); if (처리값 < 0) return 처리값;
        int FAYL = Yaddaş_Fayllar.Aç(0); if (FAYL < 0) return FAYL;
        int 첫값 = Yaddaş_Fayllar.Oxuma(FAYL), bayt_verilənlər = Yaddaş_Fayllar.Oxuma(FAYL), simvol_kodu = Yaddaş_Fayllar.Oxuma(FAYL), 뒷값 = Yaddaş_Fayllar.Oxuma(FAYL);
        Yaddaş_Fayllar.Bağla(FAYL);
        if (첫값 == 127 && bayt_verilənlər == 'E' && simvol_kodu == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bayt_verilənlər == 'K' && simvol_kodu == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        lövhə.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) lövhə.arqument_bayt(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return lövhə.icra_istifadəçi_proqram(INDEX);
    }
    static void SMS_bayt(int FAYL, int VALUE) { Yaddaş_Fayllar.Yazma(FAYL, VALUE); }
    static void statik_fayl(String Ad, String Məzmun_VALUE) {
        // paket 파일명은 ASCII. FAYL 내용은 UTF-8로 저장한다.
        Yaddaş_Fayllar.yol_Başla(Ad.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Ad.length(); Loop_INDEX++) Yaddaş_Fayllar.yol_bayt(Loop_INDEX, Ad.charAt(Loop_INDEX));
        int FAYL = Yaddaş_Fayllar.Aç(193); if (FAYL < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Məzmun_VALUE.length(); Loop_INDEX++) {
            int simvol_kodu = Məzmun_VALUE.charAt(Loop_INDEX);
            if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdbff && Loop_INDEX + 1 < Məzmun_VALUE.length()) simvol_kodu = 0x10000 + ((simvol_kodu - 0xd800) << 10) + Məzmun_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (simvol_kodu < 128) SMS_bayt(FAYL, simvol_kodu);
            else {
                int 수 = simvol_kodu < 2048 ? 2 : simvol_kodu < 65536 ? 3 : 4;
                SMS_bayt(FAYL, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (simvol_kodu >> (6 * (수 - 1))));
                for (int daxiletmə_COUNT = 수 - 1; daxiletmə_COUNT > 0; daxiletmə_COUNT--) SMS_bayt(FAYL, 0x80 | ((simvol_kodu >> (6 * (daxiletmə_COUNT - 1))) & 63));
            }
        }
        Yaddaş_Fayllar.Bağla(FAYL);
    }
    static void 한글도움말() {
        단말.Yazma("F9 / Shift+Space: [EN] ↔ [az]\n");
        단말.Yazma("  [AZ] keyboard; [EN] ASCII\n");
        단말.Yazma("  a → a\n");
        단말.Yazma("  F9: EN ↔ az | Ctrl+Shift+V: UTF-8\n");
        단말.Yazma("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Yazma("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Ad) {
        int bayt_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ad.length(); Loop_INDEX++) { int simvol_kodu = Ad.charAt(Loop_INDEX); if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdfff) return -22; bayt_COUNT += simvol_kodu < 128 ? 1 : simvol_kodu < 2048 ? 2 : 3; }
        int 처리값 = Yaddaş_Fayllar.yol_Başla(bayt_COUNT); if (처리값 < 0) return 처리값;
        int yerinə_qoymaq_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ad.length(); Loop_INDEX++) {
            int simvol_kodu = Ad.charAt(Loop_INDEX);
            if (simvol_kodu < 128) Yaddaş_Fayllar.yol_bayt(yerinə_qoymaq_INDEX++, simvol_kodu);
            else if (simvol_kodu < 2048) { Yaddaş_Fayllar.yol_bayt(yerinə_qoymaq_INDEX++, 0xc0 | (simvol_kodu >> 6)); Yaddaş_Fayllar.yol_bayt(yerinə_qoymaq_INDEX++, 0x80 | (simvol_kodu & 63)); }
            else { Yaddaş_Fayllar.yol_bayt(yerinə_qoymaq_INDEX++, 0xe0 | (simvol_kodu >> 12)); Yaddaş_Fayllar.yol_bayt(yerinə_qoymaq_INDEX++, 0x80 | ((simvol_kodu >> 6) & 63)); Yaddaş_Fayllar.yol_bayt(yerinə_qoymaq_INDEX++, 0x80 | (simvol_kodu & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Ad) {
        int 처리값 = 예제경로(Ad); if (처리값 < 0) return 처리값;
        처리값 = Yaddaş_Fayllar.yarat_kataloq(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Ad, String verilənlər) {
        int 처리값 = 예제경로(Ad); if (처리값 < 0) return 처리값;
        int FAYL = Yaddaş_Fayllar.Aç(193); if (FAYL == -17) return 0; if (FAYL < 0) return FAYL;
        for (int Loop_INDEX = 0; Loop_INDEX < verilənlər.length(); Loop_INDEX += 2) {
            처리값 = Yaddaş_Fayllar.Yazma(FAYL, onaltılıq_VALUE(verilənlər.charAt(Loop_INDEX)) * 16 + onaltılıq_VALUE(verilənlər.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Yaddaş_Fayllar.Bağla(FAYL); return 처리값; }
        }
        return Yaddaş_Fayllar.Bağla(FAYL);
    }
    static void göstərmək_kömək() {
        sistem_alət.göstərmək_kömək();
        단말.Yazma("sshd / təhlükəsiz_örtük start|stop|status: SSH :22 (user, 장치별 parol_VALUE)\n");
        단말.Yazma("vncd / uzaq_displey start|stop|status: VNC :5900 (장치별 parol_VALUE)\n");
        단말.Yazma("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Yazma("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Yazma("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Yazma("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Yazma("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Yazma("모서리 + 왼쪽 버튼 sürükləmək_VALUE: Terminal Böyüklük dəyişdirmək_VALUE; terminal size: sütun_VALUE/ROW_VALUE\n");
        단말.Yazma("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Yazma("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Yazma("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Yazma("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Yazma("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Yazma("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Yazma("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Yazma("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Yazma("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Yazma("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Yazma("pip: MicroPython mənbə_ağac quraşdır_VALUE; host --network --pip 필요; /lib는 RAM\n");
        단말.Yazma("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Yazma("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Yazma("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Yazma("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && lövhə.Terminal(2) != 0) { lövhə.Terminal(0); 단말.Yazma("TERMINAL CLOSED\n"); }
        else if (lövhə.Terminal(1) < 0) XƏTA(-19);
        else 단말.Yazma("TERMINAL READY — az terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Əmr() {
        if (nişan_COUNT == 0) return;
        if (sistem_alət.icra_etmək_əmr()) return;
        if (같음(0,"sshd") || 같음(0,"təhlükəsiz_örtük") || 같음(0,"vncd") || 같음(0,"uzaq_displey")) {
            int 종류=같음(0,"vncd")||같음(0,"uzaq_displey")?1:0;
            int Gedişat=같음(1,"start")||같음(1,"İcra_Et")?1:같음(1,"stop")||같음(1,"Dayan")?0:2;
            int vəziyyət_VALUE=lövhə.kölgələmə(종류,Gedişat);
            if(vəziyyət_VALUE<0)XƏTA(vəziyyət_VALUE);else 단말.Yazma(lövhə.kölgələmə(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else göstərmək_kömək(); }
        else if (같음(0, "info") || 같음(0, "i")) nüvə.msinfo32_exe();
        else if (같음(0, "pwd")) { Yaddaş_Fayllar.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (nişan_COUNT == 1) { Yaddaş_Fayllar.yol_Başla(1); 처리값 = Yaddaş_Fayllar.yol_bayt(0, '/'); } else 처리값 = nişan_COUNT == 2 ? Cığır(1) : -22;
            if (처리값 >= 0) 처리값 = Yaddaş_Fayllar.dəyişdirmək_kataloq(); if (처리값 < 0) XƏTA(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int arqument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (nişan_COUNT == arqument_INDEX) { Yaddaş_Fayllar.yol_Başla(1); 처리값 = Yaddaş_Fayllar.yol_bayt(0, '.'); } else 처리값 = nişan_COUNT == arqument_INDEX + 1 ? Cığır(arqument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Yaddaş_Fayllar.경로목록(); if (처리값 < 0) XƏTA(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) örtük_Alətlər.fayl_müqavilə(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) örtük_Alətlər.nümunə_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) örtük_Alətlər.baxmaq_VALUE();
        else if (같음(0, "wc")) örtük_Alətlər.세기();
        else if (같음(0, "grep")) örtük_Alətlər.FIND_daxiletmə();
        else if (같음(0, "head") || 같음(0, "tail")) örtük_Alətlər.머리(같음(0, "tail"));
        else if (같음(0, "tee")) örtük_Alətlər.함께쓰기();
        else if (같음(0, "env")) örtük_sintaksis.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (nişan_COUNT == 1) örtük_sintaksis.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < nişan_COUNT; Loop_INDEX++) { int 처리값 = örtük_sintaksis.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { ölçü = 처리값; 단말.Yazma("Əmr parselləmək_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) örtük_sintaksis.icra_etmək_fayl();
        else if (같음(0, "true")) ölçü = 0;
        else if (같음(0, "false")) ölçü = 1;
        else if (같음(0, "history")) xətt_Redaktor.göstərmək_LOG();
        else if (같음(0, "exit")) {
            if (örtük_sintaksis.깊이 > 0) { ölçü = nişan_COUNT == 1 ? örtük_sintaksis.vəziyyət_VALUE : örtük_Alətlər.rəqəm_VALUE(1); if (ölçü < 0 || ölçü > 255) ölçü = 2; örtük_sintaksis.skript_bitirmək = true; }
            else if (lövhə.Terminal(2) != 0) Terminal(true);
            else 단말.Yazma("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) redaktə_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (nişan_COUNT < 2) { ölçü = 2; 단말.Yazma("사용법: rm FAYL...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < nişan_COUNT; Loop_INDEX++) { int 처리값 = Cığır(Loop_INDEX); if (처리값 == 0) 처리값 = Yaddaş_Fayllar.silmək_daxiletmə_c8dbc399(); if (처리값 < 0) XƏTA(처리값); }
        }
        else if (같음(0, "echo")) {
            int Başla_yerinə_qoymaq = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Başla_yerinə_qoymaq; 첫값 < nişan_COUNT; 첫값++) { if (첫값 > Başla_yerinə_qoymaq) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < uzunluq_VALUE[첫값]; Loop_INDEX++) lövhə.직렬쓰기(nişan_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Başla_yerinə_qoymaq == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Yazma("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_paket() : Alətlər(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); ölçü = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !örtük_sintaksis.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Alətlər(13); ölçü = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Alətlər(15); ölçü = 처리값 < 0 ? 126 : 처리값; if (!örtük_sintaksis.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Alətlər(16); ölçü = 처리값 < 0 ? 126 : 처리값; if (!örtük_sintaksis.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Böyüklük = lövhə.Terminal(13); 단말.Yazma("TERMINAL SIZE "); 단말.수(Böyüklük & 65535); 단말.문자('x'); 단말.수(Böyüklük >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { lövhə.Terminal(9); iş_masası.icra_etmək_əmr(); }
        else if (같음(0, "c")) nüvə.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) nüvə.작업시험();
        else if (같음(0, "g")) nüvə.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) nüvə.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = lövhə.icra_istifadəçi_proqram(0); if (처리값 == 0) 단말.Yazma("ELF DEMO PASS\n"); else XƏTA(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? alət_daxiletmə(-2, 2) : Alətlər(-1); ölçü = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !örtük_sintaksis.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) nüvə.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = lövhə.fayl_ötürmə_xidmət(1); if (처리값 < 0) XƏTA(처리값); else { 단말.Yazma("FTP listening "); sistem_alət.yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(0,0)); 단말.Yazma(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { lövhə.fayl_ötürmə_xidmət(0); 단말.Yazma("FTP stopped\n"); }
            else 단말.Yazma(lövhə.fayl_ötürmə_xidmət(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { paket.Hazırla(); 단말.Yazma("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Dil = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (nişan_COUNT != 2 || Dil < 0) 단말.Yazma("example java|c|python: 출력, FAYL, 네트워크, 그래픽, Java Swing pəncərə 예제\n");
            else { int 처리값 = 예제꾸러미.quraşdır_VALUE(Dil); if (처리값 < 0) { XƏTA(처리값); if (처리값 == -28) 단말.Yazma("RAM full: remove unused files, then retry example\n"); } else 단말.Yazma("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = alət_daxiletmə(format_VALUE == 1 ? -1 : 14, 0); ölçü = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !örtük_sintaksis.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { ölçü = 126; 단말.Yazma("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { ölçü = 127; 단말.Yazma("Unknown command. help: commands\n"); }
        }
    }
    public static void icra_etmək_əmr() {
        paket.Hazırla();
        for (int Dil = 0; Dil < 3; Dil++) { int 처리값 = 예제꾸러미.quraşdır_VALUE(Dil); if (처리값 < 0) XƏTA(처리값); }
        göstərmək_kömək();
        while (true) {
            pəncərə_seans.Proses_VALUE_daxiletmə(); if (pəncərə_seans.재개()) continue;
            if (!pəncərə_seans.이어읽기) 단말.Yazma("jkoros-native> "); xətt_Redaktor.əmr_sətri = true; lövhə.uzaq_gözlə(1); int Böyüklük = 줄읽기(); lövhə.uzaq_gözlə(0); xətt_Redaktor.əmr_sətri = false;
            if (Böyüklük == -3) continue;
            if (Böyüklük == -2) 단말.Yazma("Əmr parselləmək_VALUE: 명령줄이 너무 깁니다\n");
            if (Böyüklük >= 0) { örtük_sintaksis.skript_bitirmək = false; örtük_sintaksis.icra_etmək_əmr(Giriş, 0, Böyüklük, 0); } else örtük_sintaksis.vəziyyət_VALUE = 130;
            lövhə.bitirmək_uzaq_əmr(örtük_sintaksis.vəziyyət_VALUE);
            xətt_Redaktor.Böyüklük = xətt_Redaktor.kursor_VALUE = xətt_Redaktor.Başla_pəncərə = 0;
        }
    }
}
