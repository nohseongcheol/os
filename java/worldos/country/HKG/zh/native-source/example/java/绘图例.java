// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 绘图例 {
    public static void 运行() {
        // 在 640×480 屏幕右侧绘制红、绿、蓝矩形。
        中文.内置.屏幕.矩形(600, 400, 28, 20, 0x0000ff);
        中文.内置.屏幕.矩形(600, 425, 28, 20, 0x00ff00);
        中文.内置.屏幕.矩形(600, 450, 28, 20, 0xff0000);
        中文.内置.输出.写入行("JAVA 그래픽: RGB");
        中文.内置.输出.写入行("Enter");
        中文.内置.屏幕.等待();
    }
}
