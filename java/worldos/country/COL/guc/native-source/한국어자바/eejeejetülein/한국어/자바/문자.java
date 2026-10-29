// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 Unikoote_ajutuu 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String alu_ujatüü_ajutuu) { return alu_ujatüü_ajutuu.getBytes(StandardCharsets.UTF_8); }
    public static String ale_ejiraa_amoutuushi_atijaaya(byte[] alu_ujatüü_ajutuu) { return new String(alu_ujatüü_ajutuu, StandardCharsets.UTF_8); }
    public static String anaajaa_ajutuu(String alu_ujatüü_ajutuu) { return Normalizer.normalize(alu_ujatüü_ajutuu, Normalizer.Form.NFC); }
    public static int 코드포인트수(String alu_ujatüü_ajutuu) { return alu_ujatüü_ajutuu.codePointCount(0, alu_ujatüü_ajutuu.length()); }
    public static List<String> 낱말(String alu_ujatüü_ajutuu, Locale anüikii_komputatooralujatü) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(anüikii_komputatooralujatü);
        나누개.setText(alu_ujatüü_ajutuu);
        List<String> 결과 = new ArrayList<>();
        int 시작 = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; 시작 = 끝, 끝 = 나누개.next())
            결과.add(alu_ujatüü_ajutuu.substring(시작, 끝));
        return 결과;
    }
}
