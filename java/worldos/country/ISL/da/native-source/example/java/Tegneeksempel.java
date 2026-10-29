// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Tegneeksempel {
    public static void Kør_2() {
        // 640x480 skærmbillede 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Dansk.eget.skærmbillede.rektangel(600, 400, 28, 20, 0x0000ff);
        Dansk.eget.skærmbillede.rektangel(600, 425, 28, 20, 0x00ff00);
        Dansk.eget.skærmbillede.rektangel(600, 450, 28, 20, 0xff0000);
        Dansk.eget.Udgang.skrive_linje("JAVA 그래픽: RGB");
        Dansk.eget.Udgang.skrive_linje("Enter");
        Dansk.eget.skærmbillede.기다리기();
    }
}
