// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
/** เอง JVM과 커널의 หน้าต่าง 관리 기능에 직접 연결되는 หน้าต่าง. */
public final class หน้าต่าง extends 화면구성요소 {
    public หน้าต่าง(String หน้าต่าง_กรรมสิทธิ์, int 폭, int 높이) {
        throw new สถานะ_ข้อยกเว้น("เอง JVM의 ไทย หน้าต่าง สร้าง_167eff27 기능이 필요합니다.");
    }
    public native void เพิ่ม_องค์ประกอบ(화면구성요소 องค์ประกอบ_ค่า);
    public native void แสดง_หน้าต่าง();
    public native void ปิด();
    public native boolean 보이는가();
}
