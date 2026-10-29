// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.tanımlayıcı_girdi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Durum_değer bölüm_değer_366e0bfa 설정값을 보관한다. */
public final class GDT {
    public static final class parça_değer {
        private final int Arka_Plan_değer;
        private final int 한계;
        private final int erişim_değer;

        parça_değer(int Arka_Plan_değer, int 한계, int erişim_değer) {
            this.Arka_Plan_değer = Arka_Plan_değer;
            this.한계 = 한계;
            this.erişim_değer = erişim_değer;
        }

        public int Arka_Plan_değer() { return Arka_Plan_değer; }
        public int 한계() { return 한계; }
        public int erişim_değer() { return erişim_değer; }
    }

    private final List<parça_değer> 조각들 = new ArrayList<parça_değer>();

    public int Ekleme_girdi(int Arka_Plan_değer, int 한계, int erişim_değer) {
        조각들.add(new parça_değer(Arka_Plan_değer, 한계, erişim_değer));
        return (조각들.size() - 1) * 8;
    }

    public List<parça_değer> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void küme_varsayılan_değer() {
        조각들.clear();
        Ekleme_girdi(0, 0, 0);
        Ekleme_girdi(0, 0xfffff, 0x9a);
        Ekleme_girdi(0, 0xfffff, 0x92);
        Ekleme_girdi(0, 0xfffff, 0xfa);
        Ekleme_girdi(0, 0xfffff, 0xf2);
    }
}

