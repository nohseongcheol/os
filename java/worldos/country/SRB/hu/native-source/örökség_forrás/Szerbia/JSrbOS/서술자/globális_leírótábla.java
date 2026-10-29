// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szerbia.JSrbOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Állapot_ÉRTÉK szakasz_ÉRTÉK 설정값을 보관한다. */
public final class globális_leírótábla {
    public static final class 조각 {
        private final int Háttér_ÉRTÉK;
        private final int 한계;
        private final int hozzáfér_ÉRTÉK;

        조각(int Háttér_ÉRTÉK, int 한계, int hozzáfér_ÉRTÉK) {
            this.Háttér_ÉRTÉK = Háttér_ÉRTÉK;
            this.한계 = 한계;
            this.hozzáfér_ÉRTÉK = hozzáfér_ÉRTÉK;
        }

        public int Háttér_ÉRTÉK() { return Háttér_ÉRTÉK; }
        public int 한계() { return 한계; }
        public int hozzáfér_ÉRTÉK() { return hozzáfér_ÉRTÉK; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int hozzáfűz_bejegyzés(int Háttér_ÉRTÉK, int 한계, int hozzáfér_ÉRTÉK) {
        조각들.add(new 조각(Háttér_ÉRTÉK, 한계, hozzáfér_ÉRTÉK));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void halmaz_alapértelmezett_érték() {
        조각들.clear();
        hozzáfűz_bejegyzés(0, 0, 0);
        hozzáfűz_bejegyzés(0, 0xfffff, 0x9a);
        hozzáfűz_bejegyzés(0, 0xfffff, 0x92);
        hozzáfűz_bejegyzés(0, 0xfffff, 0xfa);
        hozzáfűz_bejegyzés(0, 0xfffff, 0xf2);
    }
}

