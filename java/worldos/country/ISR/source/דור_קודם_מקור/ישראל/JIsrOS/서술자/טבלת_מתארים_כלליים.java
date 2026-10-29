// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 מצב_ערך מקטע_ערך 설정값을 보관한다. */
public final class טבלת_מתארים_כלליים {
    public static final class 조각 {
        private final int טפט_ערך;
        private final int 한계;
        private final int גישה_ערך;

        조각(int טפט_ערך, int 한계, int גישה_ערך) {
            this.טפט_ערך = טפט_ערך;
            this.한계 = 한계;
            this.גישה_ערך = גישה_ערך;
        }

        public int טפט_ערך() { return טפט_ערך; }
        public int 한계() { return 한계; }
        public int גישה_ערך() { return גישה_ערך; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int צירוף_ערך_b73accca(int טפט_ערך, int 한계, int גישה_ערך) {
        조각들.add(new 조각(טפט_ערך, 한계, גישה_ערך));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ערכה_ערך_ברירת_מחדל() {
        조각들.clear();
        צירוף_ערך_b73accca(0, 0, 0);
        צירוף_ערך_b73accca(0, 0xfffff, 0x9a);
        צירוף_ערך_b73accca(0, 0xfffff, 0x92);
        צירוף_ערך_b73accca(0, 0xfffff, 0xfa);
        צירוף_ערך_b73accca(0, 0xfffff, 0xf2);
    }
}

