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
    public static byte[] 부호화(String اجزاء_قدر) { return اجزاء_قدر.getBytes(StandardCharsets.UTF_8); }
    public static String ضابطہ_کشائی_کرو_کوائف(byte[] اجزاء_قدر) { return new String(اجزاء_قدر, StandardCharsets.UTF_8); }
    public static String عام_بناؤ_قدر(String اجزاء_قدر) { return Normalizer.normalize(اجزاء_قدر, Normalizer.Form.NFC); }
    public static int 코드포인트수(String اجزاء_قدر) { return اجزاء_قدر.codePointCount(0, اجزاء_قدر.length()); }
    public static List<String> 낱말(String اجزاء_قدر, Locale زبان) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(زبان);
        나누개.setText(اجزاء_قدر);
        List<String> 결과 = new ArrayList<>();
        int چلاؤ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; چلاؤ = 끝, 끝 = 나누개.next())
            결과.add(اجزاء_قدر.substring(چلاؤ, 끝));
        return 결과;
    }
}
