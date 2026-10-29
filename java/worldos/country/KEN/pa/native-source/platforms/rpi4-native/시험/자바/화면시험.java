// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 화면시험 {
    public static void main(String[] args) {
        ਪੰਜਾਬੀ.자체.화면.사각형(400, 400, 20, 20, 0x123456);
        try { ਪੰਜਾਬੀ.자체.화면.사각형(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("화면 ਕਲਿਪ 거부"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
