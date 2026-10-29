// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 화면시험 {
    public static void main(String[] args) {
        हिंदी.निज.화면.रेक्_टेंगल(400, 400, 20, 20, 0x123456);
        try { हिंदी.निज.화면.रेक्_टेंगल(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("화면 क्लिप अस्वीकृत_करें_मान"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
