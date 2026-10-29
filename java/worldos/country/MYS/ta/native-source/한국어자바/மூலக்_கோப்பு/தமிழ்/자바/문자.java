// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 யூனிகோட்_மதிப்பு குறியீடு_மதிப்பு 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String உள்ளடக்கம்_மதிப்பு) { return உள்ளடக்கம்_மதிப்பு.getBytes(StandardCharsets.UTF_8); }
    public static String குறிநீக்கு_தரவு(byte[] உள்ளடக்கம்_மதிப்பு) { return new String(உள்ளடக்கம்_மதிப்பு, StandardCharsets.UTF_8); }
    public static String சீராக்கு_மதிப்பு(String உள்ளடக்கம்_மதிப்பு) { return Normalizer.normalize(உள்ளடக்கம்_மதிப்பு, Normalizer.Form.NFC); }
    public static int 코드포인트수(String உள்ளடக்கம்_மதிப்பு) { return உள்ளடக்கம்_மதிப்பு.codePointCount(0, உள்ளடக்கம்_மதிப்பு.length()); }
    public static List<String> 낱말(String உள்ளடக்கம்_மதிப்பு, Locale மொழி) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(மொழி);
        나누개.setText(உள்ளடக்கம்_மதிப்பு);
        List<String> அளவிடக்கூடியது = new ArrayList<>();
        int செயல்படுத்துக = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; செயல்படுத்துக = 끝, 끝 = 나누개.next())
            அளவிடக்கூடியது.add(உள்ளடக்கம்_மதிப்பு.substring(செயல்படுத்துக, 끝));
        return அளவிடக்கூடியது;
    }
}
