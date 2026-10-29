// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Msumbiji.JMozOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 hali_thamani sehemu_thamani 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int nyuma_thamani;
        private final int 한계;
        private final int fikia_thamani;

        조각(int nyuma_thamani, int 한계, int fikia_thamani) {
            this.nyuma_thamani = nyuma_thamani;
            this.한계 = 한계;
            this.fikia_thamani = fikia_thamani;
        }

        public int nyuma_thamani() { return nyuma_thamani; }
        public int 한계() { return 한계; }
        public int fikia_thamani() { return fikia_thamani; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int nyuma_thamani, int 한계, int fikia_thamani) {
        조각들.add(new 조각(nyuma_thamani, 한계, fikia_thamani));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void seti_hali_ya_chaguo_msingi() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

