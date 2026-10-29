// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Verbindungsorientierte Byteströme im Kernel: eine lokale socket-Schicht, kein Ethernet/TCP-Paketstapel. */
public final class DatenstromNetzwerk {
    static int[] statuswertWert = new int[16], portWert = new int[16], gepaartWert = new int[16], gegenstellePort = new int[16], wertWarten = new int[16], istGebunden = new int[16];
    static int[] vorderseiteWert = new int[16], Zahl = new int[16], Daten = new int[16 * 1024];
    static int nächsterElementeintrag = 50000;
    static int überprüfen(int geöffnetDateiNummer) { return geöffnetDateiNummer >= 40 && geöffnetDateiNummer < 56 && statuswertWert[geöffnetDateiNummer - 40] != 0 ? geöffnetDateiNummer - 40 : -1; }
    static boolean istEingehendBenutzen(int portNummer) { for (int schleifeIndex = 0; schleifeIndex < 16; schleifeIndex++) if (statuswertWert[schleifeIndex] != 0 && istGebunden[schleifeIndex] != 0 && portWert[schleifeIndex] == portNummer) return true; return false; }
    public static int eintragErstellen() {
        for (int schleifeIndex = 0; schleifeIndex < 16; schleifeIndex++) if (statuswertWert[schleifeIndex] == 0) { statuswertWert[schleifeIndex] = 1; gegenstellePort[schleifeIndex] = portWert[schleifeIndex] = vorderseiteWert[schleifeIndex] = Zahl[schleifeIndex] = wertWarten[schleifeIndex] = istGebunden[schleifeIndex] = 0; gepaartWert[schleifeIndex] = -1; return schleifeIndex + 40; }
        return -24;
    }
    public static int AusführbündelPacken(int geöffnetDateiNummer, int NetzbuchseAdresse, int portNummer) {
        int schleifeIndex = überprüfen(geöffnetDateiNummer); if (schleifeIndex < 0) return -9;
        if (NetzbuchseAdresse != 0 && NetzbuchseAdresse != 0x7f000001) return -99;
        if (statuswertWert[schleifeIndex] != 1 || portNummer < 0 || portNummer > 65535) return -22;
        if (portNummer == 0) { do { portNummer = nächsterElementeintrag++; if (nächsterElementeintrag > 65535) nächsterElementeintrag = 50000; } while (istEingehendBenutzen(portNummer)); }
        if (istEingehendBenutzen(portNummer)) return -98; portWert[schleifeIndex] = portNummer; istGebunden[schleifeIndex] = 1; statuswertWert[schleifeIndex] = 2; return 0;
    }
    public static int endpunktLauschen(int geöffnetDateiNummer, int wartebestand) { int schleifeIndex = überprüfen(geöffnetDateiNummer); if (schleifeIndex < 0) return -9; if (statuswertWert[schleifeIndex] != 2 || wartebestand < 1) return -22; statuswertWert[schleifeIndex] = 3; return 0; }
    public static int verbinden(int geöffnetDateiNummer, int NetzbuchseAdresse, int portNummer) {
        int schleifeIndex = überprüfen(geöffnetDateiNummer); if (schleifeIndex < 0) return -9; if (NetzbuchseAdresse != 0x7f000001) return -101;
        if (portNummer < 1 || portNummer > 65535 || statuswertWert[schleifeIndex] > 2) return -22;
        int seiteEmpfangen = -1; for (int innerlichPosition = 0; innerlichPosition < 16; innerlichPosition++) if (statuswertWert[innerlichPosition] == 3 && portWert[innerlichPosition] == portNummer) seiteEmpfangen = innerlichPosition;
        if (seiteEmpfangen < 0) return -111;
        int istEingereiht = 0; for (int innerlichPosition = 0; innerlichPosition < 16; innerlichPosition++) if (wertWarten[innerlichPosition] == seiteEmpfangen + 1) istEingereiht++;
        if (istEingereiht >= 4) return -11;
        if (statuswertWert[schleifeIndex] == 1) { int verarbeitetWert = AusführbündelPacken(geöffnetDateiNummer, 0x7f000001, 0); if (verarbeitetWert < 0) return verarbeitetWert; }
        int anderer = eintragErstellen(); if (anderer < 0) return anderer; anderer -= 40;
        statuswertWert[schleifeIndex] = statuswertWert[anderer] = 4; gepaartWert[schleifeIndex] = anderer; gepaartWert[anderer] = schleifeIndex; portWert[anderer] = portNummer; gegenstellePort[schleifeIndex] = portNummer; gegenstellePort[anderer] = portWert[schleifeIndex]; wertWarten[anderer] = seiteEmpfangen + 1; return 0;
    }
    public static int verbindungAnnehmen(int geöffnetDateiNummer) { int schleifeIndex = überprüfen(geöffnetDateiNummer); if (schleifeIndex < 0) return -9; if (statuswertWert[schleifeIndex] != 3) return -22; for (int innerlichPosition = 0; innerlichPosition < 16; innerlichPosition++) if (statuswertWert[innerlichPosition] != 0 && wertWarten[innerlichPosition] == schleifeIndex + 1) { wertWarten[innerlichPosition] = 0; return innerlichPosition + 40; } return -11; }
    public static int schreiben(int geöffnetDateiNummer, int eintragAnzahl) {
        int schleifeIndex = überprüfen(geöffnetDateiNummer); if (schleifeIndex < 0) return -9; if (statuswertWert[schleifeIndex] != 4) return -107;
        if (eintragAnzahl < 0 || eintragAnzahl > 512) return -22; if (eintragAnzahl == 0) return 0;
        int innerlichPosition = gepaartWert[schleifeIndex]; if (innerlichPosition < 0) return -32; int gesamtwertAnzahl = 1024 - Zahl[innerlichPosition]; if (gesamtwertAnzahl == 0) return -11; if (gesamtwertAnzahl > eintragAnzahl) gesamtwertAnzahl = eintragAnzahl;
        for (int vergleichPosition = 0; vergleichPosition < gesamtwertAnzahl; vergleichPosition++) Daten[innerlichPosition * 1024 + (vorderseiteWert[innerlichPosition] + Zahl[innerlichPosition] + vergleichPosition) % 1024] = RückschleifeNetzwerk.vorwärtsWert[vergleichPosition]; Zahl[innerlichPosition] += gesamtwertAnzahl; return gesamtwertAnzahl;
    }
    public static int lesen(int geöffnetDateiNummer, int eintragAnzahl) {
        int schleifeIndex = überprüfen(geöffnetDateiNummer); if (schleifeIndex < 0) return -9; if (statuswertWert[schleifeIndex] != 4) return -107; if (eintragAnzahl < 0 || eintragAnzahl > 512) return -22;
        if (eintragAnzahl == 0) return 0; if (Zahl[schleifeIndex] == 0) return gepaartWert[schleifeIndex] < 0 ? 0 : -11; if (eintragAnzahl > Zahl[schleifeIndex]) eintragAnzahl = Zahl[schleifeIndex];
        for (int vergleichPosition = 0; vergleichPosition < eintragAnzahl; vergleichPosition++) RückschleifeNetzwerk.vorwärtsWert[vergleichPosition] = Daten[schleifeIndex * 1024 + (vorderseiteWert[schleifeIndex] + vergleichPosition) % 1024]; vorderseiteWert[schleifeIndex] = (vorderseiteWert[schleifeIndex] + eintragAnzahl) % 1024; Zahl[schleifeIndex] -= eintragAnzahl; return eintragAnzahl;
    }
    public static int endpunktPortLesen(int geöffnetDateiNummer) { int schleifeIndex = überprüfen(geöffnetDateiNummer); return schleifeIndex < 0 ? -9 : portWert[schleifeIndex]; }
    public static int gegenstellePortLesen(int geöffnetDateiNummer) { int schleifeIndex = überprüfen(geöffnetDateiNummer); return schleifeIndex < 0 ? -9 : gegenstellePort[schleifeIndex]; }
    public static int schließen(int geöffnetDateiNummer) {
        int schleifeIndex = überprüfen(geöffnetDateiNummer); if (schleifeIndex < 0) return -9;
        if (statuswertWert[schleifeIndex] == 3) for (int innerlichPosition = 0; innerlichPosition < 16; innerlichPosition++) if (wertWarten[innerlichPosition] == schleifeIndex + 1) { if (gepaartWert[innerlichPosition] >= 0) gepaartWert[gepaartWert[innerlichPosition]] = -1; statuswertWert[innerlichPosition] = wertWarten[innerlichPosition] = istGebunden[innerlichPosition] = 0; }
        if (gepaartWert[schleifeIndex] >= 0) gepaartWert[gepaartWert[schleifeIndex]] = -1; statuswertWert[schleifeIndex] = istGebunden[schleifeIndex] = Zahl[schleifeIndex] = wertWarten[schleifeIndex] = 0; return 0;
    }
}
