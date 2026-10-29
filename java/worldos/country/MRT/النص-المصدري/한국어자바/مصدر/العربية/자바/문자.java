// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 유니코드 رمز_قيمة_f3cd31ee 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] يرمّز(String محتوى_قيمة) { return محتوى_قيمة.getBytes(StandardCharsets.UTF_8); }
    public static String يفك_التشفير_بيانات(byte[] محتوى_قيمة) { return new String(محتوى_قيمة, StandardCharsets.UTF_8); }
    public static String يقلل_التكرار_قيمة(String محتوى_قيمة) { return Normalizer.normalize(محتوى_قيمة, Normalizer.Form.NFC); }
    public static int 코드포인트수(String محتوى_قيمة) { return محتوى_قيمة.codePointCount(0, محتوى_قيمة.length()); }
    public static List<String> 낱말(String محتوى_قيمة, Locale لغة) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(لغة);
        나누개.setText(محتوى_قيمة);
        List<String> نتيجة = new ArrayList<>();
        int تشغيل = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; تشغيل = 끝, 끝 = 나누개.next())
            نتيجة.add(محتوى_قيمة.substring(تشغيل, 끝));
        return نتيجة;
    }
}
