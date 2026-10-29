// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class test_scherm {
    public static void main(String[] args) {
        Nederlands.Eigen.scherm.rechthoek(400, 400, 20, 20, 0x123456);
        try { Nederlands.Eigen.scherm.rechthoek(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("scherm clip weigeren_WAARDE"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
