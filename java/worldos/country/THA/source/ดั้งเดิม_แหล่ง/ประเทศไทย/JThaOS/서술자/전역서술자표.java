// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 สถานะ_ค่า ส่วน_ค่า 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int พื้นหลัง_ค่า;
        private final int 한계;
        private final int เข้าถึง_ค่า;

        조각(int พื้นหลัง_ค่า, int 한계, int เข้าถึง_ค่า) {
            this.พื้นหลัง_ค่า = พื้นหลัง_ค่า;
            this.한계 = 한계;
            this.เข้าถึง_ค่า = เข้าถึง_ค่า;
        }

        public int พื้นหลัง_ค่า() { return พื้นหลัง_ค่า; }
        public int 한계() { return 한계; }
        public int เข้าถึง_ค่า() { return เข้าถึง_ค่า; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int ผนวก_รายการ(int พื้นหลัง_ค่า, int 한계, int เข้าถึง_ค่า) {
        조각들.add(new 조각(พื้นหลัง_ค่า, 한계, เข้าถึง_ค่า));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ชุด_ค่าเริ่มต้น() {
        조각들.clear();
        ผนวก_รายการ(0, 0, 0);
        ผนวก_รายการ(0, 0xfffff, 0x9a);
        ผนวก_รายการ(0, 0xfffff, 0x92);
        ผนวก_รายการ(0, 0xfffff, 0xfa);
        ผนวก_รายการ(0, 0xfffff, 0xf2);
    }
}

