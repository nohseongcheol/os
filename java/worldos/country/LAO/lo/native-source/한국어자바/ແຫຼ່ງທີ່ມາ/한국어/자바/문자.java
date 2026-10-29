// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 ຢູນິໂຄດ_ຄ່າ ລະຫັດ_ຄ່າ 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] 부호화(String ເນື້ອໃນ_ຄ່າ_cb0f2404) { return ເນື້ອໃນ_ຄ່າ_cb0f2404.getBytes(StandardCharsets.UTF_8); }
    public static String ຖອດລະຫັດ_ຂໍ້ມູນ(byte[] ເນື້ອໃນ_ຄ່າ_cb0f2404) { return new String(ເນື້ອໃນ_ຄ່າ_cb0f2404, StandardCharsets.UTF_8); }
    public static String ເຮັດ_ເປັນ_ທໍາ_ມະ_ດາ_ຄ່າ(String ເນື້ອໃນ_ຄ່າ_cb0f2404) { return Normalizer.normalize(ເນື້ອໃນ_ຄ່າ_cb0f2404, Normalizer.Form.NFC); }
    public static int 코드포인트수(String ເນື້ອໃນ_ຄ່າ_cb0f2404) { return ເນື້ອໃນ_ຄ່າ_cb0f2404.codePointCount(0, ເນື້ອໃນ_ຄ່າ_cb0f2404.length()); }
    public static List<String> 낱말(String ເນື້ອໃນ_ຄ່າ_cb0f2404, Locale ພາ_ສາ) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ພາ_ສາ);
        나누개.setText(ເນື້ອໃນ_ຄ່າ_cb0f2404);
        List<String> ມາດຕະການ = new ArrayList<>();
        int ແລ່ນ = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; ແລ່ນ = 끝, 끝 = 나누개.next())
            ມາດຕະການ.add(ເນື້ອໃນ_ຄ່າ_cb0f2404.substring(ແລ່ນ, 끝));
        return ມາດຕະການ;
    }
}
