// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.ThiếtBị;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Quản lý kết quả tìm thiết bị PCI và các giá trị BAR/IRQ. */
public final class BộQuảnLýĐườngTruyềnChungNgoạiVi {
    public static final class ThiếtBị {
        private final int địnhDanhNhàCungCấp;
        private final int địnhDanhThiếtBị;
        private final int cơSởVàoRa;
        private final int sốNgắtXửLý;

        public ThiếtBị(int địnhDanhNhàCungCấp, int địnhDanhThiếtBị, int cơSởVàoRa, int sốNgắtXửLý) {
            this.địnhDanhNhàCungCấp = địnhDanhNhàCungCấp;
            this.địnhDanhThiếtBị = địnhDanhThiếtBị;
            this.cơSởVàoRa = cơSởVàoRa;
            this.sốNgắtXửLý = sốNgắtXửLý;
        }

        public int địnhDanhNhàCungCấp() { return địnhDanhNhàCungCấp; }
        public int địnhDanhThiếtBị() { return địnhDanhThiếtBị; }
        public int cơSởVàoRa() { return cơSởVàoRa; }
        public int sốNgắtXửLý() { return sốNgắtXửLý; }
    }

    private final List<ThiếtBị> danhSáchCácThiếtBị = new ArrayList<ThiếtBị>();

    public void giáTrịĐãPhátHiện(ThiếtBị ThiếtBị) {
        danhSáchCácThiếtBị.add(ThiếtBị);
    }

    public List<ThiếtBị> danhSáchCácThiếtBị() {
        return Collections.unmodifiableList(danhSáchCácThiếtBị);
    }

    public ThiếtBị tìmMục(int địnhDanhNhàCungCấp, int địnhDanhThiếtBị) {
        for (ThiếtBị ứngViên : danhSáchCácThiếtBị) {
            if (ứngViên.địnhDanhNhàCungCấp == địnhDanhNhàCungCấp && ứngViên.địnhDanhThiếtBị == địnhDanhThiếtBị) {
                return ứngViên;
            }
        }
        return null;
    }
}

