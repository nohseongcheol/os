// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Eingebaute Shell-Werkzeuge mit gemeinsamem RAM-VFS und gemeinsamer Standardein- und -ausgabe. */
public final class BefehlshülleWerkzeuge {
    static int[] Daten = new int[16384];
    static int eingabeDatei = -1;
    static int dateiÖffnen(int argumentIndex, int prozessBetriebsart) {
        int verarbeitetWert = Befehlsinterpreter.pfad(argumentIndex); return verarbeitetWert < 0 ? verarbeitetWert : SpeicherDateien.öffnen(prozessBetriebsart);
    }
    static boolean eingabeVorbereiten(int argumentIndex) {
        eingabeDatei = -1;
        if (argumentIndex < Befehlsinterpreter.wortzeichenAnzahl) {
            eingabeDatei = dateiÖffnen(argumentIndex, 0);
            if (eingabeDatei < 0) { Befehlsinterpreter.fehler(eingabeDatei); return false; }
        }
        return true;
    }
    static int lesen() {
        if (eingabeDatei >= 3) return SpeicherDateien.lesen(eingabeDatei);
        while (true) {
            int byteDaten = Platine.seriellLesen(); if (byteDaten == -2 || byteDaten == 4) return 256;
            if (byteDaten == 3) { Befehlsinterpreter.ergebnis = 130; return 256; }
            if (byteDaten >= 0) return byteDaten; Platine.prozessorAbgeben();
        }
    }
    static void schließen() { if (eingabeDatei >= 3) SpeicherDateien.schließen(eingabeDatei); eingabeDatei = -1; }
    static void ansichtWert() {
        int letzterPosition = Befehlsinterpreter.wortzeichenAnzahl == 1 ? 2 : Befehlsinterpreter.wortzeichenAnzahl;
        for (int argumentIndex = 1; argumentIndex < letzterPosition; argumentIndex++) {
            if (!eingabeVorbereiten(argumentIndex)) continue;
            int byteDaten; while ((byteDaten = lesen()) != 256 && byteDaten >= 0) Platine.seriellSchreiben(byteDaten);
            if (byteDaten < 0) Befehlsinterpreter.fehler(byteDaten); schließen();
        }
    }
    static void dateiAuftrag(String aktionNummer) {
        if (Befehlsinterpreter.wortzeichenAnzahl != 2) { Befehlsinterpreter.ergebnis = 2; TerminalEinAusgabe.schreiben("사용법: mkdir/rmdir/touch Datei\n"); return; }
        int verarbeitetWert = Befehlsinterpreter.pfad(1);
        if (verarbeitetWert >= 0) {
            if (aktionNummer.charAt(0) == 'm') verarbeitetWert = SpeicherDateien.verzeichnisErstellen();
            else if (aktionNummer.charAt(0) == 'r') verarbeitetWert = SpeicherDateien.verzeichnisEntfernen();
            else { verarbeitetWert = SpeicherDateien.öffnen(65); if (verarbeitetWert >= 3) verarbeitetWert = SpeicherDateien.schließen(verarbeitetWert); }
        }
        if (verarbeitetWert < 0) Befehlsinterpreter.fehler(verarbeitetWert);
    }
    static void wertKopieren(boolean hatVerschoben) {
        if (Befehlsinterpreter.wortzeichenAnzahl != 3) { Befehlsinterpreter.ergebnis = 2; TerminalEinAusgabe.schreiben("사용법: cp/mv ursprünglich zielEndpunkt (Datei)\n"); return; }
        int verarbeitetWert = Befehlsinterpreter.pfad(1); if (verarbeitetWert >= 0) verarbeitetWert = SpeicherDateien.wertNormalisieren();
        if (verarbeitetWert < 0) { Befehlsinterpreter.fehler(verarbeitetWert); return; }
        int ursprünglichNummer = SpeicherDateien.eintragFinden(); if (ursprünglichNummer < 0) { Befehlsinterpreter.fehler(-2); return; }
        int eintragAnzahl = SpeicherDateien.Länge[ursprünglichNummer]; for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) Daten[schleifeIndex] = SpeicherDateien.datenLesen(ursprünglichNummer, schleifeIndex);
        verarbeitetWert = Befehlsinterpreter.pfad(2); if (verarbeitetWert >= 0) verarbeitetWert = SpeicherDateien.wertNormalisieren();
        if (verarbeitetWert < 0) { Befehlsinterpreter.fehler(verarbeitetWert); return; }
        if (SpeicherDateien.eintragFinden() == ursprünglichNummer) { if (!hatVerschoben) Befehlsinterpreter.fehler(-22); return; }
        if (hatVerschoben) { verarbeitetWert = SpeicherDateien.eintragUmbenennen(ursprünglichNummer); if (verarbeitetWert < 0) Befehlsinterpreter.fehler(verarbeitetWert); return; }
        int geöffnetDateiNummer = SpeicherDateien.öffnen(577); if (geöffnetDateiNummer < 0) { Befehlsinterpreter.fehler(geöffnetDateiNummer); return; }
        for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) { verarbeitetWert = SpeicherDateien.schreiben(geöffnetDateiNummer, Daten[schleifeIndex]); if (verarbeitetWert < 0) { Befehlsinterpreter.fehler(verarbeitetWert); break; } }
        SpeicherDateien.schließen(geöffnetDateiNummer);
    }
    static int zifferWert(int argumentIndex) {
        if (argumentIndex >= Befehlsinterpreter.wortzeichenAnzahl) return -1;
        int eintragAnzahl = 0; for (int schleifeIndex = 0; schleifeIndex < Befehlsinterpreter.Länge[argumentIndex]; schleifeIndex++) { int zeichenKode = Befehlsinterpreter.wortzeichenWert[Befehlsinterpreter.beginnendPunkt[argumentIndex] + schleifeIndex]; if (zeichenKode < '0' || zeichenKode > '9' || eintragAnzahl > 10000) return -1; eintragAnzahl = eintragAnzahl * 10 + zeichenKode - '0'; } return eintragAnzahl;
    }
    static void zählendWert() {
        int argumentIndex = 1, wahlmöglichkeit = 0;
        if (Befehlsinterpreter.gleichText(1, "-c") || Befehlsinterpreter.gleichText(1, "-l") || Befehlsinterpreter.gleichText(1, "-w")) { wahlmöglichkeit = Befehlsinterpreter.gleichText(1, "-c") ? 1 : Befehlsinterpreter.gleichText(1, "-l") ? 2 : 3; argumentIndex++; }
        if (Befehlsinterpreter.wortzeichenAnzahl > argumentIndex + 1) { Befehlsinterpreter.ergebnis = 2; TerminalEinAusgabe.schreiben("사용법: wc [-c|-l|-w] [Datei]\n"); return; }
        if (!eingabeVorbereiten(argumentIndex)) return;
        int byteAnzahl = 0, zeilen = 0, lexikalischMaschinenwortAnzahl = 0, byteDaten; boolean lexikalischMaschinenwort = false;
        while ((byteDaten = lesen()) >= 0 && byteDaten != 256) { byteAnzahl++; if (byteDaten == 10) zeilen++; boolean raum = byteDaten == 32 || byteDaten >= 9 && byteDaten <= 13; if (!raum && !lexikalischMaschinenwort) lexikalischMaschinenwortAnzahl++; lexikalischMaschinenwort = !raum; }
        schließen(); if (byteDaten < 0) { Befehlsinterpreter.fehler(byteDaten); return; }
        if (wahlmöglichkeit != 0) TerminalEinAusgabe.Zahl(wahlmöglichkeit == 1 ? byteAnzahl : wahlmöglichkeit == 2 ? zeilen : lexikalischMaschinenwortAnzahl);
        else { TerminalEinAusgabe.Zahl(zeilen); TerminalEinAusgabe.Zeichen(' '); TerminalEinAusgabe.Zahl(lexikalischMaschinenwortAnzahl); TerminalEinAusgabe.Zeichen(' '); TerminalEinAusgabe.Zahl(byteAnzahl); } TerminalEinAusgabe.Zeichen(10);
    }
    static void eintragFinden() {
        if (Befehlsinterpreter.wortzeichenAnzahl < 2 || Befehlsinterpreter.wortzeichenAnzahl > 3) { Befehlsinterpreter.ergebnis = 2; TerminalEinAusgabe.schreiben("사용법: grep 찾을문구 [Datei]\n"); return; }
        if (!eingabeVorbereiten(2)) return;
        int eintragAnzahl = 0, byteDaten, übereinstimmungen = 0;
        while (true) {
            byteDaten = lesen();
            if (byteDaten == 10 || byteDaten == 256 || byteDaten < 0) {
                boolean warGefunden = false;
                for (int schleifeIndex = 0; schleifeIndex <= eintragAnzahl - Befehlsinterpreter.Länge[1]; schleifeIndex++) {
                    boolean istDerselbe = true; for (int innerlichPosition = 0; innerlichPosition < Befehlsinterpreter.Länge[1]; innerlichPosition++) if (Daten[schleifeIndex + innerlichPosition] != Befehlsinterpreter.wortzeichenWert[Befehlsinterpreter.beginnendPunkt[1] + innerlichPosition]) istDerselbe = false;
                    if (istDerselbe) warGefunden = true;
                }
                if (warGefunden && (eintragAnzahl > 0 || byteDaten == 10)) { for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) Platine.seriellSchreiben(Daten[schleifeIndex]); TerminalEinAusgabe.Zeichen(10); übereinstimmungen++; }
                eintragAnzahl = 0; if (byteDaten != 10) break;
            } else if (eintragAnzahl < Daten.length) Daten[eintragAnzahl++] = byteDaten;
            else { Befehlsinterpreter.fehler(-28); schließen(); return; }
        }
        schließen(); if (byteDaten < 0) Befehlsinterpreter.fehler(byteDaten); else if (Befehlsinterpreter.ergebnis == 0) Befehlsinterpreter.ergebnis = übereinstimmungen == 0 ? 1 : 0;
    }
    static void kopfWert(boolean hintenPosition) {
        int argumentIndex = 1, zeilen = 10;
        if (Befehlsinterpreter.gleichText(1, "-n")) { zeilen = zifferWert(2); argumentIndex = 3; }
        if (zeilen < 0 || Befehlsinterpreter.wortzeichenAnzahl > argumentIndex + 1) { Befehlsinterpreter.ergebnis = 2; TerminalEinAusgabe.schreiben("사용법: head/tail [-n zeilen] [Datei]\n"); return; }
        if (!eingabeVorbereiten(argumentIndex)) return;
        int eintragAnzahl = 0, byteDaten;
        while ((byteDaten = lesen()) != 256 && byteDaten >= 0) { if (eintragAnzahl == Daten.length) { Befehlsinterpreter.fehler(-28); schließen(); return; } Daten[eintragAnzahl++] = byteDaten; }
        schließen(); if (byteDaten < 0) { Befehlsinterpreter.fehler(byteDaten); return; }
        int lokalStarten = 0, endePosition = eintragAnzahl;
        if (zeilen == 0) return;
        if (hintenPosition) { int gesamtwertAnzahl = 0; for (int schleifeIndex = eintragAnzahl - 2; schleifeIndex >= 0; schleifeIndex--) if (Daten[schleifeIndex] == 10 && ++gesamtwertAnzahl == zeilen) { lokalStarten = schleifeIndex + 1; break; } }
        else { int gesamtwertAnzahl = 0; for (int schleifeIndex = 0; schleifeIndex < eintragAnzahl; schleifeIndex++) if (Daten[schleifeIndex] == 10 && ++gesamtwertAnzahl == zeilen) { endePosition = schleifeIndex + 1; break; } }
        for (int schleifeIndex = lokalStarten; schleifeIndex < endePosition; schleifeIndex++) Platine.seriellSchreiben(Daten[schleifeIndex]);
    }
    static void zusammenSchreiben() {
        boolean anhängen = Befehlsinterpreter.gleichText(1, "-a"); int argumentIndex = anhängen ? 2 : 1;
        if (Befehlsinterpreter.wortzeichenAnzahl != argumentIndex + 1) { Befehlsinterpreter.ergebnis = 2; TerminalEinAusgabe.schreiben("사용법: tee [-a] Datei\n"); return; }
        int geöffnetDateiNummer = dateiÖffnen(argumentIndex, anhängen ? 1089 : 577); if (geöffnetDateiNummer < 0) { Befehlsinterpreter.fehler(geöffnetDateiNummer); return; }
        eingabeDatei = -1; int byteDaten;
        while ((byteDaten = lesen()) != 256 && byteDaten >= 0) { int verarbeitetWert = SpeicherDateien.schreiben(geöffnetDateiNummer, byteDaten); if (verarbeitetWert < 0) { Befehlsinterpreter.fehler(verarbeitetWert); break; } Platine.seriellSchreiben(byteDaten); }
        SpeicherDateien.schließen(geöffnetDateiNummer);
    }
}
