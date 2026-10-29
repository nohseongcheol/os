// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Efni_VALUE) { return Efni_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dulráða_gögn(byte[] Efni_VALUE) { return new String(Efni_VALUE, StandardCharsets.UTF_8); }
    public static String staðla_VALUE(String Efni_VALUE) { return Normalizer.normalize(Efni_VALUE, Normalizer.Form.NFC); }
    public static int stafkóði_COUNT(String Efni_VALUE) { return Efni_VALUE.codePointCount(0, Efni_VALUE.length()); }
    public static List<String> 낱말(String Efni_VALUE, Locale Tungumál) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Tungumál);
        나누개.setText(Efni_VALUE);
        List<String> NIÐURSTAÐA = new ArrayList<>();
        int Keyra_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Keyra_2 = 끝, 끝 = 나누개.next())
            NIÐURSTAÐA.add(Efni_VALUE.substring(Keyra_2, 끝));
        return NIÐURSTAÐA;
    }
}
