// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sverige.JSweOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 status_värde avsnitt_värde 설정값을 보관한다. */
public final class GDT {
    public static final class 조각 {
        private final int Bakgrund_värde;
        private final int 한계;
        private final int ansluta_värde;

        조각(int Bakgrund_värde, int 한계, int ansluta_värde) {
            this.Bakgrund_värde = Bakgrund_värde;
            this.한계 = 한계;
            this.ansluta_värde = ansluta_värde;
        }

        public int Bakgrund_värde() { return Bakgrund_värde; }
        public int 한계() { return 한계; }
        public int ansluta_värde() { return ansluta_värde; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Lägga_till_post(int Bakgrund_värde, int 한계, int ansluta_värde) {
        조각들.add(new 조각(Bakgrund_värde, 한계, ansluta_värde));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void uppsättning_standardvärde() {
        조각들.clear();
        Lägga_till_post(0, 0, 0);
        Lägga_till_post(0, 0xfffff, 0x9a);
        Lägga_till_post(0, 0xfffff, 0x92);
        Lägga_till_post(0, 0xfffff, 0xfa);
        Lägga_till_post(0, 0xfffff, 0xf2);
    }
}

