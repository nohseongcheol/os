// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.HệThốngTệp;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Đọc bốn phân vùng chính của DOS MBR. */
public final class bảngTraPhânVùngChínhThức {
    public static final class giáTrịPhânVùng {
        private final int giáTrịLoại;
        private final long bắtChạyMụcĐoạn;
        private final long sốLượngMụcĐoạn;

        giáTrịPhânVùng(int giáTrịLoại, long bắtChạyMụcĐoạn, long sốLượngMụcĐoạn) {
            this.giáTrịLoại = giáTrịLoại;
            this.bắtChạyMụcĐoạn = bắtChạyMụcĐoạn;
            this.sốLượngMụcĐoạn = sốLượngMụcĐoạn;
        }

        public int giáTrịLoại() { return giáTrịLoại; }
        public long bắtChạyMụcĐoạn() { return bắtChạyMụcĐoạn; }
        public long sốLượngMụcĐoạn() { return sốLượngMụcĐoạn; }
    }

    public List<giáTrịPhânVùng> đọc(byte[] mụcĐoạnĐầuTiên) {
        if (mụcĐoạnĐầuTiên == null || mụcĐoạnĐầuTiên.length < 512
                || (mụcĐoạnĐầuTiên[510] & 0xff) != 0x55 || (mụcĐoạnĐầuTiên[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<giáTrịPhânVùng> kếtQuả = new ArrayList<giáTrịPhânVùng>();
        for (int sốHiệu = 0; sốHiệu < 4; sốHiệu++) {
            int vịTrí = 446 + sốHiệu * 16;
            int giáTrịLoại = mụcĐoạnĐầuTiên[vịTrí + 4] & 0xff;
            long chạy = sốNguyênThứTựByteNhỏ(mụcĐoạnĐầuTiên, vịTrí + 8);
            long cỡ = sốNguyênThứTựByteNhỏ(mụcĐoạnĐầuTiên, vịTrí + 12);
            if (giáTrịLoại != 0 && cỡ != 0) {
                kếtQuả.add(new giáTrịPhânVùng(giáTrịLoại, chạy, cỡ));
            }
        }
        return Collections.unmodifiableList(kếtQuả);
    }

    private long sốNguyênThứTựByteNhỏ(byte[] DữLiệu, int vịTrí) {
        return (DữLiệu[vịTrí] & 0xffL)
                | ((DữLiệu[vịTrí + 1] & 0xffL) << 8)
                | ((DữLiệu[vịTrí + 2] & 0xffL) << 16)
                | ((DữLiệu[vịTrí + 3] & 0xffL) << 24);
    }
}

