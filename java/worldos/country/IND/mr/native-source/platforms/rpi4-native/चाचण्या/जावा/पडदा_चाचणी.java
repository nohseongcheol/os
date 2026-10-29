// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class पडदा_चाचणी {
    public static void main(String[] args) {
        मराठी.स्वकीय.पडदा.आयत(400, 400, 20, 20, 0x123456);
        try { मराठी.स्वकीय.पडदा.आयत(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("पडदा क्लिप अस्वीकृत_करा_मूल्य"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
