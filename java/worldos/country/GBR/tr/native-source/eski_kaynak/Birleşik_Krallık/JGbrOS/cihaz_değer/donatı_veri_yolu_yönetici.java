// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Birleşik_Krallık.JGbrOS.cihaz_değer;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI cihaz_değer 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class donatı_veri_yolu_yönetici {
    public static final class cihaz_değer {
        private final int satıcı_tanımlayıcı;
        private final int cihaz_tanımlayıcı;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public cihaz_değer(int satıcı_tanımlayıcı, int cihaz_tanımlayıcı, int 입출력바탕, int 개입중단번호) {
            this.satıcı_tanımlayıcı = satıcı_tanımlayıcı;
            this.cihaz_tanımlayıcı = cihaz_tanımlayıcı;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int satıcı_tanımlayıcı() { return satıcı_tanımlayıcı; }
        public int cihaz_tanımlayıcı() { return cihaz_tanımlayıcı; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<cihaz_değer> Cihazlar_Liste = new ArrayList<cihaz_değer>();

    public void 발견(cihaz_değer cihaz_değer) {
        Cihazlar_Liste.add(cihaz_değer);
    }

    public List<cihaz_değer> Cihazlar_Liste() {
        return Collections.unmodifiableList(Cihazlar_Liste);
    }

    public cihaz_değer BUL_girdi(int satıcı_tanımlayıcı, int cihaz_tanımlayıcı) {
        for (cihaz_değer aday : Cihazlar_Liste) {
            if (aday.satıcı_tanımlayıcı == satıcı_tanımlayıcı && aday.cihaz_tanımlayıcı == cihaz_tanımlayıcı) {
                return aday;
            }
        }
        return null;
    }
}

