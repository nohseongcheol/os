// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import English.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class Greeting {
    public static void main(String[] arguments) throws Exception {
        String text = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path path = file.path("Greeting.txt");
        file.write(path, text);
        System.out.println(file.read(path));
        Thread workValue = performTask.run("Greeting performTask", () -> System.out.println("performTask threadValue executeCommand"));
        performTask.await(workValue);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            Screen.laterValue(() -> Screen.window("다국어 Greeting", new JLabel(text), 700, 160));
        }
    }
}
