// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_uara CODE_uara 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Ihirangi_uara) { return Ihirangi_uara.getBytes(StandardCharsets.UTF_8); }
    public static String wetemuna_raraunga(byte[] Ihirangi_uara) { return new String(Ihirangi_uara, StandardCharsets.UTF_8); }
    public static String whakanoa_uara(String Ihirangi_uara) { return Normalizer.normalize(Ihirangi_uara, Normalizer.Form.NFC); }
    public static int waehere_pūāhua_COUNT(String Ihirangi_uara) { return Ihirangi_uara.codePointCount(0, Ihirangi_uara.length()); }
    public static List<String> 낱말(String Ihirangi_uara, Locale reo) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(reo);
        나누개.setText(Ihirangi_uara);
        List<String> mēhua = new ArrayList<>();
        int whakahaere = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; whakahaere = 끝, 끝 = 나누개.next())
            mēhua.add(Ihirangi_uara.substring(whakahaere, 끝));
        return mēhua;
    }
}
