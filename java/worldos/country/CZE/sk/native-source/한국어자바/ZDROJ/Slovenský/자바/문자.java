// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE kód_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kódovať(String obsah_VALUE) { return obsah_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dešifrovať_údaje(byte[] obsah_VALUE) { return new String(obsah_VALUE, StandardCharsets.UTF_8); }
    public static String normalizovať_VALUE(String obsah_VALUE) { return Normalizer.normalize(obsah_VALUE, Normalizer.Form.NFC); }
    public static int bod_kódu_COUNT(String obsah_VALUE) { return obsah_VALUE.codePointCount(0, obsah_VALUE.length()); }
    public static List<String> 낱말(String obsah_VALUE, Locale Jazyky) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Jazyky);
        나누개.setText(obsah_VALUE);
        List<String> KR = new ArrayList<>();
        int Spustiť_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Spustiť_2 = 끝, 끝 = 나누개.next())
            KR.add(obsah_VALUE.substring(Spustiť_2, 끝));
        return KR;
    }
}
