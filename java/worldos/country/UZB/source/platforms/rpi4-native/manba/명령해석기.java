// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 buyruq_satri. Sitata_kiritish, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] satr = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], uzunlik_VALUE = new int[32];
    static int[] 편집내용 = new int[16384], tahrirlamoq_nom = new int[63];
    static int token_COUNT, tahrirlamoq_nom_uzunlik, o_lchov;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { yozuv_taxtasi.직렬쓰기(VALUE); }
    static int 줄읽기() { return satr_Muharrir.Oʻqish(); }
    static boolean 나누기(int Hajmi) {
        int Holati = 0, 끝 = 0; token_COUNT = 0;
        while (Holati < Hajmi) {
            while (Holati < Hajmi && (satr[Holati] == 32 || satr[Holati] == 9)) Holati++;
            if (Holati == Hajmi) break;
            if (token_COUNT == 16) { 단말.Yozish("Buyruq tahlil_qilmoq_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Sitata_kiritish_VALUE = 0;
            while (Holati < Hajmi) {
                int VALUE = satr[Holati++];
                if (Sitata_kiritish_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Sitata_kiritish_VALUE) { Sitata_kiritish_VALUE = 0; continue; }
                if (Sitata_kiritish_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Sitata_kiritish_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Sitata_kiritish_VALUE != 0) { 단말.Yozish("Buyruq tahlil_qilmoq_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            uzunlik_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int holat_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int belgi_kodi=Word_SMS.charAt(순번);
            if (belgi_kodi>=0xd800 && belgi_kodi<=0xdbff && 순번+1<Word_SMS.length()) belgi_kodi=0x10000+((belgi_kodi-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bayt_COUNT=belgi_kodi<128?1:belgi_kodi<2048?2:belgi_kodi<65536?3:4;
            for (int SEQUENCE_VALUE=bayt_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=bayt_COUNT==1?belgi_kodi:SEQUENCE_VALUE==bayt_COUNT-1?(bayt_COUNT==2?0xc0:bayt_COUNT==3?0xe0:0xf0)|(belgi_kodi>>(6*SEQUENCE_VALUE)):0x80|((belgi_kodi>>(6*SEQUENCE_VALUE))&63);
                if (holat_INDEX>=uzunlik_VALUE[INDEX] || token_VALUE[시작점[INDEX]+holat_INDEX++]!=VALUE) return false;
            }
        }
        return holat_INDEX==uzunlik_VALUE[INDEX];
    }
    static int yo_l(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int o_lchov = Xotira_Fayllar.yo_l_Start(uzunlik_VALUE[INDEX]); if (o_lchov < 0) return o_lchov;
        for (int Loop_INDEX = 0; Loop_INDEX < uzunlik_VALUE[INDEX]; Loop_INDEX++) {
            o_lchov = Xotira_Fayllar.yo_l_bayt(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (o_lchov < 0) return o_lchov;
        }
        return 0;
    }
    static void Xato(int INDEX) { o_lchov = 1; 단말.Yozish("Xato "); 단말.수(INDEX); 단말.문자(10); }
    static void ko_rinish_VALUE() {
        if (token_COUNT != 2) { 단말.Yozish("사용법: cat Fayl\n"); return; }
        int o_lchov = yo_l(1); if (o_lchov < 0) { Xato(o_lchov); return; }
        int Fayl = Xotira_Fayllar.Ochish(0); if (Fayl < 0) { Xato(Fayl); return; }
        while (true) { int VALUE = Xotira_Fayllar.Oʻqish(Fayl); if (VALUE == 256) break; if (VALUE < 0) { Xato(VALUE); break; } 원바이트(VALUE); }
        Xotira_Fayllar.Yopish(Fayl); 단말.문자(10);
    }
    static void tahrirlamoq_VALUE() {
        if (token_COUNT != 2) { 단말.Yozish("사용법: edit Fayl\n"); return; }
        int o_lchov = yo_l(1); if (o_lchov < 0) { Xato(o_lchov); return; }
        tahrirlamoq_nom_uzunlik = uzunlik_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < tahrirlamoq_nom_uzunlik; Loop_INDEX++) tahrirlamoq_nom[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Yozish("EDIT: Fayl 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Hajmi = 0;
        while (true) {
            단말.Yozish("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Yozish("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && satr[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Hajmi) { 단말.Yozish("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) 편집내용[Hajmi++] = satr[Loop_INDEX];
            편집내용[Hajmi++] = 10;
        }
        Xotira_Fayllar.yo_l_Start(tahrirlamoq_nom_uzunlik);
        for (int Loop_INDEX = 0; Loop_INDEX < tahrirlamoq_nom_uzunlik; Loop_INDEX++) Xotira_Fayllar.yo_l_bayt(Loop_INDEX, tahrirlamoq_nom[Loop_INDEX]);
        int Fayl = Xotira_Fayllar.Ochish(577); if (Fayl < 0) { Xato(Fayl); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Hajmi; Loop_INDEX++) Xotira_Fayllar.Yozish(Fayl, 편집내용[Loop_INDEX]);
        Xotira_Fayllar.Yopish(Fayl); 단말.Yozish("SAVED "); 단말.수(Hajmi); 단말.Yozish("bayt_VALUE(주기억 Fayl)\n");
    }
    static int o_n_oltilik_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.Yozish("사용법: load Fayl | hex Fayl\n"); return; }
        int o_lchov = yo_l(1); if (o_lchov < 0) { Xato(o_lchov); return; }
        if (!넣기) {
            int Fayl = Xotira_Fayllar.Ochish(0); if (Fayl < 0) { Xato(Fayl); return; }
            단말.Yozish("HEX BEGIN "); 단말.수(Xotira_Fayllar.Hajmi(Fayl)); 단말.문자(10);
            int kiritish_COUNT = 0;
            while (true) {
                int VALUE = Xotira_Fayllar.Oʻqish(Fayl); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++kiritish_COUNT % 32 == 0) 단말.문자(10);
            }
            if (kiritish_COUNT % 32 != 0) 단말.문자(10);
            Xotira_Fayllar.Yopish(Fayl); 단말.Yozish("HEX END\n"); return;
        }
        tahrirlamoq_nom_uzunlik = uzunlik_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < tahrirlamoq_nom_uzunlik; Loop_INDEX++) tahrirlamoq_nom[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Yozish("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Hajmi = 0;
        while (true) {
            단말.Yozish("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Yozish("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && satr[0] == '.') break;
            int old_kamera_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (satr[Loop_INDEX] == 32 || satr[Loop_INDEX] == 9) continue;
                int VALUE = o_n_oltilik_VALUE(satr[Loop_INDEX]);
                if (VALUE < 0 || Hajmi >= 편집내용.length) { 단말.Yozish("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (old_kamera_VALUE < 0) old_kamera_VALUE = VALUE; else { 편집내용[Hajmi++] = old_kamera_VALUE * 16 + VALUE; old_kamera_VALUE = -1; }
            }
            if (old_kamera_VALUE >= 0) { 단말.Yozish("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Xotira_Fayllar.yo_l_Start(tahrirlamoq_nom_uzunlik);
        for (int Loop_INDEX = 0; Loop_INDEX < tahrirlamoq_nom_uzunlik; Loop_INDEX++) Xotira_Fayllar.yo_l_bayt(Loop_INDEX, tahrirlamoq_nom[Loop_INDEX]);
        int Fayl = Xotira_Fayllar.Ochish(577); if (Fayl < 0) { Xato(Fayl); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Hajmi; Loop_INDEX++) Xotira_Fayllar.Yozish(Fayl, 편집내용[Loop_INDEX]);
        Xotira_Fayllar.Yopish(Fayl); 단말.Yozish("LOADED "); 단말.수(Hajmi); 단말.Yozish("bayt_VALUE(주기억 Fayl)\n");
    }
    static int Vositalar(int INDEX) {
        return vosita_kiritish(INDEX, 1);
    }
    static int vosita_kiritish(int INDEX, int Bajarish) {
        if (token_COUNT - Bajarish > 8) return -22;
        yozuv_taxtasi.인수준비(token_COUNT - Bajarish);
        for (int 첫값 = Bajarish; 첫값 < token_COUNT; 첫값++) {
            if (uzunlik_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < uzunlik_VALUE[첫값]; Loop_INDEX++) yozuv_taxtasi.dalil_bayt(첫값 - Bajarish, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? yozuv_taxtasi.리눅스파일실행() : INDEX < 0 ? yozuv_taxtasi.bajarmoq_foydalanuvchi_fayl() : yozuv_taxtasi.ishlash_foydalanuvchi_ilova(INDEX);
    }
    static int PYTHON_to_plam() {
        if (token_COUNT > 8) return -22;
        yozuv_taxtasi.인수준비(token_COUNT);
        String yo_l = "/lib/to_plam.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int holat_INDEX = 0;
        for (int 순번 = 0; 순번 < yo_l.length(); 순번++) {
            int belgi_VALUE = yo_l.charAt(순번);
            if (belgi_VALUE < 128) yozuv_taxtasi.dalil_bayt(0, holat_INDEX++, belgi_VALUE);
            else { yozuv_taxtasi.dalil_bayt(0, holat_INDEX++, 0xe0 | (belgi_VALUE >> 12)); yozuv_taxtasi.dalil_bayt(0, holat_INDEX++, 0x80 | ((belgi_VALUE >> 6) & 63)); yozuv_taxtasi.dalil_bayt(0, holat_INDEX++, 0x80 | (belgi_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (uzunlik_VALUE[순번] > 255) return -36;
            for (int belgi_VALUE = 0; belgi_VALUE < uzunlik_VALUE[순번]; belgi_VALUE++) yozuv_taxtasi.dalil_bayt(순번, belgi_VALUE, token_VALUE[시작점[순번] + belgi_VALUE]);
        }
        return yozuv_taxtasi.ishlash_foydalanuvchi_ilova(12);
    }
    static int 실행형식() {
        int 처리값 = yo_l(0); if (처리값 < 0) return 처리값;
        int Fayl = Xotira_Fayllar.Ochish(0); if (Fayl < 0) return Fayl;
        int 첫값 = Xotira_Fayllar.Oʻqish(Fayl), bayt_ma_lumotlar = Xotira_Fayllar.Oʻqish(Fayl), belgi_kodi = Xotira_Fayllar.Oʻqish(Fayl), 뒷값 = Xotira_Fayllar.Oʻqish(Fayl);
        Xotira_Fayllar.Yopish(Fayl);
        if (첫값 == 127 && bayt_ma_lumotlar == 'E' && belgi_kodi == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bayt_ma_lumotlar == 'K' && belgi_kodi == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        yozuv_taxtasi.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) yozuv_taxtasi.dalil_bayt(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return yozuv_taxtasi.ishlash_foydalanuvchi_ilova(INDEX);
    }
    static void SMS_bayt(int Fayl, int VALUE) { Xotira_Fayllar.Yozish(Fayl, VALUE); }
    static void statik_fayl(String Nomi, String tarkib_VALUE) {
        // to_plam 파일명은 ASCII. Fayl 내용은 UTF-8로 저장한다.
        Xotira_Fayllar.yo_l_Start(Nomi.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Nomi.length(); Loop_INDEX++) Xotira_Fayllar.yo_l_bayt(Loop_INDEX, Nomi.charAt(Loop_INDEX));
        int Fayl = Xotira_Fayllar.Ochish(193); if (Fayl < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < tarkib_VALUE.length(); Loop_INDEX++) {
            int belgi_kodi = tarkib_VALUE.charAt(Loop_INDEX);
            if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdbff && Loop_INDEX + 1 < tarkib_VALUE.length()) belgi_kodi = 0x10000 + ((belgi_kodi - 0xd800) << 10) + tarkib_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (belgi_kodi < 128) SMS_bayt(Fayl, belgi_kodi);
            else {
                int 수 = belgi_kodi < 2048 ? 2 : belgi_kodi < 65536 ? 3 : 4;
                SMS_bayt(Fayl, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (belgi_kodi >> (6 * (수 - 1))));
                for (int kiritish_COUNT = 수 - 1; kiritish_COUNT > 0; kiritish_COUNT--) SMS_bayt(Fayl, 0x80 | ((belgi_kodi >> (6 * (kiritish_COUNT - 1))) & 63));
            }
        }
        Xotira_Fayllar.Yopish(Fayl);
    }
    static void 한글도움말() {
        단말.Yozish("F9 / Shift+Space: [EN] ↔ [Uzbek]\n");
        단말.Yozish("  [UZ_LATN] keyboard; [EN] ASCII\n");
        단말.Yozish("  ' → ʻ\n");
        단말.Yozish("  F9: EN ↔ Uzbek | Ctrl+Shift+V: UTF-8\n");
        단말.Yozish("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Yozish("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nomi) {
        int bayt_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nomi.length(); Loop_INDEX++) { int belgi_kodi = Nomi.charAt(Loop_INDEX); if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdfff) return -22; bayt_COUNT += belgi_kodi < 128 ? 1 : belgi_kodi < 2048 ? 2 : 3; }
        int 처리값 = Xotira_Fayllar.yo_l_Start(bayt_COUNT); if (처리값 < 0) return 처리값;
        int holat_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nomi.length(); Loop_INDEX++) {
            int belgi_kodi = Nomi.charAt(Loop_INDEX);
            if (belgi_kodi < 128) Xotira_Fayllar.yo_l_bayt(holat_INDEX++, belgi_kodi);
            else if (belgi_kodi < 2048) { Xotira_Fayllar.yo_l_bayt(holat_INDEX++, 0xc0 | (belgi_kodi >> 6)); Xotira_Fayllar.yo_l_bayt(holat_INDEX++, 0x80 | (belgi_kodi & 63)); }
            else { Xotira_Fayllar.yo_l_bayt(holat_INDEX++, 0xe0 | (belgi_kodi >> 12)); Xotira_Fayllar.yo_l_bayt(holat_INDEX++, 0x80 | ((belgi_kodi >> 6) & 63)); Xotira_Fayllar.yo_l_bayt(holat_INDEX++, 0x80 | (belgi_kodi & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nomi) {
        int 처리값 = 예제경로(Nomi); if (처리값 < 0) return 처리값;
        처리값 = Xotira_Fayllar.Yaratish_katalog(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nomi, String ma_lumotlar) {
        int 처리값 = 예제경로(Nomi); if (처리값 < 0) return 처리값;
        int Fayl = Xotira_Fayllar.Ochish(193); if (Fayl == -17) return 0; if (Fayl < 0) return Fayl;
        for (int Loop_INDEX = 0; Loop_INDEX < ma_lumotlar.length(); Loop_INDEX += 2) {
            처리값 = Xotira_Fayllar.Yozish(Fayl, o_n_oltilik_VALUE(ma_lumotlar.charAt(Loop_INDEX)) * 16 + o_n_oltilik_VALUE(ma_lumotlar.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Xotira_Fayllar.Yopish(Fayl); return 처리값; }
        }
        return Xotira_Fayllar.Yopish(Fayl);
    }
    static void ko_rsatmoq_yordam() {
        tizim_vosita.ko_rsatmoq_yordam();
        단말.Yozish("sshd / xavfsiz_qobiq start|stop|status: SSH :22 (user, 장치별 parol_VALUE)\n");
        단말.Yozish("vncd / masofaviy_ekran start|stop|status: VNC :5900 (장치별 parol_VALUE)\n");
        단말.Yozish("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Yozish("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Yozish("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Yozish("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Yozish("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Yozish("모서리 + 왼쪽 버튼 tortib_o_tkazmoq_VALUE: Terminal Hajmi o_zgartirmoq_VALUE; terminal size: ustun_VALUE/ROW_VALUE\n");
        단말.Yozish("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Yozish("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Yozish("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Yozish("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Yozish("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Yozish("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Yozish("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Yozish("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Yozish("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Yozish("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Yozish("pip: MicroPython manba_daraxt o_rnatish_VALUE; tashkilotchi --network --pip 필요; /lib는 RAM\n");
        단말.Yozish("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Yozish("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Yozish("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Yozish("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && yozuv_taxtasi.Terminal(2) != 0) { yozuv_taxtasi.Terminal(0); 단말.Yozish("TERMINAL CLOSED\n"); }
        else if (yozuv_taxtasi.Terminal(1) < 0) Xato(-19);
        else 단말.Yozish("TERMINAL READY — Uzbek terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Buyruq() {
        if (token_COUNT == 0) return;
        if (tizim_vosita.bajarmoq_buyruq()) return;
        if (같음(0,"sshd") || 같음(0,"xavfsiz_qobiq") || 같음(0,"vncd") || 같음(0,"masofaviy_ekran")) {
            int 종류=같음(0,"vncd")||같음(0,"masofaviy_ekran")?1:0;
            int Amal=같음(1,"start")||같음(1,"Bajarish")?1:같음(1,"stop")||같음(1,"Toʻxtatish")?0:2;
            int holat_VALUE_e10195a1=yozuv_taxtasi.soyalashtirish(종류,Amal);
            if(holat_VALUE_e10195a1<0)Xato(holat_VALUE_e10195a1);else 단말.Yozish(yozuv_taxtasi.soyalashtirish(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else ko_rsatmoq_yordam(); }
        else if (같음(0, "info") || 같음(0, "i")) o_zak.msinfo32_exe();
        else if (같음(0, "pwd")) { Xotira_Fayllar.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Xotira_Fayllar.yo_l_Start(1); 처리값 = Xotira_Fayllar.yo_l_bayt(0, '/'); } else 처리값 = token_COUNT == 2 ? yo_l(1) : -22;
            if (처리값 >= 0) 처리값 = Xotira_Fayllar.o_zgartirmoq_katalog(); if (처리값 < 0) Xato(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int dalil_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == dalil_INDEX) { Xotira_Fayllar.yo_l_Start(1); 처리값 = Xotira_Fayllar.yo_l_bayt(0, '.'); } else 처리값 = token_COUNT == dalil_INDEX + 1 ? yo_l(dalil_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Xotira_Fayllar.경로목록(); if (처리값 < 0) Xato(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) qobiq_Vositalar.fayl_ish(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) qobiq_Vositalar.namuna_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) qobiq_Vositalar.ko_rinish_VALUE();
        else if (같음(0, "wc")) qobiq_Vositalar.세기();
        else if (같음(0, "grep")) qobiq_Vositalar.FIND_kiritish();
        else if (같음(0, "head") || 같음(0, "tail")) qobiq_Vositalar.머리(같음(0, "tail"));
        else if (같음(0, "tee")) qobiq_Vositalar.함께쓰기();
        else if (같음(0, "env")) qobiq_sintaksis.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) qobiq_sintaksis.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = qobiq_sintaksis.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { o_lchov = 처리값; 단말.Yozish("Buyruq tahlil_qilmoq_VALUE: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) qobiq_sintaksis.bajarmoq_fayl();
        else if (같음(0, "true")) o_lchov = 0;
        else if (같음(0, "false")) o_lchov = 1;
        else if (같음(0, "history")) satr_Muharrir.ko_rsatmoq_LOG();
        else if (같음(0, "exit")) {
            if (qobiq_sintaksis.깊이 > 0) { o_lchov = token_COUNT == 1 ? qobiq_sintaksis.holat_VALUE_e10195a1 : qobiq_Vositalar.raqam_VALUE(1); if (o_lchov < 0 || o_lchov > 255) o_lchov = 2; qobiq_sintaksis.ssenariy_to_xtatmoq = true; }
            else if (yozuv_taxtasi.Terminal(2) != 0) Terminal(true);
            else 단말.Yozish("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) tahrirlamoq_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { o_lchov = 2; 단말.Yozish("사용법: rm Fayl...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = yo_l(Loop_INDEX); if (처리값 == 0) 처리값 = Xotira_Fayllar.tozalash_kiritish(); if (처리값 < 0) Xato(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_holat = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_holat; 첫값 < token_COUNT; 첫값++) { if (첫값 > Start_holat) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < uzunlik_VALUE[첫값]; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Start_holat == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Yozish("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_to_plam() : Vositalar(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); o_lchov = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !qobiq_sintaksis.연결중) { 단말.Yozish("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Vositalar(13); o_lchov = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Vositalar(15); o_lchov = 처리값 < 0 ? 126 : 처리값; if (!qobiq_sintaksis.연결중) { 단말.Yozish("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Vositalar(16); o_lchov = 처리값 < 0 ? 126 : 처리값; if (!qobiq_sintaksis.연결중) { 단말.Yozish("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Hajmi = yozuv_taxtasi.Terminal(13); 단말.Yozish("TERMINAL SIZE "); 단말.수(Hajmi & 65535); 단말.문자('x'); 단말.수(Hajmi >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { yozuv_taxtasi.Terminal(9); ishchi_stol.bajarmoq_buyruq(); }
        else if (같음(0, "c")) o_zak.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) o_zak.작업시험();
        else if (같음(0, "g")) o_zak.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) o_zak.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = yozuv_taxtasi.ishlash_foydalanuvchi_ilova(0); if (처리값 == 0) 단말.Yozish("ELF DEMO PASS\n"); else Xato(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? vosita_kiritish(-2, 2) : Vositalar(-1); o_lchov = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !qobiq_sintaksis.연결중) { 단말.Yozish("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) o_zak.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = yozuv_taxtasi.fayl_uzatish_xizmat(1); if (처리값 < 0) Xato(처리값); else { 단말.Yozish("FTP listening "); tizim_vosita.yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(0,0)); 단말.Yozish(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { yozuv_taxtasi.fayl_uzatish_xizmat(0); 단말.Yozish("FTP stopped\n"); }
            else 단말.Yozish(yozuv_taxtasi.fayl_uzatish_xizmat(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { to_plam.Tayyorlamoq(); 단말.Yozish("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Til = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Til < 0) 단말.Yozish("example java|c|python: 출력, Fayl, 네트워크, 그래픽, Java Swing oyna 예제\n");
            else { int 처리값 = 예제꾸러미.o_rnatish_VALUE(Til); if (처리값 < 0) { Xato(처리값); if (처리값 == -28) 단말.Yozish("RAM full: remove unused files, then retry example\n"); } else 단말.Yozish("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = vosita_kiritish(format_VALUE == 1 ? -1 : 14, 0); o_lchov = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !qobiq_sintaksis.연결중) { 단말.Yozish("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { o_lchov = 126; 단말.Yozish("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { o_lchov = 127; 단말.Yozish("Unknown command. help: commands\n"); }
        }
    }
    public static void bajarmoq_buyruq() {
        to_plam.Tayyorlamoq();
        for (int Til = 0; Til < 3; Til++) { int 처리값 = 예제꾸러미.o_rnatish_VALUE(Til); if (처리값 < 0) Xato(처리값); }
        ko_rsatmoq_yordam();
        while (true) {
            oyna_seans.Jarayon_VALUE_kiritish(); if (oyna_seans.재개()) continue;
            if (!oyna_seans.이어읽기) 단말.Yozish("jkoros-native> "); satr_Muharrir.buyruq_satri = true; yozuv_taxtasi.masofaviy_bir_daqiqa(1); int Hajmi = 줄읽기(); yozuv_taxtasi.masofaviy_bir_daqiqa(0); satr_Muharrir.buyruq_satri = false;
            if (Hajmi == -3) continue;
            if (Hajmi == -2) 단말.Yozish("Buyruq tahlil_qilmoq_VALUE: 명령줄이 너무 깁니다\n");
            if (Hajmi >= 0) { qobiq_sintaksis.ssenariy_to_xtatmoq = false; qobiq_sintaksis.bajarmoq_buyruq(satr, 0, Hajmi, 0); } else qobiq_sintaksis.holat_VALUE_e10195a1 = 130;
            yozuv_taxtasi.to_xtatmoq_masofaviy_buyruq(qobiq_sintaksis.holat_VALUE_e10195a1);
            satr_Muharrir.Hajmi = satr_Muharrir.kursor_VALUE = satr_Muharrir.Start_oyna = 0;
        }
    }
}
