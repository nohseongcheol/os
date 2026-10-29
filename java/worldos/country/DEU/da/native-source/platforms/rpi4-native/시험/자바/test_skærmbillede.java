// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class test_skærmbillede {
    public static void main(String[] args) {
        Dansk.eget.skærmbillede.rektangel(400, 400, 20, 20, 0x123456);
        try { Dansk.eget.skærmbillede.rektangel(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("skærmbillede klippe afvise_VÆRDI"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
