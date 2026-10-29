// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kodirati(String vsebina_VALUE) { return vsebina_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dešifrirati_podatki(byte[] vsebina_VALUE) { return new String(vsebina_VALUE, StandardCharsets.UTF_8); }
    public static String normalizirati_VALUE(String vsebina_VALUE) { return Normalizer.normalize(vsebina_VALUE, Normalizer.Form.NFC); }
    public static int koda_znaka_COUNT(String vsebina_VALUE) { return vsebina_VALUE.codePointCount(0, vsebina_VALUE.length()); }
    public static List<String> 낱말(String vsebina_VALUE, Locale jezik) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(jezik);
        나누개.setText(vsebina_VALUE);
        List<String> REZULTAT = new ArrayList<>();
        int Zaženi = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Zaženi = 끝, 끝 = 나누개.next())
            REZULTAT.add(vsebina_VALUE.substring(Zaženi, 끝));
        return REZULTAT;
    }
}
