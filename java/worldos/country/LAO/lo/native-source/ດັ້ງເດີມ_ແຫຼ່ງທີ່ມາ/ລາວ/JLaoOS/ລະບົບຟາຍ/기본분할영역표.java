// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ລະບົບຟາຍ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ການແບ່ງສ່ວນ_ຄ່າ {
        private final int 종류;
        private final long ເລີ່ມ_ຕອນ;
        private final long 구역수;

        ການແບ່ງສ່ວນ_ຄ່າ(int 종류, long ເລີ່ມ_ຕອນ, long 구역수) {
            this.종류 = 종류;
            this.ເລີ່ມ_ຕອນ = ເລີ່ມ_ຕອນ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ເລີ່ມ_ຕອນ() { return ເລີ່ມ_ຕອນ; }
        public long 구역수() { return 구역수; }
    }

    public List<ການແບ່ງສ່ວນ_ຄ່າ> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ການແບ່ງສ່ວນ_ຄ່າ> ມາດຕະການ = new ArrayList<ການແບ່ງສ່ວນ_ຄ່າ>();
        for (int ດັດຊະນີ = 0; ດັດຊະນີ < 4; ດັດຊະນີ++) {
            int ຈັດຕໍາແຫນ່ງ = 446 + ດັດຊະນີ * 16;
            int 종류 = 첫구역[ຈັດຕໍາແຫນ່ງ + 4] & 0xff;
            long ແລ່ນ = 작은순서정수(첫구역, ຈັດຕໍາແຫນ່ງ + 8);
            long ຂະ_ຫນາດ = 작은순서정수(첫구역, ຈັດຕໍາແຫນ່ງ + 12);
            if (종류 != 0 && ຂະ_ຫນາດ != 0) {
                ມາດຕະການ.add(new ການແບ່ງສ່ວນ_ຄ່າ(종류, ແລ່ນ, ຂະ_ຫນາດ));
            }
        }
        return Collections.unmodifiableList(ມາດຕະການ);
    }

    private long 작은순서정수(byte[] ຂໍ້ມູນ, int ຈັດຕໍາແຫນ່ງ) {
        return (ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ] & 0xffL)
                | ((ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ + 1] & 0xffL) << 8)
                | ((ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ + 2] & 0xffL) << 16)
                | ((ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ + 3] & 0xffL) << 24);
    }
}

