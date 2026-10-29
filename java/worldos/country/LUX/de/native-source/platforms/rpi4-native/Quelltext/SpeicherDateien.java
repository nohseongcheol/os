// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 64 RAM-Dateien mit je 16384 Byte, 16 Deskriptoren. Alle Daten und Regeln liegen in Java. Aufrufe geben die Ausführung nicht ab und sind daher zwischen kooperativen Aufgaben auf dem derzeitigen Einzelkern atomar. Dies ist weder Plattenspeicherung noch eine vollständige POSIX-Implementierung. Negative Rückgaben sind Fehlernummern. */
public final class SpeicherDateien {
    static final int dateiAnzahl = 64;
    static int[] Name = new int[dateiAnzahl * 64];
    static int[] namenlänge = new int[dateiAnzahl];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] inhaltswertWert = new int[dateiAnzahl * 4096];
    static int[] Länge = new int[dateiAnzahl];
    static int[] verweisAnzahl = new int[dateiAnzahl];
    static int[] benutzenWert = new int[16];
    static int[] zielobjektWert = new int[16];
    static int[] position = new int[16];
    static int[] methodeBetriebsart = new int[16];
    static int[] pfad = new int[64];
    static int pfadLänge;

    public static int dateiGrenzwert() { return dateiAnzahl; }
    static int datenLesen(int Datei, int positionIndex) { return (inhaltswertWert[Datei * 4096 + positionIndex / 4] >>> ((positionIndex & 3) * 8)) & 255; }
    static void datenSchreiben(int Datei, int positionIndex, int Wert) {
        int platzEintrag = Datei * 4096 + positionIndex / 4, bewegenWert = (positionIndex & 3) * 8;
        inhaltswertWert[platzEintrag] = (inhaltswertWert[platzEintrag] & ~(255 << bewegenWert)) | ((Wert & 255) << bewegenWert);
    }

    public static int pfadStarten(int größe) {
        pfadLänge = 0;
        if (größe < 1 || größe > 63) return -36;
        pfadLänge = größe;
        for (int schleifeIndex = 0; schleifeIndex < größe; schleifeIndex++) pfad[schleifeIndex] = 0;
        return 0;
    }
    public static int pfadByte(int Nummer, int Wert) {
        if (Nummer < 0 || Nummer >= pfadLänge || Wert < 1 || Wert > 255) return -22;
        pfad[Nummer] = Wert; return 0;
    }
    static int eintragFinden() {
        for (int dateiIndex = 0; dateiIndex < dateiAnzahl; dateiIndex++) if (namenlänge[dateiIndex] > 0 && namenlänge[dateiIndex] == kanonischLänge && vorsilbeWert(Name, dateiIndex * 64, namenlänge[dateiIndex], kanonischWert, kanonischLänge)) return dateiIndex;
        return -1;
    }
    public static int öffnen(int merkmalbitsWert) {
        if (pfadLänge == 0 || (merkmalbitsWert & ~0x6c3) != 0 || (merkmalbitsWert & 3) == 3) return -22;
        for (int schleifeIndex = 0; schleifeIndex < pfadLänge; schleifeIndex++) if (pfad[schleifeIndex] == 0) return -22;
        if ((merkmalbitsWert & 0x200) != 0 && (merkmalbitsWert & 3) == 0) return -22;
        int ergebnis = wertNormalisieren(); if (ergebnis < 0) return ergebnis;
        if (verzeichnisFinden(kanonischLänge) >= 0) return -21;
        ergebnis = elternknotenPrüfen(); if (ergebnis < 0) return ergebnis;
        int Datei = eintragFinden();
        if (Datei >= 0 && (merkmalbitsWert & 0xc0) == 0xc0) return -17;
        if (Datei < 0 && (merkmalbitsWert & 0x40) == 0) return -2;
        int deskriptorEintrag = -1;
        for (int schleifeIndex = 0; schleifeIndex < 16; schleifeIndex++) if (benutzenWert[schleifeIndex] == 0) { deskriptorEintrag = schleifeIndex; break; }
        if (deskriptorEintrag < 0) return -24;
        if (Datei < 0) {
            for (int schleifeIndex = 0; schleifeIndex < dateiAnzahl; schleifeIndex++) if (namenlänge[schleifeIndex] == 0 && verweisAnzahl[schleifeIndex] == 0) { Datei = schleifeIndex; break; }
            if (Datei < 0) return -28;
            namenlänge[Datei] = kanonischLänge;
            for (int schleifeIndex = 0; schleifeIndex < kanonischLänge; schleifeIndex++) Name[Datei * 64 + schleifeIndex] = kanonischWert[schleifeIndex];
            Länge[Datei] = 0;
        }
        if ((merkmalbitsWert & 0x200) != 0) Länge[Datei] = 0;
        benutzenWert[deskriptorEintrag] = 1; zielobjektWert[deskriptorEintrag] = Datei; position[deskriptorEintrag] = 0; methodeBetriebsart[deskriptorEintrag] = merkmalbitsWert;
        verweisAnzahl[Datei]++;
        return deskriptorEintrag + 3;
    }
    static int überprüfen(int deskriptorEintrag) {
        return deskriptorEintrag >= 3 && deskriptorEintrag < 19 && benutzenWert[deskriptorEintrag - 3] != 0 ? deskriptorEintrag - 3 : -1;
    }
    public static int lesen(int deskriptorEintrag) {
        int platzEintrag = überprüfen(deskriptorEintrag);
        if (platzEintrag < 0 || (methodeBetriebsart[platzEintrag] & 3) == 1) return -9;
        int Datei = zielobjektWert[platzEintrag];
        if (position[platzEintrag] >= Länge[Datei]) return 256; // EOF von tatsächlichen Bytes 0x00..0xff unterscheiden.
        return datenLesen(Datei, position[platzEintrag]++);
    }
    public static int schreiben(int deskriptorEintrag, int Wert) {
        int platzEintrag = überprüfen(deskriptorEintrag);
        if (platzEintrag < 0 || (methodeBetriebsart[platzEintrag] & 3) == 0) return -9;
        int Datei = zielobjektWert[platzEintrag];
        if ((methodeBetriebsart[platzEintrag] & 0x400) != 0) position[platzEintrag] = Länge[Datei];
        if (position[platzEintrag] >= 16384) return -28;
        while (Länge[Datei] < position[platzEintrag]) datenSchreiben(Datei, Länge[Datei]++, 0);
        datenSchreiben(Datei, position[platzEintrag]++, Wert);
        if (Länge[Datei] < position[platzEintrag]) Länge[Datei] = position[platzEintrag];
        return 1;
    }
    public static int positionPositionieren(int deskriptorEintrag, int entfernungWert, int projektWurzel) {
        int platzEintrag = überprüfen(deskriptorEintrag);
        if (platzEintrag < 0) return -9;
        if (projektWurzel < 0 || projektWurzel > 2 || entfernungWert < -16384 || entfernungWert > 16384) return -22;
        int neuPosition = entfernungWert + (projektWurzel == 0 ? 0 : projektWurzel == 1 ? position[platzEintrag] : Länge[zielobjektWert[platzEintrag]]);
        if (neuPosition < 0 || neuPosition > 16384) return -22;
        position[platzEintrag] = neuPosition; return neuPosition;
    }
    public static int schließen(int deskriptorEintrag) {
        int platzEintrag = überprüfen(deskriptorEintrag);
        if (platzEintrag < 0) return -9;
        verweisAnzahl[zielobjektWert[platzEintrag]]--; benutzenWert[platzEintrag] = 0; return 0;
    }
    public static int größe(int deskriptorEintrag) {
        int platzEintrag = überprüfen(deskriptorEintrag); return platzEintrag < 0 ? -9 : Länge[zielobjektWert[platzEintrag]];
    }
    public static int längeSetzen(int deskriptorEintrag, int größe) {
        int platzEintrag = überprüfen(deskriptorEintrag);
        if (platzEintrag < 0 || (methodeBetriebsart[platzEintrag] & 3) == 0) return -9;
        if (größe < 0 || größe > 16384) return -22;
        int Datei = zielobjektWert[platzEintrag];
        while (Länge[Datei] < größe) datenSchreiben(Datei, Länge[Datei]++, 0);
        Länge[Datei] = größe; return 0;
    }
    public static int eintragTilgen() {
        if (pfadLänge == 0) return -22;
        int ergebnis = wertNormalisieren(); if (ergebnis < 0) return ergebnis;
        if (verzeichnisFinden(kanonischLänge) >= 0) return -21;
        ergebnis = elternknotenPrüfen(); if (ergebnis < 0) return ergebnis;
        int Datei = eintragFinden();
        if (Datei < 0) return -2;
        namenlänge[Datei] = 0; return 0; // Eine geöffnete Datei bis zum letzten close behalten.
    }
    static void eintragListe() {
        pfadStarten(1); pfadByte(0, '.'); pfadEinträge();
    }
    public static int exportiertNameLänge(int Nummer) {
        if (Nummer < 0 || Nummer >= dateiAnzahl || namenlänge[Nummer] == 0) return 0;
        for (int schleifeIndex = 0; schleifeIndex < namenlänge[Nummer]; schleifeIndex++) if (Name[Nummer * 64 + schleifeIndex] == '/') return 0;
        return namenlänge[Nummer];
    }
    public static int exportiertNameByte(int Nummer, int positionIndex) {
        return Nummer >= 0 && Nummer < dateiAnzahl && positionIndex >= 0 && positionIndex < namenlänge[Nummer] ? Name[Nummer * 64 + positionIndex] : -22;
    }
    public static int exportiertDateiGröße(int Nummer) { return Nummer >= 0 && Nummer < dateiAnzahl ? Länge[Nummer] : -22; }
    static int[] kanonischWert = new int[64], aktuellElementeintrag = new int[64], verzeichnisName = new int[16 * 64], verzeichnisLänge = new int[16];
    static int kanonischLänge, aktuellLänge;
    static boolean vorsilbeWert(int[] namenListe, int ausführenVorgang, int pfadWert, int[] vorderseiteWert, int voranstehendPfad) {
        if (pfadWert < voranstehendPfad) return false;
        for (int schleifeIndex = 0; schleifeIndex < voranstehendPfad; schleifeIndex++) if (namenListe[ausführenVorgang + schleifeIndex] != vorderseiteWert[schleifeIndex]) return false;
        return true;
    }
    static int wertNormalisieren() {
        if (pfadLänge == 0) return -22;
        kanonischLänge = pfad[0] == '/' ? 0 : aktuellLänge;
        for (int schleifeIndex = 0; schleifeIndex < kanonischLänge; schleifeIndex++) kanonischWert[schleifeIndex] = aktuellElementeintrag[schleifeIndex];
        int mauszeigerLesen = 0;
        while (mauszeigerLesen < pfadLänge) {
            while (mauszeigerLesen < pfadLänge && pfad[mauszeigerLesen] == '/') mauszeigerLesen++;
            int positionStarten = mauszeigerLesen; while (mauszeigerLesen < pfadLänge && pfad[mauszeigerLesen] != '/') { if (pfad[mauszeigerLesen] == 0) return -22; mauszeigerLesen++; }
            int eintragAnzahl = mauszeigerLesen - positionStarten; if (eintragAnzahl == 0 || eintragAnzahl == 1 && pfad[positionStarten] == '.') continue;
            if (eintragAnzahl == 2 && pfad[positionStarten] == '.' && pfad[positionStarten + 1] == '.') {
                while (kanonischLänge > 0 && kanonischWert[kanonischLänge - 1] != '/') kanonischLänge--;
                if (kanonischLänge > 0) kanonischLänge--;
                continue;
            }
            if (kanonischLänge + eintragAnzahl + (kanonischLänge == 0 ? 0 : 1) > 63) return -36;
            if (kanonischLänge > 0) kanonischWert[kanonischLänge++] = '/';
            for (int schleifeIndex = positionStarten; schleifeIndex < mauszeigerLesen; schleifeIndex++) kanonischWert[kanonischLänge++] = pfad[schleifeIndex];
        }
        return 0;
    }
    static int verzeichnisFinden(int eintragAnzahl) {
        if (eintragAnzahl == 0) return 0;
        for (int schleifeIndex = 1; schleifeIndex < 16; schleifeIndex++) if (verzeichnisLänge[schleifeIndex] == eintragAnzahl && vorsilbeWert(verzeichnisName, schleifeIndex * 64, eintragAnzahl, kanonischWert, eintragAnzahl)) return schleifeIndex;
        return -1;
    }
    static int elternknotenPrüfen() {
        int eintragAnzahl = kanonischLänge; while (eintragAnzahl > 0 && kanonischWert[eintragAnzahl - 1] != '/') eintragAnzahl--;
        return verzeichnisFinden(eintragAnzahl == 0 ? 0 : eintragAnzahl - 1) < 0 ? -2 : 0;
    }
    public static int verzeichnisErstellen() {
        int verarbeitetWert = wertNormalisieren(); if (verarbeitetWert < 0) return verarbeitetWert;
        if (verzeichnisFinden(kanonischLänge) >= 0 || eintragFinden() >= 0) return -17;
        verarbeitetWert = elternknotenPrüfen(); if (verarbeitetWert < 0) return verarbeitetWert;
        for (int schleifeIndex = 1; schleifeIndex < 16; schleifeIndex++) if (verzeichnisLänge[schleifeIndex] == 0) {
            verzeichnisLänge[schleifeIndex] = kanonischLänge; for (int innerlichPosition = 0; innerlichPosition < kanonischLänge; innerlichPosition++) verzeichnisName[schleifeIndex * 64 + innerlichPosition] = kanonischWert[innerlichPosition]; return 0;
        }
        return -28;
    }
    public static int eintragArt() {
        int verarbeitetWert = wertNormalisieren(); if (verarbeitetWert < 0) return verarbeitetWert;
        if (verzeichnisFinden(kanonischLänge) >= 0) return 2;
        return eintragFinden() >= 0 ? 1 : 0;
    }
    public static int verzeichnisÄndern() {
        int verarbeitetWert = wertNormalisieren(); if (verarbeitetWert < 0) return verarbeitetWert;
        if (verzeichnisFinden(kanonischLänge) < 0) return -2;
        aktuellLänge = kanonischLänge; for (int schleifeIndex = 0; schleifeIndex < aktuellLänge; schleifeIndex++) aktuellElementeintrag[schleifeIndex] = kanonischWert[schleifeIndex]; return 0;
    }
    public static int verzeichnisEntfernen() {
        int verarbeitetWert = wertNormalisieren(); if (verarbeitetWert < 0) return verarbeitetWert;
        int verzeichnisNummer = verzeichnisFinden(kanonischLänge); if (verzeichnisNummer < 0) return -2; if (verzeichnisNummer == 0) return -16;
        if (aktuellLänge == kanonischLänge && vorsilbeWert(aktuellElementeintrag, 0, aktuellLänge, kanonischWert, kanonischLänge)) return -16;
        for (int schleifeIndex = 0; schleifeIndex < dateiAnzahl; schleifeIndex++) {
            if (namenlänge[schleifeIndex] > kanonischLänge && vorsilbeWert(Name, schleifeIndex * 64, namenlänge[schleifeIndex], kanonischWert, kanonischLänge) && Name[schleifeIndex * 64 + kanonischLänge] == '/') return -39;
        }
        for (int schleifeIndex = 0; schleifeIndex < 16; schleifeIndex++) {
            if (verzeichnisLänge[schleifeIndex] > kanonischLänge && vorsilbeWert(verzeichnisName, schleifeIndex * 64, verzeichnisLänge[schleifeIndex], kanonischWert, kanonischLänge) && verzeichnisName[schleifeIndex * 64 + kanonischLänge] == '/') return -39;
        }
        verzeichnisLänge[verzeichnisNummer] = 0; return 0;
    }
    public static int eintragUmbenennen(int ursprünglichNummer) {
        if (ursprünglichNummer < 0 || ursprünglichNummer >= dateiAnzahl || namenlänge[ursprünglichNummer] == 0) return -2;
        int verarbeitetWert = wertNormalisieren(); if (verarbeitetWert < 0) return verarbeitetWert;
        if (verzeichnisFinden(kanonischLänge) >= 0) return -21;
        verarbeitetWert = elternknotenPrüfen(); if (verarbeitetWert < 0) return verarbeitetWert;
        int vorherigWert = eintragFinden(); if (vorherigWert == ursprünglichNummer) return 0;
        if (vorherigWert >= 0) namenlänge[vorherigWert] = 0;
        namenlänge[ursprünglichNummer] = kanonischLänge; for (int schleifeIndex = 0; schleifeIndex < kanonischLänge; schleifeIndex++) Name[ursprünglichNummer * 64 + schleifeIndex] = kanonischWert[schleifeIndex]; return 0;
    }
    static int eintragStarten(int[] datenDatenfeld, int beginnendPunkt, int eintragAnzahl) {
        if (!vorsilbeWert(datenDatenfeld, beginnendPunkt, eintragAnzahl, kanonischWert, kanonischLänge)) return -1;
        int positionStarten = kanonischLänge;
        if (positionStarten > 0) { if (eintragAnzahl <= positionStarten || datenDatenfeld[beginnendPunkt + positionStarten] != '/') return -1; positionStarten++; }
        if (eintragAnzahl <= positionStarten) return -1;
        for (int schleifeIndex = positionStarten; schleifeIndex < eintragAnzahl; schleifeIndex++) if (datenDatenfeld[beginnendPunkt + schleifeIndex] == '/') return -1;
        return positionStarten;
    }
    static void aktuellSchreiben() { TerminalEinAusgabe.Zeichen('/'); for (int schleifeIndex = 0; schleifeIndex < aktuellLänge; schleifeIndex++) Platine.seriellSchreiben(aktuellElementeintrag[schleifeIndex]); }
    static int pfadEinträge() {
        int verarbeitetWert = wertNormalisieren(); if (verarbeitetWert < 0) return verarbeitetWert;
        int dateiZielobjektWert = eintragFinden();
        if (dateiZielobjektWert >= 0) { for (int schleifeIndex = 0; schleifeIndex < kanonischLänge; schleifeIndex++) Platine.seriellSchreiben(kanonischWert[schleifeIndex]); TerminalEinAusgabe.schreiben("  "); TerminalEinAusgabe.Zahl(Länge[dateiZielobjektWert]); TerminalEinAusgabe.schreiben("byteWert(주기억 Datei)\n"); return 0; }
        if (verzeichnisFinden(kanonischLänge) < 0) return -2;
        for (int nachlaufendWert = 1; nachlaufendWert < 16; nachlaufendWert++) if (verzeichnisLänge[nachlaufendWert] > 0) {
            int positionStarten = eintragStarten(verzeichnisName, nachlaufendWert * 64, verzeichnisLänge[nachlaufendWert]); if (positionStarten < 0) continue;
            for (int schleifeIndex = positionStarten; schleifeIndex < verzeichnisLänge[nachlaufendWert]; schleifeIndex++) Platine.seriellSchreiben(verzeichnisName[nachlaufendWert * 64 + schleifeIndex]); TerminalEinAusgabe.schreiben("/\n");
        }
        for (int dateiIndex = 0; dateiIndex < dateiAnzahl; dateiIndex++) if (namenlänge[dateiIndex] > 0) {
            int positionStarten = eintragStarten(Name, dateiIndex * 64, namenlänge[dateiIndex]); if (positionStarten < 0) continue;
            for (int schleifeIndex = positionStarten; schleifeIndex < namenlänge[dateiIndex]; schleifeIndex++) Platine.seriellSchreiben(Name[dateiIndex * 64 + schleifeIndex]);
            TerminalEinAusgabe.schreiben("  "); TerminalEinAusgabe.Zahl(Länge[dateiIndex]); TerminalEinAusgabe.schreiben("byteWert(주기억 Datei)\n");
        }
        return 0;
    }
}
