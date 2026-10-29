// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class тест_экран {
    public static void main(String[] args) {
        русский.свой.экран.прямоугольник(400, 400, 20, 20, 0x123456);
        try { русский.свой.экран.прямоугольник(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("экран клип отклонить_ЗНАЧЕН"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
