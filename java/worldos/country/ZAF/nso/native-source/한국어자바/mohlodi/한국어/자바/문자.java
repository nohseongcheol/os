// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Yunikhoute_boleng 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Diteng_boleng) { return Diteng_boleng.getBytes(StandardCharsets.UTF_8); }
    public static String boetša_sekeng_data(byte[] Diteng_boleng) { return new String(Diteng_boleng, StandardCharsets.UTF_8); }
    public static String fokotša_kopišo_boleng(String Diteng_boleng) { return Normalizer.normalize(Diteng_boleng, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Diteng_boleng) { return Diteng_boleng.codePointCount(0, Diteng_boleng.length()); }
    public static List<String> 낱말(String Diteng_boleng, Locale Polelo) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Polelo);
        나누개.setText(Diteng_boleng);
        List<String> 결과 = new ArrayList<>();
        int Diriša = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Diriša = 끝, 끝 = 나누개.next())
            결과.add(Diteng_boleng.substring(Diriša, 끝));
        return 결과;
    }
}
