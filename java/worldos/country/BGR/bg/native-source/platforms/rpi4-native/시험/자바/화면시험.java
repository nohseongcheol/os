// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 화면시험 {
    public static void main(String[] args) {
        Български.자체.화면.правоъгълник(400, 400, 20, 20, 0x123456);
        try { Български.자체.화면.правоъгълник(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("화면 клип отхвърлям_стойност_e3ecc00b"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
