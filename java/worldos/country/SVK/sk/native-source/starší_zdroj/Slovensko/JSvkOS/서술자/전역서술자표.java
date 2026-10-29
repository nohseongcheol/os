// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Stav_VALUE sekcia_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int tapeta_VALUE;
        private final int 한계;
        private final int prístup_VALUE;

        조각(int tapeta_VALUE, int 한계, int prístup_VALUE) {
            this.tapeta_VALUE = tapeta_VALUE;
            this.한계 = 한계;
            this.prístup_VALUE = prístup_VALUE;
        }

        public int tapeta_VALUE() { return tapeta_VALUE; }
        public int 한계() { return 한계; }
        public int prístup_VALUE() { return prístup_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Pripojiť_položka(int tapeta_VALUE, int 한계, int prístup_VALUE) {
        조각들.add(new 조각(tapeta_VALUE, 한계, prístup_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void množina_predvolená_hodnota() {
        조각들.clear();
        Pripojiť_položka(0, 0, 0);
        Pripojiť_položka(0, 0xfffff, 0x9a);
        Pripojiť_položka(0, 0xfffff, 0x92);
        Pripojiť_položka(0, 0xfffff, 0xfa);
        Pripojiť_položka(0, 0xfffff, 0xf2);
    }
}

