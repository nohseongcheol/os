// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE kod_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Përmbajtje_VALUE) { return Përmbajtje_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String dekriptoj_të_dhëna(byte[] Përmbajtje_VALUE) { return new String(Përmbajtje_VALUE, StandardCharsets.UTF_8); }
    public static String normalizoj_VALUE(String Përmbajtje_VALUE) { return Normalizer.normalize(Përmbajtje_VALUE, Normalizer.Form.NFC); }
    public static int kodi_i_karakterit_COUNT(String Përmbajtje_VALUE) { return Përmbajtje_VALUE.codePointCount(0, Përmbajtje_VALUE.length()); }
    public static List<String> 낱말(String Përmbajtje_VALUE, Locale Gjuha) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Gjuha);
        나누개.setText(Përmbajtje_VALUE);
        List<String> llogaritje = new ArrayList<>();
        int Ekzekuto = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Ekzekuto = 끝, 끝 = 나누개.next())
            llogaritje.add(Përmbajtje_VALUE.substring(Ekzekuto, 끝));
        return llogaritje;
    }
}
