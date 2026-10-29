// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 یونی_کوڈ_قدر 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String مشمول_قدر) { return مشمول_قدر.getBytes(StandardCharsets.UTF_8); }
    public static String خفیہ_کشائی_کریں_کوائف(byte[] مشمول_قدر) { return new String(مشمول_قدر, StandardCharsets.UTF_8); }
    public static String عمومی_بنائيں_قدر(String مشمول_قدر) { return Normalizer.normalize(مشمول_قدر, Normalizer.Form.NFC); }
    public static int 코드포인트수(String مشمول_قدر) { return مشمول_قدر.codePointCount(0, مشمول_قدر.length()); }
    public static List<String> 낱말(String مشمول_قدر, Locale زبان) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(زبان);
        나누개.setText(مشمول_قدر);
        List<String> پیمائش = new ArrayList<>();
        int چلائیں = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; چلائیں = 끝, 끝 = 나누개.next())
            پیمائش.add(مشمول_قدر.substring(چلائیں, 끝));
        return پیمائش;
    }
}
