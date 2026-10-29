// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Erste Pi4-Portierung des eigenständigen Java-Kernels. Läuft direkt, nicht auf Linux oder einer Host-JVM. */
public final class Betriebskern {
    static int[] aufgabeWiederholungsanzahl = new int[3];
    static int[] aufgabeSumme = new int[3];
    static int aufgabeReihenfolge;
    static int aufgabeFehler;
    static int zufälligStartwert = 17;

    static void überprüfen(boolean bedingung, int Nummer) {
        if (!bedingung) { TerminalEinAusgabe.schreiben("FAIL "); TerminalEinAusgabe.Zahl(Nummer); Platine.stoppen(Nummer); }
    }
    static int verzweigung(int Wert) {
        switch (Wert) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int dichtUmschalten(int Wert) {
        switch (Wert) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] zurückkehrenDatenfeld(int[] datenfeldWert) { return datenfeldWert; }
    static void arithmetikPrüfung() {
        int Wert = zufälligStartwert;
        überprüfen(Wert * 7 - Wert == 102 && Wert / 3 == 5 && Wert % 3 == 2, 1);
        int mindestwertGanzzahl = 0x80000000, negativEins = -1;
        überprüfen(mindestwertGanzzahl / negativEins == mindestwertGanzzahl && mindestwertGanzzahl % negativEins == 0, 2);
        überprüfen(mindestwertGanzzahl + mindestwertGanzzahl == 0 && -mindestwertGanzzahl == mindestwertGanzzahl, 3);
        überprüfen((-Wert >> 2) == -5 && (-Wert >>> 2) == 1073741819 && (Wert << 33) == 34, 4);
        überprüfen((byte)(Wert * 16) == 16 && (short)65535 == -1 && (char)negativEins == 65535, 5);
        int[] datenfeldWert = new int[5];
        for (int schleifeIndex = 0; schleifeIndex < datenfeldWert.length; schleifeIndex++) datenfeldWert[schleifeIndex] = schleifeIndex * Wert;
        datenfeldWert[2]++;
        überprüfen(zurückkehrenDatenfeld(datenfeldWert) == datenfeldWert && datenfeldWert[2] == 35 && datenfeldWert[4] == 68, 6);
        überprüfen(verzweigung(Wert - 117) == 7 && verzweigung(Wert - 15) == 9 && verzweigung(Wert) == 3 && dichtUmschalten(Wert - 15) == 17, 7);
        String Text = "한글 😀";
        überprüfen(Text.length() == 5 && Text.charAt(0) == '한' && Text.charAt(3) == 0xd83d, 8);
        überprüfen(Platine.cPUVorrechtEbene() == 1, 9);
        TerminalEinAusgabe.schreiben("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void Aufgabe(int Nummer) {
        // Prüfen, ob lokale Variablen die Ausführungsabgabe überstehen: Jede Aufgabe hat einen eigenen Maschinenstapel.
        int lokalWert = Nummer * 100;
        for (int schleifeIndex = 0; schleifeIndex < 10; schleifeIndex++) {
            if (aufgabeReihenfolge % 2 + 1 != Nummer) aufgabeFehler++;
            aufgabeReihenfolge++;
            lokalWert += schleifeIndex + Nummer;
            aufgabeSumme[Nummer] = lokalWert;
            aufgabeWiederholungsanzahl[Nummer]++;
            Platine.prozessorAbgeben();
            if (lokalWert != aufgabeSumme[Nummer]) aufgabeFehler++;
        }
    }
    static void aufgabenPrüfung() {
        aufgabeReihenfolge = 0; aufgabeFehler = 0;
        aufgabeWiederholungsanzahl[1] = 0; aufgabeWiederholungsanzahl[2] = 0;
        überprüfen(Platine.aufgabeErstellen(1) == 0 && Platine.aufgabeErstellen(2) == 0, 20);
        int drehungAnzahl = 0;
        while (Platine.aufgabeStatuswert(1) != 0 || Platine.aufgabeStatuswert(2) != 0) {
            Platine.prozessorAbgeben();
            überprüfen(++drehungAnzahl < 100, 21);
        }
        überprüfen(aufgabeWiederholungsanzahl[1] == 10 && aufgabeWiederholungsanzahl[2] == 10 && aufgabeReihenfolge == 20 && aufgabeFehler == 0, 22);
        überprüfen(aufgabeSumme[1] == 155 && aufgabeSumme[2] == 265, 23);
        TerminalEinAusgabe.schreiben("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void rechteck(int waagerechtPosition, int senkrechtPosition, int breiteWert, int höheWert, int farbeWert) {
        for (int senkrechteKoordinateKoordinate = senkrechtPosition; senkrechteKoordinateKoordinate < senkrechtPosition + höheWert; senkrechteKoordinateKoordinate++)
            for (int waagerechteKoordinateKoordinate = waagerechtPosition; waagerechteKoordinateKoordinate < waagerechtPosition + breiteWert; waagerechteKoordinateKoordinate++) Platine.bildschirmBildpunktAblegen(waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate, farbeWert);
    }
    static void Bildschirm() {
        if (Platine.bildschirmVorbereiten() == 0) { TerminalEinAusgabe.schreiben("FRAMEBUFFER unavailable\n"); return; }
        rechteck(0, 0, Platine.bildschirmBreite(), Platine.bildschirmHöhe(), 0x302018);
        rechteck(40, 40, 560, 400, 0xefe8e2);
        rechteck(40, 40, 560, 40, 0x905020);
        rechteck(60, 110, 240, 140, 0x90b050);
        rechteck(320, 110, 260, 140, 0xd0a040);
        rechteck(60, 290, 520, 120, 0xd8d0c8);
        TerminalEinAusgabe.schreiben("FRAMEBUFFER PASS "); TerminalEinAusgabe.Zahl(Platine.bildschirmBreite()); TerminalEinAusgabe.Zeichen('x');
        TerminalEinAusgabe.Zahl(Platine.bildschirmHöhe()); TerminalEinAusgabe.schreiben(" RGB32 (drawing only)\n");
    }
    static void cPrüfung() {
        int ergebnis = Platine.cppPrüfung();
        überprüfen(ergebnis == 0, 100 + ergebnis);
        TerminalEinAusgabe.schreiben("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void benutzerProgrammePrüfung() {
        überprüfen(Platine.benutzerProgrammPrüfen() == 0, 200);
        TerminalEinAusgabe.schreiben("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int anfänglichErgebnis = Platine.benutzerProgrammAusführenVorgang(0);
        if (anfänglichErgebnis != 0) { TerminalEinAusgabe.schreiben("USER DEMO RESULT "); TerminalEinAusgabe.Zahl(anfänglichErgebnis); TerminalEinAusgabe.Zeichen(10); }
        überprüfen(anfänglichErgebnis == 0, 201);
        TerminalEinAusgabe.schreiben("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] erwartetWerte = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int Nummer = 0; Nummer < erwartetWerte.length; Nummer++) {
            TerminalEinAusgabe.schreiben("USER CHECK "); TerminalEinAusgabe.Zahl(Nummer); TerminalEinAusgabe.Zeichen(10);
            int ergebnis = Platine.benutzerProgrammAusführenVorgang(Nummer + 1);
            if (ergebnis != erwartetWerte[Nummer]) { TerminalEinAusgabe.schreiben("USER RESULT "); TerminalEinAusgabe.Zahl(ergebnis); TerminalEinAusgabe.Zeichen(10); }
            überprüfen(ergebnis == erwartetWerte[Nummer], 210 + Nummer);
        }
        überprüfen(Platine.benutzerProgrammAusführenVorgang(0) == 0, 220);
        TerminalEinAusgabe.schreiben("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void netzbetriebPrüfung() {
        int ergebnis = Platine.benutzerProgrammAusführenVorgang(9);
        if (ergebnis != 0) { TerminalEinAusgabe.schreiben("UDP RESULT "); TerminalEinAusgabe.Zahl(ergebnis); TerminalEinAusgabe.Zeichen(10); }
        überprüfen(ergebnis == 0, 230);
    }
    static void systemInformation() {
        TerminalEinAusgabe.schreiben("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        TerminalEinAusgabe.schreiben("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        TerminalEinAusgabe.schreiben("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        TerminalEinAusgabe.schreiben("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        TerminalEinAusgabe.schreiben("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void ausführenVorgang() {
        TerminalEinAusgabe.schreiben("WorldOS de · Guten Tag · 😀\n");
        arithmetikPrüfung();
        cPrüfung();
        aufgabenPrüfung();
        Bildschirm();
        benutzerProgrammePrüfung();
        netzbetriebPrüfung();
        TerminalEinAusgabe.schreiben("NATIVE READY\n");
        Befehlsinterpreter.befehlAusführen();
    }
}
