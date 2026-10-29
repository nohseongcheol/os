// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class PrzykładRysunku {
    public static void Uruchom_2() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        polski.własny.화면.prostokąt(600, 400, 28, 20, 0x0000ff);
        polski.własny.화면.prostokąt(600, 425, 28, 20, 0x00ff00);
        polski.własny.화면.prostokąt(600, 450, 28, 20, 0xff0000);
        polski.własny.pozycja_wyjścia.zapis_linia("JAVA 그래픽: RGB");
        polski.własny.pozycja_wyjścia.zapis_linia("Enter");
        polski.własny.화면.기다리기();
    }
}
