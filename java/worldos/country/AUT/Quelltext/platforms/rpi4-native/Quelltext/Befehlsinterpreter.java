// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8-Befehlszeile über UART mit Anführungszeichen, Backspace, Ctrl-U, Ctrl-C und RAM-Editor. */
public final class Befehlsinterpreter {
    static int[] zeile = new int[4096], wortzeichenWert = new int[4096], beginnendPunkt = new int[32], Länge = new int[32];
    static int[] bearbeitetInhalt = new int[16384], bearbeitenName = new int[63];
    static int wortzeichenAnzahl, bearbeitenNameLänge, ergebnis;
    static boolean vorherigZeile;
    static void ursprünglichByte(int Wert) { Platine.seriellSchreiben(Wert); }
    static int eingabeZeileLesen() { return ZeileEditor.lesen(); }
    static boolean teilenWerte(int größe) {
        int position = 0, endung = 0; wortzeichenAnzahl = 0;
        while (position < größe) {
            while (position < größe && (zeile[position] == 32 || zeile[position] == 9)) position++;
            if (position == größe) break;
            if (wortzeichenAnzahl == 16) { TerminalEinAusgabe.schreiben("befehl wertAnalysieren: 인수가 너무 많습니다\n"); return false; }
            beginnendPunkt[wortzeichenAnzahl] = endung; int anführungszeichenWert = 0;
            while (position < größe) {
                int Wert = zeile[position++];
                if (anführungszeichenWert == 0 && (Wert == 32 || Wert == 9)) break;
                if (Wert == anführungszeichenWert) { anführungszeichenWert = 0; continue; }
                if (anführungszeichenWert == 0 && (Wert == 39 || Wert == 34)) { anführungszeichenWert = Wert; continue; }
                wortzeichenWert[endung++] = Wert;
            }
            if (anführungszeichenWert != 0) { TerminalEinAusgabe.schreiben("befehl wertAnalysieren: 따옴표가 닫히지 않았습니다\n"); return false; }
            Länge[wortzeichenAnzahl] = endung - beginnendPunkt[wortzeichenAnzahl]; wortzeichenAnzahl++;
        }
        return true;
    }
    static boolean gleichText(int Nummer, String maschinenwortText) {
        if (Nummer >= wortzeichenAnzahl) return false;
        int positionIndex=0;
        for (int ordnungszahlIndex=0; ordnungszahlIndex<maschinenwortText.length(); ordnungszahlIndex++) {
            int zeichenKode=maschinenwortText.charAt(ordnungszahlIndex);
            if (zeichenKode>=0xd800 && zeichenKode<=0xdbff && ordnungszahlIndex+1<maschinenwortText.length()) zeichenKode=0x10000+((zeichenKode-0xd800)<<10)+maschinenwortText.charAt(++ordnungszahlIndex)-0xdc00;
            int byteAnzahl=zeichenKode<128?1:zeichenKode<2048?2:zeichenKode<65536?3:4;
            for (int folgeWert=byteAnzahl-1; folgeWert>=0; folgeWert--) {
                int Wert=byteAnzahl==1?zeichenKode:folgeWert==byteAnzahl-1?(byteAnzahl==2?0xc0:byteAnzahl==3?0xe0:0xf0)|(zeichenKode>>(6*folgeWert)):0x80|((zeichenKode>>(6*folgeWert))&63);
                if (positionIndex>=Länge[Nummer] || wortzeichenWert[beginnendPunkt[Nummer]+positionIndex++]!=Wert) return false;
            }
        }
        return positionIndex==Länge[Nummer];
    }
    static int pfad(int Nummer) {
        if (Nummer >= wortzeichenAnzahl) return -22;
        int ergebnis = SpeicherDateien.pfadStarten(Länge[Nummer]); if (ergebnis < 0) return ergebnis;
        for (int schleifeIndex = 0; schleifeIndex < Länge[Nummer]; schleifeIndex++) {
            ergebnis = SpeicherDateien.pfadByte(schleifeIndex, wortzeichenWert[beginnendPunkt[Nummer] + schleifeIndex]); if (ergebnis < 0) return ergebnis;
        }
        return 0;
    }
    static void fehler(int Nummer) { ergebnis = 1; TerminalEinAusgabe.schreiben("fehler "); TerminalEinAusgabe.Zahl(Nummer); TerminalEinAusgabe.Zeichen(10); }
    static void ansichtWert() {
        if (wortzeichenAnzahl != 2) { TerminalEinAusgabe.schreiben("사용법: cat Datei\n"); return; }
        int ergebnis = pfad(1); if (ergebnis < 0) { fehler(ergebnis); return; }
        int Datei = SpeicherDateien.öffnen(0); if (Datei < 0) { fehler(Datei); return; }
        while (true) { int Wert = SpeicherDateien.lesen(Datei); if (Wert == 256) break; if (Wert < 0) { fehler(Wert); break; } ursprünglichByte(Wert); }
        SpeicherDateien.schließen(Datei); TerminalEinAusgabe.Zeichen(10);
    }
    static void bearbeitenWert() {
        if (wortzeichenAnzahl != 2) { TerminalEinAusgabe.schreiben("사용법: edit Datei\n"); return; }
        int ergebnis = pfad(1); if (ergebnis < 0) { fehler(ergebnis); return; }
        bearbeitenNameLänge = Länge[1];
        for (int schleifeIndex = 0; schleifeIndex < bearbeitenNameLänge; schleifeIndex++) bearbeitenName[schleifeIndex] = wortzeichenWert[beginnendPunkt[1] + schleifeIndex];
        TerminalEinAusgabe.schreiben("EDIT: Datei 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(höchstwertWert 16384바이트)\n");
        int größe = 0;
        while (true) {
            TerminalEinAusgabe.schreiben("edit> "); int Eingabewert = eingabeZeileLesen();
            if (Eingabewert < 0) { TerminalEinAusgabe.schreiben("EDIT CANCELLED\n"); return; }
            if (Eingabewert == 1 && zeile[0] == '.') break;
            if (Eingabewert + 1 > bearbeitetInhalt.length - größe) { TerminalEinAusgabe.schreiben("EDIT CANCELLED: file too large\n"); return; }
            for (int schleifeIndex = 0; schleifeIndex < Eingabewert; schleifeIndex++) bearbeitetInhalt[größe++] = zeile[schleifeIndex];
            bearbeitetInhalt[größe++] = 10;
        }
        SpeicherDateien.pfadStarten(bearbeitenNameLänge);
        for (int schleifeIndex = 0; schleifeIndex < bearbeitenNameLänge; schleifeIndex++) SpeicherDateien.pfadByte(schleifeIndex, bearbeitenName[schleifeIndex]);
        int Datei = SpeicherDateien.öffnen(577); if (Datei < 0) { fehler(Datei); return; }
        for (int schleifeIndex = 0; schleifeIndex < größe; schleifeIndex++) SpeicherDateien.schreiben(Datei, bearbeitetInhalt[schleifeIndex]);
        SpeicherDateien.schließen(Datei); TerminalEinAusgabe.schreiben("SAVED "); TerminalEinAusgabe.Zahl(größe); TerminalEinAusgabe.schreiben("byteWert(주기억 Datei)\n");
    }
    static int hexadezimalWert(int Wert) {
        if (Wert >= '0' && Wert <= '9') return Wert - '0';
        if (Wert >= 'a' && Wert <= 'f') return Wert - 'a' + 10;
        if (Wert >= 'A' && Wert <= 'F') return Wert - 'A' + 10;
        return -1;
    }
    static void binärEinAusgabe(boolean wertAblegen) {
        if (wortzeichenAnzahl != 2) { TerminalEinAusgabe.schreiben("사용법: load Datei | hex Datei\n"); return; }
        int ergebnis = pfad(1); if (ergebnis < 0) { fehler(ergebnis); return; }
        if (!wertAblegen) {
            int Datei = SpeicherDateien.öffnen(0); if (Datei < 0) { fehler(Datei); return; }
            TerminalEinAusgabe.schreiben("HEX BEGIN "); TerminalEinAusgabe.Zahl(SpeicherDateien.größe(Datei)); TerminalEinAusgabe.Zeichen(10);
            int eintragAnzahl = 0;
            while (true) {
                int Wert = SpeicherDateien.lesen(Datei); if (Wert < 0 || Wert == 256) break;
                TerminalEinAusgabe.Zeichen("0123456789abcdef".charAt(Wert >> 4)); TerminalEinAusgabe.Zeichen("0123456789abcdef".charAt(Wert & 15));
                if (++eintragAnzahl % 32 == 0) TerminalEinAusgabe.Zeichen(10);
            }
            if (eintragAnzahl % 32 != 0) TerminalEinAusgabe.Zeichen(10);
            SpeicherDateien.schließen(Datei); TerminalEinAusgabe.schreiben("HEX END\n"); return;
        }
        bearbeitenNameLänge = Länge[1];
        for (int schleifeIndex = 0; schleifeIndex < bearbeitenNameLänge; schleifeIndex++) bearbeitenName[schleifeIndex] = wortzeichenWert[beginnendPunkt[1] + schleifeIndex];
        TerminalEinAusgabe.schreiben("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int größe = 0;
        while (true) {
            TerminalEinAusgabe.schreiben("hex> "); int Eingabewert = eingabeZeileLesen();
            if (Eingabewert < 0) { TerminalEinAusgabe.schreiben("LOAD CANCELLED\n"); return; }
            if (Eingabewert == 1 && zeile[0] == '.') break;
            int vorderseiteWert = -1;
            for (int schleifeIndex = 0; schleifeIndex < Eingabewert; schleifeIndex++) {
                if (zeile[schleifeIndex] == 32 || zeile[schleifeIndex] == 9) continue;
                int Wert = hexadezimalWert(zeile[schleifeIndex]);
                if (Wert < 0 || größe >= bearbeitetInhalt.length) { TerminalEinAusgabe.schreiben("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (vorderseiteWert < 0) vorderseiteWert = Wert; else { bearbeitetInhalt[größe++] = vorderseiteWert * 16 + Wert; vorderseiteWert = -1; }
            }
            if (vorderseiteWert >= 0) { TerminalEinAusgabe.schreiben("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        SpeicherDateien.pfadStarten(bearbeitenNameLänge);
        for (int schleifeIndex = 0; schleifeIndex < bearbeitenNameLänge; schleifeIndex++) SpeicherDateien.pfadByte(schleifeIndex, bearbeitenName[schleifeIndex]);
        int Datei = SpeicherDateien.öffnen(577); if (Datei < 0) { fehler(Datei); return; }
        for (int schleifeIndex = 0; schleifeIndex < größe; schleifeIndex++) SpeicherDateien.schreiben(Datei, bearbeitetInhalt[schleifeIndex]);
        SpeicherDateien.schließen(Datei); TerminalEinAusgabe.schreiben("LOADED "); TerminalEinAusgabe.Zahl(größe); TerminalEinAusgabe.schreiben("byteWert(주기억 Datei)\n");
    }
    static int Werkzeuge(int Nummer) {
        return WerkzeugEintrag(Nummer, 1);
    }
    static int WerkzeugEintrag(int Nummer, int ausführenVorgang) {
        if (wortzeichenAnzahl - ausführenVorgang > 8) return -22;
        Platine.argumenteVorbereiten(wortzeichenAnzahl - ausführenVorgang);
        for (int ersterDaten = ausführenVorgang; ersterDaten < wortzeichenAnzahl; ersterDaten++) {
            if (Länge[ersterDaten] > 255) return -36;
            for (int schleifeIndex = 0; schleifeIndex < Länge[ersterDaten]; schleifeIndex++) Platine.argumentByte(ersterDaten - ausführenVorgang, schleifeIndex, wortzeichenWert[beginnendPunkt[ersterDaten] + schleifeIndex]);
        }
        return Nummer == -2 ? Platine.linuxDateiAusführen() : Nummer < 0 ? Platine.benutzerDateiAusführen() : Platine.benutzerProgrammAusführenVorgang(Nummer);
    }
    static int PythonBündel() {
        if (wortzeichenAnzahl > 8) return -22;
        Platine.argumenteVorbereiten(wortzeichenAnzahl);
        String pfad = "/lib/Paket.py";
        // Java-Zeichenkette in den UTF-8-Argumentpuffer der Shell schreiben.
        int positionIndex = 0;
        for (int ordnungszahlIndex = 0; ordnungszahlIndex < pfad.length(); ordnungszahlIndex++) {
            int zeichenWert = pfad.charAt(ordnungszahlIndex);
            if (zeichenWert < 128) Platine.argumentByte(0, positionIndex++, zeichenWert);
            else { Platine.argumentByte(0, positionIndex++, 0xe0 | (zeichenWert >> 12)); Platine.argumentByte(0, positionIndex++, 0x80 | ((zeichenWert >> 6) & 63)); Platine.argumentByte(0, positionIndex++, 0x80 | (zeichenWert & 63)); }
        }
        for (int ordnungszahlIndex = 1; ordnungszahlIndex < wortzeichenAnzahl; ordnungszahlIndex++) {
            if (Länge[ordnungszahlIndex] > 255) return -36;
            for (int zeichenWert = 0; zeichenWert < Länge[ordnungszahlIndex]; zeichenWert++) Platine.argumentByte(ordnungszahlIndex, zeichenWert, wortzeichenWert[beginnendPunkt[ordnungszahlIndex] + zeichenWert]);
        }
        return Platine.benutzerProgrammAusführenVorgang(12);
    }
    static int ausführungFormat() {
        int verarbeitetWert = pfad(0); if (verarbeitetWert < 0) return verarbeitetWert;
        int Datei = SpeicherDateien.öffnen(0); if (Datei < 0) return Datei;
        int ersterDaten = SpeicherDateien.lesen(Datei), byteDaten = SpeicherDateien.lesen(Datei), zeichenKode = SpeicherDateien.lesen(Datei), nachlaufendWert = SpeicherDateien.lesen(Datei);
        SpeicherDateien.schließen(Datei);
        if (ersterDaten == 127 && byteDaten == 'E' && zeichenKode == 'L' && nachlaufendWert == 'F') return 1;
        if (ersterDaten == 'P' && byteDaten == 'K' && zeichenKode == 3 && nachlaufendWert == 4) return 2;
        return 0;
    }
    static int beispielAusführenVorgang(int Nummer, String argumente) {
        Platine.argumenteVorbereiten(1);
        for (int schleifeIndex = 0; schleifeIndex < argumente.length(); schleifeIndex++) Platine.argumentByte(0, schleifeIndex, argumente.charAt(schleifeIndex));
        return Platine.benutzerProgrammAusführenVorgang(Nummer);
    }
    static void textByte(int Datei, int Wert) { SpeicherDateien.schreiben(Datei, Wert); }
    static void statischDatei(String Name, String inhaltswertWert) {
        // Dateinamen im Bündel verwenden ASCII; Dateiinhalte werden als UTF-8 gespeichert.
        SpeicherDateien.pfadStarten(Name.length());
        for (int schleifeIndex = 0; schleifeIndex < Name.length(); schleifeIndex++) SpeicherDateien.pfadByte(schleifeIndex, Name.charAt(schleifeIndex));
        int Datei = SpeicherDateien.öffnen(193); if (Datei < 0) return;
        for (int schleifeIndex = 0; schleifeIndex < inhaltswertWert.length(); schleifeIndex++) {
            int zeichenKode = inhaltswertWert.charAt(schleifeIndex);
            if (zeichenKode >= 0xd800 && zeichenKode <= 0xdbff && schleifeIndex + 1 < inhaltswertWert.length()) zeichenKode = 0x10000 + ((zeichenKode - 0xd800) << 10) + inhaltswertWert.charAt(++schleifeIndex) - 0xdc00;
            if (zeichenKode < 128) textByte(Datei, zeichenKode);
            else {
                int Zahl = zeichenKode < 2048 ? 2 : zeichenKode < 65536 ? 3 : 4;
                textByte(Datei, (Zahl == 2 ? 0xc0 : Zahl == 3 ? 0xe0 : 0xf0) | (zeichenKode >> (6 * (Zahl - 1))));
                for (int eintragAnzahl = Zahl - 1; eintragAnzahl > 0; eintragAnzahl--) textByte(Datei, 0x80 | ((zeichenKode >> (6 * (eintragAnzahl - 1))) & 63));
            }
        }
        SpeicherDateien.schließen(Datei);
    }
    static void hangulHilfe() {
        TerminalEinAusgabe.schreiben("F9 oder Shift+Space schaltet zur deutschen Tastatur um.\n");
        TerminalEinAusgabe.schreiben("  [DE] keyboard; [EN] ASCII\n");
        TerminalEinAusgabe.schreiben("  # → §\n");
        TerminalEinAusgabe.schreiben("  F9: EN ↔ Deutsch | Ctrl+Shift+V: UTF-8\n");
        TerminalEinAusgabe.schreiben("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        TerminalEinAusgabe.schreiben("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int beispielPfad(String Name) {
        int byteAnzahl = 0;
        for (int schleifeIndex = 0; schleifeIndex < Name.length(); schleifeIndex++) { int zeichenKode = Name.charAt(schleifeIndex); if (zeichenKode >= 0xd800 && zeichenKode <= 0xdfff) return -22; byteAnzahl += zeichenKode < 128 ? 1 : zeichenKode < 2048 ? 2 : 3; }
        int verarbeitetWert = SpeicherDateien.pfadStarten(byteAnzahl); if (verarbeitetWert < 0) return verarbeitetWert;
        int positionIndex = 0;
        for (int schleifeIndex = 0; schleifeIndex < Name.length(); schleifeIndex++) {
            int zeichenKode = Name.charAt(schleifeIndex);
            if (zeichenKode < 128) SpeicherDateien.pfadByte(positionIndex++, zeichenKode);
            else if (zeichenKode < 2048) { SpeicherDateien.pfadByte(positionIndex++, 0xc0 | (zeichenKode >> 6)); SpeicherDateien.pfadByte(positionIndex++, 0x80 | (zeichenKode & 63)); }
            else { SpeicherDateien.pfadByte(positionIndex++, 0xe0 | (zeichenKode >> 12)); SpeicherDateien.pfadByte(positionIndex++, 0x80 | ((zeichenKode >> 6) & 63)); SpeicherDateien.pfadByte(positionIndex++, 0x80 | (zeichenKode & 63)); }
        }
        return 0;
    }
    static int beispielVerzeichnis(String Name) {
        int verarbeitetWert = beispielPfad(Name); if (verarbeitetWert < 0) return verarbeitetWert;
        verarbeitetWert = SpeicherDateien.verzeichnisErstellen(); return verarbeitetWert == -17 ? 0 : verarbeitetWert;
    }
    static int beispielDatei(String Name, String Daten) {
        int verarbeitetWert = beispielPfad(Name); if (verarbeitetWert < 0) return verarbeitetWert;
        int Datei = SpeicherDateien.öffnen(193); if (Datei == -17) return 0; if (Datei < 0) return Datei;
        for (int schleifeIndex = 0; schleifeIndex < Daten.length(); schleifeIndex += 2) {
            verarbeitetWert = SpeicherDateien.schreiben(Datei, hexadezimalWert(Daten.charAt(schleifeIndex)) * 16 + hexadezimalWert(Daten.charAt(schleifeIndex + 1)));
            if (verarbeitetWert < 0) { SpeicherDateien.schließen(Datei); return verarbeitetWert; }
        }
        return SpeicherDateien.schließen(Datei);
    }
    static void hilfeAnzeigen() {
        systemWerkzeug.hilfeAnzeigen();
        TerminalEinAusgabe.schreiben("sshd / absichernBefehlshülle start|stop|status: SSH :22 (user, 장치별 passwortWert)\n");
        TerminalEinAusgabe.schreiben("vncd / EntferntDarstellen start|stop|status: VNC :5900 (장치별 passwortWert)\n");
        TerminalEinAusgabe.schreiben("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        TerminalEinAusgabe.schreiben("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        TerminalEinAusgabe.schreiben("wc grep head tail tee env export unset history sh source true false exit\n");
        TerminalEinAusgabe.schreiben("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        TerminalEinAusgabe.schreiben("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        TerminalEinAusgabe.schreiben("eckeWert + linksSeiteRand 버튼 ziehenWert: terminal größe wertÄndern; terminal size: spalteWert/zeilennummerWert\n");
        TerminalEinAusgabe.schreiben("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        TerminalEinAusgabe.schreiben("vi FILE: i to insert; Esc then :wq to save and quit\n");
        TerminalEinAusgabe.schreiben("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        TerminalEinAusgabe.schreiben("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        TerminalEinAusgabe.schreiben("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        TerminalEinAusgabe.schreiben("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        TerminalEinAusgabe.schreiben("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        TerminalEinAusgabe.schreiben("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        TerminalEinAusgabe.schreiben("python FILE.py | python -c 'CODE' (MicroPython)\n");
        TerminalEinAusgabe.schreiben("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        TerminalEinAusgabe.schreiben("pip: MicroPython quelltextBaum wertEinrichten; Wirtssystem --network --pip benötigtWert; /lib는 RAM\n");
        TerminalEinAusgabe.schreiben("gui | run cpp | net test | tasks | selftest | samples\n");
        TerminalEinAusgabe.schreiben("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        TerminalEinAusgabe.schreiben("/example/java /example/c /example/python: examples ready at boot\n");
        TerminalEinAusgabe.schreiben("example java|c|python: restore missing examples (keeps existing files)\n");
        hangulHilfe();
    }
    static void terminal(boolean warUmgeschaltet) {
        if (warUmgeschaltet && Platine.terminal(2) != 0) { Platine.terminal(0); TerminalEinAusgabe.schreiben("TERMINAL CLOSED\n"); }
        else if (Platine.terminal(1) < 0) fehler(-19);
        else TerminalEinAusgabe.schreiben("TERMINAL READY — Deutsch terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void befehl() {
        if (wortzeichenAnzahl == 0) return;
        if (systemWerkzeug.befehlAusführen()) return;
        if (gleichText(0,"sshd") || gleichText(0,"absichernBefehlshülle") || gleichText(0,"vncd") || gleichText(0,"EntferntDarstellen")) {
            int artWert=gleichText(0,"vncd")||gleichText(0,"EntferntDarstellen")?1:0;
            int aktion=gleichText(1,"start")||gleichText(1,"ausführenVorgang")?1:gleichText(1,"stop")||gleichText(1,"stoppen")?0:2;
            int statuswertWert=Platine.entferntSteuerung(artWert,aktion);
            if(statuswertWert<0)fehler(statuswertWert);else TerminalEinAusgabe.schreiben(Platine.entferntSteuerung(artWert,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (gleichText(0, "help") || gleichText(0, "h")) { if (gleichText(1, "ko") || gleichText(1, "input")) hangulHilfe(); else hilfeAnzeigen(); }
        else if (gleichText(0, "info") || gleichText(0, "i")) Betriebskern.systemInformation();
        else if (gleichText(0, "pwd")) { SpeicherDateien.aktuellSchreiben(); TerminalEinAusgabe.Zeichen(10); }
        else if (gleichText(0, "cd")) {
            int verarbeitetWert;
            if (wortzeichenAnzahl == 1) { SpeicherDateien.pfadStarten(1); verarbeitetWert = SpeicherDateien.pfadByte(0, '/'); } else verarbeitetWert = wortzeichenAnzahl == 2 ? pfad(1) : -22;
            if (verarbeitetWert >= 0) verarbeitetWert = SpeicherDateien.verzeichnisÄndern(); if (verarbeitetWert < 0) fehler(verarbeitetWert);
        }
        else if (gleichText(0, "ls") || gleichText(0, "f")) {
            int argumentIndex = gleichText(1, "-l") ? 2 : 1, verarbeitetWert;
            if (wortzeichenAnzahl == argumentIndex) { SpeicherDateien.pfadStarten(1); verarbeitetWert = SpeicherDateien.pfadByte(0, '.'); } else verarbeitetWert = wortzeichenAnzahl == argumentIndex + 1 ? pfad(argumentIndex) : -22;
            if (verarbeitetWert >= 0) verarbeitetWert = SpeicherDateien.pfadEinträge(); if (verarbeitetWert < 0) fehler(verarbeitetWert);
        }
        else if (gleichText(0, "mkdir") || gleichText(0, "rmdir") || gleichText(0, "touch")) BefehlshülleWerkzeuge.dateiAuftrag(gleichText(0, "mkdir") ? "mkdir" : gleichText(0, "rmdir") ? "rmdir" : "touch");
        else if (gleichText(0, "cp") || gleichText(0, "mv")) BefehlshülleWerkzeuge.wertKopieren(gleichText(0, "mv"));
        else if (gleichText(0, "cat")) BefehlshülleWerkzeuge.ansichtWert();
        else if (gleichText(0, "wc")) BefehlshülleWerkzeuge.zählendWert();
        else if (gleichText(0, "grep")) BefehlshülleWerkzeuge.eintragFinden();
        else if (gleichText(0, "head") || gleichText(0, "tail")) BefehlshülleWerkzeuge.kopfWert(gleichText(0, "tail"));
        else if (gleichText(0, "tee")) BefehlshülleWerkzeuge.zusammenSchreiben();
        else if (gleichText(0, "env")) BefehlshülleSatzbau.umgebungAnzeigen();
        else if (gleichText(0, "export") || gleichText(0, "unset")) {
            if (wortzeichenAnzahl == 1) BefehlshülleSatzbau.umgebungAnzeigen();
            for (int schleifeIndex = 1; schleifeIndex < wortzeichenAnzahl; schleifeIndex++) { int verarbeitetWert = BefehlshülleSatzbau.umgebungEinstellungen(schleifeIndex, gleichText(0, "unset")); if (verarbeitetWert != 0) { ergebnis = verarbeitetWert; TerminalEinAusgabe.schreiben("befehl wertAnalysieren: variableWert 이름이 잘못되었거나 예약된 이름이거나 umgebung 공간이 가득 찼습니다\n"); } }
        }
        else if (gleichText(0, "sh") || gleichText(0, "source")) BefehlshülleSatzbau.dateiAusführen();
        else if (gleichText(0, "true")) ergebnis = 0;
        else if (gleichText(0, "false")) ergebnis = 1;
        else if (gleichText(0, "history")) ZeileEditor.protokolldateiAnzeigen();
        else if (gleichText(0, "exit")) {
            if (BefehlshülleSatzbau.tiefeWert > 0) { ergebnis = wortzeichenAnzahl == 1 ? BefehlshülleSatzbau.statuswertWert : BefehlshülleWerkzeuge.zifferWert(1); if (ergebnis < 0 || ergebnis > 255) ergebnis = 2; BefehlshülleSatzbau.skriptEnde = true; }
            else if (Platine.terminal(2) != 0) terminal(true);
            else TerminalEinAusgabe.schreiben("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (gleichText(0, "edit")) bearbeitenWert();
        else if (gleichText(0, "load") || gleichText(0, "hex")) binärEinAusgabe(gleichText(0, "load"));
        else if (gleichText(0, "rm")) {
            if (wortzeichenAnzahl < 2) { ergebnis = 2; TerminalEinAusgabe.schreiben("사용법: rm Datei...\n"); }
            for (int schleifeIndex = 1; schleifeIndex < wortzeichenAnzahl; schleifeIndex++) { int verarbeitetWert = pfad(schleifeIndex); if (verarbeitetWert == 0) verarbeitetWert = SpeicherDateien.eintragTilgen(); if (verarbeitetWert < 0) fehler(verarbeitetWert); }
        }
        else if (gleichText(0, "echo")) {
            int positionStarten = gleichText(1, "-n") ? 2 : 1;
            for (int ersterDaten = positionStarten; ersterDaten < wortzeichenAnzahl; ersterDaten++) { if (ersterDaten > positionStarten) TerminalEinAusgabe.Zeichen(32); for (int schleifeIndex = 0; schleifeIndex < Länge[ersterDaten]; schleifeIndex++) Platine.seriellSchreiben(wortzeichenWert[beginnendPunkt[ersterDaten] + schleifeIndex]); }
            if (positionStarten == 1) TerminalEinAusgabe.Zeichen(10);
        }
        else if (gleichText(0, "clear")) TerminalEinAusgabe.schreiben("\u001b[2J\u001b[H");
        else if (gleichText(0, "javac") || gleichText(0, "java") || gleichText(0, "python") || gleichText(0, "pip")) {
            int verarbeitetWert = gleichText(0, "pip") ? PythonBündel() : Werkzeuge(gleichText(0, "javac") ? 10 : gleichText(0, "java") ? 11 : 12); ergebnis = verarbeitetWert == -1005 ? -1005 : verarbeitetWert < 0 ? 126 : verarbeitetWert;
            if (verarbeitetWert != -1005 && !BefehlshülleSatzbau.istVerbindend) { TerminalEinAusgabe.schreiben("exit "); TerminalEinAusgabe.Zahl(verarbeitetWert); TerminalEinAusgabe.Zeichen(10); }
        }
        else if (gleichText(0, "vi")) { int verarbeitetWert = Werkzeuge(13); ergebnis = verarbeitetWert == -1005 ? -1005 : verarbeitetWert < 0 ? 126 : verarbeitetWert; }
        else if (gleichText(0, "cc") || gleichText(0, "tcc")) { int verarbeitetWert = Werkzeuge(15); ergebnis = verarbeitetWert < 0 ? 126 : verarbeitetWert; if (!BefehlshülleSatzbau.istVerbindend) { TerminalEinAusgabe.schreiben("exit "); TerminalEinAusgabe.Zahl(verarbeitetWert); TerminalEinAusgabe.Zeichen(10); } }
        else if (gleichText(0, "jaot")) { int verarbeitetWert = Werkzeuge(16); ergebnis = verarbeitetWert < 0 ? 126 : verarbeitetWert; if (!BefehlshülleSatzbau.istVerbindend) { TerminalEinAusgabe.schreiben("exit "); TerminalEinAusgabe.Zahl(verarbeitetWert); TerminalEinAusgabe.Zeichen(10); } }
        else if (gleichText(0, "terminal")) {
            if (gleichText(1, "size")) { int größe = Platine.terminal(13); TerminalEinAusgabe.schreiben("TERMINAL SIZE "); TerminalEinAusgabe.Zahl(größe & 65535); TerminalEinAusgabe.Zeichen('x'); TerminalEinAusgabe.Zahl(größe >>> 16); TerminalEinAusgabe.Zeichen(10); }
            else terminal(false);
        }
        else if (gleichText(0, "gui") || gleichText(0, "v")) { Platine.terminal(9); Arbeitsfläche.befehlAusführen(); }
        else if (gleichText(0, "c")) Betriebskern.cPrüfung();
        else if (gleichText(0, "tasks") || gleichText(0, "t")) Betriebskern.aufgabenPrüfung();
        else if (gleichText(0, "g")) Betriebskern.Bildschirm();
        else if (gleichText(0, "selftest") || gleichText(0, "u")) Betriebskern.benutzerProgrammePrüfung();
        else if (gleichText(0, "e") || (gleichText(0, "run") && gleichText(1, "cpp"))) {
            int verarbeitetWert = Platine.benutzerProgrammAusführenVorgang(0); if (verarbeitetWert == 0) TerminalEinAusgabe.schreiben("ELF DEMO PASS\n"); else fehler(verarbeitetWert);
        }
        else if (gleichText(0, "run")) { int verarbeitetWert = gleichText(1, "--linux") ? WerkzeugEintrag(-2, 2) : Werkzeuge(-1); ergebnis = verarbeitetWert == -1005 ? -1005 : verarbeitetWert < 0 ? 126 : verarbeitetWert; if (verarbeitetWert != -1005 && !BefehlshülleSatzbau.istVerbindend) { TerminalEinAusgabe.schreiben("exit "); TerminalEinAusgabe.Zahl(verarbeitetWert); TerminalEinAusgabe.Zeichen(10); } }
        else if (gleichText(0, "n") || (gleichText(0, "net") && gleichText(1, "test"))) Betriebskern.netzbetriebPrüfung();
        else if (gleichText(0, "ftpd")) {
            if (gleichText(1, "start")) { int verarbeitetWert = Platine.dateiÜbertragungDienst(1); if (verarbeitetWert < 0) fehler(verarbeitetWert); else { TerminalEinAusgabe.schreiben("FTP listening "); systemWerkzeug.adresseSchreiben(Platine.netzwerkZustand(0,0)); TerminalEinAusgabe.schreiben(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (gleichText(1, "stop")) { Platine.dateiÜbertragungDienst(0); TerminalEinAusgabe.schreiben("FTP stopped\n"); }
            else TerminalEinAusgabe.schreiben(Platine.dateiÜbertragungDienst(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (gleichText(0, "samples")) { Paket.vorbereiten(); TerminalEinAusgabe.schreiben("SAMPLES READY (existing files kept)\n"); }
        else if (gleichText(0, "example")) {
            int Sprache = gleichText(1, "java") ? 0 : gleichText(1, "c") ? 1 : gleichText(1, "python") ? 2 : -1;
            if (wortzeichenAnzahl != 2 || Sprache < 0) TerminalEinAusgabe.schreiben("example java|c|python: Ausgabe, Datei, 네트워크, 그래픽, Java Swing fenster Beispiele\n");
            else { int verarbeitetWert = BeispielBündel.wertEinrichten(Sprache); if (verarbeitetWert < 0) { fehler(verarbeitetWert); if (verarbeitetWert == -28) TerminalEinAusgabe.schreiben("RAM full: remove unused files, then retry example\n"); } else TerminalEinAusgabe.schreiben("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formatWert = ausführungFormat();
            if (formatWert == 1 || formatWert == 2) {
                int verarbeitetWert = WerkzeugEintrag(formatWert == 1 ? -1 : 14, 0); ergebnis = verarbeitetWert == -1005 ? -1005 : verarbeitetWert < 0 ? 126 : verarbeitetWert;
                if (verarbeitetWert != -1005 && !BefehlshülleSatzbau.istVerbindend) { TerminalEinAusgabe.schreiben("exit "); TerminalEinAusgabe.Zahl(verarbeitetWert); TerminalEinAusgabe.Zeichen(10); }
            } else if (formatWert == 0) { ergebnis = 126; TerminalEinAusgabe.schreiben("실행할 Zahl 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { ergebnis = 127; TerminalEinAusgabe.schreiben("Unknown command. help: commands\n"); }
        }
    }
    public static void befehlAusführen() {
        Paket.vorbereiten();
        for (int Sprache = 0; Sprache < 3; Sprache++) { int verarbeitetWert = BeispielBündel.wertEinrichten(Sprache); if (verarbeitetWert < 0) fehler(verarbeitetWert); }
        hilfeAnzeigen();
        while (true) {
            fensterSitzung.prozessWertEintrag(); if (fensterSitzung.fortführenAusführung()) continue;
            if (!fensterSitzung.fortsetzungLesen) TerminalEinAusgabe.schreiben("jkoros-native> "); ZeileEditor.befehlZeile = true; Platine.entferntWarten(1); int größe = eingabeZeileLesen(); Platine.entferntWarten(0); ZeileEditor.befehlZeile = false;
            if (größe == -3) continue;
            if (größe == -2) TerminalEinAusgabe.schreiben("befehl wertAnalysieren: 명령줄이 너무 깁니다\n");
            if (größe >= 0) { BefehlshülleSatzbau.skriptEnde = false; BefehlshülleSatzbau.befehlAusführen(zeile, 0, größe, 0); } else BefehlshülleSatzbau.statuswertWert = 130;
            Platine.endeEntferntBefehl(BefehlshülleSatzbau.statuswertWert);
            ZeileEditor.größe = ZeileEditor.mauszeigerWert = ZeileEditor.fensterStarten = 0;
        }
    }
}
