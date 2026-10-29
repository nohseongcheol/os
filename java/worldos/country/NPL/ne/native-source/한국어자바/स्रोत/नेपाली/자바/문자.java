// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 युनिकोड_मान 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String सामग्री_मान) { return सामग्री_मान.getBytes(StandardCharsets.UTF_8); }
    public static String गुप्तलेखन_उल्टाउनुहोस्_लगत(byte[] सामग्री_मान) { return new String(सामग्री_मान, StandardCharsets.UTF_8); }
    public static String सामान्यकरण_गर्नुहोस्_मान(String सामग्री_मान) { return Normalizer.normalize(सामग्री_मान, Normalizer.Form.NFC); }
    public static int 코드포인트수(String सामग्री_मान) { return सामग्री_मान.codePointCount(0, सामग्री_मान.length()); }
    public static List<String> 낱말(String सामग्री_मान, Locale भाषा) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(भाषा);
        나누개.setText(सामग्री_मान);
        List<String> मापन = new ArrayList<>();
        int चलाउनुहोस् = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; चलाउनुहोस् = 끝, 끝 = 나누개.next())
            मापन.add(सामग्री_मान.substring(चलाउनुहोस्, 끝));
        return मापन;
    }
}
