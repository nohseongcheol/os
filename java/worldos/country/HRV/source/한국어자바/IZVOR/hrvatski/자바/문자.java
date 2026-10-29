// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE kod_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kodirati(String Sadržaj_VALUE) { return Sadržaj_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dešifrirati_podaci(byte[] Sadržaj_VALUE) { return new String(Sadržaj_VALUE, StandardCharsets.UTF_8); }
    public static String normalizirati_VALUE(String Sadržaj_VALUE) { return Normalizer.normalize(Sadržaj_VALUE, Normalizer.Form.NFC); }
    public static int točka_koda_COUNT(String Sadržaj_VALUE) { return Sadržaj_VALUE.codePointCount(0, Sadržaj_VALUE.length()); }
    public static List<String> 낱말(String Sadržaj_VALUE, Locale Jezik) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Jezik);
        나누개.setText(Sadržaj_VALUE);
        List<String> REZULTAT = new ArrayList<>();
        int Pokreni = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Pokreni = 끝, 끝 = 나누개.next())
            REZULTAT.add(Sadržaj_VALUE.substring(Pokreni, 끝));
        return REZULTAT;
    }
}
