// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukrajna.JUkrOS.mobil_ÉRTÉK;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI mobil_ÉRTÉK 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class tartozék_busz_kezelő {
    public static final class mobil_ÉRTÉK {
        private final int vendor_azonosító;
        private final int mobil_azonosító;
        private final int 입출력바탕;
        private final int megszakítás_szám;

        public mobil_ÉRTÉK(int vendor_azonosító, int mobil_azonosító, int 입출력바탕, int megszakítás_szám) {
            this.vendor_azonosító = vendor_azonosító;
            this.mobil_azonosító = mobil_azonosító;
            this.입출력바탕 = 입출력바탕;
            this.megszakítás_szám = megszakítás_szám;
        }

        public int vendor_azonosító() { return vendor_azonosító; }
        public int mobil_azonosító() { return mobil_azonosító; }
        public int 입출력바탕() { return 입출력바탕; }
        public int megszakítás_szám() { return megszakítás_szám; }
    }

    private final List<mobil_ÉRTÉK> Eszközök_Lista = new ArrayList<mobil_ÉRTÉK>();

    public void 발견(mobil_ÉRTÉK mobil_ÉRTÉK) {
        Eszközök_Lista.add(mobil_ÉRTÉK);
    }

    public List<mobil_ÉRTÉK> Eszközök_Lista() {
        return Collections.unmodifiableList(Eszközök_Lista);
    }

    public mobil_ÉRTÉK keres_bejegyzés(int vendor_azonosító, int mobil_azonosító) {
        for (mobil_ÉRTÉK 후보 : Eszközök_Lista) {
            if (후보.vendor_azonosító == vendor_azonosító && 후보.mobil_azonosító == mobil_azonosító) {
                return 후보;
            }
        }
        return null;
    }
}

