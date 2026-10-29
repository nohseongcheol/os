// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Юникод_ЗНАЧЕН кодовое_значение 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] кодировать(String контент_ЗНАЧЕН) { return контент_ЗНАЧЕН.getBytes(StandardCharsets.UTF_8); }
    public static String расшифровать_данные(byte[] контент_ЗНАЧЕН) { return new String(контент_ЗНАЧЕН, StandardCharsets.UTF_8); }
    public static String нормализовать_ЗНАЧЕН(String контент_ЗНАЧЕН) { return Normalizer.normalize(контент_ЗНАЧЕН, Normalizer.Form.NFC); }
    public static int код_знака_СЧЁТ(String контент_ЗНАЧЕН) { return контент_ЗНАЧЕН.codePointCount(0, контент_ЗНАЧЕН.length()); }
    public static List<String> 낱말(String контент_ЗНАЧЕН, Locale Язык) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Язык);
        나누개.setText(контент_ЗНАЧЕН);
        List<String> результат = new ArrayList<>();
        int запустить = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; запустить = 끝, 끝 = 나누개.next())
            результат.add(контент_ЗНАЧЕН.substring(запустить, 끝));
        return результат;
    }
}
