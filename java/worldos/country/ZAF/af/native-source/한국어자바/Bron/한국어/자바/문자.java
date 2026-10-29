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
    public static byte[] 부호화(String Inhoud_VALUE) { return Inhoud_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dekripteer_data(byte[] Inhoud_VALUE) { return new String(Inhoud_VALUE, StandardCharsets.UTF_8); }
    public static String normaliseer_VALUE(String Inhoud_VALUE) { return Normalizer.normalize(Inhoud_VALUE, Normalizer.Form.NFC); }
    public static int karakterkode_COUNT(String Inhoud_VALUE) { return Inhoud_VALUE.codePointCount(0, Inhoud_VALUE.length()); }
    public static List<String> 낱말(String Inhoud_VALUE, Locale Taal) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Taal);
        나누개.setText(Inhoud_VALUE);
        List<String> maatreël = new ArrayList<>();
        int Loop = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Loop = 끝, 끝 = 나누개.next())
            maatreël.add(Inhoud_VALUE.substring(Loop, 끝));
        return maatreël;
    }
}
