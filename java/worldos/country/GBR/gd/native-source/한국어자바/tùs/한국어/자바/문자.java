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
    public static byte[] 부호화(String susbaint_VALUE) { return susbaint_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dì_chrioptaich_dàta(byte[] susbaint_VALUE) { return new String(susbaint_VALUE, StandardCharsets.UTF_8); }
    public static String àbhaistich_VALUE(String susbaint_VALUE) { return Normalizer.normalize(susbaint_VALUE, Normalizer.Form.NFC); }
    public static int còd_a_charactair_COUNT(String susbaint_VALUE) { return susbaint_VALUE.codePointCount(0, susbaint_VALUE.length()); }
    public static List<String> 낱말(String susbaint_VALUE, Locale cànan) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(cànan);
        나누개.setText(susbaint_VALUE);
        List<String> tomhas = new ArrayList<>();
        int ruith = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ruith = 끝, 끝 = 나누개.next())
            tomhas.add(susbaint_VALUE.substring(ruith, 끝));
        return tomhas;
    }
}
