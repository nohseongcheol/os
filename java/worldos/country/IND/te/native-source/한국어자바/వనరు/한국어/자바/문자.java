// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 యూనికోడ్_మూల్యం కోడ్_మూల్యం 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String విషయం_మూల్యం) { return విషయం_మూల్యం.getBytes(StandardCharsets.UTF_8); }
    public static String వ్యక్తపరుచు_డేటా(byte[] విషయం_మూల్యం) { return new String(విషయం_మూల్యం, StandardCharsets.UTF_8); }
    public static String సాధారణీకరించు_మూల్యం(String విషయం_మూల్యం) { return Normalizer.normalize(విషయం_మూల్యం, Normalizer.Form.NFC); }
    public static int 코드포인트수(String విషయం_మూల్యం) { return విషయం_మూల్యం.codePointCount(0, విషయం_మూల్యం.length()); }
    public static List<String> 낱말(String విషయం_మూల్యం, Locale భాష) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(భాష);
        나누개.setText(విషయం_మూల్యం);
        List<String> ప్రమాణం = new ArrayList<>();
        int నడుపుము = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; నడుపుము = 끝, 끝 = 나누개.next())
            ప్రమాణం.add(విషయం_మూల్యం.substring(నడుపుము, 끝));
        return ప్రమాణం;
    }
}
