// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class bildschirmPrüfung {
    public static void main(String[] args) {
        Deutsch.eigen.Bildschirm.rechteck(400, 400, 20, 20, 0x123456);
        try { Deutsch.eigen.Bildschirm.rechteck(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("Bildschirm beschneiden wertZurückweisen"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
