// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ዩኒኮድ_ዋጋ 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ትሕዝቶ_ዋጋ) { return ትሕዝቶ_ዋጋ.getBytes(StandardCharsets.UTF_8); }
    public static String ምስጢር_ፍታሕ_ሓበሬታ(byte[] ትሕዝቶ_ዋጋ) { return new String(ትሕዝቶ_ዋጋ, StandardCharsets.UTF_8); }
    public static String ኖርማላይዝ_ዋጋ(String ትሕዝቶ_ዋጋ) { return Normalizer.normalize(ትሕዝቶ_ዋጋ, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ትሕዝቶ_ዋጋ) { return ትሕዝቶ_ዋጋ.codePointCount(0, ትሕዝቶ_ዋጋ.length()); }
    public static List<String> 낱말(String ትሕዝቶ_ዋጋ, Locale ቋንቋ) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ቋንቋ);
        나누개.setText(ትሕዝቶ_ዋጋ);
        List<String> 결과 = new ArrayList<>();
        int ኣኺድ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ኣኺድ = 끝, 끝 = 나누개.next())
            결과.add(ትሕዝቶ_ዋጋ.substring(ኣኺድ, 끝));
        return 결과;
    }
}
