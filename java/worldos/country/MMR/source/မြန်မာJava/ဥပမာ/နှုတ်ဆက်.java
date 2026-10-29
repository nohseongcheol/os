// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import မြန်မာ.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class နှုတ်ဆက် {
    public static void main(String[] အချက်များ) throws Exception {
        String စာသား = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path လမ်း = ဖိုင်.လမ်း("နှုတ်ဆက်.txt");
        ဖိုင်.ရေး(လမ်း, စာသား);
        System.out.println(ဖိုင်.ဖတ်(လမ်း));
        Thread လုပ်စရာတန်ဖိုး = အလုပ်.လုပ်ဆောင်("နှုတ်ဆက် အလုပ်", () -> System.out.println("အလုပ် အလုပ်ကြိုးတန်ဖိုး စက်မောင်း"));
        အလုပ်.စောင့်(လုပ်စရာတန်ဖိုး);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 အဆုံးသုံးမျက်နှာပြင် 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            မျက်နှာပြင်.နောက်မှ(() -> မျက်နှာပြင်.ဝင်း("다국어 နှုတ်ဆက်", new JLabel(စာသား), 700, 160));
        }
    }
}
