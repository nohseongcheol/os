// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Việt_Nam.JVnmOS.HệThốngTệp;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Kiểm chứng phần đầu và đoạn nạp của tệp thực thi ELF32 thứ tự byte nhỏ trước. */
public final class BộNạpTệpThựcThi {
    public static final class giáTrịMụcĐoạn {
        private final int giáTrịLoại;
        private final int giáTrịCờ;
        private final int địaChỉ;
        private final int vịTríTệp;
        private final int cỡ;

        giáTrịMụcĐoạn(int giáTrịLoại, int giáTrịCờ, int địaChỉ, int vịTríTệp, int cỡ) {
            this.giáTrịLoại = giáTrịLoại;
            this.giáTrịCờ = giáTrịCờ;
            this.địaChỉ = địaChỉ;
            this.vịTríTệp = vịTríTệp;
            this.cỡ = cỡ;
        }

        public int giáTrịLoại() {
            return giáTrịLoại;
        }

        public int giáTrịCờ() {
            return giáTrịCờ;
        }

        public int địaChỉ() {
            return địaChỉ;
        }

        public int vịTríTệp() {
            return vịTríTệp;
        }

        public int cỡ() {
            return cỡ;
        }
    }

    public static final class ảnh {
        private final int bắtChạyĐịaChỉ;
        private final List<giáTrịMụcĐoạn> danhSáchCácMụcĐoạn;

        ảnh(int bắtChạyĐịaChỉ, List<giáTrịMụcĐoạn> danhSáchCácMụcĐoạn) {
            this.bắtChạyĐịaChỉ = bắtChạyĐịaChỉ;
            this.danhSáchCácMụcĐoạn = Collections.unmodifiableList(danhSáchCácMụcĐoạn);
        }

        public int bắtChạyĐịaChỉ() {
            return bắtChạyĐịaChỉ;
        }

        public List<giáTrịMụcĐoạn> danhSáchCácMụcĐoạn() {
            return danhSáchCácMụcĐoạn;
        }
    }

    public ảnh CácPhépKiểmTra(byte[] DữLiệu) {
        if (DữLiệu == null || DữLiệu.length < 52
                || DữLiệu[0] != 0x7f || DữLiệu[1] != 'E' || DữLiệu[2] != 'L' || DữLiệu[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (DữLiệu[4] != 1 || DữLiệu[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int bắtChạyĐịaChỉ = phânTíchCúPhápSốNguyên(DữLiệu, 24);
        int vịTríBảngTraMụcĐoạn = phânTíchCúPhápSốNguyên(DữLiệu, 32);
        int cỡMụcMụcĐoạn = đọcSốNguyênNgắnKiểu(DữLiệu, 46);
        int sốLượngMụcĐoạn = đọcSốNguyênNgắnKiểu(DữLiệu, 48);
        if (cỡMụcMụcĐoạn < 40 || vịTríBảngTraMụcĐoạn < 0
                || (long) vịTríBảngTraMụcĐoạn + (long) cỡMụcMụcĐoạn * sốLượngMụcĐoạn > DữLiệu.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<giáTrịMụcĐoạn> danhSáchCácMụcĐoạn = new ArrayList<giáTrịMụcĐoạn>();
        for (int sốHiệu = 0; sốHiệu < sốLượngMụcĐoạn; sốHiệu++) {
            int vịTrí = vịTríBảngTraMụcĐoạn + sốHiệu * cỡMụcMụcĐoạn;
            int giáTrịLoại = phânTíchCúPhápSốNguyên(DữLiệu, vịTrí + 4);
            int giáTrịCờ = phânTíchCúPhápSốNguyên(DữLiệu, vịTrí + 8);
            int địaChỉ = phânTíchCúPhápSốNguyên(DữLiệu, vịTrí + 12);
            int vịTríTệp = phânTíchCúPhápSốNguyên(DữLiệu, vịTrí + 16);
            int cỡ = phânTíchCúPhápSốNguyên(DữLiệu, vịTrí + 20);
            if (cỡ < 0 || (giáTrịLoại != 8 && ((long) vịTríTệp + cỡ > DữLiệu.length || vịTríTệp < 0))) {
                throw new IllegalArgumentException("ELF giáTrịMụcĐoạn DữLiệu 범위가 올바르지 않습니다.");
            }
            danhSáchCácMụcĐoạn.add(new giáTrịMụcĐoạn(giáTrịLoại, giáTrịCờ, địaChỉ, vịTríTệp, cỡ));
        }
        return new ảnh(bắtChạyĐịaChỉ, danhSáchCácMụcĐoạn);
    }

    private int phânTíchCúPhápSốNguyên(byte[] DữLiệu, int vịTrí) {
        if (vịTrí < 0 || vịTrí > DữLiệu.length - 4) {
            throw new IllegalArgumentException("ELF SốNguyên 범위를 벗어났습니다.");
        }
        return (DữLiệu[vịTrí] & 0xff)
                | ((DữLiệu[vịTrí + 1] & 0xff) << 8)
                | ((DữLiệu[vịTrí + 2] & 0xff) << 16)
                | ((DữLiệu[vịTrí + 3] & 0xff) << 24);
    }

    private int đọcSốNguyênNgắnKiểu(byte[] DữLiệu, int vịTrí) {
        if (vịTrí < 0 || vịTrí > DữLiệu.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 SốNguyên 범위를 벗어났습니다.");
        }
        return (DữLiệu[vịTrí] & 0xff) | ((DữLiệu[vịTrí + 1] & 0xff) << 8);
    }
}
