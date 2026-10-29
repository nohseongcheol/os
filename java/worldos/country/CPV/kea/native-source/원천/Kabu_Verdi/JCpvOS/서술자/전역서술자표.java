// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kabu_Verdi.JCpvOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 상태 구역 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int 바탕;
        private final int 한계;
        private final int 접근값;

        조각(int 바탕, int 한계, int 접근값) {
            this.바탕 = 바탕;
            this.한계 = 한계;
            this.접근값 = 접근값;
        }

        public int 바탕() { return 바탕; }
        public int 한계() { return 한계; }
        public int 접근값() { return 접근값; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int 바탕, int 한계, int 접근값) {
        조각들.add(new 조각(바탕, 한계, 접근값));
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

