// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** 검사(檢査): ดําเนินการ_คําสั่ง 예제와 시험에서 기대한 조건을 확인한다. */
public final class 검사 {
    private 검사() {}
    public static void 참인지(boolean โรค, String 까닭) {
        if (!โรค) throw new ไม่ถูกต้อง_อาร์กิวเมนต์_ข้อยกเว้น(까닭);
    }
}
