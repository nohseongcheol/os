// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
/** เอง JVM 스케줄러가 관리하는 ดําเนินการ_คําสั่ง สตรีม_ค่า. 표준 Thread를 감싸지 않는다. */
public final class งานเบื้องหลัง {
    public งานเบื้องหลัง(실행할일 งาน_แอคชัน) {
        throw new สถานะ_ข้อยกเว้น("เอง JVM의 ไทย 작업 เธรด_ค่า สร้าง_167eff27 기능이 필요합니다.");
    }
    public native void เริ่ม_งาน() throws เธรด_สถานะ_ข้อยกเว้น;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void หยุดชั่วคราว_งาน();
}
