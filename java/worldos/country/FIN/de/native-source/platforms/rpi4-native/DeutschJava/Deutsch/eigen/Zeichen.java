// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Konvertiert UTF-8-Bytes und UTF-16-Zeichenketten. Normalisierung und kombinierende Eingabe werden getrennt behandelt. */
public final class Zeichen {
    public static int byteAnzahl(byte[] Daten) { return Daten.length; }
    private Zeichen() {}
    public static int Länge(String Text) { return Text.length(); }
    public static boolean gleichText(String vorderseiteWert, String rückseiteWert) { return vorderseiteWert == null ? rückseiteWert == null : vorderseiteWert.equals(rückseiteWert); }
    public static String einsetzenText(String vorderseiteWert, String rückseiteWert) { return vorderseiteWert.concat(rückseiteWert); }
    public static String schneidenWert(String Text, int ausführenVorgang, int endung) { return Text.substring(ausführenVorgang, endung); }
    public static int ganzzahlAnalysieren(String Text) { try { return Integer.parseInt(Text); } catch (NumberFormatException fehler) { throw new NummerFormatFehlschlag("Prüfen Sie das Zahlenformat und den Wertebereich."); } }
    public static String ganzzahlWertSchreiben(int Zahl) { return Integer.toString(Zahl); }
    public static int kodePunktAnzahl(String Text) {
        int Zahl = 0;
        for (int schleifeIndex = 0; schleifeIndex < Text.length(); schleifeIndex++, Zahl++) {
            int zeichenKode = Text.charAt(schleifeIndex);
            if (zeichenKode >= 0xd800 && zeichenKode <= 0xdbff && schleifeIndex + 1 < Text.length() && Text.charAt(schleifeIndex + 1) >= 0xdc00 && Text.charAt(schleifeIndex + 1) <= 0xdfff) schleifeIndex++;
        }
        return Zahl;
    }
    public static byte[] kodieren(String Text) {
        byte[] vorläufigWert = new byte[Text.length() * 3]; int geschrieben = 0;
        for (int schleifeIndex = 0; schleifeIndex < Text.length(); schleifeIndex++) {
            int zeichenKode = Text.charAt(schleifeIndex);
            if (zeichenKode >= 0xd800 && zeichenKode <= 0xdbff && schleifeIndex + 1 < Text.length() && Text.charAt(schleifeIndex + 1) >= 0xdc00 && Text.charAt(schleifeIndex + 1) <= 0xdfff) zeichenKode = 0x10000 + ((zeichenKode - 0xd800) << 10) + Text.charAt(++schleifeIndex) - 0xdc00;
            else if (zeichenKode >= 0xd800 && zeichenKode <= 0xdfff) zeichenKode = '?';
            if (zeichenKode < 128) vorläufigWert[geschrieben++] = (byte)zeichenKode;
            else if (zeichenKode < 2048) { vorläufigWert[geschrieben++] = (byte)(192 | zeichenKode >> 6); vorläufigWert[geschrieben++] = (byte)(128 | zeichenKode & 63); }
            else if (zeichenKode < 65536) { vorläufigWert[geschrieben++] = (byte)(224 | zeichenKode >> 12); vorläufigWert[geschrieben++] = (byte)(128 | zeichenKode >> 6 & 63); vorläufigWert[geschrieben++] = (byte)(128 | zeichenKode & 63); }
            else { vorläufigWert[geschrieben++] = (byte)(240 | zeichenKode >> 18); vorläufigWert[geschrieben++] = (byte)(128 | zeichenKode >> 12 & 63); vorläufigWert[geschrieben++] = (byte)(128 | zeichenKode >> 6 & 63); vorläufigWert[geschrieben++] = (byte)(128 | zeichenKode & 63); }
        }
        byte[] ergebnis = new byte[geschrieben]; System.arraycopy(vorläufigWert, 0, ergebnis, 0, geschrieben); return ergebnis;
    }
    /** Weist ungültiges UTF-8 mit der API-Ausnahme für ungültige Argumente ab. */
    public static String datenEntschlüsseln(byte[] byteWert) {
        StringBuilder ergebnis = new StringBuilder();
        for (int schleifeIndex = 0; schleifeIndex < byteWert.length;) {
            int zeichenKode = byteWert[schleifeIndex++] & 255, Zahl = zeichenKode < 128 ? 0 : zeichenKode >= 194 && zeichenKode < 224 ? 1 : zeichenKode >= 224 && zeichenKode < 240 ? 2 : zeichenKode >= 240 && zeichenKode <= 244 ? 3 : -1;
            if (Zahl < 0 || byteWert.length - schleifeIndex < Zahl) throw new UngültigArgumentAusnahme("Ungültiges UTF-8");
            int mindestwertWert = Zahl == 1 ? 128 : Zahl == 2 ? 2048 : Zahl == 3 ? 65536 : 0;
            if (Zahl > 0) zeichenKode &= (1 << (6 - Zahl)) - 1;
            for (int innerlichPosition = 0; innerlichPosition < Zahl; innerlichPosition++) { int rückseiteWert = byteWert[schleifeIndex++] & 255; if ((rückseiteWert & 192) != 128) throw new UngültigArgumentAusnahme("Ungültiges UTF-8"); zeichenKode = zeichenKode << 6 | rückseiteWert & 63; }
            if (zeichenKode < mindestwertWert || zeichenKode > 0x10ffff || zeichenKode >= 0xd800 && zeichenKode <= 0xdfff) throw new UngültigArgumentAusnahme("Ungültiges UTF-8");
            if (zeichenKode < 65536) ergebnis.append((char)zeichenKode);
            else { zeichenKode -= 65536; ergebnis.append((char)(0xd800 | zeichenKode >> 10)); ergebnis.append((char)(0xdc00 | zeichenKode & 1023)); }
        }
        return ergebnis.toString();
    }
}
