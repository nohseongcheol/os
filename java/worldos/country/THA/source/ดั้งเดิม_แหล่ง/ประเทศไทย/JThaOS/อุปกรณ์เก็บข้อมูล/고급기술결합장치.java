// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.อุปกรณ์เก็บข้อมูล;

import java.util.Arrays;

/** ATA 28비트 คําสั่ง 계층과 같은 512바이트 논리 ส่วน_ค่า 장치다. */
public final class 고급기술결합장치 {
    public static final int ส่วน_ขนาด = 512;
    private final byte[] ข้อมูล;
    private final boolean อ่านอย่างเดียว_ค่า;

    public 고급기술결합장치(int 구역수, boolean อ่านอย่างเดียว_ค่า) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ส่วน_ค่า 수가 올바르지 않습니다.");
        }
        ข้อมูล = new byte[Math.multiplyExact(구역수, ส่วน_ขนาด)];
        this.อ่านอย่างเดียว_ค่า = อ่านอย่างเดียว_ค่า;
    }

    public int 구역수() {
        return ข้อมูล.length / ส่วน_ขนาด;
    }

    public void อ่าน(int ส่วน_ดัชนี, byte[] รับ_ปลายทาง) {
        เช็ค_ช่วง(ส่วน_ดัชนี, รับ_ปลายทาง);
        System.arraycopy(ข้อมูล, ส่วน_ดัชนี * ส่วน_ขนาด, รับ_ปลายทาง, 0, ส่วน_ขนาด);
    }

    public void เขียน(int ส่วน_ดัชนี, byte[] 쓸자료) {
        if (อ่านอย่างเดียว_ค่า) {
            throw new IllegalStateException("อ่าน 전용 장치입니다.");
        }
        เช็ค_ช่วง(ส่วน_ดัชนี, 쓸자료);
        System.arraycopy(쓸자료, 0, ข้อมูล, ส่วน_ดัชนี * ส่วน_ขนาด, ส่วน_ขนาด);
    }

    public void ลบ_รายการ() {
        if (อ่านอย่างเดียว_ค่า) {
            throw new IllegalStateException("อ่าน 전용 장치입니다.");
        }
        Arrays.fill(ข้อมูล, (byte) 0);
    }

    private void เช็ค_ช่วง(int ส่วน_ดัชนี, byte[] 임시공간) {
        if (ส่วน_ดัชนี < 0 || ส่วน_ดัชนี >= 구역수() || 임시공간.length < ส่วน_ขนาด) {
            throw new IllegalArgumentException("ATA ส่วน_ค่า 범위가 올바르지 않습니다.");
        }
    }
}

