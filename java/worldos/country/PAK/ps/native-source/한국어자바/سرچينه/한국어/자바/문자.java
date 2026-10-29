// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 يونيکوډ_ارزښت 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String منځپانګه_ارزښت) { return منځپانګه_ارزښت.getBytes(StandardCharsets.UTF_8); }
    public static String کوډ_پرانېستل_اومتوک(byte[] منځپانګه_ارزښت) { return new String(منځپانګه_ارزښت, StandardCharsets.UTF_8); }
    public static String لیوی_کول_ارزښت(String منځپانګه_ارزښت) { return Normalizer.normalize(منځپانګه_ارزښت, Normalizer.Form.NFC); }
    public static int 코드포인트수(String منځپانګه_ارزښت) { return منځپانګه_ارزښت.codePointCount(0, منځپانګه_ارزښت.length()); }
    public static List<String> 낱말(String منځپانګه_ارزښت, Locale کمپیوټر_ژبه) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(کمپیوټر_ژبه);
        나누개.setText(منځپانګه_ارزښت);
        List<String> 결과 = new ArrayList<>();
        int ځغلول = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ځغلول = 끝, 끝 = 나누개.next())
            결과.add(منځپانګه_ارزښت.substring(ځغلول, 끝));
        return 결과;
    }
}
