// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Innhald_VALUE) { return Innhald_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dekryptere_data(byte[] Innhald_VALUE) { return new String(Innhald_VALUE, StandardCharsets.UTF_8); }
    public static String normalisere_VALUE(String Innhald_VALUE) { return Normalizer.normalize(Innhald_VALUE, Normalizer.Form.NFC); }
    public static int teiknkode_COUNT(String Innhald_VALUE) { return Innhald_VALUE.codePointCount(0, Innhald_VALUE.length()); }
    public static List<String> 낱말(String Innhald_VALUE, Locale Språk) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Språk);
        나누개.setText(Innhald_VALUE);
        List<String> forretningsmål = new ArrayList<>();
        int Køyr_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Køyr_2 = 끝, 끝 = 나누개.next())
            forretningsmål.add(Innhald_VALUE.substring(Køyr_2, 끝));
        return forretningsmål;
    }
}
