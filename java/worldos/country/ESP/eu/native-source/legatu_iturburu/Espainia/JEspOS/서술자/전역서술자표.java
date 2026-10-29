// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Egoera_balio sekzio_balio 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int horma_paper_balio;
        private final int 한계;
        private final int atzitu_balio;

        조각(int horma_paper_balio, int 한계, int atzitu_balio) {
            this.horma_paper_balio = horma_paper_balio;
            this.한계 = 한계;
            this.atzitu_balio = atzitu_balio;
        }

        public int horma_paper_balio() { return horma_paper_balio; }
        public int 한계() { return 한계; }
        public int atzitu_balio() { return atzitu_balio; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Erantsi_sarrera(int horma_paper_balio, int 한계, int atzitu_balio) {
        조각들.add(new 조각(horma_paper_balio, 한계, atzitu_balio));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void sorta_balio_lehenetsi() {
        조각들.clear();
        Erantsi_sarrera(0, 0, 0);
        Erantsi_sarrera(0, 0xfffff, 0x9a);
        Erantsi_sarrera(0, 0xfffff, 0x92);
        Erantsi_sarrera(0, 0xfffff, 0xfa);
        Erantsi_sarrera(0, 0xfffff, 0xf2);
    }
}

