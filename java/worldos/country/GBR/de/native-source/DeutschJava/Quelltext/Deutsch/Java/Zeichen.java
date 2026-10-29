// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** Unterscheidet die Zahl der UTF-16-char-Einheiten von der Zahl der Unicode-Codepunkte. */
public final class Zeichen {
    private Zeichen() {}
    public static byte[] kodieren(String inhaltswertWert) { return inhaltswertWert.getBytes(StandardCharsets.UTF_8); }
    public static String datenEntschlüsseln(byte[] inhaltswertWert) { return new String(inhaltswertWert, StandardCharsets.UTF_8); }
    public static String wertNormalisieren(String inhaltswertWert) { return Normalizer.normalize(inhaltswertWert, Normalizer.Form.NFC); }
    public static int kodePunktAnzahl(String inhaltswertWert) { return inhaltswertWert.codePointCount(0, inhaltswertWert.length()); }
    public static List<String> lexikalischMaschinenwort(String inhaltswertWert, Locale Sprache) {
        BreakIterator teilerWert = BreakIterator.getWordInstance(Sprache);
        teilerWert.setText(inhaltswertWert);
        List<String> ergebnis = new ArrayList<>();
        int ausführenVorgang = teilerWert.first();
        for (int endung = teilerWert.next(); endung != BreakIterator.DONE; ausführenVorgang = endung, endung = teilerWert.next())
            ergebnis.add(inhaltswertWert.substring(ausführenVorgang, endung));
        return ergebnis;
    }
}
