// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 화면시험 {
    public static void main(String[] args) {
        ไทย.เอง.화면.สี่เหลี่ยมผืนผ้า(400, 400, 20, 20, 0x123456);
        try { ไทย.เอง.화면.สี่เหลี่ยมผืนผ้า(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("화면 คลิป ปฏิเสธ_ค่า"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
