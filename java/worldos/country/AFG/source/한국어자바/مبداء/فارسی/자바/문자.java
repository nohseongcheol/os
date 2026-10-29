// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 یونیکد_مقدار کد_مقدار 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String محتوا_مقدار) { return محتوا_مقدار.getBytes(StandardCharsets.UTF_8); }
    public static String رمزگشایی_داده_ها(byte[] محتوا_مقدار) { return new String(محتوا_مقدار, StandardCharsets.UTF_8); }
    public static String بهنجار_کردن_مقدار(String محتوا_مقدار) { return Normalizer.normalize(محتوا_مقدار, Normalizer.Form.NFC); }
    public static int 코드포인트수(String محتوا_مقدار) { return محتوا_مقدار.codePointCount(0, محتوا_مقدار.length()); }
    public static List<String> 낱말(String محتوا_مقدار, Locale زبان) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(زبان);
        나누개.setText(محتوا_مقدار);
        List<String> سنجش = new ArrayList<>();
        int اجرا_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; اجرا_2 = 끝, 끝 = 나누개.next())
            سنجش.add(محتوا_مقدار.substring(اجرا_2, 끝));
        return سنجش;
    }
}
