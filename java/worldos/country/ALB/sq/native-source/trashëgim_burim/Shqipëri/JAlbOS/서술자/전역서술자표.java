// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Shqipëri.JAlbOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 status_VALUE seksion_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Sfond_VALUE;
        private final int 한계;
        private final int qasem_VALUE;

        조각(int Sfond_VALUE, int 한계, int qasem_VALUE) {
            this.Sfond_VALUE = Sfond_VALUE;
            this.한계 = 한계;
            this.qasem_VALUE = qasem_VALUE;
        }

        public int Sfond_VALUE() { return Sfond_VALUE; }
        public int 한계() { return 한계; }
        public int qasem_VALUE() { return qasem_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Sfond_VALUE, int 한계, int qasem_VALUE) {
        조각들.add(new 조각(Sfond_VALUE, 한계, qasem_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void bashkësi_vlerë_e_parazgjedhur() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

