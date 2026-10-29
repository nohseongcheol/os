// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALORE CODICE_VALORE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] codificare(String Contenuto_VALORE) { return Contenuto_VALORE.getBytes(StandardCharsets.UTF_8); }
    public static String decifrare_dati(byte[] Contenuto_VALORE) { return new String(Contenuto_VALORE, StandardCharsets.UTF_8); }
    public static String normalizzare_VALORE(String Contenuto_VALORE) { return Normalizer.normalize(Contenuto_VALORE, Normalizer.Form.NFC); }
    public static int punto_di_codice_CONTA_NUMERI(String Contenuto_VALORE) { return Contenuto_VALORE.codePointCount(0, Contenuto_VALORE.length()); }
    public static List<String> 낱말(String Contenuto_VALORE, Locale Lingua) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Lingua);
        나누개.setText(Contenuto_VALORE);
        List<String> risultato = new ArrayList<>();
        int avvia = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; avvia = 끝, 끝 = 나누개.next())
            risultato.add(Contenuto_VALORE.substring(avvia, 끝));
        return risultato;
    }
}
