// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 問候例 {
    public static void main(String[] 實參) throws Exception {
        String 文本 = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path 路徑 = 檔案.路徑("問候例.txt");
        檔案.寫入(路徑, 文本);
        System.out.println(檔案.讀取(路徑));
        Thread 工作值 = 任務.運行("問候例 任務", () -> System.out.println("任務 執行緒值 執行命令"));
        任務.等待(工作值);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 終端 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            屏幕.稍後值(() -> 屏幕.窗口("다국어 問候例", new JLabel(文本), 700, 160));
        }
    }
}
