// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijeer.JNerOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ngonka_njaru taƴre_njaru 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int cakkital_njaru;
        private final int 한계;
        private final int naatde_njaru;

        조각(int cakkital_njaru, int 한계, int naatde_njaru) {
            this.cakkital_njaru = cakkital_njaru;
            this.한계 = 한계;
            this.naatde_njaru = naatde_njaru;
        }

        public int cakkital_njaru() { return cakkital_njaru; }
        public int 한계() { return 한계; }
        public int naatde_njaru() { return naatde_njaru; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int cakkital_njaru, int 한계, int naatde_njaru) {
        조각들.add(new 조각(cakkital_njaru, 한계, naatde_njaru));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void 기본값설정() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

