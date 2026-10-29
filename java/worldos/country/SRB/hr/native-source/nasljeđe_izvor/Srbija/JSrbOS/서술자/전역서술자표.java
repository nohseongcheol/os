// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Srbija.JSrbOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Stanje_VALUE sekcija_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class fragment_VALUE {
        private final int podloga_VALUE;
        private final int 한계;
        private final int pristup_VALUE;

        fragment_VALUE(int podloga_VALUE, int 한계, int pristup_VALUE) {
            this.podloga_VALUE = podloga_VALUE;
            this.한계 = 한계;
            this.pristup_VALUE = pristup_VALUE;
        }

        public int podloga_VALUE() { return podloga_VALUE; }
        public int 한계() { return 한계; }
        public int pristup_VALUE() { return pristup_VALUE; }
    }

    private final List<fragment_VALUE> 조각들 = new ArrayList<fragment_VALUE>();

    public int dodati_unos(int podloga_VALUE, int 한계, int pristup_VALUE) {
        조각들.add(new fragment_VALUE(podloga_VALUE, 한계, pristup_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<fragment_VALUE> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void skup_zadana_vrijednost() {
        조각들.clear();
        dodati_unos(0, 0, 0);
        dodati_unos(0, 0xfffff, 0x9a);
        dodati_unos(0, 0xfffff, 0x92);
        dodati_unos(0, 0xfffff, 0xfa);
        dodati_unos(0, 0xfffff, 0xf2);
    }
}

