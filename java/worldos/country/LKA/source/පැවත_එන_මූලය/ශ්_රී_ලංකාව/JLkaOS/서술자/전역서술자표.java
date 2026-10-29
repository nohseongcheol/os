// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 තත්වය_අගය අංශය_අගය 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int පසුබිම_අගය;
        private final int 한계;
        private final int ප්_රවේශය_අගය;

        조각(int පසුබිම_අගය, int 한계, int ප්_රවේශය_අගය) {
            this.පසුබිම_අගය = පසුබිම_අගය;
            this.한계 = 한계;
            this.ප්_රවේශය_අගය = ප්_රවේශය_අගය;
        }

        public int පසුබිම_අගය() { return පසුබිම_අගය; }
        public int 한계() { return 한계; }
        public int ප්_රවේශය_අගය() { return ප්_රවේශය_අගය; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int පසුබිම_අගය, int 한계, int ප්_රවේශය_අගය) {
        조각들.add(new 조각(පසුබිම_අගය, 한계, ප්_රවේශය_අගය));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void කට්ටලය_පෙරනිමි_අගය() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

