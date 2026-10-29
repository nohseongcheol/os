// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class thửMànHình {
    public static void main(String[] args) {
        tiếngViệt.tựThân.MànHình.hìnhChữNhật(400, 400, 20, 20, 0x123456);
        try { tiếngViệt.tựThân.MànHình.hìnhChữNhật(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("MànHình cắtXén từChốiGiáTrị"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
