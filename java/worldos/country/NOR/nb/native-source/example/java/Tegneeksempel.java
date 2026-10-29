// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Tegneeksempel {
    public static void Kjør_2() {
        // 640x480 skjermbilde 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        norsk.eget.skjermbilde.rektangel(600, 400, 28, 20, 0x0000ff);
        norsk.eget.skjermbilde.rektangel(600, 425, 28, 20, 0x00ff00);
        norsk.eget.skjermbilde.rektangel(600, 450, 28, 20, 0xff0000);
        norsk.eget.Utgang.skrive_linje("JAVA 그래픽: RGB");
        norsk.eget.Utgang.skrive_linje("Enter");
        norsk.eget.skjermbilde.기다리기();
    }
}
