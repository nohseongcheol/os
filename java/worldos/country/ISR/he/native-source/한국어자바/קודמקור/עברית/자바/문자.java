// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 יוניקוד_ערך קוד_ערך 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] לקדד(String תוכן_ערך) { return תוכן_ערך.getBytes(StandardCharsets.UTF_8); }
    public static String פענח_נתונים(byte[] תוכן_ערך) { return new String(תוכן_ערך, StandardCharsets.UTF_8); }
    public static String לנרמל_ערך(String תוכן_ערך) { return Normalizer.normalize(תוכן_ערך, Normalizer.Form.NFC); }
    public static int 코드포인트수(String תוכן_ערך) { return תוכן_ערך.codePointCount(0, תוכן_ערך.length()); }
    public static List<String> 낱말(String תוכן_ערך, Locale שפה) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(שפה);
        나누개.setText(תוכן_ערך);
        List<String> תוצאה = new ArrayList<>();
        int הפעלה = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; הפעלה = 끝, 끝 = 나누개.next())
            תוצאה.add(תוכן_ערך.substring(הפעלה, 끝));
        return תוצאה;
    }
}
