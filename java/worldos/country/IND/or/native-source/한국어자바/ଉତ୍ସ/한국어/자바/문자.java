// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ଯୁନିକୋଡ୍_ମୂଲ୍ୟ 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ବିଷୟ_ମୂଲ୍ୟ) { return ବିଷୟ_ମୂଲ୍ୟ.getBytes(StandardCharsets.UTF_8); }
    public static String ଡିକ୍ରିପ୍ଟ_ଡାଟା(byte[] ବିଷୟ_ମୂଲ୍ୟ) { return new String(ବିଷୟ_ମୂଲ୍ୟ, StandardCharsets.UTF_8); }
    public static String ସ୍ୱାଭାବିକ_ମୂଲ୍ୟ(String ବିଷୟ_ମୂଲ୍ୟ) { return Normalizer.normalize(ବିଷୟ_ମୂଲ୍ୟ, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ବିଷୟ_ମୂଲ୍ୟ) { return ବିଷୟ_ମୂଲ୍ୟ.codePointCount(0, ବିଷୟ_ମୂଲ୍ୟ.length()); }
    public static List<String> 낱말(String ବିଷୟ_ମୂଲ୍ୟ, Locale ଭାଷା) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ଭାଷା);
        나누개.setText(ବିଷୟ_ମୂଲ୍ୟ);
        List<String> ମାପ = new ArrayList<>();
        int ଚଳାନ୍ତୁ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ଚଳାନ୍ତୁ = 끝, 끝 = 나누개.next())
            ମାପ.add(ବିଷୟ_ମୂଲ୍ୟ.substring(ଚଳାନ୍ତୁ, 끝));
        return ମାପ;
    }
}
