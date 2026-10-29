// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 يۇنىكود_قىممىتى 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String مەزمۇن_قىممىتى) { return مەزمۇن_قىممىتى.getBytes(StandardCharsets.UTF_8); }
    public static String شىفىر_يېشىش_مەلۇمات(byte[] مەزمۇن_قىممىتى) { return new String(مەزمۇن_قىممىتى, StandardCharsets.UTF_8); }
    public static String نورماللاشتۇرماق_قىممىتى(String مەزمۇن_قىممىتى) { return Normalizer.normalize(مەزمۇن_قىممىتى, Normalizer.Form.NFC); }
    public static int 코드포인트수(String مەزمۇن_قىممىتى) { return مەزمۇن_قىممىتى.codePointCount(0, مەزمۇن_قىممىتى.length()); }
    public static List<String> 낱말(String مەزمۇن_قىممىتى, Locale تىل) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(تىل);
        나누개.setText(مەزمۇن_قىممىتى);
        List<String> ئۆلچەم = new ArrayList<>();
        int ئىجرا_قىل_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ئىجرا_قىل_2 = 끝, 끝 = 나누개.next())
            ئۆلچەم.add(مەزمۇن_قىممىتى.substring(ئىجرا_قىل_2, 끝));
        return ئۆلچەم;
    }
}
