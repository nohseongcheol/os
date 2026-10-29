// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unicode_njaru 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String loowdi_njaru) { return loowdi_njaru.getBytes(StandardCharsets.UTF_8); }
    public static String dokkitde_keɓe(byte[] loowdi_njaru) { return new String(loowdi_njaru, StandardCharsets.UTF_8); }
    public static String 정규화(String loowdi_njaru) { return Normalizer.normalize(loowdi_njaru, Normalizer.Form.NFC); }
    public static int 코드포인트수(String loowdi_njaru) { return loowdi_njaru.codePointCount(0, loowdi_njaru.length()); }
    public static List<String> 낱말(String loowdi_njaru, Locale 언어) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(언어);
        나누개.setText(loowdi_njaru);
        List<String> 결과 = new ArrayList<>();
        int huutoraade = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; huutoraade = 끝, 끝 = 나누개.next())
            결과.add(loowdi_njaru.substring(huutoraade, 끝));
        return 결과;
    }
}
