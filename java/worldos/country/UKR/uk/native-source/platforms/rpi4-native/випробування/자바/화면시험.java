// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 화면시험 {
    public static void main(String[] args) {
        українська.своє.화면.прямокутник(400, 400, 20, 20, 0x123456);
        try { українська.своє.화면.прямокутник(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("화면 кліп відхилити_значення"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
