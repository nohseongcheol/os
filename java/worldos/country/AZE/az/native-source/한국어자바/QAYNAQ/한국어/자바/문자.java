// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_VALUE kod_VALUE 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Məzmun_VALUE) { return Məzmun_VALUE.getBytes(StandardCharsets.UTF_8); }
    public static String şifr_açmaq_verilənlər(byte[] Məzmun_VALUE) { return new String(Məzmun_VALUE, StandardCharsets.UTF_8); }
    public static String normallaşdırmaq_VALUE(String Məzmun_VALUE) { return Normalizer.normalize(Məzmun_VALUE, Normalizer.Form.NFC); }
    public static int simvol_kodu_COUNT(String Məzmun_VALUE) { return Məzmun_VALUE.codePointCount(0, Məzmun_VALUE.length()); }
    public static List<String> 낱말(String Məzmun_VALUE, Locale Dil) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Dil);
        나누개.setText(Məzmun_VALUE);
        List<String> ölçü = new ArrayList<>();
        int İcra_Et = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; İcra_Et = 끝, 끝 = 나누개.next())
            ölçü.add(Məzmun_VALUE.substring(İcra_Et, 끝));
        return ölçü;
    }
}
