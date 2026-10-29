// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE cod_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] codifica(String Conținut_VALUE) { return Conținut_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String decripta_date(byte[] Conținut_VALUE) { return new String(Conținut_VALUE, StandardCharsets.UTF_8); }
    public static String normaliza_VALUE(String Conținut_VALUE) { return Normalizer.normalize(Conținut_VALUE, Normalizer.Form.NFC); }
    public static int cod_caracter_COUNT(String Conținut_VALUE) { return Conținut_VALUE.codePointCount(0, Conținut_VALUE.length()); }
    public static List<String> 낱말(String Conținut_VALUE, Locale Limbi_străine) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Limbi_străine);
        나누개.setText(Conținut_VALUE);
        List<String> KR = new ArrayList<>();
        int Pornește = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Pornește = 끝, 끝 = 나누개.next())
            KR.add(Conținut_VALUE.substring(Pornește, 끝));
        return KR;
    }
}
