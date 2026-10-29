// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Юнікод_значення код_значення 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] кодувати(String Вміст_значення) { return Вміст_значення.getBytes(StandardCharsets.UTF_8); }
    public static String дешифрувати_дані(byte[] Вміст_значення) { return new String(Вміст_значення, StandardCharsets.UTF_8); }
    public static String нормалізувати_значення(String Вміст_значення) { return Normalizer.normalize(Вміст_значення, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Вміст_значення) { return Вміст_значення.codePointCount(0, Вміст_значення.length()); }
    public static List<String> 낱말(String Вміст_значення, Locale Мови) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Мови);
        나누개.setText(Вміст_значення);
        List<String> результат = new ArrayList<>();
        int запустити = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; запустити = 끝, 끝 = 나누개.next())
            результат.add(Вміст_значення.substring(запустити, 끝));
        return результат;
    }
}
