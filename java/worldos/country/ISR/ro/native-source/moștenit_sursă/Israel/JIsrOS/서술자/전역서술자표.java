// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Israel.JIsrOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Stare_VALUE secțiune_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int tapet_VALUE;
        private final int 한계;
        private final int acces_VALUE;

        조각(int tapet_VALUE, int 한계, int acces_VALUE) {
            this.tapet_VALUE = tapet_VALUE;
            this.한계 = 한계;
            this.acces_VALUE = acces_VALUE;
        }

        public int tapet_VALUE() { return tapet_VALUE; }
        public int 한계() { return 한계; }
        public int acces_VALUE() { return acces_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int adăuga_intrare(int tapet_VALUE, int 한계, int acces_VALUE) {
        조각들.add(new 조각(tapet_VALUE, 한계, acces_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void set_valoare_implicită() {
        조각들.clear();
        adăuga_intrare(0, 0, 0);
        adăuga_intrare(0, 0xfffff, 0x9a);
        adăuga_intrare(0, 0xfffff, 0x92);
        adăuga_intrare(0, 0xfffff, 0xfa);
        adăuga_intrare(0, 0xfffff, 0xf2);
    }
}

