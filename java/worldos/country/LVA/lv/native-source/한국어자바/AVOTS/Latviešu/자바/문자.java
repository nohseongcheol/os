// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kodēt(String Saturs_VALUE) { return Saturs_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String atšifrēt_dati(byte[] Saturs_VALUE) { return new String(Saturs_VALUE, StandardCharsets.UTF_8); }
    public static String normalizēt_VALUE(String Saturs_VALUE) { return Normalizer.normalize(Saturs_VALUE, Normalizer.Form.NFC); }
    public static int koda_punkts_COUNT(String Saturs_VALUE) { return Saturs_VALUE.codePointCount(0, Saturs_VALUE.length()); }
    public static List<String> 낱말(String Saturs_VALUE, Locale Valodas) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Valodas);
        나누개.setText(Saturs_VALUE);
        List<String> mērs = new ArrayList<>();
        int Palaist = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Palaist = 끝, 끝 = 나누개.next())
            mērs.add(Saturs_VALUE.substring(Palaist, 끝));
        return mērs;
    }
}
