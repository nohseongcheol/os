// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Gemeinsame Ausgabe und Behandlung von ASCII-Dateinamen für Gastwerkzeuge. */
public final class JavaWerkzeug {
    /** Wandelt ein UTF-8-Bytefeld im selben Feld in UTF-16-Einheiten um. Weist fehlerhafte Eingaben ab. */
    static int quelltextDekodieren(int[] Daten, int Länge) {
        int lesen = 0, schreiben = 0;
        if (Länge >= 3 && Daten[0] == 239 && Daten[1] == 187 && Daten[2] == 191) lesen = 3;
        while (lesen < Länge) {
            int Wert = Daten[lesen++], Zahl = 0, mindestwertWert = 0;
            if (Wert >= 194 && Wert <= 223) { Zahl = 1; mindestwertWert = 128; Wert &= 31; }
            else if (Wert >= 224 && Wert <= 239) { Zahl = 2; mindestwertWert = 2048; Wert &= 15; }
            else if (Wert >= 240 && Wert <= 244) { Zahl = 3; mindestwertWert = 65536; Wert &= 7; }
            else if (Wert >= 128 || Wert < 0) return -1;
            if (Zahl > Länge - lesen) return -1;
            for (int i = 0; i < Zahl; i++) {
                int nächsterElementeintrag = Daten[lesen++]; if ((nächsterElementeintrag & 192) != 128) return -1;
                Wert = (Wert << 6) | (nächsterElementeintrag & 63);
            }
            if (Wert < mindestwertWert || Wert > 0x10ffff || (Wert >= 0xd800 && Wert <= 0xdfff)) return -1;
            if (Wert >= 65536) { Wert -= 65536; Daten[schreiben++] = 0xd800 | (Wert >> 10); Daten[schreiben++] = 0xdc00 | (Wert & 1023); }
            else Daten[schreiben++] = Wert;
        }
        return schreiben;
    }
    static void nummerSchreiben(int Wert) {
        if (Wert < 0) Benutzer.zeichenWertSchreiben('-'); else Wert = -Wert;
        int positionIndex = 1000000000;
        boolean ausführenVorgang = false;
        while (positionIndex != 0) {
            int Zahl = -(Wert / positionIndex);
            if (Zahl != 0 || ausführenVorgang || positionIndex == 1) { Benutzer.zeichenWertSchreiben('0' + Zahl); ausführenVorgang = true; }
            Wert %= positionIndex; positionIndex /= 10;
        }
    }
    static int Name(int[] zielWert, String ursprünglich) {
        if (ursprünglich.length() >= zielWert.length) return -1;
        for (int Zahl = 0; Zahl < zielWert.length; Zahl++) zielWert[Zahl] = Zahl < ursprünglich.length() ? ursprünglich.charAt(Zahl) : 0;
        return ursprünglich.length();
    }
    static boolean gleichText(String ersterOperand, String zweiterOperand) {
        if (ersterOperand.length() != zweiterOperand.length()) return false;
        for (int Zahl = 0; Zahl < ersterOperand.length(); Zahl++) if (ersterOperand.charAt(Zahl) != zweiterOperand.charAt(Zahl)) return false;
        return true;
    }
}
