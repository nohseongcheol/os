// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italija.JItaOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 stanje_VALUE odsek_VALUE 설정값을 보관한다. */
public final class GDT {
    public static final class 조각 {
        private final int Ozadje_VALUE;
        private final int 한계;
        private final int dostop_VALUE;

        조각(int Ozadje_VALUE, int 한계, int dostop_VALUE) {
            this.Ozadje_VALUE = Ozadje_VALUE;
            this.한계 = 한계;
            this.dostop_VALUE = dostop_VALUE;
        }

        public int Ozadje_VALUE() { return Ozadje_VALUE; }
        public int 한계() { return 한계; }
        public int dostop_VALUE() { return dostop_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int dodati_vnos(int Ozadje_VALUE, int 한계, int dostop_VALUE) {
        조각들.add(new 조각(Ozadje_VALUE, 한계, dostop_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void nabor_privzeta_vrednost() {
        조각들.clear();
        dodati_vnos(0, 0, 0);
        dodati_vnos(0, 0xfffff, 0x9a);
        dodati_vnos(0, 0xfffff, 0x92);
        dodati_vnos(0, 0xfffff, 0xfa);
        dodati_vnos(0, 0xfffff, 0xf2);
    }
}

