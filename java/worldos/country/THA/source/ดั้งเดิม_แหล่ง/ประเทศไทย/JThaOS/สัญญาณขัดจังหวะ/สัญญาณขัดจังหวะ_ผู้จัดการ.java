// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ประเทศไทย.JThaOS.สัญญาณขัดจังหวะ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class สัญญาณขัดจังหวะ_ผู้จัดการ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ว่าง;

    public void ทะเบียน_รายการ(int ดัชนี, 개입중단처리기 처리기) {
        ยืนยัน_หมายเลข(ดัชนี);
        처리기들[ดัชนี] = 처리기;
    }

    public void ปล่อย_ที่เก็บ(int ดัชนี) {
        ยืนยัน_หมายเลข(ดัชนี);
        처리기들[ดัชนี] = null;
    }

    public int กระจาย_ค่า(int ดัชนี, int 저장된쌓임주소) {
        ยืนยัน_หมายเลข(ดัชนี);
        if (!ว่าง) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ดัชนี];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.กระบวนการ_ค่า_รายการ(저장된쌓임주소);
    }

    public void เปิดใช้งาน() {
        ว่าง = true;
    }

    public void ปิดใช้งาน() {
        ว่าง = false;
    }

    public boolean เทคโนโลยีสารสนเทศ_ว่าง() {
        return ว่าง;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void ยืนยัน_หมายเลข(int ดัชนี) {
        if (ดัชนี < 0 || ดัชนี >= 처리기들.length) {
            throw new IllegalArgumentException("สัญญาณขัดจังหวะ 번호가 올바르지 않습니다.");
        }
    }
}

