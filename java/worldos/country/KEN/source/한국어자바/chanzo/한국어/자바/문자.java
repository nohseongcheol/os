// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Msimbosare_thamani msimbo_thamani 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String maudhui_thamani) { return maudhui_thamani.getBytes(StandardCharsets.UTF_8); }
    public static String simbua_fiche_data(byte[] maudhui_thamani) { return new String(maudhui_thamani, StandardCharsets.UTF_8); }
    public static String kawaidisha_thamani(String maudhui_thamani) { return Normalizer.normalize(maudhui_thamani, Normalizer.Form.NFC); }
    public static int 코드포인트수(String maudhui_thamani) { return maudhui_thamani.codePointCount(0, maudhui_thamani.length()); }
    public static List<String> 낱말(String maudhui_thamani, Locale Lugha) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Lugha);
        나누개.setText(maudhui_thamani);
        List<String> 결과 = new ArrayList<>();
        int endesha = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; endesha = 끝, 끝 = 나누개.next())
            결과.add(maudhui_thamani.substring(endesha, 끝));
        return 결과;
    }
}
