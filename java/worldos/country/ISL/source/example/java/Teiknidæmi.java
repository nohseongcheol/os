// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Teiknidæmi {
    public static void Keyra_2() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Íslenska.eigin.화면.사각형(600, 400, 28, 20, 0x0000ff);
        Íslenska.eigin.화면.사각형(600, 425, 28, 20, 0x00ff00);
        Íslenska.eigin.화면.사각형(600, 450, 28, 20, 0xff0000);
        Íslenska.eigin.úttak.skrifa_lína("JAVA 그래픽: RGB");
        Íslenska.eigin.úttak.skrifa_lína("Enter");
        Íslenska.eigin.화면.기다리기();
    }
}
