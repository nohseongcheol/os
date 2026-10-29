// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.자바;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** UTF-16 char 수와 유니코드 รหัส_ค่า 포인트 수를 구분한다. */
public final class 문자 {
    private 문자() {}
    public static byte[] เข้ารหัส(String เนื้อหา_ค่า) { return เนื้อหา_ค่า.getBytes(StandardCharsets.UTF_8); }
    public static String ถอดรหัสลับ_ข้อมูล(byte[] เนื้อหา_ค่า) { return new String(เนื้อหา_ค่า, StandardCharsets.UTF_8); }
    public static String นอร์มัลไลซ์_ค่า(String เนื้อหา_ค่า) { return Normalizer.normalize(เนื้อหา_ค่า, Normalizer.Form.NFC); }
    public static int 코드포인트수(String เนื้อหา_ค่า) { return เนื้อหา_ค่า.codePointCount(0, เนื้อหา_ค่า.length()); }
    public static List<String> 낱말(String เนื้อหา_ค่า, Locale ภาษา) {
        BreakIterator 나누개 = BreakIterator.getWordInstance(ภาษา);
        나누개.setText(เนื้อหา_ค่า);
        List<String> ผลลัพธ์ = new ArrayList<>();
        int เรียกใช้งาน = 나누개.first();
        for (int 끝 = 나누개.next(); 끝 != BreakIterator.DONE; เรียกใช้งาน = 끝, 끝 = 나누개.next())
            ผลลัพธ์.add(เนื้อหา_ค่า.substring(เรียกใช้งาน, 끝));
        return ผลลัพธ์;
    }
}
