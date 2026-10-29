// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
/** 작업 เธรด_ค่า: 하나의 ดําเนินการ_คําสั่ง สตรีม_ค่า. เอง JVM 안에서 คําสั่ง 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static งานเบื้องหลัง เรียกใช้งาน(실행할일 งาน_แอคชัน) { งานเบื้องหลัง เธรด_ค่า = new งานเบื้องหลัง(งาน_แอคชัน); เธรด_ค่า.เริ่ม_งาน(); return เธรด_ค่า; }
    public static void 기다리기(งานเบื้องหลัง เธรด_ค่า) throws 대기중단예외 { เธรด_ค่า.기다리기(); }
    public static boolean 살아있는가(งานเบื้องหลัง เธรด_ค่า) { return เธรด_ค่า.살아있는가(); }
    public static void หยุดชั่วคราว_งาน() { งานเบื้องหลัง.หยุดชั่วคราว_งาน(); }
}
