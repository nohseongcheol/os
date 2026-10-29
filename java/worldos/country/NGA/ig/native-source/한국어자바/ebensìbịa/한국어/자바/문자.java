// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Yunīkoòdù_valuu 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ndịnà_valuu) { return ndịnà_valuu.getBytes(StandardCharsets.UTF_8); }
    public static String tụghee_edenzizo_datà(byte[] ndịnà_valuu) { return new String(ndịnà_valuu, StandardCharsets.UTF_8); }
    public static String mèzima_valuu(String ndịnà_valuu) { return Normalizer.normalize(ndịnà_valuu, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ndịnà_valuu) { return ndịnà_valuu.codePointCount(0, ndịnà_valuu.length()); }
    public static List<String> 낱말(String ndịnà_valuu, Locale Asụsụ) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Asụsụ);
        나누개.setText(ndịnà_valuu);
        List<String> 결과 = new ArrayList<>();
        int Bido = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Bido = 끝, 끝 = 나누개.next())
            결과.add(ndịnà_valuu.substring(Bido, 끝));
        return 결과;
    }
}
