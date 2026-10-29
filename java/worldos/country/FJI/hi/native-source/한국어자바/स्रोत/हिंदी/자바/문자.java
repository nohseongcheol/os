// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 यूनिकोड_मान कोड_मान 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String सामग्री_मान) { return सामग्री_मान.getBytes(StandardCharsets.UTF_8); }
    public static String डिक्रिप्ट_करें_डेटा(byte[] सामग्री_मान) { return new String(सामग्री_मान, StandardCharsets.UTF_8); }
    public static String सामान्य_करें_मान(String सामग्री_मान) { return Normalizer.normalize(सामग्री_मान, Normalizer.Form.NFC); }
    public static int 코드포인트수(String सामग्री_मान) { return सामग्री_मान.codePointCount(0, सामग्री_मान.length()); }
    public static List<String> 낱말(String सामग्री_मान, Locale भाषा) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(भाषा);
        나누개.setText(सामग्री_मान);
        List<String> परिणाम = new ArrayList<>();
        int चलाएँ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; चलाएँ = 끝, 끝 = 나누개.next())
            परिणाम.add(सामग्री_मान.substring(चलाएँ, 끝));
        return परिणाम;
    }
}
