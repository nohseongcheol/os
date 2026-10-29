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
    public static byte[] 부호화(String Inhalt_VALUE) { return Inhalt_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String decryptéieren_Daten(byte[] Inhalt_VALUE) { return new String(Inhalt_VALUE, StandardCharsets.UTF_8); }
    public static String normaliséieren_VALUE(String Inhalt_VALUE) { return Normalizer.normalize(Inhalt_VALUE, Normalizer.Form.NFC); }
    public static int Zeechecode_COUNT(String Inhalt_VALUE) { return Inhalt_VALUE.codePointCount(0, Inhalt_VALUE.length()); }
    public static List<String> 낱말(String Inhalt_VALUE, Locale Sprooch) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Sprooch);
        나누개.setText(Inhalt_VALUE);
        List<String> Mooss = new ArrayList<>();
        int Laf = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Laf = 끝, 끝 = 나누개.next())
            Mooss.add(Inhalt_VALUE.substring(Laf, 끝));
        return Mooss;
    }
}
