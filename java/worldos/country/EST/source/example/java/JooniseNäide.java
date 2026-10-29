// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class JooniseNäide {
    public static void Käivita_2() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Eesti.oma.화면.ristkülik(600, 400, 28, 20, 0x0000ff);
        Eesti.oma.화면.ristkülik(600, 425, 28, 20, 0x00ff00);
        Eesti.oma.화면.ristkülik(600, 450, 28, 20, 0xff0000);
        Eesti.oma.Väljund.kirjutamine_liin("JAVA 그래픽: RGB");
        Eesti.oma.Väljund.kirjutamine_liin("Enter");
        Eesti.oma.화면.기다리기();
    }
}
