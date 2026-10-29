// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unicode_ᏧᎬᏩᎶᏗᏯ 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) { return ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.getBytes(StandardCharsets.UTF_8); }
    public static String ᎠᎭᏓᏗᎭ_ᎦᏟᏌᏅᎯ(byte[] ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) { return new String(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, StandardCharsets.UTF_8); }
    public static String 정규화(String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) { return Normalizer.normalize(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) { return ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.codePointCount(0, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.length()); }
    public static List<String> 낱말(String ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, Locale ᎦᏬᏂᎯᏍᏗ) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ᎦᏬᏂᎯᏍᏗ);
        나누개.setText(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ);
        List<String> 결과 = new ArrayList<>();
        int ᎠᎢᏎᏍᏗ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ᎠᎢᏎᏍᏗ = 끝, 끝 = 나누개.next())
            결과.add(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.substring(ᎠᎢᏎᏍᏗ, 끝));
        return 결과;
    }
}
