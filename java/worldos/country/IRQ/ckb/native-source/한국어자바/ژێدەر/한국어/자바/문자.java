// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 یونیکۆد_نرخ 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ناوەرۆک_نرخ) { return ناوەرۆک_نرخ.getBytes(StandardCharsets.UTF_8); }
    public static String بێڕەمز_کردن_دەیتا(byte[] ناوەرۆک_نرخ) { return new String(ناوەرۆک_نرخ, StandardCharsets.UTF_8); }
    public static String ئاساییکردن_نرخ(String ناوەرۆک_نرخ) { return Normalizer.normalize(ناوەرۆک_نرخ, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ناوەرۆک_نرخ) { return ناوەرۆک_نرخ.codePointCount(0, ناوەرۆک_نرخ.length()); }
    public static List<String> 낱말(String ناوەرۆک_نرخ, Locale زمان) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(زمان);
        나누개.setText(ناوەرۆک_نرخ);
        List<String> 결과 = new ArrayList<>();
        int ڕادان = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ڕادان = 끝, 끝 = 나누개.next())
            결과.add(ناوەرۆک_نرخ.substring(ڕادان, 끝));
        return 결과;
    }
}
