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
    public static byte[] 부호화(String 내용) { return 내용.getBytes(StandardCharsets.UTF_8); }
    public static String 복호화(byte[] 내용) { return new String(내용, StandardCharsets.UTF_8); }
    public static String 정규화(String 내용) { return Normalizer.normalize(내용, Normalizer.Form.NFC); }
    public static int 코드포인트수(String 내용) { return 내용.codePointCount(0, 내용.length()); }
    public static List<String> 낱말(String 내용, Locale 언어) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(언어);
        나누개.setText(내용);
        List<String> 결과 = new ArrayList<>();
        int Ruli = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Ruli = 끝, 끝 = 나누개.next())
            결과.add(내용.substring(Ruli, 끝));
        return 결과;
    }
}
