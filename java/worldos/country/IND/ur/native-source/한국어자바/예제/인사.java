// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import اردو.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] دلائل) throws Exception {
        String متن = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path راستہ_2 = فائل_کا_نام.راستہ_2("인사.txt");
        فائل_کا_نام.لکھیں(راستہ_2, متن);
        System.out.println(فائل_کا_نام.پڑھیں(راستہ_2));
        Thread 일 = 작업.چلائیں("인사 작업", () -> System.out.println("작업 تھریڈ_قدر نفاذ_کریں_حکم"));
        작업.기다리기(일);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 حکم_کی_تشریح_کرنے_والا 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.ونڈو("다국어 인사", new JLabel(متن), 700, 160));
        }
    }
}
