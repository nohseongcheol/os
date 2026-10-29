// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ইউনিকোড_মান কোড_মান 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String সামগ্রি_মান) { return সামগ্রি_মান.getBytes(StandardCharsets.UTF_8); }
    public static String ডিক্রিপ্ট_ডাটা(byte[] সামগ্রি_মান) { return new String(সামগ্রি_মান, StandardCharsets.UTF_8); }
    public static String সাধারণকরণ_মান(String সামগ্রি_মান) { return Normalizer.normalize(সামগ্রি_মান, Normalizer.Form.NFC); }
    public static int 코드포인트수(String সামগ্রি_মান) { return সামগ্রি_মান.codePointCount(0, সামগ্রি_মান.length()); }
    public static List<String> 낱말(String সামগ্রি_মান, Locale ভাষা) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ভাষা);
        나누개.setText(সামগ্রি_মান);
        List<String> পরিমাপ = new ArrayList<>();
        int চালনা = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; চালনা = 끝, 끝 = 나누개.next())
            পরিমাপ.add(সামগ্রি_মান.substring(চালনা, 끝));
        return পরিমাপ;
    }
}
