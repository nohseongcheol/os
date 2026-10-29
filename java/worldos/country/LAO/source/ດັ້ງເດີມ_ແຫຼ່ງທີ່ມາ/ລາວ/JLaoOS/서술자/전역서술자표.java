// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ສະຖານະ_ຄ່າ ຕອນ_ຄ່າ 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ພື້ນຫຼັງ_ຄ່າ;
        private final int 한계;
        private final int ເຂົ້າຫາ_ຄ່າ;

        조각(int ພື້ນຫຼັງ_ຄ່າ, int 한계, int ເຂົ້າຫາ_ຄ່າ) {
            this.ພື້ນຫຼັງ_ຄ່າ = ພື້ນຫຼັງ_ຄ່າ;
            this.한계 = 한계;
            this.ເຂົ້າຫາ_ຄ່າ = ເຂົ້າຫາ_ຄ່າ;
        }

        public int ພື້ນຫຼັງ_ຄ່າ() { return ພື້ນຫຼັງ_ຄ່າ; }
        public int 한계() { return 한계; }
        public int ເຂົ້າຫາ_ຄ່າ() { return ເຂົ້າຫາ_ຄ່າ; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ພື້ນຫຼັງ_ຄ່າ, int 한계, int ເຂົ້າຫາ_ຄ່າ) {
        조각들.add(new 조각(ພື້ນຫຼັງ_ຄ່າ, 한계, ເຂົ້າຫາ_ຄ່າ));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ຊຸດ_ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

