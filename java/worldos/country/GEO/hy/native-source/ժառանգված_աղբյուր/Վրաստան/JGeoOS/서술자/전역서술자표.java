// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Վրաստան.JGeoOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 վիճակ_արժեք խումբ_արժեք_366e0bfa 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int խորք_արժեք;
        private final int 한계;
        private final int մատչել_արժեք;

        조각(int խորք_արժեք, int 한계, int մատչել_արժեք) {
            this.խորք_արժեք = խորք_արժեք;
            this.한계 = 한계;
            this.մատչել_արժեք = մատչել_արժեք;
        }

        public int խորք_արժեք() { return խորք_արժեք; }
        public int 한계() { return 한계; }
        public int մատչել_արժեք() { return մատչել_արժեք; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int խորք_արժեք, int 한계, int մատչել_արժեք) {
        조각들.add(new 조각(խորք_արժեք, 한계, մատչել_արժեք));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void կազմ_սկզբնադիր_արժեք() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

