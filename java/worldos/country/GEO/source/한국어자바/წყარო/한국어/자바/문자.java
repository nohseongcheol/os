// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 უნიკოდი_მნიშვნელობა კოდექსი_მნიშვნელობა 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String შიგთავსი_მნიშვნელობა) { return შიგთავსი_მნიშვნელობა.getBytes(StandardCharsets.UTF_8); }
    public static String გაშიფვრა_მონაცემები(byte[] შიგთავსი_მნიშვნელობა) { return new String(შიგთავსი_მნიშვნელობა, StandardCharsets.UTF_8); }
    public static String მოწესრიგება_მნიშვნელობა(String შიგთავსი_მნიშვნელობა) { return Normalizer.normalize(შიგთავსი_მნიშვნელობა, Normalizer.Form.NFC); }
    public static int 코드포인트수(String შიგთავსი_მნიშვნელობა) { return შიგთავსი_მნიშვნელობა.codePointCount(0, შიგთავსი_მნიშვნელობა.length()); }
    public static List<String> 낱말(String შიგთავსი_მნიშვნელობა, Locale ენა) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ენა);
        나누개.setText(შიგთავსი_მნიშვნელობა);
        List<String> გაზომვა = new ArrayList<>();
        int გაშვება = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; გაშვება = 끝, 끝 = 나누개.next())
            გაზომვა.add(შიგთავსი_მნიშვნელობა.substring(გაშვება, 끝));
        return გაზომვა;
    }
}
