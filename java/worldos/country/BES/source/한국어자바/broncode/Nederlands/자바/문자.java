// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_WAARDE CODE_WAARDE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] coderen(String Inhoud_WAARDE) { return Inhoud_WAARDE.getBytes(StandardCharsets.UTF_8); }
    public static String ontsleutelen_gegevens(byte[] Inhoud_WAARDE) { return new String(Inhoud_WAARDE, StandardCharsets.UTF_8); }
    public static String normaliseren_WAARDE(String Inhoud_WAARDE) { return Normalizer.normalize(Inhoud_WAARDE, Normalizer.Form.NFC); }
    public static int codepoint_AANTAL(String Inhoud_WAARDE) { return Inhoud_WAARDE.codePointCount(0, Inhoud_WAARDE.length()); }
    public static List<String> 낱말(String Inhoud_WAARDE, Locale Taal) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Taal);
        나누개.setText(Inhoud_WAARDE);
        List<String> resultaat = new ArrayList<>();
        int starten = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; starten = 끝, 끝 = 나누개.next())
            resultaat.add(Inhoud_WAARDE.substring(starten, 끝));
        return resultaat;
    }
}
