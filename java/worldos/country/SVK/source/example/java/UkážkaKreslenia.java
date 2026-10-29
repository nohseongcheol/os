// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class UkážkaKreslenia {
    public static void Spustiť_2() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Slovenský.vlastné.화면.obdĺžnik(600, 400, 28, 20, 0x0000ff);
        Slovenský.vlastné.화면.obdĺžnik(600, 425, 28, 20, 0x00ff00);
        Slovenský.vlastné.화면.obdĺžnik(600, 450, 28, 20, 0xff0000);
        Slovenský.vlastné.Výstup.zapísať_linka("JAVA 그래픽: RGB");
        Slovenský.vlastné.Výstup.zapísať_linka("Enter");
        Slovenský.vlastné.화면.기다리기();
    }
}
