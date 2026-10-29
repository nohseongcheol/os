// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 画面試験 {
    public static void main(String[] args) {
        日本語.内蔵.画面.矩形(400, 400, 20, 20, 0x123456);
        try { 日本語.内蔵.画面.矩形(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("画面 切抜き 値却下"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
