// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 kommandorad. Citat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] inmatningsrad = new int[4096], kod_värde = new int[4096], 시작점 = new int[32], längd_värde = new int[32];
    static int[] Redigerat_Innehåll = new int[16384], ändring_namn = new int[63];
    static int kod_ANTAL, ändring_namn_längd, RESULTAT;
    static boolean Föregående_rad;
    static void 원바이트(int värde) { Tavla.직렬쓰기(värde); }
    static int läs_inmatningsrad() { return radredigerare.Läs(); }
    static boolean 나누기(int Storlek) {
        int position = 0, 끝 = 0; kod_ANTAL = 0;
        while (position < Storlek) {
            while (position < Storlek && (inmatningsrad[position] == 32 || inmatningsrad[position] == 9)) position++;
            if (position == Storlek) break;
            if (kod_ANTAL == 16) { 단말.Skriv("kommando parsa_värde: 인수가 너무 많습니다\n"); return false; }
            시작점[kod_ANTAL] = 끝; int Citat_värde = 0;
            while (position < Storlek) {
                int värde = inmatningsrad[position++];
                if (Citat_värde == 0 && (värde == 32 || värde == 9)) break;
                if (värde == Citat_värde) { Citat_värde = 0; continue; }
                if (Citat_värde == 0 && (värde == 39 || värde == 34)) { Citat_värde = värde; continue; }
                kod_värde[끝++] = värde;
            }
            if (Citat_värde != 0) { 단말.Skriv("kommando parsa_värde: 따옴표가 닫히지 않았습니다\n"); return false; }
            längd_värde[kod_ANTAL] = 끝 - 시작점[kod_ANTAL]; kod_ANTAL++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Ord_SMS) {
        if (INDEX >= kod_ANTAL) return false;
        int positionsindex=0;
        for (int 순번=0; 순번<Ord_SMS.length(); 순번++) {
            int kodpunkt=Ord_SMS.charAt(순번);
            if (kodpunkt>=0xd800 && kodpunkt<=0xdbff && 순번+1<Ord_SMS.length()) kodpunkt=0x10000+((kodpunkt-0xd800)<<10)+Ord_SMS.charAt(++순번)-0xdc00;
            int byte_ANTAL=kodpunkt<128?1:kodpunkt<2048?2:kodpunkt<65536?3:4;
            for (int SEKVENS_värde=byte_ANTAL-1; SEKVENS_värde>=0; SEKVENS_värde--) {
                int värde=byte_ANTAL==1?kodpunkt:SEKVENS_värde==byte_ANTAL-1?(byte_ANTAL==2?0xc0:byte_ANTAL==3?0xe0:0xf0)|(kodpunkt>>(6*SEKVENS_värde)):0x80|((kodpunkt>>(6*SEKVENS_värde))&63);
                if (positionsindex>=längd_värde[INDEX] || kod_värde[시작점[INDEX]+positionsindex++]!=värde) return false;
            }
        }
        return positionsindex==längd_värde[INDEX];
    }
    static int sökväg_2(int INDEX) {
        if (INDEX >= kod_ANTAL) return -22;
        int RESULTAT = Minne_Filer.väg_START(längd_värde[INDEX]); if (RESULTAT < 0) return RESULTAT;
        for (int Loop_INDEX = 0; Loop_INDEX < längd_värde[INDEX]; Loop_INDEX++) {
            RESULTAT = Minne_Filer.väg_byte(Loop_INDEX, kod_värde[시작점[INDEX] + Loop_INDEX]); if (RESULTAT < 0) return RESULTAT;
        }
        return 0;
    }
    static void fel(int INDEX) { RESULTAT = 1; 단말.Skriv("fel "); 단말.nummer(INDEX); 단말.문자(10); }
    static void vy_värde() {
        if (kod_ANTAL != 2) { 단말.Skriv("사용법: cat filnamn\n"); return; }
        int RESULTAT = sökväg_2(1); if (RESULTAT < 0) { fel(RESULTAT); return; }
        int filnamn = Minne_Filer.Öppna(0); if (filnamn < 0) { fel(filnamn); return; }
        while (true) { int värde = Minne_Filer.Läs(filnamn); if (värde == 256) break; if (värde < 0) { fel(värde); break; } 원바이트(värde); }
        Minne_Filer.Stäng(filnamn); 단말.문자(10);
    }
    static void ändring_värde() {
        if (kod_ANTAL != 2) { 단말.Skriv("사용법: edit filnamn\n"); return; }
        int RESULTAT = sökväg_2(1); if (RESULTAT < 0) { fel(RESULTAT); return; }
        ändring_namn_längd = längd_värde[1];
        for (int Loop_INDEX = 0; Loop_INDEX < ändring_namn_längd; Loop_INDEX++) ändring_namn[Loop_INDEX] = kod_värde[시작점[1] + Loop_INDEX];
        단말.Skriv("EDIT: filnamn 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Storlek = 0;
        while (true) {
            단말.Skriv("edit> "); int indata_värde = läs_inmatningsrad();
            if (indata_värde < 0) { 단말.Skriv("EDIT CANCELLED\n"); return; }
            if (indata_värde == 1 && inmatningsrad[0] == '.') break;
            if (indata_värde + 1 > Redigerat_Innehåll.length - Storlek) { 단말.Skriv("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < indata_värde; Loop_INDEX++) Redigerat_Innehåll[Storlek++] = inmatningsrad[Loop_INDEX];
            Redigerat_Innehåll[Storlek++] = 10;
        }
        Minne_Filer.väg_START(ändring_namn_längd);
        for (int Loop_INDEX = 0; Loop_INDEX < ändring_namn_längd; Loop_INDEX++) Minne_Filer.väg_byte(Loop_INDEX, ändring_namn[Loop_INDEX]);
        int filnamn = Minne_Filer.Öppna(577); if (filnamn < 0) { fel(filnamn); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Storlek; Loop_INDEX++) Minne_Filer.Skriv(filnamn, Redigerat_Innehåll[Loop_INDEX]);
        Minne_Filer.Stäng(filnamn); 단말.Skriv("SAVED "); 단말.nummer(Storlek); 단말.Skriv("byte_värde(주기억 filnamn)\n");
    }
    static int hex_värde(int värde) {
        if (värde >= '0' && värde <= '9') return värde - '0';
        if (värde >= 'a' && värde <= 'f') return värde - 'a' + 10;
        if (värde >= 'A' && värde <= 'F') return värde - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (kod_ANTAL != 2) { 단말.Skriv("사용법: load filnamn | hex filnamn\n"); return; }
        int RESULTAT = sökväg_2(1); if (RESULTAT < 0) { fel(RESULTAT); return; }
        if (!넣기) {
            int filnamn = Minne_Filer.Öppna(0); if (filnamn < 0) { fel(filnamn); return; }
            단말.Skriv("HEX BEGIN "); 단말.nummer(Minne_Filer.Storlek(filnamn)); 단말.문자(10);
            int post_ANTAL = 0;
            while (true) {
                int värde = Minne_Filer.Läs(filnamn); if (värde < 0 || värde == 256) break;
                단말.문자("0123456789abcdef".charAt(värde >> 4)); 단말.문자("0123456789abcdef".charAt(värde & 15));
                if (++post_ANTAL % 32 == 0) 단말.문자(10);
            }
            if (post_ANTAL % 32 != 0) 단말.문자(10);
            Minne_Filer.Stäng(filnamn); 단말.Skriv("HEX END\n"); return;
        }
        ändring_namn_längd = längd_värde[1];
        for (int Loop_INDEX = 0; Loop_INDEX < ändring_namn_längd; Loop_INDEX++) ändring_namn[Loop_INDEX] = kod_värde[시작점[1] + Loop_INDEX];
        단말.Skriv("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Storlek = 0;
        while (true) {
            단말.Skriv("hex> "); int indata_värde = läs_inmatningsrad();
            if (indata_värde < 0) { 단말.Skriv("LOAD CANCELLED\n"); return; }
            if (indata_värde == 1 && inmatningsrad[0] == '.') break;
            int framåtvänd_värde = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < indata_värde; Loop_INDEX++) {
                if (inmatningsrad[Loop_INDEX] == 32 || inmatningsrad[Loop_INDEX] == 9) continue;
                int värde = hex_värde(inmatningsrad[Loop_INDEX]);
                if (värde < 0 || Storlek >= Redigerat_Innehåll.length) { 단말.Skriv("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (framåtvänd_värde < 0) framåtvänd_värde = värde; else { Redigerat_Innehåll[Storlek++] = framåtvänd_värde * 16 + värde; framåtvänd_värde = -1; }
            }
            if (framåtvänd_värde >= 0) { 단말.Skriv("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Minne_Filer.väg_START(ändring_namn_längd);
        for (int Loop_INDEX = 0; Loop_INDEX < ändring_namn_längd; Loop_INDEX++) Minne_Filer.väg_byte(Loop_INDEX, ändring_namn[Loop_INDEX]);
        int filnamn = Minne_Filer.Öppna(577); if (filnamn < 0) { fel(filnamn); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Storlek; Loop_INDEX++) Minne_Filer.Skriv(filnamn, Redigerat_Innehåll[Loop_INDEX]);
        Minne_Filer.Stäng(filnamn); 단말.Skriv("LOADED "); 단말.nummer(Storlek); 단말.Skriv("byte_värde(주기억 filnamn)\n");
    }
    static int verktyg(int INDEX) {
        return verktyg_post(INDEX, 1);
    }
    static int verktyg_post(int INDEX, int Kör) {
        if (kod_ANTAL - Kör > 8) return -22;
        Tavla.인수준비(kod_ANTAL - Kör);
        for (int 첫값 = Kör; 첫값 < kod_ANTAL; 첫값++) {
            if (längd_värde[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < längd_värde[첫값]; Loop_INDEX++) Tavla.argument_byte(첫값 - Kör, Loop_INDEX, kod_värde[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Tavla.리눅스파일실행() : INDEX < 0 ? Tavla.köra_användare_fil() : Tavla.köra_användare_app(INDEX);
    }
    static int PYTHON_bunt() {
        if (kod_ANTAL > 8) return -22;
        Tavla.인수준비(kod_ANTAL);
        String sökväg_2 = "/lib/bunt.py";
        // Java 문자열을 셸의 UTF-8 argument 버퍼에 기록한다.
        int positionsindex = 0;
        for (int 순번 = 0; 순번 < sökväg_2.length(); 순번++) {
            int tecken_värde = sökväg_2.charAt(순번);
            if (tecken_värde < 128) Tavla.argument_byte(0, positionsindex++, tecken_värde);
            else { Tavla.argument_byte(0, positionsindex++, 0xe0 | (tecken_värde >> 12)); Tavla.argument_byte(0, positionsindex++, 0x80 | ((tecken_värde >> 6) & 63)); Tavla.argument_byte(0, positionsindex++, 0x80 | (tecken_värde & 63)); }
        }
        for (int 순번 = 1; 순번 < kod_ANTAL; 순번++) {
            if (längd_värde[순번] > 255) return -36;
            for (int tecken_värde = 0; tecken_värde < längd_värde[순번]; tecken_värde++) Tavla.argument_byte(순번, tecken_värde, kod_värde[시작점[순번] + tecken_värde]);
        }
        return Tavla.köra_användare_app(12);
    }
    static int körning_format() {
        int 처리값 = sökväg_2(0); if (처리값 < 0) return 처리값;
        int filnamn = Minne_Filer.Öppna(0); if (filnamn < 0) return filnamn;
        int 첫값 = Minne_Filer.Läs(filnamn), byte_data = Minne_Filer.Läs(filnamn), kodpunkt = Minne_Filer.Läs(filnamn), 뒷값 = Minne_Filer.Läs(filnamn);
        Minne_Filer.Stäng(filnamn);
        if (첫값 == 127 && byte_data == 'E' && kodpunkt == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_data == 'K' && kodpunkt == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String argument) {
        Tavla.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < argument.length(); Loop_INDEX++) Tavla.argument_byte(0, Loop_INDEX, argument.charAt(Loop_INDEX));
        return Tavla.köra_användare_app(INDEX);
    }
    static void SMS_byte(int filnamn, int värde) { Minne_Filer.Skriv(filnamn, värde); }
    static void statisk_fil(String Namn, String Innehåll_värde) {
        // bunt 파일명은 ASCII. filnamn 내용은 UTF-8로 저장한다.
        Minne_Filer.väg_START(Namn.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Namn.length(); Loop_INDEX++) Minne_Filer.väg_byte(Loop_INDEX, Namn.charAt(Loop_INDEX));
        int filnamn = Minne_Filer.Öppna(193); if (filnamn < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Innehåll_värde.length(); Loop_INDEX++) {
            int kodpunkt = Innehåll_värde.charAt(Loop_INDEX);
            if (kodpunkt >= 0xd800 && kodpunkt <= 0xdbff && Loop_INDEX + 1 < Innehåll_värde.length()) kodpunkt = 0x10000 + ((kodpunkt - 0xd800) << 10) + Innehåll_värde.charAt(++Loop_INDEX) - 0xdc00;
            if (kodpunkt < 128) SMS_byte(filnamn, kodpunkt);
            else {
                int nummer = kodpunkt < 2048 ? 2 : kodpunkt < 65536 ? 3 : 4;
                SMS_byte(filnamn, (nummer == 2 ? 0xc0 : nummer == 3 ? 0xe0 : 0xf0) | (kodpunkt >> (6 * (nummer - 1))));
                for (int post_ANTAL = nummer - 1; post_ANTAL > 0; post_ANTAL--) SMS_byte(filnamn, 0x80 | ((kodpunkt >> (6 * (post_ANTAL - 1))) & 63));
            }
        }
        Minne_Filer.Stäng(filnamn);
    }
    static void 한글도움말() {
        단말.Skriv("F9 eller Shift+Space växlar till svensk inmatning.\n");
        단말.Skriv("  [SV] keyboard; [EN] ASCII\n");
        단말.Skriv("  $ → ¤\n");
        단말.Skriv("  F9: EN ↔ sv | Ctrl+Shift+V: UTF-8\n");
        단말.Skriv("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Skriv("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Namn) {
        int byte_ANTAL = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Namn.length(); Loop_INDEX++) { int kodpunkt = Namn.charAt(Loop_INDEX); if (kodpunkt >= 0xd800 && kodpunkt <= 0xdfff) return -22; byte_ANTAL += kodpunkt < 128 ? 1 : kodpunkt < 2048 ? 2 : 3; }
        int 처리값 = Minne_Filer.väg_START(byte_ANTAL); if (처리값 < 0) return 처리값;
        int positionsindex = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Namn.length(); Loop_INDEX++) {
            int kodpunkt = Namn.charAt(Loop_INDEX);
            if (kodpunkt < 128) Minne_Filer.väg_byte(positionsindex++, kodpunkt);
            else if (kodpunkt < 2048) { Minne_Filer.väg_byte(positionsindex++, 0xc0 | (kodpunkt >> 6)); Minne_Filer.väg_byte(positionsindex++, 0x80 | (kodpunkt & 63)); }
            else { Minne_Filer.väg_byte(positionsindex++, 0xe0 | (kodpunkt >> 12)); Minne_Filer.väg_byte(positionsindex++, 0x80 | ((kodpunkt >> 6) & 63)); Minne_Filer.väg_byte(positionsindex++, 0x80 | (kodpunkt & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Namn) {
        int 처리값 = 예제경로(Namn); if (처리값 < 0) return 처리값;
        처리값 = Minne_Filer.Skapa_Katalog(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Namn, String data) {
        int 처리값 = 예제경로(Namn); if (처리값 < 0) return 처리값;
        int filnamn = Minne_Filer.Öppna(193); if (filnamn == -17) return 0; if (filnamn < 0) return filnamn;
        for (int Loop_INDEX = 0; Loop_INDEX < data.length(); Loop_INDEX += 2) {
            처리값 = Minne_Filer.Skriv(filnamn, hex_värde(data.charAt(Loop_INDEX)) * 16 + hex_värde(data.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Minne_Filer.Stäng(filnamn); return 처리값; }
        }
        return Minne_Filer.Stäng(filnamn);
    }
    static void visa_hjälp() {
        System_verktyg.visa_hjälp();
        단말.Skriv("sshd / säker_Shell start|stop|status: SSH :22 (user, 장치별 lösenord_värde)\n");
        단말.Skriv("vncd / fjärr_visa start|stop|status: VNC :5900 (장치별 lösenord_värde)\n");
        단말.Skriv("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Skriv("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Skriv("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Skriv("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Skriv("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Skriv("모서리 + 왼쪽 버튼 dra_värde: kommandotolk Storlek ändra_värde; terminal size: spalt_värde/RAD_värde\n");
        단말.Skriv("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Skriv("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Skriv("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Skriv("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Skriv("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Skriv("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Skriv("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Skriv("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Skriv("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Skriv("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Skriv("pip: MicroPython källa_träd installera_värde; värd --network --pip 필요; /lib는 RAM\n");
        단말.Skriv("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Skriv("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Skriv("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Skriv("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void kommandotolk(boolean 전환여부) {
        if (전환여부 && Tavla.kommandotolk(2) != 0) { Tavla.kommandotolk(0); 단말.Skriv("TERMINAL CLOSED\n"); }
        else if (Tavla.kommandotolk(1) < 0) fel(-19);
        else 단말.Skriv("TERMINAL READY — sv terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void kommando() {
        if (kod_ANTAL == 0) return;
        if (System_verktyg.köra_kommando()) return;
        if (같음(0,"sshd") || 같음(0,"säker_Shell") || 같음(0,"vncd") || 같음(0,"fjärr_visa")) {
            int variant_värde=같음(0,"vncd")||같음(0,"fjärr_visa")?1:0;
            int Åtgärd=같음(1,"start")||같음(1,"Kör")?1:같음(1,"stop")||같음(1,"Stopp")?0:2;
            int status_värde=Tavla.skuggning(variant_värde,Åtgärd);
            if(status_värde<0)fel(status_värde);else 단말.Skriv(Tavla.skuggning(variant_värde,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else visa_hjälp(); }
        else if (같음(0, "info") || 같음(0, "i")) kärna.msinfo32_exe();
        else if (같음(0, "pwd")) { Minne_Filer.aktuellt_skriva(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (kod_ANTAL == 1) { Minne_Filer.väg_START(1); 처리값 = Minne_Filer.väg_byte(0, '/'); } else 처리값 = kod_ANTAL == 2 ? sökväg_2(1) : -22;
            if (처리값 >= 0) 처리값 = Minne_Filer.ändra_Katalog(); if (처리값 < 0) fel(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (kod_ANTAL == argument_INDEX) { Minne_Filer.väg_START(1); 처리값 = Minne_Filer.väg_byte(0, '.'); } else 처리값 = kod_ANTAL == argument_INDEX + 1 ? sökväg_2(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Minne_Filer.경로목록(); if (처리값 < 0) fel(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) Shell_Verktyg.fil_Jobb(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) Shell_Verktyg.kopia_värde(같음(0, "mv"));
        else if (같음(0, "cat")) Shell_Verktyg.vy_värde();
        else if (같음(0, "wc")) Shell_Verktyg.세기();
        else if (같음(0, "grep")) Shell_Verktyg.Sök_post();
        else if (같음(0, "head") || 같음(0, "tail")) Shell_Verktyg.머리(같음(0, "tail"));
        else if (같음(0, "tee")) Shell_Verktyg.skriva_Tillsammans();
        else if (같음(0, "env")) Shell_syntax.visa_miljö();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (kod_ANTAL == 1) Shell_syntax.visa_miljö();
            for (int Loop_INDEX = 1; Loop_INDEX < kod_ANTAL; Loop_INDEX++) { int 처리값 = Shell_syntax.miljö_Inställningar(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { RESULTAT = 처리값; 단말.Skriv("kommando parsa_värde: variabel_värde 이름이 잘못되었거나 예약된 이름이거나 miljö 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) Shell_syntax.köra_fil();
        else if (같음(0, "true")) RESULTAT = 0;
        else if (같음(0, "false")) RESULTAT = 1;
        else if (같음(0, "history")) radredigerare.visa_LOG();
        else if (같음(0, "exit")) {
            if (Shell_syntax.깊이 > 0) { RESULTAT = kod_ANTAL == 1 ? Shell_syntax.status_värde : Shell_Verktyg.siffra_värde(1); if (RESULTAT < 0 || RESULTAT > 255) RESULTAT = 2; Shell_syntax.skript_avsluta = true; }
            else if (Tavla.kommandotolk(2) != 0) kommandotolk(true);
            else 단말.Skriv("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) ändring_värde();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (kod_ANTAL < 2) { RESULTAT = 2; 단말.Skriv("사용법: rm filnamn...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < kod_ANTAL; Loop_INDEX++) { int 처리값 = sökväg_2(Loop_INDEX); if (처리값 == 0) 처리값 = Minne_Filer.radera_post(); if (처리값 < 0) fel(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_placera = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_placera; 첫값 < kod_ANTAL; 첫값++) { if (첫값 > START_placera) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < längd_värde[첫값]; Loop_INDEX++) Tavla.직렬쓰기(kod_värde[시작점[첫값] + Loop_INDEX]); }
            if (START_placera == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Skriv("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_bunt() : verktyg(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); RESULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !Shell_syntax.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = verktyg(13); RESULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = verktyg(15); RESULTAT = 처리값 < 0 ? 126 : 처리값; if (!Shell_syntax.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = verktyg(16); RESULTAT = 처리값 < 0 ? 126 : 처리값; if (!Shell_syntax.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Storlek = Tavla.kommandotolk(13); 단말.Skriv("TERMINAL SIZE "); 단말.nummer(Storlek & 65535); 단말.문자('x'); 단말.nummer(Storlek >>> 16); 단말.문자(10); }
            else kommandotolk(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Tavla.kommandotolk(9); Dator.köra_kommando(); }
        else if (같음(0, "c")) kärna.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) kärna.test_Tasks();
        else if (같음(0, "g")) kärna.skärmbild();
        else if (같음(0, "selftest") || 같음(0, "u")) kärna.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Tavla.köra_användare_app(0); if (처리값 == 0) 단말.Skriv("ELF DEMO PASS\n"); else fel(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? verktyg_post(-2, 2) : verktyg(-1); RESULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !Shell_syntax.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kärna.test_Nätverk();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Tavla.filöverföring_tjänst(1); if (처리값 < 0) fel(처리값); else { 단말.Skriv("FTP listening "); System_verktyg.skriva_ADRESS(Tavla.nätverk_status(0,0)); 단말.Skriv(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Tavla.filöverföring_tjänst(0); 단말.Skriv("FTP stopped\n"); }
            else 단말.Skriv(Tavla.filöverföring_tjänst(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { bunt.Förbereda(); 단말.Skriv("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Språk = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (kod_ANTAL != 2 || Språk < 0) 단말.Skriv("example java|c|python: utmatningsposition, filnamn, 네트워크, 그래픽, Java Swing Fönster 예제\n");
            else { int 처리값 = 예제꾸러미.installera_värde(Språk); if (처리값 < 0) { fel(처리값); if (처리값 == -28) 단말.Skriv("RAM full: remove unused files, then retry example\n"); } else 단말.Skriv("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_värde = körning_format();
            if (format_värde == 1 || format_värde == 2) {
                int 처리값 = verktyg_post(format_värde == 1 ? -1 : 14, 0); RESULTAT = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !Shell_syntax.연결중) { 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); }
            } else if (format_värde == 0) { RESULTAT = 126; 단말.Skriv("실행할 nummer 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { RESULTAT = 127; 단말.Skriv("Unknown command. help: commands\n"); }
        }
    }
    public static void köra_kommando() {
        bunt.Förbereda();
        for (int Språk = 0; Språk < 3; Språk++) { int 처리값 = 예제꾸러미.installera_värde(Språk); if (처리값 < 0) fel(처리값); }
        visa_hjälp();
        while (true) {
            fönster_session.Process_värde_post(); if (fönster_session.CV_körning()) continue;
            if (!fönster_session.이어읽기) 단말.Skriv("jkoros-native> "); radredigerare.kommandorad = true; Tavla.fjärr_vänta(1); int Storlek = läs_inmatningsrad(); Tavla.fjärr_vänta(0); radredigerare.kommandorad = false;
            if (Storlek == -3) continue;
            if (Storlek == -2) 단말.Skriv("kommando parsa_värde: 명령줄이 너무 깁니다\n");
            if (Storlek >= 0) { Shell_syntax.skript_avsluta = false; Shell_syntax.köra_kommando(inmatningsrad, 0, Storlek, 0); } else Shell_syntax.status_värde = 130;
            Tavla.avsluta_fjärr_kommando(Shell_syntax.status_värde);
            radredigerare.Storlek = radredigerare.markör_värde_04ee3e20 = radredigerare.START_fönster = 0;
        }
    }
}
