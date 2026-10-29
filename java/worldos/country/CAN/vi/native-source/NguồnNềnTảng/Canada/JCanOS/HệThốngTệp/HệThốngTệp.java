// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.HệThốngTệp;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** Mô hình được quản lý của kho tệp chỉ đọc, tương ứng lớp đọc FAT của engos. */
public final class HệThốngTệp {
    static final class tệpĐãMở {
        final byte[] DữLiệu;
        int vịTrí;
        int sốLượngThamChiếu = 1;

        tệpĐãMở(byte[] DữLiệu) {
            this.DữLiệu = DữLiệu;
        }
    }

    private final Map<String, byte[]> cácMụcTệp = new LinkedHashMap<String, byte[]>();

    public void thêmCuốiTệp(String tên, byte[] DữLiệu) {
        cácMụcTệp.put(tênChuẩnTắc(tên), Arrays.copyOf(DữLiệu, DữLiệu.length));
    }

    tệpĐãMở mở(String tên) {
        byte[] DữLiệu = cácMụcTệp.get(tênChuẩnTắc(tên));
        if (DữLiệu == null) {
            return null;
        }
        return new tệpĐãMở(DữLiệu);
    }

    public boolean giáTrịCóTồnTại(String tên) {
        return cácMụcTệp.containsKey(tênChuẩnTắc(tên));
    }

    public thôngTinTệp thôngTinHệThống(String tên) {
        byte[] DữLiệu = cácMụcTệp.get(tênChuẩnTắc(tên));
        if (DữLiệu == null) {
            return null;
        }
        return new thôngTinTệp(DữLiệu.length, 0100444);
    }

    private String tênChuẩnTắc(String tên) {
        if (tên == null) {
            throw new NullPointerException("Tệp 이름이 없습니다.");
        }
        String kếtQuả = tên.startsWith("/") ? tên.substring(1) : tên;
        return kếtQuả.toUpperCase(Locale.ROOT);
    }
}
