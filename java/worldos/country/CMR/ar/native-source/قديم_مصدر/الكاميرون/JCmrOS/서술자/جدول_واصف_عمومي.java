// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package الكاميرون.JCmrOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 حالة_قيمة قسم_قيمة_366e0bfa 설정값을 보관한다. */
public final class جدول_واصف_عمومي {
    public static final class 조각 {
        private final int خلفية_قيمة;
        private final int 한계;
        private final int يصل_قيمة;

        조각(int خلفية_قيمة, int 한계, int يصل_قيمة) {
            this.خلفية_قيمة = خلفية_قيمة;
            this.한계 = 한계;
            this.يصل_قيمة = يصل_قيمة;
        }

        public int خلفية_قيمة() { return خلفية_قيمة; }
        public int 한계() { return 한계; }
        public int يصل_قيمة() { return يصل_قيمة; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int إلحاق_إدخال(int خلفية_قيمة, int 한계, int يصل_قيمة) {
        조각들.add(new 조각(خلفية_قيمة, 한계, يصل_قيمة));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void مجموعة_قيمة_افتراضية() {
        조각들.clear();
        إلحاق_إدخال(0, 0, 0);
        إلحاق_إدخال(0, 0xfffff, 0x9a);
        إلحاق_إدخال(0, 0xfffff, 0x92);
        إلحاق_إدخال(0, 0xfffff, 0xfa);
        إلحاق_إدخال(0, 0xfffff, 0xf2);
    }
}

