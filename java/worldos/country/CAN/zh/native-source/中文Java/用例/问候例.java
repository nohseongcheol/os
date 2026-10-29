// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 问候例 {
    public static void main(String[] 实参) throws Exception {
        String 文本 = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path 路径 = 文件.路径("问候例.txt");
        文件.写入(路径, 文本);
        System.out.println(文件.读取(路径));
        Thread 工作值 = 任务.运行("问候例 任务", () -> System.out.println("任务 线程值 执行命令"));
        任务.等待(工作值);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 终端 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            屏幕.稍后值(() -> 屏幕.窗口("다국어 问候例", new JLabel(文本), 700, 160));
        }
    }
}
