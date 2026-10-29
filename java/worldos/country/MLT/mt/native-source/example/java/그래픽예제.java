// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 그래픽예제 {
    public static void serje() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Malti.자체.화면.사각형(600, 400, 28, 20, 0x0000ff);
        Malti.자체.화면.사각형(600, 425, 28, 20, 0x00ff00);
        Malti.자체.화면.사각형(600, 450, 28, 20, 0xff0000);
        Malti.자체.출력.kiteb_linja("JAVA 그래픽: RGB");
        Malti.자체.출력.kiteb_linja("Enter");
        Malti.자체.화면.기다리기();
    }
}
