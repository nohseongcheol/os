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
    public static byte[] 부호화(String Nilalaman_VALUE) { return Nilalaman_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String i_decrypt_data(byte[] Nilalaman_VALUE) { return new String(Nilalaman_VALUE, StandardCharsets.UTF_8); }
    public static String normalisahin_VALUE(String Nilalaman_VALUE) { return Normalizer.normalize(Nilalaman_VALUE, Normalizer.Form.NFC); }
    public static int character_code_COUNT(String Nilalaman_VALUE) { return Nilalaman_VALUE.codePointCount(0, Nilalaman_VALUE.length()); }
    public static List<String> 낱말(String Nilalaman_VALUE, Locale Wika) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Wika);
        나누개.setText(Nilalaman_VALUE);
        List<String> sukat = new ArrayList<>();
        int run = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; run = 끝, 끝 = 나누개.next())
            sukat.add(Nilalaman_VALUE.substring(run, 끝));
        return sukat;
    }
}
