// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class test_skärmbild {
    public static void main(String[] args) {
        Svenska.eget.skärmbild.rektangel(400, 400, 20, 20, 0x123456);
        try { Svenska.eget.skärmbild.rektangel(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("skärmbild klipp avvisa_värde"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
