// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 繪圖例 {
    public static void 運行() {
        // 在 640×480 畫面右側繪製紅、綠、藍矩形。
        中文.內建.屏幕.矩形(600, 400, 28, 20, 0x0000ff);
        中文.內建.屏幕.矩形(600, 425, 28, 20, 0x00ff00);
        中文.內建.屏幕.矩形(600, 450, 28, 20, 0xff0000);
        中文.內建.輸出.寫入行("JAVA 그래픽: RGB");
        中文.內建.輸出.寫入行("Enter");
        中文.內建.屏幕.等待();
    }
}
