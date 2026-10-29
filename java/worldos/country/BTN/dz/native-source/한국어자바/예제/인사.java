// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] 인수) throws Exception {
        String བརྟག_ཞིབ = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path འགྲུལ_ལམ = ཡིག_སྣོད.འགྲུལ_ལམ("인사.txt");
        ཡིག_སྣོད.བྲིས(འགྲུལ_ལམ, བརྟག_ཞིབ);
        System.out.println(ཡིག_སྣོད.ལྷག(འགྲུལ_ལམ));
        Thread 일 = 작업.གཡོག_བཀོལ("인사 작업", () -> System.out.println("작업 가닥 실행"));
        작업.기다리기(일);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 ཊར_མི_ནཱལ 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.창("다국어 인사", new JLabel(བརྟག_ཞིབ), 700, 160));
        }
    }
}
