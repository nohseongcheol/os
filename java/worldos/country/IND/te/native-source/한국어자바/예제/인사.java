// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] 인수) throws Exception {
        String పాఠ్యము = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path పాత్ = దస్త్రం.పాత్("인사.txt");
        దస్త్రం.వ్రాయుము(పాత్, పాఠ్యము);
        System.out.println(దస్త్రం.చదువు(పాత్));
        Thread పని_మూల్యం = 작업.నడుపుము("인사 작업", () -> System.out.println("작업 థ్రెడ్_మూల్యం అమలు_చేయి_ఆదేశం"));
        작업.기다리기(పని_మూల్యం);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 టెర్మినల్ 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.విండో("다국어 인사", new JLabel(పాఠ్యము), 700, 160));
        }
    }
}
