// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unicode_xëyma 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Këmb_xëyma) { return Këmb_xëyma.getBytes(StandardCharsets.UTF_8); }
    public static String fecci_mbir(byte[] Këmb_xëyma) { return new String(Këmb_xëyma, StandardCharsets.UTF_8); }
    public static String yonnal_xëyma(String Këmb_xëyma) { return Normalizer.normalize(Këmb_xëyma, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Këmb_xëyma) { return Këmb_xëyma.codePointCount(0, Këmb_xëyma.length()); }
    public static List<String> 낱말(String Këmb_xëyma, Locale Làkk) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Làkk);
        나누개.setText(Këmb_xëyma);
        List<String> 결과 = new ArrayList<>();
        int daw = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; daw = 끝, 끝 = 나누개.next())
            결과.add(Këmb_xëyma.substring(daw, 끝));
        return 결과;
    }
}
