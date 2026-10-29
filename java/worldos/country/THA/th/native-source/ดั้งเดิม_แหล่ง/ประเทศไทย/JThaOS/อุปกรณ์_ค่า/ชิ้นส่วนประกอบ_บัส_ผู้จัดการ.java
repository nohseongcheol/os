// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.อุปกรณ์_ค่า;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI อุปกรณ์_ค่า 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ชิ้นส่วนประกอบ_บัส_ผู้จัดการ {
    public static final class อุปกรณ์_ค่า {
        private final int ผู้ขาย_ตัวระบุ;
        private final int อุปกรณ์_ตัวระบุ;
        private final int 입출력바탕;
        private final int สัญญาณขัดจังหวะ_หมายเลข;

        public อุปกรณ์_ค่า(int ผู้ขาย_ตัวระบุ, int อุปกรณ์_ตัวระบุ, int 입출력바탕, int สัญญาณขัดจังหวะ_หมายเลข) {
            this.ผู้ขาย_ตัวระบุ = ผู้ขาย_ตัวระบุ;
            this.อุปกรณ์_ตัวระบุ = อุปกรณ์_ตัวระบุ;
            this.입출력바탕 = 입출력바탕;
            this.สัญญาณขัดจังหวะ_หมายเลข = สัญญาณขัดจังหวะ_หมายเลข;
        }

        public int ผู้ขาย_ตัวระบุ() { return ผู้ขาย_ตัวระบุ; }
        public int อุปกรณ์_ตัวระบุ() { return อุปกรณ์_ตัวระบุ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int สัญญาณขัดจังหวะ_หมายเลข() { return สัญญาณขัดจังหวะ_หมายเลข; }
    }

    private final List<อุปกรณ์_ค่า> อุปกรณ์_รายการ = new ArrayList<อุปกรณ์_ค่า>();

    public void 발견(อุปกรณ์_ค่า อุปกรณ์_ค่า) {
        อุปกรณ์_รายการ.add(อุปกรณ์_ค่า);
    }

    public List<อุปกรณ์_ค่า> อุปกรณ์_รายการ() {
        return Collections.unmodifiableList(อุปกรณ์_รายการ);
    }

    public อุปกรณ์_ค่า ค้นพบ_รายการ(int ผู้ขาย_ตัวระบุ, int อุปกรณ์_ตัวระบุ) {
        for (อุปกรณ์_ค่า 후보 : อุปกรณ์_รายการ) {
            if (후보.ผู้ขาย_ตัวระบุ == ผู้ขาย_ตัวระบุ && 후보.อุปกรณ์_ตัวระบุ == อุปกรณ์_ตัวระบุ) {
                return 후보;
            }
        }
        return null;
    }
}

