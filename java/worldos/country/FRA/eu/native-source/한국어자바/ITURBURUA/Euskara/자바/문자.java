// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_balio KODE_balio 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String eduki_balio) { return eduki_balio.getBytes(StandardCharsets.UTF_8); }
    public static String desenkriptatu_datuak(byte[] eduki_balio) { return new String(eduki_balio, StandardCharsets.UTF_8); }
    public static String normalizatu_balio(String eduki_balio) { return Normalizer.normalize(eduki_balio, Normalizer.Form.NFC); }
    public static int karaktere_kode_ZENBATU(String eduki_balio) { return eduki_balio.codePointCount(0, eduki_balio.length()); }
    public static List<String> 낱말(String eduki_balio, Locale Hizkuntza) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Hizkuntza);
        나누개.setText(eduki_balio);
        List<String> EMAITZA = new ArrayList<>();
        int Exekutatu_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Exekutatu_2 = 끝, 끝 = 나누개.next())
            EMAITZA.add(eduki_balio.substring(Exekutatu_2, 끝));
        return EMAITZA;
    }
}
