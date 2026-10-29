// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Shell-Zustand für vier Terminals. Der Dateispeicher ist gemeinsam; Pfade, Variablen, Verlauf und Eingabe sind getrennt. */
public final class fensterSitzung {
    static int[] wertBewahren = new int[4 * 30000], vorbereiten = new int[4];
    static int aktuellElementeintrag, position;
    static boolean fortsetzungLesen;
    static void datenfeldWert(int[] Daten, boolean ablegenDatenWert) {
        for (int schleifeIndex = 0; schleifeIndex < Daten.length; schleifeIndex++) { if (ablegenDatenWert) wertBewahren[position++] = Daten[schleifeIndex]; else Daten[schleifeIndex] = wertBewahren[position++]; }
    }
    static int Wert(int datenWert, boolean warAbgelegt) { if (warAbgelegt) { wertBewahren[position++] = datenWert; return datenWert; } return wertBewahren[position++]; }
    static void positionPositionieren(int bewahrtPlatz, boolean warAbgelegt) {
        position = bewahrtPlatz * 30000;
        datenfeldWert(SpeicherDateien.aktuellElementeintrag, warAbgelegt); SpeicherDateien.aktuellLänge = Wert(SpeicherDateien.aktuellLänge, warAbgelegt);
        datenfeldWert(BefehlshülleSatzbau.variableName, warAbgelegt); datenfeldWert(BefehlshülleSatzbau.variableDaten, warAbgelegt); datenfeldWert(BefehlshülleSatzbau.namenlänge, warAbgelegt); datenfeldWert(BefehlshülleSatzbau.wertLänge, warAbgelegt);
        BefehlshülleSatzbau.statuswertWert = Wert(BefehlshülleSatzbau.statuswertWert, warAbgelegt);
        datenfeldWert(ZeileEditor.protokolldateiAufzeichnung, warAbgelegt); datenfeldWert(ZeileEditor.protokolldateiLänge, warAbgelegt); datenfeldWert(ZeileEditor.ablegenDatenWert, warAbgelegt); datenfeldWert(Befehlsinterpreter.zeile, warAbgelegt);
        ZeileEditor.protokolldateiAnzahl = Wert(ZeileEditor.protokolldateiAnzahl, warAbgelegt); ZeileEditor.protokolldateiAufzeichnungEnde = Wert(ZeileEditor.protokolldateiAufzeichnungEnde, warAbgelegt);
        ZeileEditor.wertSuchen = Wert(ZeileEditor.wertSuchen, warAbgelegt); ZeileEditor.abgelegtLänge = Wert(ZeileEditor.abgelegtLänge, warAbgelegt);
        ZeileEditor.größe = Wert(ZeileEditor.größe, warAbgelegt); ZeileEditor.mauszeigerWert = Wert(ZeileEditor.mauszeigerWert, warAbgelegt); ZeileEditor.fensterStarten = Wert(ZeileEditor.fensterStarten, warAbgelegt);
        vorbereiten[bewahrtPlatz] = 1;
    }
    static void prozessWertEintrag() {
        int ereignisNummer = Platine.terminal(12); if (ereignisNummer == 0) return;
        positionPositionieren(aktuellElementeintrag, true);
        for (int schleifeIndex = 0; schleifeIndex < 4; schleifeIndex++) {
            if ((ereignisNummer & (1 << (8 + schleifeIndex))) != 0) { Platine.steuerungBenutzerProgramm(32 + schleifeIndex); vorbereiten[schleifeIndex] = 0; }
            if ((ereignisNummer & (1 << (4 + schleifeIndex))) != 0 && schleifeIndex != aktuellElementeintrag) vorbereiten[schleifeIndex] = 0;
        }
        int nächsterPosition = (ereignisNummer & 15) - 1; if (nächsterPosition < 0) nächsterPosition = 0;
        if (vorbereiten[nächsterPosition] == 0) for (int schleifeIndex = 0; schleifeIndex < 30000; schleifeIndex++) wertBewahren[nächsterPosition * 30000 + schleifeIndex] = 0;
        aktuellElementeintrag = nächsterPosition; positionPositionieren(aktuellElementeintrag, false); Platine.terminal(100 + aktuellElementeintrag); fortsetzungLesen = true;
        TerminalEinAusgabe.schreiben("\nTERMINAL FOCUS "); TerminalEinAusgabe.Zahl(aktuellElementeintrag + 1); TerminalEinAusgabe.Zeichen(10);
    }
    static boolean fortführenAusführung() {
        if (Platine.steuerungBenutzerProgramm(16 + aktuellElementeintrag) == 0) return false;
        BefehlshülleEinAusgabe.interaktivErlauben = true; BefehlshülleEinAusgabe.ausführenVorgang(false, false); Platine.umschaltenEinAusgabe(1);
        int verarbeitetWert = Platine.steuerungBenutzerProgramm(aktuellElementeintrag); BefehlshülleEinAusgabe.endung();
        if (verarbeitetWert != -1005) { fortsetzungLesen = false; BefehlshülleSatzbau.statuswertWert = verarbeitetWert < 0 ? 126 : verarbeitetWert; TerminalEinAusgabe.schreiben("exit "); TerminalEinAusgabe.Zahl(verarbeitetWert); TerminalEinAusgabe.Zeichen(10); Platine.terminal(3); }
        return true;
    }
}
