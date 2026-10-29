// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_värde KOD_värde 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] koda(String Innehåll_värde) { return Innehåll_värde.getBytes(StandardCharsets.UTF_8); }
    public static String avkryptera_data(byte[] Innehåll_värde) { return new String(Innehåll_värde, StandardCharsets.UTF_8); }
    public static String normalisera_värde(String Innehåll_värde) { return Normalizer.normalize(Innehåll_värde, Normalizer.Form.NFC); }
    public static int kodpunkt_ANTAL(String Innehåll_värde) { return Innehåll_värde.codePointCount(0, Innehåll_värde.length()); }
    public static List<String> 낱말(String Innehåll_värde, Locale Språk) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Språk);
        나누개.setText(Innehåll_värde);
        List<String> RESULTAT = new ArrayList<>();
        int Kör = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Kör = 끝, 끝 = 나누개.next())
            RESULTAT.add(Innehåll_värde.substring(Kör, 끝));
        return RESULTAT;
    }
}
