// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.ระบบแฟ้ม;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ดําเนินการ_คําสั่ง 파일의 머리부와 적재 구역을 검증한다. */
public final class แฟ้มปฏิบัติการ_ตัวโหลด {
    public static final class ส่วน_ค่า {
        private final int 종류;
        private final int ค่าสถานะ_ค่า;
        private final int อีเมล;
        private final int แฟ้ม_ตําแหน่ง;
        private final int ขนาด;

        ส่วน_ค่า(int 종류, int ค่าสถานะ_ค่า, int อีเมล, int แฟ้ม_ตําแหน่ง, int ขนาด) {
            this.종류 = 종류;
            this.ค่าสถานะ_ค่า = ค่าสถานะ_ค่า;
            this.อีเมล = อีเมล;
            this.แฟ้ม_ตําแหน่ง = แฟ้ม_ตําแหน่ง;
            this.ขนาด = ขนาด;
        }

        public int 종류() {
            return 종류;
        }

        public int ค่าสถานะ_ค่า() {
            return ค่าสถานะ_ค่า;
        }

        public int อีเมล() {
            return อีเมล;
        }

        public int แฟ้ม_ตําแหน่ง() {
            return แฟ้ม_ตําแหน่ง;
        }

        public int ขนาด() {
            return ขนาด;
        }
    }

    public static final class รูป {
        private final int เริ่ม_อีเมล;
        private final List<ส่วน_ค่า> 구역들;

        รูป(int เริ่ม_อีเมล, List<ส่วน_ค่า> 구역들) {
            this.เริ่ม_อีเมล = เริ่ม_อีเมล;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int เริ่ม_อีเมล() {
            return เริ่ม_อีเมล;
        }

        public List<ส่วน_ค่า> 구역들() {
            return 구역들;
        }
    }

    public รูป 검사(byte[] ข้อมูล) {
        if (ข้อมูล == null || ข้อมูล.length < 52
                || ข้อมูล[0] != 0x7f || ข้อมูล[1] != 'E' || ข้อมูล[2] != 'L' || ข้อมูล[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ข้อมูล[4] != 1 || ข้อมูล[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int เริ่ม_อีเมล = แยกวิเคราะห์_จํานวนเต็ม(ข้อมูล, 24);
        int ส่วน_ตาราง_ตําแหน่ง = แยกวิเคราะห์_จํานวนเต็ม(ข้อมูล, 32);
        int ส่วน_รายการ_ขนาด = 짧은정수읽기(ข้อมูล, 46);
        int 구역수 = 짧은정수읽기(ข้อมูล, 48);
        if (ส่วน_รายการ_ขนาด < 40 || ส่วน_ตาราง_ตําแหน่ง < 0
                || (long) ส่วน_ตาราง_ตําแหน่ง + (long) ส่วน_รายการ_ขนาด * 구역수 > ข้อมูล.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ส่วน_ค่า> 구역들 = new ArrayList<ส่วน_ค่า>();
        for (int ดัชนี = 0; ดัชนี < 구역수; ดัชนี++) {
            int ตําแหน่ง = ส่วน_ตาราง_ตําแหน่ง + ดัชนี * ส่วน_รายการ_ขนาด;
            int 종류 = แยกวิเคราะห์_จํานวนเต็ม(ข้อมูล, ตําแหน่ง + 4);
            int ค่าสถานะ_ค่า = แยกวิเคราะห์_จํานวนเต็ม(ข้อมูล, ตําแหน่ง + 8);
            int อีเมล = แยกวิเคราะห์_จํานวนเต็ม(ข้อมูล, ตําแหน่ง + 12);
            int แฟ้ม_ตําแหน่ง = แยกวิเคราะห์_จํานวนเต็ม(ข้อมูล, ตําแหน่ง + 16);
            int ขนาด = แยกวิเคราะห์_จํานวนเต็ม(ข้อมูล, ตําแหน่ง + 20);
            if (ขนาด < 0 || (종류 != 8 && ((long) แฟ้ม_ตําแหน่ง + ขนาด > ข้อมูล.length || แฟ้ม_ตําแหน่ง < 0))) {
                throw new IllegalArgumentException("ELF ส่วน_ค่า ข้อมูล 범위가 올바르지 않습니다.");
            }
            구역들.add(new ส่วน_ค่า(종류, ค่าสถานะ_ค่า, อีเมล, แฟ้ม_ตําแหน่ง, ขนาด));
        }
        return new รูป(เริ่ม_อีเมล, 구역들);
    }

    private int แยกวิเคราะห์_จํานวนเต็ม(byte[] ข้อมูล, int ตําแหน่ง) {
        if (ตําแหน่ง < 0 || ตําแหน่ง > ข้อมูล.length - 4) {
            throw new IllegalArgumentException("ELF จํานวนเต็ม 범위를 벗어났습니다.");
        }
        return (ข้อมูล[ตําแหน่ง] & 0xff)
                | ((ข้อมูล[ตําแหน่ง + 1] & 0xff) << 8)
                | ((ข้อมูล[ตําแหน่ง + 2] & 0xff) << 16)
                | ((ข้อมูล[ตําแหน่ง + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ข้อมูล, int ตําแหน่ง) {
        if (ตําแหน่ง < 0 || ตําแหน่ง > ข้อมูล.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 จํานวนเต็ม 범위를 벗어났습니다.");
        }
        return (ข้อมูล[ตําแหน่ง] & 0xff) | ((ข้อมูล[ตําแหน่ง + 1] & 0xff) << 8);
    }
}
