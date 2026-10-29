// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.popisovač_položka;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Stav_HODNOTA oddíl_HODNOTA_366e0bfa 설정값을 보관한다. */
public final class Globální_popisovač_tabulka {
    public static final class 조각 {
        private final int Pozadí_HODNOTA;
        private final int 한계;
        private final int přístup_HODNOTA;

        조각(int Pozadí_HODNOTA, int 한계, int přístup_HODNOTA) {
            this.Pozadí_HODNOTA = Pozadí_HODNOTA;
            this.한계 = 한계;
            this.přístup_HODNOTA = přístup_HODNOTA;
        }

        public int Pozadí_HODNOTA() { return Pozadí_HODNOTA; }
        public int 한계() { return 한계; }
        public int přístup_HODNOTA() { return přístup_HODNOTA; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Připojit_položka(int Pozadí_HODNOTA, int 한계, int přístup_HODNOTA) {
        조각들.add(new 조각(Pozadí_HODNOTA, 한계, přístup_HODNOTA));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void sada_výchozí_hodnota() {
        조각들.clear();
        Připojit_položka(0, 0, 0);
        Připojit_položka(0, 0xfffff, 0x9a);
        Připojit_položka(0, 0xfffff, 0x92);
        Připojit_položka(0, 0xfffff, 0xfa);
        Připojit_položka(0, 0xfffff, 0xf2);
    }
}

