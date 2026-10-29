// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VERDI KODE_VERDI 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Innhold_VERDI) { return Innhold_VERDI.getBytes(StandardCharsets.UTF_8); }
    public static String dekryptere_data(byte[] Innhold_VERDI) { return new String(Innhold_VERDI, StandardCharsets.UTF_8); }
    public static String normalisere_VERDI(String Innhold_VERDI) { return Normalizer.normalize(Innhold_VERDI, Normalizer.Form.NFC); }
    public static int tegnkode_ANTALL(String Innhold_VERDI) { return Innhold_VERDI.codePointCount(0, Innhold_VERDI.length()); }
    public static List<String> 낱말(String Innhold_VERDI, Locale Språk) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Språk);
        나누개.setText(Innhold_VERDI);
        List<String> KR = new ArrayList<>();
        int Kjør_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Kjør_2 = 끝, 끝 = 나누개.next())
            KR.add(Innhold_VERDI.substring(Kjør_2, 끝));
        return KR;
    }
}
