// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 opdrachtregel. Citaat, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class Opdrachtvertolker {
    static int[] invoerregel = new int[4096], token_WAARDE = new int[4096], 시작점 = new int[32], tijdsduur_WAARDE = new int[32];
    static int[] Bewerkt_Inhoud = new int[16384], Bewerk_naam = new int[63];
    static int token_AANTAL, Bewerk_naam_tijdsduur, resultaat;
    static boolean Vorige_lijn;
    static void 원바이트(int WAARDE) { Bord.직렬쓰기(WAARDE); }
    static int invoerregel_lezen() { return regeleditor.Lezen(); }
    static boolean 나누기(int Grootte) {
        int positie = 0, 끝 = 0; token_AANTAL = 0;
        while (positie < Grootte) {
            while (positie < Grootte && (invoerregel[positie] == 32 || invoerregel[positie] == 9)) positie++;
            if (positie == Grootte) break;
            if (token_AANTAL == 16) { 단말.Schrijven("opdracht parseren_WAARDE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_AANTAL] = 끝; int Citaat_WAARDE = 0;
            while (positie < Grootte) {
                int WAARDE = invoerregel[positie++];
                if (Citaat_WAARDE == 0 && (WAARDE == 32 || WAARDE == 9)) break;
                if (WAARDE == Citaat_WAARDE) { Citaat_WAARDE = 0; continue; }
                if (Citaat_WAARDE == 0 && (WAARDE == 39 || WAARDE == 34)) { Citaat_WAARDE = WAARDE; continue; }
                token_WAARDE[끝++] = WAARDE;
            }
            if (Citaat_WAARDE != 0) { 단말.Schrijven("opdracht parseren_WAARDE: 따옴표가 닫히지 않았습니다\n"); return false; }
            tijdsduur_WAARDE[token_AANTAL] = 끝 - 시작점[token_AANTAL]; token_AANTAL++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_sms) {
        if (INDEX >= token_AANTAL) return false;
        int plaatsingsindex=0;
        for (int 순번=0; 순번<Word_sms.length(); 순번++) {
            int codepoint=Word_sms.charAt(순번);
            if (codepoint>=0xd800 && codepoint<=0xdbff && 순번+1<Word_sms.length()) codepoint=0x10000+((codepoint-0xd800)<<10)+Word_sms.charAt(++순번)-0xdc00;
            int byte_AANTAL=codepoint<128?1:codepoint<2048?2:codepoint<65536?3:4;
            for (int REEKS_WAARDE=byte_AANTAL-1; REEKS_WAARDE>=0; REEKS_WAARDE--) {
                int WAARDE=byte_AANTAL==1?codepoint:REEKS_WAARDE==byte_AANTAL-1?(byte_AANTAL==2?0xc0:byte_AANTAL==3?0xe0:0xf0)|(codepoint>>(6*REEKS_WAARDE)):0x80|((codepoint>>(6*REEKS_WAARDE))&63);
                if (plaatsingsindex>=tijdsduur_WAARDE[INDEX] || token_WAARDE[시작점[INDEX]+plaatsingsindex++]!=WAARDE) return false;
            }
        }
        return plaatsingsindex==tijdsduur_WAARDE[INDEX];
    }
    static int pad(int INDEX) {
        if (INDEX >= token_AANTAL) return -22;
        int resultaat = GeheugenBestanden.pad_START(tijdsduur_WAARDE[INDEX]); if (resultaat < 0) return resultaat;
        for (int lus_INDEX = 0; lus_INDEX < tijdsduur_WAARDE[INDEX]; lus_INDEX++) {
            resultaat = GeheugenBestanden.pad_byte(lus_INDEX, token_WAARDE[시작점[INDEX] + lus_INDEX]); if (resultaat < 0) return resultaat;
        }
        return 0;
    }
    static void fout(int INDEX) { resultaat = 1; 단말.Schrijven("fout "); 단말.nummer(INDEX); 단말.문자(10); }
    static void Weergave_WAARDE() {
        if (token_AANTAL != 2) { 단말.Schrijven("사용법: cat bestand\n"); return; }
        int resultaat = pad(1); if (resultaat < 0) { fout(resultaat); return; }
        int bestand = GeheugenBestanden.Openen(0); if (bestand < 0) { fout(bestand); return; }
        while (true) { int WAARDE = GeheugenBestanden.Lezen(bestand); if (WAARDE == 256) break; if (WAARDE < 0) { fout(WAARDE); break; } 원바이트(WAARDE); }
        GeheugenBestanden.Sluiten(bestand); 단말.문자(10);
    }
    static void Bewerk_WAARDE() {
        if (token_AANTAL != 2) { 단말.Schrijven("사용법: edit bestand\n"); return; }
        int resultaat = pad(1); if (resultaat < 0) { fout(resultaat); return; }
        Bewerk_naam_tijdsduur = tijdsduur_WAARDE[1];
        for (int lus_INDEX = 0; lus_INDEX < Bewerk_naam_tijdsduur; lus_INDEX++) Bewerk_naam[lus_INDEX] = token_WAARDE[시작점[1] + lus_INDEX];
        단말.Schrijven("EDIT: bestand 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Grootte = 0;
        while (true) {
            단말.Schrijven("edit> "); int invoer_WAARDE = invoerregel_lezen();
            if (invoer_WAARDE < 0) { 단말.Schrijven("EDIT CANCELLED\n"); return; }
            if (invoer_WAARDE == 1 && invoerregel[0] == '.') break;
            if (invoer_WAARDE + 1 > Bewerkt_Inhoud.length - Grootte) { 단말.Schrijven("EDIT CANCELLED: file too large\n"); return; }
            for (int lus_INDEX = 0; lus_INDEX < invoer_WAARDE; lus_INDEX++) Bewerkt_Inhoud[Grootte++] = invoerregel[lus_INDEX];
            Bewerkt_Inhoud[Grootte++] = 10;
        }
        GeheugenBestanden.pad_START(Bewerk_naam_tijdsduur);
        for (int lus_INDEX = 0; lus_INDEX < Bewerk_naam_tijdsduur; lus_INDEX++) GeheugenBestanden.pad_byte(lus_INDEX, Bewerk_naam[lus_INDEX]);
        int bestand = GeheugenBestanden.Openen(577); if (bestand < 0) { fout(bestand); return; }
        for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) GeheugenBestanden.Schrijven(bestand, Bewerkt_Inhoud[lus_INDEX]);
        GeheugenBestanden.Sluiten(bestand); 단말.Schrijven("SAVED "); 단말.nummer(Grootte); 단말.Schrijven("byte_WAARDE(주기억 bestand)\n");
    }
    static int hexadecimaal_WAARDE(int WAARDE) {
        if (WAARDE >= '0' && WAARDE <= '9') return WAARDE - '0';
        if (WAARDE >= 'a' && WAARDE <= 'f') return WAARDE - 'a' + 10;
        if (WAARDE >= 'A' && WAARDE <= 'F') return WAARDE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_AANTAL != 2) { 단말.Schrijven("사용법: load bestand | hex bestand\n"); return; }
        int resultaat = pad(1); if (resultaat < 0) { fout(resultaat); return; }
        if (!넣기) {
            int bestand = GeheugenBestanden.Openen(0); if (bestand < 0) { fout(bestand); return; }
            단말.Schrijven("HEX BEGIN "); 단말.nummer(GeheugenBestanden.Grootte(bestand)); 단말.문자(10);
            int invoer_AANTAL_8f7753a1 = 0;
            while (true) {
                int WAARDE = GeheugenBestanden.Lezen(bestand); if (WAARDE < 0 || WAARDE == 256) break;
                단말.문자("0123456789abcdef".charAt(WAARDE >> 4)); 단말.문자("0123456789abcdef".charAt(WAARDE & 15));
                if (++invoer_AANTAL_8f7753a1 % 32 == 0) 단말.문자(10);
            }
            if (invoer_AANTAL_8f7753a1 % 32 != 0) 단말.문자(10);
            GeheugenBestanden.Sluiten(bestand); 단말.Schrijven("HEX END\n"); return;
        }
        Bewerk_naam_tijdsduur = tijdsduur_WAARDE[1];
        for (int lus_INDEX = 0; lus_INDEX < Bewerk_naam_tijdsduur; lus_INDEX++) Bewerk_naam[lus_INDEX] = token_WAARDE[시작점[1] + lus_INDEX];
        단말.Schrijven("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Grootte = 0;
        while (true) {
            단말.Schrijven("hex> "); int invoer_WAARDE = invoerregel_lezen();
            if (invoer_WAARDE < 0) { 단말.Schrijven("LOAD CANCELLED\n"); return; }
            if (invoer_WAARDE == 1 && invoerregel[0] == '.') break;
            int voorkant_WAARDE = -1;
            for (int lus_INDEX = 0; lus_INDEX < invoer_WAARDE; lus_INDEX++) {
                if (invoerregel[lus_INDEX] == 32 || invoerregel[lus_INDEX] == 9) continue;
                int WAARDE = hexadecimaal_WAARDE(invoerregel[lus_INDEX]);
                if (WAARDE < 0 || Grootte >= Bewerkt_Inhoud.length) { 단말.Schrijven("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (voorkant_WAARDE < 0) voorkant_WAARDE = WAARDE; else { Bewerkt_Inhoud[Grootte++] = voorkant_WAARDE * 16 + WAARDE; voorkant_WAARDE = -1; }
            }
            if (voorkant_WAARDE >= 0) { 단말.Schrijven("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        GeheugenBestanden.pad_START(Bewerk_naam_tijdsduur);
        for (int lus_INDEX = 0; lus_INDEX < Bewerk_naam_tijdsduur; lus_INDEX++) GeheugenBestanden.pad_byte(lus_INDEX, Bewerk_naam[lus_INDEX]);
        int bestand = GeheugenBestanden.Openen(577); if (bestand < 0) { fout(bestand); return; }
        for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) GeheugenBestanden.Schrijven(bestand, Bewerkt_Inhoud[lus_INDEX]);
        GeheugenBestanden.Sluiten(bestand); 단말.Schrijven("LOADED "); 단말.nummer(Grootte); 단말.Schrijven("byte_WAARDE(주기억 bestand)\n");
    }
    static int hulpmiddelen(int INDEX) {
        return hulpmiddel_invoer(INDEX, 1);
    }
    static int hulpmiddel_invoer(int INDEX, int starten) {
        if (token_AANTAL - starten > 8) return -22;
        Bord.인수준비(token_AANTAL - starten);
        for (int 첫값 = starten; 첫값 < token_AANTAL; 첫값++) {
            if (tijdsduur_WAARDE[첫값] > 255) return -36;
            for (int lus_INDEX = 0; lus_INDEX < tijdsduur_WAARDE[첫값]; lus_INDEX++) Bord.argument_byte(첫값 - starten, lus_INDEX, token_WAARDE[시작점[첫값] + lus_INDEX]);
        }
        return INDEX == -2 ? Bord.리눅스파일실행() : INDEX < 0 ? Bord.Uitvoeren_gebruiker_Bestand() : Bord.uitvoeren_gebruiker_app(INDEX);
    }
    static int PYTHON_bundel() {
        if (token_AANTAL > 8) return -22;
        Bord.인수준비(token_AANTAL);
        String pad = "/lib/bundel.py";
        // Java 문자열을 셸의 UTF-8 argumenten 버퍼에 기록한다.
        int plaatsingsindex = 0;
        for (int 순번 = 0; 순번 < pad.length(); 순번++) {
            int teken_WAARDE = pad.charAt(순번);
            if (teken_WAARDE < 128) Bord.argument_byte(0, plaatsingsindex++, teken_WAARDE);
            else { Bord.argument_byte(0, plaatsingsindex++, 0xe0 | (teken_WAARDE >> 12)); Bord.argument_byte(0, plaatsingsindex++, 0x80 | ((teken_WAARDE >> 6) & 63)); Bord.argument_byte(0, plaatsingsindex++, 0x80 | (teken_WAARDE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_AANTAL; 순번++) {
            if (tijdsduur_WAARDE[순번] > 255) return -36;
            for (int teken_WAARDE = 0; teken_WAARDE < tijdsduur_WAARDE[순번]; teken_WAARDE++) Bord.argument_byte(순번, teken_WAARDE, token_WAARDE[시작점[순번] + teken_WAARDE]);
        }
        return Bord.uitvoeren_gebruiker_app(12);
    }
    static int uitvoerbewerking_opmaak() {
        int 처리값 = pad(0); if (처리값 < 0) return 처리값;
        int bestand = GeheugenBestanden.Openen(0); if (bestand < 0) return bestand;
        int 첫값 = GeheugenBestanden.Lezen(bestand), byte_gegevens = GeheugenBestanden.Lezen(bestand), codepoint = GeheugenBestanden.Lezen(bestand), navolgend_WAARDE = GeheugenBestanden.Lezen(bestand);
        GeheugenBestanden.Sluiten(bestand);
        if (첫값 == 127 && byte_gegevens == 'E' && codepoint == 'L' && navolgend_WAARDE == 'F') return 1;
        if (첫값 == 'P' && byte_gegevens == 'K' && codepoint == 3 && navolgend_WAARDE == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String argumenten) {
        Bord.인수준비(1);
        for (int lus_INDEX = 0; lus_INDEX < argumenten.length(); lus_INDEX++) Bord.argument_byte(0, lus_INDEX, argumenten.charAt(lus_INDEX));
        return Bord.uitvoeren_gebruiker_app(INDEX);
    }
    static void sms_byte(int bestand, int WAARDE) { GeheugenBestanden.Schrijven(bestand, WAARDE); }
    static void statisch_Bestand(String Naam, String Inhoud_WAARDE) {
        // bundel 파일명은 ASCII. bestand 내용은 UTF-8로 저장한다.
        GeheugenBestanden.pad_START(Naam.length());
        for (int lus_INDEX = 0; lus_INDEX < Naam.length(); lus_INDEX++) GeheugenBestanden.pad_byte(lus_INDEX, Naam.charAt(lus_INDEX));
        int bestand = GeheugenBestanden.Openen(193); if (bestand < 0) return;
        for (int lus_INDEX = 0; lus_INDEX < Inhoud_WAARDE.length(); lus_INDEX++) {
            int codepoint = Inhoud_WAARDE.charAt(lus_INDEX);
            if (codepoint >= 0xd800 && codepoint <= 0xdbff && lus_INDEX + 1 < Inhoud_WAARDE.length()) codepoint = 0x10000 + ((codepoint - 0xd800) << 10) + Inhoud_WAARDE.charAt(++lus_INDEX) - 0xdc00;
            if (codepoint < 128) sms_byte(bestand, codepoint);
            else {
                int nummer = codepoint < 2048 ? 2 : codepoint < 65536 ? 3 : 4;
                sms_byte(bestand, (nummer == 2 ? 0xc0 : nummer == 3 ? 0xe0 : 0xf0) | (codepoint >> (6 * (nummer - 1))));
                for (int invoer_AANTAL_8f7753a1 = nummer - 1; invoer_AANTAL_8f7753a1 > 0; invoer_AANTAL_8f7753a1--) sms_byte(bestand, 0x80 | ((codepoint >> (6 * (invoer_AANTAL_8f7753a1 - 1))) & 63));
            }
        }
        GeheugenBestanden.Sluiten(bestand);
    }
    static void 한글도움말() {
        단말.Schrijven("Met F9 of Shift+Space schakelt u over naar Nederlands typen.\n");
        단말.Schrijven("  [NL] keyboard; [EN] ASCII\n");
        단말.Schrijven("  : → ±\n");
        단말.Schrijven("  F9: EN ↔ nl | Ctrl+Shift+V: UTF-8\n");
        단말.Schrijven("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Schrijven("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Naam) {
        int byte_AANTAL = 0;
        for (int lus_INDEX = 0; lus_INDEX < Naam.length(); lus_INDEX++) { int codepoint = Naam.charAt(lus_INDEX); if (codepoint >= 0xd800 && codepoint <= 0xdfff) return -22; byte_AANTAL += codepoint < 128 ? 1 : codepoint < 2048 ? 2 : 3; }
        int 처리값 = GeheugenBestanden.pad_START(byte_AANTAL); if (처리값 < 0) return 처리값;
        int plaatsingsindex = 0;
        for (int lus_INDEX = 0; lus_INDEX < Naam.length(); lus_INDEX++) {
            int codepoint = Naam.charAt(lus_INDEX);
            if (codepoint < 128) GeheugenBestanden.pad_byte(plaatsingsindex++, codepoint);
            else if (codepoint < 2048) { GeheugenBestanden.pad_byte(plaatsingsindex++, 0xc0 | (codepoint >> 6)); GeheugenBestanden.pad_byte(plaatsingsindex++, 0x80 | (codepoint & 63)); }
            else { GeheugenBestanden.pad_byte(plaatsingsindex++, 0xe0 | (codepoint >> 12)); GeheugenBestanden.pad_byte(plaatsingsindex++, 0x80 | ((codepoint >> 6) & 63)); GeheugenBestanden.pad_byte(plaatsingsindex++, 0x80 | (codepoint & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Naam) {
        int 처리값 = 예제경로(Naam); if (처리값 < 0) return 처리값;
        처리값 = GeheugenBestanden.maken_map(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Naam, String gegevens) {
        int 처리값 = 예제경로(Naam); if (처리값 < 0) return 처리값;
        int bestand = GeheugenBestanden.Openen(193); if (bestand == -17) return 0; if (bestand < 0) return bestand;
        for (int lus_INDEX = 0; lus_INDEX < gegevens.length(); lus_INDEX += 2) {
            처리값 = GeheugenBestanden.Schrijven(bestand, hexadecimaal_WAARDE(gegevens.charAt(lus_INDEX)) * 16 + hexadecimaal_WAARDE(gegevens.charAt(lus_INDEX + 1)));
            if (처리값 < 0) { GeheugenBestanden.Sluiten(bestand); return 처리값; }
        }
        return GeheugenBestanden.Sluiten(bestand);
    }
    static void hulp_tonen() {
        Systeem_hulpmiddel.hulp_tonen();
        단말.Schrijven("sshd / veilig_Shell start|stop|status: SSH :22 (user, 장치별 wachtwoord_WAARDE)\n");
        단말.Schrijven("vncd / extern_weergeven start|stop|status: VNC :5900 (장치별 wachtwoord_WAARDE)\n");
        단말.Schrijven("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Schrijven("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Schrijven("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Schrijven("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Schrijven("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Schrijven("모서리 + 왼쪽 버튼 slepen_WAARDE: terminal Grootte wijzigen_WAARDE; terminal size: KOLOM_WAARDE/RIJ_WAARDE\n");
        단말.Schrijven("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Schrijven("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Schrijven("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Schrijven("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Schrijven("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Schrijven("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Schrijven("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Schrijven("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Schrijven("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Schrijven("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Schrijven("pip: MicroPython bron_structuur installeren_WAARDE; host --network --pip 필요; /lib는 RAM\n");
        단말.Schrijven("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Schrijven("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Schrijven("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Schrijven("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void terminal(boolean 전환여부) {
        if (전환여부 && Bord.terminal(2) != 0) { Bord.terminal(0); 단말.Schrijven("TERMINAL CLOSED\n"); }
        else if (Bord.terminal(1) < 0) fout(-19);
        else 단말.Schrijven("TERMINAL READY — nl terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void opdracht() {
        if (token_AANTAL == 0) return;
        if (Systeem_hulpmiddel.Uitvoeren_opdracht()) return;
        if (같음(0,"sshd") || 같음(0,"veilig_Shell") || 같음(0,"vncd") || 같음(0,"extern_weergeven")) {
            int soort_WAARDE=같음(0,"vncd")||같음(0,"extern_weergeven")?1:0;
            int Actie=같음(1,"start")||같음(1,"starten")?1:같음(1,"stop")||같음(1,"Stoppen")?0:2;
            int Status_WAARDE=Bord.extern_beheer(soort_WAARDE,Actie);
            if(Status_WAARDE<0)fout(Status_WAARDE);else 단말.Schrijven(Bord.extern_beheer(soort_WAARDE,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else hulp_tonen(); }
        else if (같음(0, "info") || 같음(0, "i")) Kern.msinfo32_exe();
        else if (같음(0, "pwd")) { GeheugenBestanden.actueel_schrijven(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_AANTAL == 1) { GeheugenBestanden.pad_START(1); 처리값 = GeheugenBestanden.pad_byte(0, '/'); } else 처리값 = token_AANTAL == 2 ? pad(1) : -22;
            if (처리값 >= 0) 처리값 = GeheugenBestanden.wijzigen_map(); if (처리값 < 0) fout(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_AANTAL == argument_INDEX) { GeheugenBestanden.pad_START(1); 처리값 = GeheugenBestanden.pad_byte(0, '.'); } else 처리값 = token_AANTAL == argument_INDEX + 1 ? pad(argument_INDEX) : -22;
            if (처리값 >= 0) 처리값 = GeheugenBestanden.경로목록(); if (처리값 < 0) fout(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) Shell_Hulpprogramma_s.Bestand_Taak(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) Shell_Hulpprogramma_s.kopiëren_WAARDE(같음(0, "mv"));
        else if (같음(0, "cat")) Shell_Hulpprogramma_s.Weergave_WAARDE();
        else if (같음(0, "wc")) Shell_Hulpprogramma_s.세기();
        else if (같음(0, "grep")) Shell_Hulpprogramma_s.Zoeken_invoer();
        else if (같음(0, "head") || 같음(0, "tail")) Shell_Hulpprogramma_s.kop_WAARDE(같음(0, "tail"));
        else if (같음(0, "tee")) Shell_Hulpprogramma_s.schrijven_Samenzijn();
        else if (같음(0, "env")) Shell_syntaxis.weergeven_omgeving();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_AANTAL == 1) Shell_syntaxis.weergeven_omgeving();
            for (int lus_INDEX = 1; lus_INDEX < token_AANTAL; lus_INDEX++) { int 처리값 = Shell_syntaxis.omgeving_Instellingen(lus_INDEX, 같음(0, "unset")); if (처리값 != 0) { resultaat = 처리값; 단말.Schrijven("opdracht parseren_WAARDE: variabele_WAARDE 이름이 잘못되었거나 예약된 이름이거나 omgeving 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) Shell_syntaxis.Uitvoeren_Bestand();
        else if (같음(0, "true")) resultaat = 0;
        else if (같음(0, "false")) resultaat = 1;
        else if (같음(0, "history")) regeleditor.weergeven_LOG();
        else if (같음(0, "exit")) {
            if (Shell_syntaxis.깊이 > 0) { resultaat = token_AANTAL == 1 ? Shell_syntaxis.Status_WAARDE : Shell_Hulpprogramma_s.cijfer_WAARDE(1); if (resultaat < 0 || resultaat > 255) resultaat = 2; Shell_syntaxis.script_beëindigen = true; }
            else if (Bord.terminal(2) != 0) terminal(true);
            else 단말.Schrijven("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Bewerk_WAARDE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_AANTAL < 2) { resultaat = 2; 단말.Schrijven("사용법: rm bestand...\n"); }
            for (int lus_INDEX = 1; lus_INDEX < token_AANTAL; lus_INDEX++) { int 처리값 = pad(lus_INDEX); if (처리값 == 0) 처리값 = GeheugenBestanden.wissen_invoer(); if (처리값 < 0) fout(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_functie = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_functie; 첫값 < token_AANTAL; 첫값++) { if (첫값 > START_functie) 단말.문자(32); for (int lus_INDEX = 0; lus_INDEX < tijdsduur_WAARDE[첫값]; lus_INDEX++) Bord.직렬쓰기(token_WAARDE[시작점[첫값] + lus_INDEX]); }
            if (START_functie == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Schrijven("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_bundel() : hulpmiddelen(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); resultaat = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !Shell_syntaxis.연결중) { 단말.Schrijven("exit "); 단말.nummer(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = hulpmiddelen(13); resultaat = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = hulpmiddelen(15); resultaat = 처리값 < 0 ? 126 : 처리값; if (!Shell_syntaxis.연결중) { 단말.Schrijven("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = hulpmiddelen(16); resultaat = 처리값 < 0 ? 126 : 처리값; if (!Shell_syntaxis.연결중) { 단말.Schrijven("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Grootte = Bord.terminal(13); 단말.Schrijven("TERMINAL SIZE "); 단말.nummer(Grootte & 65535); 단말.문자('x'); 단말.nummer(Grootte >>> 16); 단말.문자(10); }
            else terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Bord.terminal(9); pc.Uitvoeren_opdracht(); }
        else if (같음(0, "c")) Kern.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) Kern.test_Tasks();
        else if (같음(0, "g")) Kern.scherm();
        else if (같음(0, "selftest") || 같음(0, "u")) Kern.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Bord.uitvoeren_gebruiker_app(0); if (처리값 == 0) 단말.Schrijven("ELF DEMO PASS\n"); else fout(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? hulpmiddel_invoer(-2, 2) : hulpmiddelen(-1); resultaat = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !Shell_syntaxis.연결중) { 단말.Schrijven("exit "); 단말.nummer(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) Kern.test_Netwerken();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Bord.bestandsoverdracht_service(1); if (처리값 < 0) fout(처리값); else { 단말.Schrijven("FTP listening "); Systeem_hulpmiddel.schrijven_ADRES(Bord.net_status(0,0)); 단말.Schrijven(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Bord.bestandsoverdracht_service(0); 단말.Schrijven("FTP stopped\n"); }
            else 단말.Schrijven(Bord.bestandsoverdracht_service(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { bundel.Bereid_voor(); 단말.Schrijven("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Taal = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_AANTAL != 2 || Taal < 0) 단말.Schrijven("example java|c|python: tekstuitvoer, bestand, 네트워크, 그래픽, Java Swing Venster 예제\n");
            else { int 처리값 = 예제꾸러미.installeren_WAARDE(Taal); if (처리값 < 0) { fout(처리값); if (처리값 == -28) 단말.Schrijven("RAM full: remove unused files, then retry example\n"); } else 단말.Schrijven("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int opmaak_WAARDE = uitvoerbewerking_opmaak();
            if (opmaak_WAARDE == 1 || opmaak_WAARDE == 2) {
                int 처리값 = hulpmiddel_invoer(opmaak_WAARDE == 1 ? -1 : 14, 0); resultaat = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !Shell_syntaxis.연결중) { 단말.Schrijven("exit "); 단말.nummer(처리값); 단말.문자(10); }
            } else if (opmaak_WAARDE == 0) { resultaat = 126; 단말.Schrijven("실행할 nummer 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { resultaat = 127; 단말.Schrijven("Unknown command. help: commands\n"); }
        }
    }
    public static void Uitvoeren_opdracht() {
        bundel.Bereid_voor();
        for (int Taal = 0; Taal < 3; Taal++) { int 처리값 = 예제꾸러미.installeren_WAARDE(Taal); if (처리값 < 0) fout(처리값); }
        hulp_tonen();
        while (true) {
            venster_sessie.Proces_WAARDE_invoer(); if (venster_sessie.cv_uitvoerbewerking()) continue;
            if (!venster_sessie.이어읽기) 단말.Schrijven("jkoros-native> "); regeleditor.opdrachtregel = true; Bord.extern_wachten(1); int Grootte = invoerregel_lezen(); Bord.extern_wachten(0); regeleditor.opdrachtregel = false;
            if (Grootte == -3) continue;
            if (Grootte == -2) 단말.Schrijven("opdracht parseren_WAARDE: 명령줄이 너무 깁니다\n");
            if (Grootte >= 0) { Shell_syntaxis.script_beëindigen = false; Shell_syntaxis.Uitvoeren_opdracht(invoerregel, 0, Grootte, 0); } else Shell_syntaxis.Status_WAARDE = 130;
            Bord.beëindigen_extern_opdracht(Shell_syntaxis.Status_WAARDE);
            regeleditor.Grootte = regeleditor.cursor_WAARDE = regeleditor.START_venster = 0;
        }
    }
}
