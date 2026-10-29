// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Юникод_қимат 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Мӯҳтаво_қимат) { return Мӯҳтаво_қимат.getBytes(StandardCharsets.UTF_8); }
    public static String рамзкушоӣ_кардан_иттилоот(byte[] Мӯҳтаво_қимат) { return new String(Мӯҳтаво_қимат, StandardCharsets.UTF_8); }
    public static String ба_тартиб_даровардан_қимат(String Мӯҳтаво_қимат) { return Normalizer.normalize(Мӯҳтаво_қимат, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Мӯҳтаво_қимат) { return Мӯҳтаво_қимат.codePointCount(0, Мӯҳтаво_қимат.length()); }
    public static List<String> 낱말(String Мӯҳтаво_қимат, Locale Забон) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Забон);
        나누개.setText(Мӯҳтаво_қимат);
        List<String> 결과 = new ArrayList<>();
        int порча = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; порча = 끝, 끝 = 나누개.next())
            결과.add(Мӯҳтаво_қимат.substring(порча, 끝));
        return 결과;
    }
}
