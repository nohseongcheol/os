// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Singapura.JSgpOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 status_VALUE seksyen_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int latar_VALUE;
        private final int 한계;
        private final int capai_VALUE;

        조각(int latar_VALUE, int 한계, int capai_VALUE) {
            this.latar_VALUE = latar_VALUE;
            this.한계 = 한계;
            this.capai_VALUE = capai_VALUE;
        }

        public int latar_VALUE() { return latar_VALUE; }
        public int 한계() { return 한계; }
        public int capai_VALUE() { return capai_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Tambah_pemasukan(int latar_VALUE, int 한계, int capai_VALUE) {
        조각들.add(new 조각(latar_VALUE, 한계, capai_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void set_nilai_lalai() {
        조각들.clear();
        Tambah_pemasukan(0, 0, 0);
        Tambah_pemasukan(0, 0xfffff, 0x9a);
        Tambah_pemasukan(0, 0xfffff, 0x92);
        Tambah_pemasukan(0, 0xfffff, 0xfa);
        Tambah_pemasukan(0, 0xfffff, 0xf2);
    }
}

