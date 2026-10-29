// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Ýunikod_baha 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Mazmun_baha) { return Mazmun_baha.getBytes(StandardCharsets.UTF_8); }
    public static String koddan_aç_maglumat(byte[] Mazmun_baha) { return new String(Mazmun_baha, StandardCharsets.UTF_8); }
    public static String adaty_ýagdaýa_getir_baha(String Mazmun_baha) { return Normalizer.normalize(Mazmun_baha, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Mazmun_baha) { return Mazmun_baha.codePointCount(0, Mazmun_baha.length()); }
    public static List<String> 낱말(String Mazmun_baha, Locale Dil) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Dil);
        나누개.setText(Mazmun_baha);
        List<String> 결과 = new ArrayList<>();
        int Bitir = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Bitir = 끝, 끝 = 나누개.next())
            결과.add(Mazmun_baha.substring(Bitir, 끝));
        return 결과;
    }
}
