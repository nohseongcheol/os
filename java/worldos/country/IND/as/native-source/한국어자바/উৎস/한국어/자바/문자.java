// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ইউনিক_ড_মান 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String সামগ্ৰী_মান) { return সামগ্ৰী_মান.getBytes(StandardCharsets.UTF_8); }
    public static String ডিক্ৰিপ্ট_কৰক_ডাটা(byte[] সামগ্ৰী_মান) { return new String(সামগ্ৰী_মান, StandardCharsets.UTF_8); }
    public static String সাধাৰণীকৰণ_কৰক_মান(String সামগ্ৰী_মান) { return Normalizer.normalize(সামগ্ৰী_মান, Normalizer.Form.NFC); }
    public static int 코드포인트수(String সামগ্ৰী_মান) { return সামগ্ৰী_মান.codePointCount(0, সামগ্ৰী_মান.length()); }
    public static List<String> 낱말(String সামগ্ৰী_মান, Locale ভাষা) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ভাষা);
        나누개.setText(সামগ্ৰী_মান);
        List<String> পৰিমাপ = new ArrayList<>();
        int সঞ্চালন = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; সঞ্চালন = 끝, 끝 = 나누개.next())
            পৰিমাপ.add(সামগ্ৰী_মান.substring(সঞ্চালন, 끝));
        return পৰিমাপ;
    }
}
