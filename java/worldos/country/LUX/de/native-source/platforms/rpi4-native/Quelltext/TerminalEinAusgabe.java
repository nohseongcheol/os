// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class TerminalEinAusgabe {
    static void Zeichen(int Wert) {
        if (Wert < 0x80) Platine.seriellSchreiben(Wert);
        else if (Wert < 0x800) {
            Platine.seriellSchreiben(0xc0 | (Wert >> 6)); Platine.seriellSchreiben(0x80 | (Wert & 63));
        } else if (Wert < 0x10000) {
            Platine.seriellSchreiben(0xe0 | (Wert >> 12)); Platine.seriellSchreiben(0x80 | ((Wert >> 6) & 63)); Platine.seriellSchreiben(0x80 | (Wert & 63));
        } else {
            Platine.seriellSchreiben(0xf0 | (Wert >> 18)); Platine.seriellSchreiben(0x80 | ((Wert >> 12) & 63));
            Platine.seriellSchreiben(0x80 | ((Wert >> 6) & 63)); Platine.seriellSchreiben(0x80 | (Wert & 63));
        }
    }
    static void schreiben(String Text) {
        for (int Nummer = 0; Nummer < Text.length(); Nummer++) {
            int Wert = Text.charAt(Nummer);
            if (Wert >= 0xd800 && Wert <= 0xdbff && Nummer + 1 < Text.length()) {
                int unterkanteWert = Text.charAt(Nummer + 1);
                if (unterkanteWert >= 0xdc00 && unterkanteWert <= 0xdfff) {
                    Wert = 0x10000 + ((Wert - 0xd800) << 10) + unterkanteWert - 0xdc00; Nummer++;
                }
            }
            if (Wert >= 0xd800 && Wert <= 0xdfff) Wert = 0xfffd;
            Zeichen(Wert);
        }
    }
    static void Zahl(int Wert) {
        if (Wert < 0) Zeichen('-'); else Wert = -Wert;
        int positionIndex = 1000000000;
        boolean ausführenVorgang = false;
        while (positionIndex > 0) {
            int zifferWert = -(Wert / positionIndex);
            if (zifferWert != 0 || ausführenVorgang || positionIndex == 1) { Zeichen('0' + zifferWert); ausführenVorgang = true; }
            Wert %= positionIndex; positionIndex /= 10;
        }
    }
}
