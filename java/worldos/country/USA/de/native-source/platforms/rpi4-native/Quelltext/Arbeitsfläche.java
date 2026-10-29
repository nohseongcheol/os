// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Kleine Startoberfläche im Bildspeicher, gesteuert über UART mit TAB/ENTER/Q. Begrenzte Oberfläche mit eigener lateinischer 5x7-Schrift, ohne Swing, USB HID oder vollständige Eingabemethode. */
public final class Arbeitsfläche {
    static String zeichenWerte = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // Sieben Zeilen je Schriftzeichen, jede durch zwei Hexadezimalziffern beschrieben. Projekteigene 5x7-Schrift.
    static String formenListe =
        "0E11111F111111" + "1E11111E11111E" + "0F10101010100F" + "1E11111111111E" +
        "1F10101E10101F" + "1F10101E101010" + "0F10101711110F" + "1111111F111111" +
        "0E04040404040E" + "0702020212120C" + "11121418141211" + "1010101010101F" +
        "111B1515111111" + "11191915131311" + "0E11111111110E" + "1E11111E101010" +
        "0E11111115120D" + "1E11111E141211" + "0F10100E01011E" + "1F040404040404" +
        "1111111111110E" + "11111111110A04" + "11111115151B11" + "11110A040A1111" +
        "11110A04040404" + "1F01020408101F" + "0E11131519110E" + "040C040404040E" +
        "0E11010204081F" + "1E01010601011E" + "02060A121F0202" + "1F10101E01011E" +
        "0E10101E11110E" + "1F010204080808" + "0E11110E11110E" + "0E11110F01010E" +
        "0004041F040400" + "0000001F000000" + "00000000000C0C" + "000C0C000C0C00";
    static int zifferWert(int zeichenWert) { return zeichenWert <= '9' ? zeichenWert - '0' : zeichenWert - 'A' + 10; }
    static void Text(int waagerechtPosition, int senkrechtPosition, String inhaltswertWert, int farbeWert) {
        for (int zeichenWert = 0; zeichenWert < inhaltswertWert.length(); zeichenWert++) {
            int gefundenWert = -1;
            for (int kandidat = 0; kandidat < zeichenWerte.length(); kandidat++) if (zeichenWerte.charAt(kandidat) == inhaltswertWert.charAt(zeichenWert)) gefundenWert = kandidat;
            if (gefundenWert < 0) continue;
            for (int zeilennummerWert = 0; zeilennummerWert < 7; zeilennummerWert++) {
                int position = gefundenWert * 14 + zeilennummerWert * 2;
                int bitWert = zifferWert(formenListe.charAt(position)) * 16 + zifferWert(formenListe.charAt(position + 1));
                for (int spalteWert = 0; spalteWert < 5; spalteWert++) if ((bitWert & (16 >> spalteWert)) != 0)
                    Betriebskern.rechteck(waagerechtPosition + zeichenWert * 12 + spalteWert * 2, senkrechtPosition + zeilennummerWert * 2, 2, 2, farbeWert);
            }
        }
    }
    static void malenBildschirm(int auswahlWert, String statuswertWert) {
        Betriebskern.rechteck(0, 0, Platine.bildschirmBreite(), Platine.bildschirmHöhe(), 0x302018);
        Betriebskern.rechteck(32, 24, 576, 432, 0xefe8e2);
        Betriebskern.rechteck(32, 24, 576, 48, 0x905020);
        Text(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int Nummer = 0; Nummer < 5; Nummer++) {
            Betriebskern.rechteck(64, 112 + Nummer * 52, 512, 40, Nummer == auswahlWert ? 0xd0a040 : 0xd8d0c8);
            Text(84, 128 + Nummer * 52, Nummer == 0 ? "RUN C++ FILE PROGRAM" : Nummer == 1 ? "RUN UDP LOOPBACK" : Nummer == 2 ? "COMPILE AND RUN JAVA" : Nummer == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Text(68, 384, statuswertWert, 0x205020);
        Text(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void befehlAusführen() {
        if (Platine.bildschirmVorbereiten() == 0) { TerminalEinAusgabe.schreiben("GUI unavailable\n"); return; }
        int auswahlWert = 0;
        String statuswertWert = "READY";
        boolean vorherigZeile = Befehlsinterpreter.vorherigZeile;
        malenBildschirm(auswahlWert, statuswertWert);
        TerminalEinAusgabe.schreiben("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int Eingabewert = Platine.seriellLesen();
            if (Eingabewert < 0) { Platine.prozessorAbgeben(); continue; }
            if (Eingabewert == 10 && vorherigZeile) { vorherigZeile = false; continue; }
            vorherigZeile = Eingabewert == 13;
            if (Eingabewert >= '1' && Eingabewert <= '5') { auswahlWert = Eingabewert - '1'; Eingabewert = 13; }
            if (Eingabewert == 't' || Eingabewert == 'T') { Befehlsinterpreter.terminal(false); return; }
            if (Eingabewert == 'q' || Eingabewert == 'Q' || Eingabewert == 27) break;
            if (Eingabewert == 9 || Eingabewert == 'j') {
                auswahlWert = (auswahlWert + 1) % 5; malenBildschirm(auswahlWert, statuswertWert); TerminalEinAusgabe.schreiben("GUI FOCUS "); TerminalEinAusgabe.Zahl(auswahlWert); TerminalEinAusgabe.Zeichen(10);
            } else if (Eingabewert == 13 || Eingabewert == 10) {
                if (auswahlWert == 4) { Befehlsinterpreter.terminal(false); return; }
                int ergebnis;
                if (auswahlWert < 2) ergebnis = Platine.benutzerProgrammAusführenVorgang(auswahlWert == 0 ? 0 : 9);
                else if (auswahlWert == 2) {
                    ergebnis = Befehlsinterpreter.beispielAusführenVorgang(10, "Hello.java");
                    if (ergebnis == 0) ergebnis = Befehlsinterpreter.beispielAusführenVorgang(11, "Hello");
                } else ergebnis = Befehlsinterpreter.beispielAusführenVorgang(12, "hello.py");
                statuswertWert = ergebnis != 0 ? "PROGRAM FAILED" : auswahlWert == 0 ? "C++ FILE OK" : auswahlWert == 1 ? "UDP LOOPBACK OK" : auswahlWert == 2 ? "JAVA OK" : "MICROPYTHON OK";
                malenBildschirm(auswahlWert, statuswertWert);
                TerminalEinAusgabe.schreiben("GUI ACTION "); TerminalEinAusgabe.Zahl(auswahlWert); TerminalEinAusgabe.schreiben(" RESULT "); TerminalEinAusgabe.Zahl(ergebnis); TerminalEinAusgabe.Zeichen(10);
            }
        }
        Betriebskern.Bildschirm();
        TerminalEinAusgabe.schreiben("GUI EXIT\n");
    }
}
