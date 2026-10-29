// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 komando_lerro. Aipua, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Marra = new int[4096], token_balio = new int[4096], 시작점 = new int[32], luzera_balio = new int[32];
    static int[] Editatutakoak_Edukia = new int[16384], edizio_izen = new int[63];
    static int token_ZENBATU, edizio_izen_luzera, EMAITZA;
    static boolean 앞줄;
    static void 원바이트(int balio) { arbel.직렬쓰기(balio); }
    static int 줄읽기() { return lerro_editore.Irakurri(); }
    static boolean 나누기(int Tamaina) {
        int Posizioa = 0, 끝 = 0; token_ZENBATU = 0;
        while (Posizioa < Tamaina) {
            while (Posizioa < Tamaina && (Marra[Posizioa] == 32 || Marra[Posizioa] == 9)) Posizioa++;
            if (Posizioa == Tamaina) break;
            if (token_ZENBATU == 16) { 단말.Idatzi("Komandoa analizatu_balio: 인수가 너무 많습니다\n"); return false; }
            시작점[token_ZENBATU] = 끝; int Aipua_balio = 0;
            while (Posizioa < Tamaina) {
                int balio = Marra[Posizioa++];
                if (Aipua_balio == 0 && (balio == 32 || balio == 9)) break;
                if (balio == Aipua_balio) { Aipua_balio = 0; continue; }
                if (Aipua_balio == 0 && (balio == 39 || balio == 34)) { Aipua_balio = balio; continue; }
                token_balio[끝++] = balio;
            }
            if (Aipua_balio != 0) { 단말.Idatzi("Komandoa analizatu_balio: 따옴표가 닫히지 않았습니다\n"); return false; }
            luzera_balio[token_ZENBATU] = 끝 - 시작점[token_ZENBATU]; token_ZENBATU++;
        }
        return true;
    }
    static boolean 같음(int INDIZE, String Word_SMS) {
        if (INDIZE >= token_ZENBATU) return false;
        int kargu_INDIZE=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int karaktere_kode=Word_SMS.charAt(순번);
            if (karaktere_kode>=0xd800 && karaktere_kode<=0xdbff && 순번+1<Word_SMS.length()) karaktere_kode=0x10000+((karaktere_kode-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_ZENBATU=karaktere_kode<128?1:karaktere_kode<2048?2:karaktere_kode<65536?3:4;
            for (int SEKUENTZIA_balio=byte_ZENBATU-1; SEKUENTZIA_balio>=0; SEKUENTZIA_balio--) {
                int balio=byte_ZENBATU==1?karaktere_kode:SEKUENTZIA_balio==byte_ZENBATU-1?(byte_ZENBATU==2?0xc0:byte_ZENBATU==3?0xe0:0xf0)|(karaktere_kode>>(6*SEKUENTZIA_balio)):0x80|((karaktere_kode>>(6*SEKUENTZIA_balio))&63);
                if (kargu_INDIZE>=luzera_balio[INDIZE] || token_balio[시작점[INDIZE]+kargu_INDIZE++]!=balio) return false;
            }
        }
        return kargu_INDIZE==luzera_balio[INDIZE];
    }
    static int Bide_izena(int INDIZE) {
        if (INDIZE >= token_ZENBATU) return -22;
        int EMAITZA = Memoria_Fitxategiak.bide_izen_HASI(luzera_balio[INDIZE]); if (EMAITZA < 0) return EMAITZA;
        for (int Loop_INDIZE = 0; Loop_INDIZE < luzera_balio[INDIZE]; Loop_INDIZE++) {
            EMAITZA = Memoria_Fitxategiak.bide_izen_byte(Loop_INDIZE, token_balio[시작점[INDIZE] + Loop_INDIZE]); if (EMAITZA < 0) return EMAITZA;
        }
        return 0;
    }
    static void errorea(int INDIZE) { EMAITZA = 1; 단말.Idatzi("errorea "); 단말.수(INDIZE); 단말.문자(10); }
    static void ikusi_balio() {
        if (token_ZENBATU != 2) { 단말.Idatzi("사용법: cat Fitxategia\n"); return; }
        int EMAITZA = Bide_izena(1); if (EMAITZA < 0) { errorea(EMAITZA); return; }
        int Fitxategia = Memoria_Fitxategiak.Ireki(0); if (Fitxategia < 0) { errorea(Fitxategia); return; }
        while (true) { int balio = Memoria_Fitxategiak.Irakurri(Fitxategia); if (balio == 256) break; if (balio < 0) { errorea(balio); break; } 원바이트(balio); }
        Memoria_Fitxategiak.Itxi(Fitxategia); 단말.문자(10);
    }
    static void edizio_balio() {
        if (token_ZENBATU != 2) { 단말.Idatzi("사용법: edit Fitxategia\n"); return; }
        int EMAITZA = Bide_izena(1); if (EMAITZA < 0) { errorea(EMAITZA); return; }
        edizio_izen_luzera = luzera_balio[1];
        for (int Loop_INDIZE = 0; Loop_INDIZE < edizio_izen_luzera; Loop_INDIZE++) edizio_izen[Loop_INDIZE] = token_balio[시작점[1] + Loop_INDIZE];
        단말.Idatzi("EDIT: Fitxategia 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Tamaina = 0;
        while (true) {
            단말.Idatzi("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Idatzi("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Marra[0] == '.') break;
            if (입력 + 1 > Editatutakoak_Edukia.length - Tamaina) { 단말.Idatzi("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDIZE = 0; Loop_INDIZE < 입력; Loop_INDIZE++) Editatutakoak_Edukia[Tamaina++] = Marra[Loop_INDIZE];
            Editatutakoak_Edukia[Tamaina++] = 10;
        }
        Memoria_Fitxategiak.bide_izen_HASI(edizio_izen_luzera);
        for (int Loop_INDIZE = 0; Loop_INDIZE < edizio_izen_luzera; Loop_INDIZE++) Memoria_Fitxategiak.bide_izen_byte(Loop_INDIZE, edizio_izen[Loop_INDIZE]);
        int Fitxategia = Memoria_Fitxategiak.Ireki(577); if (Fitxategia < 0) { errorea(Fitxategia); return; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < Tamaina; Loop_INDIZE++) Memoria_Fitxategiak.Idatzi(Fitxategia, Editatutakoak_Edukia[Loop_INDIZE]);
        Memoria_Fitxategiak.Itxi(Fitxategia); 단말.Idatzi("SAVED "); 단말.수(Tamaina); 단말.Idatzi("byte_balio(주기억 Fitxategia)\n");
    }
    static int hamaseitarra_balio(int balio) {
        if (balio >= '0' && balio <= '9') return balio - '0';
        if (balio >= 'a' && balio <= 'f') return balio - 'a' + 10;
        if (balio >= 'A' && balio <= 'F') return balio - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_ZENBATU != 2) { 단말.Idatzi("사용법: load Fitxategia | hex Fitxategia\n"); return; }
        int EMAITZA = Bide_izena(1); if (EMAITZA < 0) { errorea(EMAITZA); return; }
        if (!넣기) {
            int Fitxategia = Memoria_Fitxategiak.Ireki(0); if (Fitxategia < 0) { errorea(Fitxategia); return; }
            단말.Idatzi("HEX BEGIN "); 단말.수(Memoria_Fitxategiak.Tamaina(Fitxategia)); 단말.문자(10);
            int sarrera_ZENBATU = 0;
            while (true) {
                int balio = Memoria_Fitxategiak.Irakurri(Fitxategia); if (balio < 0 || balio == 256) break;
                단말.문자("0123456789abcdef".charAt(balio >> 4)); 단말.문자("0123456789abcdef".charAt(balio & 15));
                if (++sarrera_ZENBATU % 32 == 0) 단말.문자(10);
            }
            if (sarrera_ZENBATU % 32 != 0) 단말.문자(10);
            Memoria_Fitxategiak.Itxi(Fitxategia); 단말.Idatzi("HEX END\n"); return;
        }
        edizio_izen_luzera = luzera_balio[1];
        for (int Loop_INDIZE = 0; Loop_INDIZE < edizio_izen_luzera; Loop_INDIZE++) edizio_izen[Loop_INDIZE] = token_balio[시작점[1] + Loop_INDIZE];
        단말.Idatzi("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Tamaina = 0;
        while (true) {
            단말.Idatzi("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Idatzi("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Marra[0] == '.') break;
            int aurrekoa_balio = -1;
            for (int Loop_INDIZE = 0; Loop_INDIZE < 입력; Loop_INDIZE++) {
                if (Marra[Loop_INDIZE] == 32 || Marra[Loop_INDIZE] == 9) continue;
                int balio = hamaseitarra_balio(Marra[Loop_INDIZE]);
                if (balio < 0 || Tamaina >= Editatutakoak_Edukia.length) { 단말.Idatzi("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (aurrekoa_balio < 0) aurrekoa_balio = balio; else { Editatutakoak_Edukia[Tamaina++] = aurrekoa_balio * 16 + balio; aurrekoa_balio = -1; }
            }
            if (aurrekoa_balio >= 0) { 단말.Idatzi("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memoria_Fitxategiak.bide_izen_HASI(edizio_izen_luzera);
        for (int Loop_INDIZE = 0; Loop_INDIZE < edizio_izen_luzera; Loop_INDIZE++) Memoria_Fitxategiak.bide_izen_byte(Loop_INDIZE, edizio_izen[Loop_INDIZE]);
        int Fitxategia = Memoria_Fitxategiak.Ireki(577); if (Fitxategia < 0) { errorea(Fitxategia); return; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < Tamaina; Loop_INDIZE++) Memoria_Fitxategiak.Idatzi(Fitxategia, Editatutakoak_Edukia[Loop_INDIZE]);
        Memoria_Fitxategiak.Itxi(Fitxategia); 단말.Idatzi("LOADED "); 단말.수(Tamaina); 단말.Idatzi("byte_balio(주기억 Fitxategia)\n");
    }
    static int Tresnak(int INDIZE) {
        return tresna_sarrera(INDIZE, 1);
    }
    static int tresna_sarrera(int INDIZE, int Exekutatu_2) {
        if (token_ZENBATU - Exekutatu_2 > 8) return -22;
        arbel.인수준비(token_ZENBATU - Exekutatu_2);
        for (int 첫값 = Exekutatu_2; 첫값 < token_ZENBATU; 첫값++) {
            if (luzera_balio[첫값] > 255) return -36;
            for (int Loop_INDIZE = 0; Loop_INDIZE < luzera_balio[첫값]; Loop_INDIZE++) arbel.arg_byte(첫값 - Exekutatu_2, Loop_INDIZE, token_balio[시작점[첫값] + Loop_INDIZE]);
        }
        return INDIZE == -2 ? arbel.리눅스파일실행() : INDIZE < 0 ? arbel.exekutatu_erabiltzaile_fitxategi() : arbel.exekutatu_erabiltzaile_aplik(INDIZE);
    }
    static int PYTHON_multzo() {
        if (token_ZENBATU > 8) return -22;
        arbel.인수준비(token_ZENBATU);
        String Bide_izena = "/lib/multzo.py";
        // Java 문자열을 셸의 UTF-8 Argumentuak 버퍼에 기록한다.
        int kargu_INDIZE = 0;
        for (int 순번 = 0; 순번 < Bide_izena.length(); 순번++) {
            int karaktere_balio = Bide_izena.charAt(순번);
            if (karaktere_balio < 128) arbel.arg_byte(0, kargu_INDIZE++, karaktere_balio);
            else { arbel.arg_byte(0, kargu_INDIZE++, 0xe0 | (karaktere_balio >> 12)); arbel.arg_byte(0, kargu_INDIZE++, 0x80 | ((karaktere_balio >> 6) & 63)); arbel.arg_byte(0, kargu_INDIZE++, 0x80 | (karaktere_balio & 63)); }
        }
        for (int 순번 = 1; 순번 < token_ZENBATU; 순번++) {
            if (luzera_balio[순번] > 255) return -36;
            for (int karaktere_balio = 0; karaktere_balio < luzera_balio[순번]; karaktere_balio++) arbel.arg_byte(순번, karaktere_balio, token_balio[시작점[순번] + karaktere_balio]);
        }
        return arbel.exekutatu_erabiltzaile_aplik(12);
    }
    static int 실행형식() {
        int 처리값 = Bide_izena(0); if (처리값 < 0) return 처리값;
        int Fitxategia = Memoria_Fitxategiak.Ireki(0); if (Fitxategia < 0) return Fitxategia;
        int 첫값 = Memoria_Fitxategiak.Irakurri(Fitxategia), byte_datuak = Memoria_Fitxategiak.Irakurri(Fitxategia), karaktere_kode = Memoria_Fitxategiak.Irakurri(Fitxategia), 뒷값 = Memoria_Fitxategiak.Irakurri(Fitxategia);
        Memoria_Fitxategiak.Itxi(Fitxategia);
        if (첫값 == 127 && byte_datuak == 'E' && karaktere_kode == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_datuak == 'K' && karaktere_kode == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDIZE, String Argumentuak) {
        arbel.인수준비(1);
        for (int Loop_INDIZE = 0; Loop_INDIZE < Argumentuak.length(); Loop_INDIZE++) arbel.arg_byte(0, Loop_INDIZE, Argumentuak.charAt(Loop_INDIZE));
        return arbel.exekutatu_erabiltzaile_aplik(INDIZE);
    }
    static void SMS_byte(int Fitxategia, int balio) { Memoria_Fitxategiak.Idatzi(Fitxategia, balio); }
    static void estatiko_fitxategi(String Izena, String eduki_balio) {
        // multzo 파일명은 ASCII. Fitxategia 내용은 UTF-8로 저장한다.
        Memoria_Fitxategiak.bide_izen_HASI(Izena.length());
        for (int Loop_INDIZE = 0; Loop_INDIZE < Izena.length(); Loop_INDIZE++) Memoria_Fitxategiak.bide_izen_byte(Loop_INDIZE, Izena.charAt(Loop_INDIZE));
        int Fitxategia = Memoria_Fitxategiak.Ireki(193); if (Fitxategia < 0) return;
        for (int Loop_INDIZE = 0; Loop_INDIZE < eduki_balio.length(); Loop_INDIZE++) {
            int karaktere_kode = eduki_balio.charAt(Loop_INDIZE);
            if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdbff && Loop_INDIZE + 1 < eduki_balio.length()) karaktere_kode = 0x10000 + ((karaktere_kode - 0xd800) << 10) + eduki_balio.charAt(++Loop_INDIZE) - 0xdc00;
            if (karaktere_kode < 128) SMS_byte(Fitxategia, karaktere_kode);
            else {
                int 수 = karaktere_kode < 2048 ? 2 : karaktere_kode < 65536 ? 3 : 4;
                SMS_byte(Fitxategia, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (karaktere_kode >> (6 * (수 - 1))));
                for (int sarrera_ZENBATU = 수 - 1; sarrera_ZENBATU > 0; sarrera_ZENBATU--) SMS_byte(Fitxategia, 0x80 | ((karaktere_kode >> (6 * (sarrera_ZENBATU - 1))) & 63));
            }
        }
        Memoria_Fitxategiak.Itxi(Fitxategia);
    }
    static void 한글도움말() {
        단말.Idatzi("F9 / Shift+Space: [EN] ↔ [eu]\n");
        단말.Idatzi("  [EU] keyboard; [EN] ASCII\n");
        단말.Idatzi("  a → a\n");
        단말.Idatzi("  F9: EN ↔ eu | Ctrl+Shift+V: UTF-8\n");
        단말.Idatzi("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Idatzi("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Izena) {
        int byte_ZENBATU = 0;
        for (int Loop_INDIZE = 0; Loop_INDIZE < Izena.length(); Loop_INDIZE++) { int karaktere_kode = Izena.charAt(Loop_INDIZE); if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdfff) return -22; byte_ZENBATU += karaktere_kode < 128 ? 1 : karaktere_kode < 2048 ? 2 : 3; }
        int 처리값 = Memoria_Fitxategiak.bide_izen_HASI(byte_ZENBATU); if (처리값 < 0) return 처리값;
        int kargu_INDIZE = 0;
        for (int Loop_INDIZE = 0; Loop_INDIZE < Izena.length(); Loop_INDIZE++) {
            int karaktere_kode = Izena.charAt(Loop_INDIZE);
            if (karaktere_kode < 128) Memoria_Fitxategiak.bide_izen_byte(kargu_INDIZE++, karaktere_kode);
            else if (karaktere_kode < 2048) { Memoria_Fitxategiak.bide_izen_byte(kargu_INDIZE++, 0xc0 | (karaktere_kode >> 6)); Memoria_Fitxategiak.bide_izen_byte(kargu_INDIZE++, 0x80 | (karaktere_kode & 63)); }
            else { Memoria_Fitxategiak.bide_izen_byte(kargu_INDIZE++, 0xe0 | (karaktere_kode >> 12)); Memoria_Fitxategiak.bide_izen_byte(kargu_INDIZE++, 0x80 | ((karaktere_kode >> 6) & 63)); Memoria_Fitxategiak.bide_izen_byte(kargu_INDIZE++, 0x80 | (karaktere_kode & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Izena) {
        int 처리값 = 예제경로(Izena); if (처리값 < 0) return 처리값;
        처리값 = Memoria_Fitxategiak.sortu_direktorio(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Izena, String datuak) {
        int 처리값 = 예제경로(Izena); if (처리값 < 0) return 처리값;
        int Fitxategia = Memoria_Fitxategiak.Ireki(193); if (Fitxategia == -17) return 0; if (Fitxategia < 0) return Fitxategia;
        for (int Loop_INDIZE = 0; Loop_INDIZE < datuak.length(); Loop_INDIZE += 2) {
            처리값 = Memoria_Fitxategiak.Idatzi(Fitxategia, hamaseitarra_balio(datuak.charAt(Loop_INDIZE)) * 16 + hamaseitarra_balio(datuak.charAt(Loop_INDIZE + 1)));
            if (처리값 < 0) { Memoria_Fitxategiak.Itxi(Fitxategia); return 처리값; }
        }
        return Memoria_Fitxategiak.Itxi(Fitxategia);
    }
    static void erakutsi_laguntza() {
        sistema_tresna.erakutsi_laguntza();
        단말.Idatzi("sshd / seguru_shell start|stop|status: SSH :22 (user, 장치별 pasahitz_balio)\n");
        단말.Idatzi("vncd / urruneko_pantaila start|stop|status: VNC :5900 (장치별 pasahitz_balio)\n");
        단말.Idatzi("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Idatzi("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Idatzi("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Idatzi("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Idatzi("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Idatzi("모서리 + 왼쪽 버튼 arrastatu_balio: Terminala Tamaina aldatu_balio; terminal size: zutabe_balio/ERRENKADA_balio\n");
        단말.Idatzi("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Idatzi("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Idatzi("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Idatzi("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Idatzi("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Idatzi("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Idatzi("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Idatzi("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Idatzi("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Idatzi("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Idatzi("pip: MicroPython iturburu_zuhaitz instalatu_balio; Ostalari --network --pip 필요; /lib는 RAM\n");
        단말.Idatzi("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Idatzi("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Idatzi("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Idatzi("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminala(boolean 전환여부) {
        if (전환여부 && arbel.Terminala(2) != 0) { arbel.Terminala(0); 단말.Idatzi("TERMINAL CLOSED\n"); }
        else if (arbel.Terminala(1) < 0) errorea(-19);
        else 단말.Idatzi("TERMINAL READY — eu terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Komandoa() {
        if (token_ZENBATU == 0) return;
        if (sistema_tresna.exekutatu_komando()) return;
        if (같음(0,"sshd") || 같음(0,"seguru_shell") || 같음(0,"vncd") || 같음(0,"urruneko_pantaila")) {
            int 종류=같음(0,"vncd")||같음(0,"urruneko_pantaila")?1:0;
            int Ekintza=같음(1,"start")||같음(1,"Exekutatu_2")?1:같음(1,"stop")||같음(1,"Gelditu")?0:2;
            int Egoera_balio=arbel.aldi_bereko_saio(종류,Ekintza);
            if(Egoera_balio<0)errorea(Egoera_balio);else 단말.Idatzi(arbel.aldi_bereko_saio(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else erakutsi_laguntza(); }
        else if (같음(0, "info") || 같음(0, "i")) nukleo.msinfo32_exe();
        else if (같음(0, "pwd")) { Memoria_Fitxategiak.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_ZENBATU == 1) { Memoria_Fitxategiak.bide_izen_HASI(1); 처리값 = Memoria_Fitxategiak.bide_izen_byte(0, '/'); } else 처리값 = token_ZENBATU == 2 ? Bide_izena(1) : -22;
            if (처리값 >= 0) 처리값 = Memoria_Fitxategiak.aldatu_direktorio(); if (처리값 < 0) errorea(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int arg_INDIZE = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_ZENBATU == arg_INDIZE) { Memoria_Fitxategiak.bide_izen_HASI(1); 처리값 = Memoria_Fitxategiak.bide_izen_byte(0, '.'); } else 처리값 = token_ZENBATU == arg_INDIZE + 1 ? Bide_izena(arg_INDIZE) : -22;
            if (처리값 >= 0) 처리값 = Memoria_Fitxategiak.경로목록(); if (처리값 < 0) errorea(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) shell_Tresnak.fitxategi_lan(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) shell_Tresnak.kopiatu_balio(같음(0, "mv"));
        else if (같음(0, "cat")) shell_Tresnak.ikusi_balio();
        else if (같음(0, "wc")) shell_Tresnak.세기();
        else if (같음(0, "grep")) shell_Tresnak.Bilatu_sarrera();
        else if (같음(0, "head") || 같음(0, "tail")) shell_Tresnak.머리(같음(0, "tail"));
        else if (같음(0, "tee")) shell_Tresnak.idatzi_Batera();
        else if (같음(0, "env")) shell_sintaxi.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_ZENBATU == 1) shell_sintaxi.환경보기();
            for (int Loop_INDIZE = 1; Loop_INDIZE < token_ZENBATU; Loop_INDIZE++) { int 처리값 = shell_sintaxi.환경설정(Loop_INDIZE, 같음(0, "unset")); if (처리값 != 0) { EMAITZA = 처리값; 단말.Idatzi("Komandoa analizatu_balio: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) shell_sintaxi.exekutatu_fitxategi();
        else if (같음(0, "true")) EMAITZA = 0;
        else if (같음(0, "false")) EMAITZA = 1;
        else if (같음(0, "history")) lerro_editore.erakutsi_LOG();
        else if (같음(0, "exit")) {
            if (shell_sintaxi.깊이 > 0) { EMAITZA = token_ZENBATU == 1 ? shell_sintaxi.Egoera_balio : shell_Tresnak.digitu_balio(1); if (EMAITZA < 0 || EMAITZA > 255) EMAITZA = 2; shell_sintaxi.script_amaitu = true; }
            else if (arbel.Terminala(2) != 0) Terminala(true);
            else 단말.Idatzi("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) edizio_balio();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_ZENBATU < 2) { EMAITZA = 2; 단말.Idatzi("사용법: rm Fitxategia...\n"); }
            for (int Loop_INDIZE = 1; Loop_INDIZE < token_ZENBATU; Loop_INDIZE++) { int 처리값 = Bide_izena(Loop_INDIZE); if (처리값 == 0) 처리값 = Memoria_Fitxategiak.ezabatu_sarrera(); if (처리값 < 0) errorea(처리값); }
        }
        else if (같음(0, "echo")) {
            int HASI_kargu = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = HASI_kargu; 첫값 < token_ZENBATU; 첫값++) { if (첫값 > HASI_kargu) 단말.문자(32); for (int Loop_INDIZE = 0; Loop_INDIZE < luzera_balio[첫값]; Loop_INDIZE++) arbel.직렬쓰기(token_balio[시작점[첫값] + Loop_INDIZE]); }
            if (HASI_kargu == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Idatzi("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_multzo() : Tresnak(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); EMAITZA = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !shell_sintaxi.연결중) { 단말.Idatzi("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Tresnak(13); EMAITZA = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Tresnak(15); EMAITZA = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxi.연결중) { 단말.Idatzi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Tresnak(16); EMAITZA = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxi.연결중) { 단말.Idatzi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Tamaina = arbel.Terminala(13); 단말.Idatzi("TERMINAL SIZE "); 단말.수(Tamaina & 65535); 단말.문자('x'); 단말.수(Tamaina >>> 16); 단말.문자(10); }
            else Terminala(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { arbel.Terminala(9); mahaigain.exekutatu_komando(); }
        else if (같음(0, "c")) nukleo.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) nukleo.작업시험();
        else if (같음(0, "g")) nukleo.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) nukleo.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = arbel.exekutatu_erabiltzaile_aplik(0); if (처리값 == 0) 단말.Idatzi("ELF DEMO PASS\n"); else errorea(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? tresna_sarrera(-2, 2) : Tresnak(-1); EMAITZA = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !shell_sintaxi.연결중) { 단말.Idatzi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) nukleo.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = arbel.fitxategi_transferitu_zerbitzu(1); if (처리값 < 0) errorea(처리값); else { 단말.Idatzi("FTP listening "); sistema_tresna.idatzi_helbide(arbel.sare_egoera(0,0)); 단말.Idatzi(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { arbel.fitxategi_transferitu_zerbitzu(0); 단말.Idatzi("FTP stopped\n"); }
            else 단말.Idatzi(arbel.fitxategi_transferitu_zerbitzu(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { multzo.준비(); 단말.Idatzi("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Hizkuntza = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_ZENBATU != 2 || Hizkuntza < 0) 단말.Idatzi("example java|c|python: Irteera, Fitxategia, 네트워크, 그래픽, Java Swing Leihoa 예제\n");
            else { int 처리값 = 예제꾸러미.instalatu_balio(Hizkuntza); if (처리값 < 0) { errorea(처리값); if (처리값 == -28) 단말.Idatzi("RAM full: remove unused files, then retry example\n"); } else 단말.Idatzi("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formatu_balio = 실행형식();
            if (formatu_balio == 1 || formatu_balio == 2) {
                int 처리값 = tresna_sarrera(formatu_balio == 1 ? -1 : 14, 0); EMAITZA = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !shell_sintaxi.연결중) { 단말.Idatzi("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (formatu_balio == 0) { EMAITZA = 126; 단말.Idatzi("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { EMAITZA = 127; 단말.Idatzi("Unknown command. help: commands\n"); }
        }
    }
    public static void exekutatu_komando() {
        multzo.준비();
        for (int Hizkuntza = 0; Hizkuntza < 3; Hizkuntza++) { int 처리값 = 예제꾸러미.instalatu_balio(Hizkuntza); if (처리값 < 0) errorea(처리값); }
        erakutsi_laguntza();
        while (true) {
            leiho_saio.prozesu_balio_sarrera(); if (leiho_saio.재개()) continue;
            if (!leiho_saio.이어읽기) 단말.Idatzi("jkoros-native> "); lerro_editore.komando_lerro = true; arbel.urruneko_itxaron(1); int Tamaina = 줄읽기(); arbel.urruneko_itxaron(0); lerro_editore.komando_lerro = false;
            if (Tamaina == -3) continue;
            if (Tamaina == -2) 단말.Idatzi("Komandoa analizatu_balio: 명령줄이 너무 깁니다\n");
            if (Tamaina >= 0) { shell_sintaxi.script_amaitu = false; shell_sintaxi.exekutatu_komando(Marra, 0, Tamaina, 0); } else shell_sintaxi.Egoera_balio = 130;
            arbel.amaitu_urruneko_komando(shell_sintaxi.Egoera_balio);
            lerro_editore.Tamaina = lerro_editore.kurtsore_balio = lerro_editore.HASI_leiho = 0;
        }
    }
}
