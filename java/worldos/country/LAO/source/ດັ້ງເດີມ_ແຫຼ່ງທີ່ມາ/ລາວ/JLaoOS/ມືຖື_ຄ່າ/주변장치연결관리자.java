// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ມືຖື_ຄ່າ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ມືຖື_ຄ່າ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class ມືຖື_ຄ່າ {
        private final int ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ;
        private final int ມືຖື_ຕົວ_ກໍາ_ນົດ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ມືຖື_ຄ່າ(int ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ, int ມືຖື_ຕົວ_ກໍາ_ນົດ, int 입출력바탕, int 개입중단번호) {
            this.ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ = ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ;
            this.ມືຖື_ຕົວ_ກໍາ_ນົດ = ມືຖື_ຕົວ_ກໍາ_ນົດ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ() { return ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ; }
        public int ມືຖື_ຕົວ_ກໍາ_ນົດ() { return ມືຖື_ຕົວ_ກໍາ_ນົດ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ມືຖື_ຄ່າ> ອຸປະກອນ_ລາຍຊື່ = new ArrayList<ມືຖື_ຄ່າ>();

    public void 발견(ມືຖື_ຄ່າ ມືຖື_ຄ່າ) {
        ອຸປະກອນ_ລາຍຊື່.add(ມືຖື_ຄ່າ);
    }

    public List<ມືຖື_ຄ່າ> ອຸປະກອນ_ລາຍຊື່() {
        return Collections.unmodifiableList(ອຸປະກອນ_ລາຍຊື່);
    }

    public ມືຖື_ຄ່າ ຊອກຫາ_ເຂົ້າໃນ(int ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ, int ມືຖື_ຕົວ_ກໍາ_ນົດ) {
        for (ມືຖື_ຄ່າ 후보 : ອຸປະກອນ_ລາຍຊື່) {
            if (후보.ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ == ຜູ້_ຂາຍ_ຕົວ_ກໍາ_ນົດ && 후보.ມືຖື_ຕົວ_ກໍາ_ນົດ == ມືຖື_ຕົວ_ກໍາ_ນົດ) {
                return 후보;
            }
        }
        return null;
    }
}

