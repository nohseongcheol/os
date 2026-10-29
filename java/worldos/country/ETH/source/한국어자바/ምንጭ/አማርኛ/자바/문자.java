// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ዩኒኮድ_እሴት 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ይዘት_እሴት) { return ይዘት_እሴት.getBytes(StandardCharsets.UTF_8); }
    public static String ምስጠራውን_ፍታ_ውሂብ(byte[] ይዘት_እሴት) { return new String(ይዘት_እሴት, StandardCharsets.UTF_8); }
    public static String አጠናቅር_እሴት(String ይዘት_እሴት) { return Normalizer.normalize(ይዘት_እሴት, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ይዘት_እሴት) { return ይዘት_እሴት.codePointCount(0, ይዘት_እሴት.length()); }
    public static List<String> 낱말(String ይዘት_እሴት, Locale ቋንቋ) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ቋንቋ);
        나누개.setText(ይዘት_እሴት);
        List<String> ልኬት = new ArrayList<>();
        int ማስኬጃ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ማስኬጃ = 끝, 끝 = 나누개.next())
            ልኬት.add(ይዘት_እሴት.substring(ማስኬጃ, 끝));
        return ልኬት;
    }
}
