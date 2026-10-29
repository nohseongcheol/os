// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Serielle COM1-Ausgabe und VGA-Textanzeige mit 80x25 Zeichen. Unicode-Text geht als UTF-8 an das serielle Terminal. */
public final class Zeichenterminal {
    static int platzEintrag = 0;
    static int farbeWert = 7;

    static void vorbereiten() {
        Gerät.einAusgabeByteSchreiben(0x3f9, 0);
        Gerät.einAusgabeByteSchreiben(0x3fb, 0x80);
        Gerät.einAusgabeByteSchreiben(0x3f8, 1);
        Gerät.einAusgabeByteSchreiben(0x3f9, 0);
        Gerät.einAusgabeByteSchreiben(0x3fb, 3);
        Gerät.einAusgabeByteSchreiben(0x3fa, 0xc7);
        Gerät.einAusgabeByteSchreiben(0x3fc, 0x0b);
        eintragTilgen();
    }

    static void seriellByte(int Wert) {
        int wiederholungAnzahl = 100000;
        while ((Gerät.einAusgabeByteLesen(0x3fd) & 0x20) == 0 && wiederholungAnzahl > 0) wiederholungAnzahl--;
        if (wiederholungAnzahl > 0) Gerät.einAusgabeByteSchreiben(0x3f8, Wert);
    }

    static void eintragTilgen() {
        for (int Nummer = 0; Nummer < 2000; Nummer++) {
            Gerät.speicherSchreiben(0xb8000 + Nummer * 2, 32);
            Gerät.speicherSchreiben(0xb8001 + Nummer * 2, farbeWert);
        }
        platzEintrag = 0;
        mauszeigerWert();
    }

    static void mauszeigerWert() {
        Gerät.einAusgabeByteSchreiben(0x3d4, 14);
        Gerät.einAusgabeByteSchreiben(0x3d5, platzEintrag >> 8);
        Gerät.einAusgabeByteSchreiben(0x3d4, 15);
        Gerät.einAusgabeByteSchreiben(0x3d5, platzEintrag & 255);
    }

    static void bildschirmZeichen(int Wert) {
        if (Wert == 13) return;
        if (Wert == 10) {
            platzEintrag = (platzEintrag / 80 + 1) * 80;
        } else if (Wert == 8) {
            if (platzEintrag > 0) {
                platzEintrag--;
                Gerät.speicherSchreiben(0xb8000 + platzEintrag * 2, 32);
            }
        } else {
            Gerät.speicherSchreiben(0xb8000 + platzEintrag * 2, Wert < 128 ? Wert : '?');
            Gerät.speicherSchreiben(0xb8001 + platzEintrag * 2, farbeWert);
            platzEintrag++;
        }
        if (platzEintrag >= 2000) {
            for (int Nummer = 0; Nummer < 3840; Nummer++)
                Gerät.speicherSchreiben(0xb8000 + Nummer, Gerät.speicherLesen(0xb80a0 + Nummer));
            for (int Nummer = 1920; Nummer < 2000; Nummer++) {
                Gerät.speicherSchreiben(0xb8000 + Nummer * 2, 32);
                Gerät.speicherSchreiben(0xb8001 + Nummer * 2, farbeWert);
            }
            platzEintrag = 1920;
        }
        mauszeigerWert();
    }

    static void Zeichen(int Wert) {
        if (Wert < 128) {
            if (Wert == 10) seriellByte(13);
            seriellByte(Wert);
        } else if (Wert < 2048) {
            seriellByte(0xc0 | (Wert >> 6));
            seriellByte(0x80 | (Wert & 63));
        } else {
            seriellByte(0xe0 | (Wert >> 12));
            seriellByte(0x80 | ((Wert >> 6) & 63));
            seriellByte(0x80 | (Wert & 63));
        }
        bildschirmZeichen(Wert);
    }

    static void schreiben(String inhaltswertWert) {
        for (int Nummer = 0; Nummer < inhaltswertWert.length(); Nummer++) Zeichen(inhaltswertWert.charAt(Nummer));
    }

    static void nummerSchreiben(int Wert) {
        // Keine Umwandlung in einen positiven Wert, daher ist auch Integer.MIN_VALUE sicher.
        if (Wert < 0) Zeichen('-');
        else Wert = -Wert;
        int positionIndex = 1000000000;
        boolean ausführenVorgang = false;
        while (positionIndex > 0) {
            int zifferWert = -(Wert / positionIndex);
            if (zifferWert != 0 || ausführenVorgang || positionIndex == 1) {
                Zeichen('0' + zifferWert);
                ausführenVorgang = true;
            }
            Wert %= positionIndex;
            positionIndex /= 10;
        }
    }

    static int seriellLesen() {
        if ((Gerät.einAusgabeByteLesen(0x3fd) & 1) != 0) return Gerät.einAusgabeByteLesen(0x3f8);
        return -1;
    }
}
