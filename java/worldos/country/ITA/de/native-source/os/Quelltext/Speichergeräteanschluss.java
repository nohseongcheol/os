// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Logische 512-Byte-Sektoren des ersten IDE-Geräts. Diese Schicht formatiert oder löscht keine beliebigen Geräte. */
public final class Speichergeräteanschluss {
    static boolean istVerfügbar = false;
    static int[] abschnittDaten = new int[512];
    static void kurzzeitigTunWarten() {
        for (int Nummer = 0; Nummer < 4; Nummer++) Gerät.einAusgabeByteLesen(0x3f6);
    }
    static int bisBereitWarten(boolean datenErforderlich) {
        int ausführenVorgang = Gerät.millisekunden();
        while (Gerät.millisekunden() - ausführenVorgang < 500) {
            int statuswertWert = Gerät.einAusgabeByteLesen(0x1f7);
            if (statuswertWert == 0 || statuswertWert == 255) return -19;
            if ((statuswertWert & 128) == 0) {
                if ((statuswertWert & 33) != 0) return -5;
                if (!datenErforderlich || (statuswertWert & 8) != 0) return 0;
            }
            Gerät.kurzzeitigTunAbgeben();
        }
        return -110;
    }
    static int anfrage(int abschnittWert, int befehl) {
        if (abschnittWert < 0 || abschnittWert >= 2048) return -22;
        Gerät.einAusgabeByteSchreiben(0x3f6, 2); // Abfragebetrieb; IDE-IRQ wird nicht verwendet.
        Gerät.einAusgabeByteSchreiben(0x1f6, 0xe0); kurzzeitigTunWarten();
        int ergebnis = bisBereitWarten(false);
        if (ergebnis < 0) return ergebnis;
        Gerät.einAusgabeByteSchreiben(0x1f2, 1);
        Gerät.einAusgabeByteSchreiben(0x1f3, abschnittWert & 255);
        Gerät.einAusgabeByteSchreiben(0x1f4, (abschnittWert >>> 8) & 255);
        Gerät.einAusgabeByteSchreiben(0x1f5, 0);
        Gerät.einAusgabeByteSchreiben(0x1f7, befehl); kurzzeitigTunWarten();
        return bisBereitWarten(true);
    }
    static int lesen(int abschnittWert) {
        int ergebnis = anfrage(abschnittWert, 0x20);
        if (ergebnis < 0) return ergebnis;
        for (int Nummer = 0; Nummer < 256; Nummer++) {
            int Wert = Gerät.einAusgabeKurzLesen(0x1f0);
            abschnittDaten[Nummer * 2] = Wert & 255; abschnittDaten[Nummer * 2 + 1] = Wert >>> 8;
        }
        kurzzeitigTunWarten(); return bisBereitWarten(false);
    }
    static int schreiben(int abschnittWert) {
        if (!istVerfügbar || abschnittWert < 1 || abschnittWert > 518) return -19;
        int ergebnis = anfrage(abschnittWert, 0x30);
        if (ergebnis < 0) return ergebnis;
        for (int Nummer = 0; Nummer < 256; Nummer++)
            Gerät.einAusgabeKurzSchreiben(0x1f0, abschnittDaten[Nummer * 2] | abschnittDaten[Nummer * 2 + 1] << 8);
        kurzzeitigTunWarten(); return bisBereitWarten(false);
    }
    static int leerenAusgabe() {
        if (!istVerfügbar) return -19;
        Gerät.einAusgabeByteSchreiben(0x1f7, 0xe7); kurzzeitigTunWarten();
        return bisBereitWarten(false);
    }
    static int ganzzahlAnalysieren(int position) {
        return abschnittDaten[position] | abschnittDaten[position + 1] << 8 | abschnittDaten[position + 2] << 16 | abschnittDaten[position + 3] << 24;
    }
    static void ganzzahlWertSchreiben(int position, int Wert) {
        for (int Nummer = 0; Nummer < 4; Nummer++) abschnittDaten[position + Nummer] = (Wert >>> (Nummer * 8)) & 255;
    }
}
