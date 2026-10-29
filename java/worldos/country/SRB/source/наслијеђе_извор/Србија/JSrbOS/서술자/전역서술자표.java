// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 стање_вриједност одељак_вриједност 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int постер_вриједност;
        private final int 한계;
        private final int приступ_вриједност;

        조각(int постер_вриједност, int 한계, int приступ_вриједност) {
            this.постер_вриједност = постер_вриједност;
            this.한계 = 한계;
            this.приступ_вриједност = приступ_вриједност;
        }

        public int постер_вриједност() { return постер_вриједност; }
        public int 한계() { return 한계; }
        public int приступ_вриједност() { return приступ_вриједност; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int додати_унос(int постер_вриједност, int 한계, int приступ_вриједност) {
        조각들.add(new 조각(постер_вриједност, 한계, приступ_вриједност));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void скуп_задана_вриједност() {
        조각들.clear();
        додати_унос(0, 0, 0);
        додати_унос(0, 0xfffff, 0x9a);
        додати_унос(0, 0xfffff, 0x92);
        додати_унос(0, 0xfffff, 0xfa);
        додати_унос(0, 0xfffff, 0xf2);
    }
}

