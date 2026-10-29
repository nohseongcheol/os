// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ikhowudi_efanayo_ixabiso 코드 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String Isiqulatho_ixabiso) { return Isiqulatho_ixabiso.getBytes(StandardCharsets.UTF_8); }
    public static String buyisela_ubhalo_oluqhelekileyo_iingcombolo(byte[] Isiqulatho_ixabiso) { return new String(Isiqulatho_ixabiso, StandardCharsets.UTF_8); }
    public static String qhelekisa_ixabiso(String Isiqulatho_ixabiso) { return Normalizer.normalize(Isiqulatho_ixabiso, Normalizer.Form.NFC); }
    public static int 코드포인트수(String Isiqulatho_ixabiso) { return Isiqulatho_ixabiso.codePointCount(0, Isiqulatho_ixabiso.length()); }
    public static List<String> 낱말(String Isiqulatho_ixabiso, Locale Ulwimi) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(Ulwimi);
        나누개.setText(Isiqulatho_ixabiso);
        List<String> 결과 = new ArrayList<>();
        int Phumeza = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; Phumeza = 끝, 끝 = 나누개.next())
            결과.add(Isiqulatho_ixabiso.substring(Phumeza, 끝));
        return 결과;
    }
}
