// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
/** ไทย 화면 구성요소를 만드는 편의 ฟังก์ชัน_ค่า. */
public final class วิดเจ็ต {
    private วิดเจ็ต() {}
    public static void 나중에실행(실행할일 งาน_แอคชัน) { กิจกรรม_คิว.나중에실행(งาน_แอคชัน); }
    public static ฉลาก ป้าย_ค่า(String ข้อความ, int 가로, int แนวตั้ง_ตําแหน่ง, int 폭, int 높이) {
        return new ฉลาก(ข้อความ, 가로, แนวตั้ง_ตําแหน่ง, 폭, 높이);
    }
    public static ปุ่ม ปุ่ม(String ข้อความ, int 가로, int แนวตั้ง_ตําแหน่ง, int 폭, int 높이, 동작받이 받이) {
        return new ปุ่ม(ข้อความ, 가로, แนวตั้ง_ตําแหน่ง, 폭, 높이, 받이);
    }
    public static เขตข้อมูลข้อความ เขตข้อมูลข้อความ(String ข้อความ, int 가로, int แนวตั้ง_ตําแหน่ง, int 폭, int 높이) {
        return new เขตข้อมูลข้อความ(ข้อความ, 가로, แนวตั้ง_ตําแหน่ง, 폭, 높이);
    }
}
