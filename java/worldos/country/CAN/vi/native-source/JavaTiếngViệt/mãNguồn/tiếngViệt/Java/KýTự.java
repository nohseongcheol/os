// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.Java;

import java.nio.charset.StandardCharsets;
import java.text.BreakIterator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** Phân biệt số char UTF-16 với số điểm mã Unicode. */
public final class KýTự {
    private KýTự() {}
    public static byte[] mãHóa(String giáTrịNộiDung) { return giáTrịNộiDung.getBytes(StandardCharsets.UTF_8); }
    public static String giảiMậtMãDữLiệu(byte[] giáTrịNộiDung) { return new String(giáTrịNộiDung, StandardCharsets.UTF_8); }
    public static String chuẩnHóaGiáTrị(String giáTrịNộiDung) { return Normalizer.normalize(giáTrịNộiDung, Normalizer.Form.NFC); }
    public static int sốLượngĐiểmMã(String giáTrịNộiDung) { return giáTrịNộiDung.codePointCount(0, giáTrịNộiDung.length()); }
    public static List<String> từTừVựng(String giáTrịNộiDung, Locale NgônNgữ) {
        BreakIterator giáTrịSốChia = BreakIterator.getWordInstance(NgônNgữ);
        giáTrịSốChia.setText(giáTrịNộiDung);
        List<String> kếtQuả = new ArrayList<>();
        int chạy = giáTrịSốChia.first();
        for (int phầnKết = giáTrịSốChia.next(); phầnKết != BreakIterator.DONE; chạy = phầnKết, phầnKết = giáTrịSốChia.next())
            kếtQuả.add(giáTrịNộiDung.substring(chạy, phầnKết));
        return kếtQuả;
    }
}
