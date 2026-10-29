// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 komandų_eilutė. Citavimas, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Eilutė = new int[4096], žetonas_VALUE = new int[4096], 시작점 = new int[32], 길이 = new int[32];
    static int[] Redaguotos_Turinys = new int[16384], redaguoti_pavadinimas = new int[63];
    static int žetonas_COUNT, 편집이름길이, REZULTATAS;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Lenta.직렬쓰기(VALUE); }
    static int 줄읽기() { return eilutinė_rengyklė.Skaitymas(); }
    static boolean 나누기(int Dydis) {
        int Pozicija = 0, 끝 = 0; žetonas_COUNT = 0;
        while (Pozicija < Dydis) {
            while (Pozicija < Dydis && (Eilutė[Pozicija] == 32 || Eilutė[Pozicija] == 9)) Pozicija++;
            if (Pozicija == Dydis) break;
            if (žetonas_COUNT == 16) { 단말.Rašymas("Komanda analizuoti_sintaksę_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[žetonas_COUNT] = 끝; int Citavimas_VALUE = 0;
            while (Pozicija < Dydis) {
                int VALUE = Eilutė[Pozicija++];
                if (Citavimas_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Citavimas_VALUE) { Citavimas_VALUE = 0; continue; }
                if (Citavimas_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Citavimas_VALUE = VALUE; continue; }
                žetonas_VALUE[끝++] = VALUE;
            }
            if (Citavimas_VALUE != 0) { 단말.Rašymas("Komanda analizuoti_sintaksę_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            길이[žetonas_COUNT] = 끝 - 시작점[žetonas_COUNT]; žetonas_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= žetonas_COUNT) return false;
        int vietos_rodyklė=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int simbolio_kodas=Word_SMS.charAt(순번);
            if (simbolio_kodas>=0xd800 && simbolio_kodas<=0xdbff && 순번+1<Word_SMS.length()) simbolio_kodas=0x10000+((simbolio_kodas-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int baitas_COUNT=simbolio_kodas<128?1:simbolio_kodas<2048?2:simbolio_kodas<65536?3:4;
            for (int SEQUENCE_VALUE=baitas_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=baitas_COUNT==1?simbolio_kodas:SEQUENCE_VALUE==baitas_COUNT-1?(baitas_COUNT==2?0xc0:baitas_COUNT==3?0xe0:0xf0)|(simbolio_kodas>>(6*SEQUENCE_VALUE)):0x80|((simbolio_kodas>>(6*SEQUENCE_VALUE))&63);
                if (vietos_rodyklė>=길이[INDEX] || žetonas_VALUE[시작점[INDEX]+vietos_rodyklė++]!=VALUE) return false;
            }
        }
        return vietos_rodyklė==길이[INDEX];
    }
    static int KELIAS(int INDEX) {
        if (INDEX >= žetonas_COUNT) return -22;
        int REZULTATAS = atmintis_Failai.kelias_Start(길이[INDEX]); if (REZULTATAS < 0) return REZULTATAS;
        for (int Loop_INDEX = 0; Loop_INDEX < 길이[INDEX]; Loop_INDEX++) {
            REZULTATAS = atmintis_Failai.kelias_baitas(Loop_INDEX, žetonas_VALUE[시작점[INDEX] + Loop_INDEX]); if (REZULTATAS < 0) return REZULTATAS;
        }
        return 0;
    }
    static void KLAIDA(int INDEX) { REZULTATAS = 1; 단말.Rašymas("KLAIDA "); 단말.numeris(INDEX); 단말.문자(10); }
    static void rodyti_VALUE() {
        if (žetonas_COUNT != 2) { 단말.Rašymas("사용법: cat Failas\n"); return; }
        int REZULTATAS = KELIAS(1); if (REZULTATAS < 0) { KLAIDA(REZULTATAS); return; }
        int Failas = atmintis_Failai.Atverti(0); if (Failas < 0) { KLAIDA(Failas); return; }
        while (true) { int VALUE = atmintis_Failai.Skaitymas(Failas); if (VALUE == 256) break; if (VALUE < 0) { KLAIDA(VALUE); break; } 원바이트(VALUE); }
        atmintis_Failai.Užverti(Failas); 단말.문자(10);
    }
    static void redaguoti_VALUE() {
        if (žetonas_COUNT != 2) { 단말.Rašymas("사용법: edit Failas\n"); return; }
        int REZULTATAS = KELIAS(1); if (REZULTATAS < 0) { KLAIDA(REZULTATAS); return; }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) redaguoti_pavadinimas[Loop_INDEX] = žetonas_VALUE[시작점[1] + Loop_INDEX];
        단말.Rašymas("EDIT: Failas 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Dydis = 0;
        while (true) {
            단말.Rašymas("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Rašymas("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Eilutė[0] == '.') break;
            if (입력 + 1 > Redaguotos_Turinys.length - Dydis) { 단말.Rašymas("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Redaguotos_Turinys[Dydis++] = Eilutė[Loop_INDEX];
            Redaguotos_Turinys[Dydis++] = 10;
        }
        atmintis_Failai.kelias_Start(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) atmintis_Failai.kelias_baitas(Loop_INDEX, redaguoti_pavadinimas[Loop_INDEX]);
        int Failas = atmintis_Failai.Atverti(577); if (Failas < 0) { KLAIDA(Failas); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Dydis; Loop_INDEX++) atmintis_Failai.Rašymas(Failas, Redaguotos_Turinys[Loop_INDEX]);
        atmintis_Failai.Užverti(Failas); 단말.Rašymas("SAVED "); 단말.numeris(Dydis); 단말.Rašymas("baitas_VALUE(주기억 Failas)\n");
    }
    static int šešioliktainis_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (žetonas_COUNT != 2) { 단말.Rašymas("사용법: load Failas | hex Failas\n"); return; }
        int REZULTATAS = KELIAS(1); if (REZULTATAS < 0) { KLAIDA(REZULTATAS); return; }
        if (!넣기) {
            int Failas = atmintis_Failai.Atverti(0); if (Failas < 0) { KLAIDA(Failas); return; }
            단말.Rašymas("HEX BEGIN "); 단말.numeris(atmintis_Failai.Dydis(Failas)); 단말.문자(10);
            int įrašas_COUNT = 0;
            while (true) {
                int VALUE = atmintis_Failai.Skaitymas(Failas); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++įrašas_COUNT % 32 == 0) 단말.문자(10);
            }
            if (įrašas_COUNT % 32 != 0) 단말.문자(10);
            atmintis_Failai.Užverti(Failas); 단말.Rašymas("HEX END\n"); return;
        }
        편집이름길이 = 길이[1];
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) redaguoti_pavadinimas[Loop_INDEX] = žetonas_VALUE[시작점[1] + Loop_INDEX];
        단말.Rašymas("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Dydis = 0;
        while (true) {
            단말.Rašymas("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Rašymas("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Eilutė[0] == '.') break;
            int priekinis_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Eilutė[Loop_INDEX] == 32 || Eilutė[Loop_INDEX] == 9) continue;
                int VALUE = šešioliktainis_VALUE(Eilutė[Loop_INDEX]);
                if (VALUE < 0 || Dydis >= Redaguotos_Turinys.length) { 단말.Rašymas("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (priekinis_VALUE < 0) priekinis_VALUE = VALUE; else { Redaguotos_Turinys[Dydis++] = priekinis_VALUE * 16 + VALUE; priekinis_VALUE = -1; }
            }
            if (priekinis_VALUE >= 0) { 단말.Rašymas("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        atmintis_Failai.kelias_Start(편집이름길이);
        for (int Loop_INDEX = 0; Loop_INDEX < 편집이름길이; Loop_INDEX++) atmintis_Failai.kelias_baitas(Loop_INDEX, redaguoti_pavadinimas[Loop_INDEX]);
        int Failas = atmintis_Failai.Atverti(577); if (Failas < 0) { KLAIDA(Failas); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Dydis; Loop_INDEX++) atmintis_Failai.Rašymas(Failas, Redaguotos_Turinys[Loop_INDEX]);
        atmintis_Failai.Užverti(Failas); 단말.Rašymas("LOADED "); 단말.numeris(Dydis); 단말.Rašymas("baitas_VALUE(주기억 Failas)\n");
    }
    static int Įrankiai(int INDEX) {
        return įrankis_įrašas(INDEX, 1);
    }
    static int įrankis_įrašas(int INDEX, int Paleisti) {
        if (žetonas_COUNT - Paleisti > 8) return -22;
        Lenta.인수준비(žetonas_COUNT - Paleisti);
        for (int 첫값 = Paleisti; 첫값 < žetonas_COUNT; 첫값++) {
            if (길이[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Lenta.argumentas_baitas(첫값 - Paleisti, Loop_INDEX, žetonas_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Lenta.리눅스파일실행() : INDEX < 0 ? Lenta.Vykdyti_naudotojas_Failas() : Lenta.vykdyti_naudotojas_programa(INDEX);
    }
    static int PYTHON_paketas() {
        if (žetonas_COUNT > 8) return -22;
        Lenta.인수준비(žetonas_COUNT);
        String KELIAS = "/lib/paketas.py";
        // Java 문자열을 셸의 UTF-8 Argumentai 버퍼에 기록한다.
        int vietos_rodyklė = 0;
        for (int 순번 = 0; 순번 < KELIAS.length(); 순번++) {
            int simbolis_VALUE_068c2631 = KELIAS.charAt(순번);
            if (simbolis_VALUE_068c2631 < 128) Lenta.argumentas_baitas(0, vietos_rodyklė++, simbolis_VALUE_068c2631);
            else { Lenta.argumentas_baitas(0, vietos_rodyklė++, 0xe0 | (simbolis_VALUE_068c2631 >> 12)); Lenta.argumentas_baitas(0, vietos_rodyklė++, 0x80 | ((simbolis_VALUE_068c2631 >> 6) & 63)); Lenta.argumentas_baitas(0, vietos_rodyklė++, 0x80 | (simbolis_VALUE_068c2631 & 63)); }
        }
        for (int 순번 = 1; 순번 < žetonas_COUNT; 순번++) {
            if (길이[순번] > 255) return -36;
            for (int simbolis_VALUE_068c2631 = 0; simbolis_VALUE_068c2631 < 길이[순번]; simbolis_VALUE_068c2631++) Lenta.argumentas_baitas(순번, simbolis_VALUE_068c2631, žetonas_VALUE[시작점[순번] + simbolis_VALUE_068c2631]);
        }
        return Lenta.vykdyti_naudotojas_programa(12);
    }
    static int 실행형식() {
        int 처리값 = KELIAS(0); if (처리값 < 0) return 처리값;
        int Failas = atmintis_Failai.Atverti(0); if (Failas < 0) return Failas;
        int 첫값 = atmintis_Failai.Skaitymas(Failas), baitas_duomenys = atmintis_Failai.Skaitymas(Failas), simbolio_kodas = atmintis_Failai.Skaitymas(Failas), 뒷값 = atmintis_Failai.Skaitymas(Failas);
        atmintis_Failai.Užverti(Failas);
        if (첫값 == 127 && baitas_duomenys == 'E' && simbolio_kodas == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && baitas_duomenys == 'K' && simbolio_kodas == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumentai) {
        Lenta.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumentai.length(); Loop_INDEX++) Lenta.argumentas_baitas(0, Loop_INDEX, Argumentai.charAt(Loop_INDEX));
        return Lenta.vykdyti_naudotojas_programa(INDEX);
    }
    static void SMS_baitas(int Failas, int VALUE) { atmintis_Failai.Rašymas(Failas, VALUE); }
    static void 정적파일(String Pavadinimas_2, String Turinys_VALUE) {
        // paketas 파일명은 ASCII. Failas 내용은 UTF-8로 저장한다.
        atmintis_Failai.kelias_Start(Pavadinimas_2.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Pavadinimas_2.length(); Loop_INDEX++) atmintis_Failai.kelias_baitas(Loop_INDEX, Pavadinimas_2.charAt(Loop_INDEX));
        int Failas = atmintis_Failai.Atverti(193); if (Failas < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Turinys_VALUE.length(); Loop_INDEX++) {
            int simbolio_kodas = Turinys_VALUE.charAt(Loop_INDEX);
            if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdbff && Loop_INDEX + 1 < Turinys_VALUE.length()) simbolio_kodas = 0x10000 + ((simbolio_kodas - 0xd800) << 10) + Turinys_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (simbolio_kodas < 128) SMS_baitas(Failas, simbolio_kodas);
            else {
                int numeris = simbolio_kodas < 2048 ? 2 : simbolio_kodas < 65536 ? 3 : 4;
                SMS_baitas(Failas, (numeris == 2 ? 0xc0 : numeris == 3 ? 0xe0 : 0xf0) | (simbolio_kodas >> (6 * (numeris - 1))));
                for (int įrašas_COUNT = numeris - 1; įrašas_COUNT > 0; įrašas_COUNT--) SMS_baitas(Failas, 0x80 | ((simbolio_kodas >> (6 * (įrašas_COUNT - 1))) & 63));
            }
        }
        atmintis_Failai.Užverti(Failas);
    }
    static void 한글도움말() {
        단말.Rašymas("F9 / Shift+Space: [EN] ↔ [lt]\n");
        단말.Rašymas("  [LT] keyboard; [EN] ASCII\n");
        단말.Rašymas("  ! → Ą\n");
        단말.Rašymas("  F9: EN ↔ lt | Ctrl+Shift+V: UTF-8\n");
        단말.Rašymas("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Rašymas("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Pavadinimas_2) {
        int baitas_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Pavadinimas_2.length(); Loop_INDEX++) { int simbolio_kodas = Pavadinimas_2.charAt(Loop_INDEX); if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdfff) return -22; baitas_COUNT += simbolio_kodas < 128 ? 1 : simbolio_kodas < 2048 ? 2 : 3; }
        int 처리값 = atmintis_Failai.kelias_Start(baitas_COUNT); if (처리값 < 0) return 처리값;
        int vietos_rodyklė = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Pavadinimas_2.length(); Loop_INDEX++) {
            int simbolio_kodas = Pavadinimas_2.charAt(Loop_INDEX);
            if (simbolio_kodas < 128) atmintis_Failai.kelias_baitas(vietos_rodyklė++, simbolio_kodas);
            else if (simbolio_kodas < 2048) { atmintis_Failai.kelias_baitas(vietos_rodyklė++, 0xc0 | (simbolio_kodas >> 6)); atmintis_Failai.kelias_baitas(vietos_rodyklė++, 0x80 | (simbolio_kodas & 63)); }
            else { atmintis_Failai.kelias_baitas(vietos_rodyklė++, 0xe0 | (simbolio_kodas >> 12)); atmintis_Failai.kelias_baitas(vietos_rodyklė++, 0x80 | ((simbolio_kodas >> 6) & 63)); atmintis_Failai.kelias_baitas(vietos_rodyklė++, 0x80 | (simbolio_kodas & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Pavadinimas_2) {
        int 처리값 = 예제경로(Pavadinimas_2); if (처리값 < 0) return 처리값;
        처리값 = atmintis_Failai.kurti_Katalogas(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Pavadinimas_2, String duomenys) {
        int 처리값 = 예제경로(Pavadinimas_2); if (처리값 < 0) return 처리값;
        int Failas = atmintis_Failai.Atverti(193); if (Failas == -17) return 0; if (Failas < 0) return Failas;
        for (int Loop_INDEX = 0; Loop_INDEX < duomenys.length(); Loop_INDEX += 2) {
            처리값 = atmintis_Failai.Rašymas(Failas, šešioliktainis_VALUE(duomenys.charAt(Loop_INDEX)) * 16 + šešioliktainis_VALUE(duomenys.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { atmintis_Failai.Užverti(Failas); return 처리값; }
        }
        return atmintis_Failai.Užverti(Failas);
    }
    static void laida_žinynas() {
        sistema_įrankis.laida_žinynas();
        단말.Rašymas("sshd / saugus_apvalkalas start|stop|status: SSH :22 (user, 장치별 slaptažodis_VALUE)\n");
        단말.Rašymas("vncd / nuotolinis_rodyti start|stop|status: VNC :5900 (장치별 slaptažodis_VALUE)\n");
        단말.Rašymas("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Rašymas("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Rašymas("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Rašymas("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Rašymas("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Rašymas("모서리 + 왼쪽 버튼 vilkti_VALUE: Terminalas Dydis keisti_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Rašymas("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Rašymas("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Rašymas("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Rašymas("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Rašymas("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Rašymas("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Rašymas("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Rašymas("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Rašymas("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Rašymas("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Rašymas("pip: MicroPython šaltinis_medis diegti_VALUE; organizuoti --network --pip 필요; /lib는 RAM\n");
        단말.Rašymas("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Rašymas("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Rašymas("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Rašymas("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminalas(boolean 전환여부) {
        if (전환여부 && Lenta.Terminalas(2) != 0) { Lenta.Terminalas(0); 단말.Rašymas("TERMINAL CLOSED\n"); }
        else if (Lenta.Terminalas(1) < 0) KLAIDA(-19);
        else 단말.Rašymas("TERMINAL READY — lt terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Komanda() {
        if (žetonas_COUNT == 0) return;
        if (sistema_įrankis.Vykdyti_komanda()) return;
        if (같음(0,"sshd") || 같음(0,"saugus_apvalkalas") || 같음(0,"vncd") || 같음(0,"nuotolinis_rodyti")) {
            int 종류=같음(0,"vncd")||같음(0,"nuotolinis_rodyti")?1:0;
            int Veiksmas=같음(1,"start")||같음(1,"Paleisti")?1:같음(1,"stop")||같음(1,"Sustabdyti")?0:2;
            int Būsena_VALUE=Lenta.stebėjimas(종류,Veiksmas);
            if(Būsena_VALUE<0)KLAIDA(Būsena_VALUE);else 단말.Rašymas(Lenta.stebėjimas(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else laida_žinynas(); }
        else if (같음(0, "info") || 같음(0, "i")) branduolys.msinfo32_exe();
        else if (같음(0, "pwd")) { atmintis_Failai.dabartinis_rašymas(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (žetonas_COUNT == 1) { atmintis_Failai.kelias_Start(1); 처리값 = atmintis_Failai.kelias_baitas(0, '/'); } else 처리값 = žetonas_COUNT == 2 ? KELIAS(1) : -22;
            if (처리값 >= 0) 처리값 = atmintis_Failai.keisti_Katalogas(); if (처리값 < 0) KLAIDA(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argumentas_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (žetonas_COUNT == argumentas_INDEX) { atmintis_Failai.kelias_Start(1); 처리값 = atmintis_Failai.kelias_baitas(0, '.'); } else 처리값 = žetonas_COUNT == argumentas_INDEX + 1 ? KELIAS(argumentas_INDEX) : -22;
            if (처리값 >= 0) 처리값 = atmintis_Failai.경로목록(); if (처리값 < 0) KLAIDA(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) apvalkalas_Įrankiai.Failas_Darbas(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) apvalkalas_Įrankiai.kopijuoti_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) apvalkalas_Įrankiai.rodyti_VALUE();
        else if (같음(0, "wc")) apvalkalas_Įrankiai.세기();
        else if (같음(0, "grep")) apvalkalas_Įrankiai.FIND_įrašas();
        else if (같음(0, "head") || 같음(0, "tail")) apvalkalas_Įrankiai.머리(같음(0, "tail"));
        else if (같음(0, "tee")) apvalkalas_Įrankiai.rašymas_Dviese();
        else if (같음(0, "env")) apvalkalas_sintaksė.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (žetonas_COUNT == 1) apvalkalas_sintaksė.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < žetonas_COUNT; Loop_INDEX++) { int 처리값 = apvalkalas_sintaksė.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { REZULTATAS = 처리값; 단말.Rašymas("Komanda analizuoti_sintaksę_VALUE: kintamasis_VALUE 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) apvalkalas_sintaksė.Vykdyti_Failas();
        else if (같음(0, "true")) REZULTATAS = 0;
        else if (같음(0, "false")) REZULTATAS = 1;
        else if (같음(0, "history")) eilutinė_rengyklė.laida_LOG();
        else if (같음(0, "exit")) {
            if (apvalkalas_sintaksė.깊이 > 0) { REZULTATAS = žetonas_COUNT == 1 ? apvalkalas_sintaksė.Būsena_VALUE : apvalkalas_Įrankiai.skaitmuo_VALUE(1); if (REZULTATAS < 0 || REZULTATAS > 255) REZULTATAS = 2; apvalkalas_sintaksė.scenarijus_baigti_pokalbį = true; }
            else if (Lenta.Terminalas(2) != 0) Terminalas(true);
            else 단말.Rašymas("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) redaguoti_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (žetonas_COUNT < 2) { REZULTATAS = 2; 단말.Rašymas("사용법: rm Failas...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < žetonas_COUNT; Loop_INDEX++) { int 처리값 = KELIAS(Loop_INDEX); if (처리값 == 0) 처리값 = atmintis_Failai.ištrinti_įrašas(); if (처리값 < 0) KLAIDA(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_padėtis = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_padėtis; 첫값 < žetonas_COUNT; 첫값++) { if (첫값 > Start_padėtis) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < 길이[첫값]; Loop_INDEX++) Lenta.직렬쓰기(žetonas_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Start_padėtis == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Rašymas("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_paketas() : Įrankiai(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); REZULTATAS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !apvalkalas_sintaksė.연결중) { 단말.Rašymas("exit "); 단말.numeris(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Įrankiai(13); REZULTATAS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Įrankiai(15); REZULTATAS = 처리값 < 0 ? 126 : 처리값; if (!apvalkalas_sintaksė.연결중) { 단말.Rašymas("exit "); 단말.numeris(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Įrankiai(16); REZULTATAS = 처리값 < 0 ? 126 : 처리값; if (!apvalkalas_sintaksė.연결중) { 단말.Rašymas("exit "); 단말.numeris(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Dydis = Lenta.Terminalas(13); 단말.Rašymas("TERMINAL SIZE "); 단말.numeris(Dydis & 65535); 단말.문자('x'); 단말.numeris(Dydis >>> 16); 단말.문자(10); }
            else Terminalas(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Lenta.Terminalas(9); darbalaukis.Vykdyti_komanda(); }
        else if (같음(0, "c")) branduolys.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) branduolys.작업시험();
        else if (같음(0, "g")) branduolys.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) branduolys.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Lenta.vykdyti_naudotojas_programa(0); if (처리값 == 0) 단말.Rašymas("ELF DEMO PASS\n"); else KLAIDA(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? įrankis_įrašas(-2, 2) : Įrankiai(-1); REZULTATAS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !apvalkalas_sintaksė.연결중) { 단말.Rašymas("exit "); 단말.numeris(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) branduolys.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Lenta.failo_perdavimas_tarnyba(1); if (처리값 < 0) KLAIDA(처리값); else { 단말.Rašymas("FTP listening "); sistema_įrankis.rašymas_ADDRESS(Lenta.tinklas_būsena(0,0)); 단말.Rašymas(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Lenta.failo_perdavimas_tarnyba(0); 단말.Rašymas("FTP stopped\n"); }
            else 단말.Rašymas(Lenta.failo_perdavimas_tarnyba(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { paketas.Parengti(); 단말.Rašymas("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Kalba = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (žetonas_COUNT != 2 || Kalba < 0) 단말.Rašymas("example java|c|python: Išvestis, Failas, 네트워크, 그래픽, Java Swing Langas 예제\n");
            else { int 처리값 = 예제꾸러미.diegti_VALUE(Kalba); if (처리값 < 0) { KLAIDA(처리값); if (처리값 == -28) 단말.Rašymas("RAM full: remove unused files, then retry example\n"); } else 단말.Rašymas("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formatas_VALUE = 실행형식();
            if (formatas_VALUE == 1 || formatas_VALUE == 2) {
                int 처리값 = įrankis_įrašas(formatas_VALUE == 1 ? -1 : 14, 0); REZULTATAS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !apvalkalas_sintaksė.연결중) { 단말.Rašymas("exit "); 단말.numeris(처리값); 단말.문자(10); }
            } else if (formatas_VALUE == 0) { REZULTATAS = 126; 단말.Rašymas("실행할 numeris 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { REZULTATAS = 127; 단말.Rašymas("Unknown command. help: commands\n"); }
        }
    }
    public static void Vykdyti_komanda() {
        paketas.Parengti();
        for (int Kalba = 0; Kalba < 3; Kalba++) { int 처리값 = 예제꾸러미.diegti_VALUE(Kalba); if (처리값 < 0) KLAIDA(처리값); }
        laida_žinynas();
        while (true) {
            langas_seansas.Procesas_VALUE_įrašas(); if (langas_seansas.재개()) continue;
            if (!langas_seansas.이어읽기) 단말.Rašymas("jkoros-native> "); eilutinė_rengyklė.komandų_eilutė = true; Lenta.nuotolinis_Palauk(1); int Dydis = 줄읽기(); Lenta.nuotolinis_Palauk(0); eilutinė_rengyklė.komandų_eilutė = false;
            if (Dydis == -3) continue;
            if (Dydis == -2) 단말.Rašymas("Komanda analizuoti_sintaksę_VALUE: 명령줄이 너무 깁니다\n");
            if (Dydis >= 0) { apvalkalas_sintaksė.scenarijus_baigti_pokalbį = false; apvalkalas_sintaksė.Vykdyti_komanda(Eilutė, 0, Dydis, 0); } else apvalkalas_sintaksė.Būsena_VALUE = 130;
            Lenta.baigti_pokalbį_nuotolinis_komanda(apvalkalas_sintaksė.Būsena_VALUE);
            eilutinė_rengyklė.Dydis = eilutinė_rengyklė.žymiklis_VALUE = eilutinė_rengyklė.Start_langas = 0;
        }
    }
}
