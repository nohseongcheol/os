// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unicode_Boleng 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Diteng_Boleng) { return Diteng_Boleng.getBytes(StandardCharsets.UTF_8); }
    public static String Sirolola_tshedimosetso(byte[] Diteng_Boleng) { return new String(Diteng_Boleng, StandardCharsets.UTF_8); }
    public static String fokotsa_ntsifatso_Boleng(String Diteng_Boleng) { return Normalizer.normalize(Diteng_Boleng, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Diteng_Boleng) { return Diteng_Boleng.codePointCount(0, Diteng_Boleng.length()); }
    public static List<String> 낱말(String Diteng_Boleng, Locale Puo) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Puo);
        나누개.setText(Diteng_Boleng);
        List<String> 결과 = new ArrayList<>();
        int dirisa = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; dirisa = 끝, 끝 = 나누개.next())
            결과.add(Diteng_Boleng.substring(dirisa, 끝));
        return 결과;
    }
}
