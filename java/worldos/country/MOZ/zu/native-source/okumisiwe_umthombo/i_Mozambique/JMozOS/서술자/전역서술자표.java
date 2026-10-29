// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package i_Mozambique.JMozOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 isimo_inani isigaba_inani 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ngemuva_inani;
        private final int 한계;
        private final int ungeno_inani;

        조각(int ngemuva_inani, int 한계, int ungeno_inani) {
            this.ngemuva_inani = ngemuva_inani;
            this.한계 = 한계;
            this.ungeno_inani = ungeno_inani;
        }

        public int ngemuva_inani() { return ngemuva_inani; }
        public int 한계() { return 한계; }
        public int ungeno_inani() { return ungeno_inani; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ngemuva_inani, int 한계, int ungeno_inani) {
        조각들.add(new 조각(ngemuva_inani, 한계, ungeno_inani));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void isethi_inani_elimisiwe() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

