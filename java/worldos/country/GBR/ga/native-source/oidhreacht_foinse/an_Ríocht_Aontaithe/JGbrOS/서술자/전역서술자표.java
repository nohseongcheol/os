// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 staid_VALUE rannán_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Cúlra_VALUE;
        private final int 한계;
        private final int rochtain_VALUE;

        조각(int Cúlra_VALUE, int 한계, int rochtain_VALUE) {
            this.Cúlra_VALUE = Cúlra_VALUE;
            this.한계 = 한계;
            this.rochtain_VALUE = rochtain_VALUE;
        }

        public int Cúlra_VALUE() { return Cúlra_VALUE; }
        public int 한계() { return 한계; }
        public int rochtain_VALUE() { return rochtain_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Cúlra_VALUE, int 한계, int rochtain_VALUE) {
        조각들.add(new 조각(Cúlra_VALUE, 한계, rochtain_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void tacar_luach_réamhshocraithe() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

