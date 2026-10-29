// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package افغانستان.JAfgOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 انکړ_ارزښت برخه_ارزښت 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int شاليد_ارزښت;
        private final int 한계;
        private final int رسى_ارزښت;

        조각(int شاليد_ارزښت, int 한계, int رسى_ارزښت) {
            this.شاليد_ارزښت = شاليد_ارزښت;
            this.한계 = 한계;
            this.رسى_ارزښت = رسى_ارزښت;
        }

        public int شاليد_ارزښت() { return شاليد_ارزښت; }
        public int 한계() { return 한계; }
        public int رسى_ارزښت() { return رسى_ارزښت; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int شاليد_ارزښت, int 한계, int رسى_ارزښت) {
        조각들.add(new 조각(شاليد_ارزښت, 한계, رسى_ارزښت));
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

