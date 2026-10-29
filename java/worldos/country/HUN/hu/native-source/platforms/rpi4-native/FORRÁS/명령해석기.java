// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 parancssor. Idézet, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Vonal = new int[4096], kód_ÉRTÉK = new int[4096], 시작점 = new int[32], hossz_ÉRTÉK = new int[32];
    static int[] Szerkesztett_Tartalom = new int[16384], szerkeszt_név = new int[63];
    static int kód_DARAB, szerkeszt_név_hossz, KR;
    static boolean Előző_sor;
    static void 원바이트(int ÉRTÉK) { fal.직렬쓰기(ÉRTÉK); }
    static int 줄읽기() { return sorszerkesztő.Olvasás(); }
    static boolean 나누기(int Méret) {
        int Pozíció = 0, 끝 = 0; kód_DARAB = 0;
        while (Pozíció < Méret) {
            while (Pozíció < Méret && (Vonal[Pozíció] == 32 || Vonal[Pozíció] == 9)) Pozíció++;
            if (Pozíció == Méret) break;
            if (kód_DARAB == 16) { 단말.Írás("Parancs elemez_ÉRTÉK: 인수가 너무 많습니다\n"); return false; }
            시작점[kód_DARAB] = 끝; int Idézet_ÉRTÉK = 0;
            while (Pozíció < Méret) {
                int ÉRTÉK = Vonal[Pozíció++];
                if (Idézet_ÉRTÉK == 0 && (ÉRTÉK == 32 || ÉRTÉK == 9)) break;
                if (ÉRTÉK == Idézet_ÉRTÉK) { Idézet_ÉRTÉK = 0; continue; }
                if (Idézet_ÉRTÉK == 0 && (ÉRTÉK == 39 || ÉRTÉK == 34)) { Idézet_ÉRTÉK = ÉRTÉK; continue; }
                kód_ÉRTÉK[끝++] = ÉRTÉK;
            }
            if (Idézet_ÉRTÉK != 0) { 단말.Írás("Parancs elemez_ÉRTÉK: 따옴표가 닫히지 않았습니다\n"); return false; }
            hossz_ÉRTÉK[kód_DARAB] = 끝 - 시작점[kód_DARAB]; kód_DARAB++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String szó_SMS) {
        if (INDEX >= kód_DARAB) return false;
        int helyzetindex=0;
        for (int 순번=0; 순번<szó_SMS.length(); 순번++) {
            int kódpont=szó_SMS.charAt(순번);
            if (kódpont>=0xd800 && kódpont<=0xdbff && 순번+1<szó_SMS.length()) kódpont=0x10000+((kódpont-0xd800)<<10)+szó_SMS.charAt(++순번)-0xdc00;
            int bájt_DARAB=kódpont<128?1:kódpont<2048?2:kódpont<65536?3:4;
            for (int szekvencia_ÉRTÉK=bájt_DARAB-1; szekvencia_ÉRTÉK>=0; szekvencia_ÉRTÉK--) {
                int ÉRTÉK=bájt_DARAB==1?kódpont:szekvencia_ÉRTÉK==bájt_DARAB-1?(bájt_DARAB==2?0xc0:bájt_DARAB==3?0xe0:0xf0)|(kódpont>>(6*szekvencia_ÉRTÉK)):0x80|((kódpont>>(6*szekvencia_ÉRTÉK))&63);
                if (helyzetindex>=hossz_ÉRTÉK[INDEX] || kód_ÉRTÉK[시작점[INDEX]+helyzetindex++]!=ÉRTÉK) return false;
            }
        }
        return helyzetindex==hossz_ÉRTÉK[INDEX];
    }
    static int ÚTVONAL(int INDEX) {
        if (INDEX >= kód_DARAB) return -22;
        int KR = Memória_Files.útvonal_START(hossz_ÉRTÉK[INDEX]); if (KR < 0) return KR;
        for (int Loop_INDEX = 0; Loop_INDEX < hossz_ÉRTÉK[INDEX]; Loop_INDEX++) {
            KR = Memória_Files.útvonal_bájt(Loop_INDEX, kód_ÉRTÉK[시작점[INDEX] + Loop_INDEX]); if (KR < 0) return KR;
        }
        return 0;
    }
    static void HIBA(int INDEX) { KR = 1; 단말.Írás("HIBA "); 단말.szám(INDEX); 단말.문자(10); }
    static void Nézet_ÉRTÉK() {
        if (kód_DARAB != 2) { 단말.Írás("사용법: cat Fájl\n"); return; }
        int KR = ÚTVONAL(1); if (KR < 0) { HIBA(KR); return; }
        int Fájl = Memória_Files.Megnyitás(0); if (Fájl < 0) { HIBA(Fájl); return; }
        while (true) { int ÉRTÉK = Memória_Files.Olvasás(Fájl); if (ÉRTÉK == 256) break; if (ÉRTÉK < 0) { HIBA(ÉRTÉK); break; } 원바이트(ÉRTÉK); }
        Memória_Files.Bezárás(Fájl); 단말.문자(10);
    }
    static void szerkeszt_ÉRTÉK() {
        if (kód_DARAB != 2) { 단말.Írás("사용법: edit Fájl\n"); return; }
        int KR = ÚTVONAL(1); if (KR < 0) { HIBA(KR); return; }
        szerkeszt_név_hossz = hossz_ÉRTÉK[1];
        for (int Loop_INDEX = 0; Loop_INDEX < szerkeszt_név_hossz; Loop_INDEX++) szerkeszt_név[Loop_INDEX] = kód_ÉRTÉK[시작점[1] + Loop_INDEX];
        단말.Írás("EDIT: Fájl 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Méret = 0;
        while (true) {
            단말.Írás("edit> "); int bevitel_ÉRTÉK = 줄읽기();
            if (bevitel_ÉRTÉK < 0) { 단말.Írás("EDIT CANCELLED\n"); return; }
            if (bevitel_ÉRTÉK == 1 && Vonal[0] == '.') break;
            if (bevitel_ÉRTÉK + 1 > Szerkesztett_Tartalom.length - Méret) { 단말.Írás("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < bevitel_ÉRTÉK; Loop_INDEX++) Szerkesztett_Tartalom[Méret++] = Vonal[Loop_INDEX];
            Szerkesztett_Tartalom[Méret++] = 10;
        }
        Memória_Files.útvonal_START(szerkeszt_név_hossz);
        for (int Loop_INDEX = 0; Loop_INDEX < szerkeszt_név_hossz; Loop_INDEX++) Memória_Files.útvonal_bájt(Loop_INDEX, szerkeszt_név[Loop_INDEX]);
        int Fájl = Memória_Files.Megnyitás(577); if (Fájl < 0) { HIBA(Fájl); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Méret; Loop_INDEX++) Memória_Files.Írás(Fájl, Szerkesztett_Tartalom[Loop_INDEX]);
        Memória_Files.Bezárás(Fájl); 단말.Írás("SAVED "); 단말.szám(Méret); 단말.Írás("bájt_ÉRTÉK(주기억 Fájl)\n");
    }
    static int hexadecimális_ÉRTÉK(int ÉRTÉK) {
        if (ÉRTÉK >= '0' && ÉRTÉK <= '9') return ÉRTÉK - '0';
        if (ÉRTÉK >= 'a' && ÉRTÉK <= 'f') return ÉRTÉK - 'a' + 10;
        if (ÉRTÉK >= 'A' && ÉRTÉK <= 'F') return ÉRTÉK - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (kód_DARAB != 2) { 단말.Írás("사용법: load Fájl | hex Fájl\n"); return; }
        int KR = ÚTVONAL(1); if (KR < 0) { HIBA(KR); return; }
        if (!넣기) {
            int Fájl = Memória_Files.Megnyitás(0); if (Fájl < 0) { HIBA(Fájl); return; }
            단말.Írás("HEX BEGIN "); 단말.szám(Memória_Files.Méret(Fájl)); 단말.문자(10);
            int bejegyzés_DARAB = 0;
            while (true) {
                int ÉRTÉK = Memória_Files.Olvasás(Fájl); if (ÉRTÉK < 0 || ÉRTÉK == 256) break;
                단말.문자("0123456789abcdef".charAt(ÉRTÉK >> 4)); 단말.문자("0123456789abcdef".charAt(ÉRTÉK & 15));
                if (++bejegyzés_DARAB % 32 == 0) 단말.문자(10);
            }
            if (bejegyzés_DARAB % 32 != 0) 단말.문자(10);
            Memória_Files.Bezárás(Fájl); 단말.Írás("HEX END\n"); return;
        }
        szerkeszt_név_hossz = hossz_ÉRTÉK[1];
        for (int Loop_INDEX = 0; Loop_INDEX < szerkeszt_név_hossz; Loop_INDEX++) szerkeszt_név[Loop_INDEX] = kód_ÉRTÉK[시작점[1] + Loop_INDEX];
        단말.Írás("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Méret = 0;
        while (true) {
            단말.Írás("hex> "); int bevitel_ÉRTÉK = 줄읽기();
            if (bevitel_ÉRTÉK < 0) { 단말.Írás("LOAD CANCELLED\n"); return; }
            if (bevitel_ÉRTÉK == 1 && Vonal[0] == '.') break;
            int elülső_kamera_ÉRTÉK = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < bevitel_ÉRTÉK; Loop_INDEX++) {
                if (Vonal[Loop_INDEX] == 32 || Vonal[Loop_INDEX] == 9) continue;
                int ÉRTÉK = hexadecimális_ÉRTÉK(Vonal[Loop_INDEX]);
                if (ÉRTÉK < 0 || Méret >= Szerkesztett_Tartalom.length) { 단말.Írás("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (elülső_kamera_ÉRTÉK < 0) elülső_kamera_ÉRTÉK = ÉRTÉK; else { Szerkesztett_Tartalom[Méret++] = elülső_kamera_ÉRTÉK * 16 + ÉRTÉK; elülső_kamera_ÉRTÉK = -1; }
            }
            if (elülső_kamera_ÉRTÉK >= 0) { 단말.Írás("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memória_Files.útvonal_START(szerkeszt_név_hossz);
        for (int Loop_INDEX = 0; Loop_INDEX < szerkeszt_név_hossz; Loop_INDEX++) Memória_Files.útvonal_bájt(Loop_INDEX, szerkeszt_név[Loop_INDEX]);
        int Fájl = Memória_Files.Megnyitás(577); if (Fájl < 0) { HIBA(Fájl); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Méret; Loop_INDEX++) Memória_Files.Írás(Fájl, Szerkesztett_Tartalom[Loop_INDEX]);
        Memória_Files.Bezárás(Fájl); 단말.Írás("LOADED "); 단말.szám(Méret); 단말.Írás("bájt_ÉRTÉK(주기억 Fájl)\n");
    }
    static int Eszközök(int INDEX) {
        return eszköz_bejegyzés(INDEX, 1);
    }
    static int eszköz_bejegyzés(int INDEX, int Futtatás) {
        if (kód_DARAB - Futtatás > 8) return -22;
        fal.인수준비(kód_DARAB - Futtatás);
        for (int 첫값 = Futtatás; 첫값 < kód_DARAB; 첫값++) {
            if (hossz_ÉRTÉK[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < hossz_ÉRTÉK[첫값]; Loop_INDEX++) fal.argumentum_bájt(첫값 - Futtatás, Loop_INDEX, kód_ÉRTÉK[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? fal.리눅스파일실행() : INDEX < 0 ? fal.végrehajt_felhasználó_Fájl() : fal.futtat_felhasználó_app(INDEX);
    }
    static int PYTHON_köteg() {
        if (kód_DARAB > 8) return -22;
        fal.인수준비(kód_DARAB);
        String ÚTVONAL = "/lib/köteg.py";
        // Java 문자열을 셸의 UTF-8 Argumentumok 버퍼에 기록한다.
        int helyzetindex = 0;
        for (int 순번 = 0; 순번 < ÚTVONAL.length(); 순번++) {
            int karakter_ÉRTÉK = ÚTVONAL.charAt(순번);
            if (karakter_ÉRTÉK < 128) fal.argumentum_bájt(0, helyzetindex++, karakter_ÉRTÉK);
            else { fal.argumentum_bájt(0, helyzetindex++, 0xe0 | (karakter_ÉRTÉK >> 12)); fal.argumentum_bájt(0, helyzetindex++, 0x80 | ((karakter_ÉRTÉK >> 6) & 63)); fal.argumentum_bájt(0, helyzetindex++, 0x80 | (karakter_ÉRTÉK & 63)); }
        }
        for (int 순번 = 1; 순번 < kód_DARAB; 순번++) {
            if (hossz_ÉRTÉK[순번] > 255) return -36;
            for (int karakter_ÉRTÉK = 0; karakter_ÉRTÉK < hossz_ÉRTÉK[순번]; karakter_ÉRTÉK++) fal.argumentum_bájt(순번, karakter_ÉRTÉK, kód_ÉRTÉK[시작점[순번] + karakter_ÉRTÉK]);
        }
        return fal.futtat_felhasználó_app(12);
    }
    static int végrehajtás_formáz() {
        int 처리값 = ÚTVONAL(0); if (처리값 < 0) return 처리값;
        int Fájl = Memória_Files.Megnyitás(0); if (Fájl < 0) return Fájl;
        int 첫값 = Memória_Files.Olvasás(Fájl), bájt_adat = Memória_Files.Olvasás(Fájl), kódpont = Memória_Files.Olvasás(Fájl), 뒷값 = Memória_Files.Olvasás(Fájl);
        Memória_Files.Bezárás(Fájl);
        if (첫값 == 127 && bájt_adat == 'E' && kódpont == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bájt_adat == 'K' && kódpont == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumentumok) {
        fal.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumentumok.length(); Loop_INDEX++) fal.argumentum_bájt(0, Loop_INDEX, Argumentumok.charAt(Loop_INDEX));
        return fal.futtat_felhasználó_app(INDEX);
    }
    static void SMS_bájt(int Fájl, int ÉRTÉK) { Memória_Files.Írás(Fájl, ÉRTÉK); }
    static void statikus_Fájl(String Név, String Tartalom_ÉRTÉK) {
        // köteg 파일명은 ASCII. Fájl 내용은 UTF-8로 저장한다.
        Memória_Files.útvonal_START(Név.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Név.length(); Loop_INDEX++) Memória_Files.útvonal_bájt(Loop_INDEX, Név.charAt(Loop_INDEX));
        int Fájl = Memória_Files.Megnyitás(193); if (Fájl < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Tartalom_ÉRTÉK.length(); Loop_INDEX++) {
            int kódpont = Tartalom_ÉRTÉK.charAt(Loop_INDEX);
            if (kódpont >= 0xd800 && kódpont <= 0xdbff && Loop_INDEX + 1 < Tartalom_ÉRTÉK.length()) kódpont = 0x10000 + ((kódpont - 0xd800) << 10) + Tartalom_ÉRTÉK.charAt(++Loop_INDEX) - 0xdc00;
            if (kódpont < 128) SMS_bájt(Fájl, kódpont);
            else {
                int szám = kódpont < 2048 ? 2 : kódpont < 65536 ? 3 : 4;
                SMS_bájt(Fájl, (szám == 2 ? 0xc0 : szám == 3 ? 0xe0 : 0xf0) | (kódpont >> (6 * (szám - 1))));
                for (int bejegyzés_DARAB = szám - 1; bejegyzés_DARAB > 0; bejegyzés_DARAB--) SMS_bájt(Fájl, 0x80 | ((kódpont >> (6 * (bejegyzés_DARAB - 1))) & 63));
            }
        }
        Memória_Files.Bezárás(Fájl);
    }
    static void 한글도움말() {
        단말.Írás("Az F9 vagy a Shift+Space magyar bevitelre vált.\n");
        단말.Írás("  [HU] keyboard; [EN] ASCII\n");
        단말.Írás("  _ → Ü\n");
        단말.Írás("  F9: EN ↔ hu | Ctrl+Shift+V: UTF-8\n");
        단말.Írás("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Írás("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Név) {
        int bájt_DARAB = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Név.length(); Loop_INDEX++) { int kódpont = Név.charAt(Loop_INDEX); if (kódpont >= 0xd800 && kódpont <= 0xdfff) return -22; bájt_DARAB += kódpont < 128 ? 1 : kódpont < 2048 ? 2 : 3; }
        int 처리값 = Memória_Files.útvonal_START(bájt_DARAB); if (처리값 < 0) return 처리값;
        int helyzetindex = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Név.length(); Loop_INDEX++) {
            int kódpont = Név.charAt(Loop_INDEX);
            if (kódpont < 128) Memória_Files.útvonal_bájt(helyzetindex++, kódpont);
            else if (kódpont < 2048) { Memória_Files.útvonal_bájt(helyzetindex++, 0xc0 | (kódpont >> 6)); Memória_Files.útvonal_bájt(helyzetindex++, 0x80 | (kódpont & 63)); }
            else { Memória_Files.útvonal_bájt(helyzetindex++, 0xe0 | (kódpont >> 12)); Memória_Files.útvonal_bájt(helyzetindex++, 0x80 | ((kódpont >> 6) & 63)); Memória_Files.útvonal_bájt(helyzetindex++, 0x80 | (kódpont & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Név) {
        int 처리값 = 예제경로(Név); if (처리값 < 0) return 처리값;
        처리값 = Memória_Files.készít_címtár(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Név, String adat) {
        int 처리값 = 예제경로(Név); if (처리값 < 0) return 처리값;
        int Fájl = Memória_Files.Megnyitás(193); if (Fájl == -17) return 0; if (Fájl < 0) return Fájl;
        for (int Loop_INDEX = 0; Loop_INDEX < adat.length(); Loop_INDEX += 2) {
            처리값 = Memória_Files.Írás(Fájl, hexadecimális_ÉRTÉK(adat.charAt(Loop_INDEX)) * 16 + hexadecimális_ÉRTÉK(adat.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memória_Files.Bezárás(Fájl); return 처리값; }
        }
        return Memória_Files.Bezárás(Fájl);
    }
    static void bemutató_súgó() {
        Rendszer_eszköz.bemutató_súgó();
        단말.Írás("sshd / biztonságos_felület start|stop|status: SSH :22 (user, 장치별 jelszó_ÉRTÉK)\n");
        단말.Írás("vncd / távoli_kijelző start|stop|status: VNC :5900 (장치별 jelszó_ÉRTÉK)\n");
        단말.Írás("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Írás("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Írás("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Írás("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Írás("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Írás("모서리 + 왼쪽 버튼 húz_ÉRTÉK: Terminál Méret módosítás_ÉRTÉK; terminal size: OSZLOP_ÉRTÉK/SOR_ÉRTÉK\n");
        단말.Írás("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Írás("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Írás("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Írás("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Írás("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Írás("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Írás("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Írás("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Írás("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Írás("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Írás("pip: MicroPython forrás_fa telepít_ÉRTÉK; gazda --network --pip 필요; /lib는 RAM\n");
        단말.Írás("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Írás("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Írás("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Írás("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminál(boolean 전환여부) {
        if (전환여부 && fal.Terminál(2) != 0) { fal.Terminál(0); 단말.Írás("TERMINAL CLOSED\n"); }
        else if (fal.Terminál(1) < 0) HIBA(-19);
        else 단말.Írás("TERMINAL READY — hu terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Parancs() {
        if (kód_DARAB == 0) return;
        if (Rendszer_eszköz.végrehajt_parancs()) return;
        if (같음(0,"sshd") || 같음(0,"biztonságos_felület") || 같음(0,"vncd") || 같음(0,"távoli_kijelző")) {
            int Altípus_ÉRTÉK=같음(0,"vncd")||같음(0,"távoli_kijelző")?1:0;
            int Művelet=같음(1,"start")||같음(1,"Futtatás")?1:같음(1,"stop")||같음(1,"Leállítás")?0:2;
            int Állapot_ÉRTÉK=fal.távkezelés(Altípus_ÉRTÉK,Művelet);
            if(Állapot_ÉRTÉK<0)HIBA(Állapot_ÉRTÉK);else 단말.Írás(fal.távkezelés(Altípus_ÉRTÉK,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else bemutató_súgó(); }
        else if (같음(0, "info") || 같음(0, "i")) kernel.msinfo32_exe();
        else if (같음(0, "pwd")) { Memória_Files.aktuális_ír(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (kód_DARAB == 1) { Memória_Files.útvonal_START(1); 처리값 = Memória_Files.útvonal_bájt(0, '/'); } else 처리값 = kód_DARAB == 2 ? ÚTVONAL(1) : -22;
            if (처리값 >= 0) 처리값 = Memória_Files.módosítás_címtár(); if (처리값 < 0) HIBA(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argumentum_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (kód_DARAB == argumentum_INDEX) { Memória_Files.útvonal_START(1); 처리값 = Memória_Files.útvonal_bájt(0, '.'); } else 처리값 = kód_DARAB == argumentum_INDEX + 1 ? ÚTVONAL(argumentum_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memória_Files.경로목록(); if (처리값 < 0) HIBA(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) felület_Eszközök.Fájl_eset(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) felület_Eszközök.másol_ÉRTÉK(같음(0, "mv"));
        else if (같음(0, "cat")) felület_Eszközök.Nézet_ÉRTÉK();
        else if (같음(0, "wc")) felület_Eszközök.세기();
        else if (같음(0, "grep")) felület_Eszközök.keres_bejegyzés();
        else if (같음(0, "head") || 같음(0, "tail")) felület_Eszközök.머리(같음(0, "tail"));
        else if (같음(0, "tee")) felület_Eszközök.ír_Együtt();
        else if (같음(0, "env")) felület_szintaxis.bemutató_környezet();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (kód_DARAB == 1) felület_szintaxis.bemutató_környezet();
            for (int Loop_INDEX = 1; Loop_INDEX < kód_DARAB; Loop_INDEX++) { int 처리값 = felület_szintaxis.környezet_Gépház(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { KR = 처리값; 단말.Írás("Parancs elemez_ÉRTÉK: változó_ÉRTÉK 이름이 잘못되었거나 예약된 이름이거나 környezet_5d36e09c 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) felület_szintaxis.végrehajt_Fájl();
        else if (같음(0, "true")) KR = 0;
        else if (같음(0, "false")) KR = 1;
        else if (같음(0, "history")) sorszerkesztő.bemutató_LOG();
        else if (같음(0, "exit")) {
            if (felület_szintaxis.깊이 > 0) { KR = kód_DARAB == 1 ? felület_szintaxis.Állapot_ÉRTÉK : felület_Eszközök.számjegy_ÉRTÉK(1); if (KR < 0 || KR > 255) KR = 2; felület_szintaxis.parancsfájl_megszüntet = true; }
            else if (fal.Terminál(2) != 0) Terminál(true);
            else 단말.Írás("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) szerkeszt_ÉRTÉK();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (kód_DARAB < 2) { KR = 2; 단말.Írás("사용법: rm Fájl...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < kód_DARAB; Loop_INDEX++) { int 처리값 = ÚTVONAL(Loop_INDEX); if (처리값 == 0) 처리값 = Memória_Files.töröl_bejegyzés(); if (처리값 < 0) HIBA(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_pozíció = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_pozíció; 첫값 < kód_DARAB; 첫값++) { if (첫값 > START_pozíció) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < hossz_ÉRTÉK[첫값]; Loop_INDEX++) fal.직렬쓰기(kód_ÉRTÉK[시작점[첫값] + Loop_INDEX]); }
            if (START_pozíció == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Írás("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_köteg() : Eszközök(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !felület_szintaxis.연결중) { 단말.Írás("exit "); 단말.szám(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Eszközök(13); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Eszközök(15); KR = 처리값 < 0 ? 126 : 처리값; if (!felület_szintaxis.연결중) { 단말.Írás("exit "); 단말.szám(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Eszközök(16); KR = 처리값 < 0 ? 126 : 처리값; if (!felület_szintaxis.연결중) { 단말.Írás("exit "); 단말.szám(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Méret = fal.Terminál(13); 단말.Írás("TERMINAL SIZE "); 단말.szám(Méret & 65535); 단말.문자('x'); 단말.szám(Méret >>> 16); 단말.문자(10); }
            else Terminál(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { fal.Terminál(9); Asztal.végrehajt_parancs(); }
        else if (같음(0, "c")) kernel.teszt_C();
        else if (같음(0, "tasks") || 같음(0, "t")) kernel.teszt_Tasks();
        else if (같음(0, "g")) kernel.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kernel.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = fal.futtat_felhasználó_app(0); if (처리값 == 0) 단말.Írás("ELF DEMO PASS\n"); else HIBA(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? eszköz_bejegyzés(-2, 2) : Eszközök(-1); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !felület_szintaxis.연결중) { 단말.Írás("exit "); 단말.szám(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kernel.teszt_hálózat();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = fal.fájlátvitel_szolgáltatás(1); if (처리값 < 0) HIBA(처리값); else { 단말.Írás("FTP listening "); Rendszer_eszköz.ír_CÍM(fal.hálózat_állapot(0,0)); 단말.Írás(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { fal.fájlátvitel_szolgáltatás(0); 단말.Írás("FTP stopped\n"); }
            else 단말.Írás(fal.fájlátvitel_szolgáltatás(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { köteg.Előkészítés(); 단말.Írás("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Nyelv = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (kód_DARAB != 2 || Nyelv < 0) 단말.Írás("example java|c|python: Kimenet, Fájl, 네트워크, 그래픽, Java Swing Ablak 예제\n");
            else { int 처리값 = 예제꾸러미.telepít_ÉRTÉK(Nyelv); if (처리값 < 0) { HIBA(처리값); if (처리값 == -28) 단말.Írás("RAM full: remove unused files, then retry example\n"); } else 단말.Írás("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formáz_ÉRTÉK = végrehajtás_formáz();
            if (formáz_ÉRTÉK == 1 || formáz_ÉRTÉK == 2) {
                int 처리값 = eszköz_bejegyzés(formáz_ÉRTÉK == 1 ? -1 : 14, 0); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !felület_szintaxis.연결중) { 단말.Írás("exit "); 단말.szám(처리값); 단말.문자(10); }
            } else if (formáz_ÉRTÉK == 0) { KR = 126; 단말.Írás("실행할 szám 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { KR = 127; 단말.Írás("Unknown command. help: commands\n"); }
        }
    }
    public static void végrehajt_parancs() {
        köteg.Előkészítés();
        for (int Nyelv = 0; Nyelv < 3; Nyelv++) { int 처리값 = 예제꾸러미.telepít_ÉRTÉK(Nyelv); if (처리값 < 0) HIBA(처리값); }
        bemutató_súgó();
        while (true) {
            ablak_munkamenet.folyamat_ÉRTÉK_bejegyzés(); if (ablak_munkamenet.CV_végrehajtás()) continue;
            if (!ablak_munkamenet.이어읽기) 단말.Írás("jkoros-native> "); sorszerkesztő.parancssor = true; fal.távoli_várj(1); int Méret = 줄읽기(); fal.távoli_várj(0); sorszerkesztő.parancssor = false;
            if (Méret == -3) continue;
            if (Méret == -2) 단말.Írás("Parancs elemez_ÉRTÉK: 명령줄이 너무 깁니다\n");
            if (Méret >= 0) { felület_szintaxis.parancsfájl_megszüntet = false; felület_szintaxis.végrehajt_parancs(Vonal, 0, Méret, 0); } else felület_szintaxis.Állapot_ÉRTÉK = 130;
            fal.megszüntet_távoli_parancs(felület_szintaxis.Állapot_ÉRTÉK);
            sorszerkesztő.Méret = sorszerkesztő.kurzor_ÉRTÉK = sorszerkesztő.START_ablak = 0;
        }
    }
}
