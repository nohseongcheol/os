// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 jamakua_iparülein_ajutuu alüjalee_ajutuu 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int apa_ajanaa_ajutuu;
        private final int 한계;
        private final int a_ttaaya_ajutuu;

        조각(int apa_ajanaa_ajutuu, int 한계, int a_ttaaya_ajutuu) {
            this.apa_ajanaa_ajutuu = apa_ajanaa_ajutuu;
            this.한계 = 한계;
            this.a_ttaaya_ajutuu = a_ttaaya_ajutuu;
        }

        public int apa_ajanaa_ajutuu() { return apa_ajanaa_ajutuu; }
        public int 한계() { return 한계; }
        public int a_ttaaya_ajutuu() { return a_ttaaya_ajutuu; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int apa_ajanaa_ajutuu, int 한계, int a_ttaaya_ajutuu) {
        조각들.add(new 조각(apa_ajanaa_ajutuu, 한계, a_ttaaya_ajutuu));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void 기본값설정() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

