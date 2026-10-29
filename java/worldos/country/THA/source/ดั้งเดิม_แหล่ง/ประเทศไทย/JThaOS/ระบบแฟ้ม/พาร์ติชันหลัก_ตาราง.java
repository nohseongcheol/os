// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.ระบบแฟ้ม;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ค่าเริ่มต้น 분할 영역을 읽는다. */
public final class พาร์ติชันหลัก_ตาราง {
    public static final class พาร์ติชัน_ค่า {
        private final int 종류;
        private final long เริ่ม_ส่วน;
        private final long 구역수;

        พาร์ติชัน_ค่า(int 종류, long เริ่ม_ส่วน, long 구역수) {
            this.종류 = 종류;
            this.เริ่ม_ส่วน = เริ่ม_ส่วน;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long เริ่ม_ส่วน() { return เริ่ม_ส่วน; }
        public long 구역수() { return 구역수; }
    }

    public List<พาร์ติชัน_ค่า> อ่าน(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<พาร์ติชัน_ค่า> ผลลัพธ์ = new ArrayList<พาร์ติชัน_ค่า>();
        for (int ดัชนี = 0; ดัชนี < 4; ดัชนี++) {
            int ตําแหน่ง = 446 + ดัชนี * 16;
            int 종류 = 첫구역[ตําแหน่ง + 4] & 0xff;
            long เรียกใช้งาน = 작은순서정수(첫구역, ตําแหน่ง + 8);
            long ขนาด = 작은순서정수(첫구역, ตําแหน่ง + 12);
            if (종류 != 0 && ขนาด != 0) {
                ผลลัพธ์.add(new พาร์ติชัน_ค่า(종류, เรียกใช้งาน, ขนาด));
            }
        }
        return Collections.unmodifiableList(ผลลัพธ์);
    }

    private long 작은순서정수(byte[] ข้อมูล, int ตําแหน่ง) {
        return (ข้อมูล[ตําแหน่ง] & 0xffL)
                | ((ข้อมูล[ตําแหน่ง + 1] & 0xffL) << 8)
                | ((ข้อมูล[ตําแหน่ง + 2] & 0xffL) << 16)
                | ((ข้อมูล[ตําแหน่ง + 3] & 0xffL) << 24);
    }
}

