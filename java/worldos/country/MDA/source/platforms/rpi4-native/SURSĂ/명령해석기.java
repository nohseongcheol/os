// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 linie_de_comandă. Citat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Linie = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], lungime_VALUE = new int[32];
    static int[] Editate_TOC = new int[16384], edita_nume = new int[63];
    static int token_COUNT, edita_nume_lungime, KR;
    static boolean Anteriorul_linie;
    static void 원바이트(int VALUE) { Avizier.직렬쓰기(VALUE); }
    static int 줄읽기() { return editor_de_linii.Citire(); }
    static boolean 나누기(int Mărime) {
        int Poziție = 0, 끝 = 0; token_COUNT = 0;
        while (Poziție < Mărime) {
            while (Poziție < Mărime && (Linie[Poziție] == 32 || Linie[Poziție] == 9)) Poziție++;
            if (Poziție == Mărime) break;
            if (token_COUNT == 16) { 단말.Scriere("Comandă analiza_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Citat_VALUE = 0;
            while (Poziție < Mărime) {
                int VALUE = Linie[Poziție++];
                if (Citat_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Citat_VALUE) { Citat_VALUE = 0; continue; }
                if (Citat_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Citat_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Citat_VALUE != 0) { 단말.Scriere("Comandă analiza_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            lungime_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int index_de_poziție=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int cod_caracter=Word_SMS.charAt(순번);
            if (cod_caracter>=0xd800 && cod_caracter<=0xdbff && 순번+1<Word_SMS.length()) cod_caracter=0x10000+((cod_caracter-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_COUNT=cod_caracter<128?1:cod_caracter<2048?2:cod_caracter<65536?3:4;
            for (int SEQUENCE_VALUE=byte_COUNT-1; SEQUENCE_VALUE>=0; SEQUENCE_VALUE--) {
                int VALUE=byte_COUNT==1?cod_caracter:SEQUENCE_VALUE==byte_COUNT-1?(byte_COUNT==2?0xc0:byte_COUNT==3?0xe0:0xf0)|(cod_caracter>>(6*SEQUENCE_VALUE)):0x80|((cod_caracter>>(6*SEQUENCE_VALUE))&63);
                if (index_de_poziție>=lungime_VALUE[INDEX] || token_VALUE[시작점[INDEX]+index_de_poziție++]!=VALUE) return false;
            }
        }
        return index_de_poziție==lungime_VALUE[INDEX];
    }
    static int Cale(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int KR = Memorie_Fișiere.cale_buta(lungime_VALUE[INDEX]); if (KR < 0) return KR;
        for (int Loop_INDEX = 0; Loop_INDEX < lungime_VALUE[INDEX]; Loop_INDEX++) {
            KR = Memorie_Fișiere.cale_byte(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (KR < 0) return KR;
        }
        return 0;
    }
    static void eroare(int INDEX) { KR = 1; 단말.Scriere("eroare "); 단말.수(INDEX); 단말.문자(10); }
    static void vizualiza_VALUE() {
        if (token_COUNT != 2) { 단말.Scriere("사용법: cat Fișier\n"); return; }
        int KR = Cale(1); if (KR < 0) { eroare(KR); return; }
        int Fișier = Memorie_Fișiere.Deschide(0); if (Fișier < 0) { eroare(Fișier); return; }
        while (true) { int VALUE = Memorie_Fișiere.Citire(Fișier); if (VALUE == 256) break; if (VALUE < 0) { eroare(VALUE); break; } 원바이트(VALUE); }
        Memorie_Fișiere.Închide(Fișier); 단말.문자(10);
    }
    static void edita_VALUE() {
        if (token_COUNT != 2) { 단말.Scriere("사용법: edit Fișier\n"); return; }
        int KR = Cale(1); if (KR < 0) { eroare(KR); return; }
        edita_nume_lungime = lungime_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < edita_nume_lungime; Loop_INDEX++) edita_nume[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Scriere("EDIT: Fișier 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Mărime = 0;
        while (true) {
            단말.Scriere("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Scriere("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Linie[0] == '.') break;
            if (입력 + 1 > Editate_TOC.length - Mărime) { 단말.Scriere("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Editate_TOC[Mărime++] = Linie[Loop_INDEX];
            Editate_TOC[Mărime++] = 10;
        }
        Memorie_Fișiere.cale_buta(edita_nume_lungime);
        for (int Loop_INDEX = 0; Loop_INDEX < edita_nume_lungime; Loop_INDEX++) Memorie_Fișiere.cale_byte(Loop_INDEX, edita_nume[Loop_INDEX]);
        int Fișier = Memorie_Fișiere.Deschide(577); if (Fișier < 0) { eroare(Fișier); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Mărime; Loop_INDEX++) Memorie_Fișiere.Scriere(Fișier, Editate_TOC[Loop_INDEX]);
        Memorie_Fișiere.Închide(Fișier); 단말.Scriere("SAVED "); 단말.수(Mărime); 단말.Scriere("byte_VALUE(주기억 Fișier)\n");
    }
    static int hexadecimal_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.Scriere("사용법: load Fișier | hex Fișier\n"); return; }
        int KR = Cale(1); if (KR < 0) { eroare(KR); return; }
        if (!넣기) {
            int Fișier = Memorie_Fișiere.Deschide(0); if (Fișier < 0) { eroare(Fișier); return; }
            단말.Scriere("HEX BEGIN "); 단말.수(Memorie_Fișiere.Mărime(Fișier)); 단말.문자(10);
            int intrare_COUNT = 0;
            while (true) {
                int VALUE = Memorie_Fișiere.Citire(Fișier); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++intrare_COUNT % 32 == 0) 단말.문자(10);
            }
            if (intrare_COUNT % 32 != 0) 단말.문자(10);
            Memorie_Fișiere.Închide(Fișier); 단말.Scriere("HEX END\n"); return;
        }
        edita_nume_lungime = lungime_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < edita_nume_lungime; Loop_INDEX++) edita_nume[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Scriere("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Mărime = 0;
        while (true) {
            단말.Scriere("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Scriere("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Linie[0] == '.') break;
            int frontală_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (Linie[Loop_INDEX] == 32 || Linie[Loop_INDEX] == 9) continue;
                int VALUE = hexadecimal_VALUE(Linie[Loop_INDEX]);
                if (VALUE < 0 || Mărime >= Editate_TOC.length) { 단말.Scriere("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (frontală_VALUE < 0) frontală_VALUE = VALUE; else { Editate_TOC[Mărime++] = frontală_VALUE * 16 + VALUE; frontală_VALUE = -1; }
            }
            if (frontală_VALUE >= 0) { 단말.Scriere("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memorie_Fișiere.cale_buta(edita_nume_lungime);
        for (int Loop_INDEX = 0; Loop_INDEX < edita_nume_lungime; Loop_INDEX++) Memorie_Fișiere.cale_byte(Loop_INDEX, edita_nume[Loop_INDEX]);
        int Fișier = Memorie_Fișiere.Deschide(577); if (Fișier < 0) { eroare(Fișier); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Mărime; Loop_INDEX++) Memorie_Fișiere.Scriere(Fișier, Editate_TOC[Loop_INDEX]);
        Memorie_Fișiere.Închide(Fișier); 단말.Scriere("LOADED "); 단말.수(Mărime); 단말.Scriere("byte_VALUE(주기억 Fișier)\n");
    }
    static int Instrumente(int INDEX) {
        return instrument_intrare(INDEX, 1);
    }
    static int instrument_intrare(int INDEX, int Pornește) {
        if (token_COUNT - Pornește > 8) return -22;
        Avizier.인수준비(token_COUNT - Pornește);
        for (int 첫값 = Pornește; 첫값 < token_COUNT; 첫값++) {
            if (lungime_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < lungime_VALUE[첫값]; Loop_INDEX++) Avizier.argument_byte(첫값 - Pornește, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Avizier.리눅스파일실행() : INDEX < 0 ? Avizier.executa_utilizator_Fișier() : Avizier.rula_utilizator_program(INDEX);
    }
    static int PYTHON_set() {
        if (token_COUNT > 8) return -22;
        Avizier.인수준비(token_COUNT);
        String Cale = "/lib/set.py";
        // Java 문자열을 셸의 UTF-8 Argumente 버퍼에 기록한다.
        int index_de_poziție = 0;
        for (int 순번 = 0; 순번 < Cale.length(); 순번++) {
            int caracter_VALUE = Cale.charAt(순번);
            if (caracter_VALUE < 128) Avizier.argument_byte(0, index_de_poziție++, caracter_VALUE);
            else { Avizier.argument_byte(0, index_de_poziție++, 0xe0 | (caracter_VALUE >> 12)); Avizier.argument_byte(0, index_de_poziție++, 0x80 | ((caracter_VALUE >> 6) & 63)); Avizier.argument_byte(0, index_de_poziție++, 0x80 | (caracter_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (lungime_VALUE[순번] > 255) return -36;
            for (int caracter_VALUE = 0; caracter_VALUE < lungime_VALUE[순번]; caracter_VALUE++) Avizier.argument_byte(순번, caracter_VALUE, token_VALUE[시작점[순번] + caracter_VALUE]);
        }
        return Avizier.rula_utilizator_program(12);
    }
    static int executare_format() {
        int 처리값 = Cale(0); if (처리값 < 0) return 처리값;
        int Fișier = Memorie_Fișiere.Deschide(0); if (Fișier < 0) return Fișier;
        int 첫값 = Memorie_Fișiere.Citire(Fișier), byte_date = Memorie_Fișiere.Citire(Fișier), cod_caracter = Memorie_Fișiere.Citire(Fișier), 뒷값 = Memorie_Fișiere.Citire(Fișier);
        Memorie_Fișiere.Închide(Fișier);
        if (첫값 == 127 && byte_date == 'E' && cod_caracter == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_date == 'K' && cod_caracter == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String Argumente) {
        Avizier.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < Argumente.length(); Loop_INDEX++) Avizier.argument_byte(0, Loop_INDEX, Argumente.charAt(Loop_INDEX));
        return Avizier.rula_utilizator_program(INDEX);
    }
    static void SMS_byte(int Fișier, int VALUE) { Memorie_Fișiere.Scriere(Fișier, VALUE); }
    static void 정적파일(String Nume, String Conținut_VALUE) {
        // set 파일명은 ASCII. Fișier 내용은 UTF-8로 저장한다.
        Memorie_Fișiere.cale_buta(Nume.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Nume.length(); Loop_INDEX++) Memorie_Fișiere.cale_byte(Loop_INDEX, Nume.charAt(Loop_INDEX));
        int Fișier = Memorie_Fișiere.Deschide(193); if (Fișier < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Conținut_VALUE.length(); Loop_INDEX++) {
            int cod_caracter = Conținut_VALUE.charAt(Loop_INDEX);
            if (cod_caracter >= 0xd800 && cod_caracter <= 0xdbff && Loop_INDEX + 1 < Conținut_VALUE.length()) cod_caracter = 0x10000 + ((cod_caracter - 0xd800) << 10) + Conținut_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (cod_caracter < 128) SMS_byte(Fișier, cod_caracter);
            else {
                int 수 = cod_caracter < 2048 ? 2 : cod_caracter < 65536 ? 3 : 4;
                SMS_byte(Fișier, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (cod_caracter >> (6 * (수 - 1))));
                for (int intrare_COUNT = 수 - 1; intrare_COUNT > 0; intrare_COUNT--) SMS_byte(Fișier, 0x80 | ((cod_caracter >> (6 * (intrare_COUNT - 1))) & 63));
            }
        }
        Memorie_Fișiere.Închide(Fișier);
    }
    static void 한글도움말() {
        단말.Scriere("F9 sau Shift+Space activează introducerea în limba română.\n");
        단말.Scriere("  [RO] keyboard; [EN] ASCII\n");
        단말.Scriere("  a → a\n");
        단말.Scriere("  F9: EN ↔ Română | Ctrl+Shift+V: UTF-8\n");
        단말.Scriere("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Scriere("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nume) {
        int byte_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nume.length(); Loop_INDEX++) { int cod_caracter = Nume.charAt(Loop_INDEX); if (cod_caracter >= 0xd800 && cod_caracter <= 0xdfff) return -22; byte_COUNT += cod_caracter < 128 ? 1 : cod_caracter < 2048 ? 2 : 3; }
        int 처리값 = Memorie_Fișiere.cale_buta(byte_COUNT); if (처리값 < 0) return 처리값;
        int index_de_poziție = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nume.length(); Loop_INDEX++) {
            int cod_caracter = Nume.charAt(Loop_INDEX);
            if (cod_caracter < 128) Memorie_Fișiere.cale_byte(index_de_poziție++, cod_caracter);
            else if (cod_caracter < 2048) { Memorie_Fișiere.cale_byte(index_de_poziție++, 0xc0 | (cod_caracter >> 6)); Memorie_Fișiere.cale_byte(index_de_poziție++, 0x80 | (cod_caracter & 63)); }
            else { Memorie_Fișiere.cale_byte(index_de_poziție++, 0xe0 | (cod_caracter >> 12)); Memorie_Fișiere.cale_byte(index_de_poziție++, 0x80 | ((cod_caracter >> 6) & 63)); Memorie_Fișiere.cale_byte(index_de_poziție++, 0x80 | (cod_caracter & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nume) {
        int 처리값 = 예제경로(Nume); if (처리값 < 0) return 처리값;
        처리값 = Memorie_Fișiere.crea_Director(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nume, String date) {
        int 처리값 = 예제경로(Nume); if (처리값 < 0) return 처리값;
        int Fișier = Memorie_Fișiere.Deschide(193); if (Fișier == -17) return 0; if (Fișier < 0) return Fișier;
        for (int Loop_INDEX = 0; Loop_INDEX < date.length(); Loop_INDEX += 2) {
            처리값 = Memorie_Fișiere.Scriere(Fișier, hexadecimal_VALUE(date.charAt(Loop_INDEX)) * 16 + hexadecimal_VALUE(date.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memorie_Fișiere.Închide(Fișier); return 처리값; }
        }
        return Memorie_Fișiere.Închide(Fișier);
    }
    static void afișa_ajutor() {
        sistem_instrument.afișa_ajutor();
        단말.Scriere("sshd / securizat_shell start|stop|status: SSH :22 (user, 장치별 parolă_VALUE)\n");
        단말.Scriere("vncd / la_distanță_afișa start|stop|status: VNC :5900 (장치별 parolă_VALUE)\n");
        단말.Scriere("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Scriere("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Scriere("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Scriere("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Scriere("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Scriere("모서리 + 왼쪽 버튼 glisa_VALUE: Terminal Mărime schimba_VALUE; terminal size: COLUMN_VALUE/ROW_VALUE\n");
        단말.Scriere("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Scriere("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Scriere("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Scriere("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Scriere("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Scriere("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Scriere("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Scriere("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Scriere("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Scriere("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Scriere("pip: MicroPython sursă_arborescență instala_VALUE; gazdă --network --pip 필요; /lib는 RAM\n");
        단말.Scriere("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Scriere("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Scriere("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Scriere("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Avizier.Terminal(2) != 0) { Avizier.Terminal(0); 단말.Scriere("TERMINAL CLOSED\n"); }
        else if (Avizier.Terminal(1) < 0) eroare(-19);
        else 단말.Scriere("TERMINAL READY — Română terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Comandă() {
        if (token_COUNT == 0) return;
        if (sistem_instrument.executa_comandă()) return;
        if (같음(0,"sshd") || 같음(0,"securizat_shell") || 같음(0,"vncd") || 같음(0,"la_distanță_afișa")) {
            int 종류=같음(0,"vncd")||같음(0,"la_distanță_afișa")?1:0;
            int Acțiuni=같음(1,"start")||같음(1,"Pornește")?1:같음(1,"stop")||같음(1,"Oprește")?0:2;
            int Stare_VALUE=Avizier.control_la_distanță(종류,Acțiuni);
            if(Stare_VALUE<0)eroare(Stare_VALUE);else 단말.Scriere(Avizier.control_la_distanță(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else afișa_ajutor(); }
        else if (같음(0, "info") || 같음(0, "i")) nucleu.msinfo32_exe();
        else if (같음(0, "pwd")) { Memorie_Fișiere.curent_scriere(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Memorie_Fișiere.cale_buta(1); 처리값 = Memorie_Fișiere.cale_byte(0, '/'); } else 처리값 = token_COUNT == 2 ? Cale(1) : -22;
            if (처리값 >= 0) 처리값 = Memorie_Fișiere.schimba_Director(); if (처리값 < 0) eroare(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argument_INDEX) { Memorie_Fișiere.cale_buta(1); 처리값 = Memorie_Fișiere.cale_byte(0, '.'); } else 처리값 = token_COUNT == argument_INDEX + 1 ? Cale(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memorie_Fișiere.경로목록(); if (처리값 < 0) eroare(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) shell_Instrumente.Fișier_caz(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) shell_Instrumente.copia_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) shell_Instrumente.vizualiza_VALUE();
        else if (같음(0, "wc")) shell_Instrumente.세기();
        else if (같음(0, "grep")) shell_Instrumente.FIND_intrare();
        else if (같음(0, "head") || 같음(0, "tail")) shell_Instrumente.머리(같음(0, "tail"));
        else if (같음(0, "tee")) shell_Instrumente.scriere_Împreună();
        else if (같음(0, "env")) shell_sintaxă.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) shell_sintaxă.환경보기();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = shell_sintaxă.환경설정(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { KR = 처리값; 단말.Scriere("Comandă analiza_VALUE: variabilă_VALUE 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) shell_sintaxă.executa_Fișier();
        else if (같음(0, "true")) KR = 0;
        else if (같음(0, "false")) KR = 1;
        else if (같음(0, "history")) editor_de_linii.afișa_LOG();
        else if (같음(0, "exit")) {
            if (shell_sintaxă.깊이 > 0) { KR = token_COUNT == 1 ? shell_sintaxă.Stare_VALUE : shell_Instrumente.cifră_VALUE(1); if (KR < 0 || KR > 255) KR = 2; shell_sintaxă.script_termina_un_apel = true; }
            else if (Avizier.Terminal(2) != 0) Terminal(true);
            else 단말.Scriere("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) edita_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { KR = 2; 단말.Scriere("사용법: rm Fișier...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = Cale(Loop_INDEX); if (처리값 == 0) 처리값 = Memorie_Fișiere.șterge_intrare(); if (처리값 < 0) eroare(처리값); }
        }
        else if (같음(0, "echo")) {
            int buta_poziție = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = buta_poziție; 첫값 < token_COUNT; 첫값++) { if (첫값 > buta_poziție) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < lungime_VALUE[첫값]; Loop_INDEX++) Avizier.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (buta_poziție == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Scriere("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_set() : Instrumente(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !shell_sintaxă.연결중) { 단말.Scriere("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Instrumente(13); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Instrumente(15); KR = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxă.연결중) { 단말.Scriere("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Instrumente(16); KR = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaxă.연결중) { 단말.Scriere("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Mărime = Avizier.Terminal(13); 단말.Scriere("TERMINAL SIZE "); 단말.수(Mărime & 65535); 단말.문자('x'); 단말.수(Mărime >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Avizier.Terminal(9); desktop.executa_comandă(); }
        else if (같음(0, "c")) nucleu.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) nucleu.작업시험();
        else if (같음(0, "g")) nucleu.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) nucleu.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Avizier.rula_utilizator_program(0); if (처리값 == 0) 단말.Scriere("ELF DEMO PASS\n"); else eroare(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? instrument_intrare(-2, 2) : Instrumente(-1); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !shell_sintaxă.연결중) { 단말.Scriere("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) nucleu.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Avizier.transfer_de_fișiere_serviciu(1); if (처리값 < 0) eroare(처리값); else { 단말.Scriere("FTP listening "); sistem_instrument.scriere_adresa(Avizier.rețea_stare(0,0)); 단말.Scriere(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Avizier.transfer_de_fișiere_serviciu(0); 단말.Scriere("FTP stopped\n"); }
            else 단말.Scriere(Avizier.transfer_de_fișiere_serviciu(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { set.Pregătiți(); 단말.Scriere("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Limbi_străine = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Limbi_străine < 0) 단말.Scriere("example java|c|python: Rezultat, Fișier, 네트워크, 그래픽, Java Swing Fereastră 예제\n");
            else { int 처리값 = 예제꾸러미.instala_VALUE(Limbi_străine); if (처리값 < 0) { eroare(처리값); if (처리값 == -28) 단말.Scriere("RAM full: remove unused files, then retry example\n"); } else 단말.Scriere("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = executare_format();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = instrument_intrare(format_VALUE == 1 ? -1 : 14, 0); KR = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !shell_sintaxă.연결중) { 단말.Scriere("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { KR = 126; 단말.Scriere("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { KR = 127; 단말.Scriere("Unknown command. help: commands\n"); }
        }
    }
    public static void executa_comandă() {
        set.Pregătiți();
        for (int Limbi_străine = 0; Limbi_străine < 3; Limbi_străine++) { int 처리값 = 예제꾸러미.instala_VALUE(Limbi_străine); if (처리값 < 0) eroare(처리값); }
        afișa_ajutor();
        while (true) {
            fereastră_sesiune.Proces_VALUE_intrare(); if (fereastră_sesiune.CV_executare()) continue;
            if (!fereastră_sesiune.이어읽기) 단말.Scriere("jkoros-native> "); editor_de_linii.linie_de_comandă = true; Avizier.원격대기(1); int Mărime = 줄읽기(); Avizier.원격대기(0); editor_de_linii.linie_de_comandă = false;
            if (Mărime == -3) continue;
            if (Mărime == -2) 단말.Scriere("Comandă analiza_VALUE: 명령줄이 너무 깁니다\n");
            if (Mărime >= 0) { shell_sintaxă.script_termina_un_apel = false; shell_sintaxă.executa_comandă(Linie, 0, Mărime, 0); } else shell_sintaxă.Stare_VALUE = 130;
            Avizier.termina_un_apel_la_distanță_comandă(shell_sintaxă.Stare_VALUE);
            editor_de_linii.Mărime = editor_de_linii.cursor_VALUE = editor_de_linii.buta_fereastră = 0;
        }
    }
}
