// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Юнікод_значэнне код_значэнне 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String кантэнт_значэнне) { return кантэнт_значэнне.getBytes(StandardCharsets.UTF_8); }
    public static String расшыфраваць_дадзеныя(byte[] кантэнт_значэнне) { return new String(кантэнт_значэнне, StandardCharsets.UTF_8); }
    public static String нармалізаваць_значэнне(String кантэнт_значэнне) { return Normalizer.normalize(кантэнт_значэнне, Normalizer.Form.NFC); }
    public static int 코드포인트수(String кантэнт_значэнне) { return кантэнт_значэнне.codePointCount(0, кантэнт_значэнне.length()); }
    public static List<String> 낱말(String кантэнт_значэнне, Locale Мова) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Мова);
        나누개.setText(кантэнт_значэнне);
        List<String> 결과 = new ArrayList<>();
        int Выканаць = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Выканаць = 끝, 끝 = 나누개.next())
            결과.add(кантэнт_значэнне.substring(Выканаць, 끝));
        return 결과;
    }
}
