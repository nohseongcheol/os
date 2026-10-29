// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 日本語.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 挨拶例 {
    public static void main(String[] 引数) throws Exception {
        String 文 = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path 経路 = ファイル.経路("挨拶例.txt");
        ファイル.書込(経路, 文);
        System.out.println(ファイル.読取(経路));
        Thread 作業内容値 = 作業.起動処理("挨拶例 作業", () -> System.out.println("作業 スレッド値 命令実行"));
        作業.待機(作業内容値);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 端末 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            画面.後続値(() -> 画面.窓("다국어 挨拶例", new JLabel(文), 700, 160));
        }
    }
}
