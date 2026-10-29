// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 UNICODE_मोल CODE_मोल 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String अनुक्रमणिका_मोल) { return अनुक्रमणिका_मोल.getBytes(StandardCharsets.UTF_8); }
    public static String डिक्रिप्ट_डेटा(byte[] अनुक्रमणिका_मोल) { return new String(अनुक्रमणिका_मोल, StandardCharsets.UTF_8); }
    public static String सामान्य_स्थितीर_येवचें_मोल(String अनुक्रमणिका_मोल) { return Normalizer.normalize(अनुक्रमणिका_मोल, Normalizer.Form.NFC); }
    public static int वर्ण_कोड_COUNT(String अनुक्रमणिका_मोल) { return अनुक्रमणिका_मोल.codePointCount(0, अनुक्रमणिका_मोल.length()); }
    public static List<String> 낱말(String अनुक्रमणिका_मोल, Locale भास) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(भास);
        나누개.setText(अनुक्रमणिका_मोल);
        List<String> मेजप = new ArrayList<>();
        int चलोवप = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; चलोवप = 끝, 끝 = 나누개.next())
            मेजप.add(अनुक्रमणिका_मोल.substring(चलोवप, 끝));
        return मेजप;
    }
}
