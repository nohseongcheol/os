// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VÆRDI KODE_VÆRDI 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kode(String Indhold_VÆRDI) { return Indhold_VÆRDI.getBytes(StandardCharsets.UTF_8); }
    public static String dekryptere_data(byte[] Indhold_VÆRDI) { return new String(Indhold_VÆRDI, StandardCharsets.UTF_8); }
    public static String normalisere_VÆRDI(String Indhold_VÆRDI) { return Normalizer.normalize(Indhold_VÆRDI, Normalizer.Form.NFC); }
    public static int tegnkode_TÆL(String Indhold_VÆRDI) { return Indhold_VÆRDI.codePointCount(0, Indhold_VÆRDI.length()); }
    public static List<String> 낱말(String Indhold_VÆRDI, Locale Sprog) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Sprog);
        나누개.setText(Indhold_VÆRDI);
        List<String> KR = new ArrayList<>();
        int Kør_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Kør_2 = 끝, 끝 = 나누개.next())
            KR.add(Indhold_VÆRDI.substring(Kør_2, 끝));
        return KR;
    }
}
