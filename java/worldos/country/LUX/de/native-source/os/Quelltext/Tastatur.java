// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Abfrage von PC/AT-PS/2-Eingaben im übersetzten Scancodesatz 1. Grundlegende US-Belegung, Shift, Backspace und Enter. */
public final class Tastatur {
    static boolean verschiebenLinks = false;
    static boolean verschiebenRechts = false;
    static boolean erweiterungWert = false;
    static String standardwertWert = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String verschiebenWert = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int lesen() {
        int statuswertWert = Gerät.einAusgabeByteLesen(0x64);
        if ((statuswertWert & 1) == 0) return -1;
        int Wert = Gerät.einAusgabeByteLesen(0x60);
        if ((statuswertWert & 0x20) != 0) return -1;
        if (Wert == 0xe0 || Wert == 0xe1) { erweiterungWert = true; return -1; }
        if (erweiterungWert) { erweiterungWert = false; return -1; }
        if (Wert == 42 || Wert == 170) { verschiebenLinks = Wert == 42; return -1; }
        if (Wert == 54 || Wert == 182) { verschiebenRechts = Wert == 54; return -1; }
        if (Wert >= standardwertWert.length()) return -1;
        int Zeichen = (verschiebenLinks || verschiebenRechts) ? verschiebenWert.charAt(Wert) : standardwertWert.charAt(Wert);
        return Zeichen == 0 ? -1 : Zeichen;
    }
}
