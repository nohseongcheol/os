// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Olek_VALUE jaotis_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int taust_VALUE;
        private final int 한계;
        private final int pöördus_VALUE;

        조각(int taust_VALUE, int 한계, int pöördus_VALUE) {
            this.taust_VALUE = taust_VALUE;
            this.한계 = 한계;
            this.pöördus_VALUE = pöördus_VALUE;
        }

        public int taust_VALUE() { return taust_VALUE; }
        public int 한계() { return 한계; }
        public int pöördus_VALUE() { return pöördus_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Lisa_kirje(int taust_VALUE, int 한계, int pöördus_VALUE) {
        조각들.add(new 조각(taust_VALUE, 한계, pöördus_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void hulk_vaikeväärtus() {
        조각들.clear();
        Lisa_kirje(0, 0, 0);
        Lisa_kirje(0, 0xfffff, 0x9a);
        Lisa_kirje(0, 0xfffff, 0x92);
        Lisa_kirje(0, 0xfffff, 0xfa);
        Lisa_kirje(0, 0xfffff, 0xf2);
    }
}

