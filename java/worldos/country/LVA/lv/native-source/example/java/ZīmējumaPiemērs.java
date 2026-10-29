// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ZīmējumaPiemērs {
    public static void Palaist() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Latviešu.savs.화면.taisnstūris(600, 400, 28, 20, 0x0000ff);
        Latviešu.savs.화면.taisnstūris(600, 425, 28, 20, 0x00ff00);
        Latviešu.savs.화면.taisnstūris(600, 450, 28, 20, 0xff0000);
        Latviešu.savs.Izvade.rakstīšana_līnija("JAVA 그래픽: RGB");
        Latviešu.savs.Izvade.rakstīšana_līnija("Enter");
        Latviešu.savs.화면.기다리기();
    }
}
