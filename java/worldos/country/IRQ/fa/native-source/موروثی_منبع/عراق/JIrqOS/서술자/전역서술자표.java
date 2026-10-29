// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عراق.JIrqOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 وضعیت_مقدار قسمت_مقدار 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int زمینه_مقدار_0764f371;
        private final int 한계;
        private final int دسترسی_مقدار;

        조각(int زمینه_مقدار_0764f371, int 한계, int دسترسی_مقدار) {
            this.زمینه_مقدار_0764f371 = زمینه_مقدار_0764f371;
            this.한계 = 한계;
            this.دسترسی_مقدار = دسترسی_مقدار;
        }

        public int زمینه_مقدار_0764f371() { return زمینه_مقدار_0764f371; }
        public int 한계() { return 한계; }
        public int دسترسی_مقدار() { return دسترسی_مقدار; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int زمینه_مقدار_0764f371, int 한계, int دسترسی_مقدار) {
        조각들.add(new 조각(زمینه_مقدار_0764f371, 한계, دسترسی_مقدار));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void مجموعه_مقدار_پیش_فرض() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

