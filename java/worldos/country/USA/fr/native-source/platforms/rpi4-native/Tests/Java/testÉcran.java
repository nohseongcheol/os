// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class testÉcran {
    public static void main(String[] args) {
        français.interne.Écran.rectangle(400, 400, 20, 20, 0x123456);
        try { français.interne.Écran.rectangle(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("Écran rogner rejeterValeur"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
