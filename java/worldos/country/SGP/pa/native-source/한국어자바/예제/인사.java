// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ਪੰਜਾਬੀ.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception {
        String ਟੈਕਸਟ = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ਮਾਰਗ = ਫਾਇਲ.ਮਾਰਗ("인사.txt");
        ਫਾਇਲ.ਲਿਖਣ(ਮਾਰਗ, ਟੈਕਸਟ);
        System.out.println(ਫਾਇਲ.ਪੜ੍ਹਨ(ਮਾਰਗ));
        Thread 일 = 작업.ਚਲਾਓ_2("인사 작업", () -> System.out.println("작업 ਥ੍ਰੈਡ_ਕੀਮਤ ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼"));
        작업.기다리기(일);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 ਟਰਮੀਨਲ 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.ਵਿੰਡੋ("다국어 인사", new JLabel(ਟੈਕਸਟ), 700, 160));
        }
    }
}
