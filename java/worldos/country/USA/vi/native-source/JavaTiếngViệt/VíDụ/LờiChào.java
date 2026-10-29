// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class LờiChào {
    public static void main(String[] cácĐốiSố) throws Exception {
        String vănBản = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path đườngDẫn = Tệp.đườngDẫn("LờiChào.txt");
        Tệp.ghi(đườngDẫn, vănBản);
        System.out.println(Tệp.đọc(đườngDẫn));
        Thread giáTrịViệc = TácVụ.chạy("LờiChào TácVụ", () -> System.out.println("TácVụ giáTrịLuồngChạy thựcThiLệnh"));
        TácVụ.đợi(giáTrịViệc);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 thiếtBịCuối 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            MànHình.giáTrịVềSau(() -> MànHình.cửaSổ("다국어 LờiChào", new JLabel(vănBản), 700, 160));
        }
    }
}
