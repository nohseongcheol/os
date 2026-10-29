// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kodeerima(String Sisu_VALUE) { return Sisu_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dekrüptima_andmed(byte[] Sisu_VALUE) { return new String(Sisu_VALUE, StandardCharsets.UTF_8); }
    public static String normaliseerima_VALUE(String Sisu_VALUE) { return Normalizer.normalize(Sisu_VALUE, Normalizer.Form.NFC); }
    public static int koodipunkt_COUNT(String Sisu_VALUE) { return Sisu_VALUE.codePointCount(0, Sisu_VALUE.length()); }
    public static List<String> 낱말(String Sisu_VALUE, Locale Keeled) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Keeled);
        나누개.setText(Sisu_VALUE);
        List<String> TULEMUS = new ArrayList<>();
        int Käivita_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Käivita_2 = 끝, 끝 = 나누개.next())
            TULEMUS.add(Sisu_VALUE.substring(Käivita_2, 끝));
        return TULEMUS;
    }
}
