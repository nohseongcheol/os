// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unicode_iye 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Àkóónú_iye) { return Àkóónú_iye.getBytes(StandardCharsets.UTF_8); }
    public static String ṣàtúpalẹ̀_àrokò_détà(byte[] Àkóónú_iye) { return new String(Àkóónú_iye, StandardCharsets.UTF_8); }
    public static String ṣe_níwọ̀n_iye(String Àkóónú_iye) { return Normalizer.normalize(Àkóónú_iye, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Àkóónú_iye) { return Àkóónú_iye.codePointCount(0, Àkóónú_iye.length()); }
    public static List<String> 낱말(String Àkóónú_iye, Locale Èdè) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Èdè);
        나누개.setText(Àkóónú_iye);
        List<String> 결과 = new ArrayList<>();
        int Rọ́ọ̀nù = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Rọ́ọ̀nù = 끝, 끝 = 나누개.next())
            결과.add(Àkóónú_iye.substring(Rọ́ọ̀nù, 끝));
        return 결과;
    }
}
