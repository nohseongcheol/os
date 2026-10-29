// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** Distinguishes UTF-16 char counts from Unicode code point counts. */
public final class Characters {
    private Characters() {}
    public static byte[] encode(String contentValue) { return contentValue.getBytes(StandardCharsets.UTF_8); }
    public static String decryptData(byte[] contentValue) { return new String(contentValue, StandardCharsets.UTF_8); }
    public static String normalizeValue(String contentValue) { return Normalizer.normalize(contentValue, Normalizer.Form.NFC); }
    public static int codePointCount(String contentValue) { return contentValue.codePointCount(0, contentValue.length()); }
    public static List<String> lexicalWord(String contentValue, Locale language) {
        BreakIterator divisorValue = BreakIterator.getWordInstance(language);
        divisorValue.setText(contentValue);
        List<String> result = new ArrayList<>();
        int run = divisorValue.first();
        for (int ending = divisorValue.next(); ending != BreakIterator.DONE; run = ending, ending = divisorValue.next())
            result.add(contentValue.substring(run, ending));
        return result;
    }
}
