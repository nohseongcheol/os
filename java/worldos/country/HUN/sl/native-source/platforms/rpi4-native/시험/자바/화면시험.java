// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 화면시험 {
    public static void main(String[] args) {
        slovenščina.lastno.화면.pravokotnik(400, 400, 20, 20, 0x123456);
        try { slovenščina.lastno.화면.pravokotnik(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("화면 izrezek zavrniti_VALUE"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
