// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE CODE_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] koduoti(String Turinys_VALUE) { return Turinys_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String iššifruoti_duomenys(byte[] Turinys_VALUE) { return new String(Turinys_VALUE, StandardCharsets.UTF_8); }
    public static String normalizuoti_VALUE(String Turinys_VALUE) { return Normalizer.normalize(Turinys_VALUE, Normalizer.Form.NFC); }
    public static int kodo_elementas_COUNT(String Turinys_VALUE) { return Turinys_VALUE.codePointCount(0, Turinys_VALUE.length()); }
    public static List<String> 낱말(String Turinys_VALUE, Locale Kalba) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Kalba);
        나누개.setText(Turinys_VALUE);
        List<String> REZULTATAS = new ArrayList<>();
        int Paleisti = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Paleisti = 끝, 끝 = 나누개.next())
            REZULTATAS.add(Turinys_VALUE.substring(Paleisti, 끝));
        return REZULTATAS;
    }
}
