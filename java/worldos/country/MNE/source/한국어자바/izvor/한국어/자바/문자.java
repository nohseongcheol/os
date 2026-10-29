// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unikod_VALUE kôd_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kodirati(String Sadržaj_VALUE) { return Sadržaj_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dešifrovati_podaci(byte[] Sadržaj_VALUE) { return new String(Sadržaj_VALUE, StandardCharsets.UTF_8); }
    public static String normalizovati_VALUE(String Sadržaj_VALUE) { return Normalizer.normalize(Sadržaj_VALUE, Normalizer.Form.NFC); }
    public static int kôd_znaka_COUNT(String Sadržaj_VALUE) { return Sadržaj_VALUE.codePointCount(0, Sadržaj_VALUE.length()); }
    public static List<String> 낱말(String Sadržaj_VALUE, Locale jezik) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(jezik);
        나누개.setText(Sadržaj_VALUE);
        List<String> KR = new ArrayList<>();
        int koristiti = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; koristiti = 끝, 끝 = 나누개.next())
            KR.add(Sadržaj_VALUE.substring(koristiti, 끝));
        return KR;
    }
}
