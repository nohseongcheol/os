// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 status_VERDI inndeling_VERDI 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int bakgrunn_VERDI;
        private final int 한계;
        private final int tilgang_VERDI;

        조각(int bakgrunn_VERDI, int 한계, int tilgang_VERDI) {
            this.bakgrunn_VERDI = bakgrunn_VERDI;
            this.한계 = 한계;
            this.tilgang_VERDI = tilgang_VERDI;
        }

        public int bakgrunn_VERDI() { return bakgrunn_VERDI; }
        public int 한계() { return 한계; }
        public int tilgang_VERDI() { return tilgang_VERDI; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Tilføye_oppføring(int bakgrunn_VERDI, int 한계, int tilgang_VERDI) {
        조각들.add(new 조각(bakgrunn_VERDI, 한계, tilgang_VERDI));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void sett_standardverdi() {
        조각들.clear();
        Tilføye_oppføring(0, 0, 0);
        Tilføye_oppføring(0, 0xfffff, 0x9a);
        Tilføye_oppføring(0, 0xfffff, 0x92);
        Tilføye_oppføring(0, 0xfffff, 0xfa);
        Tilføye_oppføring(0, 0xfffff, 0xf2);
    }
}

