// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_değer KOD_değer 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] kodlamak(String içerik_değer) { return içerik_değer.getBytes(StandardCharsets.UTF_8); }
    public static String şifre_çözmek_veri(byte[] içerik_değer) { return new String(içerik_değer, StandardCharsets.UTF_8); }
    public static String normalleştirmek_değer(String içerik_değer) { return Normalizer.normalize(içerik_değer, Normalizer.Form.NFC); }
    public static int kod_öğesi_BAĞ_DEĞ_SAY(String içerik_değer) { return içerik_değer.codePointCount(0, içerik_değer.length()); }
    public static List<String> 낱말(String içerik_değer, Locale Dil) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Dil);
        나누개.setText(içerik_değer);
        List<String> sonuç = new ArrayList<>();
        int çalıştır = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; çalıştır = 끝, 끝 = 나누개.next())
            sonuç.add(içerik_değer.substring(çalıştır, 끝));
        return sonuç;
    }
}
