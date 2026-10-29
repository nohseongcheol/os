// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_ARVO KOODI_ARVO 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] koodata(String Sisältö_ARVO) { return Sisältö_ARVO.getBytes(StandardCharsets.UTF_8); }
    public static String pura_salaus_data(byte[] Sisältö_ARVO) { return new String(Sisältö_ARVO, StandardCharsets.UTF_8); }
    public static String normalisoida_ARVO(String Sisältö_ARVO) { return Normalizer.normalize(Sisältö_ARVO, Normalizer.Form.NFC); }
    public static int koodipiste_LASKE(String Sisältö_ARVO) { return Sisältö_ARVO.codePointCount(0, Sisältö_ARVO.length()); }
    public static List<String> 낱말(String Sisältö_ARVO, Locale Kieli) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Kieli);
        나누개.setText(Sisältö_ARVO);
        List<String> TULOS = new ArrayList<>();
        int Suorita_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Suorita_2 = 끝, 끝 = 나누개.next())
            TULOS.add(Sisältö_ARVO.substring(Suorita_2, 끝));
        return TULOS;
    }
}
