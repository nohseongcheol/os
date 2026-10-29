// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Kontenut_VALUE) { return Kontenut_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String ddeċifra_data(byte[] Kontenut_VALUE) { return new String(Kontenut_VALUE, StandardCharsets.UTF_8); }
    public static String nnormalizza_VALUE(String Kontenut_VALUE) { return Normalizer.normalize(Kontenut_VALUE, Normalizer.Form.NFC); }
    public static int kodiċi_tal_karattru_COUNT(String Kontenut_VALUE) { return Kontenut_VALUE.codePointCount(0, Kontenut_VALUE.length()); }
    public static List<String> 낱말(String Kontenut_VALUE, Locale Lingwa) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Lingwa);
        나누개.setText(Kontenut_VALUE);
        List<String> miżura = new ArrayList<>();
        int serje = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; serje = 끝, 끝 = 나누개.next())
            miżura.add(Kontenut_VALUE.substring(serje, 끝));
        return miżura;
    }
}
