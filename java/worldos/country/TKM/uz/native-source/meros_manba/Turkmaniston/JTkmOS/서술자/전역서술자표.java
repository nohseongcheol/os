// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 holat_VALUE_e10195a1 bo_lim_VALUE_366e0bfa 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Fon_VALUE;
        private final int 한계;
        private final int kirish_huquqi_VALUE;

        조각(int Fon_VALUE, int 한계, int kirish_huquqi_VALUE) {
            this.Fon_VALUE = Fon_VALUE;
            this.한계 = 한계;
            this.kirish_huquqi_VALUE = kirish_huquqi_VALUE;
        }

        public int Fon_VALUE() { return Fon_VALUE; }
        public int 한계() { return 한계; }
        public int kirish_huquqi_VALUE() { return kirish_huquqi_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Fon_VALUE, int 한계, int kirish_huquqi_VALUE) {
        조각들.add(new 조각(Fon_VALUE, 한계, kirish_huquqi_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void to_plam_sukut_bo_yicha_qiymat() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

