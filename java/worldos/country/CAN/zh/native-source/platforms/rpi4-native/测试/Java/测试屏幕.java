// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 测试屏幕 {
    public static void main(String[] args) {
        中文.内置.屏幕.矩形(400, 400, 20, 20, 0x123456);
        try { 中文.内置.屏幕.矩形(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("屏幕 裁剪 拒绝值"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
