// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 යුනිකෝඩ්_අගය 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String අන්තර්ගතය_අගය) { return අන්තර්ගතය_අගය.getBytes(StandardCharsets.UTF_8); }
    public static String විගුප්ත_කේතනය_කරන්න_දත්ත(byte[] අන්තර්ගතය_අගය) { return new String(අන්තර්ගතය_අගය, StandardCharsets.UTF_8); }
    public static String ප්_රමත_කරන්න_අගය(String අන්තර්ගතය_අගය) { return Normalizer.normalize(අන්තර්ගතය_අගය, Normalizer.Form.NFC); }
    public static int 코드포인트수(String අන්තර්ගතය_අගය) { return අන්තර්ගතය_අගය.codePointCount(0, අන්තර්ගතය_අගය.length()); }
    public static List<String> 낱말(String අන්තර්ගතය_අගය, Locale භාෂාව) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(භාෂාව);
        나누개.setText(අන්තර්ගතය_අගය);
        List<String> 결과 = new ArrayList<>();
        int ක්_රියාත්මක_කරන්න_2 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ක්_රියාත්මක_කරන්න_2 = 끝, 끝 = 나누개.next())
            결과.add(අන්තර්ගතය_අගය.substring(ක්_රියාත්මක_කරන්න_2, 끝));
        return 결과;
    }
}
