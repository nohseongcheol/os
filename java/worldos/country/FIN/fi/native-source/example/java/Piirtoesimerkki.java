// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Piirtoesimerkki {
    public static void Suorita_2() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        suomi.oma.화면.suorakulmio(600, 400, 28, 20, 0x0000ff);
        suomi.oma.화면.suorakulmio(600, 425, 28, 20, 0x00ff00);
        suomi.oma.화면.suorakulmio(600, 450, 28, 20, 0xff0000);
        suomi.oma.tulostuspaikka.kirjoitus_rivi("JAVA 그래픽: RGB");
        suomi.oma.tulostuspaikka.kirjoitus_rivi("Enter");
        suomi.oma.화면.기다리기();
    }
}
