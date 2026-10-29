// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Statuss_VALUE sadaļa_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Fons_VALUE;
        private final int 한계;
        private final int piekļūt_VALUE;

        조각(int Fons_VALUE, int 한계, int piekļūt_VALUE) {
            this.Fons_VALUE = Fons_VALUE;
            this.한계 = 한계;
            this.piekļūt_VALUE = piekļūt_VALUE;
        }

        public int Fons_VALUE() { return Fons_VALUE; }
        public int 한계() { return 한계; }
        public int piekļūt_VALUE() { return piekļūt_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Pievienot_ievade(int Fons_VALUE, int 한계, int piekļūt_VALUE) {
        조각들.add(new 조각(Fons_VALUE, 한계, piekļūt_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void kopa_noklusējuma_vērtība() {
        조각들.clear();
        Pievienot_ievade(0, 0, 0);
        Pievienot_ievade(0, 0xfffff, 0x9a);
        Pievienot_ievade(0, 0xfffff, 0x92);
        Pievienot_ievade(0, 0xfffff, 0xfa);
        Pievienot_ievade(0, 0xfffff, 0xf2);
    }
}

