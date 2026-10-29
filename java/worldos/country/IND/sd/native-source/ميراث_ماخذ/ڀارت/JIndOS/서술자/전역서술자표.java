// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ڀارت.JIndOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 حالت_قدر سيڪشن_قدر 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int پس_منظر_قدر;
        private final int 한계;
        private final int پهچ_قدر;

        조각(int پس_منظر_قدر, int 한계, int پهچ_قدر) {
            this.پس_منظر_قدر = پس_منظر_قدر;
            this.한계 = 한계;
            this.پهچ_قدر = پهچ_قدر;
        }

        public int پس_منظر_قدر() { return پس_منظر_قدر; }
        public int 한계() { return 한계; }
        public int پهچ_قدر() { return پهچ_قدر; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int پس_منظر_قدر, int 한계, int پهچ_قدر) {
        조각들.add(new 조각(پس_منظر_قدر, 한계, پهچ_قدر));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void سيٽ_طئي_ٿيل_ملهه() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

