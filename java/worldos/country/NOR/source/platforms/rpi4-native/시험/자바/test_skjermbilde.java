// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class test_skjermbilde {
    public static void main(String[] args) {
        norsk.eget.skjermbilde.rektangel(400, 400, 20, 20, 0x123456);
        try { norsk.eget.skjermbilde.rektangel(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("skjermbilde klippe avvise_VERDI"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
