// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ລະບົບຟາຍ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class ຕອນ_ຄ່າ {
        private final int 종류;
        private final int ທຸງ_ຄ່າ;
        private final int ອີເມວ;
        private final int ຟາຍ_ຈັດຕໍາແຫນ່ງ;
        private final int ຂະ_ຫນາດ;

        ຕອນ_ຄ່າ(int 종류, int ທຸງ_ຄ່າ, int ອີເມວ, int ຟາຍ_ຈັດຕໍາແຫນ່ງ, int ຂະ_ຫນາດ) {
            this.종류 = 종류;
            this.ທຸງ_ຄ່າ = ທຸງ_ຄ່າ;
            this.ອີເມວ = ອີເມວ;
            this.ຟາຍ_ຈັດຕໍາແຫນ່ງ = ຟາຍ_ຈັດຕໍາແຫນ່ງ;
            this.ຂະ_ຫນາດ = ຂະ_ຫນາດ;
        }

        public int 종류() {
            return 종류;
        }

        public int ທຸງ_ຄ່າ() {
            return ທຸງ_ຄ່າ;
        }

        public int ອີເມວ() {
            return ອີເມວ;
        }

        public int ຟາຍ_ຈັດຕໍາແຫນ່ງ() {
            return ຟາຍ_ຈັດຕໍາແຫນ່ງ;
        }

        public int ຂະ_ຫນາດ() {
            return ຂະ_ຫນາດ;
        }
    }

    public static final class ຮູບ {
        private final int ເລີ່ມ_ອີເມວ;
        private final List<ຕອນ_ຄ່າ> 구역들;

        ຮູບ(int ເລີ່ມ_ອີເມວ, List<ຕອນ_ຄ່າ> 구역들) {
            this.ເລີ່ມ_ອີເມວ = ເລີ່ມ_ອີເມວ;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ເລີ່ມ_ອີເມວ() {
            return ເລີ່ມ_ອີເມວ;
        }

        public List<ຕອນ_ຄ່າ> 구역들() {
            return 구역들;
        }
    }

    public ຮູບ 검사(byte[] ຂໍ້ມູນ) {
        if (ຂໍ້ມູນ == null || ຂໍ້ມູນ.length < 52
                || ຂໍ້ມູນ[0] != 0x7f || ຂໍ້ມູນ[1] != 'E' || ຂໍ້ມູນ[2] != 'L' || ຂໍ້ມູນ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ຂໍ້ມູນ[4] != 1 || ຂໍ້ມູນ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ເລີ່ມ_ອີເມວ = ການແຈກຄໍາສັບ_ຕົວເລກຈໍານວນເຕັມ(ຂໍ້ມູນ, 24);
        int ຕອນ_ຕາຕະລາງ_ຈັດຕໍາແຫນ່ງ = ການແຈກຄໍາສັບ_ຕົວເລກຈໍານວນເຕັມ(ຂໍ້ມູນ, 32);
        int ຕອນ_ເຂົ້າໃນ_ຂະ_ຫນາດ = 짧은정수읽기(ຂໍ້ມູນ, 46);
        int 구역수 = 짧은정수읽기(ຂໍ້ມູນ, 48);
        if (ຕອນ_ເຂົ້າໃນ_ຂະ_ຫນາດ < 40 || ຕອນ_ຕາຕະລາງ_ຈັດຕໍາແຫນ່ງ < 0
                || (long) ຕອນ_ຕາຕະລາງ_ຈັດຕໍາແຫນ່ງ + (long) ຕອນ_ເຂົ້າໃນ_ຂະ_ຫນາດ * 구역수 > ຂໍ້ມູນ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ຕອນ_ຄ່າ> 구역들 = new ArrayList<ຕອນ_ຄ່າ>();
        for (int ດັດຊະນີ = 0; ດັດຊະນີ < 구역수; ດັດຊະນີ++) {
            int ຈັດຕໍາແຫນ່ງ = ຕອນ_ຕາຕະລາງ_ຈັດຕໍາແຫນ່ງ + ດັດຊະນີ * ຕອນ_ເຂົ້າໃນ_ຂະ_ຫນາດ;
            int 종류 = ການແຈກຄໍາສັບ_ຕົວເລກຈໍານວນເຕັມ(ຂໍ້ມູນ, ຈັດຕໍາແຫນ່ງ + 4);
            int ທຸງ_ຄ່າ = ການແຈກຄໍາສັບ_ຕົວເລກຈໍານວນເຕັມ(ຂໍ້ມູນ, ຈັດຕໍາແຫນ່ງ + 8);
            int ອີເມວ = ການແຈກຄໍາສັບ_ຕົວເລກຈໍານວນເຕັມ(ຂໍ້ມູນ, ຈັດຕໍາແຫນ່ງ + 12);
            int ຟາຍ_ຈັດຕໍາແຫນ່ງ = ການແຈກຄໍາສັບ_ຕົວເລກຈໍານວນເຕັມ(ຂໍ້ມູນ, ຈັດຕໍາແຫນ່ງ + 16);
            int ຂະ_ຫນາດ = ການແຈກຄໍາສັບ_ຕົວເລກຈໍານວນເຕັມ(ຂໍ້ມູນ, ຈັດຕໍາແຫນ່ງ + 20);
            if (ຂະ_ຫນາດ < 0 || (종류 != 8 && ((long) ຟາຍ_ຈັດຕໍາແຫນ່ງ + ຂະ_ຫນາດ > ຂໍ້ມູນ.length || ຟາຍ_ຈັດຕໍາແຫນ່ງ < 0))) {
                throw new IllegalArgumentException("ELF ຕອນ_ຄ່າ ຂໍ້ມູນ 범위가 올바르지 않습니다.");
            }
            구역들.add(new ຕອນ_ຄ່າ(종류, ທຸງ_ຄ່າ, ອີເມວ, ຟາຍ_ຈັດຕໍາແຫນ່ງ, ຂະ_ຫນາດ));
        }
        return new ຮູບ(ເລີ່ມ_ອີເມວ, 구역들);
    }

    private int ການແຈກຄໍາສັບ_ຕົວເລກຈໍານວນເຕັມ(byte[] ຂໍ້ມູນ, int ຈັດຕໍາແຫນ່ງ) {
        if (ຈັດຕໍາແຫນ່ງ < 0 || ຈັດຕໍາແຫນ່ງ > ຂໍ້ມູນ.length - 4) {
            throw new IllegalArgumentException("ELF ຕົວເລກຈໍານວນເຕັມ 범위를 벗어났습니다.");
        }
        return (ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ] & 0xff)
                | ((ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ + 1] & 0xff) << 8)
                | ((ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ + 2] & 0xff) << 16)
                | ((ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ຂໍ້ມູນ, int ຈັດຕໍາແຫນ່ງ) {
        if (ຈັດຕໍາແຫນ່ງ < 0 || ຈັດຕໍາແຫນ່ງ > ຂໍ້ມູນ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ຕົວເລກຈໍານວນເຕັມ 범위를 벗어났습니다.");
        }
        return (ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ] & 0xff) | ((ຂໍ້ມູນ[ຈັດຕໍາແຫນ່ງ + 1] & 0xff) << 8);
    }
}
