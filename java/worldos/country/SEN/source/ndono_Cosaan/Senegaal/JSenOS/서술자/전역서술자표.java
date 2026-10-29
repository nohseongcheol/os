// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 nekkin_xëyma dog_xëyma 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Njiitlay_xëyma;
        private final int 한계;
        private final int jot_xëyma;

        조각(int Njiitlay_xëyma, int 한계, int jot_xëyma) {
            this.Njiitlay_xëyma = Njiitlay_xëyma;
            this.한계 = 한계;
            this.jot_xëyma = jot_xëyma;
        }

        public int Njiitlay_xëyma() { return Njiitlay_xëyma; }
        public int 한계() { return 한계; }
        public int jot_xëyma() { return jot_xëyma; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Njiitlay_xëyma, int 한계, int jot_xëyma) {
        조각들.add(new 조각(Njiitlay_xëyma, 한계, jot_xëyma));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void Boole_gi_xayma_bi_teew() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

