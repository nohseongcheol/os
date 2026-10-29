// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 유니코드 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String مواد_قدر) { return مواد_قدر.getBytes(StandardCharsets.UTF_8); }
    public static String طئي_ٿيل_ڪوائف(byte[] مواد_قدر) { return new String(مواد_قدر, StandardCharsets.UTF_8); }
    public static String عام_ڪرڻ_قدر(String مواد_قدر) { return Normalizer.normalize(مواد_قدر, Normalizer.Form.NFC); }
    public static int 코드포인트수(String مواد_قدر) { return مواد_قدر.codePointCount(0, مواد_قدر.length()); }
    public static List<String> 낱말(String مواد_قدر, Locale ٻولي) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ٻولي);
        나누개.setText(مواد_قدر);
        List<String> 결과 = new ArrayList<>();
        int هلائڻ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; هلائڻ = 끝, 끝 = 나누개.next())
            결과.add(مواد_قدر.substring(هلائڻ, 끝));
        return 결과;
    }
}
